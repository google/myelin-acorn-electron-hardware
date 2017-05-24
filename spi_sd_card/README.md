spi_sd_card
===========

This folder contains VHDL for an experimental SD card interface, that
implements the simple parallel port interface used by MMC_ElkPlus1.asm
in [MMFS](https://github.com/hoglet67/MMFS/).

The original plan was to implement the memory-mapped SPI port as seen
in MMC_MemoryMapped.asm, except at &FCD0 rather than &FE18, but this
was easier :)

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
