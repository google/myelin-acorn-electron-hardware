setMode -bscan
addDevice -p 1 -file minus_one.jed

setCable -p svf -file minus_one.svf
program -e -v -p 1

setCable -p xsvf -file minus_one.xsvf
program -e -v -p 1

quit
