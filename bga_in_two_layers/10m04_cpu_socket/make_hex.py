from intelhex import IntelHex

ih = IntelHex()

ih.fromfile("rom_one.bin", format="bin")
ih.write_hex_file(open("rom_one.hex", "w"))


