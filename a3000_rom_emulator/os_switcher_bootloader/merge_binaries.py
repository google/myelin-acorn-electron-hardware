# Merge ROM images to create the Arcflash bootloader image

import struct
import sys

output_fn = sys.argv[1]

# Read binaries
risc_os = open("risc_os.bin", "rb").read()
arc_boot = open("arc_boot.bin", "rb").read()
rpc_boot = open("rpc_boot.bin", "rb").read()

# Combine everything.  See README.md for details on memory map.
f = open(output_fn, "wb")

# Start with RISC OS
f.write(risc_os)

arc_offset = len(risc_os) + 8
rpc_offset = arc_offset + len(arc_boot)

print("Arc bootloader at %08x, RPC bootloader at %08x" % (arc_offset, rpc_offset))

# Offset of RPC bootloader
f.write(struct.pack("<i", rpc_offset))

# Offset of Arc bootloader
f.write(struct.pack("<i", arc_offset))

# Arc bootloader
f.write(arc_boot)

# RPC bootloader
f.write(rpc_boot)

total = f.tell()
print("Arcflash bootloader size %d (%dk, 0x%08x)" % (total, (total+1023)/1024, total))

# And we're done!
f.close()
