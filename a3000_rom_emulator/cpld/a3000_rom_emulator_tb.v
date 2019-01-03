// Copyright 2018 Google LLC
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


`timescale 1ns/100ps
`include "a3000_rom_emulator.v"

`define assert(condition, message) if(!(condition)) begin $display(message); $finish(1); end

module a3000_rom_emulator_tb;

  // test clock
  reg clk;

  // inputs to the module under test
  wire [31:0] arm_D;  // inout, but we only care about it when it's an output
  reg [19:0] arm_A = 16'b0;  // driven by ARM

  // outputs from the module under test
  wire [21:0] flash_A;
  wire [31:0] flash_D;
  wire flash_nCE;
  wire flash_nOE;
  wire flash_nWE;

  // test spi feeder
  reg spi_ss = 1'b1;
  reg spi_sck = 1'b0;
  reg spi_mosi = 1'b0;
  wire spi_miso;

  reg [63:0] spi_shift;
  reg [63:0] spi_d;
  reg spi_start = 0; // drive this high for one clk pulse to start an spi transaction
  reg [6:0] spi_count;

  // module under test
  a3000_rom_emulator dut(
    .arc_RESET(arc_RESET),
    .rom_D(arm_D),
    .rom_A(arm_A),
    .rom_nCS(rom_nCS),
    .flash_A(flash_A),
    .flash0_DQ(flash_D[15:0]),
    .flash1_DQ(flash_D[31:16]),
    .flash_nCE(flash_nCE),
    .flash_nOE(flash_nOE),
    .flash_nWE(flash_nWE),
    .cpld_clock_from_mcu(cpld_clock_from_mcu),
    .cpld_clock_osc(cpld_clock_osc),
    .cpld_MOSI(spi_mosi),
    .cpld_SS(spi_ss),
    .cpld_SCK(spi_sck),
    .cpld_MISO(spi_miso)
  );

  // clock driver
  initial begin
    clk = 1'b0;
    forever #9 clk = ~clk;
  end

  // spi process
  always @(posedge clk) begin
    if (spi_start == 1'b1) begin
      $display("- start SPI transaction with spi_d=%x", spi_d);
      spi_ss <= 1'b0;
      spi_count <= 7'd64;
      spi_mosi <= spi_d[63]; // first bit
      spi_shift <= {spi_d[62:0], 1'b0};
      spi_sck <= 1'b0;
    end else if (spi_ss == 1'b0) begin
      if (spi_count == 0) begin
        $display("- end SPI transaction with spi_shift=%x (arm acc %x, rnw %x, A %x, wdata %x, rdata %x)",
          spi_shift, spi_shift[63], spi_shift[62], spi_shift[61:40], spi_shift[39:8], spi_shift[31:0]);
        spi_ss <= 1'b1; // end of transaction
      end else if (spi_sck == 1'b0) begin
        spi_sck <= 1'b1;
      end else begin
        // mid-transaction
        spi_mosi <= spi_shift[63];
        spi_shift <= {spi_shift[62:0], spi_miso};
        spi_count <= spi_count - 1;
        spi_sck <= 1'b0;
      end;
    end
  end

  always @(negedge dut.allowing_arm_access) begin
    $display("disallowing ARM access");
  end

  always @(posedge dut.allowing_arm_access) begin
    $display("allowing ARM access");
  end

  always @(negedge flash_nOE) begin
    $display("flash_nOE low with flash_A=%x", flash_A);
  end

  // flash fixture always reads 0x42
  assign D = (flash_nOE == 1'b0) ? 8'h42 : 8'hZZ;

  always @(posedge flash_nOE) begin
    $display("flash_nOE high with flash_A=%x", flash_A);
  end

  always @(negedge flash_nWE) begin
    $display("flash_nWE low with flash_A=%x and flash_D=%x", flash_A, flash_D);
  end

  always @(posedge flash_nWE) begin
    $display("flash_nWE high with flash_A=%x and flash_D=%x", flash_A, flash_D);
  end

  initial begin

    $display("running a3000_rom_emulator_tb");

    $dumpfile("a3000_rom_emulator_tb.vcd");
    $dumpvars(0, a3000_rom_emulator_tb);

    $display("start");
    repeat(10) @(posedge clk);

    // check that we start out letting the ARM control the flash
    `assert(dut.allowing_arm_access == 1'b1, "FAIL: not allowing ARM access initially");

    $display("\nSetting arm_A to 12345");
    arm_A <= 17'h12345;

    $display("\nTEST that 7fffffffffffffff disables ARM access");
    spi_d <= 64'h7fffffffffffffff;
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    @(posedge clk);
    `assert(dut.allowing_arm_access == 1'b0, "FAIL: ffffff00 didn't disable ARM access");

    $display("\nTEST that ffffffffffffffff reenables ARM access");
    spi_d <= 64'hffffffffffffffff;
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    @(posedge clk);
    `assert(dut.allowing_arm_access == 1'b1, "FAIL: 32 1's didn't reenable ARM access");

    $display("\nTEST that we can write to the flash (51234)");
    // message format for a WRITE: acc, rnw, a[22], d[32], 8'b0
    // with the write happening during the six zeros
    spi_d <= {1'b0, 1'b0, 22'b1010001001000110100, 32'h12345678, 8'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    `assert(dut.allowing_arm_access == 1'b0, "FAIL: write operation unlocked ARM access");

    $display("\nTEST that we can read from the flash (70f0f)");
    // message format for a WRITE: acc, rnw, a[22], 8'b0, d[32]
    // with the data byte returned in the final 8 bits
    spi_d <= {1'b0, 1'b1, 22'b1110000111100001111, 40'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    `assert(dut.allowing_arm_access == 1'b0, "FAIL: write operation unlocked ARM access");

    $display("\nTEST that the unlock process appears correct");
    spi_d <= {19'h5555, 1'b0, 8'hAA, 4'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    spi_d <= {19'h2AAA, 1'b0, 8'h55, 4'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    spi_d <= {19'h5555, 1'b0, 8'h90, 4'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    spi_d <= {19'h0, 1'b1, 12'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    spi_d <= {19'h1, 1'b1, 12'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    spi_d <= {19'h5555, 1'b0, 8'hF0, 4'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);

    $display("^^^ expect write 5555, write 2AAA, write 5555, read 0, read 1, write 5555");

    // finish off
    $display("running out the clock");
    repeat(1000) @(posedge clk);

    $display("PASS");

    $finish;

  end

endmodule
