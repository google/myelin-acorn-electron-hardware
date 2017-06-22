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
// #define USE_INVERTED_SOFTWARE_SERIAL
// #define USE_SOFTWARE_SERIAL

// For debugging -- define this to echo everything back to the USB port.
// This will break UPURS, by sometimes spending too long between characters.
// #define DEBUG_USB_LOOPBACK

// Define this to ignore anything coming back from the BBC, i.e. when
// using a CPLD to output debug pulses on the RX pin...
#define IGNORE_BBC_RX

#if defined(USE_INVERTED_SOFTWARE_SERIAL) || defined(USE_SOFTWARE_SERIAL)
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
#elif defined(USE_SOFTWARE_SERIAL)
SoftwareSerial SerialBBC(RXD_PIN, TXD_PIN);
#else
#define SerialBBC Serial1
#endif

void setup() {
	// Init USB serial port with dummy speed value
	SerialUSB.begin(9600);

	// Init hardware or software serial port for comms with BBC/Electron
	pinMode(TXD_PIN, OUTPUT);
	pinMode(RXD_PIN, INPUT);
	SerialBBC.begin(115200);

	// Configure flow control
	pinMode(CTS_PIN, INPUT);
	pinMode(RTS_PIN, OUTPUT);
	digitalWrite(RTS_PIN, HIGH);
}

// static unsigned long last_activity = 0;

void loop() {
	int cts = 0;
	// static int written = 0;

	while (1) {
		while (digitalRead(CTS_PIN) == HIGH && SerialUSB.available()) {
			int c = SerialUSB.read();
			SerialBBC.write(c);
			SerialBBC.flush();
#ifdef DEBUG_USB_LOOPBACK
			SerialUSB.write(c);
#endif
			// last_activity = millis();
			// ++written;
		}

#ifndef IGNORE_BBC_RX
		while (SerialBBC.available()) {
			SerialUSB.write(SerialBBC.read());
			last_activity = millis();
		}
#endif

		// if (millis() - last_activity > 1000) {
		// 	SerialUSB.print("status: ");
		// 	SerialUSB.print(digitalRead(CTS_PIN) == HIGH ? "cts high" : "cts low");
		// 	SerialUSB.println();
		// 	last_activity = millis();
		// }
	}
}
