setMode -bscan
addDevice -p 1 -file econet.jed

setCable -p svf -file econet.svf
program -e -v -p 1

setCable -p xsvf -file econet.xsvf
program -e -v -p 1

quit
