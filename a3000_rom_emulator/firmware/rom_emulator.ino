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
// - CPLD clock generation (48MHz)

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
#define CPLD_SS_PORT (PORT->Group[0])
#define CPLD_SS_PORT_BIT 10
#define CPLD_SS_SET() do { CPLD_SS_PORT.OUTSET.reg = 1 << CPLD_SS_PORT_BIT; } while (0)
#define CPLD_SS_CLEAR() do { CPLD_SS_PORT.OUTCLR.reg = 1 << CPLD_SS_PORT_BIT; } while (0)
// #define CPLD_SS_CLEAR() digitalWrite(CPLD_SS_PIN, LOW)
// #define CPLD_SS_SET() digitalWrite(CPLD_SS_PIN, HIGH)
// PA11 / SERCOM2.3 (SERCOM-ALT) - D22 - cpld_MISO
#define CPLD_MISO_PIN 22

// PA14 - D5 - flash_nRESET (pull up)
#define FLASH_NRESET_PIN 5
// PA15 - D7 - flash_nREADY (pull up)
#define FLASH_NREADY_PIN 7

// PA28 - D4 - cpld_clock_from_mcu (clock output)
#define CPLD_CLOCK_FROM_MCU_PIN 4


// Uncomment this to show every byte sent and received over SPI
// #define SHOW_ALL_SPI_TRANSFERS

// Uncomment this to show all flash reads and writes
// #define SHOW_ALL_FLASH_ACCESS

// Disable USB serial commands (CPLD programming etc) by commenting this out:
#define ENABLE_USB_SERIAL

// Uncomment this to disable programming flash (for performance testing)
// #define DEBUG_DONT_PROGRAM_FLASH

// Uncomment this to fake out fetching data from USB (for performance testing)
// #define DEBUG_DONT_GET_USB_DATA


// We have the S29GL064S70DHI010 (S29GL064S 70-ns D-LAE064-BGA-pkg H-halogen/lead-free I-industrial 01-uniform sector 0-tray)
// 2 x 64 (4Mwordx16) megabit flash chips, so addresses are 22 bits long
#define CHIP_SIZE (4 * 1048576L)
// Sectors are 32k word / 64kB long
#define SECTOR_SIZE (32768L)
#define SECTOR_MASK ((CHIP_SIZE * 4 - 1) & ~(SECTOR_SIZE - 1))


// libxsvf (xsvftool-arduino) entry point
extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

// SPI on SERCOM2 to talk to the CPLD at 24MHz
SPIClass cpld_spi(&sercom2, CPLD_MISO_PIN, CPLD_SCK_PIN, CPLD_MOSI_PIN, SPI_PAD_0_SCK_1, SERCOM_RX_PAD_3);

// Alternate function: UART to talk to host
Uart cpld_uart(&sercom2, CPLD_MISO_PIN, CPLD_MOSI_PIN, SERCOM_RX_PAD_3, UART_TX_PAD_0);
// to enable: cpld_uart.begin(); then same pinPeripheral calls as for SPI (because we're using the same sercom pins/pads, just a different function.)

enum { NOTHING_SELECTED, SPI_SELECTED, UART_SELECTED } spi_port_state = NOTHING_SELECTED;

// Set MOSI/SCK/MISO/SS pins up for SPI comms with CPLD
void select_spi() {
  if (spi_port_state == SPI_SELECTED) return;
  spi_port_state = SPI_SELECTED;
  if (Serial.dtr()) Serial.println("select spi");
  sercom2.disableSPI();  // disable SERCOM so we can write registers
  cpld_spi.begin();
  pinPeripheral(CPLD_MOSI_PIN, PIO_SERCOM_ALT);
  pinPeripheral(CPLD_SCK_PIN, PIO_SERCOM_ALT);
  pinPeripheral(CPLD_MISO_PIN, PIO_SERCOM_ALT);
  cpld_spi.beginTransaction(SPISettings(12000000L, MSBFIRST, SPI_MODE0));
}

