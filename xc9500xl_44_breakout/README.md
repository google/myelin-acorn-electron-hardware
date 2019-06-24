Simple breakout board for an XC9536XL-10VQG44 or XC9572XL-10VQG44 CPLD.

See ../notes/pld_programming_and_jtag.md for programming tips.  This board
uses the Altera JTAG pinout, so be careful wiring up a Xilinx Platform Cable.

The cpld_template folder contains a sample "quick start" project, with all the
pins already specified.  Copy this folder and edit xc9500.v.  Edit Makefile
and change the part type if you are not using an XC9536XL, and edit xc9500.prj
and change "verilog work xc9500.v" to "vhdl work xc9500.vhd" if you prefer
VHDL.

## Errata

v1 has 5V and 0V marked the wrong way around on the power pins at the top of
the board.
