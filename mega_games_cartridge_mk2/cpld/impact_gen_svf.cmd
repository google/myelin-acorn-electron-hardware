setMode -bscan
addDevice -p 1 -file MGC.jed

setCable -p svf -file MGC.svf
program -e -v -p 1

setCable -p xsvf -file MGC.xsvf
program -e -v -p 1

quit
