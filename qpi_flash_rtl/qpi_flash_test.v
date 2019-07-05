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


`timescale 1ns/100ps
`include "qpi_flash.v"

`define assert(condition, message) if(!(condition)) begin $display("ASSERTION FAILED: %s", message); $finish(1); end

module qpi_flash_test;

  // test clock
  reg clk;

  // inputs to the module under test
  wire ready;
  reg reset = 0;
  reg read = 0;
  reg [23:0] addr = 0;
  reg passthrough = 0;
  reg passthrough_nCE;
  reg passthrough_SCK;
  reg passthrough_MOSI;

  // outputs from the module under test
  wire [7:0] data_out;

  // connections to the outside world
  wire flash_SCK;
  wire flash_nCE;
  wire flash_IO0;
  wire flash_IO1;
  wire flash_IO2;
  wire flash_IO3;

  reg driving_IO = 0;
  reg [3:0] output_IO = 4'bz;

  assign flash_IO3 = output_IO[3];
  assign flash_IO2 = output_IO[2];
  assign flash_IO1 = output_IO[1];
  assign flash_IO0 = output_IO[0];

  // test spi feeder
  reg spi_ss = 1'b1;
  reg spi_sck = 1'b0;
  reg spi_mosi = 1'b0;
  wire spi_miso;

  `define SHIFT_HIGH 63
  reg [`SHIFT_HIGH:0] spi_shift;
  reg [8:0] shift_count = 0;

  reg waiting_for_reset = 0;
  reg reset_wait_finished = 0;
  reg [31:0] reset_wait_count = 0;

  // module under test
  qpi_flash dut(
    .clk(clk),
    .ready(ready),
    .reset(reset),
    .read(read),

    .addr(addr),
    .data_out(data_out),
    .passthrough(passthrough),
    .passthrough_nCE(passthrough_nCE),
    .passthrough_SCK(passthrough_SCK),
    .passthrough_MOSI(passthrough_MOSI),

    .flash_nCE(flash_nCE),
    .flash_SCK(flash_SCK),
    .flash_IO0(flash_IO0),
    .flash_IO1(flash_IO1),
    .flash_IO2(flash_IO2),
    .flash_IO3(flash_IO3)
  );

  // clock driver
  initial begin
    clk = 1'b0;
    forever #9 clk = ~clk;
  end

  always @(posedge dut.ready) begin
    $display("rising edge on ready");
  end

  always @(negedge dut.reset) begin
    $display("falling edge on reset");
  end

  always @(negedge dut.read) begin
    $display("falling edge on read");
  end

  always @(negedge flash_nCE) begin
    $display("falling edge on flash_nCE");
    shift_count <= 0;
  end

  always @(posedge flash_SCK) begin
    if (dut.qpi_mode == 1) begin
      spi_shift <= {spi_shift[`SHIFT_HIGH-4:0], flash_IO3, flash_IO2, flash_IO1, flash_IO0};
      $display("rising QPI edge with output nybble %x", {flash_IO3, flash_IO2, flash_IO1, flash_IO0});
      shift_count <= shift_count + 4;
    end else begin
      spi_shift <= {spi_shift[`SHIFT_HIGH-1:0], flash_IO0};
      // $display("rising SPI edge with MOSI %x", flash_IO0);
      shift_count <= shift_count + 1;
    end
  end

  always @(negedge flash_SCK) begin
      if (shift_count == 8) begin
        $display("-> output byte %x", spi_shift[7:0]);
        shift_count <= 0;
      end
  end

  always @(posedge clk) begin
    if (ready == 1 || reset_wait_count > 10000) begin
      reset_wait_finished <= 1;
    end else if (reset_wait_finished == 0) begin
      reset_wait_count <= reset_wait_count + 1;
    end
  end

  initial begin

    $display("running qpi_flash_test");

    $dumpfile("qpi_flash_test.vcd");
    $dumpvars(0, qpi_flash_test);

    $display("start");
    reset <= 1;
    repeat(10) @(posedge clk);
    reset <= 0;
    waiting_for_reset <= 1;
    reset_wait_count <= 0;
    reset_wait_finished <= 0;
    @(posedge reset_wait_finished);

    `assert(ready == 1'b1, "FAIL: device not ready");

    $display("\n\nReset successful; trying a read (0 alignment)");
    addr <= 24'h123454;
    read <= 1;
    @(posedge clk);
    read <= 0;
    // wait for 4 qpi bytes
    repeat(8) @(negedge flash_SCK);
    // now push some data
    output_IO <= 4'hA;
    @(negedge flash_SCK);
    output_IO <= 4'hB;
    @(negedge flash_SCK);
    // output_IO <= 4'hC;
    // @(negedge flash_SCK);
    // output_IO <= 4'hD;
    // @(negedge flash_SCK);
    // output_IO <= 4'hE;
    // @(negedge flash_SCK);
    // output_IO <= 4'hF;
    // @(negedge flash_SCK);
    // output_IO <= 4'h1;
    // @(negedge flash_SCK);
    // output_IO <= 4'h2;
    // @(negedge flash_SCK);
    output_IO <= 4'bz;
    // wait for end of txn
    @(posedge flash_nCE);
    $display("Read transaction finished, by the looks of things; shifter == %x", dut.shifter);
    // `assert(dut.shifter[31:0] == 32'habcdef12, "shift value incorrect");
    $display("data_out == %x", data_out);
    `assert(data_out == 8'hab, "data_out incorrect");

    // $finish;

    // $display("\n\nReset successful; trying a read (1 alignment)");
    // addr <= 24'h000005;
    // read <= 1;
    // @(posedge clk);
    // read <= 0;
    // // wait for 4 qpi bytes
    // repeat(8) @(negedge flash_SCK);
    // // now push some data
    // output_IO <= 4'h1;
    // @(negedge flash_SCK);
    // output_IO <= 4'h2;
    // @(negedge flash_SCK);
    // output_IO <= 4'h3;
    // @(negedge flash_SCK);
    // output_IO <= 4'h4;
    // @(negedge flash_SCK);
    // // output_IO <= 4'h5;
    // // @(negedge flash_SCK);
    // // output_IO <= 4'h6;
    // // @(negedge flash_SCK);
    // // output_IO <= 4'h7;
    // // @(negedge flash_SCK);
    // // output_IO <= 4'h8;
    // // @(negedge flash_SCK);
    // output_IO <= 4'bz;
    // // wait for end of txn
    // @(posedge flash_nCE);
    // $display("Read transaction finished, by the looks of things; shifter == %x", dut.shifter);
    // // `assert(dut.shifter[31:0] == 32'h12345678, "shift value incorrect");
    // $display("data_out == %x", data_out);
    // `assert(data_out == 8'h34, "data_out incorrect");

    // $display("\n\nReset successful; trying a read (2 alignment)");
    // addr <= 24'hfffff2;
    // read <= 1;
    // @(posedge clk);
    // read <= 0;
    // // wait for 4 qpi bytes
    // repeat(8) @(negedge flash_SCK);
    // // now push some data
    // output_IO <= 4'h1;
    // @(negedge flash_SCK);
    // output_IO <= 4'ha;
    // @(negedge flash_SCK);
    // output_IO <= 4'h2;
    // @(negedge flash_SCK);
    // output_IO <= 4'hb;
    // @(negedge flash_SCK);
    // output_IO <= 4'h3;
    // @(negedge flash_SCK);
    // output_IO <= 4'hc;
    // @(negedge flash_SCK);
    // // output_IO <= 4'h4;
    // // @(negedge flash_SCK);
    // // output_IO <= 4'hd;
    // // @(negedge flash_SCK);
    // output_IO <= 4'bz;
    // // wait for end of txn
    // @(posedge flash_nCE);
    // $display("Read transaction finished, by the looks of things; shifter == %x", dut.shifter);
    // // `assert(dut.shifter[31:0] == 32'h1a2b3c4d, "shift value incorrect");
    // $display("data_out == %x", data_out);
    // `assert(data_out == 8'h3c, "data_out incorrect");

    // $display("\n\nReset successful; trying a read (3 alignment)");
    // addr <= 24'hcccc5b;
    // read <= 1;
    // @(posedge clk);
    // read <= 0;
    // // wait for 4 qpi bytes
    // repeat(8) @(negedge flash_SCK);
    // // now push some data
    // output_IO <= 4'hf;
    // @(negedge flash_SCK);
    // output_IO <= 4'h9;
    // @(negedge flash_SCK);
    // output_IO <= 4'he;
    // @(negedge flash_SCK);
    // output_IO <= 4'h8;
    // @(negedge flash_SCK);
    // output_IO <= 4'hd;
    // @(negedge flash_SCK);
    // output_IO <= 4'h7;
    // @(negedge flash_SCK);
    // output_IO <= 4'hc;
    // @(negedge flash_SCK);
    // output_IO <= 4'h6;
    // @(negedge flash_SCK);
    // output_IO <= 4'bz;
    // // wait for end of txn
    // @(posedge flash_nCE);
    // $display("Read transaction finished, by the looks of things; shifter == %x", dut.shifter);
    // // `assert(dut.shifter[31:0] == 32'hf9e8d7c6, "shift value incorrect");
    // $display("data_out == %x", data_out);
    // `assert(data_out == 8'hc6, "data_out incorrect");

    // finish off
    $display("running out the clock");
    repeat(32) @(posedge clk);

    $display("PASS");

    $finish;

  end

endmodule
