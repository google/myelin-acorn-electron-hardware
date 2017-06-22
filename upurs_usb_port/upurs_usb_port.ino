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

// ----------------------------------------------------------------------

// This code is designed to run on an Atmel ATMEGA32U4 chip (in my case, a
// $3.50 Pro Micro clone from Aliexpress), connected to a BBC Micro or Acorn
// Electron running Martin Barr's UPURS ROM software.

// --- Serial comms options ---

// UPURS uses inverted logic because it expects the User Port pins to be wired
// (with a series resistor and a diode from GND) straight to pins at RS232
// levels (+13V = 0, -13V = 1).

// If you're connecting directly to a BBC's User Port,
// USE_INVERTED_SOFTWARE_SERIAL will give you an accurate baud rate, with the
// inverted logic levels that it expects:

#define USE_INVERTED_SOFTWARE_SERIAL

// If you're connecting TXD and RXD via an inverter (perhaps a CPLD running
// the code in spi_sd_card/cpld), USE_SOFTWARE_SERIAL will give you the an
// accurate baud rate that should be compatible with UPURS:

// #define USE_SOFTWARE_SERIAL

// Alternatively you can leave both of the above undefined to use hardware
// serial, which is a bit easier on the AVR, but runs at a slightly high baud
// rate that isn't compatible with the current version of UPURS.

// --- Debug options ---

// Define DEBUG_USB_LOOPBACK to echo everything back to the USB port. This
// will break UPURS, by sometimes spending too long between characters, and
// also confuse clients, but is good when you have a logic analyzer attached
// to TXD and TXD.

// #define DEBUG_USB_LOOPBACK

// Define IGNORE_BBC_RX this to ignore anything coming back from the BBC, i.e.
// when using a CPLD to output debug pulses on the RX pin:

// #define IGNORE_BBC_RX

// Define DEBUG_REPORT_WHEN_QUIET to output a report on the state of the
// system every second when nothing else is happening:

// #define DEBUG_REPORT_WHEN_QUIET

// ----------------------------------------------------------------------

#if defined(USE_INVERTED_SOFTWARE_SERIAL) || defined(USE_SOFTWARE_SERIAL)
#include <SoftwareSerial.h>
#endif

// Serial receive -- usually PD2, D0, but we need one with a pin change
// interrupt, so we use pin 8 (PB4/PCINT4/ADC11)
#define RXD_PIN 8

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
#if defined(USE_INVERTED_SOFTWARE_SERIAL) || defined(USE_SOFTWARE_SERIAL)
	SerialBBC.begin(114000);  // 114678 bps using SoftwareSerial
#else
	SerialBBC.begin(115200);  // 117647 bps using HardwareSerial
#endif

	// Configure flow control
	pinMode(CTS_PIN, INPUT);
	pinMode(RTS_PIN, OUTPUT);
	digitalWrite(RTS_PIN, HIGH);
}

static unsigned long last_activity = 0;

void loop() {
	// static int written = 0;

	while (1) {
		while (digitalRead(CTS_PIN) == HIGH && SerialUSB.available()) {
			int c = SerialUSB.read();
			SerialBBC.write(c);
			SerialBBC.flush();
#ifdef DEBUG_USB_LOOPBACK
			SerialUSB.write(c);
#endif
			last_activity = millis();
			// ++written;
		}

#ifndef IGNORE_BBC_RX
		while (SerialBBC.available()) {
			SerialUSB.write(SerialBBC.read());
			last_activity = millis();
		}
#endif

#ifdef DEBUG_REPORT_WHEN_QUIET
		if (millis() - last_activity > 1000) {
			SerialUSB.print("status: ");
			SerialUSB.print(digitalRead(CTS_PIN) == HIGH ? "cts high" : "cts low");
			SerialUSB.println();
			last_activity = millis();
		}
#endif
	}
}
