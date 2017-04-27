This folder contains the PCB design, HDL, and firmware for a board
that allows access to an Acorn Electron cartridge over USB.

I've built one of these boards and implemented the read path, so it
can dump out the contents of a ROM cartridge.  nINFC, nINFD, and
writes are not yet implemented.

[pcb/](pcb/) - PCB design

[cpld/](cpld/) - HDL for the on-board CPLD (use Xilinx ISE and
xc3sprog)

[mcu/](mcu/) - Firmware for the Pro Micro (use the Arduino IDE,
selecting the Arduino Leonardo board option)
