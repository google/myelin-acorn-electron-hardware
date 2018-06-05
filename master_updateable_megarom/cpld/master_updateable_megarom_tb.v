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
`include "master_updateable_megarom.v"

`define assert(condition, message) if(!(condition)) begin $display(message); $finish(1); end

module master_updateable_megarom_tb;

  // test clock
  reg clk;

  // inputs to the module under test
  wire [7:0] D;  // inout, but we only care about it when it's an output
  reg [16:0] bbc_A = 16'b0;  // driven by BBC
  reg [1:0] cpld_JP = 2'b00;  // driven externally

  // outputs from the module under test
  wire [18:0] flash_A;
  wire flash_nOE;
  wire flash_nWE;

  // test spi feeder
  reg spi_ss = 1'b1;
  reg spi_sck = 1'b0;
  reg spi_mosi = 1'b0;
  wire spi_miso;

  reg [31:0] spi_shift;
  reg [31:0] spi_d;
  reg spi_start = 0; // drive this high for one clk pulse to start an spi transaction
  reg [5:0] spi_count;

  // module under test
  master_updateable_megarom dut(
    .D(D),
    .bbc_A(bbc_A),
    .flash_A(flash_A),
    .flash_nOE(flash_nOE),
    .flash_nWE(flash_nWE),
    .cpld_SCK_in(spi_sck),
    .cpld_MOSI(spi_mosi),
    .cpld_SS(spi_ss),
    .cpld_MISO(spi_miso),
    .cpld_JP(cpld_JP)
  );

  // clock driver
  initial begin
    clk = 1'b0;
    forever #9 clk = ~clk;
  end

  // spi process
  always @(posedge clk) begin
    if (spi_start == 1'b1) begin
      $display("- start SPI transaction");
      spi_ss <= 1'b0;
      spi_count <= 6'd32;
      spi_mosi <= spi_d[31]; // first bit
      spi_shift <= {spi_d[30:0], 1'b0};
      spi_sck <= 1'b0;
    end else if (spi_ss == 1'b0) begin
      if (spi_count == 0) begin
        $display("- end SPI transaction with spi_shift=%x (A %x, rnw %x, wdata %x, rdata %x)",
          spi_shift, spi_shift[31:13], spi_shift[12], spi_shift[11:4], spi_shift[7:0]);
        spi_ss <= 1'b1; // end of transaction
      end else if (spi_sck == 1'b0) begin
        spi_sck <= 1'b1;
      end else begin
        // mid-transaction
        spi_mosi <= spi_shift[31];
        spi_shift <= {spi_shift[30:0], spi_miso};
        spi_count <= spi_count - 1;
        spi_sck <= 1'b0;
      end;
    end
  end

  always @(negedge dut.allowing_bbc_access) begin
    $display("disallowing bbc access");
  end

  always @(posedge dut.allowing_bbc_access) begin
    $display("allowing bbc access");
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
    $display("flash_nWE low with flash_A=%x and D=%x", flash_A, D);
  end

  always @(posedge flash_nWE) begin
    $display("flash_nWE high with flash_A=%x and D=%x", flash_A, D);
  end

  initial begin

    $display("running master_updateable_megarom_tb");

    $dumpfile("master_updateable_megarom_tb.vcd");
    $dumpvars(0, master_updateable_megarom_tb);

    $display("start");
    repeat(10) @(posedge clk);

    // check that we start out letting the BBC control the flash
    `assert(dut.allowing_bbc_access == 1'b1, "FAIL: not allowing bbc access initially");

    $display("\nSetting bbc_A to 12345");
    bbc_A <= 17'h12345;

    $display("\nTEST that ffffff00 disables BBC access");
    spi_d <= 32'hffffff00;
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    @(posedge clk);
    `assert(dut.allowing_bbc_access == 1'b0, "FAIL: ffffff00 didn't disable bbc access");

    $display("\nTEST that ffffffff reenables BBC access");
    spi_d <= 32'hffffffff;
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    @(posedge clk);
    `assert(dut.allowing_bbc_access == 1'b1, "FAIL: 32 1's didn't reenable bbc access");

    $display("\nTEST that we can write to the flash (51234)");
    // message format for a WRITE: 17 address bits, rnw, 8 data bits, 6 zeros (32 bits total)
    // with the write happening during the six zeros
    spi_d <= {19'b1010001001000110100, 1'b0, 8'b10001001, 4'b0000};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    `assert(dut.allowing_bbc_access == 1'b0, "FAIL: write operation unlocked bbc access");

    $display("\nTEST that we can read from the flash (70f0f)");
    // message format for a READ: 17 address bits, rnw, 14 zeros (32 bits total)
    // with the data byte returned in the final 8 bits
    spi_d <= {19'b1110000111100001111, 1'b1, 12'b0};
    spi_start <= 1;
    @(posedge clk);
    #1 spi_start <= 0;
    @(posedge spi_ss);
    `assert(dut.allowing_bbc_access == 1'b0, "FAIL: write operation unlocked bbc access");

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