// Set MOSI/MISO pins up for UART comms with host machine (forwarded by CPLD)
void select_uart() {
  if (spi_port_state == UART_SELECTED) return;
  spi_port_state = UART_SELECTED;
  if (Serial.dtr()) Serial.println("select uart");
  sercom2.disableSPI();  // disable SERCOM so we can write registers
  cpld_uart.begin(57600);
  pinPeripheral(CPLD_MOSI_PIN, PIO_SERCOM_ALT);
  pinPeripheral(CPLD_MISO_PIN, PIO_SERCOM_ALT);
  // disable all interrupts that begin() enables
  SERCOM2->USART.INTENCLR.reg = SERCOM_USART_INTENSET_DRE |
                                SERCOM_USART_INTENSET_RXC |
                                SERCOM_USART_INTENSET_ERROR;

}

// Send/receive a byte over SPI, optionally dumping details to the serial port
uint8_t spi_transfer(uint8_t b) {
  uint8_t r = cpld_spi.transfer(b);
#ifdef SHOW_ALL_SPI_TRANSFERS
  Serial.print("[");
  Serial.print(b, HEX);
  Serial.print(" -> ");
  Serial.print(r, HEX);
  Serial.print("]");
#endif
  return r;
}

// Write a 32-bit word to the flash chips
void flash_write(uint32_t A, uint32_t D) {
  // Write a 32-bit word to the flash, leaving allowing_arm_access == 0
  CPLD_SS_CLEAR();
  spi_transfer((uint8_t)(0x00 | ((A & 0x3f0000L) >> 16L)));  // allowing_arm_access, rnw, A[21:16]
  spi_transfer((uint8_t)((A & 0xff00L) >> 8L));  // A[15:8]
  spi_transfer((uint8_t)(A & 0xffL));  // A[7:0]
  spi_transfer((uint8_t)((D & 0xff000000L) >> 24L));  // D[31:24]
  spi_transfer((uint8_t)((D & 0xff0000L) >> 16L));  // D[23:16]
  spi_transfer((uint8_t)((D & 0xff00L) >> 8L));  // D[15:8]
  spi_transfer((uint8_t)(D & 0xffL));  // D[7:0]
  spi_transfer(0);
  CPLD_SS_SET();
#ifdef SHOW_ALL_FLASH_ACCESS
  Serial.print("Flash write *0x");
  Serial.print(A, HEX);
  Serial.print(" = ");
  Serial.println(D, HEX);
#endif
}

// Write a 16-bit word to the same address on both flash chips
void flash_write_both(uint32_t A, uint16_t D) {
  uint32_t D32 = D;
  flash_write(A, D32 | (D32 << 16));
}

// Read a 32-bit word from the flash chips
uint32_t flash_read(uint32_t A) {
  // Read a 32-bit word from the flash, leaving allowing_arm_access == 0
  CPLD_SS_CLEAR();
  spi_transfer((uint8_t)(0x40 | ((A & 0x3f0000) >> 16)));  // allowing_arm_access, rnw, A[21:16]
  spi_transfer((uint8_t)((A & 0xff00) >> 8));  // A[15:8]
  spi_transfer((uint8_t)(A & 0xff));  // A[7:0]
  spi_transfer(0);
  uint32_t D = ((uint32_t)spi_transfer(0)) << 24;  // D[31:24]
  D |= ((uint32_t)spi_transfer(0)) << 16;  // D[23:16]
  D |= ((uint32_t)spi_transfer(0)) << 8;  // D[15:8]
  D |= ((uint32_t)spi_transfer(0));  // D[7:0]
  CPLD_SS_SET();
#ifdef SHOW_ALL_FLASH_ACCESS
  Serial.print("Flash read *0x");
  Serial.print(A, HEX);
  Serial.print(" == ");
  Serial.println(D, HEX);
#endif
  return D;
}

// 7 bits: reset_arm (0x40), use_la21 (0x20), use_la20 (0x10), bank:4
static uint8_t flash_bank = 0;
#define RESET_ARM 0x40
#define BANK_4M   0x30
#define BANK_2M   0x10
#define BANK_1M   0x00

