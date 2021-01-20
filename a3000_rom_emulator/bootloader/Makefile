all: build

clean:
	rm -rf uf2-samdx1 *.bin *.ino *.uf2

uf2-samdx1:
	git clone https://github.com/myelin/uf2-samdx1.git

build: uf2-samdx1
	(cd uf2-samdx1; make BOARD=myelin_arcflash)
	rm -f *.bin *.ino *.uf2
	cp uf2-samdx1/build/myelin_arcflash/{bootloader-*.bin,update-*.{ino,uf2}} ./
