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

import standalone_programmer
import time

def main():
	data_to_write = "*" * 131072
	with standalone_programmer.Port() as ser:
		ser.write("Z")  # USB test mode
		written = read = 0
		to_write = len(data_to_write)
		while written < to_write:
			n = ser.write(data_to_write[written:written+63])
			if n:
				print("written %d: %d/%d (read %d)" % (n, written, to_write, read))
				written += n
			else:
				time.sleep(0.01)
			r = ser.read(1024)
			if r:
				read += len(r)
				print("READ %d: %d total" % (len(r), read))
				print(repr(r))

if __name__ == '__main__':
	main()
