# Arcflash CPLD RTL

This is the RTL for the Xilinx XC95144XL CPLD on the Arcflash board.

Build this using Xilinx ISE 14.7.  This is a discontinued product, but you can still download it.  I don't recommend using the Windows 10 version (which is a Linux VM running an old version of Oracle Linux).  If you're on Windows, use WSL2 and Ubuntu and install the Linux version instead.  To install the Linux version, google `xilinx ise 14.7 download` and download the *Full Installer for Linux* or the *Full DVD Single File Download Image*, untar somewhere, and run `./xsetup`.  If you get an error about `libncurses.so.5`, at least on Ubuntu Noble you can just `cd /usr/lib/x86_64-linux-gnu && ln -s libncurses.so.6 libncurses.so.5`, and the graphical installer will start up fine.

To build the `.svf` image: `make local`

Arcflash has no external JTAG connector; program the CPLD via the MCU: `make program`

To run the testbenches (the old Verilog one and the new Python/cocotb one), install Icarus Verilog and `cocotb`, and run: `make test2`

I run builds under Linux but test on macOS, so this means `brew install icarus-verilog gtkwave python3; python3 -m venv ~/ve; source ~/ve/bin/activate; pip3 install cocotb pytest; make test2`
