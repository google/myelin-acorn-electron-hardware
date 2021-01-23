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
import serial.tools.list_ports

def guess_port():
    # Try to detect a connected Arduino-like device
    arcflash_port = circuitplay_port = None
    for port in serial.tools.list_ports.comports():
        print(port.device,
            port.product,
            port.hwid,
            port.vid,
            port.pid,
            port.manufacturer,
        )
        if not port.vid:
            # Virtual device -- this isn't it
            continue
        print("Found something that looks like a serial port at %s" % port.device)
        return port.device

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

