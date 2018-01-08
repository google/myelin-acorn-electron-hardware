ARDUINO=/Applications/Arduino.app/Contents/Java
ARDUINO15=$(HOME)/Library/Arduino15
LOCAL_ARDUINO=$(HOME)/Documents/Arduino

PROJECT=usb_keyboard_forwarder

TARGET=$(BUILD)/$(PROJECT).ino.elf
BUILD=$$(pwd)/build
CACHE=$(BUILD)/cache

.PHONY: default build clean program reset

default: build

clean:
	rm -rf $(BUILD) $(CACHE)

program:
	JLinkExe -CommanderScript program.jlink

reset:
	JLinkExe -CommanderScript reset.jlink

build:
	mkdir -p $(BUILD) $(CACHE)
	$(ARDUINO)/arduino-builder -compile \
		-logger=machine \
		-hardware $(ARDUINO)/hardware \
		-hardware $(ARDUINO15)/packages \
		-hardware $(LOCAL_ARDUINO)/hardware \
		-tools $(ARDUINO)/tools-builder \
		-tools $(ARDUINO)/hardware/tools/avr \
		-tools $(ARDUINO15)/packages \
		-built-in-libraries $(ARDUINO)/libraries \
		-libraries $(LOCAL_ARDUINO)/libraries \
		-fqbn=MattairTech_Arduino:samd:mattairtech_mt_d21e_revb:clock=crystal_32k,cpu=samd21e18a,bootloader=0kb,serial=one_uart,usb=cdc_hid \
		-ide-version=10805 \
		-build-path $(BUILD) \
		-warnings=none \
		-build-cache $(CACHE) \
		-prefs=build.warn_data_percentage=75 \
		-prefs=runtime.tools.CMSIS.path=$(ARDUINO15)/packages/arduino/tools/CMSIS/4.5.0 \
		-prefs=runtime.tools.arm-none-eabi-gcc.path=$(ARDUINO15)/packages/arduino/tools/arm-none-eabi-gcc/4.8.3-2014q1 \
		-prefs=runtime.tools.arduinoOTA.path=$(ARDUINO15)/packages/arduino/tools/arduinoOTA/1.2.0 \
		-prefs=runtime.tools.openocd.path=$(ARDUINO15)/packages/arduino/tools/openocd/0.9.0-arduino \
		-prefs=runtime.tools.bossac.path=$(ARDUINO15)/packages/MattairTech_Arduino/tools/bossac/1.7.0-mattairtech-2 \
		-prefs=runtime.tools.CMSIS-Atmel.path=$(ARDUINO15)/packages/MattairTech_Arduino/tools/CMSIS-Atmel/1.0.0-mattairtech-2 \
		-verbose \
		$(PROJECT).ino
	echo "Build done"
	ls -al $(TARGET)
