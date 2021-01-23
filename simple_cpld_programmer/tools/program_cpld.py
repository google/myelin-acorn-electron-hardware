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

# Program a .svf file into the CPLD on the standalone_cartridge_programmer
# board

import simple_cpld_programmer
import sys
import time


assert sys.version_info[0] >= 3, "Python 3+ required"


def main():
    svf_fn, = sys.argv[1:]
    svf = open(svf_fn, "rb").read() + b"\n\x04"

    with simple_cpld_programmer.Port() as ser:
        # print("Serial port opened:", ser)

        while True:
            r = ser.read(1024)
            if not r: break
            print(repr(r))
            time.sleep(0.1)

        ser.write(b"C\n")

        resp = b''
        print("Waiting for SEND SVF")
        while True:
            r = ser.read(1024)
            if r:
                resp += r
                print(repr(r))
                if resp.find(b"SEND SVF") != -1:
                    print("got SEND SVF - continuing")
                    break
            time.sleep(0.1)

        svf_start_time = time.time()
        resp = b''
        SLEEP_TIME = 0.01
        sleep_count = 0
        svf_pos = 0
        all_done = False
        line_no = 1
        stars = 0  # count of how many times we've seen *#, which means send another packet
        while not all_done:
            if stars < -3:
                time.sleep(0.001)
            else:
                print("\r  (write @ line %d, %d/%d)" % (line_no, svf_pos, len(svf)), end=' ')
                sys.stdout.flush()

                # always send 63 chars if we can
                p = min(len(svf), svf_pos + 63)

                n = ser.write(svf[svf_pos:p])
                if n:
                    stars -= 1
                    # print("  (%d bytes written)" % n)
                    # print("  (sent: %s)" % repr(svf[svf_pos:p]))
                    line_no += svf[svf_pos:p].count(b"\n")
                    svf_pos += n

            while True:
                r = ser.read(1024)
                if not r:
                    break
                #print(r)
                resp += r
                while True:
                    p = resp.find(b"\n")
                    if p == -1: break
                    line = resp[:p].strip()
                    if line == b"*#":
                        stars += 1
                    else:
                        print("\r%s" % line)
                    resp = resp[p+1:]
                    if line.find(b"SVF DONE") != -1:
                        all_done = True
                        print("all done")
            if not n:
                time.sleep(SLEEP_TIME)
                sleep_count += 1
        svf_delivery_time = time.time() - svf_start_time

        print("SVF entirely sent, in %.2f s" % svf_delivery_time)
        total_sleep_time = SLEEP_TIME * sleep_count
        if total_sleep_time > 0.3:
            print("Slept for %.2f s total" % total_sleep_time)

if __name__ == '__main__':
    main()
