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

# Read all the ROM images out of a Retro Hardware Mega Games Cartridge

import re
import standalone_programmer
import time

BANK_SEL = '\xfc\x00'

def main():
	with standalone_programmer.Port() as ser:

		cart_read_start = time.time()
		print("setting flags: RPM=0 RBS=0 RWE=0")
		ser.write("w" + BANK_SEL + "\x00")

		for bank in range(128):
			print("READ BANK %d" % bank)
			bank_read_start = time.time()
			write_cmd = "w" + BANK_SEL + chr(bank)
			print(repr(write_cmd))
			ser.write(write_cmd)
			ser.write("S")  # fast read
			resp = ''
			while True:
				r = ser.read(1024)
				if r:
					#print `r`
					resp += r
					if resp.rstrip().endswith("ROM DONE"):
						break
				else:
					time.sleep(0.1)
			print("Bank read in %.2f s" % (time.time() - bank_read_start))

			rom_data = re.search("ROM\[(.{32768})\]", resp, re.DOTALL).group(1)
			print(len(rom_data))
			open("mgc_rom_%d.bin" % (bank * 2), "w").write(rom_data[:16384])
			open("mgc_rom_%d.bin" % (bank * 2 + 1), "w").write(rom_data[16384:])

		print("Whole cartridge read in %.2f s" % (time.time() - cart_read_start))

if __name__ == '__main__':
	main()