static uint8_t banks[8] = {
  // initial layout: four 1M banks, two 2M banks, two 4M banks = 16M total.
  BANK_1M | 0,
  BANK_1M | 1,
  BANK_1M | 2,
  BANK_1M | 3,
  BANK_2M | 4,
  BANK_2M | 6,
  BANK_4M | 8,
  BANK_4M | 12,
};

// Tell the CPLD to return control of the flash to the host machine
void flash_unlock() {
  select_spi();

  // Reset allowing_arm_access to 1 in the CPLD
  CPLD_SS_CLEAR();
  spi_transfer(0x80 | banks[flash_bank]);
  CPLD_SS_SET();
}

// Select a particular flash bank
void select_flash_bank(uint8_t bank) {
  if (bank > 7) bank = 0;
  flash_bank = bank;
  if (Serial.dtr()) {
    Serial.print("Selecting flash bank ");
    Serial.println(flash_bank);
  }
  flash_unlock();
}

// Pulse NRESET on the flash chips
void flash_reset() {
  pinMode(FLASH_NRESET_PIN, OUTPUT);
  digitalWrite(FLASH_NRESET_PIN, LOW);
  digitalWrite(FLASH_NRESET_PIN, HIGH);
  pinMode(FLASH_NRESET_PIN, INPUT_PULLUP);
}

// System startup
void setup() {

  // Set up fast SPI comms on SERCOM2 with CPLD
  pinMode(CPLD_SS_PIN, OUTPUT);
  CPLD_SS_SET();
  select_spi();

  // Select configured flash_bank
  flash_unlock();

  // I made a poor pin choice in the v1 board, putting cpld_clock_from_mcu on
  // PA28, which is GCLK_IO[0].  It looks like only GCLK0 can drive GCLK_MAIN,
  // so to change the clock frequency output on PA28, we need to slow down the
  // CPU.

  // DIV=2 gives 24MHz, but breaks USB
  // DIV=0 gives 48MHz
  GCLK->GENDIV.reg = GCLK_GENDIV_ID(0) | GCLK_GENDIV_DIV(0);
  while (GCLK->STATUS.reg & GCLK_STATUS_SYNCBUSY);

  // Update with same settings as in Arduino SAMD startup.c, but also
  // GCLK_GENCTRL_OE, to output the clock on GCLK_IO[0].  (Also, is there a
  // way to read the current settings for a GCLK, so I can just set the OE bit
  // without having to repeat the config?)
  GCLK->GENCTRL.reg = GCLK_GENCTRL_ID(0) |
                      GCLK_GENCTRL_SRC_DFLL48M |
                      GCLK_GENCTRL_OE |
                      GCLK_GENCTRL_IDC |
                      GCLK_GENCTRL_GENEN;
  while (GCLK->STATUS.reg & GCLK_STATUS_SYNCBUSY);

  // enable GCLK_IO[0] on PA28 (cpld_clock_from_mcu)
  pinPeripheral(CPLD_CLOCK_FROM_MCU_PIN, PIO_AC_CLK);

  // Set pin directions for CPLD JTAG.
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, OUTPUT);
	digitalWrite(TDI_PIN, HIGH);
  pinMode(TMS_PIN, OUTPUT);
	digitalWrite(TMS_PIN, HIGH);
  pinMode(TCK_PIN, OUTPUT);
	digitalWrite(TCK_PIN, LOW);

  // Set up pullups for flash pins
  flash_reset();
  pinMode(FLASH_NREADY_PIN, INPUT_PULLUP);

  // Set up USB serial port
  Serial.begin(9600);

  select_uart();
}

// Read a byte from the USB serial port
uint8_t serial_get_uint8() {
  while (!Serial.available());
  return (uint8_t)Serial.read();
}

// // Read a big-endian uint32 from the USB serial port
// uint32_t serial_get_uint32() {
//   uint32_t v = (uint32_t)serial_get_uint8() << 24L;
//   v |= (uint32_t)serial_get_uint8() << 16L;
//   v |= (uint32_t)serial_get_uint8() << 8L;
//   v |= (uint32_t)serial_get_uint8();
//   return v;
// }

