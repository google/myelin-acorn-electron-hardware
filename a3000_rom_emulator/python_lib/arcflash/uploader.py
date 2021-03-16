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

# Program a ROM image into an Arcflash board.

# TODO figure out a less CPU intensive way to do this.  We can probably use
# blocking serial comms (that would hang on the ATMEGA32U4) for Arcflash with
# its ATSAMD21.

import re
import sys
import time

from . import afserial

def read_until(ser, match):
    resp = b''
    while True:
        r = ser.read(1024)
        if r:
            print(repr(r))
            resp += r
            if resp.find(match) != -1:
                break
            else:
                time.sleep(0.1)
    return resp

def upload(rom):
    with afserial.Port() as ser:
        print("\n* Port open.  Giving it a kick, and waiting for OK.")
        ser.write(b"\n")
        r = read_until(ser, b"OK")

        print("\n* Requesting chip ID and locking chip")
        ser.write(b"I\n")  # identify chip
        r = read_until(ser, b"OK")
        m = re.search(br"Size = (\d+)", r)
        if not m:
            raise Exception("Chip identification failed")
        chip_size = int(m.group(1))
        print("\n* Chip size = %d bytes" % chip_size)
        usb_block_size = 63 if (chip_size < 1048576) else 1024  # atmega32u4 can't handle big usb chunks, but atsamd21 can

        if len(rom) != chip_size:
            raise Exception("%s is %d bytes long, which does not match the flash capacity of %d bytes" % (rom_fn, len(rom), chip_size))

        print("\n* Start programming process")
        ser.write(b"P\n")  # program chip

        input_buf = b''
        done = 0
        while not done:
            input_buf += read_until(ser, b"\n")
            while input_buf.find(b"\n") != -1:
                p = input_buf.find(b"\n") + 1
                line, input_buf = input_buf[:p], input_buf[p:]
                line = line.strip()
                print("parse",repr(line))
                if line == b"OK":
                    print("All done!")
                    done = 1
                    break
                m = re.search(br"^(\d+)\+(\d+)$", line)
                if not m: continue

                start, size = int(m.group(1)), int(m.group(2))
                print("* [%.1f%%] Sending data from %d-%d" % (start * 100.0 / len(rom), start, start+size))
                blk = rom[start:start+size]
                #print `blk[:64]`
                while len(blk):
                    n = ser.write(blk[:usb_block_size])
                    if n:
                        blk = blk[n:]
                        #print("wrote %d bytes" % n)
                    else:
                        time.sleep(0.01)
