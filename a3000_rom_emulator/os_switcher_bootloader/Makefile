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
CC = arm-none-eabi-g++
LD = arm-none-eabi-g++
OBJCOPY = arm-none-eabi-objcopy
CFLAGS = -mcpu=arm2 -mno-thumb-interwork -fno-exceptions
LDFLAGS = -nostdlib -lgcc

.PHONY: default all clean

default: all

clean:
	rm -vf *.bin *.elf *.o *.rom

all: switcher.bin jump_to_rom.bin

%.o: %.s
	$(AS) -o $@ $<

%.o: %.cc
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.c
	$(CCC) $(CFLAGS) -c -o $@ $<

%.elf: %.o
	$(LD) $(CFLAGS) $(LDFLAGS) -Wl,--section-start=.text=0 -o $@ $<

%.rom: %.bin
	python pad_to_rom.py $< $@

SWITCHER_OBJS=start.o cstartup.o main.o

switcher.elf: $(SWITCHER_OBJS)
	$(LD) $(CFLAGS) $(LDFLAGS) -Wl,--section-start=.text=0 -o $@ $(SWITCHER_OBJS)

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@

show: switcher.rom
	arm-none-eabi-objdump -S --disassemble switcher.elf