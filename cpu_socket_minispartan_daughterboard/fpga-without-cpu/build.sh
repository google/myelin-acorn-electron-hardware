#!/bin/bash

export LM_LICENSE_FILE=$HOME/.Xilinx.lic
. /opt/Xilinx/14.7/ISE_DS/settings64.sh

set -uex
./build.tcl
