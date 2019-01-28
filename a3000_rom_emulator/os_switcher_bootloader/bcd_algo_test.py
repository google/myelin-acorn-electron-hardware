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

GENCODE = 1

def to_bcd(i):
    b = 0
    if GENCODE:
        print("convert_int_to_bcd:")
        print("  @ input in r0, output in r0, clobbers r1, r2, r3")
        print("  mov r1, #0  @ bcd output")
        print("  mov r3, #0  @ 0-31 loop counter")
        print("bcd_conversion_loop:")
    for bit in range(32):
        for col in range(8):
            colshift = col * 4
            colmask = 0xF << colshift
            v = (b & colmask)
            if v >= (5 << colshift):
                b += (3 << colshift)
            if GENCODE and bit == 0:
                print("  and r2, r1, #0x%x  @ check if we need to add 3 to column %d" % (colmask, col))
                print("  cmp r2, #0x%x" % (5 << colshift))
                print("  addhs r1, r1, #0x%x" % (3 << colshift))
        if GENCODE and bit == 0:
            print("  @ shift new bit in")
            print("  lsl r1, #1  @ make room")
            print("  lsls r0, #1  @ shift bit out from the left into C flag")
            print("  adc r1, r1, #0  @ add shifted bit")
        b = (b << 1) | ((i & 0x80000000) >> 31)
        i = (i & 0x7FFFFFFF) << 1
        #print(hex(i), hex(b))
        if GENCODE and bit == 0:
            print("  @ continue around loop")
            print("  add r3, r3, #1")
            print("  cmp r3, #32")
            print("  blo bcd_conversion_loop")
    if GENCODE:
        print("bcd_conversion_done:")
        print("  mov r0, r1  @ output in r0")
        print("  mov pc, lr")
    return b

def to_int(b):
    i = 0
    for digit in range(8):
        d = (b & 0xF0000000) >> 28
        i = (i * 10) + d
        b = (b & 0x0FFFFFFF) << 4
    return i

for i in xrange(99990000, 99999999):
    b = to_bcd(i)
    ii = to_int(b)
    if i != ii:
        print("bcd(%d) == %d/%x, which decodes as %d :(" % (i, b, b, ii))
    GENCODE = 0
