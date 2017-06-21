// Copyright 2017 Google Inc.
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

// UPURS uses inverted logic because it expects the User Port pins to be wired
// (with a series resistor and a diode from GND) straight to pins at RS232
// levels (+13V = 0, -13V = 1).

// Either define USE_INVERTED_SOFTWARE_SERIAL to do this in software, using
// SoftwareSerial, or leave it undefined, and add an inverter externally
// on the TX/RX lines (CTS and RTS are implemented in software either way).
#define USE_INVERTED_SOFTWARE_SERIAL

// For debugging -- define this to echo everything back to the USB port
#define DEBUG_USB_LOOPBACK

#ifdef USE_INVERTED_SOFTWARE_SERIAL
#include <SoftwareSerial.h>
#endif

// Serial receive -- PD2, D0.
#define RXD_PIN 0

// Serial transmit -- PD3, D1.
#define TXD_PIN 1

// CTS is an active-high input that tells us that we're Cleared To Send.
// The hardware pin is PD5 (pin 22, green LED).
#define CTS_PIN 4

// RTS is an active-high output that tells the remote that we're Requesting
// them To Send.  The hardware pin is PB7 (D11, not used).
#define RTS_PIN 5

// On the Pro Micro:
//   SerialUSB = Serial = the USB CDC serial port
//   Serial1 = the hardware serial port on pins 0, 1
//   SoftwareSerial = bit banged serial port so we can do inverse logic

#ifdef USE_INVERTED_SOFTWARE_SERIAL
SoftwareSerial SerialBBC(RXD_PIN, TXD_PIN, true);
#else
#define SerialBBC Serial1
#endif

void setup() {
	SerialUSB.begin(9600);

	pinMode(TXD_PIN, OUTPUT);
	pinMode(RXD_PIN, INPUT);
	SerialBBC.begin(115200);

	pinMode(CTS_PIN, INPUT); // ~35k pullup
	pinMode(RTS_PIN, OUTPUT);
	digitalWrite(RTS_PIN, HIGH);
}

#ifdef USE_BUFFER

#define BUF_SIZE 1024
uint8_t buf[BUF_SIZE];
int buf_write_ptr = 0;
int buf_read_ptr = 0;
int buf_usage = 0;
unsigned long last_activity = 0;

void loop() {
	// read everything we can from USB
	while (buf_usage < BUF_SIZE && SerialUSB.available()) {
		buf[buf_write_ptr] = SerialUSB.read();
		buf_write_ptr = (buf_write_ptr + 1) % BUF_SIZE;
		buf_usage++;
		last_activity = millis();
	}
	// write as much as we can to the BBC
	while (buf_usage > 0 && digitalRead(CTS_PIN) == HIGH) {
		// BBC is clearing us to send; pass anything we have on
		// from the USB port
		SerialBBC.write(buf[buf_read_ptr]);
		buf_read_ptr = (buf_read_ptr + 1) % BUF_SIZE;
		buf_usage--;
		last_activity = millis();
	}
	// pass BBC data back up to the USB
	if (SerialBBC.available()) {
		SerialUSB.write(SerialBBC.read());
		last_activity = millis();
	}
	if (millis() - last_activity > 1000) {
		SerialUSB.print("status: ");
		SerialUSB.print(digitalRead(CTS_PIN) == HIGH ? "cts high" : "cts low");
		SerialUSB.println();
		last_activity = millis();
	}
}

#else // !USE_BUFFER

//#define RETRY_AFTER_CTS
unsigned long last_activity = 0;

void loop() {
	int cts = 0;
	int buffered_char = -1;
	static int written = 0;

	while (1) {
		cts = digitalRead(CTS_PIN);
		while (cts == HIGH && SerialUSB.available()) {
#ifdef RETRY_AFTER_CTS
			if (buffered_char == -1) {
#endif
				buffered_char = SerialUSB.read();
#ifdef RETRY_AFTER_CTS
			}
#endif
			SerialBBC.write(buffered_char);
			cts = digitalRead(CTS_PIN);
			if (cts == LOW) {
				digitalWrite(RTS_PIN, LOW); // DEBUG blip after writing a char
				digitalWrite(RTS_PIN, HIGH);
				break;
			}
#ifdef DEBUG_USB_LOOPBACK
			// SerialUSB.write(buffered_char);
#endif
			buffered_char = -1; // successfully wrote the character -- no need to retry
			// last_activity = millis();
			// ++written;
		}
		// if (!cts && written) {
		// 	SerialUSB.print("[CTS!]");
		// 	written = 0;
		// }
		while (SerialBBC.available()) {
			SerialUSB.write(SerialBBC.read());
			last_activity = millis();
		}
		// if (millis() - last_activity > 1000) {
		// 	SerialUSB.print("status: ");
		// 	SerialUSB.print(digitalRead(CTS_PIN) == HIGH ? "cts high" : "cts low");
		// 	SerialUSB.println();
		// 	last_activity = millis();
		// }
	}
}

#endif // !USE_BUFFER
