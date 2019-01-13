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
import serial

def guess_port():
    port = None
    for pattern in "/dev/ttyACM? /dev/ttyUSB? /dev/tty.usbserial* /dev/tty.usbmodem* /dev/tty.wchusbserial*".split():
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

class Port:
    def __init__(self):
        port = guess_port()
        if not port:
            raise Exception("Could not guess serial port")

        print("Opening port %s" % port)
        self.ser = serial.Serial(port, timeout=0)
        print("Serial port opened: %s" % repr(self.ser))

    def __enter__(self):
        return self.ser

    def __exit__(self, type, value, traceback):
        self.ser.close()

