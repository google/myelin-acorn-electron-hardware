An adapter board to make it easy to monitor your Electron, BBC Micro, or BBC
Master's bus using a cheap logic analyzer.

In development, untested.

[Discussion on the Stardot forums](http://stardot.org.uk/forums/viewtopic.php?f=3&t=13882&p=186574#p186574)

![PCB front](pcb/pcb-front.png)

![PCB back](pcb/pcb-back.png)

Planning
--------

This was originally just going to be a quick adapter board to allow attaching an
lctech Cypress EZ-USB FX2 board to an Electron cartridge port or a BBC Tube
port.  The clock instability on the Electron forced the addition of the CPLD, at
which point it would have been a waste not to also put in level shifting for
PiTubeDirect.

All the signals to the logic analyzer except nNMI, nIRQ, READY, and SYNC are
provided to the Pi.  The Tube socket includes nIRQ, but nNMI and READY have to
come out from the cartridge port, and SYNC is a flying lead on all machines.

It's probably easiest to move the Tube socket over by the cartridge pins, then
have the CPLD above it, then the Pi, and finally the logic analyzer.

Pins that have to go from the cartridge port to the CPLD but aren't on the Tube
port: A7, /INFC, 16MHz.  Pins that have to go to the logic analyzer but not CPLD
or Tube: /NMI, READY.

We need 35 CPLD pins to do this properly.  elk_pi_tube_direct only needs 34, but
we need the 16 MHz clock here.  Hoglet suggests using a Schottky diode and
pullup to convert nRESET, which I think is the easiest solution.  Another option
would be to use a 64-pin CPLD, but those are harder to solder (although would
allow a few more signals, if we think of anything there).
