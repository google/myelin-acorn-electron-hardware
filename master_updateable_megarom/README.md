Updateable BBC Master MegaROM
=============================

http://myelin.nz/acorn/megarom

A board that replaces IC24, the 1 megabit ROM containing the OS and sideways
banks 9-15 on a Master 128, and allows you to update the contents of the ROM
over USB (via a microcontroller) while the machine is running.

Status: I've built up a PCB with an SST39SF010A (128kB) flash chip,
implemented the CPLD design, and written the AVR firmware.  Flash programming
and readback works with the board running standalone and inside a Master 128.
I think this is ready for others to try out.

- [PCB design](pcb/)
- [Xilinx XC9572-64VQG CPLD design](cpld/)
- [Pro Micro firmware for USB interface](avr_firmware/)

To do for next version
----------------------

Make the board compatible with a Model B, providing 8 x 16kB sideways banks:

- Add jumpers for A14 and A15 so they can be wired to IC76
- Add jumper to connect socket pin 20 (/CS) to cpld_JP1

Installation
------------

First test the board outside the Master 128.  Connect a JTAG adapter to the JTAG
port on the top left of the board, which uses the Altera USB Blaster pinout,
with pin 1 on the bottom left.

Wire the SPI port up to an ATMEGA32U4-based Arduino board, like a Leonardo or
Pro Micro.  From left to right: GND, SCK (Arduino pin 15), SS (pin 10), MOSI
(pin 16), MISO (pin 14).

Connect power to the EXTPWR port -- GND on the left, 5V on the right.

Program the CPLD and the ATMEGA32U4, then make a serial connection to the board
and send I<CR>.  It should respond with the size of the flash chip, and "OK".

To program an image into the flash: python program_rom.py <rom file>

To read the current flash image: python read_rom.py

If you can successfully program and read an image (noting that you'll get an
error if your image file isn't the same size as the flash soldered onto the
board), it's time to install it in your Master 128.

First, *DISCONNECT POWER FROM THE EXTPWR PORT*.  Otherwise you'll end up
trying to power your Master 128 via USB, or you may short your USB port's 5V
supply to the Master 128's power supply, which will also be bad.

Now remove your MOS ROM (IC24, on the far right hand side of the motherboard,
just below the Econet module socket), and plug the board in, then turn the
machine on.  It should boot with the image you just programmed into the flash.

If you run program_rom.py or read_rom.py now, you should see screen
corruption, and the machine will probably crash.  This is expected, because
when accessing the flash, the BBC is blocked out, and gets garbage data.
Hitting Ctrl-BREAK (and maybe \*FX 200,2 then BREAK to clear the memory, if
you get a "Bad sum" error) should fix it though.

