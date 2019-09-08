#!/bin/bash

set -e

cd $(dirname $0)

# Copy various files from //third_party/libxsvf into
# ./src/libxsvf, to make it buildable as an Arduino library.

SRC=../../third_party/libxsvf
DEST=src/libxsvf

rm -rf $DEST
mkdir -p $DEST
cp -a $SRC/*.c $SRC/*.cpp $SRC/*.h $DEST/
rm $DEST/xsvftool-ft232h.c $DEST/xsvftool-gpio.c
echo "This is copied from third_party/libxsvf; do not edit these files" > $DEST/README
chmod -w $DEST/*
