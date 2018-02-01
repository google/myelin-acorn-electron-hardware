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

// Receive-only UART

// IDLE state -- rxd high

// READING state -- clocking in bits

// STOP_BIT state -- waiting for stop bit, then sending the data out rx_data

module uart_rx(
  input wire clock,           // main clock
  input wire rxd,             // rxd pin
  output reg [7:0] rx_data,  // received data output register
  output reg rx_full = 1'b0,  // '1' when rx_data is valid
  input wire ack              // pulse '1' to ack rx_data and allow a new byte
);


// clock divider to get baud rate x 4.  82M / 115.2k / 4 = 178, giving 115.169 kb/s
parameter divide_count = 178;
reg [9:0] divider = 0;  // 0-1023

// state machine
parameter IDLE = 0, READING = 1, STOP_BIT = 2;
reg [1:0] state = 0;

// input shift register
reg [7:0] shifter;

// how many bits to shift (0-7)
reg [2:0] shift_count;

// sync external rxd signal
reg [2:0] rxd_sync;

// timer to sample the bit right in the center (0-7)
reg [2:0] bit_timer;

always @(posedge clock) begin

  if (ack == 1'b1) begin
    rx_full <= 1'b0;
  end

  rxd_sync <= {rxd_sync[1:0], rxd};

  // divider divides clock down to the serial bit rate (x 4 for reception)
  if (state == IDLE) begin

    // hold divider
    divider = 3;

    // look for a falling edge on rxd
    if (rxd_sync[2] == 0) begin
      bit_timer <= 3'd5;
      state <= READING;
      shift_count <= 7;
    end

  end else begin  // READING or STOP_BIT state

    if (divider != divide_count) begin
      divider <= divider + 10'd1;
    end else begin

      // divider just hit its target -- reset it
      divider <= 1;

      if (bit_timer != 0) begin
        bit_timer <= bit_timer - 3'd1;
      end else begin

        // it's time to sample a bit on divider + bit_timer expiry
        // uart is little-endian, so we shift in from the left.
        if (state == STOP_BIT) begin
          if (rxd_sync[2] == 1'b1) begin
            rx_full <= 1'b1;
            rx_data <= shifter;
          end;
          state <= IDLE;
        end else begin
          shifter <= {rxd_sync[2], shifter[7:1]};
          if (shift_count == 0) begin
            state <= STOP_BIT;
          end else begin
            shift_count <= shift_count - 3'd1;
          end
        end
        bit_timer <= 3;
      end

    end

    if (divider == 0) begin
    end
  end
end

endmodule
