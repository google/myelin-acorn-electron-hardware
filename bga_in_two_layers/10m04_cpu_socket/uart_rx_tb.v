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
`include "uart_rx.v"
`include "uart.v"

module uart_tb;

  integer i;

  // transmit side
  reg clk, transmit;
  reg [23:0] tx_data;
  wire txd, tx_empty;

  // receive side
  wire [7:0] rx_data;
  wire rx_full;
  reg rx_ack = 1;  // insta-ack everything

  // transmit uart to test my receiver
  uart #(
    .divide_count(20)
  ) test_uart(
    .clock(clk),
    .txd(txd),
    .tx_data(tx_data),
    .tx_empty(tx_empty),
    .transmit(transmit)
  );

  uart_rx #(
    .divide_count(5)
  ) test_uart_rx(
    .clock(clk),
    .rxd(txd),  // attached to transmitter
    .rx_data(rx_data),
    .rx_full(rx_full),
    .ack(rx_ack)
  );

  initial begin
    clk = 1'b0;
    forever #9 clk = ~clk;
  end

  initial begin

    $display("running uart_tb");

    $dumpfile("uart_rx_tb.vcd");
    $dumpvars(0, uart_tb);

    $display("start");
    transmit = 0;
    repeat(8) @(posedge clk);

    $display("transmit");
    tx_data = 24'b111111110000000010110010;
    transmit = 1;
    @(posedge clk);
    #1 transmit = 0;

    $display("observe");
    @(posedge tx_empty);
    tx_data = 8'h00;
    transmit = 1;
    @(posedge clk);
    #1 transmit = 0;

    @(posedge tx_empty);
    repeat(100) @(posedge clk);

    $display("stop now");

    $finish;

  end

endmodule
