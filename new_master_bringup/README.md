Bringing a BBC Master 128 motherboard to life
=============================================

Hywel Evans very nicely gave me a Master 128 motherboard, which I'm attempting
to get to work without all the surrounding hardware that it would usually have
(case, power supply, keyboard).

Power
-----

Step 1 is to get it powered.  It looks like you can skip the -5V power supply
and it will still work, just without the RS423 and cassette ports.  The latter
is often pretty important for the bringup process, but with any luck I can get
something working for now.  Later on I can either get a proper PSU, or use an
isolated DC-DC converter (which I can scavenge from an older project to make a
DMX lighting receiver), to produce -5V.

The motherboard has three separate pairs of blade connectors for 0V/5V.  The
0V lines are all connected together, but not the 5V lines -- the system must
actually have three separate power domains, although I assume they're usually
joined in the PSU.  (I've read that this dates back to the original BBC Micro,
which had a linear power supply with three 7805s, one for each motherboard 5V
connection.)

I'm going to just hook this up to a 10A 5V power supply, using alligator clips
to connect to the blade connectors for now.

Success!  It boots to "Acorn MOS" / "Acorn 1770 DFS", then hangs.  Time to see
if I can get something keyboard-like working.

Keyboard
--------

It looks like the Master 128 has the keyboard encoder logic on the
motherboard, so the keyboard connector is quite a lot longer than on the Model
B, and is connected directly to the rows and columns on the keyboard.

PL11
- 1 - C6
- 2 - BAT
- 3 - R0
- 4 - R6
- 5 - R7
- 6 - R2
- 7 - R1
- 8 - C11
- 9 - C10
- 10 - C12
- 11 - C0
- 12 - C2
- 13 - C9
- 14 - C4
- 15 - C5

PL24
- 1 - C8
- 2 - C7
- 3 - C3
- 4 - C1
- 5 - R5
- 6 - R4
- 7 - R3
- 8 - C (diode to C1) -- ctrl probably
- 9 - SHIFT LOCK (330R to IC10 pin 7)
- 10 - CAPS LOCK (330R to IC10 pin 6)
- 11 - POWER LED (330R to 5V)
- 12 - S (diode to C0) -- shift probably
- 13 - KBD SW (BREAK: GND when BREAK pressed, high-Z normally)
- 14 - GND
- 15 - 5V

Apparently the keyboard encoder pulls the columns low one by one, so we should
be able to use a CPLD which outputs '0' or 'Z' as appropriate.  Working on
this -- VHDL code in emulated_keyboard/emulated_keyboard.vhd.

Ctrl and Shift are interesting: these pins aren't connected to the keyboard
encoder: C has a diode down to C1; S has a diode down to C0.  So they'll
respectively be pulled to 0.7V when C0 and C1 are low.  Both connect to R7.  I
guess this is anti-ghosting, and we don't actually want to connect the CPLD to
C and S.

Can probably do a super hacky approach by shorting pins together too! 'R' is
C3 R4.  Connect PL24 pin 3 and 6 to hold down R.  Success!  Starting up with
'R' "pressed" results in the expected CMOS RAM reset message.

1024MAK on Stardot mentions that the Master 128 can use a BBC Micro keyboard
too.  Looks like they have mostly the same layout, although the rows and cols
are reorganized.

Pinout with CPLD dev board: need 24 pins plus vcc/gnd.  Plugged a bunch of
jumper wires into the keyboard socket on the Master board.  Matching these to
the CPLD board:

PL11
- 1 - C6 - skip
- 2 - (skip)
- 3 - R0 - P2
- 4 - R6 - P3
- 5 - R7 - P5
- 6 - R2 - P6
- 7 - R1 - P7
- 8 - C11 - skip
- 9 - C10 - skip
- 10 - C12 - skip
- 11 - C0 - skip
- 12 - C2 - skip
- 13 - C9 - skip
- 14 - C4 - skip
- 15 - C5 - skip

PL24
- 1 - C8 - skip
- 2 - C7 - skip
- 3 - C3 - skip
- 4 - C1 - skip
- 5 - R5 - P41
- 6 - R4 - P42
- 7 - R3 - P43
- 8 - (skip)
- 9 - (skip)
- 10 - (skip)
- 11 - (skip)
- 12 - (skip)
- 13 - KBD SW - P44
- 14 - GND
- 15 - 5V

