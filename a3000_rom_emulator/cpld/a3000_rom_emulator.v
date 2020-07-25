// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


// Verilog for the XC95144XL chip onboard an a3000_rom_emulator board.

// This connects to the host machine pins (rom_A, rom_nCS, rom_D), most flash
// signals (flash_A, flash0_DQ, flash1_DQ, flash_nCE, flash_nOE, flash_nWE --
// flash_nREADY and flash_nRESET are driven by the on-board microcontroller),
// and the SPI port on the microcontroller (cpld_{MOSI, SS, SCK, MISO}).

// In normal operation (allowing_arm_access==1), rom_A is simply passed
// through to flash_A, with rom_nCS driving both flash_nCE and flash_nOE (with
// flash_nWE==1).  rom_D is tristated when rom_nCS == 1, and flash_{0, 1}_DQ
// are passed through to rom_D when rom_nCS == 0.

// When the microcontroller wants to take over, it drives an 8-byte SPI
// transaction:

// read: <allowing_arm_access> 1 <A x 22> <0 x 40> -- data returned in final 32 bits

// write: <allowing_arm_access> 0 <A x 22> <data x 32> <0 x 8>

// If allowing_arm_access == 1, the read or write will be ignored, and all the
// transaction will do is give access to the flash back to the host machine.


module a3000_rom_emulator(

  // connections to archimedes motherboard
  inout wire [31:0] rom_D,  // ARM data bus
  input wire [19:0] rom_A,  // LA21:2
  input wire rom_nCS,       // MEMC Romcs*
  input wire rom_nOE,       // Lionrw (latched IO nR/W) on a Risc PC, debug everywhere else

  // connections to two flash chips
  output wire [21:0] flash_A,
  inout wire [15:0] flash0_DQ,
  inout wire [15:0] flash1_DQ,
  output wire flash_nCE,
  output wire flash_nOE,
  output wire flash_nWE,

  // 48MHz clock
  input wire cpld_clock_from_mcu,

  // 5V line from ROM socket, used to attempt to detect if the host machine is
  // powered. Unreliable, so it's safest to just not fit D2, which ensures
  // that the CPLD is only ever powered from rom_5V and prevents the board
  // from attempting to power the host system if something goes wrong.
  input wire rom_5V,

  // SPI connection to MCU
  input wire cpld_MOSI,  // doubles as serial RXD when cpld_SS=1
  input wire cpld_SS,
  input wire cpld_SCK,
  output wire cpld_MISO  // doubles as serial TXD when cpld_SS=1
);

// set to 1 for v2 boards and v1 with Risc PC adapter
parameter use_output_enable_signal_from_host = 1;
wire host_output_enable;
assign host_output_enable = use_output_enable_signal_from_host ? rom_nOE : 1'b0;

// set to 1 once the power signal has been wired to rom_5V
parameter use_power_signal_from_host = 1;
wire host_power_on;
assign host_power_on = use_power_signal_from_host ? rom_5V : 1'b1;


// ----- ARM-MCU comms with handshaking -- better than bit-banged serial, but won't fit in XC95144) -----

// enable/disable arm-mcu comms
parameter enable_comms = 0;

// width of the buffer used to communicate between the ARM and MCU; requires 2x this in registers.
parameter comms_buffer_width = 1;

reg [comms_buffer_width-1:0] mcu_to_arm_buffer;
reg mcu_to_arm_write_state = 1'b0;  // toggles when cpld receives byte from MCU
reg mcu_to_arm_write_state_sync = 1'b0;  // synchronized to cpld_clock_from_mcu (48MHz)
reg mcu_to_arm_read_state = 1'b0;  // toggles when ARM reads byte from buffer
reg mcu_to_arm_read_state_sync = 1'b0;  // synchronized to cpld_SCK

reg [comms_buffer_width-1:0] arm_to_mcu_buffer;
reg arm_to_mcu_write_state = 1'b0;  // toggles when cpld receives byte from ARM
reg arm_to_mcu_write_state_sync = 1'b0;  // synchronized to cpld_SCK
reg arm_to_mcu_read_state = 1'b0;  // toggles when MCU reads byte from buffer
reg arm_to_mcu_read_state_sync = 1'b0;  // synchronized to cpld_clock_from_mcu (48MHz)


// ----- Hacky bit-banged serial comms; actually works but requires more work on ARM side -----

// enable/disable hacky bit banged serial comms
parameter enable_bitbang_serial = !enable_comms;

// for bit-banged serial comms
reg cpld_TXD_sync = 1'b1;  // synchronized to rom_nCS falling edge
reg cpld_MISO_TXD = 1'b1;  // value to assign to cpld_MISO when cpld_SS==1


// ---- SPI registers -----

// SPI MISO output
reg cpld_MISO_int = 1'b1;  // MISO when cpld_SS==0

