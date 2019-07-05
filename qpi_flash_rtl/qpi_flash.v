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


// QPI flash interface

// Targetted at Winbond W25Q128JV (16MB QPI)

// We use the Fast Read Quad I/O (EBh) instruction in QPI mode, and enable
// Continuous Read Mode.

// First request:
// EB AA AA AA MM -> DO
// Subsequent requests:
// AA AA AA MM -> DO

// Format of the mode bits (MM):
// M7-6: xx
// M5-4: 10 to enable Continuous Read Mode
// M3-0: xxxx
// So 00100000 (0x20) will enter Continuous Read Mode

// To exit Continuous Read Mode, it's recommended to go into SPI mode (IO1-3
// don't care) and clock in 0xFFFF (sixteen clocks).  Won't this cause a clash
// on the first query though?

// Probably want to do two transactions with spi_mode==1, clocking in 0xFF
// (eight clocks) each time.  If we're in QPI continuous read mode, this will
// register as an address of FF FF FF and a mode of FF.  If we're in QPI mode,
// it will register as an FF command, which exits QPI mode.

// READ COMMAND OPTIONS

// Fast Read (0Bh) in QPI Mode with 2 dummy clocks:
// \ 0B AA AA AA 00 DD / = 13 clocks

// Fast Read Quad I/O (EBh) in QPI Mode with 2 dummy clocks (used for the Mode byte)
// \ EB AA AA AA 20 DD / = 13 clocks for first request
// \ AA AA AA 20 DD / = 11 clocks for subsequent requests

// The datasheet suggests that in QPI mode, addresses may need to be aligned
// on a 4-byte boundary, but this doesn't seem to be the case.

module qpi_flash(

    // Fast clock for flash
    input wire clk,

    // Control interface; all signals synchronous w.r.t. clk

    // Active high to indicate that the module can accept a read command
    output reg ready = 0,

    // Active high reset; when this transitions low, the module will
    // initialize the flash chip.
    input wire reset,

    // Active high read instruction; pulse this for one clock with valid addr
    // to start a read.  When finished, ready will go high and data_out will
    // be valid.
    input wire read,

    // Bus
    input wire [23:0] addr,
    // input wire [7:0] data_in,  // one day...
    output reg [7:0] data_out = 8'hFF,

    // Passthrough
    input wire passthrough,
    input wire passthrough_nCE,
    input wire passthrough_SCK,
    input wire passthrough_MOSI,

    // Flash pins
    output reg flash_nCE = 1,
    output reg flash_SCK = 0,
    inout wire flash_IO0,
    inout wire flash_IO1,
    inout wire flash_IO2,
    inout wire flash_IO3

);

// Setup/hold notes:
// - Don't change /CS within 3ns of a rising clock edge.  (min 3ns clk to flash_nCE)
// - IO* setup 1ns hold 2ns w.r.t. SCK.  (min 2ns clk to flash_IO*)

// Reset: state register
reg [3:0] reset_state = 0;

`define RESET_START 0
`define RESET_DISABLE_CONT_READ 1
`define RESET_DISABLE_QPI 2
`define RESET_RESET_CHIP 3
`define RESET_WAIT_CHIP 4
`define RESET_ENTER_QPI 5
`define RESET_SET_DUMMY_CLOCKS 6
`define RESET_ENTER_CONT_READ 7
`define RESET_TEST_CONT_READ 8
`define RESET_SET_READY 9
`define RESET_DONE 10


// Reset: 30us counter
reg [12:0] reset_delay_counter = 13'b0;

// Shifter for IO[3:0]
reg [39:0] shifter = 0;
reg [6:0] shift_count = 0;

// Tracking previous passthrough value so we can reset after a passthrough ends
reg last_passthrough = 0;

// IO state
reg spi_mode = 1'b0;    // IO0 output, IO1 input, IO2/3 tristate
reg qpi_mode = 1'b0;
reg qpi_output = 1'b0;  // if qpi_mode == 1, this means we're in the output phase
reg [5:0] qpi_output_count = 0;  // countdown to turnaround

`define TXN_IDLE 0
`define TXN_START 1
`define TXN_RUNNING 2
`define TXN_FINISH 3
`define TXN_DONE 4

