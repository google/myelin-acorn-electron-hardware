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

# Create (and open) a .wav file to transfer data to an Acorn Electron

# You'll need a 3.5mm-to-DIN cable to connect your computer to the electron's
# cassette input.

import os, stat, sys

HERE = os.path.abspath(os.path.split(sys.argv[0])[0])
print(HERE)

def cmd(s):
	print(s)
	return os.system(s)

fn, leaf, load_addr = sys.argv[1:]

cmd("cp -v %s out/file" % fn)
size = os.stat("out/file")[stat.ST_SIZE]
load = start = int(load_addr, 16)
print("$.%s\t%X\t%X\t%X" % (
    leaf, load, start, size), file=open("out/file.inf", "w"))
cmd("rm -f out/file.uef")
cmd("python UEFtrans.py out/file.uef new Electron any")
cmd("python UEFtrans.py out/file.uef append out/file")
cmd("python UEFtrans.py out/file.uef append out/file")
cmd("rm -f out/file.wav")
cmd("python uef2wave.py out/file.uef out/file.wav")
cmd("open out/file.wav")

print("On the Electron, run: *LOAD %s %x" % (leaf, load))