PL7
- 1 - GND
- 2 - KBD SW
- 3 - 1MHZE
- 4 - NKBEN - P12
- 5 - SA4
- 6 - SA5
- 7 - SA6
- 8 - SA0 - P13
- 9 - SA1 - P14
- 10 - SA2 - P16
- 11 - SA3 - P18
- 12 - SA7
- 13 - BAT
- 14 - CA2
- 15 - +5V
- 16 - SHIFT LOCK
- 17 - CAPS LOCK

Wired this up and programmed the CPLD, and the machine hangs.  Disabling the
row outputs brings it back to life.  Eventually realized that the column
outputs from the keyboard encoder are open collector, so I'd need to add
pullups.  Nowhere to do that in my current rat's nest of wires... deciding if
I should just make a PCB for the whole thing.

Can I use pullups from a MCU to make it easier?

Figuring out what the internal pullups are.  Pulled R0 to GND through a 9.85k
resistor and measured 3.47V across it.  OC voltage is 5V.  So current was 0.35
mA.  1.53V over pullup / 0.35 mA = 4371 ohm. So short circuit current should
be 1.14 mA.  That looks good.  So we're talking 4-5k pullups on rows.

Pro Micro has 18 pins.  Needs 2 for PS/2 and 4 for SPI, leaving 12.  Just use
discrete resistors.

XC9572XL PCB (easiest option but only gives two key rollover, prob bad for games)
- Pin headers for PL11 and PL24
- 13 pullup resistors
- 3 indicator LEDs
- 3v3 regulator
- XC9572XL 44 pin $3.50
- Pro Micro $3

XC9500 PCB:
- As above except XC95144XL instead so +$3.75 and more difficult to solder

MachXO2 PCB:
- As for XC9572XL PCB except need four conversion chips, although also get way more room.
- Need to do this anyway for something one day.
- ACTUALLY I might not need much level translation here.
  - The column inputs are OC, so if I pull them to 3V3 they should work.
  - The rows are pulled to 5V, as are shift, ctrl, break, so we need at least two buffers,
    unless I can use the PCI clamp diode to protect these inputs.
    Clamping to 3.3V means dropping 1.7V over 4371 ohm, or sinking 0.38 mA.
    Need to either pull these all to 3V3, or have an OC output.  74hct125d maybe?
  - The LED outputs are pulled low when active, but are driven by a latch so 5V when inactive.

Hacky / clever idea!
  - Solder a pin header onto PL7
  - Pull the rows low when we have a key pressed and NKBEN (pin 4) is high
  - When NKBEN is low, read column address from PA0-3 (pins 8-11) and set rows accordingly

SUCCESS!!!  I have it starting up thinking I'm pressing 'R' and giving the "CMOS RAM reset" message.

Pro Micro wiring
- Pin 10 - SS - P30
- Pin 16 - MOSI - P29
- Pin 14 - MISO - P28
- Pin 15 - SCK - P27

Tested Pro Micro connection by making it hit BREAK every 1.5 seconds.  That works.

Soldered up PS/2 keyboard socket.  Wiring:
- GND (purple) - 
- 5V (red) - 
- Clock (grey) - pin 3
- Data (white) - pin 2

Doesn't work on the Pro Micro but it *does* work on my Duemilanove, with
clock=3 (PD3/INT1/PCINT19) and data=2 (PD2/INT0/PCINT18).  Overall seems flaky
-- maybe I have a bad keyboard?

Back to trying it with pygame.  That works!  listen_pygame.py.

TO DO
-----

- Get the PS/2 keyboard working
- Provide -5V for the cassette port using a DC/DC converter board
- Test out loading from cassette
- Switch to using blade (spade?) connectors, for a better contact surface.
- Wire up a battery pack, for the RTC and configuration memory.

Ideal BBC Master motherboard support board
------------------------------------------

- Board #1, which sits at the back of the machine
  - Barrel jack for 5V input
  - DC-DC converter for -5V
  - PS/2 jack for keyboard
  - Cable to send PS/2 signals to CPLD board

- Board #2, which plugs into the keyboard socket
  - 3v3 regulator
  - AVR (pro micro?)
  - CPLD
  - Keyboard connector
  - Header to connect to board #1

Homebrew BBC Master keyboard
----------------------------

- PCB mount cherry mx red (soft touch -- not tactile like cherry mx brown) keyswitches
- keycaps: flat for convenience
  - 1.5x: tab, shift(l), shift(r)
  - 2x: return, return(kp)
  - 8x: space
  - 1x: everything else.  red f0-f9, brown up/down/left/right/copy, otherwise black.