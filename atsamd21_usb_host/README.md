atsamd21_usb_host
==================

Simple board consisting of an Atmel ATSAMD21 chip, a USB-A socket (for USB host
operation), a micro USB socket (for USB device operation), a voltage regulator,
and an SWD header.

The ATSAMD21 is a cheap ($1-2) microcontroller that can act as a USB host, which
I plan to use to connect USB keyboards to my currently-keyboardless Master 128
and Beeb motherboards.

r1: Sent to oshpark.com for fabrication 2017-11-06.  Assembled and
tested; appears to work.  Functions fine as a USB CDC device.  USB
host not tested yet.

![PCB front](pcb/pcb-front.png)

![PCB back](pcb/pcb-back.png)
