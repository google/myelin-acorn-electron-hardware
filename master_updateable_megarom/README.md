Upgradeable BBC Master MegaROM
==============================

http://myelin.nz/acorn/megarom

A board that replaces IC24, the 1 megabit ROM containing the OS and sideways
banks 9-15 on a Master 128, and allows you to update the contents of the ROM
over USB (via a microcontroller) while the machine is running.

Status: I've built up a PCB with an SST39SF010A (128kB) flash chip,
implemented the CPLD design, and written the AVR firmware.  Flash programming
and readback works with the board running standalone and inside a Master 128.
I think this is ready for others to try out.

- [PCB design](pcb/)
- [Xilinx XC9572-64VQG CPLD design](cpld/)
- [Pro Micro firmware for USB interface](avr_firmware/)

Installation
------------

First test the board outside the Master 128.  Connect a JTAG adapter to the JTAG
port on the top left of the board, which uses the Altera USB Blaster pinout,
with pin 1 on the bottom left.

Wire the SPI port up to an ATMEGA32U4-based Arduino board, like a Leonardo or
Pro Micro.  From left to right: GND, SCK (Arduino pin 15), SS (pin 10), MOSI
(pin 16), MISO (pin 14).

Connect power to the EXTPWR port -- GND on the left, 5V on the right.

Program the CPLD and the ATMEGA32U4, then make a serial connection to the board
and send I<CR>.  It should respond with the size of the flash chip, and "OK".

To program an image into the flash: python program_rom.py <rom file>

To read the current flash image: python read_rom.py

If you can successfully program and read an image (noting that you'll get an
error if your image file isn't the same size as the flash soldered onto the
board), it's time to install it in your Master 128.

First, *DISCONNECT POWER FROM THE EXTPWR PORT*.  Otherwise you'll end up
trying to power your Master 128 via USB, or you may short your USB port's 5V
supply to the Master 128's power supply, which will also be bad.

Now remove your MOS ROM (IC24, on the far right hand side of the motherboard,
just below the Econet module socket), and plug the board in, then turn the
machine on.  It should boot with the image you just programmed into the flash.

If you run program_rom.py or read_rom.py now, you should see screen
corruption, and the machine will probably crash.  This is expected, because
when accessing the flash, the BBC is blocked out, and gets garbage data.
Hitting Ctrl-BREAK (and maybe \*FX 200,2 then BREAK to clear the memory, if
you get a "Bad sum" error) should fix it though.

One way to stop the machine from trying to access the flash while you're
writing to it is to disable interrupts and send the processor into a loop,
like this:

    P%=&1000
    [SEI:.A JMP A
    CALL &1000

![PCB front](pcb/pcb-front.png)

![PCB back](pcb/pcb-back.png)
