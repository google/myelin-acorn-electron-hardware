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

# Program a 32kB ROM image into a cartridge attached to a standalone programmer board

import re
import standalone_programmer
import sys
import time

def read_until(ser, match):
	resp = ''
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
	rom_fn, = sys.argv[1:]
	rom = open(rom_fn).read()
	assert len(rom) == 32768
	with standalone_programmer.Port() as ser:
		ser.write("I")  # identify chip
		resp = read_until(ser, "ID DONE")
		print("DONE")
		print()
		print(resp.strip())

		pos = 0
		if resp.find("SST39SF010") != -1:
			print("it's a SST39SF010; we can program that")
			ser.write("W")  # write 32k
			print(read_until(ser, "Programming"))
			while pos < len(rom):
				n = ser.write(rom[pos:pos+63])
				if n:
					pos += n
					print("wrote %d bytes" % n)
				else:
					time.sleep(0.01)

				r = ser.read(1024)
				if r:
					print(repr(r))
			print(read_until(ser, "WRITE DONE"))


if __name__ == '__main__':
	main()
