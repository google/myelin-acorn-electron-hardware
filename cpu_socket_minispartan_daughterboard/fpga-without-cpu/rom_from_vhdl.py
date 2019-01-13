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

import re
import sys
import time


def rom_from_vhdl(data):

    # extract binary data from a bunch of VHDL lines
    bytes = ['\xff' for _ in range(16384)]
    for line in data.split("\n"):
        m = re.search('when x"(....)" => Di <= x"(..)"', line)
        if not m: continue
        addr, value = m.groups()
        bytes[int(addr, 16)] = chr(int(value, 16))
        
    return ''.join(bytes)

if __name__ == '__main__':
    infile, outfile = sys.argv[1:]
    print("extracting bytes from %s and saving to %s" % (infile, outfile))
    bytes = rom_from_vhdl(open(infile).read())
    print("writing %d bytes" % len(bytes))
    open(outfile, 'w').write(bytes)