// counts up to 63
reg [5:0] spi_bit_count = 6'b0;

// 1 if the SPI transaction is a read, 0 for a write
reg spi_rnw = 1'b1;

// Address value in SPI transaction
reg [21:0] spi_A = 22'b0;

// Data value in SPI transaction
reg [31:0] spi_D = 32'b0;

// 1 when an SPI transaction wants flash_nCE low (and flash_nOE for reads)
reg accessing_flash = 1'b0;

// 1 when an SPI transaction wants flash_nWE low
reg writing_flash = 1'b0;


// ----- Config registers -----
// 1 to pass host accesses through to the flash, 0 to control flash from SPI
reg allowing_arm_access = 1'b1;

// 1 to use rom_A[19] (LA21) and provide 4MB of flash, 0 to ignore it and provide 2MB
reg use_la21 = 1'b0;

// 1 to use rom_A[18] (LA20) for a 2+MB bank, 0 for a 1MB bank
reg use_la20 = 1'b1;

// Flash bank selected; bit 1 is ignored if use_la21==1, bit 0 is ignored if use_la20==1
reg [3:0] flash_bank = 4'b0;

// set to 1 to reset the ARM, 0 to let it run
reg reset_arm = 1'b0;


// ----- Read-sensitive ROM locations -----

// 1 when rom_A is pointing at the top 16 bytes (4 words) of ROM
wire accessing_signal_ROM;
assign accessing_signal_ROM = (
    rom_A[18:2] == 17'b11111111111111111
    && (use_la21 == 1'b0 || rom_A[19] == 1'b1)
  ) ? 1'b1 : 1'b0;  // TODO this can prob be 18:2==17'b1...1 because we only need 2 bits

// synchronize mcu-to-arm signals when romcs goes active.
// any metastability should settle by the time these values are read.
always @(negedge rom_nCS) begin
  mcu_to_arm_write_state_sync <= mcu_to_arm_write_state;
  arm_to_mcu_read_state_sync <= arm_to_mcu_read_state;
  if (enable_bitbang_serial) begin
    // synchronize MOSI / TXD
    cpld_TXD_sync <= cpld_MOSI;
  end
end

// synchronizer for romcs*
`define DOUBLE_SYNC_ROMCS
reg romcs_sync = 0;
`ifdef DOUBLE_SYNC_ROMCS
  reg romcs_pre_sync = 0;
