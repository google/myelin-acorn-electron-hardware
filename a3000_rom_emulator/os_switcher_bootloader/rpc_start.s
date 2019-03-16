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


@ Risc PC bootloader (rpc_boot) startup code.  Pretty trivial because
@ everything will run from RAM (origin 0x8000), and RISC OS has already
@ booted, so no initialization is necessary.

.equ XOS_WriteS, 0x20001
.equ OS_WriteS,  0x1

.global _start

_start:
    swi OS_WriteS
    .asciz "rpc_start: Arcflash Risc PC bootloader starting\r\n"
    .align

    @ Enter user mode or SWIs will clobber R14
    msr cpsr_c, #0x10

    @ Disable Escape key
    mov r0, #200  @ OS_Byte 200
    mov r1, #1    @ EOR 1
    mov r2, #0    @ AND 0
    swi 6         @ OS_Byte

    @ And get started!
    swi OS_WriteS
    .asciz "rpc_start: Copying bootloader to RAM\r\n"
    .align

    @ TODO do we need to create the stack, or has RISC OS already done it for us?
    @ create stack
    ldr sp, =__stack_end @ todo can prob get this from a linker var
    @ not sure if we need sp to point to free space, but just in case...
    sub sp, sp, #4
    @ not really using the frame pointer, but init it to stack pointer
    mov fp, sp

    @ copy everything to 0x8000 from wherever we are right now
    adr r1, _start   @ source address, PC-relative
    ldr r2, =_text   @ dest address
    ldr r3, =_edata  @ where to stop
still_copying_data:
    cmp r2, r3
    ldrlo r0, [r1], #4  @ read from ROM
    strlo r0, [r2], #4  @ write to RAM
    blo still_copying_data

    @ clear bss section
    mov r0, #0
    ldr r1, =__bss_start__
    ldr r2, =__bss_end__
still_clearing_bss:
    cmp r1, r2
    strlo r0, [r1], #4
    blo still_clearing_bss

    swi OS_WriteS
    .asciz "rpc_start: Jumping to C code\r\n"
    .align

    @ and we are now ready to jump into C!
    ldr pc, cstartup_addr  @ load absolute address to make sure we end up in RAM
cstartup_addr: .word cstartup
