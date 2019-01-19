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

  // ground this to reset the machine
  inout wire arc_RESET,

  // connections to archimedes motherboard
  inout wire [31:0] rom_D,  // ARM data bus
  input wire [19:0] rom_A,  // LA21:2
  input wire rom_nCS,       // MEMC Romcs*

  // connections to two flash chips
  output wire [21:0] flash_A,
  inout wire [15:0] flash0_DQ,
  inout wire [15:0] flash1_DQ,
  output wire flash_nCE,
  output wire flash_nOE,
  output wire flash_nWE,

  // possible clocks (unused)
  input wire cpld_clock_from_mcu,
  input wire cpld_clock_osc,  // PHI1 from a flying lead
  
  // SPI connection to MCU
  input wire cpld_MOSI,
  input wire cpld_SS,
  input wire cpld_SCK,
  output reg cpld_MISO = 1'b1
);


// width of the buffer used to communicate between the ARM and MCU; requires 2x this in registers
parameter comms_buffer_width = 8;

reg [comms_buffer_width-1:0] mcu_to_arm_buffer;
reg mcu_to_arm_write_state = 1'b0;  // toggles when cpld receives byte from MCU
reg mcu_to_arm_write_state_sync = 1'b0;  // synchronized to cpld_clock_osc (ARM phi1)
reg mcu_to_arm_read_state = 1'b0;  // toggles when ARM reads byte from buffer
reg mcu_to_arm_read_state_sync = 1'b0;  // synchronized to cpld_SCK

reg [comms_buffer_width-1:0] arm_to_mcu_buffer;
reg arm_to_mcu_write_state = 1'b0;  // toggles when cpld receives byte from ARM
reg arm_to_mcu_write_state_sync = 1'b0;  // synchronized to cpld_SCK
reg arm_to_mcu_read_state = 1'b0;  // toggles when MCU reads byte from buffer
reg arm_to_mcu_read_state_sync = 1'b0;  // synchronized to cpld_clock_osc (ARM phi1)


// 1 to pass host accesses through to the flash, 0 to control flash from SPI
reg allowing_arm_access = 1'b1;

// 1 to use rom_A[19] (LA21) and provide 4MB of flash, 0 to ignore it and provide 2MB
reg use_la21 = 1'b0;

// Flash bank selected; bit 0 is ignored if use_la21==1
reg [2:0] flash_bank = 3'b0;

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

// set to 1 to reset the ARM, 0 to let it run
reg reset_arm = 1'b0;


// 1 when rom_A is pointing at the top 2048 bytes (512 words) of ROM
wire accessing_signal_ROM;
assign accessing_signal_ROM = (rom_A[18:11] == 8'b11111111) ? 1'b1 : 1'b0;


// synchronizer for romcs*
reg [1:0] romcs_sync = 2'b0;
// pulse length measurement for romcs*
reg [2:0] romcs_pulse_length = 3'b0;

always @(posedge cpld_clock_from_mcu) begin
  romcs_sync <= {romcs_sync[0], rom_nCS};
  if (romcs_sync[1] == 1'b1) begin
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
        if (rom_A[10] == 1'b0) begin
          // ARM is writing data for the MCU
        end else begin
          // ARM is reading data from the MCU
        end
      end
    end
  end
end


// ARM reset line; open collector
assign arc_RESET = reset_arm == 1'b1 ? 1'b0 : 1'bZ;
//assign arc_RESET = romcs_sync[1]; // DEBUG: synchronized romcs
//assign arc_RESET = clock_divider[0]; // DEBUG
//assign arc_RESET = cpld_clock_from_mcu; // DEBUG
//assign arc_RESET = cpld_SCK; // DEBUG


// ARM data bus
assign rom_D = rom_nCS == 1'b1 ? 32'bZ : (
  allowing_arm_access == 1'b1 ? (
    // Pass flash output through to rom_D
    {flash1_DQ, flash0_DQ}
  ) : (
    // allowing_arm_access == 1'b0; we can't handle a flash access now

    // The intention below was to make all ROM reads return "mov pc, #0x3400000" (32'he3a0f50d)
    // during programming, so the system might jump to the start of the ROM
    // afterward.  It didn't seem to do anything though, so I've removed it.
    // 32'hE3A0F50E  // mov pc, #0x3800000
    32'hE3A0F000  // mov pc, #0
    // 32'bZ
  )
);

// Flash chip address lines
assign flash_A = allowing_arm_access == 1'b1 ? (
    // If LA21 is connected, use top two bits of flash_bank and LA21:2.
    // If disconnected, use three bits of flash_bank and LA20:2.
    use_la21 == 1'b1 ? {flash_bank[2:1], rom_A} : {flash_bank, rom_A[18:0]}
  ) : (
    spi_A
  );

// Flash chip data lines
assign flash0_DQ = allowing_arm_access == 1'b1 ? 16'bZ : (accessing_flash == 1'b1 && spi_rnw == 1'b0 ? spi_D[15:0] : 16'bZ);
assign flash1_DQ = allowing_arm_access == 1'b1 ? 16'bZ : (accessing_flash == 1'b1 && spi_rnw == 1'b0 ? spi_D[31:16] : 16'bZ);

// Flash chip control lines
assign flash_nCE = allowing_arm_access == 1'b1 ? rom_nCS : (accessing_flash == 1'b1 ? 1'b0 : 1'b1);
assign flash_nOE = allowing_arm_access == 1'b1 ? rom_nCS : (accessing_flash == 1'b1 && spi_rnw == 1'b1 ? 1'b0 : 1'b1);
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
      // $display("SPI: Set allowing_arm_access to %d", cpld_MOSI);
    end else if (allowing_arm_access == 1) begin
      // allowing ARM access: rest of SPI transaction is a control message
      if (spi_bit_count < 8) begin
        flash_bank <= {flash_bank[1:0], cpld_MOSI};
      end else if (spi_bit_count == 8) begin
        use_la21 <= cpld_MOSI;
      end else if (spi_bit_count == 9) begin
        reset_arm <= cpld_MOSI;
      end else if (spi_bit_count == 12) begin
        // mcu has data for me
      end else if (spi_bit_count == 13) begin
        // mcu has buffer space for me to transmit
      end else if (spi_bit_count == 14) begin
        // send: i have data for mcu
      end else if (spi_bit_count == 15) begin
        // send: i have buffer space for mcu
      end else if (spi_bit_count < 24) begin
        mcu_to_arm_buffer <= {mcu_to_arm_buffer[comms_buffer_width-2:0], cpld_MOSI};
      end
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
  if (spi_bit_count < 32) begin
    cpld_MISO <= spi_bit_count[0];  // should toggle and result in data & ffffe00 == 55554000
  end else begin
    cpld_MISO <= spi_D[31];
  end
end


endmodule
