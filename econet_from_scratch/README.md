Econet from scratch
===================

Can we implement an Econet interface from scratch, without having to use a BBC
Master Econet module or MC68B54 chip?

This is a partial design, with an unfinished and very unproven PCB.

![PCB front](pcb/pcb-front.png)

![PCB back](pcb/pcb-back.png)

Econet wire protocol
--------------------

The Econet wire protocol is fairly simple.  A frame begins with the sequence
01111110, followed by the payload, two CRC bytes, and 01111110.  The MC6845
datasheet specifies a standard format for the payload, but it appears that this
is optional, as Econet frames don't appear to follow the rules.

It shouldn't be too hard to convert this into an asynchronous serial interface
running at a higher frequency, which a sufficiently fast microcontroller should
be able to drive safely.

The maximum clock rate for compatibility with 6502 systems is 250 kHz,
resulting in 31250 bytes per second, or one every 32 us.  Archimedes systems
can handle up to 660 kHz, or one byte every 12 us.  A CPLD could easily
convert this into an asynchronous serial stream, or feed it into an SPI-
accessible shift register.

The tiny ATSAMD11 and the very cheap ATSAMD21 both have DMA, so it should be
possible to output arbitrary sized messages without processor involvement,
ideally with the USRT. When using the USRT, the CPLD can drive the XCK pin,
stopping the clock when its buffer is full. Because Econet is a half-duplex
protocol, we should never need to transmit in both directions at once, so an
interface like this should work well:

- Econet transceiver->CPLD: clock (R, D, DE)
- Econet transceiver<->CPLD: data (R, D, DE)
- Econet transceiver->CPLD: collision detect
- MCU->CPLD: 8MHz clock (or similar)
- MCU->CPLD: Econet clock signal (if we want to act as a clock)
- MCU->CPLD: data direction
- CPLD->MCU: XCK (stopped when the CPLD's buffers are full)
- MCU->CPLD: TXD (data to transmit to Econet)
- CPLD->MCU: RXD (data received from Econet)

As long as XCK runs faster than the Econet clock, there will never be a buffer
overrun or underrun anywhere.

Alternative transceiver chip
----------------------------

The SN65C1168/SN75C1168 is cheap and can handle both the data and clock lines.
(Not to be confused with the SN65/75C1167, which ties the driver enable line for
both outputs together, and won't work for Econet).  The SN65- parts have a wider
temperature range but are otherwise identical to the SN75- parts.

I'm using the SN65C1168NS (SOIC) for convenience ($1.61 from Digikey).

Collision detection
-------------------

There's a standard BBC circuit for collision detection, used on the
Model B and on the Master Econet module; it works by finding the
average of the D+ and D- lines, adding about 0.125V, and signalling a
collision if neither line is above the average.  In a collision
situation, two drivers on different stations are fighting each other,
which probably results in D+ and D- both being pulled down near 0V, as
the high side of the SN95159 output has a 9 ohm series resistor.

It's possible that this isn't necessary, because the CPLD can just
compare what comes back from the receive side and flag a collision if
it doesn't match what's being transmitted.  I'm putting the standard
collision-detect circuit on the board, just in case.

BBC Master interface
--------------------

The Econet module has a 17-pin interface (PL1) to the host machine (SK5):

- 1 /NETINT
- 2 RnW
- 3 /ADLC
- 4 PHI2
- 5 A0
- 6 A1
- 7 D0
- 8 D1
- 9 D2
- 10 D3
- 11 D4
- 12 D5
- 13 D6
- 14 D7
- 15 /RST
- 16 0V
- 17 5V

Two extra pins, A and B, bring out A2 and A3 respectively, although are not
present on the Econet module board.

There are 15 data pins: 7 are inputs to the module, and 8 are bidirectional,
so two 74LVC245 chips or one XC9536XL CPLD would handle the level shifting.

Physically, the module measures 94x58mm, with 44mm
between the vertical centre of PL2 (which connects to the Econet socket) and PL1
(which connects to the bus).  PL2 starts 9.5mm from the right edge of the board,
and PL1 starts 4.5mm in.  PL2 pin 5 is vertically in line with PL1 pin 15.

PL1's 17 pins cover 40.5mm, so they appear to be spaced at 0.1".

The MC68B54 has four 8-bit control registers, two status registers, and two
3-byte FIFOs, for a total of 96 bits of RAM, plus probably a few shift
registers.  This suggests that with an LCMXO256 chip (with 2048 bits of RAM) we
could possibly expand the FIFOs a bit.

Alternatively this might work with a small but fast MCU like the ATSAMD11C; one
or two USRTs running at 24 MHz would allow queuing to happen in the MCU's RAM
rather than the CPLD.

BBC B interface
---------------

Would it be possible to hook up to the BBC B as well?  All the pins from PL1 on
the module go to the ADLC (68B54) chip.  The Econet data pins connect to pins
12/13 on IC93 (SN75159), and the clock pins connect to R38 and R39.  Fitting 0R
links in R38 and R39 would bring the clock signals to pins 9/10 on IC94 (LM319).
So it would be fairly feasible to create an adapter to fit an Econet module to a
BBC B.
