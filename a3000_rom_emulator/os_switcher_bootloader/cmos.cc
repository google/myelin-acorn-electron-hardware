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


// Functions to access the PCF8583 battery backed ("CMOS") RAM/timer chip.

// PCF8583 A0 is grounded and OSCI/OSCO are connected to a 32.768kHz crystal.
// PCF8583 max frequency is 100 kHz, i.e. 10 us clock period.


// Commands available:

// Write from address: START <addr with RnW=0> <reg address> <data bytes...> STOP
// Read from address: START <addr with RnW=0> <reg address> START <addr with RnW=1> <read data bytes...> STOP
// Continuing read: START <addr with RnW=1> <read data bytes...> STOP


// Memory map:

// 0x00 = control/status
// 0x01 = hundredth second
// 0x02 = seconds
// 0x03 = minutes
// 0x04 = hours
// 0x05 = year and date
// 0x06 = weekday and months
// 0x07 = timer
// 0x08 = alarm control
// 0x09-0x0f = alarm or ram
// 0x10-0xff = ram

// The following PRM links show the RAM map; note that addresses 0-239 correspond to 0x10-0xff on the chip.

// http://www.riscos.com/support/developers/prm/memoryman.html#40894 shows the map for RISC OS 3.11
// http://www.riscos.com/support/developers/prm/cmos.html shows the map for RISC OS 3.6

#include "arcflash.h"

void cmos_wait() {
	// TODO
}

// Set C<1> (SCL) and C<0> (SDA)
static void cmos_signal(uint8_t clock, uint8_t data) {
	IOC_CTRL = 0xfc | (clock ? 2 : 0) | (data ? 1 : 0);
	cmos_wait();
}

// Read C<0> (SDA)
static uint8_t cmos_read_data() {
	return IOC_CTRL & 1;
}

// Send I2C start condition
static void cmos_start() {
	// data and clock high (idle condition)
	cmos_signal(1, 1);
	// data transitions low while clock high
	cmos_signal(1, 0);
	// clock and data low, ready for transaction
	cmos_signal(0, 0);
}

// Send I2C stop condition
static void cmos_stop() {
	// clock and data low at end of transaction
	cmos_signal(0, 0);
	// clock high with data still low
	cmos_signal(1, 0);
	// data transitions high while clock high (idle condition)
	cmos_signal(1, 1);
}

static void cmos_send_bit(uint8_t bit) {
	bit = bit ? 1 : 0;
	cmos_signal(0, bit);
	cmos_signal(1, bit);
	cmos_signal(0, bit);
}

static uint8_t cmos_read_bit() {
	cmos_signal(0, 1);  // clock low, don't drive data
	cmos_signal(1, 1);  // clock high, don't drive data
	uint8_t bit = cmos_read_data();
	cmos_signal(0, 1);  // clock low, don't drive data
	return bit;
}

static uint8_t cmos_send(uint8_t byte) {
	// MSB-first: send 8 bits then read ack bit
	for (int i = 0; i < 8; ++i) {
		cmos_send_bit(byte & 0x80);
		byte <<= 1;
	}
	return cmos_read_bit();  // Acknowledge
}

static uint8_t cmos_receive(uint8_t should_ack) {
	// MSB-first; clock in 8 bits then send ack (or not)
	uint8_t byte = 0;
	for (int i = 0; i < 8; ++i) {
		byte = (byte << 1) | cmos_read_bit();
	}
	cmos_send_bit(should_ack ? 0 : 1);
	return byte;
}

void read_cmos() {
	// To read the device, we need to do an initial write to set the register address
	cmos_start();     // First start
	cmos_send(0xa0);  // Write
	cmos_send(0);     // Address zero

	cmos_start();     // Second start, for reading
	cmos_send(0xa1);  // Read from device with A0=0
	uint8_t data[256];
	for (int i = 0; i < 256; ++i) {
		data[i] = cmos_receive((i == 255) ? 0 : 1);  // Ack all but last byte
	}
	cmos_stop();

	display_printf("CMOS: ");
	for (int i = 0; i < 256; ++i) {
		display_printf(" %x", data[i]);
	}
	display_printf("\n");
}

void write_cmos() {
	cmos_start();
	cmos_send(0xa0);  // Write to device with A0=0
	cmos_send(0);
	// TODO
	cmos_stop();
}