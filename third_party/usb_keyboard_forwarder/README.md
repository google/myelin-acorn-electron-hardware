USB Keyboard Forwarder
======================

Firmware for an ATSAMD21E18A that acts as a USB Host, expecting a keyboard
supporting the HID boot protocol to be connected.  It outputs debug information
to a serial port (TX=PA10, RX=PA11).

I intend to add SPI transmission, similar to
[emu_keyboard_mcu](../../emulated_keyboard/emu_keyboard_mcu), so this can be
wired up to the [emulated_keyboard](../../emulated_keyboard/) hardware, allowing
me to connect a USB keyboard to my BBC Master motherboard.  Eventually I'll make
a single PCB that does all of this.

Building and installing
-----------------------

- Install the latest Arduino IDE, and the "MattairTech SAM M0+ Boards"
  package (see the "SAM M0+ Core Installation" section in the [MT-D21E rev B user
  guide](https://www.mattairtech.com/docs/MT-D21E/MT-D21E_revB_User_Guide.pdf).
- At the command line, run "make build".
- If you have a J-Link, at the command line, run "make program".  Otherwise
  program the board with your favourite SWD programmer.

third_party note
----------------

This is in the `third_party` folder because it is derived from external work,
and to clarify that it is covered by a mixed set of licenses, and may have more
distribution requirements than other folders in the repository.

PPKeyboard is derived from KeyboardController.{cpp, h} by Arduino, released
under the LGPLv2.1, and it depends on hidboot.{cpp, h} by Circuits At Home, LTD,
released under the GPLv2 license.  Changes added in this project are released
under Apache 2.0 license.
