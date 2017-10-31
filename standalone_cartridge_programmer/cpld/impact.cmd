setMode -bscan
addDevice -p 1 -file standalone_programmer.jed

setCable -p svf -file standalone_programmer.svf
program -e -v -p 1

setCable -p xsvf -file standalone_programmer.xsvf
program -e -v -p 1

quit
