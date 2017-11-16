; Actually program something into the flash
PROGRAM_ROM = 1

; Read bank ID from here (written by Makefile)
INCLUDE "bank_to_program.inc"

INCLUDE "common.asm"
SAVE "flash_rom.bin", entry_point, end_of_code
