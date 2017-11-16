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

; ----------------------------------------
; SST39SF010A programming code
; Phillip Pearson - philpearson@google.com
; ----------------------------------------

; This is built to run at &1100, so it'll only work if you're running from
; tape, or something with a fairly low PAGE.  I'm using it to program UPURS
; and MMFS into an SST39SF010A chip installed as IC100 in a BBC B issue 7,
; after reading them over the tape interface.

; PAGE=E00
; HIMEM=1100 because i've *RUN something which loads in there
; mode 6 screen start = 6000
; we can load a 16k rom from $2000-$6000 and program it from there.

BBC = 1 ; set one of these to 1 depending on the target machine
ELECTRON = 0

ERASE_CART_FIRST = 0 ; set to 1 to erase the whole chip (all banks) first
ERASE_INDIVIDUAL_BANKS = 1 ; set to 1 to erase individual banks as they are programmed

; Set in parent script
; PROGRAM_ROM = 0 ; set to 0 to just probe banks
; BANK_TO_PROGRAM = &E ; set to the bank you want to program

; zero page addresses
zp_lo = $90
zp_hi = $91

; constants
OSWRCH = $FFEE
OSNEWL = $FFE7
if BBC
    BANKREG = $FE30 ; BBC
elif ELECTRON
    BANKREG = $FE05 ; Electron
else
    ERROR "Neither BBC or ELECTRON are set to 1"
endif

; assemble at &1900
    org $1900

; program entry point
.entry_point:
    JMP main

; 'puts' macro
.puts_pos: equb $00 ; string position
MACRO puts addr
    lda #0
    sta puts_pos
.write_byte:
    ldx puts_pos
    lda addr, x
    cmp #0
    beq done
    jsr OSWRCH
    inc puts_pos
    jmp write_byte
.done:
ENDMACRO

; smaller (?) puts macro
MACRO puts2 addr
    ldx #0
.write_byte2:
    lda addr, x
    cmp #0
    beq done_puts2
    jsr OSWRCH
    inx
    jmp write_byte2
.done_puts2:
ENDMACRO

;.puts3_string: equw 0
;.puts3_internal:
;    ldy #0
;.write_byte3:
;    lda (puts3_string), y
;    cmp #0
;    beq done_puts3
;    jsr OSWRCH
;    iny
;    jmp write_byte3
;.done_puts3:
;    rts
;MACRO puts3 addr
;    lda #lo(addr)
;    sta puts3_string
;    ldx #hi(addr)
;    sta puts3_string+1
;    jsr puts3_internal
;ENDMACRO

.probing_bank_msg:
    equb "Probing bank ", $00
.colon_space:
    equb ":"
.space:
    equb " ", $00
.programming_bank_msg:
    equb "Programming bank ", $00
.all_done_msg:
    equb "All done :)", $0d, $0a, $00
.programming_msg:
    equb "Programming...", $0d, $0a, $00
.blank_msg
    equb "ROM is blank!", $0d, $0a, $00
.waiting_msg
    equb "Waiting...", $0d, $0a, $00
.erasing_msg
    equb "Erasing...", $0d, $0a, $00
.done_msg
    equb "Done.", $0d, $0a, $00
.chip_is_flash_msg
    equb "FLASH", $00
.chip_is_ram_msg
    equb "RAM", $00

.previous_rom: equb $00
.main
    ; stash initial ROM ID
    lda $f4
    sta previous_rom

    ; probe banks 0-15
    lda #0
.main__probe_cart
    jsr identify_flash_chip
    clc
    adc #1
    cmp #16
    bne main__probe_cart

    ; now program in a rom, if we need to
if PROGRAM_ROM
    puts programming_bank_msg
    lda #BANK_TO_PROGRAM
    jsr write_hex_byte
    jsr OSNEWL

    ;TODO ideally we should erase 4k chunks while programming,
    ; which means no need for ERASE_CART_FIRST
if ERASE_CART_FIRST
    jsr erase_whole_chip
endif ; ERASE_CART_FIRST

    lda #BANK_TO_PROGRAM
    jsr select_rom
if ERASE_INDIVIDUAL_BANKS
    jsr erase_16k
endif
    jsr program_16k_rom
    jsr blank_check

endif ; PROGRAM_ROM

.back_to_basic
    puts all_done_msg
    lda previous_rom
    jsr select_rom
    RTS

.hang
    puts all_done_msg
    JMP hang

; A = number to write (0-15)
.write_hex_char
    CMP #10
    BCC less_than_ten
    CLC
    ADC #55 ; add 'A' - 10
    JMP print_it
.less_than_ten
    CLC
    ADC #48 ; add '0'
.print_it
    jsr OSWRCH
    RTS

; A = byte to write
.write_hex_byte
    PHA
    PHA ; stash two copy of the char
    AND #$F0
    LSR A
    LSR A
    LSR A
    LSR A
    JSR write_hex_char ; write high nybble
    PLA ; get the char back in A
    AND #$0F
    JSR write_hex_char ; write low nybble
    PLA ; get the char back in A
    RTS

; X, Y = address to write
; roughly: printf("%02x%02x\r\n", y, x)
.write_hex_address
    ; stash a, x, y for later
    pha
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
    jsr OSNEWL
    ; and get a, x, y back
    pla
    tay
    pla
    tax
    pla
    rts

; put the cartridge in the 0/1 slot
; A = rom ID to select (0-3)
.select_rom

if ELECTRON
    pha
    lda #12 ; deselect BASIC
    sta $F4
    sta BANKREG
    pla
