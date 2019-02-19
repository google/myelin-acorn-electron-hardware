# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

AS = arm-none-eabi-as
CCC = arm-none-eabi-g++
CC = arm-none-eabi-gcc
LD = arm-none-eabi-g++
OBJCOPY = arm-none-eabi-objcopy
CFLAGS = -mcpu=arm2 -mno-thumb-interwork -fno-exceptions -ffreestanding -O2 -I../../third_party/nanopb
LDFLAGS = -nostdlib -lgcc

.PHONY: default all clean

default: all

clean:
	rm -vf *.bin *.elf *.o *.rom

all: switcher.rom jump_to_rom.bin

%.o: %.s
	$(AS) -o $@ $<

riscos_font.o: ../../third_party/riscos/riscos_font.s
	$(AS) -o $@ $<

%.o: %.cc
	$(CCC) $(CFLAGS) -c -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.elf: %.o
	$(LD) $(CFLAGS) $(LDFLAGS) -Wl,--section-start=.text=0 -o $@ $<

%.rom: %.bin
	cp $< $@

# nanopb build step
../../third_party/nanopb/generator/proto/nanopb_pb2.py: ../../third_party/nanopb/generator/proto/nanopb.proto
	cd ../../third_party/nanopb/generator/proto; protoc --python_out=. nanopb.proto

arcflash.pb arcflash.pb.c arcflash.pb.h arcflash_pb2.py: arcflash.proto ../../third_party/nanopb/generator/proto/nanopb_pb2.py
	protoc --python_out=. -o$@ $<
	python3 ../../third_party/nanopb/generator/nanopb_generator.py $@

SWITCHER_OBJS=cmos.o display.o cstartup.o keyboard.o main.o riscos_font.o start.o \
	arcflash.pb.o \
	../../third_party/arm-trusted-firmware/arm32_aeabi_divmod.o \
	../../third_party/arm-trusted-firmware/arm32_aeabi_divmod_a32.o \
	../../third_party/arm-trusted-firmware/memcpy.o \
	../../third_party/arm-trusted-firmware/memset.o \
	../../third_party/nanopb/pb_common.o ../../third_party/nanopb/pb_encode.o ../../third_party/nanopb/pb_decode.o

switcher.elf: $(SWITCHER_OBJS)
	$(LD) $(CFLAGS) $(LDFLAGS) -Wl,--script=switcher.ld -Wl,-Map,switcher.map -o $@ $(SWITCHER_OBJS)
	arm-none-eabi-objdump -S --disassemble switcher.elf > switcher.list

%.bin: %.elf
	arm-none-eabi-size $<
	$(OBJCOPY) -O binary $< $@
	ls -al $@
