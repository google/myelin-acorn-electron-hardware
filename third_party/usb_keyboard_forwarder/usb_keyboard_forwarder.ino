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

#include <hidboot.h>

#include "PPKeyboard.h"

USBHost usb;
PPKeyboard keyboard(usb);

// See
// https://github.com/mattairtech/ArduinoCore-samd/tree/master/variants/MT_D21E_revB
// for pin mapping details.

// Serial1 uses PA10 = TX and PA11 = RX.  These are six rows from the top on my
// board; with PA11 (RX) on the left (outside of the board) and PA10 (TX) on the
// right.  On the Adafruit serial cable, green is TX and white is RX.

void debug(bool down) {
  Serial1.print("OEM 0x");
  Serial1.print(keyboard.getOemKey(), HEX);

  int mod = keyboard.getModifiers();
  Serial1.print("; mod: 0x");
  Serial1.print(mod, HEX);

  Serial1.print("; key: 0x");
  Serial1.print(keyboard.getKey(), HEX);

  Serial1.print(" ");
  Serial1.println(down ? "DOWN" : "UP");
}

// Key-down callback from PPKeyboard.cpp
void PPkeyPressed() {
  debug(true);
}

// Key-up callback from PPKeyboard.cpp
void PPkeyReleased() {
  debug(false);
}

void setup()
{
  Serial1.begin(115200);
  Serial1.println("USB Keyboard Forwarder");

  usb.Init();
  delay(20);
}

static long last_update = 0;
void loop()
{
  // Set the keyboard LEDs to a random state every 500 ms
  long now = millis();
  if (now - last_update > 500) {
    last_update = now;
    bool num = rand() & 1, caps = rand() & 1, scroll = rand() & 1;
    keyboard.setLeds(num, caps, scroll);
  }

  // Poll USB
  usb.Task();
}
