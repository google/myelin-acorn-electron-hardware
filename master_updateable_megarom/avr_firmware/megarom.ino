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


// Arduino sketch to interface an ATMEGA32U4 board (Leonardo, Pro Micro) with
// the Updateable Master MegaROM board -- http://myelin.nz/acorn/megarom

// This provides the following functions to a connected host machine, over a USB
// CDC serial port:

// Identify flash chip
// -------------------

// The flash chip on board can be a 128kB, 256kB, or 512kB part.

// Send "I\n" to the board.  It will respond with "size\nOK\n", with the chip
// size in "%d" format, followed by a carriage return.  If size detection fails,
// it will return "0\nOK\n".

// Read entire flash chip
// ----------------------

// Send "R\n" to the board.  It will respond with the size of the flash chip (as
// text), or 0 if detection failed, followed by a carriage return, followed by
// the entire contents of the chip, followed by "OK\n"

// Program entire flash chip
// -------------------------

// Send "P\n" to the board.  It will respond with a series of queries for data,
// in the format "start+length\n", e.g. "0+512\n".  It may ask for the same
// range multiple times, depending on the programming algorithm.  When
// programming is finished, it will send "OK\n".

// Program range
// -------------

// Send "p<start>+<range>\n" (e.g. "p0+131072\n") to the board.  It will respond
// as for the whole-chip programming process, requesting ranges and finishing
// with "OK\n".

#include "megarom.h"

// atmega32u4 only has 2.5kB SRAM, so we reuse the same buffer for everything
#define CHUNK_SIZE 512
#define BUF_SIZE (CHUNK_SIZE + 1)
static uint8_t read_buf[BUF_SIZE];
// count of chars read into read_buf
static int buf_pos = 0;
// true if we've seen dtr=1, false if we're disconnected or reset
static bool connected = false;
// state machine state
enum { //TODO rip this out unless it turns out to actually be necessary
  READING_COMMAND = 0,
  LAST_STATE
} state;
// flash chip size
uint32_t chip_end = 0L;
// for range programming state
uint32_t range_start = 0L, range_end = 0L; // range left to program
int range_chunk_size = 0; // how many bytes to expect in the buffer

void reset() {
  // reset SPI
  digitalWrite(SPI_SS_PIN, HIGH);
  SPI.transfer(0);  // synchronous reset
  // reset state machine
  state = READING_COMMAND;
  // reset read buffer
  buf_pos = 0;
  // reset connection flag
  connected = false;
  // clear out any unread input
  while (Serial.available() && !Serial.dtr()) {
    Serial.read();
  }
}

