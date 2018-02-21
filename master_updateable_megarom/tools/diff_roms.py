from glob import glob
import sys

roms = sorted(sys.argv[1:])

print roms

images = [open(rom).read() for rom in roms]

n = len(roms)

for i in range(128*1024):
    match = not any(image[i] != images[0][i] for image in images)
    print "%06d: %s%s" % (i, " ".join("%02x" % ord(image[i]) for image in images), "" if match else " MISMATCH")
