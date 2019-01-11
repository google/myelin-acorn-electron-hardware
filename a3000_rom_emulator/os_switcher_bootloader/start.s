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
	@ TODO set screen border color

	@ TODO test system memory

	@ create stack, at memory+512kB-4
	mov sp, #0x2080000
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
