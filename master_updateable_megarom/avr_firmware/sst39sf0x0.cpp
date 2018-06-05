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


#include <stdint.h>
#include "megarom.h"

// #define SHOW_ALL_SPI_TRANSFERS
// #define VERBOSE_FLASH_DEBUG

// start an SPI transaction
static inline void spi_select() {
  digitalWrite(SPI_SS_PIN, LOW);
}

// end an SPI transaction
static inline void spi_deselect() {
  digitalWrite(SPI_SS_PIN, HIGH);
}

static inline uint8_t spi_transfer(uint8_t b) {
#ifdef SHOW_ALL_SPI_TRANSFERS
  Serial.print("[");
  Serial.print(b, HEX);
  Serial.print("-");
#endif
  b = SPI.transfer(b);
#ifdef SHOW_ALL_SPI_TRANSFERS
  Serial.print(b, HEX);
  Serial.print("]");
#endif
  return b;
}

static void reset_spi() {
  // synchronous reset -- clock SCK while SS is high
  spi_deselect();
  SPI.transfer(0);
}

// write a single byte and leave the chip locked for more SPI access
static void write_byte(uint32_t address, uint8_t data) {
  // 19 address bits, rnw bit, 8 data bits, 4 zeros
  // A18:11, A10:3, {A2:0, rnw, D7:4}, {D3:0, 0000}
  spi_select();
  uint8_t i = spi_transfer((uint8_t)(address >> 11));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 0 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return;
  }
  i = spi_transfer((uint8_t)(address >> 3));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 1 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return;
  }
  i = spi_transfer((uint8_t)(address << 5) | (data >> 4));
  if ((i & 0xe0) != 0x40) {
    Serial.print("SPI error; expected byte 2 & e0 == 40 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return;
  }
  spi_transfer(data << 4);
  spi_deselect();
#ifdef VERBOSE_FLASH_DEBUG
  Serial.print("w ");
  Serial.print(address, HEX);
  Serial.print(" ");
  Serial.println(data, HEX);
#endif
}

// read a single byte and leave the chip locked for more SPI access
uint8_t read_byte(uint32_t address) {
  // 19 address bits, rnw bit, 8 data bits, 4 zeros
  // A18:11, A10:3, A2:0, rnw, D7:4, D3:0, 0000
  spi_select();
  uint8_t i = spi_transfer((uint8_t)(address >> 11));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 0 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  i = spi_transfer((uint8_t)(address >> 3));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 1 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  i = spi_transfer((uint8_t)(address << 5) | 0x10);
  if ((i & 0xe0) != 0x40) {
    Serial.print("SPI error; expected byte 2 & e0 == 40 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  uint8_t r = spi_transfer(0);
  spi_deselect();
#ifdef VERBOSE_FLASH_DEBUG
  Serial.print("r ");
  Serial.print(address, HEX);
  Serial.print(" ");
  Serial.println(r, HEX);
#endif
  return r;
}

// read a single byte and return control of the chip to the BBC
uint8_t read_byte_and_unlock(uint32_t address) {
  // 19 address bits, rnw bit, 8 data bits, 0001
  // A18:11, A10:3, A2:0, rnw, D7:4, D3:0, 0001
  spi_select();
  uint8_t i = spi_transfer((uint8_t)(address >> 11));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 0 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  i = spi_transfer((uint8_t)(address >> 3));
  if (i != 0x55) {
    Serial.print("SPI error; expected byte 1 == 55 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  i = spi_transfer((uint8_t)(address << 5) | (uint8_t)0x10);
  if ((i & 0xe0) != 0x40) {
    Serial.print("SPI error; expected byte 2 & e0 == 40 but got ");
    Serial.println(i, HEX);
    spi_deselect();
    return 0;
  }
  uint8_t r = spi_transfer((uint8_t)0x01);
  spi_deselect();
#ifdef VERBOSE_FLASH_DEBUG
  Serial.print("R ");
  Serial.print(address, HEX);
  Serial.print(" ");
  Serial.println(r, HEX);
#endif
  return r;
}

// repeatedly read an address until bit 6 stops toggling
void wait_toggle(uint32_t address) {
  uint8_t last = read_byte(address);
  while (1) {
    uint8_t current = read_byte(address);
    if ((last & 0x40) == (current & 0x40)) {
      return;
    }
    last = current;
  }
}

// returns 0 on failure, or the chip ID: B5/B6/B7 for SST39SF010A/020A/040
// (actually whatever reads back from address 1 if address 0 == 0xbf)
uint8_t identify_chip() {
  reset_spi();
  Serial.print("test: *0 = ");
  Serial.println(read_byte(0), HEX);
  Serial.print("test: *1 = ");
  Serial.println(read_byte(1), HEX);
  Serial.print("test: *2 = ");
  Serial.println(read_byte(2), HEX);
  Serial.print("test: *3 = ");
  Serial.println(read_byte(3), HEX);
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte((uint32_t)0x5555L, 0x90);
  uint8_t manufacturer_id = read_byte(0L);
  uint8_t device_id = read_byte(1L);
  write_byte((uint32_t)0x5555L, 0xF0);
  if (manufacturer_id != 0xbf) {
    Serial.print("manufacturer id ");
    Serial.println(manufacturer_id, HEX);
    return 0;
  }
  return device_id;
}

// more usable way to detect what's going on with the chip
uint32_t chip_size() {
  uint8_t device_id = identify_chip();

  switch (device_id) {
    case 0xb5: return 128*1024L;
    case 0xb6: return 256*1024L;
    case 0xb7: return 512*1024L;
    default: return 0L;
  }
}

// wipe the entire chip
void erase_entire_chip() {
  reset_spi();
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte((uint32_t)0x5555L, 0x80);
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte((uint32_t)0x5555L, 0x10);
  wait_toggle(0x5555L);
}

// wipe a single sector of SECTOR_SIZE bytes
void erase_sector(uint32_t address) {
  reset_spi();
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte((uint32_t)0x5555L, 0x80);
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte(address, 0x30);
  wait_toggle(address);
}

// program a single byte (requires that the byte be erased to 0xff first)
void program_byte(uint32_t address, uint8_t data) {
  write_byte((uint32_t)0x5555L, 0xAA);
  write_byte((uint32_t)0x2AAAL, 0x55);
  write_byte((uint32_t)0x5555L, 0xA0);
  write_byte(address, data);
  wait_toggle(address);
}

// check that the range from start_addr to end_addr-1 is blank
bool is_range_blank(uint32_t start_addr, uint32_t end_addr) {
  reset_spi();
  for (uint32_t addr = start_addr; addr < end_addr; ++addr) {
    if (read_byte_and_unlock(addr) != 0xff) {
      return false;
    }
  }
  return true;
}

bool is_chip_blank() {
  return is_range_blank(0L, CHIP_SIZE);
}

// erase the 4k block containing address if the block isn't blank
void erase_sector_if_necessary(uint32_t address) {
  address &= SECTOR_MASK;
  if (is_range_blank(address, address + SECTOR_SIZE)) {
    return;
  }
  erase_sector(address);
}

// erase all sectors in a range (will erase more than just the bytes
// from start_addr to end_addr-1 if they aren't on sector boundaries).
void erase_range_if_necessary(uint32_t start_addr, uint32_t end_addr) {
  for (uint32_t sector_addr = start_addr & SECTOR_MASK;
       sector_addr <= ((end_addr - 1) & SECTOR_MASK);
       sector_addr += SECTOR_SIZE) {
    erase_sector_if_necessary(sector_addr);
  }
}
