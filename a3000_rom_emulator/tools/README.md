# Arcflash tools

This folder contains example ROM build scripts for Arcflash.

First install the Python library:

~~~
(cd ../python_lib; python3 -m pip install --user -e .)
~~~

Now you can build a ROM and save it:

~~~
python3 make_arc_rom.py save myrom.bin
~~~

Or build and upload it to the Arcflash in one go:

~~~
python3 make_arc_rom.py upload
~~~

> (2021-01-19) Note that on macOS, with the first v3 Arcflash board to be built, with the latest bootloader and firmware, this seems to hang after uploading a few megabytes.  Unplugging and replugging the USB cable and rerunning should get it a bit further, and eventually you should get a "Done" message.  I can't reproduce this on Linux, and haven't tried on Windows yet.  `test_serial_comms.py` is a tester for this that forces the worst-case scenario (16MB of entirely new data) to debug this.
