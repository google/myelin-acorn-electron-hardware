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
import os
import random
import serial
from serial.serialutil import SerialTimeoutException
from StringIO import StringIO
import sys
import time
import zipfile

def guess_port():
    port = os.environ.get('UPURS_PORT')
    if port:
        return port
    for pattern in "/dev/ttyACM? /dev/ttyUSB? /dev/tty.usbserial* /dev/tty.usbmodem* /dev/tty.wchusbserial*".split():
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

print("Opening port")
USE_TIMEOUT=0
ser = serial.Serial(guess_port(), timeout=0, write_timeout=0.5 if USE_TIMEOUT else None)

decompress = False
fn = None
for arg in sys.argv[1:]:
    if arg == '-d':
        decompress = True
    else:
        fn = arg

if not decompress:
    data = open(fn).read()
else:
    data = None
    # try loading a .uef out of a .zip
    try:
        zf = zipfile.ZipFile(fn)
        for f in zf.namelist():
            if f.endswith(".uef"):
                print("found %s in zip" % f)
                data = zf.read(f)
                print("read %d bytes from %s inside %s" % (len(data), f, fn))
                break
    except zipfile.BadZipfile:
        print("not a zip file")
    if data is None:
        # not a zip or can't find a .uef in there
        data = open(fn).read()
        print("read %d bytes from %s" % (len(data), fn))

    # try un-gzipping it
    try:
        data = gzip.GzipFile(fileobj=StringIO(data)).read()
        print("after gunzipping: %d bytes" % len(data))
    except IOError:
        print("not gzipped")

print("Sending %s to port and verifying that it comes back" % fn)

n_out = n_in = 0
received = []
n_retries = 0
print("Writing %d (%x) bytes" % (len(data), len(data)))
for c in data:
    while True:
        v = ord(c)
        print("%02x %c" % (v, c if 32 < v < 127 else '.'))
        try:
            n = ser.write(c)
        except SerialTimeoutException:
            n = 0
        print(n)
        if not USE_TIMEOUT: break

        # try receiving
        r = ser.read(1000)
        if r:
            print("RECEIVED", repr(r))
            received.append(r)

        if n: break # next char
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
print("%d (%x) bytes (%d missing).  %d retries." % (n, n, len(data) - n, n_retries))
