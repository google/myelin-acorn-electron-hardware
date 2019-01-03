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

#include <SPI.h>

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

// PA08 / SERCOM2.0 (SERCOM-ALT) - D35 - cpld_MOSI
#define CPLD_MOSI_PIN 35
// PA09 / SERCOM2.1 (SERCOM-ALT) - D23 - cpld_SCK
#define CPLD_SCK_PIN 23
// PA10 / SERCOM2.2 (SERCOM-ALT) - D34 - cpld_SS
#define CPLD_SS_PIN 34
// PA11 / SERCOM2.3 (SERCOM-ALT) - D22 - cpld_MISO
#define CPLD_MISO_PIN 22

// PA14 - D5 - flash_nRESET (pull up)
#define FLASH_NRESET_PIN 5
// PA15 - D7 - flash_nREADY (pull up)
#define FLASH_NREADY_PIN 7

// PA28 - cpld_clock_from_mcu

//#define NOISY

// libxsvf (xsvftool-arduino) entry point
extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

SPIClass cpld_spi(&sercom2, CPLD_MISO_PIN, CPLD_SCK_PIN, CPLD_MOSI_PIN, SPI_PAD_0_SCK_1, SERCOM_RX_PAD_3);

uint8_t spi_transfer(uint8_t b) {
  uint8_t r = cpld_spi.transfer(b);
  Serial.print("[");
  Serial.print(b, HEX);
  Serial.print(" -> ");
  Serial.print(r, HEX);
  Serial.print("]");
  return r;
}

void flash_write(uint32_t A, uint32_t D) {
  // Write a 32-bit word to the flash, leaving allowing_arm_access == 0
  digitalWrite(CPLD_SS_PIN, LOW);
  spi_transfer((uint8_t)(0x00 | ((A & 0x3f0000L) >> 16L)));  // allowing_arm_access, rnw, A[21:16]
  spi_transfer((uint8_t)((A & 0xff00L) >> 8L));  // A[15:8]
  spi_transfer((uint8_t)(A & 0xffL));  // A[7:0]
  spi_transfer((uint8_t)((D & 0xff000000L) >> 24L));  // D[31:24]
  spi_transfer((uint8_t)((D & 0xff0000L) >> 16L));  // D[23:16]
  spi_transfer((uint8_t)((D & 0xff00L) >> 8L));  // D[15:8]
  spi_transfer((uint8_t)(D & 0xffL));  // D[7:0]
  spi_transfer(0);
  digitalWrite(CPLD_SS_PIN, HIGH);
}

uint32_t flash_read(uint32_t A) {
  // Read a 32-bit word from the flash, leaving allowing_arm_access == 0
  digitalWrite(CPLD_SS_PIN, LOW);
  spi_transfer((uint8_t)(0x40 | ((A & 0x3f0000) >> 16)));  // allowing_arm_access, rnw, A[21:16]
  spi_transfer((uint8_t)((A & 0xff00) >> 8));  // A[15:8]
  spi_transfer((uint8_t)(A & 0xff));  // A[7:0]
  spi_transfer(0);
  uint32_t D = ((uint32_t)spi_transfer(0)) << 24;  // D[31:24]
  D |= ((uint32_t)spi_transfer(0)) << 16;  // D[23:16]
  D |= ((uint32_t)spi_transfer(0)) << 8;  // D[15:8]
  D |= ((uint32_t)spi_transfer(0));  // D[7:0]
  digitalWrite(CPLD_SS_PIN, HIGH);
  return D;
}

void flash_unlock() {
  // Reset allowing_arm_access to 1 in the CPLD
  digitalWrite(CPLD_SS_PIN, LOW);
  spi_transfer(0xff);
  digitalWrite(CPLD_SS_PIN, HIGH);
}

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
  pinMode(FLASH_NRESET_PIN, OUTPUT);
  digitalWrite(FLASH_NRESET_PIN, LOW);
  digitalWrite(FLASH_NRESET_PIN, HIGH);
  pinMode(FLASH_NRESET_PIN, INPUT_PULLUP);
  pinMode(FLASH_NREADY_PIN, INPUT_PULLUP);

  // Set up SPI comms on SERCOM2 with CPLD: MOSI=PA08, SCK=PA09, SS=PA10, MISO=PA11
  // pinMode(CPLD_MOSI_PIN, OUTPUT);
  // pinMode(CPLD_SCK_PIN, OUTPUT);
  // pinMode(CPLD_MISO_PIN, INPUT);
  pinMode(CPLD_SS_PIN, OUTPUT);
  digitalWrite(CPLD_SS_PIN, HIGH);
  cpld_spi.begin();
  pinPeripheral(CPLD_MOSI_PIN, PIO_SERCOM_ALT);
  pinPeripheral(CPLD_SCK_PIN, PIO_SERCOM_ALT);
  pinPeripheral(CPLD_MISO_PIN, PIO_SERCOM_ALT);
  cpld_spi.beginTransaction(SPISettings(24000000L, MSBFIRST, SPI_MODE0));

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
      case 'I': {
        Serial.println("IDENTIFY FLASH");
        flash_write(0x55, 0x00980098L);
        Serial.println(" <-- write");
        for (uint32_t cfi_addr = 0x10; cfi_addr <= 0x50; ++cfi_addr) {
          Serial.println(flash_read(cfi_addr), HEX);
        }
        flash_unlock();
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
