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


// Functions to access the Archimedes keyboard
// TODO support Risc PC, which uses a PS/2 keyboard

#include <stdint.h>
#include "arcregs.h"

void keyboard_init() {
	// Set up IOC TIMER3 to drive KART serial clock
	// From the VL86C410 databook: baud rate 31250 Hz is set with latch=1
	IOC_TIMER3_HIGH = 0;
	IOC_TIMER3_LOW = 1;
	IOC_TIMER3_GO = 0;
}

void keyboard_poll() {
	if (IOC_RX_FULL) {
		// Delay half a bit (1e6 / 31250 / 2 = 16 us) to work around IOC bug
		
		// Read keyboard serial port, which clears the RX_FULL flag
		uint8_t data = IOC_SERIAL;
	}
}