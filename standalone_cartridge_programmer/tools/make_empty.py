# Make an empty 16kB ROM image

open("empty.rom", "w").write("\xff" * 16384)
