[Stardot thread](https://stardot.org.uk/forums/viewtopic.php?f=30&t=16420)

A bootloader that runs on the Archimedes machine and selects the OS based on
which function keys are pressed.  Also the start of a modern test ROM for 30
year old machines with possibly bad RAM or chips, or tracks that have been
eaten by leaking battery chemicals.

Getting started
---------------

Prerequisites:
- Python (2 or 3 should work)
- protobuf (on macOS: brew install protobuf)

To build, run 'make clean all'.  This will generate switcher.rom, which can be
run on Arculator -- just put it in one of the riscos folders and set rom_set
appropriately.  (For example, if you save it as roms/riscos3/switcher.rom, you
want to have rom_set = 3 in arc.cfg.  Make sure there are no other ROM files
in the same folder.)

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
