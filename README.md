myelin-acorn-electron-hardware
==============================

The [Acorn Electron](https://en.wikipedia.org/wiki/Acorn_Electron) is a British computer that was very popular in the UK and New
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

Cross-platform projects
-----------------------

- [cpu_socket_expansion](cpu_socket_expansion/): Mezzanine board that attaches
  to the CPU socket of a BBC or Electron and translates between 5V TTL and 3.3V
  CMOS levels. (Built, tested.)

- [cpu_socket_minispartan_daughterboard](cpu_socket_minispartan_daughterboard/):
  Attaches to a cpu_socket_expansion board and connects a miniSpartan6+ FPGA
  board and a Raspberry Pi Zero running PiTubeDirect.  (Built, tested.)

- [spi_sd_card](spi_sd_card/): Experimental implementation of the interface
  used by MMFS to access SD cards, for the CPLD on an elk_pi_tube_direct board.
  (Code only.)

- [fx2_tube_cartridge_adapter](fx2_tube_cartridge_adapter/): Adapter to allow
  connecting an FX2-based logic analyzer board to the BBC Tube interface or
  as an Electron cartridge.  (Partly tested.)

- [bbc_power_distribution](bbc_power_distribution/): Small board to
  make it easy to power a Model B or Master motherboard from a 5V
  power supply with a barrel jack or Micro USB output.  Uses an
  LTC1983 to generate -5V, so you don't need to provide it externally.

BBC Model B projects
--------------------

- [new_bbc_bringup](new_bbc_bringup/): Notes on modernizing a BBC Model B,
  with flash and sideways RAM, and an emulated disk interface.

- [upurs_usb_port](upurs_usb_port/): Code to run on an ATMEGA32U4 to
  use it as a USB to serial adapter for UPURS.  (Flaky.)

- [serial_sd_adapter](serial_sd_adapter/): VHDL that runs on an
  elk_pi_tube_direct board and provides a fast serial port and SD card
  interface.  Also, a board that attaches to a BBC using the 1MHz Bus and
  provides the same interfaces.  (Built, tested serial port.  SD card interface
  untested.)

- [econet_from_scratch](econet_from_scratch/): USB Econet interface.
  (Untested.)

- [econet_hub](econet_hub/): Clock and bias circuit, with five Econet sockets,
  to connect a simple network together.  (Untested.)

BBC Master 128 projects
-----------------------

- [master_updateable_megarom](master_updateable_megarom/): BBC Master 128 MOS
  ROM replacement that can be reprogrammed while in the machine.  (Untested.)

- [emulated_keyboard](emulated_keyboard/): Code and VHDL to allow an attached
  computer to act as a keyboard for a BBC Master 128.  (Code only, verified.)

- [new_master_bringup](new_master_bringup/): Notes on getting a BBC Master 128
  motherboard to run without a keyboard or standard power supply.

Miscellaneous things that happened along the way
------------------------------------------------

- [atsamd11_pro_micro](atsamd11_pro_micro/): Tester board to experiment with
  USB on the Atmel ATSAMD11C14 chip.  (Untested.)

- [atsamd21_usb_host](atsamd21_usb_host/): Tester board to experiment with
  USB hosting on the Atmel ATSAMD21E18A chip.  (Untested.)

- [cherry_mx_keyswitch_tester](cherry_mx_keyswitch_tester/): Tester board to
  verify my Cherry MX keyswitch footprint before I order anything expensive.
  (Built, verified.)

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
any of the `pcb` folders, running 'make' (or 'make net') should rebuild the
netlist.

The Makefile will also plot gerbers once a .kicad_pcb file has been created.
This requires some messing around on macOS -- you have to copy the system
Python executable into the pcbnew folder.

Generating the previews linked from the `README.md` files requires pcb-tools,
which you can install using `python setup.py install` in the `third_party/pcb-tools` folder (after running `git submodule update --init`).  On macOS, first
install its dependencies with `brew install cairo pango`.
