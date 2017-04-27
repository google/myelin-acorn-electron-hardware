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

#include <SPI.h>

// This code is for the Pro Micro onboard a standalone_programmer PCB.
// It talks to the CPLD over SPI, and provides a USB serial interface.

// It is also connected to the CPLD's JTAG port, and will one day be
// able to program the CPLD too.

// Pinout:

// TDO = D18 (PF7)
#define TDO_PIN 18
// TMS = D19 (PF6)
#define TMS_PIN 19
// TCK = D20 (PF5)
#define TCK_PIN 20
// TDI = D21 (PF4)
#define TDI_PIN 21

#define cart_nIRQ 6
#define cart_nNMI 7
#define cart_nRDY 8
#define cart_nRST 9
#define cpld_SS 10
#define cpld_MOSI 16
#define cpld_MISO 14
#define cpld_SCK 15

//#define NOISY

void setup() {
  // Set clock divider so we're running at full speed

  // Set pin directions for CPLD JTAG
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, INPUT_PULLUP);
  pinMode(TMS_PIN, INPUT_PULLUP);
  // Ideally we would pull this down, but we don't want a conflict
  // with an attached JTAG probe
  pinMode(TCK_PIN, INPUT);
  // In future we'll set TDI, TMS, and TCK as outputs, set TDI=1 and
  // TMS=1, and pulse TCK 5 times to reset the CPLD.

  // Set pin directions for cartridge control lines
  pinMode(cart_nIRQ, INPUT_PULLUP);
  pinMode(cart_nNMI, INPUT_PULLUP);
  pinMode(cart_nRDY, INPUT_PULLUP);
  pinMode(cart_nRST, INPUT_PULLUP);

  // Set up USB serial port
  Serial.begin(9600);

  // Set up CPLD SPI interface
  pinMode(cpld_SS, OUTPUT);
  digitalWrite(cpld_SS, HIGH);
  SPI.begin();
}

uint8_t read_byte(uint16_t A) {
  uint8_t read_nwrite = 1; // read

#ifdef NOISY
  Serial.print(read_nwrite ? "reading " : "writing ");
  Serial.println(A, HEX);
#endif
  digitalWrite(cpld_SS, LOW);
  // address space:
  // FCxx = 1111 1100 xxxx xxxx
  // FDxx = 1111 1101 xxxx xxxx
  // ROM0 = 00xx xxxx xxxx xxxx (0000-3FFF)
  // ROM1 = 01xx xxxx xxxx xxxx (4000-7FFF)
  // ROM2 = 10xx xxxx xxxx xxxx (8000-BFFF)

  uint8_t ctl = (read_nwrite ? 0x80 : 0x00) | ((A & (uint16_t)0x8000) >> (uint16_t)15);
  uint8_t ctl_r = SPI.transfer(ctl);
  uint8_t a_high = (A & (uint16_t)0x7F80) >> (uint16_t)7;
  uint8_t a_high_r = SPI.transfer(a_high);
  uint8_t a_low = (A & (uint16_t)0x007F) << (uint16_t)1;
  uint8_t a_low_r = SPI.transfer(a_low);
  uint8_t d = 0x42;
  uint8_t d_r = SPI.transfer(d);
#ifdef NOISY
  Serial.print("Sent: ");
  Serial.print(ctl, HEX);
  Serial.print(" ");
  Serial.print(a_high, HEX);
  Serial.print(" ");
  Serial.print(a_low, HEX);
  Serial.print(" ");
  Serial.print(d, HEX);
  Serial.println();
  Serial.print("ctl = ");
  Serial.print(ctl_r, HEX);
  Serial.print("; A = ");
  Serial.print(a_high_r, HEX);
  Serial.print(" ");
  Serial.print(a_low_r, HEX);
  Serial.print("; D = ");
  Serial.print(d_r, HEX);
  if (d_r > 31 && d_r < 128) {
    Serial.print(" (");
    Serial.print((char)d_r);
    Serial.print(")");
  }
  Serial.println();
#endif
  digitalWrite(cpld_SS, HIGH);

  return d_r;
}

void loop() {

#define LINE_SIZE 16
  uint8_t buf[LINE_SIZE];

  if (Serial.available()) {
    if (Serial.read() == 'R') {
      for (uint16_t addr = 0; addr < (uint16_t)32768; ++addr) {

        uint8_t d = read_byte(addr);
        buf[addr % LINE_SIZE] = d;
        Serial.print(" ");
        Serial.print(d/16, HEX);
        Serial.print(d & 0x0F, HEX);

        if ((addr % LINE_SIZE) == LINE_SIZE - 1) {
          Serial.print("  ");
          for (uint8_t i = 0; i < 16; ++i) {
            char c = (char)buf[i];
            Serial.print((c < 32 || c > 127) ? '.' : c);
          }
          Serial.println();
        }

      }
      Serial.print("\n\n");
    }
  }

}
