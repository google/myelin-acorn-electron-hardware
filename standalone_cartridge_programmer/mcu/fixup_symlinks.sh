#!/bin/bash
set -e

# Fix up all the symlinks that Dropbox likes to break

for f in libxsvf.h memname.c play.c scan.c statename.c svf.c tap.c xsvf.c xsvftool-arduino.cpp; do
    S=../../third_party/libxsvf/$f
    rm -vf $f
    ln -sv $S
done
