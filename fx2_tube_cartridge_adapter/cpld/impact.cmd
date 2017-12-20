setMode -bscan
addDevice -p 1 -file fx2_tube_cartridge_adapter.jed

setCable -p svf -file fx2_tube_cartridge_adapter.svf
program -e -v -p 1

setCable -p xsvf -file fx2_tube_cartridge_adapter.xsvf
program -e -v -p 1

quit
