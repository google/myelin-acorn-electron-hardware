This repository contains various hardware expansions I've designed for
the Acorn Electron, a computer that was very popular in the UK in the
80s, and was the first computer I ever used, from 1985 onward.

Background: https://www.theregister.co.uk/2013/08/23/acorn_electron_history_at_30/

Designed by Phillip Pearson <philpearson@google.com>

This is not an official Google product.

- standalone_cartridge_programmer: USB Acorn Electron cartridge
  interface, allowing read/write access to cartridges without an
  actual Electron / Plus 1.

- elk_pi_tube_direct: Acorn Electron cartridge using a CPLD to provide
  address decoding and level shifting for a Raspberry Pi running
  PiTubeDirect.

Coming soon:

- 32kb_flash_cartridge: Simple Acorn Electron cartridge with two 16kB
  flash banks.

- dual_ported_ram: Acorn Electron cartridge using a CPLD and a 128kB
  SRAM chip to implement dual ported RAM that can be read or written
  by both the Electron and a USB-attached computer.
