setMode -bscan
addDevice -p 1 -file xc9500.jed

setCable -p svf -file xc9500.svf
program -e -v -p 1

setCable -p xsvf -file xc9500.xsvf
program -e -v -p 1

quit
