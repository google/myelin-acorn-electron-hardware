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
import serial
import sys
import time

def guess_port():
    port = None
    for pattern in "/dev/ttyACM? /dev/ttyUSB? /dev/tty.usbserial* /dev/tty.usbmodem* /dev/tty.wchusbserial*".split():
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

def main():
    svf_fn, = sys.argv[1:]
    svf = open(svf_fn).read() + "\n\x04"

    port = guess_port()
    if not port:
        raise Exception("Could not guess serial port")

    with serial.Serial(port, timeout=0) as ser:
        print "Serial port opened:", ser

        while 1:
            r = ser.read(1024)
            if not r: break
            print `r`
            time.sleep(0.1)

        ser.write("C\n")

        resp = ''
        print "Waiting for SEND SVF"
        while 1:
            r = ser.read(1024)
            if r:
                resp += r
                print `r`
                if resp.find("SEND SVF") != -1:
                    print "got SEND SVF - continuing"
                    break
            time.sleep(0.1)

        resp = ''
        SLEEP_TIME = 0.01
        sleep_count = 0
        svf_pos = 0
        while 1: #len(svf):
            print "  (write @ %d/%d)" % (svf_pos, len(svf))
            n = ser.write(svf[svf_pos:svf_pos+100])
            if n:
                svf_pos += n
                print "  (%d bytes written)" % n
                print "  (sent: %s)" % `svf[svf_pos:svf_pos+100]`
            r = ser.read(1024)
            if r:
                print "READ:\n%s\n" % r
                resp += r
                if resp.find("SVF DONE") != -1:
                    break
            if not n:
                time.sleep(SLEEP_TIME)
                sleep_count += 1
        print "slept for %.2f s total" % (SLEEP_TIME * sleep_count)

if __name__ == '__main__':
    main()
