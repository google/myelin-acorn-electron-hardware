from __future__ import print_function
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os
import pygame
import serial
import time

# Keyboard mappings

# The goal here is to have something that I can use in my C code for the PS/2 keyboard,
# although those codes are probably different.

KEY_NONE = 0xff
KEY_BREAK = 0x1ff

# Taken from the BBC Master Service Manual.  Col 0 is leftmost, Row 0 is topmost.
bbc_master_keycodes = [
    # col 0 (esc)
    # quirk: CAPS LOCK on macos sends KEYDOWN when enabled, KEYUP when disabled.
    # quirk: F10 used for SHIFT LOCK
    [27, 9, 292, 301, 49, 291, 113, (304, 303)],
    # col 1 (f1)
    [282, 122, 115, 97, 50, 119, 51, 306],
    # col 2 (f2)
    [283, 32, 99, 120, 100, 101, 52],
    # col 3 (f3)
    [284, 118, 103, 102, 114, 116, 53],
    # col 4 (f5)
    [286, 98, 104, 121, 54, 55, 285],
    # col 5 (f6)
    [287, 109, 110, 106, 117, 105, 56],
    # col 6 (f8)
    [289, 44, 108, 107, 111, 57, 288],
    # col 7 (f9)
    # quirk: no key for @; where does that go???
    [290, 46, 59, None, 112, 48, 45],
    # col 8 (|)
    [92, 47, 93, 39, 91, 61, 96],
    # col 9 (->)
    [275, 307, (309, 8), 13, 273, 274, 276],
    # col 10 (4')
    [], # skipping the numpad
    # col 11 (5')
    [], # skipping the numpad
    # col 12 (2')
    [], # skipping the numpad
]

scancodes_to_beebcodes = {293: KEY_BREAK}

for col in range(len(bbc_master_keycodes)):
    coldata = bbc_master_keycodes[col]
    for row in range(len(coldata)):
        scancodes = coldata[row]
        if scancodes is None: continue
        if not isinstance(scancodes, type(())): scancodes = (scancodes,)
        for scancode in scancodes:
            beebcode = (col << 4) | row
            if scancode in scancodes_to_beebcodes:
                print("WARNING: overriding scancode %s dest %s with %s" % (
                    scancode, scancodes_to_beebcodes[scancode], beebcode))
            scancodes_to_beebcodes[scancode] = beebcode

def guess_port():
    port = os.environ.get('KB_PORT')
    if port:
        return port
    for pattern in "/dev/ttyACM? /dev/ttyUSB? /dev/tty.usbserial* /dev/tty.usbmodem* /dev/tty.wchusbserial*".split():
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

class Main:
    def set_keys(self, key1, key2, shift_down, ctrl_down, break_down):
        msg = '*%c%c%c#' % (
            key1,
            key2,
            (0x80 if shift_down else 0) | (0x40 if ctrl_down else 0) | (0x20 if break_down else 0),
        )
        self.ser.write(msg)
        print(repr(self.ser.read(1)))

    def send_keys(self):
        s = c = b = 0
        others = []
        for beebcode in self.keys_down:
            if beebcode == 0x07:
                s = 1
            elif beebcode == 0x17:
                c = 1
            elif beebcode == KEY_BREAK:
                b = 1
            else:
                others.append(beebcode)
        # max 2 keys at once, with most recently pressed keys having priority.
        # this probably breaks games, but gives nice rollover when typing :)
        others, leftovers = others[-2:], others[:-2]
        while len(others) < 2: others.append(KEY_NONE)
        print(s, c, b, others, leftovers)
        self.set_keys(others[0], others[1], s, c, b)

    def main(self):
        self.keys_down = []

        print("Opening port")
        self.ser = serial.Serial(guess_port(), timeout=2)

        print("Forwarding key input through to the connected MCU")
        pygame.init()
        pygame.display.set_mode((100, 100))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    v = scancodes_to_beebcodes.get(event.key, None)
                    if v is not None:
                        print("beebcode %02x" % v)
                        if v not in self.keys_down:
                            self.keys_down.append(v)
                            self.send_keys()
                    print("KEYDOWN %s %s" % (
                        event.key,
                        '' if (event.key < 32 or event.key > 127) else '(%s)' % chr(event.key)))
                elif event.type == pygame.KEYUP:
                    print("KEYUP %s" % event.key)
                    v = scancodes_to_beebcodes.get(event.key, None)
                    if v is not None:
                        print("beebcode %02x" % v)
                        if v in self.keys_down:
                            while v in self.keys_down:
                                self.keys_down.remove(v)
                            self.send_keys()
            time.sleep(1.0/60)

if __name__ == '__main__':
    Main().main()
