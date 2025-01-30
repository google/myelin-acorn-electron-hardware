[Stardot thread](https://stardot.org.uk/forums/viewtopic.php?f=30&t=16420)

A bootloader that runs on the Archimedes machine and selects the OS based on
which function keys are pressed.  Also the start of a modern test ROM for 30
year old machines with possibly bad RAM or chips, or tracks that have been
eaten by leaking battery chemicals.

Getting started
---------------

Prerequisites:
- [GNU Arm Embedded Toolchain](https://developer.arm.com/downloads/-/gnu-rm) (GCC 9 dropped ARM2 support though, so you need 9-2019-q3-update)
- Python 3
- protobuf (on macOS: brew install protobuf)

On macOS: `brew install protobuf python`, and to de-quarantine the toolchain, `find /opt/gcc-arm-none-eabi-8-2019-q3-update/ -type f -perm +111 -exec xattr -d com.apple.quarantine {} \;`

To build, run 'make clean all'.  This will generate switcher.rom, which can be
run on Arculator -- just put it in one of the riscos folders and set rom_set
appropriately.  (For example, if you save it as roms/riscos3/switcher.rom, you
want to have rom_set = 3 in arc.cfg.  Make sure there are no other ROM files
in the same folder.)

ROM structure
-------------

The ROM is designed to run on both Archimedes (26-bit ARMv2, MEMC) and Risc PC
(32-bit IOMD) machines.  The Archimedes code is "freestanding", handling all
IO etc itself, whereas the Risc PC code runs under a stripped-down RISC OS
build and uses RISC OS SWI commands for its UI, to access the NVRAM, etc.  To
make all this work, a number of images are concatenated to make the actual
ROM:

- 336k: RISC OS build, with modifications:
  - CPU test on startup, jumping to Archimedes bootloader if ARMv2 detected
  - No 3 second wait for special keys on boot
  - Instead of running the configured language module, run RPC bootloader
- 4 bytes: offset of RPC bootloader
- 4 bytes: offset of Arc bootloader
- Arc bootloader
- RPC bootloader

The Arc bootloader is almost but not quite position-independent code, so it's
built with a start address of 0x3854008 (Arc ROM area + 336k + 8 bytes), which
will need to be changed if the RISC OS image ever changes size.  The RPC
bootloader is copied to RAM by the final boot step in the RISC OS build, so
it's built with a start address of 0x8000.

Notes about bare metal programming for the Archimedes
-----------------------------------------------------

The initial entrypoint is \_start in start.s, which calls cstartup() in
cstartup.cc, which calls main_program() in main.cc.

The intention here is to compile everything with the latest arm-none-eabi-gcc,
rather than the ROOL DDE or GCCSDK.  It seems to be going OK so far; here are
some issues I've encountered:

- Needed to compile with -nostdlib, to avoid clashing with GCC's
  expectations for main() etc.

- Needed to compile with -fno-exceptions, otherwise the linker
  complains that it can't find \__aeabi_unwind_cpp_pr0.

- Needed to compile with -mno-thumb-interwork, otherwise the compiler
  generates "bx lr" instructions, which aren't in ARMv2.