`endif
// pulse length measurement for romcs*
reg [2:0] romcs_pulse_length = 3'b0;

always @(posedge cpld_clock_from_mcu) begin

  // Synchronize Romcs*
  `ifdef DOUBLE_SYNC_ROMCS
    {romcs_sync, romcs_pre_sync} <= {romcs_pre_sync, rom_nCS};
  `else
    romcs_sync <= rom_nCS;
  `endif
  if (romcs_sync == 1'b1) begin
    romcs_pulse_length <= 3'b0;
  end else begin
    if (romcs_pulse_length != 3'b111) begin
      // don't allow the counter to wrap
      romcs_pulse_length <= romcs_pulse_length + 1;
    end
    if (romcs_pulse_length == 3'b110) begin
      // pulse length of synchronized romcs = 6, which means
      // we're about 180 ns into the pulse, and safely past
      // the point where MEMC might change its mind and
      // bring romcs* high again.

      // see if rom_A is pointing at the last 2kB of ROM, i.e.
      // the last 512 words.  rom_A[9:2] contain a data byte
      // for us, and rom_A[10] is RnW.
      if (accessing_signal_ROM == 1'b1) begin
        if (rom_A[1] == 1'b0) begin
          if (enable_comms) begin
            // ARM is writing data for the MCU
            arm_to_mcu_buffer <= rom_A[comms_buffer_width+1:2];
            arm_to_mcu_write_state <= !arm_to_mcu_write_state;
          end
          if (enable_bitbang_serial) begin
            cpld_MISO_TXD <= rom_A[0];
          end
        end else begin
          if (enable_comms) begin
            // ARM is reading data from the MCU
            mcu_to_arm_read_state <= !mcu_to_arm_read_state;
          end
        end
      end
    end
  end
end


// latched nR/W (Lionrw) on a Risc PC, debug everywhere else
// (see use_output_enable_signal_from_host above)
// assign rom_nOE = 1'bZ;
// assign rom_nOE = cpld_TXD_sync;  // DEBUG: bit-banged serial
// assign rom_nOE = cpld_MOSI;  // DEBUG: bit-banged serial
// assign rom_nOE = cpld_MISO_TXD;  // DEBUG: bit-banged serial
// assign rom_nOE = romcs_sync[1]; // DEBUG: synchronized romcs
// assign rom_nOE = clock_divider[0]; // DEBUG
// assign rom_nOE = cpld_clock_from_mcu; // DEBUG
// assign rom_nOE = cpld_SCK; // DEBUG


wire n_selected;  // Romcs* low and power high
assign n_selected = (rom_nCS == 1'b0 && host_power_on == 1'b1 && host_output_enable == 1'b0) ? 1'b0 : 1'b1;

// ARM data bus
assign rom_D = n_selected == 1'b1 ? 32'bZ : (
  allowing_arm_access == 1'b1 ? (
    // Pass flash output through to rom_D
    // DEBUG actually should be mcu_to_arm_buffer, but this lets us loopback
    (accessing_signal_ROM == 1'b1 && rom_A[1] == 1'b1) ? {
      enable_bitbang_serial ? {flash1_DQ, flash0_DQ[15:1], cpld_TXD_sync}
      : (enable_comms ? {flash1_DQ, flash0_DQ[15:3], mcu_to_arm_write_state_sync, arm_to_mcu_read_state_sync, mcu_to_arm_buffer}
                      : {flash1_DQ, flash0_DQ})
    } :
    {flash1_DQ, flash0_DQ}
  ) : (
    // allowing_arm_access == 1'b0; we can't handle a flash access now

    // The intention below was to make all ROM reads return "mov pc, #0x3400000" (32'he3a0f50d)
    // during programming, so the system might jump to the start of the ROM
    // afterward.  It didn't seem to do anything though, so I've removed it.
    // 32'hE3A0F50E  // mov pc, #0x3800000
    // 32'hE3A0F000  // mov pc, #0
    32'bZ
  )
);

// Flash chip address lines
assign flash_A = allowing_arm_access == 1'b1 ? (
    // If LA21 is connected, use top two bits of flash_bank and LA21:2.
    // If disconnected, use three bits of flash_bank and LA20:2.
    // use_la21 == 1'b1 ? {flash_bank[2:1], rom_A} : {flash_bank, rom_A[18:0]}
    {
      flash_bank[3:2],
      (use_la21 == 1'b1 ? rom_A[19] : flash_bank[1]),
      (use_la20 == 1'b1 ? rom_A[18] : flash_bank[0]),
      rom_A[17:0]
    }
  ) : (
    spi_A
  );

// Flash chip data lines
assign flash0_DQ = allowing_arm_access == 1'b1 ? 16'bZ : (accessing_flash == 1'b1 && spi_rnw == 1'b0 ? spi_D[15:0] : 16'bZ);
assign flash1_DQ = allowing_arm_access == 1'b1 ? 16'bZ : (accessing_flash == 1'b1 && spi_rnw == 1'b0 ? spi_D[31:16] : 16'bZ);

// Flash chip control lines
assign flash_nCE = allowing_arm_access == 1'b1 ? n_selected : (accessing_flash == 1'b1 ? 1'b0 : 1'b1);
assign flash_nOE = allowing_arm_access == 1'b1 ? n_selected : (accessing_flash == 1'b1 && spi_rnw == 1'b1 ? 1'b0 : 1'b1);
assign flash_nWE = allowing_arm_access == 1'b1 ? 1'b1 : (writing_flash == 1'b1 ? 1'b0 : 1'b1);


always @(posedge cpld_SCK or posedge cpld_SS) begin

  if (cpld_SS == 1'b1) begin
    accessing_flash <= 1'b0;
    spi_bit_count <= 6'b0;
  end else begin
    // $display("\nSPI tick!  mosi=%d", cpld_MOSI);
    // the master device should bring cpld_SS high between every transaction.

    // SPI is big-endian; send the MSB first and clock into the LSB.

    // Address to output delay is 70ns for a read, and /CE can be raised
    // straight away after. With a 24MHz (42ns) SPI clock plus transit delays,
    // that means three clocks to be safe:

    // t=0: Set up address and drop /CE and /OE
    // t=2ck: Read data, raise /CE and /OE

    // For writes, the cycle time is 60ns, write pulse width is 25ns, write
    // pulse high is 20ns, and address hold time is 45ns.  Ideally four clocks:

    // t=0: Set up address and data and drop /CE
    // t=1ck: Drop /WR
    // t=2ck: Raise /WR
    // t=3ck: Raise /CE

    // So for reads:   0=arm 1=rnw 2-23=A 24-31=0 32-63=data (setting up A from 2-23, reading at 31)
    // And for writes: 0=arm 1=rnw 2-23=A 24-55=data 56-63=0 (setting up A and D from 2-55, /CE low from 56-59, /WR low from 57-58)

    if (spi_bit_count == 0) begin
      allowing_arm_access <= cpld_MOSI;
      arm_to_mcu_write_state_sync <= arm_to_mcu_write_state;
      mcu_to_arm_read_state_sync <= mcu_to_arm_read_state;
      // $display("SPI: Set allowing_arm_access to %d", cpld_MOSI);
    end else if (allowing_arm_access == 1) begin
      // allowing ARM access: rest of SPI transaction (one byte) is a control message
      // bit 1: reset_arm
      // bit 2: use_la21
      // bit 3: use_la20
      // bit 4-7: flash_bank
      reset_arm <= use_la21;
      use_la21 <= use_la20;
      use_la20 <= flash_bank[3];
      flash_bank <= {flash_bank[2:0], cpld_MOSI};
      // Macrocells Used Pterms Used Registers Used  Pins Used Function Block Inputs Used
      // 142/144  (99%)  459/720  (64%)  79/144  (55%) 117/117  (100%) 319/432  (74%)
      // if (spi_bit_count < 8) begin
      //   flash_bank <= {flash_bank[1:0], cpld_MOSI};
      // end else if (spi_bit_count == 8) begin
      //   use_la21 <= cpld_MOSI;
      // end else if (spi_bit_count == 9) begin
      //   reset_arm <= cpld_MOSI;
      // end else if (spi_bit_count == 12) begin
      //   if (enable_comms) begin
      //     // mcu has data for me
      //     mcu_to_arm_write_state <= cpld_MOSI;
      //     spi_D[31] <= arm_to_mcu_write_state;  // HACK: 41.6ns to resolve metastability
      //     // TODO toggle write state rather than copy
      //   end
      // end else if (spi_bit_count == 13) begin
      //   if (enable_comms) begin
      //     // mcu has buffer space for me to transmit
      //     arm_to_mcu_read_state <= cpld_MOSI;
      //     // TODO toggle read state rather than copy
      //     spi_D[31] <= mcu_to_arm_read_state;  // HACK: 41.6ns to resolve metastability
      //   end
      // end else if (spi_bit_count == 14) begin
      //   if (enable_comms) begin
      //     // data bit from mcu
      //     // TODO only replace if there's room
      //     // (can dispense with this if we really need the space)
      //     mcu_to_arm_buffer <= {cpld_MOSI};
      //     spi_D[31] <= arm_to_mcu_buffer[0];  // HACK: 41.6ns to resolve metastability
      //   end
      // end
    end else begin
      // not allowing ARM access: rest of SPI transaction is a flash access request
      if (spi_bit_count == 1) begin
        spi_rnw <= cpld_MOSI;
      end else if (spi_bit_count < 24) begin  // 22 bit address in spi bits 2-23
        spi_A <= {spi_A[20:0], cpld_MOSI};
      end else if (spi_rnw == 1'b1) begin
        // FLASH READ
        // 24-31=0 32-63=data (setting up A from 2-23, /CE+/OE low at 24,reading at 31)
        if (spi_bit_count == 24) begin
          // start read
          accessing_flash <= 1'b1;
        end else if (spi_bit_count == 31) begin
          // end read
          spi_D <= {flash1_DQ, flash0_DQ};
          accessing_flash <= 1'b0;
        end else if (spi_bit_count >= 32) begin
          spi_D <= {spi_D[30:0], 1'b0};
        end
      end else if (spi_rnw == 1'b0) begin
        // FLASH WRITE
        // 24-55=data 56-63=0 (setting up A and D from 2-55, /CE low from 56-59, /WR low from 57-58)
        if (spi_bit_count < 56) begin
          spi_D <= {spi_D[30:0], cpld_MOSI};
        end
        if (spi_bit_count == 56) begin
          accessing_flash <= 1'b1;
        end
        if (spi_bit_count == 57) begin
          writing_flash <= 1'b1;
        end
        if (spi_bit_count == 58) begin
          writing_flash <= 1'b0;
        end
        if (spi_bit_count == 59) begin
          accessing_flash <= 1'b0;
        end
      end
    end
    spi_bit_count <= spi_bit_count + 1;
  end
end

always @(negedge cpld_SCK) begin
  cpld_MISO_int <= spi_D[31];
  if (enable_comms) begin
    if (spi_bit_count == 12) begin
      // we have data for mcu
      // cpld_MISO <= arm_to_mcu_write_state_sync;
      // TODO toggle write state rather than copy
    end else if (spi_bit_count == 13) begin
      // we have buffer space for mcu to transmit
      // cpld_MISO <= mcu_to_arm_read_state_sync;
      // TODO toggle read state rather than copy
    end else if (spi_bit_count == 14) begin
      // data bit from arm
      // TODO only replace if there's room
      // (can dispense with this if we really need the space)
      // cpld_MISO <= arm_to_mcu_buffer[0];
    end
  end
end

// output cpld_MISO_TXD when cpld_SS==1 and the bit-banged serial port is enabled
assign cpld_MISO = (enable_bitbang_serial && cpld_SS == 1'b1) ? cpld_MISO_TXD : cpld_MISO_int;


endmodule
