@ Copyright 2019 Google LLC
@
@ Licensed under the Apache License, Version 2.0 (the "License");
@ you may not use this file except in compliance with the License.
@ You may obtain a copy of the License at
@
@     http://www.apache.org/licenses/LICENSE-2.0
@
@ Unless required by applicable law or agreed to in writing, software
@ distributed under the License is distributed on an "AS IS" BASIS,
@ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@ See the License for the specific language governing permissions and
@ limitations under the License.


@ Initial startup code, designed to run on a possibly flaky system with bad
@ RAM or malfunctioning chips.  Assume as little as possible.

@ Run from 0x3800000
@ Expect at least 512kB RAM, physically mapped at 0x2000000-0x207ffff

.global _start

_start:
	@ On reset, pc==0, but we want to be at 0x3800000.
	@ Jump to in_rom_now by loading its proper address into pc.
	ldr pc, in_rom_now_addr
in_rom_now_addr: .word in_rom_now

in_rom_now:
	@ Init MEMC
	@ RISC OS 3 writes the following for a 4MB machine:
	@ 036E000C: os mode off, sound off, video off, no refresh, slow roms, 32kB
	@ 036E010C: refresh during flyback, otherwise as above
	@ 036E0D0C: sound on, video on, refresh during flyback
	@ On a 1024K machine:
	@ 036E000C
	@ 036E0104
	@ ... etc
	@ On a 512K machine, RO3 gives an error on boot
	ldr r0, =0x036E050C  @ os mode off, sound off, video on, refresh during flyback, rom slow, 32k pages
	ldr r1, =0
	str r1, [r0]

	@ Set up initial video display

	@ VIDC registers
	ldr r1, =0x03400000  @ VIDCR

	ldr r2, =vidc_reg_table
	ldr r3, =vidc_setup_done
write_to_one_vidc_reg:
	cmp r2, r3
	ldrlo r0, [r2], #4
	strlo r0, [r1]
	blo write_to_one_vidc_reg
	b vidc_setup_done
vidc_reg_table:
	@ Init SFR reg to turn off test mode
	.word 0xC0000100
	@ MODE 13: 640x256, 256 colors (8bpp), 163840 bytes
	.word 0x807FC000  @ reg 80 = 0x7FC000 - horizontal cycle
	.word 0x8408C000  @ reg 84 = 0x08C000 - horizontal sync width
	.word 0x8810C000  @ reg 88 = 0x10C000 - horizontal border start
	.word 0x8C1B4000  @ reg 8C = 0x1B4000 - horizontal display start
	.word 0x906B4000  @ reg 90 = 0x6B4000 - horizontal display end
	.word 0x9476C000  @ reg 94 = 0x76C000 - horizontal border end
	.word 0x9C400000  @ reg 9C = 0x400000 - horizontal interlace
	.word 0xA04DC000  @ reg A0 = 0x4DC000 - vertical cycle
	.word 0xA4008000  @ reg A4 = 0x008000 - vertical sync width
	.word 0xA8048000  @ reg A8 = 0x048000 - vertical border start
	.word 0xAC08C000  @ reg AC = 0x08C000 - vertical display start
	.word 0xB048C000  @ reg B0 = 0x48C000 - vertical display end
	.word 0xB44D0000  @ reg B4 = 0x4D0000 - vertical border end
	.word 0xE00000AE  @ reg E0 = 0x0000AE - control
	.word 0xB8000000  @ reg B8 = 0x000000 - vertical cursor start
	.word 0xBC000000  @ reg BC = 0x000000 - vertical cursor end
	@ Palette
	.word 0x00000000
	.word 0x04000111
	.word 0x08000222
	.word 0x0C000333
	.word 0x10000004
	.word 0x14000115
	.word 0x18000226
	.word 0x1C000337
	.word 0x20000400
	.word 0x24000511
	.word 0x28000622
	.word 0x2C000733
	.word 0x30000404
	.word 0x34000515
	.word 0x38000626
	.word 0x3C000737
	@ White screen border
	.word 0x40000FFF
vidc_setup_done:

	@ Set up video DMA registers in MEMC.  These refer to physical memory and
	@ are limited to the bottom 512kB of memory.  RISC OS sets vstart=0 and
	@ maps these to the top of the 32MB logical memory space.
	@ Set vstart=0
	ldr r0, =0x03600000
	str r1, [r0]
	@ Set vinit=0
	ldr r0, =0x03620000
	str r1, [r0]
	@ Set vend=163840/16 = 10240
	ldr r0, =0x0364a000
	str r1, [r0]

	@ TODO test system memory

	@ memory tested!
	@ now we can run ordinary C code :)

	@ create stack, at memory+512kB-4
	mov sp, #0x2080000 @ todo can prob get this from a linker var
	sub sp, sp, #4
	@ not really using the frame pointer, but init it to stack pointer
	mov fp, sp

	@ clear bss section
	mov r0, #0
	ldr r1, =__bss_start__
	ldr r2, =__bss_end__
still_clearing_bss:
	cmp r1, r2
	strlo r0, [r1], #4
	blo still_clearing_bss

	@ copy initial values from rom (_etext) into .data (_data)
	ldr r1, =_etext
	ldr r2, =_data
	ldr r3, =_edata
still_copying_data:
	cmp r2, r3
	ldrlo r0, [r1], #4
	strlo r0, [r2], #4
	blo still_copying_data

	@ done with all the pre-memory stuff -- jump into C for the rest
	b cstartup
