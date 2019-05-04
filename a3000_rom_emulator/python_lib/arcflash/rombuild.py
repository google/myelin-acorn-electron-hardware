from __future__ import print_function

# Arcflash ROM builder

import hashlib
import pkg_resources
import struct
import sys

from arcflash import arcflash_pb2
from arcflash import uploader

__all__ = ["_1M", "_2M", "_4M", "ROM", "FlashImage"]

_512k = 512*1024
_1M = 1024*1024
_2M = _1M * 2
_4M = _1M * 4

class ROM:
    def __init__(self, name, files, size=_2M, tag=None, cmos=None):
        self.name, self.files, self.size, self.cmos, self.tag = \
            name, files, size, cmos, tag
        self.ptr = -1  # byte location in flash

    def readable_size(self):
        if self.size < _1M:
            return "%dk" % (self.size/1024)
        return "%dM" % (self.size/_1M)

    def as_proto(self):
        p = arcflash_pb2.FlashBank(
            bank_ptr=self.ptr,
            bank_size=self.size,
            bank_name=self.name,
            )
        if self.tag:
            p.bank_tag = self.tag
        if self.cmos:
            p.cmos_tag = self.cmos
        return p

    def __repr__(self):
        if self.tag:
            if self.name:
                desc = "%s (%s)" % (self.tag, self.name)
            else:
                desc = self.tag
        else:
            desc = self.name
        desc += " [%s]" % self.readable_size()
        return desc

def read_rom_file(fn, byte_order):
    bytes = open(fn, "rb").read()

    if len(bytes) % 4:
        # special case for arthur 1.20 image
        if len(bytes) == 524289 and bytes[-1] == '\\':
            print("Dropping the last byte of known Arthur image")
            bytes = bytes[:512*1024]
        else:
            bytes += b"\xFF" * (4 - (len(bytes) % 4))

    if byte_order == "0123":
        return bytes

    if byte_order == "2301":
        # swap pairs of bytes (Risc PC adapter)
        output = []
        for idx in xrange(0, len(bytes), 4):
            output.append(bytes[idx+2] + bytes[idx+3] + bytes[idx] + bytes[idx+1])
        return b"".join(output)

    if byte_order == "3210":
        # reverse bytes in each word (A5000 adapter)
        output = []
        for idx in xrange(0, len(bytes), 4):
            output.append(bytes[idx+3] + bytes[idx+2] + bytes[idx+1] + bytes[idx])
        return b"".join(output)

    raise ValueError("Invalid byte_order value: %s" % byte_order)

