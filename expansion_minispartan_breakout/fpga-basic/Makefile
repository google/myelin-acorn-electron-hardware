default: all

push:
	rsync -avrz --delete . xilinx:minispartan_basic/

all: push
	ssh xilinx 'cd minispartan_basic && ./build.sh'
	rsync -avrz xilinx:minispartan_basic/*.bit .
	xc3sprog -c ftdi minispartan_expansion.bit

pull:
	rsync -avrz xilinx:minispartan_basic/*.bit .

unload_ftdi:
	sudo kextunload -bundle-id com.apple.driver.AppleUSBFTDI

load_ftdi:
	sudo kextload -bundle-id com.apple.driver.AppleUSBFTDI

program:
	xc3sprog -c ftdi minispartan_expansion.bit
