spi_sd_card
===========

This folder contains VHDL for an experimental SD card interface, that
implements the simple parallel port interface used by MMC_ElkPlus1.asm
in [MMFS](https://github.com/hoglet67/MMFS/).

It also contains an experimental version of the memory-mapped SPI port
as seen in MMC_MemoryMapped.asm, except at &FCD0 rather than &FE18,
but this isn't working yet.

Hardware-wise, right now it's an elk_pi_tube_direct cartridge with an
SD socket taped to the top, and jumper wires everywhere.  It draws
power from the minus_one's 3.3V pin.

Connections (with wire colours for my convenience):

- tube_D<5> - blue, nSS
- tube_D<6> - green, MOSI
- tube_D<7> - yellow, SCK
- tube_D<0> - orange, MISO

On SD card:

- 9 (notch) - DAT2
- 1 - DAT3/nSS (blue)
- 2 - CMD/MOSI (green)
- 3 - GND
- 4 - 3.3V
- 5 - CLK/SCK (yellow)
- 6 - GND
- 7 - DAT0/MISO (orange)
- 8 - DAT1

[Discussion on the Stardot forums](http://www.stardot.org.uk/forums/viewtopic.php?f=3&t=12737&start=30#p170599).

![Photo of the hardware](elk_pi_tube_direct_sd_mmfs_600px.jpeg)
