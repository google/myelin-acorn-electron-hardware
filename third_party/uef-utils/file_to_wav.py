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

import os, stat, sys, tempfile

HERE = os.path.abspath(os.path.split(sys.argv[0])[0])
print(HERE)

def cmd(s):
	print(s)
	return os.system(s)

class UEF(object):
	def __init__(self, uef_fn, arch="Electron"):
		self.uef_fn = uef_fn
		cmd("rm -f %s" % self.uef_fn)
		cmd("python %s/UEFtrans.py %s new %s any" % (HERE, self.uef_fn, arch))

	def add_file(self, fn, load_addr):
		size = os.stat(fn)[stat.ST_SIZE]
		load = start = int(load_addr, 16)

		temp = tempfile.mkdtemp("_uef_append")
		try:
			cmd("cp -v %s %s/file" % (fn, temp))
			print("$.%s\t%X\t%X\t%X" % (
				leaf, load, start, size), file=open("%s/file.inf" % temp, "w"))
			cmd("python %s/UEFtrans.py %s append %s/file" % (HERE, self.uef_fn, temp))
		finally:
			os.unlink("%s/file" % temp)
			os.unlink("%s/file.inf" % temp)
			os.rmdir(temp)

	def make_wav(self, wav_fn):
		cmd("rm -f %s" % wav_fn)
		cmd("python %s/uef2wave.py %s %s" % (HERE, self.uef_fn, wav_fn))
		return wav_fn
		
def make_wav(leaf, load_addr):
	uef = UEF("%s.uef" % leaf)
	uef.add_file(leaf, load_addr)
	return uef.make_wav("%s.wav" % leaf)

if __name__ == '__main__':
	leaf, load_addr = sys.argv[1:]
	wav_fn = make_wav(leaf, load_addr)
	cmd("open '%s'" % wav_fn)
	print("On the Electron, run: *LOAD %s %x" % (leaf, int(load_addr, 16)))