// // Write a big-endian uint32 to the USB serial port
// void serial_put_uint32(uint32_t v) {
//   Serial.write((uint8_t)((v & 0xFF000000) >> 24));
//   Serial.write((uint8_t)((v & 0xFF0000) >> 16));
//   Serial.write((uint8_t)((v & 0xFF00) >> 8));
//   Serial.write((uint8_t)(v & 0xFF));
// }

// Read a little-endian uint32 from the USB serial port
uint32_t serial_get_uint32() {
  uint32_t v = (uint32_t)serial_get_uint8();
  v |= (uint32_t)serial_get_uint8() << 8L;
  v |= (uint32_t)serial_get_uint8() << 16L;
  v |= (uint32_t)serial_get_uint8() << 24L;
  return v;
}

// Write a big-endian uint32 to the USB serial port
void serial_put_uint32(uint32_t v) {
  Serial.write((uint8_t)(v & 0xFF));
  Serial.write((uint8_t)((v & 0xFF00) >> 8));
  Serial.write((uint8_t)((v & 0xFF0000) >> 16));
  Serial.write((uint8_t)((v & 0xFF000000) >> 24));
}

// USB chunks: read 16kB at a time
#define CHUNK_SIZE (16384 / 4)
#define BUF_SIZE (CHUNK_SIZE + 1)
// Program 512 bytes (128 words) at a time
#define PROGRAM_BLOCK_SIZE 128

// TODO move all these vars into the programming code -- we have more RAM in this chip than the atmega32u4 this was originally written for
static uint32_t read_buf[BUF_SIZE];

// count of chars read into read_buf
static int buf_pos = 0;

// flash chip size
uint32_t chip_end = 0L;

// for range programming state
uint32_t range_start = 0L, range_end = 0L; // range left to program
int range_chunk_size = 0; // how many bytes to expect in the buffer


// true if we've seen dtr=1, false if we're disconnected or reset
static bool connected = false;

void reset() {
  // reset read buffer
  buf_pos = 0;
  // reset connection flag
  connected = false;
  // clear out any unread input
  while (Serial.available() && !Serial.dtr()) {
    Serial.read();
  }
  // leave flash accessible by host machine
  flash_unlock();
  Serial.println("OK");
  select_uart();
}

// Return the number of bytes of flash on this board, i.e. double the byte count of one chip
uint32_t chip_size() {
  select_spi();
  flash_write_both(0x55, 0x0098L);  // Enter CFI mode
  uint32_t size_log2 = flash_read(0x27) & 0xffff;
  flash_write_both(0x00, 0xf0);  // Exit CFI mode
  flash_unlock();  // Allow host access again

  uint32_t size = 1;
  while (size_log2--) size <<= 1;

  return size * 2;  // Double it because we have two flash chips
}

// returns true if we're disconnected and have been reset
bool check_disconnect() {
  if (Serial.dtr()) {
    return false; // all is well
  }

  // remote has disconnected -- reset everything / keep it reset
  reset();
  return true;
}

// request bytes from remote; range_start and range_end are word addresses
bool get_range(uint32_t range_start, uint32_t range_end) {
#ifdef DEBUG_DONT_GET_USB_DATA
  return true;
#endif
  if (check_disconnect()) return false;

  Serial.print(range_start * 4, DEC);
  Serial.print("+");
  Serial.println((range_end - range_start) * 4, DEC);  // Ask for byte count for compatibility with 8-bit code

  long start_time = millis();
  buf_pos = 0;

  uint32_t bytes_to_receive = (range_end - range_start) * 4;
  uint32_t byte_count = 0;

  while (byte_count < bytes_to_receive) { // buf_pos < (int)(range_end - range_start)) {
    if (check_disconnect()) return false;
    if (millis() - start_time > 1000) {
      Serial.print("Timeout reading data after ");
      Serial.print(buf_pos);
      Serial.println(" bytes");
      return false;
    }

    byte_count += Serial.readBytes(((char *)read_buf) + byte_count, bytes_to_receive - byte_count);
  }
  buf_pos += byte_count / 4;

  // Endian swap.  Disabled this because I think the data coming from the host may
  // already have the correct endianness.

  // for (uint32_t pos = 0; pos < (range_end - range_start); ++pos) {
  //   read_buf[pos] =
  //     ((read_buf[pos] & 0xFF000000L) >> 24)
  //     | ((read_buf[pos] & 0xFF0000L) >> 8)
  //     | ((read_buf[pos] & 0xFF00L) << 8)
  //     | ((read_buf[pos] & 0xFFL) << 24);
  // }

  return true;
}

