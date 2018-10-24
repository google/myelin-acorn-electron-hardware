#!/bin/bash

set -e

cd $(dirname $0)

# Copy crcccitt.c from //third_party/libcrc
cp -a ../../third_party/libcrc/src/crceconet.c ../../third_party/libcrc/include/checksum.h .

# Copy various files from //third_party/libxsvf into
# ./libraries/libxsvf, to make it buildable as an Arduino library.

SRC=../../third_party/libxsvf
DEST=libraries/libxsvf

rm -rf $DEST
mkdir -p $DEST
cp -a $SRC/*.c $SRC/*.cpp $SRC/*.h $DEST/
rm $DEST/xsvftool-ft232h.c $DEST/xsvftool-gpio.c
echo "This is copied from third_party/libxsvf; do not edit these files" > $DEST/README
chmod -w $DEST/*
