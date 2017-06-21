myelin-acorn-electron-hardware
==============================

This repository contains various hardware expansions I've designed for
the Acorn Electron, a computer that was very popular in the UK in the
80s, and was the first computer I ever used, from 1985 onward.

Background: https://www.theregister.co.uk/2013/08/23/acorn_electron_history_at_30/

Designed by Phillip Pearson (philpearson@google.com)

This is not an official Google product.

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
  (Built, untested.)

- [minus_one](minus_one/): Acorn Electron expansion that provides
  three Plus 1 workalike cartridge slots.  (Built, verified.)

- [32kb_flash_cartridge](32kb_flash_cartridge/): Simple Acorn Electron
  cartridge with two 16kB flash banks.  (Built, verified standard PCB.
  Mini PCB built but had a PCB error.)

- [upurs_usb_port](upurs_usb_port/): Code to run on an ATMEGA32U4 to
  use it as a USB to serial adapter for UPURS.

Coming soon:

- dual_ported_ram: Acorn Electron cartridge using a CPLD and a 128kB
  SRAM chip to implement dual ported RAM that can be read or written
  by both the Electron and a USB-attached computer.  (Working on the
  PCB layout.)

- expansion_debugger: Pro Micro, CPLD, and edge connector that can be
  connected to a Plus 1 or other Electron expansion for testing.
  (Just an idea so far.)