// kick off a range-program operation
void program_range(uint32_t start_addr, uint32_t end_addr) {

  select_spi();

  // verify addresses
  if (start_addr != (start_addr & SECTOR_MASK)) {
    Serial.println("ERR Start addr must be sector aligned");
    reset();
    return;
  }
  if (end_addr != (end_addr & SECTOR_MASK)) {
    Serial.println("ERR End addr must be sector aligned");
    Serial.println(SECTOR_MASK, HEX);
    reset();
    return;
  }

  // Program a sector at a time
  for (; start_addr < end_addr; start_addr += SECTOR_SIZE) {

    // Read entire sector from remote host and skip it if it's already
    // programmed
    bool matches = true;
    for (uint32_t chunk_start = start_addr;
         chunk_start < start_addr + SECTOR_SIZE;
         chunk_start += CHUNK_SIZE) {
      // Get one chunk of data from the remote host
      if (!get_range(chunk_start, chunk_start + CHUNK_SIZE)) return;
      // Serial.print("first word in buf: ");
      // Serial.println(read_buf[0], HEX);
      // Compare it with the data in flash
      for (uint32_t pos = 0; pos < CHUNK_SIZE; ++pos) {
        if (flash_read(chunk_start + pos) != read_buf[pos]) {
          matches = false;
          Serial.print("mismatch at ");
          Serial.println(chunk_start + pos);
          break;
        }
      }
      if (!matches) break;
    }
    // If whole sector matches data from remote, skip programming
    if (matches) {
      Serial.println("whole sector matches");
      continue;
    }

    // Mismatch!  Program the sector.
    Serial.println("erasing sector");
    flash_write_both(0x555, 0xAA); // (1) Unlock 1
    flash_write_both(0x2AA, 0x55); // (2) Unlock 2
    flash_write_both(0x555, 0x80); // (3) Setup
    flash_write_both(0x555, 0xAA); // (4) Unlock
    flash_write_both(0x2AA, 0x55); // (5) Unlock
    flash_write_both(start_addr, 0x30); // (6) Sector address
    while (1) {
      uint32_t status = flash_read(start_addr);
      if (status == 0xFFFFFFFFL) {
        // Erase complete
        break;
      }
      if (check_disconnect()) return;

      // Check for error conditions on each chip
      for (uint32_t shift = 0; shift < 17; shift += 16) {
        uint32_t mask = 0xFFFFL << shift;

        // Not done - check DQ5
        if (!(status & 0x00200020L & mask)) {
          // DQ5 == 0; no timeout
          continue;
        }

        // DQ5 == 1; double check this isn't a glitch
        status = flash_read(start_addr);
        if (status & 0xFFFFFFFFL & mask) {
          // We're ok!
          continue;
        }

        // DQ5 indicated an error -- fail and reset
        Serial.println("ERR Flash erase failed - exceeded erase time limit");
        // Write reset command
        flash_write_both(0, 0xF0);
        // Just to be safe...
        flash_reset();
        return;
      }
    }

    Serial.println("programming sector");
#ifndef DEBUG_DONT_PROGRAM_FLASH
    for (uint32_t chunk_start = start_addr;
         chunk_start < start_addr + SECTOR_SIZE;
         chunk_start += CHUNK_SIZE) {

      // This is the algorithm descripted in Figure 8 (Write Buffer
      // Programming Operation) of the S29GL064S datasheet.

      // Get one chunk of data from the remote host
      if (!get_range(chunk_start, chunk_start + CHUNK_SIZE)) return;

      // Program it into the flash, 512 bytes (128 words) at a time
      for (uint32_t program_offset = 0;
          program_offset < CHUNK_SIZE;
          program_offset += PROGRAM_BLOCK_SIZE) {

        uint32_t program_start = chunk_start + program_offset;

        Serial.print("Program at ");
        Serial.println(program_start);
        // Serial.print("first word in buf: ");
        // Serial.println(read_buf[0], HEX);
        // Enter Write Buffer Programming mode
        flash_write_both(0x555, 0xAA); // (1) Unlock 1
        flash_write_both(0x2AA, 0x55); // (2) Unlock 2
        flash_write_both(program_start, 0x25); // (3) Write Buffer Load
        flash_write_both(program_start, PROGRAM_BLOCK_SIZE - 1); // (4) Sector address + Number of word locations to program minus one
        for (uint32_t pos = 0; pos < PROGRAM_BLOCK_SIZE; ++pos) {
          flash_write(program_start + pos, read_buf[program_offset + pos]);
        }
        flash_write_both(program_start, 0x29); // (n+5) Program Buffer to Flash

        // Serial.println("Wait for completion");
        // Poll last address written to buffer (program_start + PROGRAM_BLOCK_SIZE - 1), looking at DQ7/6/5/1
        uint32_t poll_comparison_value = read_buf[program_offset + PROGRAM_BLOCK_SIZE-1] & 0x00800080L;  // Compare with DQ7
        // Serial.print("Final word: ");
        // Serial.println(read_buf[PROGRAM_BLOCK_SIZE-1], HEX);
        uint32_t status_addr = program_start + PROGRAM_BLOCK_SIZE - 1;
        while (1) {
          uint32_t status = flash_read(status_addr);
          // Serial.print("Status & 80: ");
          // Serial.print(status & 0x00800080L, HEX);
          // Serial.print(" c.f. this: ");
          // Serial.println(poll_comparison_value, HEX);
          // Check for final state on both chips
          if ((status & 0x00800080L) == poll_comparison_value) {
            // We're done
            // Serial.println("got it");
            break;
          }
          if (check_disconnect()) return;

          // Check both chips independently for failure states
          for (uint32_t shift = 0; shift < 17; shift += 16) {
            uint32_t mask = 0xFFFFL << shift;

            uint32_t status = flash_read(status_addr);
            if ((status & 0x00800080L & mask) == (poll_comparison_value & mask)) {
              // This chip is done
              continue;
            }

            // Not done - check DQ5
            if (!(status & 0x00200020L & mask)) {
              // DQ5 == 0; check DQ1
              if (!(status & 0x00020002L & mask)) {
                // DQ1 == 0; continue
                continue;
              }
            }

            // Either DQ5 == 1 or DQ1 == 1; double check this isn't a glitch
            status = flash_read(status_addr);
            if ((status & 0x00800080L & mask) == (poll_comparison_value & mask)) {
              // This chip is done
              continue;
            }

            Serial.print("Failure state: read status==");
            Serial.println(status & mask, HEX);
            Serial.print(status & 0x00800080L & mask, HEX);

            Serial.print(" and poll comparison value is ");
            Serial.println(poll_comparison_value & mask, HEX);

            Serial.print("Actual value we're writing: ");
            Serial.println(read_buf[program_offset + PROGRAM_BLOCK_SIZE-1], HEX);

            // Either DQ5 or DQ1 indicated an error -- fail and reset
            if (status & 0x00200020L & mask) {
              // Device failed
              Serial.println("ERR Flash programming failed - exceeded program time limit");
              Serial.println(status, HEX);
              Serial.println(mask, HEX);
            } else if (status & 0x00020002L & mask) {
              // Operation aborted
              Serial.println("ERR Flash programming aborted");
              Serial.println(status, HEX);
              Serial.println(mask, HEX);
              // Write write-to-buffer-abort command
              flash_write_both(0x555, 0xAA);
              flash_write_both(0x2AA, 0x55);
              flash_write_both(0x555, 0xF0);
            }
            // Write reset command
            flash_write_both(0, 0xF0);
            // Just to be safe...
            flash_reset();
            return;
          }
        }
        // Block programmed
      }
      // If we got here, the chunk is programmed and we can continue
      Serial.println("Chunk programmed");
    }
    Serial.println("Sector programmed");
#endif // DEBUG_DONT_PROGRAM_FLASH
  }
}

