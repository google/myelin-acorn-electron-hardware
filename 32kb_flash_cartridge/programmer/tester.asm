; Copyright 2017 Google Inc.
;
; Licensed under the Apache License, Version 2.0 (the "License");
; you may not use this file except in compliance with the License.
; You may obtain a copy of the License at
;
;     http://www.apache.org/licenses/LICENSE-2.0
;
; Unless required by applicable law or agreed to in writing, software
; distributed under the License is distributed on an "AS IS" BASIS,
; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; See the License for the specific language governing permissions and
; limitations under the License.

; flash cartridge test code

; TO DO
	; PCBv2: hardware write protect jumper option

; programming limits
; PAGE=E00
; HIMEM=1100 because i've *RUN something which loads in there
; mode 6 screen start = 6000
; 6000-1000 = 5000h
; hopper is 283A long
; we can load a 16k rom at $2000 and have it fit between us and screen memory!

; zero page addresses
zp_lo := $90
zp_hi := $91

; constants
OSWRCH := $FFEE

; program entry point
entry_point:
	JMP main

; 'puts' macro
puts_pos: .byte $00 ; string position
.macro	puts	addr
.proc
	lda #0
	sta puts_pos
write_byte:
	ldx puts_pos
	lda addr, x
	cmp #0
	beq done
	jsr OSWRCH
	inc puts_pos
	jmp write_byte
done:
.endproc
.endmacro

probing_cart0_msg:
	.byte "Probing cart 0"
	.byte $0D
	.byte $0A
	.byte $00
probing_cart2_msg:
	.byte "Probing cart 2"
	.byte $0D
	.byte $0A
	.byte $00
programming_bank_msg:
	.byte "Programming bank "
	.byte $00
all_done_msg:
	.byte "All done!"
	.byte $0D
	.byte $0A
	.byte $00
programming_msg:
	.byte "Programming..."
	.byte $0D
	.byte $0A
	.byte $00
blank_msg:
	.byte "ROM is blank!"
	.byte $0D
	.byte $0A
	.byte $00
waiting_msg:
	.byte "Waiting..."
	.byte $0D
	.byte $0A
	.byte $00
erasing_msg:
	.byte "Erasing..."
	.byte $0D
	.byte $0A
	.byte $00
done_msg:
	.byte "Done."
	.byte $0D
	.byte $0A
	.byte $00
crlf:
	.byte $0D
	.byte $0A
	.byte $00

previous_rom: .byte $00
erase_cart_first: .byte $00 ; erases if 1
rom_to_program: .byte $01 ; bank 00 or 01
main:
	; stash initial ROM ID
	lda $f4
	sta previous_rom

	; probe cartridge 0,1
	puts probing_cart0_msg
	LDA #0
	JSR identify_flash_chip

	puts programming_bank_msg
	lda rom_to_program
	jsr write_hex_byte
	puts crlf

	; do we need to erase the chip first?
	lda erase_cart_first
	cmp #0
	beq main__erase_done
	jsr erase_whole_chip
main__erase_done:

	lda rom_to_program
	jsr select_rom
	jsr program_16k_rom
	jsr blank_check

	; probe cartridge 2,3
	;puts probing_cart2_msg
	;LDA #2
	;JSR select_rom
	;JSR identify_flash_chip

back_to_basic:
	puts all_done_msg
	lda previous_rom
	jsr select_rom
	RTS

hang:
	puts all_done_msg
	JMP hang

; A = number to write (0-15)
write_hex_char:
	CMP #10
	BCC less_than_ten
	CLC
	ADC #55 ; add 'A' - 10
	JMP print_it
less_than_ten:
	CLC
	ADC #48 ; add '0'
print_it:
	jsr OSWRCH
	RTS

; A = byte to write
write_hex_byte:
	PHA ; stash a copy of the char
	AND #$F0
	LSR
	LSR
	LSR
	LSR
	JSR write_hex_char ; write high nybble
	PLA ; get the char back in A
	AND #$0F
	JSR write_hex_char ; write low nybble
	RTS

