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

# Read two 16kB ROM images out of a cartridge attached to a standalone programmer board

import re
import standalone_programmer
import time

def main():
	with standalone_programmer.Port() as ser:
		ser.write("S")  # fast read
		resp = ''
		while True:
			r = ser.read(1024)
			if r:
				print(repr(r))
				resp += r
				if resp.rstrip().endswith("ROM DONE"):
					break
			else:
				time.sleep(0.1)
		print("DONE")


	rom_data = re.search("ROM\[(.{32768})\]", resp, re.DOTALL).group(1)
	print(len(rom_data))
	open("rom1.bin", "w").write(rom_data[:16384])
	open("rom2.bin", "w").write(rom_data[16384:])

if __name__ == '__main__':
	main()