endif

    ; select the actual ROM
    sta $F4
    sta BANKREG

    rts

; we need to be able to write to addresses 2AAA and 5555 (A14-A0; don't care about A15+)
; A16 = ROMQA (bank ID)
; A15 = 0
; A14 = A12
; A13-A0 map into $8000-$BFFF
; so we select the low bank (rom_id), then
; 2AAA = 010 1010 1010 1010, i.e. A13:0 = 2AAA, + 8000 = AAAA
; 5555 = 101 0101 0101 0101, i.e. A13:0 = 1555, + 8000 = 9555

; on the BBC A16 and A15 are connected to bank select pins
; but A14 is still wired to A12, and A13:0 map to $8000-BFFF.


; flash chip identification
; A = base rom ID to select (0 or 2)
; this will output: Probing bank XX: YY ZZ
; YY = BF for SST39SF010
; ZZ = B5 for SST39SF010, B6 for -020, B7 for -040
.rom_id: equb $00
.chip_id: equb $00
; temp space so we don't trash sideways ram
.tmp_a: equb $00
.tmp_b: equb $00
.is_flash: equb $00
.identify_flash_chip
    sta rom_id

    puts probing_bank_msg
    lda rom_id
    jsr write_hex_byte
    puts colon_space

    lda rom_id
    jsr select_rom

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

    lda #0
    sta is_flash

    ; read 0000, should be $BF
    LDA $8000
    JSR write_hex_byte

    ; check if it's flash, and set is_flash to 1 if it is
    cmp #$BF
    bne identify_flash_chip__not_flash
    lda #1
    sta is_flash

.identify_flash_chip__not_flash
    puts space

    ; read 0001, should be $B5 (or B6 for 39SF020A, B7 for 39SF040)
    LDA $8001
    JSR write_hex_byte
    puts space

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

    ; print "FLASH" message if it's flash
    lda is_flash
    beq check_chip_is_ram
    puts chip_is_flash_msg

.check_chip_is_ram
    ; check if it's RAM

    ; stash the first two bytes
    lda $8000
    sta tmp_a
    lda $8001
    sta tmp_b
    ; zero them out and verify that they stay that way
    lda #$00
    sta $8000
    sta $8001
    lda $8000
    bne identify_flash_chip__not_ram
    lda $8001
    bne identify_flash_chip__not_ram
    ; write some new values in
    lda rom_id
    STA $8000
    clc
    adc #1
    sta $8001
    tax
    ; verify they were written
    lda rom_id
    cmp $8000
    bne identify_flash_chip__not_ram
    txa
    cmp $8001
    bne identify_flash_chip__not_ram

    ; it's ram!
    puts chip_is_ram_msg

.identify_flash_chip__not_ram
    ; whether it was ram or not, put the bytes back the way we found them
    lda tmp_a
    sta $8000
    lda tmp_b
    sta $8001

    jsr OSNEWL
    lda rom_id ; return A to starting value
    RTS

.blank_check
    ; counter
    lda #0
    sta zp_lo
    lda #$80
    sta zp_hi

.blank_check__loop
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

.blank_check__done
    RTS

.blank_check__not_blank
    ldx #0
    ldy zp_hi
    jmp dump_page

; --- programming ---
; A = byte to write
; X, Y = low/high bytes of address to write to (in 8000-BFFF)
; this assumes the correct bank is already selected and the sector is erased
.program_byte
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
.src_hi: equb $00
.src_lo: equb $00
; dest ($8000)
.dest_hi: equb $00
.dest_lo: equb $00
; counter ($0000 - $4000)
.pos_hi: equb $00
.pos_lo: equb $00
; dest + counter
.op_hi: equb $00
.op_lo: equb $00
.program_16k_rom:
    ; Programming ...
    puts programming_msg

    ; store src and dest addresses
    lda #$00
    sta src_lo
    sta dest_lo

    lda #$20  ; src = $2000
    sta src_hi

    lda #$80  ; dest = $8000
    sta dest_hi

    ; reset offset
    lda #$00
    sta pos_hi
    sta pos_lo

    ; now program bytes, one by one
.program_16k_rom__loop:
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

.program_16k_rom__done_writing_addr:
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

; --- 16kB erase ---
.erase_16k
    puts erasing_msg

    ldx #$00
    ldy #$80
    jsr erase_sector

    ldx #$00
    ldy #$90
    jsr erase_sector

    ldx #$00
    ldy #$a0
    jsr erase_sector

    ldx #$00
    ldy #$b0
    jsr erase_sector

    RTS

; --- 4kB sector erase ---
; X, Y = low, high address of a byte in the sector to erase
; this assumes the correct bank is already selected
.erase_sector:
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
    STA (zp_lo, X)  ; = STA (zp_lo) because X=0

    ; * poll toggle bit until the sector erase is complete
    JSR wait_until_operation_done

    RTS

; --- chip erase ---
.erase_whole_chip:
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
.dump_page:
    STX zp_lo ; page lo = zp_lo
    STY zp_hi ; page hi = zp_hi

    JSR write_hex_address

    LDA #0 ; loop counter (0-FF)
.dump_page__next:
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

.dump_page__done:
    jsr OSNEWL
    RTS

; --- data# / toggle bit detection ---
.wait_until_operation_done:
    ; keep reading DQ6 until it stops toggling
    LDA $8000
    EOR $8000
    AND #$40
    BNE wait_until_operation_done

    RTS

; all done!
.end_of_code
SAVE "flash_rom.bin", entry_point, end_of_code
