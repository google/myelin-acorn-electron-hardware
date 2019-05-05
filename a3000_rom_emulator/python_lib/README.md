# Arcflash

Arcflash is a flash ROM board for the Acorn Archimedes and Risc PC computers.

This is the Python support library, which lets you build your own flash
images, and program them into the memory on an Arcflash board connected over
USB.

Project homepage: http://myelin.nz/arcflash

Python library code: https://github.com/google/myelin-acorn-electron-hardware/tree/master/a3000_rom_emulator/python_lib

## Getting started

First, install the library with `pip install arcflash`.

Next, copy the following example and save it as `myrom.py`.  This assumes you have the [3QD classic rom archive](http://www.riscos.com/shop/products/101/index.htm) unpacked in a folder called `classics`.

~~~~
from arcflash.rombuild import *

FlashImage(
    roms=[
        ROM(
            tag="arthur030",
            name="Arthur 0.30",
            files=['classics/Arthur/Arthur_030'],
            size=_1M,
            cmos="arthur030",
            ),
        ROM(
            tag="arthur120",
            name="Arthur 1.20",
            files=['classics/Arthur/Arthur_120'],
            size=_1M,
            cmos="arthur120",
            ),
        ROM(
            tag="riscos201",
            name="RISC OS 2.01",
            files=['classics/RISC_OS_2/ROM_201'],
            size=_1M,
            cmos="riscos201",
        ),
        ROM(
            tag="riscos311",
            name="RISC OS 3.11",
            files=['classics/RISC_OS_3/ROM_311'],
            size=_2M,
            cmos="riscos311",
            ),
    ],
)
~~~~

Now run `python myrom.py save rom.bin` to build the flash image and save it as rom.bin.  This file should be 16MB long.  If that worked, plug in your Arcflash board and run `python myrom.py upload` to build and upload the flash image.