void setup() {
  pinMode(SPI_SS_PIN, OUTPUT);
  digitalWrite(SPI_SS_PIN, HIGH);
  SPI.begin();
  SPI.beginTransaction(SPISettings(1000000L, MSBFIRST, SPI_MODE0));

  Serial.begin(115200);

  reset();

  // give access to BBC
  read_byte_and_unlock(0L);
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

// request bytes from remote
bool get_range(uint32_t range_start, uint32_t range_end) {
  if (check_disconnect()) return false;

  Serial.print(range_start, DEC);
  Serial.print("+");
  Serial.println(range_end - range_start, DEC);

  long start_time = millis();
  buf_pos = 0;
  while (buf_pos < (int)(range_end - range_start)) {
    if (check_disconnect()) return false;
    if (millis() - start_time > 1000) {
      Serial.print("Timeout reading data after ");
      Serial.print(buf_pos);
      Serial.println(" bytes");
      return false;
    }
    if (!Serial.available()) continue;

    uint8_t c = Serial.read();
    read_buf[buf_pos++] = c;
  }

  return true;
}

// kick off a range-program operation
void program_range(uint32_t start_addr, uint32_t end_addr) {
  // verify addresses
  if (start_addr != (start_addr & SECTOR_MASK)) {
    Serial.println("ERR Start addr must be sector aligned");
    reset();
    return;
  }
  if (end_addr != (end_addr & SECTOR_MASK)) {
    Serial.println("ERR End addr must be sector aligned");
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
      // Compare it with the data in flash
      for (uint32_t pos = 0; pos < CHUNK_SIZE; ++pos) {
        if (read_byte_and_unlock(chunk_start + pos) != read_buf[pos]) {
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
    Serial.println("programming sector");
    erase_sector(start_addr);
    for (uint32_t chunk_start = start_addr;
         chunk_start < start_addr + SECTOR_SIZE;
         chunk_start += CHUNK_SIZE) {
      // Get one chunk of data from the remote host
      if (!get_range(chunk_start, chunk_start + CHUNK_SIZE)) return;
      // Program it into the flash
      Serial.print("Program at ");
      Serial.println(chunk_start);
      for (uint32_t pos = 0; pos < CHUNK_SIZE; ++pos) {
        program_byte(chunk_start + pos, read_buf[pos]);
        if (read_byte(chunk_start + pos) != read_buf[pos]) {
          Serial.print("Failed to program at ");
          Serial.println(chunk_start + pos);
          return;
        }
      }
    }
  }
}

void loop() {
  if (check_disconnect()) {
    return;
  }

  if (!connected) {
    // just connected
    connected = true;
    Serial.println("OK");
  }

  // we have a serial connection -- process input
  if (Serial.available()) {
    uint8_t c = Serial.read();
    read_buf[buf_pos++] = c;
    if (buf_pos >= BUF_SIZE) {
      Serial.println("ERR Buffer overflow");
      reset();
      return;
    }
    read_buf[buf_pos] = 0;

    switch (state) {
      case READING_COMMAND: {
        if (c != '\n') break;

        if (!strcmp((char *)read_buf, "U\n")) {
          read_byte_and_unlock(0);
          Serial.println("Unlocked.");
          reset();
          break;
        }

        if (!strcmp((char *)read_buf, "I\n")) {
          uint8_t device_id = identify_chip();
          Serial.print("Chip ID ");
          Serial.println(device_id, HEX);
          chip_end = chip_size();
          Serial.print("Size = ");
          Serial.println(chip_end);
          read_byte_and_unlock(0);
          reset();
          break;
        }

        if (!strcmp((char *)read_buf, "P\n")) {
          chip_end = chip_size();
          Serial.print("Program whole chip.  Size = ");
          Serial.println(chip_end);
          program_range(0, chip_end);
          read_byte_and_unlock(0);
          reset();
          break;
        }

        if (!strcmp((char *)read_buf, "R\n")) {
          chip_end = chip_size();
          Serial.print("Read whole chip.  Size = ");
          Serial.println(chip_end);
          Serial.print("DATA:");
          for (uint32_t addr = 0; addr < chip_end; ++addr) {
            // fail gracefully on disconnect
            do {
              if (check_disconnect()) return;
            } while (!Serial.availableForWrite());
            // read a byte from flash and send it to the remote host
            Serial.write(read_byte_and_unlock(addr));
          }
          read_byte_and_unlock(0);
          reset();
          break;
        }

        if (read_buf[0] == 'p') {
          Serial.println("program range");
          uint32_t start_addr = 0, range = 0;
          int i;
          for (i = 1; read_buf[i] >= '0' && read_buf[i] <= '9'; ++i) {
            start_addr = (start_addr * 10) + (read_buf[i] - '0');
          }
          if (read_buf[i] != '+') {
            Serial.println("ERR Expected +");
            reset();
            break;
          }
          for (++i; read_buf[i] >= '0' && read_buf[i] <= '9'; ++i) {
            range = (range * 10) + (read_buf[i] - '0');
          }
          if (read_buf[i] != '\n') {
            Serial.println("ERR Expected \\n");
            reset();
            break;
          }
          Serial.print("from ");
          Serial.print(start_addr, HEX);
          Serial.print(" to ");
          Serial.println(start_addr + range, HEX);
          program_range(start_addr, start_addr + range);
          read_byte_and_unlock(0);
          reset();
          break;
        }

        Serial.println("ERR Unknown command");
        read_byte_and_unlock(0);
        reset();
        break;
      } // READING_COMMAND

      default: {
        Serial.println("ERR Invalid state");
        reset();
        break;
      }

    } // switch (state)

  } // if (Serial.available())

} // loop()
