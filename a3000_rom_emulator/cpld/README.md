# CPLD RTL

Build this using Xilinx ISE 14.7.  I have it installed on Linux, where you can just run: `make local`

There's no external JTAG connector; you have to program it into the CPLD on an Arcflash via the MCU: `make program`