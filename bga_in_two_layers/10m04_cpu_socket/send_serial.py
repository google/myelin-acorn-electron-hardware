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
import gzip
import random
import serial
from serial.serialutil import SerialTimeoutException
from StringIO import StringIO
import sys
import time
import zipfile

def guess_port():
    port = None
    for pattern in "/dev/ttyACM? /dev/ttyUSB? /dev/tty.usbserial* /dev/tty.usbmodem* /dev/tty.wchusbserial*".split():
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

print("Opening port")
USE_TIMEOUT = 0
ser = serial.Serial(guess_port(), timeout=0, write_timeout=0.5 if USE_TIMEOUT else None)
print("Set baudrate")
ser.baudrate = 115200

fn = None
for arg in sys.argv[1:]:
    fn = arg

data = open(fn).read()

print("Sending %s to port and dumping whatever comes back" % fn)

n_out = n_in = 0
received = []
n_retries = 0
print("Writing %d (%x) bytes" % (len(data), len(data)))
addr = 0
for c in data:
    while True:
        v = ord(c)
        print("%04x: %02x %c" % (addr, v, c if 32 < v < 127 else '.'))
        addr += 1
        try:
            n = ser.write(c)
        except SerialTimeoutException:
            n = 0
        print(n)
        #time.sleep(0.01)
        #print `ser.read(3)`
        if not USE_TIMEOUT: break

        # try receiving
        r = ser.read(1000)
        if r:
            print("RECEIVED", repr(r))
            received.append(r)

        if n:
            break # next char
        time.sleep(0.01)
        print("RETRY", end=' ')
        n_retries += 1

print("Waiting for final serial loopback")
start = time.time()
while (time.time() - start) < 0.5:
    r = ser.read()
    if not r:
        time.sleep(0.1)
        continue
    # we got something, so reset the timeout
    start = time.time()
    print(repr(r))
    received.append(r)

print("ALL SENT")
received = ''.join(received)
print("This is what we received:")
print(repr(received))
n = len(received)
print("%d (0x%x) bytes (%d missing).  %d retries." % (n, n, len(data) - n, n_retries))