One way to stop the machine from trying to access the flash while you're
writing to it is to disable interrupts and send the processor into a loop,
like this:

    P%=&1000
    [SEI:.A JMP A
    CALL &1000

Building a ROM image
--------------------

For more info on the MOS ROM layout, see [J.G.Harston's "Replacing the Master
System ROM"](http://mdfs.net/Info/Comp/BBC/SROMs/MegaROM.htm).  The MOS itself
occupies the first 16kB of the chip, but also various other spots, depending on
the version, so building an image that will function correctly is a little
tricky.

[build_rom.py](tools/build_rom.py) will combine a bunch of individual ROM images
and fragments into a single 128kB image.  You'll either need a 3.20 or 3.50 ROM
image (distributed with various emulators -- b-em, jsbeeb, etc) or J.G.Harston's
MOS321.rom, from the link above), and all the ROM images you want to patch into
the image.  Patch ROMs can be any size, so if you just want to replace a few
bytes in the middle of another image, that's OK.

Practically, with MOS 3.20, you can replace DFS, ADFS, ViewSheet, EDIT, and
BASIC with any 16kB ROM image, and VIEW with any image up to 14848 bytes. JGH's
MOS321.rom replaces EDIT with ANFS, ViewSheet with HADFS, and adds mouse, Y2K,
and IDE compatibility.

For MOS 3.50, ADFS and DFS share code so they come as a pair, and MOS code
occupies space in both images, as well as the Terminal/Tube image (as in 3.20).
This means you can replace ViewSheet, EDIT, BASIC, and VIEW with any 16kB ROM
image, and if you don't want floppy disk compatibility, you can replace DFS with
a ROM up to 12032 bytes long, and ADFS with a ROM up to 16720 bytes long.

Some more links:

- [BBC Master and Y2K](http://www.adsb.co.uk/bbc/bbc_master.html): Y2K patches
  for 3.20 and 3.50.

- A [thread on Stardot discussing mixing and matching these and the 3.20/3.50
  versions](http://stardot.org.uk/forums/viewtopic.php?t=8115).  It sounds like
  Mark Haysman of [RetroClinic](https://www.facebook.com/RetroClinic/) has made
  ROM images with all these patches, although you may need to buy a
  [MultiOS](https://www.facebook.com/RetroClinic/posts/567921580048712) to get a
  copy.

- The [Raf Giaccio Collection](http://8bs.com/submit/subry2kfix.htm) looks
  worth trying out also.

Similar projects
----------------

I don't believe anyone else has made an in-system-updateable MOS ROM
replacement, but these projects allow you to program a flash/EEPROM chip with
multiple images and select between them with a physical switch:

- RetroClinic
  [DualOS](http://chrisacorns.computinghistory.org.uk/New4Old/RetroClinic_DualOS.html)
  and [MultiOS](https://www.facebook.com/RetroClinic/posts/567921580048712).

- [Sundby/System DIY BBC Master quad OS ROM
  switch](http://www.sundby.com/index.php/diy-bbc-master-quad-os-rom-switch/).

- [IFEL/ctorwy31 Switchable Master 128 MOS OS ROM
  3.20/3.50](http://chrisacorns.computinghistory.org.uk/New4Old/ctorwy31_MasterOS.html).

Modification for use in a pair of Model B ROM sockets
-----------------------------------------------------

The MegaROM also works when installed in a Model B!  It gives you 8 flash
banks, which behave like true ROMs, ignoring writes from the BBC.

This does not work nearly as well as it does in a Master 128, because the
Master 128 has a separate data bus for the MOS ROM, whereas the Model B just
connects all the ROM chips to the system bus.  On a Master 128 you can just
run read_rom.py and program_rom.py without worrying about what the host
machine is doing (if you don't care about it crashing), whereas on a Model B
you need to force the machine into an idle state before running anything.

I tried a bunch of ways of doing this, and finally hit upon one that worked.
The MOS 6502 has a bunch of undocumented instructions, many of which just halt
the CPU.  If you have the standard Model B BASIC ROM installed in the MegaROM
board, there's a character 0x02 at &8038, and you can halt the machine with
CALL &8038.  This doesn't completely let go of the bus, but if you CALL &8038
then hold down the BREAK key while the MegaROM is being read or programmed, it
works.

#### A couple of things that didn't work

- Doing nothing at all (like on the Master 128).

- Just holding down BREAK (presumably this halted the CPU while reading an
  address from RAM or the OS ROM, which took over the bus).

- Just executing the 'crash' instruction with CALL &8038.  I don't know why
  this wasn't sufficient to halt the machine; maybe the 6502's address bus
  isn't stable in the crashed state?

All of these resulted in about a 20% error rate, suggesting that the MegaROM
read/update code is lucky enough to perform most of its reads during the low
clock period, when the bus is free, but something else takes over during the
high period.

#### The clever way to do it

The ideal way to do this would be to use the low period of the BBC's clock cycle
to perform all flash access.  We have partial access to the clock, via the /OE
pin, which goes low during the high part of the clock cycle, however this
behaviour is masked during accesses to &FCxx/FDxx/FExx, so it would be necessary
to use a separate clock to wait for a rising edge on /OE and perform the memory
access within the next 250 ns.  With some careful synchronization, it's probably
possible to make this work with the 8MHz SPI clock.

### Modification instructions

This board can also be used to fill two of the ROM sockets on a Model B, and
provide 8 16kB flash banks.  Some modifications are required.

The Master 128's MOS ROM socket differs from the Model B's ROM sockets in the
following ways:

- Pin 1 is A15 on the Master, and 5V on the Model B
- Pin 27 is A14 on the Master, and 5V on the Model B
- Pin 22 is A16 on the Master, and /OE on the Model B
- Pin 20 is /CE on both, but is always tied low on the Master and is selectable
  on the BBC, and is left disconnected on this board.

Wiring it up like this should work:

- Cut pin 1 and solder a jumper wire from the top of the pin to IC76 pin 12.
- Cut pin 27 and solder a jumper wire from the top of the pin to IC76 pin 11.
- Solder a jumper wire from the top of pin 20 to the cpld_JP1 pin.
- Connect a jumper wire from pin 20 on the adjacent socket to the cpld_JP0 pin.

Changes are required to the Verilog also:

- Set flash_A16=0 when cpld_JP1=0, and A16=1 when cpld_JP2=0
- Set flash_nOE=0 when bbc_A16=0 and (cpld_JP1=0 or cpld_JP2 = 0)

These are included in master_updateable_megarom.v; just change this line:

    reg installed_in_bbc_master = 1'b1;

to this:

    reg installed_in_bbc_master = 1'b0;

Pictures
--------

![PCB front](pcb/pcb-front.png)

![PCB back](pcb/pcb-back.png)
