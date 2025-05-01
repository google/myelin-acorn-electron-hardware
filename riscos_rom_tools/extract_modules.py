# Copyright 2020 Google LLC
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

"""Extract kernel and modules from a RISC OS ROM image.

Written originally to investigate the contents of the Bush IBX250 OS ROM.

"""

import os
import struct
import sys


def translate_filename(risc_fn):
    # swap . and /
    # replace invalid chars with spaces
    fn = ""
    for c in risc_fn:
        if c == ord("."):
            r = "/"
        elif c == ord("/"):
            r = "."
        elif 32 <= c <= 127:
            r = chr(c)
        else:
            r = "?"
        fn += r
    return fn


(os_fn,) = sys.argv[1:]

rom = open(os_fn, "rb").read()
print("Read %d-byte ROM from %s" % (len(rom), os_fn))

os.makedirs("modules", exist_ok=True)

module_list = open("module_list.txt", "wt")

def rom_word(ptr):
    return struct.unpack("<L", rom[ptr : ptr + 4])[0]


def rom_string(t):
    return rom[t : rom.find(0, t)]


search_module = b"UtilityModule"
m = f = rom.find(search_module)
assert f != -1, "Can't find %s" % search_module.decode()
f = f & (~3)
# now M% = offset of UtilityModule, F% is word aligned version of M%
print("Found %s text at %d (aligned: %d)" % (search_module.decode(), m, f))

# find pointer to UtilityModule text, i.e. start of module
while f > 0 and rom_word(f) != m - f + 16:
    f -= 4
if f == 0:
    raise Exception("%s not found" % search_module.decode())
f -= 16
kernel_size = f - 4
print(
    "Found start of %s at %d, i.e. kernel runs until %d"
    % (search_module.decode(), f, kernel_size)
)

# Now find all modules; each is preceded by a size word, and the last module is followed by a zero word.

kernel_fn = "modules/00000000 - kernel.bin"
print(f"Save kernel as {kernel_fn}")
with open(kernel_fn, "wb") as kf:
    kf.write(rom[: f - 4])

while 1:
    module_size = rom_word(f - 4)
    if module_size == 0:
        print("End of module chain at %d (%x)" % (f, f))
        break

    # Extract null-terminated title
    module_title = rom_string(f + rom_word(f + 16))

    # Extract null-terminated copyright
    module_copyright = rom_string(f + rom_word(f + 20))

    print(
        "Module: start=0x%x, title=%s, copyright=%s, size=%d"
        % (f, repr(module_title), repr(module_copyright), module_size)
    )
    module_list.write(f"{module_title.decode()}\n")
    module = rom[f : f + module_size]
    assert len(module) == module_size
    module_fn = "modules/%08x - %s.riscosmodule" % (
        f,
        bytearray(
            c if (c != ord("/") and 32 <= c <= 127) else 32
            for c in (module_title + b" - " + module_copyright)
        ).decode(),
    )
    print("-> save to %s" % repr(module_fn))
    with open(module_fn, "wb") as mf:
        mf.write(module)
    f += module_size

if len(rom) - f < 10000:
    print(
        "Not much room at the end of the ROM; it's probably an old ROM with no ResourceFS"
    )
    credits = rom[f:]
    credits = credits[: credits.find(b"\x00")]
    for line in credits.split(b"\n"):
        if line:
            print(line)
else:
    extract_resourcefs(f)


def extract_resourcefs(f):
    print("Looking for ResourceFS at 0x%x" % f)
    while 1:
        offset_to_next = rom_word(f)
        if offset_to_next == 0:
            break

        offset = 20
        filename = rom_string(f + offset)
        print(offset_to_next, repr(filename))

        offset = (offset + len(filename) + 1 + 3) & ~3
        file_size = rom_word(f + offset) - 4
        print(file_size)

        offset += 4
        file_data = rom[f + offset : f + offset + file_size]
        assert (
            len(file_data) == file_size
        ), f"file data is {len(file_data)} B long -- does not match file size {file_size} B"

        offset = (offset + file_size + 3) & ~3
        # print(offset)

        assert offset == offset_to_next

        localfn = "resources/%s" % translate_filename(filename)
        print("%s -> %s (%d bytes)" % (repr(filename), repr(localfn), file_size))
        p = []
        for part in localfn.split("/")[:-1]:
            p.append(part)
            pth = "/".join(p)
            if not os.path.exists(pth):
                os.mkdir(pth)
        with open(localfn, "wb") as rf:
            rf.write(file_data)

        f += offset_to_next
