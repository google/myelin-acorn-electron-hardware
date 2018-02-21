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
    while 1:
        r = ser.read(1024)
        if r:
            print `r`
            resp += r
            if resp.find(match) != -1:
                break
            else:
                time.sleep(0.1)
    return resp

def main():
    with megarom.Port() as ser:
        print "\n* Port open.  Giving it a kick, and waiting for OK."
        ser.write("\n")
        r = read_until(ser, "", "OK")

        print "\n* Requesting chip ID"
        ser.write("I\n")  # identify chip
        r = read_until(ser, "", "OK")
        m = re.search("Size = (\d+)", r)
        if not m:
            raise Exception("Chip identification failed")
        chip_size = int(m.group(1))
        print "\n* Chip size = %d bytes" % chip_size

        print "\n* Start read"
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
                print "parse",`line`
                if line.find("Size = ") != -1:
                    done = 1
                    break
        input_buf = read_until(ser, input_buf, "DATA:")
        input_buf = input_buf[input_buf.find("DATA:") + 5:]
        while len(input_buf) < chip_size:
            r = ser.read(1024)
            if r:
                print `r`
                input_buf += r
        time_taken = time.time() - start_time
        print "Saving"
        contents, input_buf = input_buf[:chip_size], input_buf[chip_size:]
        open("read.rom", "w").write(contents)
        print "%d bytes read in %.2f s - md5 %s - sha1 %s" % (
            len(contents),
            time_taken,
            hashlib.md5(contents).hexdigest(),
            hashlib.sha1(contents).hexdigest(),
        )
        print "input:", `input_buf`
        read_until(ser, input_buf, "OK")
        print "Done!"

if __name__ == '__main__':
    main()