def FlashImage(roms,
               byte_order="0123",
               bootloader_512k=False,
               bootloader_image_override=None,
               skip_bootloader=False):
    print("Arcflash ROM builder / image flasher\n")

    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if len(args):
        cmd = args.pop(0)
    else:
        cmd = 'build'

    # Arcflash v1 has 16MB of flash
    flash_size = _1M * 16
    bootloader_bank_size = 0 if skip_bootloader else _1M

    # Fit ROM images into the space available.  We have 16M, but flash banks
    # must be aligned -- 4M banks must be on a 4M boundary, and 2M banks must
    # be on a 2M boundary.  As such we want to fit in the 4M images first,
    # then 2M, then 1M (with the exception of the bootloader, which is a 1M
    # bank that must be placed at the start of the flash).

    roms_by_size = {}
    for rom in roms:
        roms_by_size.setdefault(rom.size, []).append(rom)
    used_blocks = [(0, bootloader_bank_size)]  # start with a 1M ROM at position zero
    flash_free = flash_size - bootloader_bank_size
    for size, romlist in sorted(roms_by_size.items(), reverse=True):
        for rom in romlist:
            placed = False
            for ptr in range(0, flash_size, size):
                # Check if ptr is in any of the ranges in used_blocks
                block_free = True
                for used_start, used_len in used_blocks:
                    if ptr >= used_start and ptr < used_start + used_len:
                        block_free = False
                        break
                if not block_free: continue

                print("Placing rom %s at flash+%dk" % (repr(rom), ptr/1024))
                used_blocks.append((ptr, rom.size))
                rom.ptr = ptr
                placed = True
                flash_free -= rom.size
                break
            if not placed:
                raise Exception("No room for rom %s.  Need %dk, but only have %dk." % (
                    repr(rom), rom.size/1024, flash_free/1024))
    print("Everything fits; %dk/%dk used, %dk free" % (
        (flash_size-flash_free)/1024, flash_size/1024, flash_free/1024))

    print("\nThe menu will look like:\n")
    romid = 0
    for rom in roms:
        print("%s: %s (%s)" % (chr(romid + ord('A')), rom.name, rom.readable_size()))
        romid += 1
    print()

    descriptor = arcflash_pb2.FlashDescriptor(
        bank=[rom.as_proto() for rom in roms],
        flash_size=flash_size,
        free_space=flash_free,
    )

    # Time to build the flash image!
    # Start by collecting all images aside from the bootloader.
    EXPLAIN_FLASH_BUILD = 0
    flash = b""
    ptr = bootloader_bank_size
    for _, rom in sorted((rom.ptr, rom) for rom in roms):
        if EXPLAIN_FLASH_BUILD: print("Adding %s at %d (currently %d)" % (rom, rom.ptr, ptr))
        assert ptr <= rom.ptr
        if rom.ptr > ptr:
            pad_len = (rom.ptr - ptr)
            if EXPLAIN_FLASH_BUILD: print("- Adding padding of %d bytes first" % pad_len)
            flash += b"\xFF" * pad_len
            ptr += pad_len
        data = []
        size = 0
        for fn in rom.files:
            fdata = read_rom_file(fn, byte_order)
            data.append(fdata)
            size += len(fdata)
        assert size <= rom.size, \
            "Read %d bytes for ROM %s, but it's specified to only have %d" % (size, rom, rom.size)
        if size < rom.size:
            data.append(b"\xFF" * (rom.size - size))
        data = b"".join(data)
        assert len(data) == rom.size
        if EXPLAIN_FLASH_BUILD: print("- Adding %d bytes (ROM %s)" % (len(data), rom))
        flash += data
        ptr += rom.size
    build_flash_size = flash_size - bootloader_bank_size
    if len(flash) < build_flash_size:
        pad_len = build_flash_size - len(flash)
        if EXPLAIN_FLASH_BUILD: print("Adding %d bytes of padding at end" % pad_len)
        flash += b"\xFF" * pad_len
    assert len(flash) == build_flash_size, \
        "Flash should be %d bytes long but it's actually %d" % (build_flash_size, len(flash))

    # TODO add rom image hash to descriptor
    descriptor.hash_sha1 = hashlib.sha1(flash).hexdigest()
    print("Flash images collected; %dk, hash %s" % (len(flash)/1024, descriptor.hash_sha1))

    if skip_bootloader:
        bootloader_bank = ''
    else:
        bootloader_size = 384 * 1024
        # The bootloader goes at the start of first 384k, and the encoded
        # descriptor followed by a length word goes at the end.  We can't put this
        # in until the end though, as it contains a hash of the rest of the flash
        # data.
        bootloader_binary = pkg_resources.resource_string(__name__, "bootloader.bin")
        descriptor_binary = descriptor.SerializeToString()

        assert len(bootloader_binary) + len(descriptor_binary) + 4 < bootloader_size, \
            "Bootloader binary plus descriptor won't fit in %sk - need to change memory map" % (bootloader_size/1024)
        bootloader_bank = (
            # Start with the binary
            bootloader_binary +
            # Then padding to make binary + padding + descriptor + length == 384k
            (b"\xff" * (bootloader_size - len(bootloader_binary) - len(descriptor_binary) - 4)) +
            descriptor_binary +
            struct.pack("<i", len(descriptor_binary)) +
            # Then padding to 1M (which in future will also contain CMOS data)
            (b"\xff" * (bootloader_bank_size - bootloader_size))
        )
        if bootloader_image_override:
            # Bootloader image overridden -- ignore descriptor etc
            bootloader_binary = read_rom_file(bootloader_image_override, byte_order)
            bootloader_bank = (
                bootloader_binary +
                ("\xff" * (bootloader_bank_size - len(bootloader_binary)))
            )
        if bootloader_512k:
            # Hack to allow running the bootloader on an A310 and Arcflash v1 without modifying LK12.
            # Electrically this has LA18 coming in on the nOE pin, but this is OC on Arcflash v1.
            print("Repeating bootloader twice in first 1MB, to accommodate unmodified A310")
            bootloader_bank = bootloader_bank[:512*1024] + bootloader_bank[:512*1024]
        print("Descriptor is %d bytes long, placed at %08X." % (
            len(descriptor_binary),
            bootloader_size - 4 - len(descriptor_binary)),
        )
        print("Bootloader added.")
    assert(len(bootloader_bank) == bootloader_bank_size)

    # Now put it all together
    flash = bootloader_bank + flash
    assert len(flash) <= flash_size, \
        "An error occurred: flash ended up %d bytes long and should be max %d" % (len(flash), flash_size)

    # And save it!  (Or upload it)
    if cmd == 'save':
        if not len(args):
            raise Exception("Syntax: %s save <filename>" % sys.argv[0])
        fn = args.pop(0)
        print("Saving flash image to %s" % fn)
        open(fn, "wb").write(flash)
        return

    if cmd == 'upload':
        print("Uploading to flash")
        uploader.upload(flash)
