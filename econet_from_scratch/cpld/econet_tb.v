`timescale 1ns/100ps
`include "econet.v"

`define assert(condition, message) if(!(condition)) begin $display(message); $finish(1); end

module econet_tb;

    reg clk;
    wire mcu_txd;
    reg mcu_rxd = 1'b1;
    reg mcu_is_transmitting;
    wire outputting_frame, serial_buffer_empty;

    wire econet_data_R, econet_data_D, econet_clock_D;
    wire econet_clock_R, econet_data_DE, econet_clock_DE;

    econet test_econet(
        .clock_24m(clk),
        .serial_cpld_to_mcu(mcu_txd),
        .serial_mcu_to_cpld(mcu_rxd),
        .mcu_is_transmitting(mcu_is_transmitting),
        .outputting_frame(outputting_frame),
        .serial_buffer_empty(serial_buffer_empty),

        .drive_econet_clock(1'b0),
        .econet_data_R(econet_data_R),
        .econet_data_D(econet_data_D),
        .econet_data_DE(econet_data_DE),
        .econet_clock_R(econet_clock_R),
        .econet_clock_D(econet_clock_D),
        .econet_clock_DE(econet_clock_DE)
    );

    reg econet_data_R_pre = 1'b1, econet_clock_R_pre = 1'b1;
    assign econet_clock_R = econet_clock_R_pre ^ test_econet.buggy_rev1_pcb;
    assign econet_data_R = econet_data_R_pre ^ test_econet.buggy_rev1_pcb;

    initial begin
        // 24 MHz clock, with 1/48 us = #10, so #480 = 1us
        clk = 1'b0;
        forever #10 clk = ~clk;
    end

    initial begin
        econet_clock_R_pre = 1'b1;
        // 1us up, 4us down
        forever begin
            #480 econet_clock_R_pre = 1'b0;
            #1920 econet_clock_R_pre = 1'b1;
        end
    end

    // econet

    reg [56:0] test_econet_receive_shifter;
    reg [7:0] test_bits_to_shift_into_econet = 0;

    // write to econet line on falling clock edge
    always @(negedge econet_clock_R_pre) begin
        if (test_bits_to_shift_into_econet != 0) begin
            econet_data_R_pre <= test_econet_receive_shifter[56];
            test_econet_receive_shifter <= {test_econet_receive_shifter[55:0], 1'b1};
            test_bits_to_shift_into_econet <= test_bits_to_shift_into_econet - 1;
        end
    end

    // serial port (MCU side)

    reg [9:0] test_serial_output_buffer = 10'b1111111111;
    reg [8:0] test_serial_send_byte = 0;
    reg [3:0] test_serial_output_bit = 0;  // counts down from 10
    reg test_serial_output_start = 1'b0;  // set high to trigger a serial transmission
    wire test_serial_output_empty;
    assign test_serial_output_empty = (test_serial_output_bit == 0);

    reg [3:0] test_serial_input_bit = 0;
    reg [8:0] test_serial_input_buffer = 0, test_serial_received_byte = 0;
    reg test_serial_input_full = 1'b0, test_serial_input_overrun = 1'b0;

    always @(posedge clk) begin
        if (test_serial_input_bit == 0) begin
            // waiting for start bit
            if (mcu_txd == 1'b0) begin
                // got start bit
                test_serial_input_bit <= 1;
            end
        end else begin
            if (test_serial_input_bit == 10) begin
                if (mcu_txd == 1'b1) begin
                    // Received byte
                    $display("Byte received on serial port: $%03x (%b)", test_serial_input_buffer, test_serial_input_buffer);
                    if (test_serial_input_full == 1'b1) begin
                        test_serial_input_overrun <= 1'b1;
                    end else begin
                        test_serial_input_full <= 1'b1;
                        test_serial_received_byte <= test_serial_input_buffer;
                    end
                end else begin
                    $display("FRAMING ERROR receiving byte from serial port");
                end
                test_serial_input_bit <= 0;
            end else begin
                // Shift value on mcu_txd in from left
                test_serial_input_buffer <= {mcu_txd, test_serial_input_buffer[8:1]};
                // $display("shift bit %b into test_serial_input_buffer; previously %b", mcu_txd, test_serial_input_buffer);
                // bits 1-9 = data bits
                test_serial_input_bit <= test_serial_input_bit + 1;
            end
        end
    end
    always @(negedge clk) begin
        if (test_serial_output_start == 1'b1 && test_serial_output_empty == 1'b1) begin
            // Kick off new transmission
            $display("[serial] starting new transmission");
            test_serial_output_buffer <= {test_serial_send_byte, 1'b0};
            test_serial_output_bit <= 10;
        end else begin
            // Change value on mcu_rxd and shift output buffer right one
            mcu_rxd <= test_serial_output_buffer[0];
            test_serial_output_buffer <= {1'b1, test_serial_output_buffer[9:1]};
            // Track if we're in a transmission or not
            if (test_serial_output_bit != 0) begin
                test_serial_output_bit <= test_serial_output_bit - 1;
                if (test_serial_output_bit == 1) begin
                    $display("[serial] byte transmitted");
                end
            end
        end
    end

    initial begin
        $display("econet_tb");
        $dumpfile("econet_tb.vcd");
        $dumpvars(0, econet_tb);

        $display("--- TESTING SENDING DATA TO ECONET ---");

        // enable tx
        #100 mcu_is_transmitting = 1'b1;

        // send flag
        $display("send flag 01111110");
        wait (test_serial_output_empty == 1'b1);
        #1 test_serial_send_byte = 10'b101111110;
        test_serial_output_start <= 1'b1;
        wait (test_serial_output_empty == 1'b0);
        #1 test_serial_output_start <= 1'b0;
        $display("wait for flag request to finish going out over the serial port");
        wait (test_serial_output_empty == 1'b1);
        $display("wait for serial port to be ready to receive another byte");
        wait (serial_buffer_empty == 1'b1);

        // send byte
        $display("send byte 011111(0)10");
        #1 test_serial_send_byte = 10'b001111110;
        test_serial_output_start <= 1'b1;
        wait (test_serial_output_empty == 1'b0);
        #1 test_serial_output_start <= 1'b0;
        wait (test_serial_output_empty == 1'b1);
        wait (serial_buffer_empty == 1'b1);

        // send byte
        $display("send byte 01000010");
        #1 test_serial_send_byte = 10'h42;
        test_serial_output_start <= 1'b1;
        wait (test_serial_output_empty == 1'b0);
        #1 test_serial_output_start <= 1'b0;
        wait (test_serial_output_empty == 1'b1);
        wait (serial_buffer_empty == 1'b1);

        // send byte
        $display("send byte 11111(0)111");
        #1 test_serial_send_byte = 10'hff;
        test_serial_output_start <= 1'b1;
        wait (test_serial_output_empty == 1'b0);
        #1 test_serial_output_start <= 1'b0;
        wait (test_serial_output_empty == 1'b1);
        wait (serial_buffer_empty == 1'b1);

        // send flag
        $display("send flag 01111110");
        #1 test_serial_send_byte = 10'b101111110;
        test_serial_output_start <= 1'b1;
        wait (test_serial_output_empty == 1'b0);
        #1 test_serial_output_start <= 1'b0;
        wait (test_serial_output_empty == 1'b1);
        wait (serial_buffer_empty == 1'b1);

        // disable tx
        wait (outputting_frame == 1'b0);
        mcu_is_transmitting = 1'b0;
        $display("done transmitting frame");
        mcu_is_transmitting = 1'b0;

        // test receiving a frame from the econet

        // enable rx
        mcu_is_transmitting = 1'b0;
        #10000 $display("--- TESTING RECEIVING DATA FROM ECONET ---");

        `assert(mcu_txd == 1'b1, "FAIL: mcu_txd should be idle (1) when not transmitting");

        $display("start sending test data on econet_clock_R");
        test_econet_receive_shifter = {
            8'b01111110,  // initial flag (17e)
            8'b10101010,  // aa
            8'b01010101,  // 55
            8'b10101010,  // aa
            9'b111110111, // ff
            8'b00000000,  // 00
            8'b01111110   // final flag (17e)
        };
        wait (econet_clock_R == 1'b0);
        test_bits_to_shift_into_econet = 64;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'h17e, "FAIL: expected 17e");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'haa, "FAIL: expected aa");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'h55, "FAIL: expected 55");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'haa, "FAIL: expected aa");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'hff, "FAIL: expected ff");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'h0, "FAIL: expected 00");
        test_serial_input_full = 1'b0;

        wait (test_serial_input_full == 1'b1);
        `assert(test_serial_input_buffer == 9'h17e, "FAIL: expected 17e");
        test_serial_input_full = 1'b0;

        wait (test_bits_to_shift_into_econet == 0);

        $display("TODO test reception of bad frame");

        $display("TODO test turnaround back to sending");

        $display("TODO test bad serial input");

        $display("econet_test done");
        #1000 $finish;
    end

    // Failsafe
    initial begin
        #1000000 $display("TIMEOUT -- EXITING");
        $finish;
    end

endmodule
