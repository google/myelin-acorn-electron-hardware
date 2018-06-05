This folder contains some experimental code to work with various disk formats.

TODO: Write ADFS read/write routines in C, to run on an AVR connected
to an Elk/Beeb.  Either with an MMC directly formatted as ADFS, or
(ideally) FAT containing ADFS/DFS/UEF images.

Ideally tape + DFS routines also, we we can use UPCFS and HostFS:UPURS
to give E00 tape/DFS/ADFS on both Beeb/Elk without extra memory.  AND
the ability to access the SD card over the USB serial link from a host
PC, without removing the SD card.

ATMEGA32U4 only gives us 2.5kB of RAM, but that might be enough here.
