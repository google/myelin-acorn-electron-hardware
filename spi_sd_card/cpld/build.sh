#!/bin/bash
set -euo pipefail

# Build for both XC9572 and XC9536

for chip in xc9572xl-10-VQ44 xc9536xl-10-VQ44; do
    echo "Building for $chip"
    echo
    sed -i.bak -e "s/PART=.*/PART=$chip/" Makefile
    make remote
done
