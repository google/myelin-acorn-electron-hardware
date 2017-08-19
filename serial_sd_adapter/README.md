serial_sd_adapter
=================

This is something I'm working on to provide a fast serial port with
reliable flow control for a BBC or Electron.  On the BBC, it'll attach
to the 1MHz bus, and on the Electron, it'll be a cartridge.

In either case it consists of:

- a CPLD to communicate with the host machine's bus and share the SD
  card between the host machine and the Pro Micro.

- a Pro Micro to provide a USB serial port, and act as a
  [HostFS](http://mdfs.net/Software/Tube/Serial/) server.

At present, it works well with a hacked-up version of J.G.Harston's
HostFS, running against sweh's TubeHost code on an attached laptop.
This provides quite a quick filing system that leaves PAGE=&E00, as
all the buffers are in the host machine's memory.

- [In-progress PCB for the BBC version](bbc_1mhz_bus_pcb/)

[Discussion on the Stardot forums](http://stardot.org.uk/forums/viewtopic.php?f=3&t=13292).