void loop() {

  // DEBUG: output 0-255 on cpld_uart
  static uint8_t uart_debug_char = 0;
  static long last_char_written = 0;
  long now = millis();
  if ((now - last_char_written) > 1 && sercom2.isDataRegisterEmptyUART()) {
    sercom2.writeDataUART(uart_debug_char++);
    while (!sercom2.isDataRegisterEmptyUART());
    last_char_written = now;
  }

  if (sercom2.availableDataUART()) {
    uint8_t c = sercom2.readDataUART();
    if (Serial.dtr()) {
      Serial.print("received: ");
      Serial.println((char)c);
    }

    static int bitbang_serial_have_star = 0;
    if (c == '*') {
      bitbang_serial_have_star = 1;
    } else {
      if (c >= '0' && c <= '7' && bitbang_serial_have_star) {
        select_flash_bank(c - '0');
      }
      bitbang_serial_have_star = 0;
    }
  }

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
    Serial.println("OK");
    serial_active = 2;
  } else if (serial_active == 2) {
    // Serial port is actually open.
  }

  if (Serial.available()) {
    int c = Serial.read();
    switch (c) {
      case 'B': {
        // benchmark
        chip_end = chip_size();
        chip_end = 512 * 1024;
        Serial.print("Reading ");
        Serial.print(chip_end);
        Serial.println(" bytes from flash...");
        for (uint32_t addr = 0; addr < chip_end / 4; ++addr) {
          (void)flash_read(addr);
        }
        Serial.println("Done.");
        reset();
        break;
      }
      case 'C': {
        // program CPLD
        Serial.println("SEND SVF");
        arduino_play_svf(TMS_PIN, TDI_PIN, TDO_PIN, TCK_PIN, -1);
        Serial.println("SVF DONE");
        reset();
        break;
      }
      case 'I': {
        Serial.println("IDENTIFY FLASH");
        select_spi();

        flash_write_both(0x55, 0x0098L);  // Enter CFI mode

        Serial.print("Device size: 2^");
        Serial.print(flash_read(0x27) & 0xffff);
        Serial.println(" bytes");

        for (uint32_t cfi_addr = 0x10; cfi_addr <= 0x50; ++cfi_addr) {
          Serial.print("CFI 0x");
          Serial.print(cfi_addr, HEX);
          Serial.print(": ");
          Serial.println(flash_read(cfi_addr), HEX);
        }

        flash_write_both(0x00, 0xf0);  // Exit CFI mode
        flash_unlock();  // Allow host access again

        chip_end = chip_size();
        Serial.print("Size = ");
        Serial.println(chip_end);

        Serial.println("OK");
        reset();
        break;
      }
      case 'P': {
        while (!Serial.available()) {
          if (check_disconnect()) break;
        }
        if (Serial.read() != '\n') break;
        chip_end = chip_size();
        Serial.print("Program whole chip.  Size = ");
        Serial.println(chip_end);
        program_range(0, chip_end / 4);  // Program chip_end/4 words
        reset();
        break;
      }
      case 'R': {
        chip_end = chip_size();
        Serial.print("Read whole chip.  Size = ");
        Serial.println(chip_end);
        Serial.print("DATA:");
        // chip_end == number of bytes in a single chip, i.e. 2 * number of words
        for (uint32_t chunk_start = 0; chunk_start < chip_end / 4; chunk_start += CHUNK_SIZE / 4) {
          // Read 16kB from flash
          for (uint32_t offset = 0; offset < CHUNK_SIZE/4; ++offset) {
            read_buf[offset] = flash_read(chunk_start + offset);
          }
          // fail gracefully on disconnect
          uint32_t bytes_to_write = CHUNK_SIZE, bytes_written = 0;
          do {
            if (check_disconnect()) return;
            bytes_written += Serial.write(((char *)read_buf) + bytes_written, bytes_to_write);
          } while (bytes_written < bytes_to_write);
        }
        flash_unlock();
        reset();
        break;
      }
      case 'S': {
        Serial.println("S");
        select_uart();
        Serial.println("send *");
        sercom2.writeDataUART(42);
        while (!sercom2.isDataRegisterEmptyUART());
        Serial.println("done");
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
        reset();
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