; X, Y = address to write
; roughly: printf("%02x%02x\r\n", y, x)
write_hex_address:
	; stash x and y for later
	txa
	pha
	tya
	pha
	; and stash x (low byte) again
	txa
	pha
	; now write y (high byte)
	tya
	jsr write_hex_byte
	; and x
	pla
	jsr write_hex_byte
	puts crlf
	; and get x and y back
	pla
	tay
	pla
	tax
	rts

; put the cartridge in the 0/1 slot
; A = rom ID to select (0-3)
select_rom:
	STA zp_lo   ; save ROM ID

	LDA #12   ; deselect BASIC
	STA $F4
	STA $FE05

	LDA zp_lo   ; load ROM ID
	STA $F4
	STA $FE05

	RTS

; we need to be able to write to addresses 2AAA and 5555 (A14-A0; don't care about A15+)
; A16 = ROMQA (bank ID)
; A15 = 0
; A14 = A12
; A13-A0 map into $8000-$BFFF
; so we select the low bank (rom_id), then:
; 2AAA = 010 1010 1010 1010, i.e. A13:0 = 2AAA, + 8000 = AAAA
; 5555 = 101 0101 0101 0101, i.e. A13:0 = 1555, + 8000 = 9555

; flash chip identification
; A = base rom ID to select (0 or 2)
rom_id: .byte $00
chip_id: .byte $00
identify_flash_chip:
	STA rom_id
	JSR select_rom

	; * enter flash ID mode
	
	; write AA to 5555
	LDA #$AA
	STA $9555
	
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	
	; write 90 to 5555
	LDA #zp_lo
	STA $9555

	; * read chip identifying info

	; read 0000, should be $BF
	LDA $8000
	JSR write_hex_byte
	puts crlf

	; read 0001, should be $B5 (or B6 for 39SF020A, B7 for 39SF040)
	LDA $8001
	JSR write_hex_byte
	puts crlf

	; * exit flash ID mode
	
	; write AA to 5555
	LDA #$AA
	STA $9555
	
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	
	; write F0 to 5555
	LDA #$F0
	STA $9555

	RTS

blank_check:
	; counter
	lda #0
	sta zp_lo
	lda #$80
	sta zp_hi

blank_check__loop:
	ldy #0
	lda (zp_lo), y
	cmp #0
	bne blank_check__not_blank ; not blank

	; increment zp_lo, zp_hi
	clc
	lda zp_lo
	adc #1
	sta zp_lo
	lda zp_hi
	adc #1
	sta zp_hi

	; are we at the end of the rom space?
	cmp #$c0
	bne blank_check__loop

	puts blank_msg ; if we get here, it's blank!

blank_check__done:
	RTS

blank_check__not_blank:
	ldx #0
	ldy zp_hi
	jmp dump_page

; --- programming ---
; A = byte to write
; X, Y = low/high bytes of address to write to (in 8000-BFFF)
; this assumes the correct bank is already selected and the sector is erased
program_byte:
	STX zp_lo ; write X,Y,A to zp_lo
	STY zp_hi
	STA $03

	; * write four command bytes
	; write AA to 5555
	LDA #$AA
	STA $9555
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	; write A0 to 5555
	LDA #$A0
	STA $9555
	; * write data to address
	LDA $03
	LDX #0
	STA (zp_lo, X)

	; * poll toggle bit until the program operation is complete
	JSR wait_until_operation_done

	RTS

; --- program 16kB rom from $2000 into bank 0 ---
; this assumes the correct bank is already selected
; and the data to program is from $2000-$6000
; (you probably want to be in MODE 6)

; source ($2000)
src_hi: .byte $00
src_lo: .byte $00
; dest ($8000)
dest_hi: .byte $00
dest_lo: .byte $00
; counter ($0000 - $4000)
pos_hi: .byte $00
pos_lo: .byte $00
; dest + counter
op_hi: .byte $00
op_lo: .byte $00
program_16k_rom:
	; start by trying to program from 4000-40ff -> a000-a0ff
	puts programming_msg

	; store src and dest addresses
	lda #$20
	sta src_hi
	clc
	adc #$60 ; 0x6000 = 0x8000 - 0x2000
	sta dest_hi

	lda #$00
	sta src_lo
	sta dest_lo

	; reset offset
	lda #$00
	sta pos_hi
	sta pos_lo

	; now loop and program 00 into every byte, to test
program_16k_rom__loop:
	; work out our destination address
	clc
	lda dest_lo
	adc pos_lo
	sta op_lo
	lda dest_hi
	adc pos_hi
	sta op_hi

	; write destination address if op_lo==0
	lda op_lo
	cmp #0
	bne program_16k_rom__done_writing_addr

	ldx op_lo
	ldy op_hi
	jsr write_hex_address

program_16k_rom__done_writing_addr:
	; get byte from memory
	clc
	lda pos_lo
	adc src_lo
	sta zp_lo
	lda pos_hi
	adc src_hi
	sta zp_hi
	; debug
	;ldx zp_lo
	;ldy zp_hi
	;jsr write_hex_address
	; /debug
	ldy #0
	lda (zp_lo), y
	; make byte programming call
	ldx op_lo
	ldy op_hi
	jsr program_byte

	; increment position
	clc
	lda pos_lo
	adc #1
	sta pos_lo
	bcc program_16k_rom__loop ; inside a 256 byte block

	; dump the page we just wrote
	clc
	lda pos_lo ; should be 0
	adc dest_lo ; should be 0
	tax
	lda pos_hi
	adc dest_hi
	tay
	;jsr dump_page

	; see if we're done otherwise go back and program another page
	clc
	lda pos_hi
	adc #1
	sta pos_hi
	cmp #$40 ; are we done programming $4000 bytes?
	bne program_16k_rom__loop

	puts done_msg
	RTS

; --- 4kB sector erase ---
; X, Y = low, high address of a byte in the sector to erase
; this assumes the correct bank is already selected
erase_sector:
	STX zp_lo ; write X,Y to zp_lo
	STY zp_hi

	; * six byte command load sequence
	; write AA to 5555
	LDA #$AA
	STA $9555
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	; write 80 to 5555
	LDA #$80
	STA $9555
	; write AA to 5555
	LDA #$AA
	STA $9555
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	; write 30 to SAx (uses Ams-A12 lines!!)
	LDA #$30
	LDX #0
	STA (zp_lo, X)

	; * poll toggle bit until the sector erase is complete
	JSR wait_until_operation_done

	RTS

; --- chip erase ---
erase_whole_chip:
	puts erasing_msg
	; * six byte command
	; write AA to 5555
	LDA #$AA
	STA $9555
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	; write 80 to 5555
	LDA #$80
	STA $9555
	; write AA to 5555
	LDA #$AA
	STA $9555
	; write 55 to 2AAA
	LDA #$55
	STA $AAAA
	; write 10 to 5555
	LDA #$10
	STA $9555

	puts waiting_msg
	; * poll toggle bit until the chip erase is complete
	JSR wait_until_operation_done
	puts done_msg

	RTS

; --- dump data from a page on the rom ---
; address in X, Y (low in X, high in Y)
dump_page:
	STX zp_lo ; page lo = zp_lo
	STY zp_hi ; page hi = zp_hi

	JSR write_hex_address

	LDA #0 ; loop counter (0-FF)
dump_page__next:
	PHA
	TAY
	LDA (zp_lo), Y
	JSR write_hex_byte
	LDA #32
	JSR OSWRCH
	PLA
	CMP #$FF
	BEQ dump_page__done
	CLC
	ADC #1
	JMP dump_page__next

dump_page__done:
	puts crlf
	RTS

; --- data# / toggle bit detection ---
wait_until_operation_done:
	; keep reading DQ6 until it stops toggling
	LDA $8000
	EOR $8000
	AND #$40
	BNE wait_until_operation_done

	RTS
