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

# Program a 128kB, 256kB, or 512kB ROM image into a master_updateable_megarom
# board.

import hashlib
import re
import megarom
import sys
import time

def read_until(ser, resp, match):
    if resp.find(match) != -1:
        return resp
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

def main():
    with megarom.Port() as ser:
        print("\n* Port open.  Giving it a kick, and waiting for OK.")
        ser.write("\n")
        r = read_until(ser, "", "OK")

        for try_number in range(5):
            print("\n* Requesting chip ID (try %d)" % (try_number + 1))
            ser.write("I\n")  # identify chip
            r = read_until(ser, "", "OK")
            print("CHIP ID TEXT %s" % repr(r))
            m = re.search("Size = (\d+)", r)
            if not m:
                raise Exception("Chip identification failed")
            chip_size = int(m.group(1))
            print("\n* Chip size = %d bytes" % chip_size)
            if chip_size: break

        assert chip_size, "failed to identify chip"

        print("\n* Start read")
        ser.write("R\n")

        input_buf = ''
        done = 0
        start_time = time.time()
        while not done:
            input_buf = read_until(ser, input_buf, "\n")
            while input_buf.find("\n") != -1:
                p = input_buf.find("\n") + 1
                line, input_buf = input_buf[:p], input_buf[p:]
                line = line.strip()
                print("parse",repr(line))
                if line.find("Size = ") != -1:
                    done = 1
                    break
        input_buf = read_until(ser, input_buf, "DATA:")
        input_buf = input_buf[input_buf.find("DATA:") + 5:]
        last_reported = 0
        try:
            while len(input_buf) < chip_size:
                r = ser.read(1024)
                if r:
                    # print(`r`, len(input_buf), chip_size)
                    input_buf += r
                    if len(input_buf) - last_reported > 65536:
                        print(len(input_buf), chip_size)
                        last_reported = len(input_buf)
        except KeyboardInterrupt:
            print("Interrupted -- saving what we have")
        time_taken = time.time() - start_time
        print("Saving")
        contents, input_buf = input_buf[:chip_size], input_buf[chip_size:]
        open("read.rom", "w").write(contents)
        print("%d bytes read in %.2f s - md5 %s - sha1 %s" % (
            len(contents),
            time_taken,
            hashlib.md5(contents).hexdigest(),
            hashlib.sha1(contents).hexdigest(),
        ))
        print("input:", repr(input_buf))
        read_until(ser, input_buf, "OK")
        print("Done!")

if __name__ == '__main__':
    main()
