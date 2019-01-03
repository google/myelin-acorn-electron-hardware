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

// For pinPeripheral(), so we can change PINMUX
#include "wiring_private.h"

// For libxsvf, so we can program the CPLD
#include "libxsvf.h"

// This code is for the ATSAMD21E18A onboard an a3000_rom_emulator PCB.
// Functions provided:
// - USB serial interface for all control
// - USB SVF+JTAG interface to program the CPLD
// - CPLD clock generation (24MHz)

// Pinout:

// Pin assignments from the Adafruit Circuit Playground Express (ATSAMD21G18A)
// are used here.  Be careful mapping these to actual pins, because the G18A and
// our E18A have different pinouts.

// Mapping: A(x) = D(x+14), e.g. A0 = D14 and A10 = D24

// CPLD JTAG port

// PA04 - D24 / A10
#define TDO_PIN 24
// PA06 - D16 / A2
#define TMS_PIN 16
// PA05 - D15 / A1
#define TCK_PIN 15
// PA07 - D17 / A3
#define TDI_PIN 17

// CPLD comms

// PA08 - D35 - cpld_MOSI
#define CPLD_MOSI_PIN 35
// PA09 - D23 - cpld_SCK
#define CPLD_SCK_PIN 23
// PA10 - D34 - cpld_SS
#define CPLD_SS_PIN 34
// PA11 - D22 - cpld_MISO
#define CPLD_MISO_PIN 22

// PA14 - D5 - flash_nRESET (pull up)
#define FLASH_NRESET_PIN 5
// PA15 - D7 - flash_nREADY (pull up)
#define FLASH_NREADY_PIN 7

// PA28 - cpld_clock_from_mcu

//#define NOISY

// libxsvf (xsvftool-arduino) entry point
extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

void setup() {
  // Set pin directions for CPLD JTAG.
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, OUTPUT);
	digitalWrite(TDI_PIN, HIGH);
  pinMode(TMS_PIN, OUTPUT);
	digitalWrite(TMS_PIN, HIGH);
  pinMode(TCK_PIN, OUTPUT);
	digitalWrite(TCK_PIN, LOW);

  // Set up pullups for flash pins
  pinMode(FLASH_NRESET_PIN, INPUT_PULLUP);
  pinMode(FLASH_NREADY_PIN, INPUT_PULLUP);

  // Set up USB serial port
  Serial.begin(9600);

}

uint8_t serial_get_uint8() {
  while (!Serial.available());
  return (uint8_t)Serial.read();
}

uint16_t serial_read_addr() {
  uint16_t addr = (uint16_t)serial_get_uint8() << 8;
  addr |= (uint16_t)serial_get_uint8();
  return addr;
}

// Disable USB serial commands (CPLD programming etc) by commenting this out:
#define ENABLE_USB_SERIAL

void loop() {

#ifdef ENABLE_USB_SERIAL
  static uint8_t serial_active = 0;
  static unsigned long serial_active_when = 0;
  if (!Serial.dtr()) {
    if (serial_active) {
      serial_active = 0;
    }
  } else if (!serial_active) {
    // USB serial connection is active
    serial_active_when = millis();
    serial_active = 1;
  } else if (serial_active == 1 && millis() - serial_active_when > 10) {
    // Serial port should have settled by now
    Serial.println(SystemCoreClock);
    serial_active = 2;
  } else if (serial_active == 2) {
    // Serial port is actually open.
  }

  if (Serial.available()) {
    int c = Serial.read();
    switch (c) {
      case 'C': {
        // program CPLD
        Serial.println("SEND SVF");
        arduino_play_svf(TMS_PIN, TDI_PIN, TDO_PIN, TCK_PIN, -1);
        Serial.println("SVF DONE");
        break;
      }
      case 'Z': {
        // USB test
        Serial.println("USB TEST");
        bool fail = false;
        for (uint32_t i = 0; i < 128 * 1024L; ++i) {
          // Serial.println(i);
          unsigned long now = millis();
          while (!Serial.available()) {
            if (millis() - now > 1000) {
              Serial.println("Failing b/c no input for 1000 ms");
              fail = true;
              break;
            }
          }
          if (fail) {
            Serial.println("fail");
            break;
          }

          Serial.write(Serial.read());
          if (i && !(i % 8192)) {
            // simulate delay every 8k
            delay(1000);
          }
        }
        Serial.println("TEST DONE");
        break;
      }
      default: {
        Serial.print("Unknown: ");
        Serial.println((char)c);
        break;
      }
    }
  }
#endif // ENABLE_USB_SERIAL

}
