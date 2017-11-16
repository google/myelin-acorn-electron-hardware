default: all

ALL=flash_rom probe

all: $(addsuffix .bin, $(ALL))

# USAGE:

# make probe
# - probes flash banks

# make program BANK=E
# - programs the data from &2000 into bank &E

program: write_bank flash_rom

write_bank:
	echo "BANK_TO_PROGRAM = &$(BANK)" > bank_to_program.inc

flash_rom.bin: bank_to_program.inc

### Common rules

%.bin: %.asm common.asm
	beebasm -i $< -o $@

$(ALL): %: %.bin
	python ../../third_party/uef-utils/file_to_wav.py $< 1900

clean:
	rm -vf bank_to_program.inc \
	       $(addsuffix .bin, $(ALL)) \
	       $(addsuffix .bin.uef, $(ALL)) \
	       $(addsuffix .bin.wav, $(ALL))
