emulated_keyboard
=================

This uses pygame, a Pro Micro, and a CPLD to allow you to use your computer as a
keyboard for a BBC Master 128.

See: http://www.stardot.org.uk/forums/viewtopic.php?f=3&t=13804

Usage
-----

- Program an XC9572XL with the code in cpld/
- Program a Pro Micro with the code in emu_keyboard_mcu/
- Run listen_pygame.py on your computer (only tested on a MacBook Pro, so YMMV with anything else)

Wiring
------

- The CPLD needs to be connected to PL11, PL24, and PL7 on the Master 128 motherboard.  PL7 is probably not populated, so you'll have to solder a header in there.  See new_master_bringup/README.md for the pinout, and see cpld/constraints.ucf for how the pins connect to the CPLD.
- The CPLD needs to be connected to the Pro Micro's SPI port.  Pinout in new_master_bringup/README.md.
- The Pro Micro should be connected to your computer's USB port before running listen_pygame.py.
