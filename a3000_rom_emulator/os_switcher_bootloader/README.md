The start of a bootloader that runs on the Archimedes machine and selects the
OS based on which function keys are pressed.

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
