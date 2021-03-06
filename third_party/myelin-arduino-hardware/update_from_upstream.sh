#!/bin/bash
set -euo pipefail

# Syntax: $0 /path/to/ArduinoCore-samd

SRC=$1
DEST=samd

for path in cores/arduino libraries/Adafruit_ZeroDMA libraries/SPI libraries/Wire; do
	rm -rf $DEST/$path
	cp -av $SRC/$path $DEST/$path
	git add $DEST/$path
done

git status -- .
