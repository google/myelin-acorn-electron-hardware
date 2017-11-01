myelin-acorn-electron-hardware
==============================

The Acorn Electron is a British computer that was very popular in the UK and New
Zealand in the 80s, and was the first computer I ever used, in 1985.  I acquired
one on eBay in 2016, and started hacking on hardware expansions for it a little
later.  In the meantime I've also acquired a BBC Model B, and some BBC Master
128 motherboards.  This repository contains various hardware expansions I've
designed for the three machines.

Background: https://www.theregister.co.uk/2013/08/23/acorn_electron_history_at_30/

Designed by Phillip Pearson (philpearson@google.com)

This is not an official Google product.

Acorn Electron projects
-----------------------

- [standalone_cartridge_programmer](standalone_cartridge_programmer/):
  USB Acorn Electron cartridge interface, allowing read/write access
  to cartridges without an actual Electron / Plus 1.  (Built,
  verified.)

- [elk_pi_tube_direct](elk_pi_tube_direct/): Acorn Electron cartridge
  using a CPLD to provide address decoding and level shifting for a
  Raspberry Pi running PiTubeDirect.  (Built, verified.)

- [expansion_minispartan_breakout](expansion_minispartan_breakout/):
  Breakout board for the Electron's rear expansion connector, with
  buffers and footprint to attach a Scarab miniSpartan6+ LX25 board.
  (Built, verified.)

- [minus_one](minus_one/): Acorn Electron expansion that provides
  three Plus 1 workalike cartridge slots.  (Built, verified.)

- [32kb_flash_cartridge](32kb_flash_cartridge/): Simple Acorn Electron
  cartridge with two 16kB flash banks.  (Built, verified standard PCB.
  Mini PCB built but had a PCB error.)

- [cpu_socket_expansion](cpu_socket_expansion/): Mezzanine board that attaches
  to the CPU socket of a BBC and translates between 5V TTL and 3.3V CMOS levels.
  (Untested.)

- [cpu_socket_minispartan_daughterboard](cpu_socket_minispartan_daughterboard/):
  Attaches to a cpu_socket_expansion board and connects a miniSpartan6+ FPGA
  board and a Raspberry Pi Zero running PiTubeDirect.  (Untested.)

- [spi_sd_card](spi_sd_card/): Experimental implementation of the interface
  used by MMFS to access SD cards, for the CPLD on an elk_pi_tube_direct board.
  (Code only.)

BBC Model B projects
--------------------

- [upurs_usb_port](upurs_usb_port/): Code to run on an ATMEGA32U4 to
  use it as a USB to serial adapter for UPURS.  (Flaky.)

- [serial_sd_adapter](serial_sd_adapter/): VHDL that runs on an
  elk_pi_tube_direct board and provides a fast serial port and SD card
  interface.  Also, a board that attaches to a BBC using the 1MHz Bus and
  provides the same interfaces.  (Untested.)

BBC Master 128 projects
-----------------------

- [master_updateable_megarom](master_updateable_megarom/): BBC Master 128 MOS
  ROM replacement that can be reprogrammed while in the machine.  (Untested.)

- [emulated_keyboard](emulated_keyboard/): Code and VHDL to allow an attached
  computer to act as a keyboard for a BBC Master 128.  (Code only, verified.)

- [bbc_master_bringup](bbc_master_bringup/): Notes on getting a BBC Master 128
  motherboard to run without a keyboard or standard power supply.

Miscellaneous things that happened along the way
------------------------------------------------

- [atsamd11_pro_micro](atsamd11_pro_micro/): Tester board to experiment with
  USB on the Atmel ATSAMD11C14 chip.  (Untested.)

- [cherry_mx_keyswitch_tester](cherry_mx_keyswitch_tester/): Tester board to
  verify my Cherry MX keyswitch footprint before I order anything expensive.
  (Untested.)

Future project ideas
--------------------

- dual_ported_ram: Acorn Electron cartridge using a CPLD and a 128kB
  SRAM chip to implement dual ported RAM that can be read or written
  by both the Electron and a USB-attached computer.  (Working on the
  PCB layout.)

- expansion_debugger: Pro Micro, CPLD, and edge connector that can be
  connected to a Plus 1 or other Electron expansion for testing.
  (Just an idea so far.)

Installation notes
------------------

I use my own Python scripts for generating netlists, rather than entering
schematics through Kicad's eeschema package.  If you change the .py file in
any of the 'pcb' folders, running 'make' (or 'make net') should rebuild the
netlist.

The Makefile will also plot gerbers once a .kicad_pcb file has been created.
This requires some messing around on macOS -- you have to copy the system
Python executable into the pcbnew folder.

Generating the previews linked from the README.md files requires pcb-tools,
which you can install using 'python setup.py install' in the third_party/pcb-
tools folder (after running git submodule update --init).  On macOS, first
install its dependencies with 'brew install cairo pango'.
