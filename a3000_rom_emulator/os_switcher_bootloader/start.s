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
	@ Jump to 0x3800008, which should hopefully be in_rom_now, below.
	@ TODO figure out a safer way of doing this.  Is there a non
	@ PC-relative way to put an address in a register?
	mov r0, #0x3800000
	add pc, r0, #8

in_rom_now:
	@ TODO set screen border color

	@ TODO test system memory

	@ create stack, at memory+512kB-4
	mov sp, #0x2080000
	sub sp, sp, #4
	@ not really using the frame pointer, but init it to stack pointer
	mov fp, sp

	@ TODO copy data

	@ TODO zero out bss

	@ done with all the pre-memory stuff -- jump into C for the rest
	b cstart
