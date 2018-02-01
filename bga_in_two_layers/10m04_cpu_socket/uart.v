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


// Simple send-only UART

module uart(
  input wire clock,         // main clock
  output reg txd = 1'b1,
  input wire [23:0] tx_data,
  output reg tx_empty = 1'b1,     // '1' when tx_data can take a new byte
  input wire transmit       // pulse '1' when tx_data is valid
);

// clock divider to get baud rate.  82M / 115.2k = 712, giving 115.169 kb/s
parameter divide_count = 712;

// clock divider, assuming divide_count <= 1023
reg [9:0] divider = 0;

// shift register -- (start bit + 8 data bits + 1 stop bit) x 3 bytes
reg [29:0] shifter;

// how many bits to shift -- counts down from 30
reg [4:0] shift_count = 0;

always @(posedge clock) begin

  // trying making this synchronous to debug missing transfers
  // that could possibly be to do with the fifo in elk_interface...
  // previously this was:
  // assign tx_empty = (shift_count == 0) ? 1'b1 : 1'b0;
  tx_empty = (shift_count == 0) ? 1'b1 : 1'b0;
  // note that we can get slightly lower latency by setting this inside the loop that
  // decrements shift_count, but that only happens on divider expiry and this happens
  // every clock, so having it out here only slows it down 12 ns!

  // accept a new byte to send
  if (tx_empty == 1'b1 && transmit == 1'b1) begin
    $display("accept new byte from tx_data");
    // shifter <= {tx_data, 1'b0}; // 8-bit
    shifter <= {1'b1, tx_data[23:16], 1'b0, 1'b1, tx_data[15:8], 1'b0, 1'b1, tx_data[7:0], 1'b0}; // 24-bit
    shift_count <= 31;
    tx_empty <= 1'b0;
  end

  // divider divides clock down to the serial bit rate (x 4 for reception?)
  if (divider == divide_count) begin
    divider <= 1;

    // transmit a bit on divider expiry
    if (shift_count != 0) begin
      txd <= shifter[0];
      // shift right
      shifter <= {1'b1, shifter[29:1]};
      shift_count <= shift_count - 5'd1;
    end

  end else begin
    divider <= divider + 10'd1;
  end
end

endmodule
