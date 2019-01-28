from __future__ import print_function

# Copyright 2019 Google LLC
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

copyright = ''
copyright_finished = False
patterns = {}

for line in open("Interfonts.s"):
    line = line.rstrip()
    if not copyright_finished:
        if line.startswith(';'):
            copyright += ('@ %s' % (line[1:])).strip() + '\n'
        else:
            copyright_finished = True

    if not re.search('^U_00(..) ', line):
        continue

    print(line)
    m = re.search(r'^U_00([A-F0-9]+) = ([A-F0-9&,]+)\s*;(.*)$', line)
    if m:
        charno, pattern, comment = m.groups()
        charno = int(charno, 16)
        pattern = pattern.replace("&", "0x")
        patterns[charno] = (pattern, comment)
        continue

    m = re.search(r'^U_00([A-F0-9]+) \* U_00([A-F0-9]+)\s*;(.*)$', line)
    if m:
        charno, copychar, comment = m.groups()
        charno = int(charno, 16)
        copychar = int(copychar, 16)
        patterns[charno] = (patterns[copychar][0], comment)
        print('copy %d (%x) for %d (%x, %s)' % (copychar, copychar, charno, charno, comment))
        continue

    raise Exception("can't match %s" % line)

f = open('riscos_font.s', 'w')
print(copyright, file=f)
print('  .global riscos_font', file=f)
print('  .align\nriscos_font:', file=f)
for charno in range(0, 256):
    if charno in patterns:
        pattern, comment = patterns[charno]
    else:
        # Just fill in the charset with a 'missing char' mark
        # when we don't have a pattern for a char; this way I
        # don't need to validate bytes at all:
        #
        #  XXXXXXX.
        #  X.....X.
        #  X.X.X.X.
        #  X..X..X.
        #  X.X.X.X.
        #  X.....X.
        #  XXXXXXX.
        #  ........
        pattern = "0xFE,0x82,0xAA,0x92,0xAA,0x82,0xFE,0x00"
        comment = ""
    print(("  .byte %s  @ %d (%x) %s" % (pattern, charno, charno, comment)).rstrip(), file=f)
print('  .align', file=f)

print('riscos_font.s written')
