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
#include <avr/power.h>
#include "libxsvf.h"

// This code is for the Pro Micro onboard a standalone_programmer PCB.
// It talks to the CPLD over SPI, and provides a USB serial interface.

// It can also program the CPLD over its JTAG port.

// Pinout:

// CPLD JTAG port

// TDO = D18 (PF7)
#define TDO_PIN 18
// TMS = D19 (PF6)
#define TMS_PIN 19
// TCK = D20 (PF5)
#define TCK_PIN 20
// TDI = D21 (PF4)
#define TDI_PIN 21

// Cartridge pins

#define cart_nIRQ 6
#define cart_nNMI 7
#define cart_nRDY 8
#define cart_nRST 9

// CPLD SPI port

#define cpld_SS 10
#define cpld_MOSI 16
#define cpld_MISO 14
#define cpld_SCK 15

//#define NOISY

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
#ifdef NOISY
  uint8_t ctl_r =
#endif
    SPI.transfer(ctl);
  uint8_t a_high = (A & (uint16_t)0x7F80) >> (uint16_t)7;
#ifdef NOISY
  uint8_t a_high_r =
#endif
    SPI.transfer(a_high);
  uint8_t a_low = (A & (uint16_t)0x007F) << (uint16_t)1;
#ifdef NOISY
  uint8_t a_low_r =
#endif
    SPI.transfer(a_low);
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

uint8_t write_byte(uint16_t A, uint8_t D) {
  uint8_t read_nwrite = 0; // write

  digitalWrite(cpld_SS, LOW);
  // address space:
  // FCxx = 1111 1100 xxxx xxxx
  // FDxx = 1111 1101 xxxx xxxx
  // ROM0 = 00xx xxxx xxxx xxxx (0000-3FFF)
  // ROM1 = 01xx xxxx xxxx xxxx (4000-7FFF)
  // ROM2 = 10xx xxxx xxxx xxxx (8000-BFFF)

  uint8_t ctl = (read_nwrite ? 0x80 : 0x00) | ((A & (uint16_t)0x8000) >> (uint16_t)15);
  SPI.transfer(ctl);
  uint8_t a_high = (A & (uint16_t)0x7F80) >> (uint16_t)7;
  SPI.transfer(a_high);
  uint8_t a_low = (A & (uint16_t)0x007F) << (uint16_t)1;
  SPI.transfer(a_low);
  uint8_t d_r = SPI.transfer(D);
  digitalWrite(cpld_SS, HIGH);

  return d_r;
}

enum ChipType {
  UNKNOWN = 0,
  SST39SF010,
  SST39SF020,
  SST39SF040
};

ChipType identify_chip() {
  write_byte(0x1555, 0xAA);
  write_byte(0x2AAA, 0x55);
  write_byte(0x1555, 0x90);
  if (read_byte(0x0000) == 0xBF) {
    uint8_t chip_id = read_byte(0x0001);
    Serial.print("Chip ID: ");
    Serial.println(chip_id, HEX);
    ChipType t = ChipType::UNKNOWN;
    switch (chip_id) {
      case 0xB5: Serial.println("SST39SF010"); t = ChipType::SST39SF010; break;
      case 0xB6: Serial.println("SST39SF020"); t = ChipType::SST39SF020; break;
      case 0xB7: Serial.println("SST39SF040"); t = ChipType::SST39SF040; break;
    }
    write_byte(0x1555, 0xAA);
    write_byte(0x2AAA, 0x55);
    write_byte(0x1555, 0xF0);
    return t;
  }

  Serial.println("Flash identify failed; maybe not an SST39SF0x0");
  return ChipType::UNKNOWN;
}

void wait_toggle_bit_sst39sf010() {
  while (1) {
    uint8_t a = read_byte(0) & (1<<6);
    uint8_t b = read_byte(0) & (1<<6);
    if (!(a ^ b)) {
      break;
    } else {
      // Serial.println("waiting");
    }
  }
}

void erase_sst39sf010(uint16_t start) {
  Serial.print("Erasing chunk starting ");
  Serial.println(start);
  write_byte(0x1555, 0xAA);
  write_byte(0x2AAA, 0x55);
  write_byte(0x1555, 0x80);
  write_byte(0x1555, 0xAA);
  write_byte(0x2AAA, 0x55);
  write_byte(start, 0x30);
  wait_toggle_bit_sst39sf010();
  Serial.println("Erased");
}

void program_sst39sf010_byte(uint16_t A, uint8_t D) {
  write_byte(0x1555, 0xAA);
  write_byte(0x2AAA, 0x55);
  write_byte(0x1555, 0xA0);
  write_byte(A, D);
  wait_toggle_bit_sst39sf010();
}

void program_sst39sf010(uint16_t start, uint16_t size) {
  if (identify_chip() != ChipType::SST39SF010) {
    Serial.println("don't know how to program this chip");
    return;
  }
  // program now!
  uint16_t chunk_size = 4096;
  if (start % chunk_size) {
    Serial.println("address does not start on a correct boundary");
    return;
  }
  if (size % chunk_size) {
    Serial.println("block size is not a multiple of the flash block size");
    return;
  }

  Serial.print("Programming ");
  Serial.print(size);
  Serial.print(" bytes at ");
  Serial.println(start);

  for (uint16_t pos = start; pos < start + size; pos += chunk_size) {
    erase_sst39sf010(pos);
    for (uint16_t ptr = pos; ptr < pos + chunk_size; ++ptr) {
      while (!Serial.available());
      program_sst39sf010_byte(ptr, Serial.read());
      Serial.write(read_byte(ptr));
    }
  }
}

extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

uint8_t serial_get_uint8() {
  while (!Serial.available());
  return (uint8_t)Serial.read();
}

uint16_t serial_read_addr() {
  uint16_t addr = (uint16_t)serial_get_uint8() << 8;
  addr |= (uint16_t)serial_get_uint8();
  return addr;
}

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
      case 'I': {
        // identify attached flash
        Serial.println("IDENTIFY");
        identify_chip();
        Serial.println("ID DONE");
        break;
      }
      case 'r': {
        // single byte read
        Serial.print("r");
        uint16_t addr = serial_read_addr();
        Serial.print((char)read_byte(addr));
        break;
      }
      case 'R': {
        // read out ROM
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
        break;
      }
      case 'S': {
        // fast ROM readout
        Serial.print("ROM[");
        for (uint16_t addr = 0; addr < (uint16_t)32768; ++addr) {
          uint8_t d = read_byte(addr);
          Serial.write(d);
        }
        Serial.println("]ROM DONE");
        break;
      }
      case 'w': {
        // single byte write
        Serial.print("w");
        uint16_t addr = serial_read_addr();
        uint8_t data = serial_get_uint8();
        write_byte(addr, data);
        Serial.print(".");
        break;
      }
      case 'W': {
        // write ROM
        Serial.println("WRITE ROM");
        program_sst39sf010(0, 32768);
        Serial.println("WRITE DONE");
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

}
