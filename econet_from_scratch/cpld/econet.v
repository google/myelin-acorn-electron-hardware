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


// Verilog implementation of the Econet wire protocol.

// This is traditionally implemented using a MC68B54 chip:
// https://www.heyrick.co.uk/econet/mc6854fixed.pdf

// All Econet transactions use a 'four way handshake':
//
// Scout frame:
// A sends: <flag> <B> <B> <A> <A> <ctrl> <port> <CRC> <CRC> <flag>
//
// Ack frame:
// B sends: <flag> <flag> <flag> ... (while busy)
//    then: <flag> <A> <A> <B> <B> <CRC> <CRC> <flag>
//
// Data frame:
// A sends: <flag> <B> <B> <A> <A> <data...> <CRC> <CRC> <flag>
//
// Second ack frame:
// B sends: <flag> <A> <A> <B> <B> <CRC> <CRC> <flag>

// Bytes are sent LSB-first.

// Zero insertion/deletion: after transmitting 11111, a zero is inserted.
// After receiving 11111, a zero is deleted.

// 01111110 = flag
// 1111111 = abort (and line idles at 1)


// We communicate with the MCU over a synchronous serial interface, which in
// practice is half-duplex because there's no need to transmit information in
// the opposite direction from the Econet line.

// mcu_is_transmitting line selects the direction.  When it transitions,
// everything gets reset.

// Right now this uses 64/72 MCs in an XC9572XL device.


module econet(
    // to MCU
    input wire clock,  // 24 MHz serial clock
    output reg mcu_txd = 1'b1,  // USRT txd (connect to MCU's rxd)
    input wire mcu_rxd,  // USRT rxd (connect to MCU's txd)
    input wire mcu_is_transmitting,  // direction select for the USRT; 1=mcu transmitting, 0 = cpld can transmit
    output reg outputting_frame = 1'b0,  // 1 when we're sending a frame, 0 when idle or underrun
    output wire serial_buffer_empty,  // 1 when the MCU can send a new byte

    // to sn65c1168 dual differential transceiver
    input wire econet_data_R,  // received data
    output reg econet_data_D = 1'b1,  // transmitted data
    output wire econet_data_DE,  // 1 to transmit data, 0 otherwise
    input wire econet_clock_R,  // received clock
    output reg econet_clock_D = 1'b1,  // transmitted clock
    output reg econet_clock_DE = 1'b0  // 1 to transmit clock, 0 otherwise
);

// So... how should this be implemented in the CPLD?  Matching the input for
// the 'flag' and 'abort' codes is fairly straightforward.

// --- INPUT SYNC ---

reg [2:0] econet_clock_sync = 3'b0;
reg [2:0] econet_data_sync = 3'b0;
reg [2:0] mcu_is_transmitting_sync = 3'b0;

// --- SERIAL PORT ---

reg [9:0] serial_shifter = 10'b1111111111;  // Start bit + 9 data bits
reg [3:0] serial_bit_count = 4'b0;  // Send/receive countdown from 11 (start + 9 + stop)
reg serial_input_buffer_full = 1'b0;
assign serial_buffer_empty = !serial_input_buffer_full && (serial_bit_count == 0);

// --- ECONET ---

// The ATSAMD21 USRT supports 9-bit words, so the CPLD can send 9'b0xxxxxxxx
// for a data word and 9'b1xxxxxxxx for anything else (9'b101111110 for a
// flag, 9'b1xxxxxxxx for an abort or any garbage).  When the MCU wants to
// send a flag, it can send 9'b101111110 ("send raw 01111110") and when it
// wants to send data it can send 9'b011111111 (which results in 111110111
// actually getting sent).

// Implement bit stuffing by generally thinking in bytes but having a 'raw'
// flag that is sent as a 9th bit from the MCU.

reg [2:0] econet_bit_count = 0;  // Bit # we're currently sending or receiving
reg [2:0] econet_ones_count = 0;  // # of ones seen in a row (0-7)
reg [7:0] econet_shifter = 0;  // 8-bit output shift register
reg econet_output_raw = 1'b0;  // If 1, don't bit stuff
reg econet_transmitting = 1'b0;  // Flag to say we're currently outputting from the shift register
reg econet_initiate_abort = 1'b0;  // Something went wrong: send an abort (raw 0xFF)

