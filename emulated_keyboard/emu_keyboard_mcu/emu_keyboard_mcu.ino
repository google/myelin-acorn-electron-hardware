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
// #include <PS2Keyboard.h>

// PS/2 keyboard to CPLD (SPI) interface for BBC Master keyboard emulation

// This program reads scan codes from an attached PS/2 keyboard, handles key
// rollover, and passes codes to a CPLD over SPI, to tell it what information
// to pass to the BBC Master keyboard encoder it's plugged into.

//TODO update these
// #define DataPin 8
// #define IRQpin 5

#define SPI_SS_PIN 10

#define KEY_NONE 0xFF

// PS2Keyboard keyboard;

// The CPLD can emulate max 2 keys at a time.
// key1 and key2: BBC Master keyboard scan codes
//   (column << 4) | row.
//   0xff = unused.
// shift_down, ctrl_down, and break_down: true if SHIFT, CTRL, or BREAK are down
void set_keys(uint8_t key1, uint8_t key2, bool shift_down, bool ctrl_down, bool break_down) {
  digitalWrite(SPI_SS_PIN, LOW);
  SPI.transfer(key1);
  SPI.transfer(key2);
  SPI.transfer((shift_down ? 0x80 : 0) | (ctrl_down ? 0x40 : 0) | (break_down ? 0x20 : 0));
  digitalWrite(SPI_SS_PIN, HIGH);
}

void setup() {
  // Init CPLD comms and reset keyboard emulator
  pinMode(SPI_SS_PIN, OUTPUT);
  digitalWrite(SPI_SS_PIN, HIGH);
  SPI.begin();
  set_keys(KEY_NONE, KEY_NONE, false, false, false);

  // Init PS/2 keyboard comms
  // delay(1000);
  // keyboard.begin(DataPin, IRQpin);

  // Init serial comms
  Serial.begin(9600);
  Serial.println("BBC Master keyboard emulator");
}

#define BUF_SIZE 10
uint8_t buf[BUF_SIZE];
int buf_end = 0;

void loop() {

  while (Serial.available()) {
    if (buf_end == BUF_SIZE) {
      // overflow!  throw it all away.
      // (this should never happen bc of the logic below, but just in case...)
      buf_end = 0;
      break;
    }

    uint8_t c = Serial.read();
    if (buf_end == 0 && c != '*') {
      // waiting for '*' to start a packet
      break;
    }
    buf[buf_end++] = c;
    if (buf_end > 4) {
      if (c != '#') {
        // bad end of packet
        buf_end = 0;
        break;
      }
      Serial.print(".");
      set_keys(buf[1], buf[2], buf[3] & 0x80 ? true : false, buf[3] & 0x40 ? true : false, buf[3] & 0x20 ? true : false);
      buf_end = 0;
    }

    break;  // this is just a while so i can break out of it!
  }

  // hit BREAK every 1.5 seconds
  // delay(1000);
  // set_keys(KEY_NONE, KEY_NONE, false, false, true);
  // delay(500);
  // set_keys(KEY_NONE, KEY_NONE, false, false, false);
  
  // Normal PS2Keyboard usage is to call keyboard.available(), followed by
  // keyboard.read() to read a character.  However, keyboard.available()
  // processes scan codes and fills the character buffer, which we don't want,
  // so we call keyboard.readScanCode() instead, to get the raw scan codes.

  // uint8_t code = keyboard.readScanCode();
  // if (code != 0) {
  //   Serial.println(code, DEC);
  // }

}
