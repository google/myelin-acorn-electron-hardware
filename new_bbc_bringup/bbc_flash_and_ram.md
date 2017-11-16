Using flash and RAM in the BBC's ROM sockets
============================================

_Part of [Starting out with a new BBC Model B](README.md)._

Each ROM socket is designed to take a single 16kB ROM.  ROMs are selected by
writing to the lower four bits of &FE30, which is latched by IC76.  Four bits
means there are actually 16 banks, but only the lower two bits are used to drive
the chip select inputs on the ROM sockets, so each socket actually maps onto
four banks.

In detail: Pins 14-11 of IC76 latch D0-3.  Pins 14-13 (D0-1) drive A-B on IC20,
which means:

- Pin 12 goes low and selects IC52 (BASIC) when banks 0, 4, 8, 12 are selected
- Pin 11 goes low and selects IC88 (DFS) when banks 1, 5, 9, 13 are selected
- Pin 10 goes low and selects IC100 when banks 2, 6, 10, 14 are selected
- Pin 9 goes low and selects IC101 when banks 3, 7, 11, 15 are selected

What people typically do in modern days is solder wires from the spare outputs
of IC76 to the higher address pins on bigger chips, which allows up to 64kB to
be mapped to each socket.

Here's the standard 28-pin layout for the BBC B's four ROM sockets.  It matches
various hard to find EPROM chips, and is close enough to a few modern flash and
SRAM pinouts to be adaptable with just a few mods.

- 10-3, 25, 24, 21, 23, 2, 26 = A0-13
- 11-13, 15-19 = D0-7
- 1, 27 = 5V
- 22 = OE
- 20 = CS

~~~~
 5V  1 +---+ 28 5V
A12  2 |   | 27 5V
 A7  3 |   | 26 A13
 A6  4 |   | 25 A8
 A5  5 |   | 24 A9
 A4  6 |   | 23 A11
 A3  7 |   | 22 OE#
 A2  8 |   | 21 A10
 A1  9 |   | 20 CE#
 A0 10 |   | 19 D7
 D0 11 |   | 18 D6
 D0 12 |   | 17 D5
 D2 13 |   | 16 D4
VSS 14 +---+ 15 D3
~~~~

Notes on good places to solder to: http://regregex.bbcmicro.net/bmem.htm

- BANK2 to the unoccupied + pad of D5 between IC98 and IC99 = IC76 pin 12.
- BANK3 to the unoccupied + pad of D4 next to IC99 = IC76 pin 11.
  - For some reason D4 is connected to ROMSEL for me, so I'm going straight to the IC76 pins instead.
- /WE to pin 8 of IC77 at the top left of the motherboard, or pin 24 of IC73.
- /RD to pin 6 of IC77, or pin 25 of IC73

Notes on locations:

- IC76 is two rows above PL9
- IC77 is a 14-pin chip, to the right of the 68B54 (far left)
- IC73 is a 28-pin chip, right below the analogue in port (center top)

SST39SF010A
-----------

This is a 32-pin 128kB flash chip, 64kB of which is conveniently usable.  As it's bigger than the 28-pin ROM sockets, it overhangs a little.

On my machine, I put a this in IC100, with a 28-pin socket underneath it to lift
it up high enough to clear the decoupling capacitor to the north.

~~~~
    NC*    +---+    VDD*
    A16*   |   |    WE#*
    A15* 1 |   | 28 NC*
    A12  2 |   | 27 A14*
    A7   3 |   | 26 A13
    A6   4 |   | 25 A8
    A5   5 |   | 24 A9
    A4   6 |   | 23 A11
    A3   7 |   | 22 OE#*
    A2   8 |   | 21 A10
    A1   9 |   | 20 CE#
    A0  10 |   | 19 D7
    D0  11 |   | 18 D6
    D0  12 |   | 17 D5
    D2  13 |   | 16 D4
    VSS 14 +---+ 15 D3
~~~~

Modifications I made:

FROM TOP LEFT PIN DOWN:
- cut top pin
- lift A16 and wire to BANK3 (IC76 pin 11)
- lift pin 1 and wire to BANK2 (IC76 pin 12)

FROM TOP RIGHT PIN DOWN:
- wire VDD to pin 28 on neighbour
- wire WE# to /WE (IC77 pin 8)
- cut pin 28 (NC)
- lift pin 27 (A14) and wire directly across to the left, to pin 2 (A12)
- skip 4 pins, then lift pin 22 (OE#) and wire to /RD (IC77 pin 6 / IC73 pin 25)

62256
-----

This is a 32kB 28-pin RAM chip, which provides two sideways RAM banks.  Ideally
I would use a 64kB chip, for four banks, but I couldn't find any with a
convenient pinout.

(The AS6C1008 would be ideal if it didn't require CMOS
levels, and the IS62C1024 is perfect but would require an adapter board to fit
the ROM socket.)

I put this in IC101, on top of an extra socket, for convenience, and because I
was afraid I would bump the surrounding components while soldering flying leads
to the chip's pins!

~~~~
    A14* 1 +---+ 28 5V
    A12  2 |   | 27 WE#*
    A7   3 |   | 26 A13
    A6   4 |   | 25 A8
    A5   5 |   | 24 A9
    A4   6 |   | 23 A11
    A3   7 |   | 22 OE#*
    A2   8 |   | 21 A10
    A1   9 |   | 20 CE#
    A0  10 |   | 19 D7
    D0  11 |   | 18 D6
    D0  12 |   | 17 D5
    D2  13 |   | 16 D4
    VSS 14 +---+ 15 D3
~~~~

The modifications here are fairly minimal; all you need to do is wire up A14 and WE#.

- lift pin 1 (top left) and wire to BANK2 (IC76 pin 12)
- lift pin 27 (one down from top right) and wire to /WE (IC77 pin 8)

I would expect to have to do this as well, but my RAM is working fine without it, so consider this optional:

- lift pin 22 and wire to /RD (IC77 pin 6)

Once everything is soldered up
------------------------------

- Double check that S32 and S33 are in their WEST positions, connecting to A13
  rather than 5V. This passes A13 through to the ROM sockets, enabling 16 kB ROM
  banks.  Your board will probably have this set up correctly already, but if you find that you're only getting 8kB out of each bank, check these jumpers.

Once this is working, it's time to program the flash, and try out UPURS :)
