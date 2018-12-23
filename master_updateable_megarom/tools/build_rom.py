from __future__ import print_function
# This attempts to build some useful MOS ROM replacements.

# Change this to point to your source ROM image -- probably mos3.20, MOS321.rom,
# or mos3.50:
SOURCE_ROM = 'mos3.20'

# List all ROMs you want to patch into the image, plus their locations, here:
PATCH_ROMS = [
    # Replace ADFS with Master user port MMFS
    (0x14000, 'U_MAMMFS.rom'),

    # Replace ViewSheet with UPURS 5.0R
    (0x08000, 'UPURS50R.rom'),
]

# The new image will be written here
DEST_ROM = 'newmos.rom'

#######

import hashlib

def show_hashes(image):
    for blk in range(0, 131072, 16384):
        print("  %6d-%6d (%5x-%5x): md5 hash %s" % (
            blk, blk+16383, blk, blk+16383,
            hashlib.md5(image[blk:blk+16384]).hexdigest(),
        ))

print("Reading %s\n" % SOURCE_ROM)
image = open(SOURCE_ROM, 'rb').read()
assert len(image) == 131072, "Image %s is %d bytes long, expected 131072" % (
    SOURCE_ROM, len(image),
)
show_hashes(image)

print()
for location, filename in PATCH_ROMS:
    patch = open(filename, 'rb').read()
    print("Patching %s (%d/&%x bytes) at location %d/&%x" % (
        filename, len(patch), len(patch), location, location,
    ))
    image = image[:location] + patch + image[location+len(patch):]
    assert len(image) == 131072, "Patching failed; length incorrect"
    print()

show_hashes(image)
print()

print("Writing %s" % DEST_ROM)
open(DEST_ROM, 'wb').write(image)