assign econet_data_DE = outputting_frame;

always @(negedge clock) begin
    // FALLING edge of serial clock: update value on mcu_txd
    mcu_txd <= mcu_is_transmitting_sync[2] ? 1'b1 : serial_shifter[0];
    // if (!mcu_is_transmitting && serial_bit_count != 0) $display("outputting bit to serial port: %b", serial_shifter[0]);
end

always @(posedge clock) begin
    // RISING edge of serial clock: sample value on mcu_rxd

    // To save on CPLD space, the entire system is half-duplex, driven by the
    // mcu_is_transmitting line.  When this line changes, the whole system is
    // reset, throwing away any half-transmitted or half-received data.

    // Synchronize signals from the Econet line.  tRDS = 50ns and tRDH = 60ns,
    // and our clock period is 42ns, so we'll have a tight enough sample.
    econet_clock_sync <= {econet_clock_sync[1:0], econet_clock_R};
    econet_data_sync <= {econet_data_sync[1:0], econet_data_R};
    mcu_is_transmitting_sync <= {mcu_is_transmitting_sync[1:0], mcu_is_transmitting};

    if (mcu_is_transmitting_sync[2] != mcu_is_transmitting_sync[1]) begin  // DIRECTION CHANGE

        serial_bit_count <= 0;
        serial_shifter[0] <= 1'b1;
        econet_transmitting <= 1'b0;
        econet_bit_count <= 0;
        econet_ones_count <= 7;

    end else if (mcu_is_transmitting_sync[2] == 1'b1) begin  // RECEIVE FROM MCU, TRANSMIT TO ECONET

        // TODO figure out if we need to synchronize mcu_is_transmitting, or
        // if it's already synchronous w.r.t the USRT clock

        // SERIAL PORT RECEIVER

        if (serial_bit_count == 0) begin
            if (mcu_rxd == 1'b0) begin
                // Received a start bit; start a transfer
                serial_bit_count <= 10;
            end
        end else if (serial_bit_count == 1) begin
            // Receiving a stop bit
            if (mcu_rxd == 1'b1) begin
                // Received data!
                if (serial_input_buffer_full == 1'b1) begin
                    // Buffer overrun; abort the frame.
                    econet_initiate_abort <= 1'b1;
                end else begin
                    serial_input_buffer_full <= 1'b1;
                end
            end else begin
                // Frame error; ignore byte and crash
                //TODO
            end
            serial_bit_count <= 0;
        end else begin
            // Receiving 9 bits from the serial port, LSB-first
            serial_shifter <= {mcu_rxd, serial_shifter[8:1]};
            serial_bit_count <= serial_bit_count - 1;
        end

        // COPY FROM SERIAL PORT TO ECONET REGISTER
        // Push a byte into the output shift register if necessary
        if (econet_transmitting == 1'b0) begin
            if (econet_initiate_abort == 1'b1) begin
                serial_input_buffer_full <= 1'b0;
                outputting_frame <= 1'b1;
                econet_transmitting <= 1'b1;
                econet_output_raw <= 1'b1;
                econet_shifter <= 8'b11111111;
                econet_bit_count <= 3'b0;
            end else if (serial_input_buffer_full == 1'b1) begin
                serial_input_buffer_full <= 1'b0;
                if (serial_shifter[8] == 1'b1) begin
                    // new frames always start with a raw (flag) byte
                    outputting_frame <= 1'b1;
                end
                econet_transmitting <= 1'b1;
                econet_output_raw <= serial_shifter[8];
                econet_shifter <= serial_shifter[7:0];
                econet_bit_count <= 3'b0;
            end
        end

        // ECONET TRANSMITTER

        if (econet_clock_sync[2] == 1'b1 && econet_clock_sync[1] == 1'b0) begin

            // FALLING ECONET CLOCK EDGE: FLIP OUTPUT

            if (outputting_frame == 1'b1) begin
                if (econet_transmitting == 1'b0) begin
                    // Buffer underrun: we're in a frame and it's time to output a bit, but we have nothing
                    outputting_frame <= 1'b0;
                end
            end

            // Transmit even if we're not inside a frame, to avoid deadlocks
            if (econet_transmitting == 1'b1) begin
                if (econet_output_raw == 1'b0 && econet_ones_count == 5) begin
                    // stuff a zero and reset the bit-stuff counter
                    econet_data_D <= 1'b0;
                    econet_ones_count <= 0;
                end else begin
                    // shift out a bit (LSB first) and increment/zero ones count as necessary
                    if (econet_shifter[0] == 1'b1) begin
                        econet_ones_count <= econet_ones_count + 1;
                    end else begin
                        econet_ones_count <= 0;
                    end
                    econet_data_D <= econet_shifter[0];
                    econet_shifter <= {1'b1, econet_shifter[7:1]};
                    econet_bit_count <= econet_bit_count + 1;

                    // econet_bit_count counts from 0-7 as the 8 bits are shifted out.
                    if (econet_bit_count == 7) begin
                        // we just finished transmitting a byte.  signal to controller
                        // that we need our shifter refilled.
                        econet_transmitting <= 1'b0;
                    end
                end
            end
        end

    end else begin  // mcu_is_transmitting == 1'b0; TRANSMIT TO MCU, RECEIVE FROM ECONET

        // SERIAL PORT TRANSMITTER

        if (serial_bit_count != 0) begin
            // --- MCU is receiving; we can drive mcu_txd ---
            serial_shifter <= {1'b1, serial_shifter[9:1]};
            serial_bit_count <= serial_bit_count - 1;
        end

        // ECONET RECEIVER

        if (econet_clock_sync[2] == 1'b0 && econet_clock_sync[1] == 1'b1) begin

            // RISING ECONET CLOCK EDGE: SAMPLE INPUT

            if (econet_ones_count == 7 && econet_data_sync[2] == 1'b1) begin
                // Stay in reset
            end else if (econet_ones_count == 6 && econet_data_sync[2] == 1'b1) begin
                // Reset!
                econet_ones_count <= econet_ones_count + 1;
                econet_bit_count <= 0;
            end else if (econet_ones_count == 6 && econet_data_sync[2] == 1'b0) begin
                // Just received a flag
                // Probably safe to assume this will never cause a serial overrun, as this would require an Econet line rate over 2MHz.
                $display("received flag: put 1+%02x (1+%b) in serial shifter", {econet_shifter[6:0], 1'b0}, {econet_shifter[6:0], 1'b0});
                serial_shifter <= {1'b1, econet_shifter[6:0], 1'b0, 1'b0};
                serial_bit_count <= 11;
                econet_ones_count <= 1'b0;
                econet_bit_count <= 0;
            end else if (econet_ones_count == 5 && econet_data_sync[2] == 1'b0) begin
                // Just read a stuffed zero
                // Reset ones count and skip this bit
                econet_ones_count <= 0;
            end else begin
                // Read a normal bit
                // Increment or reset ones count
                if (econet_data_sync[2] == 1'b1) begin
                    econet_ones_count <= econet_ones_count + 1;
                end else begin
                    econet_ones_count <= 0;
                end
                // Shift it into the receive register
                econet_shifter <= {econet_shifter[6:0], econet_data_sync[2]};
                // $display("econet_shifter about to be %b", {econet_shifter[6:0], econet_data_sync[2]});
                econet_bit_count <= econet_bit_count + 1;
                if (econet_bit_count == 7) begin
                    // Probably safe to assume this will never cause a serial overrun, as this would require an Econet line rate over 2MHz.
                    $display("received byte: put 0+%02x (0+%b) in serial shifter", {econet_shifter[6:0], econet_data_sync[2]}, {econet_shifter[6:0], econet_data_sync[2]});
                    serial_shifter <= {1'b0, {econet_shifter[6:0], econet_data_sync[2]}, 1'b0};
                    serial_bit_count <= 11;
                end
            end
        end  // rising econet_clock_R edge

    end  // !mcu_is_transmitting

end

endmodule
