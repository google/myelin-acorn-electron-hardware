Starting out with a new BBC Model B
===================================

In the 80s, when your shiny new Beeb arrived, you'd run software off tape
cassette -- or floppy disk if you were lucky enough to have a model with the
disk interface and DFS ROM fitted.  Nowadays, unless you're going for a fully
authentic retro experience, neither of these options is particularly appealing.
Ideally, you want something like a hard disk and a network connection.

IMHO the best options in 2017 are MMFS and UPURS.  MMFS provides a hard disk /
multi disk changer type interface via files on an SD card, and UPURS provides
various connectivity options to an attached computer.  Both connect via the
Beeb's User Port.

Getting either of these running requires a bit of bootstrapping.  They both run
out of ROM, and I don't have any traditional EPROM chips or a programmer for
them, so I'm modifying a Microchip SST39SF010A 128kB flash chip and soldering
some extra wires onto the computer's main board to simulate multiple ROM chips.

This document is getting kinda long, so I'm breaking it up into multiple sections; follow the links below:

- ## [Using flash and RAM in the BBC's ROM sockets](bbc_flash_and_ram.md)
- ## [Programming UPURS and MMFS into the flash](programming_flash.md)
- ## (TODO) Using sideways RAM