reg [2:0] txn_state = `TXN_IDLE;
reg reading = 0;

// Output register
reg [3:0] output_IO = 4'b0;

// Drive flash_IO* correctly depending on mode
assign flash_IO0 = (spi_mode == 1'b1 || qpi_output == 1'b1) ? output_IO[0] : 1'bZ;
assign flash_IO1 = (qpi_output == 1'b1) ? output_IO[1] : 1'bZ;
assign flash_IO2 = (qpi_output == 1'b1) ? output_IO[2] : 1'bZ;
assign flash_IO3 = (qpi_output == 1'b1) ? output_IO[3] : 1'bZ;

always @(posedge clk) begin

    // Lowest priority: read by MCU
    if (read == 1'b1) begin
        $display("Read triggered with addr %x", addr);
        qpi_output_count <= 6'd24 + 6'd8;  // output address and mode byte

        // 4-byte alignment
        // shifter <= {addr[23:2], 2'b00, 8'h20, 8'b0};  // addr & ~3
        // shift_count <= 7'd24 + 7'd8 + 7'd8 + (7'd8 * addr[1:0]);  // read 1-4 data bytes

        // 1-byte alignment (seems to work, despite what the datasheet says...)
        shifter <= {addr, 8'h20, 8'b0};
        shift_count <= 7'd24 + 7'd8 + 7'd8;  // read one data byte

        txn_state <= `TXN_START;
        reading <= 1;
        ready <= 0;

        // When running at 2MHz with an internal 6502, we have to be stable
        // while cpu_clken==1, but we have 7 x 62.5ns 16MHz clocks = 42 x
        // 96MHz clocks = 437.5 ns for memory access.

        // With running at 2MHz with an external 6502, we have 280 ns after
        // allowing for 170 ns address setup (30ns PHI0-PHI2 delay, 140ns
        // PHI2-A setup) and 50ns data hold.

        // The current read algorithm here will take 1 + (24 + 8 + 32) / 2 + 3
        // clocks (two clocks to transmit 4 bits in the data phase) = 36 x
        // 10.42 ns = 375.12 ns, so it should work with an internal T65 but
        // not an external 6502 yet.

    end
    if (reading && txn_state == `TXN_DONE) begin
        reading <= 0;
        ready <= 1;
        data_out <= shifter[7:0];
    end

    // Medium priority: SPI passthrough for MCU-driven SPI
    if (passthrough == 1'b1) begin
        spi_mode <= 1'b1;
        qpi_mode <= 0;
        qpi_output <= 1'b0;
        flash_nCE <= passthrough_nCE;
        flash_SCK <= passthrough_SCK;
        output_IO[0] <= passthrough_MOSI;
    end
    last_passthrough <= passthrough;
    if (last_passthrough == 1'b1 && passthrough == 1'b0) begin
        // Reset line after passthrough is disabled
        flash_nCE <= 1'b1;
        flash_SCK <= 1'b0;
        output_IO[0] <= 1'b0;

        // Re-enter QPI mode
        //reset_state <= `RESET_START;  // DEBUG don't reset after passthrough
    end

    // Execute SPI requests
    if (spi_mode == 1'b1) begin
        case (txn_state)
            `TXN_START : begin
                flash_nCE <= 1'b0;
                output_IO[0] = shifter[39];
                shifter <= {shifter[38:0], 1'b0};
                txn_state <= `TXN_RUNNING;
            end
            `TXN_RUNNING : begin
                if (shift_count == 0) begin
                    txn_state <= `TXN_FINISH;
                end else if (flash_SCK == 1'b0) begin
                    // Rising SCK edge
                    flash_SCK <= 1'b1;
                end else begin
                    // Falling SCK edge; clock data in and out
                    flash_SCK <= 1'b0;
                    output_IO[0] = shifter[39];
                    shifter <= {shifter[38:0], flash_IO1};
                    shift_count <= shift_count - 1;
                end
            end
            `TXN_FINISH : begin
                flash_nCE <= 1'b1;
                txn_state <= `TXN_DONE;
            end
        endcase
    end

    // Execute QPI requests
    if (qpi_mode == 1'b1) begin
        case (txn_state)
            `TXN_START : begin
                flash_nCE <= 1'b0;
                output_IO <= shifter[39:36];
                shifter <= {shifter[35:0], 4'b0};
                qpi_output <= 1;
                txn_state <= `TXN_RUNNING;
            end
            `TXN_RUNNING : begin
                if (shift_count == 0) begin
                    txn_state <= `TXN_FINISH;
                end else if (flash_SCK == 1'b0) begin
                    // Rising SCK edge
                    flash_SCK <= 1'b1;
                end else begin
                    // Falling SCK edge; clock data in and out
                    flash_SCK <= 1'b0;
                    output_IO <= shifter[39:36];
                    shifter <= {shifter[35:0], flash_IO3, flash_IO2, flash_IO1, flash_IO0};
                    shift_count <= shift_count - 7'd4;
                    if (qpi_output_count == 4) begin
                        qpi_output <= 0;
                    end else begin
                        qpi_output_count <= qpi_output_count - 6'd4;
                    end
                    if (qpi_output == 0 && shift_count == 7'd4) begin
                        data_out <= {shifter[3:0], flash_IO3, flash_IO2, flash_IO1, flash_IO0};
                    end
                end
            end
            `TXN_FINISH : begin
                flash_nCE <= 1'b1;
                qpi_output <= 1'b0;
                txn_state <= `TXN_DONE;
            end
        endcase
    end

    // Highest priority: reset
    case (reset_state)
        `RESET_START : begin
            // During flash programming, the QE (Quad Enable) bit is set, and
            // it's non-volatile, so we don't need to deal with that here.
            reset_state <= `RESET_DISABLE_CONT_READ;
        end

        `RESET_DISABLE_CONT_READ : begin
            // Start with a single-byte (FF) SPI transaction to disable
            // continuous read mode, if enabled.

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Disabling continuous read");
                    shifter <= 40'hFF00000000;
                    shift_count <= 8;
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_DISABLE_QPI;
                end
            endcase
        end

        `RESET_DISABLE_QPI : begin

            // Now a second single-byte (FF) SPI transaction, to disable
            // QPI mode, if enabled.

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Disabling QPI mode");
                    shifter <= 40'hFF00000000;
                    shift_count <= 8;
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_ENTER_QPI;
                    // reset_state <= `RESET_SET_READY;  // Disable QPI for testing
                end
            endcase

        end

       //`RESET_RESET_CHIP: begin
       //    // Now a two-byte (66 99) SPI transaction to reset the chip.
       //    case (txn_state)
       //        `TXN_IDLE : begin
       //            shifter <= 40'h6699000000;
       //            shift_count <= 8;
       //        end
       //        `TXN_DONE : begin
       //            txn_state <= `TXN_IDLE;
       //            reset_state <= `RESET_WAIT_CHIP;
       //        end
       //    endcase
       //end

       //`RESET_WAIT_CHIP : begin
       //    // Now delay 30us (2880 96MHz clocks using reset_delay_counter) to
       //    // let the chip reset finish.
       //    //TODO
       //    reset_state <= `RESET_ENTER_QPI;
       //end

        `RESET_ENTER_QPI : begin

            // Now a one-byte (38) SPI transaction to enter QPI mode.

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Entering QPI mode");
                    shifter <= 40'h3800000000;
                    shift_count <= 8;
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_SET_DUMMY_CLOCKS;
                    spi_mode <= 0;
                    qpi_mode <= 1;
                    // reset_state <= `RESET_SET_READY;  // DEBUG skip QPI transactions
                end
            endcase

        end

        `RESET_SET_DUMMY_CLOCKS : begin

            // Now a two-byte (C0 00) QPI transaction to set 2 dummy clocks
            // (which is what we need below 50 MHz).

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Setting read params");
                    shifter <= 40'hC000000000;
                    shift_count <= 16;
                    qpi_output_count <= 20;  // Remain in output state after txn
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_ENTER_CONT_READ;
                end
            endcase

        end

        `RESET_ENTER_CONT_READ : begin

            // Now a five-byte (EB 00 00 00 20) QPI transaction to enter
            // continuous read mode.

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Entering continuous read mode");
                    // shifter <= 40'hEB00000020;
                    // shifter <= 40'hEB00000120;  // test unaligned read; expect ab
                    // shifter <= 40'hEB00000220;  // test unaligned read; expect 8e
                    shifter <= 40'hEB00000320;  // test unaligned read; expect 82 (or 4c with single byte read)
                    // shift_count <= 72;  // read 4 bytes at the end
                    shift_count <= 48;  // read one byte at the end
                    qpi_output_count <= 40;
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_TEST_CONT_READ;
                end
            endcase

        end

        `RESET_TEST_CONT_READ : begin

            // Try aa four-byte (00 00 00 20) QPI read

            case (txn_state)
                `TXN_IDLE : begin
                    $display("qpi_flash: Testing continuous read mode");
                    shifter <= 40'h0000072000;  // test unaligned read; expect 1b
                    shift_count <= 40;  // read one byte at the end
                    qpi_output_count <= 32;
                    txn_state <= `TXN_START;
                end
                `TXN_DONE : begin
                    txn_state <= `TXN_IDLE;
                    reset_state <= `RESET_SET_READY;
                end
            endcase

        end

        `RESET_SET_READY : begin

            // Now set ready = 1'b1 and go to normal operation

            $display("qpi_flash: Reset done");
            ready <= 1;
            reset_state <= `RESET_DONE;

        end

        `RESET_DONE : begin

            // Normal operation!

        end

        default : begin

            // ERROR

        end

    endcase

    if (reset == 1'b1) begin
        ready <= 1'b0;

        flash_nCE <= 1'b1;
        flash_SCK <= 1'b0;
        output_IO <= 4'b0;
        spi_mode <= 1'b1;
        qpi_mode <= 1'b0;
        qpi_output <= 1'b0;
        reading <= 0;

        reset_state <= `RESET_START;
    end
end

endmodule