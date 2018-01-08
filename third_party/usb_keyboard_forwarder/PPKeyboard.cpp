/*
 Copyright (c) 2012 Arduino.  All right reserved.
 Copyright 2018 Google LLC

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include "PPKeyboard.h"

extern "C" {
void __PPKeyboardEmptyCallback() { }
}

void PPkeyPressed()  __attribute__ ((weak, alias("__PPKeyboardEmptyCallback")));
void PPkeyReleased() __attribute__ ((weak, alias("__PPKeyboardEmptyCallback")));

uint8_t PPKeyboard::HandleLockingKeys(HID* hid, uint8_t key) {

  // This is called from hidboot.cpp on every keyDown event, to handle keys that
  // change state, i.e. Num/Caps/ScrollLock.  We'd rather handle these through
  // the usual keyDown/keyUp process, so we do nothing here.

  return 0;
}

void PPKeyboard::OnControlKeysChanged(uint8_t before, uint8_t after) {
  Serial1.print("Control keys changed from ");
  Serial1.print(before, HEX);
  Serial1.print(" to ");
  Serial1.println(after, HEX);
}

void PPKeyboard::OnKeyDown(uint8_t _mod, uint8_t _oemKey) {
  modifiers = _mod;
  keyOem = _oemKey;
  key = OemToAscii(_mod, _oemKey);
  PPkeyPressed();
}

void PPKeyboard::OnKeyUp(uint8_t _mod, uint8_t _oemKey) {
  modifiers = _mod;
  keyOem = _oemKey;
  key = OemToAscii(_mod, _oemKey);
  PPkeyReleased();
}
