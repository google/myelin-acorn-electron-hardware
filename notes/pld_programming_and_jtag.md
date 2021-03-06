CPLD and FPGA Programming (using JTAG)
======================================

Most of the projects in this repository include a programmable logic device
(PLD), either a CPLD (Xilinx XC9500XL) or an FPGA (Lattice MachXO or Intel Max
10).  All of these include flash memory that needs to be programmed.

The easiest way to program the chips on my boards
=================================================

If you've come to this page because you're building one of the boards from this
repository and need to program in a .jed or .svf file, this section is what
you're looking for.

_Something I'm working on (EXPERIMENTAL SO FAR)_:
- Get an Arduino Leonardo or Pro Micro board:
  - Most reliable way: Get an original Leonardo from an Arduino distributor (TODO add link), or [an original Pro Micro direct from SparkFun](https://www.sparkfun.com/products/12640)
  - There are plenty on eBay and Aliexpress, but labelling is inconsistent, so be careful when shopping there.
  - Leonardo shopping advice:
    - Make sure it has an ATMEGA32U4 chip.  If it has an ATMEGA328P, it's an Uno, not a Leonardo.
  - Pro Micro shopping advice:
    - Make sure you get one with an ATMEGA32U4 chip and a micro USB socket.  Often you'll see ones with ATMEGA328P or mini USB -- these are different boards and won't work here.
    - It doesn't matter for this project, but I've also found two different form factors; the original measures 1.3 by 0.7 inches.
    - There are 3.3V and 5V versions; the 5V version runs at 16MHz, is more flexible for retro hardware work, and works to program the Xilinx XC9500XL-series CPLDs in many of the projects in this repository, but the 3.3V version will also work fine for the project, and will be required for interfacing with 3.3V-only chips (all modern FPGAs, including the Lattice MachXO/MachXO2 and Intel MAX 10, which are used in this repository).
- Program the simple_cpld_programmer firmware into it:
  - Using the Arduino IDE:
    - Open [simple_cpld_programmer_firmware.ino](../simple_cpld_programmer/simple_cpld_programmer_firmware/simple_cpld_programmer_firmware.ino) in the Arduino IDE
    - Plug the board into a USB port
    - Select the correct board type: _Arduino Leonardo_ if you have a Leonardo or a 5V Pro Micro, or _LilyPad Arduino USB_ if you have a 3.3V Pro Micro
    - Select the port associated with the board
    - Click the 'Upload' button
  - Or at the command line:
    - Plug the board into a USB port
    - cd simple_cpld_programmer/simple_cpld_programmer_firmware
    - make upload
- Wire it to the JTAG port on the target board (the one with the CPLD you wish to program):
  - JTAG GND to Arduino GND
  - JTAG TDO to Arduino pin 18
  - JTAG TMS to Arduino pin 19
  - JTAG TCK to Arduino pin 20
  - JTAG TDI to Arduino pin 21
- Use the simple_cpld_programmer/tools/program_cpld.py script to play JTAG
  commands from the .svf file and program the chip.
  - python simple_cpld_programmer/tools/program_cpld.py path/to/datafile.svf
  - Or from a project folder: cd cpld; make program

_Ready made Xilinx solution_: If you already have a Xilinx Platform Cable and an
ISE installation, you can use Xilinx iMPACT to program the .jed file into the
chip.

_Ready made open source solution_: If you have an FTDI FT232H or FT2232H
breakout board, you can use xc3sprog to program the .jed file into the chip.

- Install xc3sprog
- From a project folder: cd cpld; make program-xc3sprog

_Trickier open source solution_: If you have a JTAG adapter supported by
openocd, you can use it to play the .svf file to program the chip.

Cables
======

If you're looking for the best dev experience, the best cable is the official
one from the device manufacturer, so a Xilinx Platform Cable II, an Intel FPGA
Download Cable II (renamed from the Altera USB Blaster II), or a Lattice
Programming Cable (HW-USBN-2B).

I use Xilinx's ISE toolchain to build my CPLD projects, but then I use my
J-Link and [my fork of xc3sprog with J-Link support
added](https://github.com/myelin/xc3sprog/tree/jlink) to program the .jed file
into the chip.  In hindsight this was way more complex than necessary, as
xc3sprog already supports FT2232H modules, which are pretty cheap, so I could
just have used one of those, but the J-Link is so good for debugging Arm chips
that my instinct is to use it for everything :)

Apparently Lattice Diamond will detect and use an [FTDI FT2232H Mini
Module](https://www.digikey.com/products/en?keywords=768-1030-ND) as a JTAG
cable, so that's probably the best option for low-cost development or device
programming.

FT232H chips are slightly cheaper and also work with OpenOCD, XC3SPROG, and
UrJTAG, so they would be a good choice if you were to design your own JTAG
adapter.  I don't know if they will work with Diamond or not.

I haven't found any lower cost options for Intel/Altera chips, so I've just
been using OpenOCD and my J-Link to play the SVF file generated by Quartus.

Pinouts
=======

The first PLD eval board I bought when starting on the retro hardware hacking
was an lc-tech XC9572XL board, with a 2x5 0.1" header that I assumed was a
standard JTAG connector, or at least a standard Xilinx JTAG connector.
Unfortunately it was actually a standard Altera/Intel JTAG connector, so now
all my projects have a slightly confusing JTAG pinout.

Here's the format I've been using, as documented in Intel's USB Blaster
datasheet (UG-USB81204) and USB-Blaster II User Guide (UG-01150), when looking
into the header on the PCB; this will be mirrored horizontally when looking
into the plug on the cable.

    +-------------------------------------+
    | (2)GND (4)VCC (6)--- (8)--- (10)GND |
    | (1)TCK (3)TDO (5)TMS (7)---  (9)TDI |
    +--------------        ---------------+

Apparently this is compatible with the standard AVR JTAG pinout, which is perhaps
how it found its way to my eval board.

Xilinx
------

From the Xilinx Platform Cable USB datasheet (DS300), here's the standard
Xilinx JTAG pinout: 2x7, with an awkward 2mm pin spacing:

    +-----------------------------------------------------+
    | (2)VCC (4)TMS (6)TCK (8)TDO (10)TDI (12)--- (14)--- |
    | (1)GND (3)GND (5)GND (7)GND  (9)GND (11)GND (13)GND |
    +---------------------        ------------------------+

The Platform Cable USB II datasheet (DS593) shows some slight changes -- one
GND is gone, and HALT/PGND are new:

    +------------------------------------------------------+
    | (2)VCC (4)TMS (6)TCK (8)TDO (10)TDI (12)--- (14)HALT |
    | (1)--- (3)GND (5)GND (7)GND  (9)GND (11)GND (13)PGND |
    +---------------------        -------------------------+


Lattice
-------

Lattice has a bunch of standard connectors, starting with this 2x5 connector
that physically matches the Altera connector, but with a different pinout:

    +--------------------------------------------+
    | (2)GND (4)GND (6)VCC (8)GND (10)ispEN/PROG |
    | (1)TCK (3)TMS (5)TDI (7)TDO  (9)TRST/DONE  |
    +-------------------      -------------------+

This looks like the pinout that shows up on all the clone programmers when you
Google something like "lattice jtag pinout":

    +---------------------------------------+
    | (2)GND (4)GND (6)VCC (8)INIT (10)PROG |
    | (1)TCK (3)TMS (5)TDI (7)TDO   (9)TRST |
    +-------------------      --------------+

Lattice's UG48 also lists this 1x8 connector:

    VCC TDO TDI ispEN/PROG TRST/DONE TMS GND TCK TRST/DONE

And this 1x10 connector:

    VCC TDO TDI ispEN/PROG TRST/DONE TMS GND TCK TRST/DONE INITN
