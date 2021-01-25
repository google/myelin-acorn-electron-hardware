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

#if defined(__AVR__)
#include <avr/power.h>
#endif
#include "src/libxsvf/libxsvf.h"

// This code allows a Pro Micro to program CPLDs by playing commands from an
// SVF file.
// Pinout:

#ifdef __AVR__

// Pro Micro pins

// TDO = A0/D18 (PF7) purple
#define TDO_PIN 18
// TMS = A1/D19 (PF6) blue
#define TMS_PIN 19
// TCK = A2/D20 (PF5) green
#define TCK_PIN 20
// TDI = A3/D21 (PF4) yellow
#define TDI_PIN 21

#else  // ARM board (experimental)

#define TDO_PIN 15
#define TMS_PIN 9
#define TCK_PIN 2
#define TDI_PIN 8

#endif

void setup() {
  // For some reason the caterina bootloader on Pro Micro clones
  // doesn't always set the clock prescaler properly.
  clock_prescale_set(clock_div_1);

  // Set pin directions for CPLD JTAG
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, INPUT_PULLUP);
  pinMode(TMS_PIN, INPUT_PULLUP);
  // Ideally we would pull this down, but we don't want a conflict
  // with an attached JTAG probe
  pinMode(TCK_PIN, INPUT);
  // In future we'll set TDI, TMS, and TCK as outputs, set TDI=1 and
  // TMS=1, and pulse TCK 5 times to reset the CPLD.

  // Set up USB serial port
  Serial.begin(9600);
}

extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

void loop() {

#define LINE_SIZE 16
  uint8_t buf[LINE_SIZE];

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
      default: {
        Serial.print("Unknown: ");
        Serial.println((char)c);
        break;
      }
    }
  }

}
