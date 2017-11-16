Programming UPURS and MMFS into the flash
=========================================

_Part of [Starting out with a new BBC Model B](README.md)._

At this point, you should have a BBC B with a 39SF010 flash chip and a 62256 RAM
chip installed into two of the ROM sockets, with wires going all over the place
and soldered onto various IC pins around the place.  Turning the machine on, you
should see "BBC Computer 32K" and "BASIC", and maybe something else like "Acorn
DFS" if you have another ROM installed.

The trick at this point is to get the data for any ROM image you want to flash
into your 39SF010 chip onto the machine.  I use a cassette cable (3.5mm to DIN;
search on eBay for Bang & Olufsen 3.5mm DIN cable to get one) and a Python
script that generates .wav files that can be played from a laptop and loaded on
the BBC through the cassette interface.

First make sure you're in tape mode (`*TAPE`) and have PAGE set properly
(`PAGE=&E00`).

Now probe your flash and RAM banks to make sure they're working properly.  On
the BBC, run `*RUN`, and on the host machine, `make -C flasher probe`.  You
should see some RAM banks and some flash banks.  If you don't, double check your
wiring and soldering.

If that looks good, you're ready to transfer the ROM image.  On your BBC, run:
`*LOAD`, and on your host machine, run
[file_to_wav.py](../third_party/uef-utils/file_to_wav.py) to generate and play
an audio stream of the ROM image, that the BBC can understand:

`python ../third_party/uef-utils/file_to_wav.py mmfs.rom 2000`

This assumes you're converting an MMFS ROM image from the current folder. Change
the filename as required.  This will convert the file, and attempt to play it in
iTunes if you're on a Mac.  On any other machine it'll probably give an error at
the end instead, but just play the .wav file with your favourite audio player.

Once the ROM image is loaded at &2000, you can run the flasher tool, to actually
flash it into the chip.  On the BBC, run `*RUN`, and on the host machine, `make
-C flasher program BANK=E` (assuming you want to program bank 0E; change as
necessary).

On my BBC, I have DFS 1.20 in bank 2, UPURS50R in bank 6, MMFS in bank A, and
bank E is empty.

_TODO figure out how to unplug/insert roms on a BBC B.  My current arrangement
results in PAGE=&1B00, which is not ideal.  Also ZMMFS should give me PAGE=&E00._
