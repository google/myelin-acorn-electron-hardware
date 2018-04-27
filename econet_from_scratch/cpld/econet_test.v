`timescale 1ns/100ps
`include "econet.v"

module econet_test;

	reg clk;
	wire mcu_txd;
	reg mcu_rxd = 1'b1;
	reg mcu_is_transmitting;
	wire outputting_frame, serial_buffer_empty;

	reg econet_data_R, econet_clock_R;
	wire econet_data_D, econet_clock_D;
	wire econet_data_DE, econet_clock_DE;

	econet test_econet(
		.clock(clk),
		.mcu_txd(mcu_txd),
		.mcu_rxd(mcu_rxd),
		.mcu_is_transmitting(mcu_is_transmitting),
		.outputting_frame(outputting_frame),
		.serial_buffer_empty(serial_buffer_empty),

		.econet_data_R(econet_data_R),
		.econet_data_D(econet_data_D),
		.econet_data_DE(econet_data_DE),
		.econet_clock_R(econet_clock_R),
		.econet_clock_D(econet_clock_D),
		.econet_clock_DE(econet_clock_DE)
	);

	initial begin
		// 24 MHz clock, with 1/48 us = #10, so #480 = 1us
		clk = 1'b0;
		forever #10 clk = ~clk;
	end

	initial begin
		econet_clock_R = 1'b1;
		// 1us up, 4us down
		forever begin
			#480 econet_clock_R = 1'b0;
			#1920 econet_clock_R = 1'b1;
		end
	end

	// serial port (MCU side)

	reg [9:0] serial_output_buffer = 10'b1111111111;
	reg [8:0] serial_send_byte = 0;
	reg [3:0] serial_output_bit = 0;  // counts down from 10
	reg serial_output_start = 1'b0;  // set high to trigger a serial transmission
	wire serial_output_empty;
	assign serial_output_empty = (serial_output_bit == 0);

	reg [3:0] serial_input_bit = 0;
	reg [9:0] serial_input_buffer = 0, serial_received_byte = 0;
	reg serial_input_full = 1'b0, serial_input_overrun = 1'b0;

	always @(posedge clk) begin
		if (serial_input_bit == 0) begin
			// waiting for start bit
			if (mcu_txd == 1'b0) begin
				// got start bit
				serial_input_bit <= 1;
			end
		end else begin
			if (serial_input_bit == 10) begin
				if (mcu_txd == 1'b1) begin
					// Received byte
					if (serial_input_full == 1'b1) begin
						serial_input_overrun <= 1'b1;
					end else begin
						serial_input_full <= 1'b1;
						serial_received_byte <= serial_input_buffer;
					end
				end
				serial_input_bit <= 0;
			end else begin
				// Shift value on mcu_txd in from left
				serial_input_buffer <= {mcu_txd, serial_input_buffer[9:1]};
				// bits 1-9 = data bits
				serial_input_bit <= serial_input_bit + 1;
			end
		end
	end
	always @(negedge clk) begin
		if (serial_output_start == 1'b1 && serial_output_empty == 1'b1) begin
			// Kick off new transmission
			$display("[serial] starting new transmission");
			serial_output_buffer <= {serial_send_byte, 1'b0};
			serial_output_bit <= 10;
		end else begin
			// Change value on mcu_rxd and shift output buffer right one
			mcu_rxd <= serial_output_buffer[0];
			serial_output_buffer <= {1'b1, serial_output_buffer[9:1]};
			// Track if we're in a transmission or not
			if (serial_output_bit != 0) begin
				serial_output_bit <= serial_output_bit - 1;
				if (serial_output_bit == 1) begin
					$display("[serial] byte transmitted");
				end
			end
		end
	end

	initial begin
		$display("econet_test");
	    $dumpfile("econet_test.vcd");
	    $dumpvars(0, econet_test);

	    // test sending a frame out to the econet

	    // enable tx
	    #100 mcu_is_transmitting = 1'b1;

	    // send flag
	    $display("send flag 01111110");
	    wait (serial_output_empty == 1'b1);
	    #1 serial_send_byte = 10'b101111110;
	    serial_output_start <= 1'b1;
	    wait (serial_output_empty == 1'b0);
	    #1 serial_output_start <= 1'b0;
	    $display("wait for flag request to finish going out over the serial port");
	    wait (serial_output_empty == 1'b1);
	    $display("wait for serial port to be ready to receive another byte");
	    wait (serial_buffer_empty == 1'b1);

	    // send byte
	    $display("send byte 011111(0)10");
	    #1 serial_send_byte = 10'b001111110;
	    serial_output_start <= 1'b1;
	    wait (serial_output_empty == 1'b0);
	    #1 serial_output_start <= 1'b0;
	    wait (serial_output_empty == 1'b1);
	    wait (serial_buffer_empty == 1'b1);

	    // send byte
	    $display("send byte 01000010");
	    #1 serial_send_byte = 10'h42;
	    serial_output_start <= 1'b1;
	    wait (serial_output_empty == 1'b0);
	    #1 serial_output_start <= 1'b0;
	    wait (serial_output_empty == 1'b1);
	    wait (serial_buffer_empty == 1'b1);

	    // send byte
	    $display("send byte 11111(0)111");
	    #1 serial_send_byte = 10'hff;
	    serial_output_start <= 1'b1;
	    wait (serial_output_empty == 1'b0);
	    #1 serial_output_start <= 1'b0;
	    wait (serial_output_empty == 1'b1);
	    wait (serial_buffer_empty == 1'b1);

	    // send flag
	    $display("send flag 01111110");
	    #1 serial_send_byte = 10'b101111110;
	    serial_output_start <= 1'b1;
	    wait (serial_output_empty == 1'b0);
	    #1 serial_output_start <= 1'b0;
	    wait (serial_output_empty == 1'b1);
	    wait (serial_buffer_empty == 1'b1);

	    // disable tx
	    wait (outputting_frame == 1'b0);
	    mcu_is_transmitting = 1'b0;
	    $display("done transmitting frame");
	    mcu_is_transmitting = 1'b0;

	    // test receiving a frame from the econet

	    // enable rx
	    // receive flag
	    // receive byte
	    // receive flag

		$display("econet_test done");
	    #1000 $finish;
	end

	// Failsafe
	initial begin
		#1000000 $finish;
	end

endmodule
