setMode -bscan
addDevice -p 1 -file master_updateable_megarom.jed

setCable -p svf -file master_updateable_megarom.svf
program -e -v -p 1

setCable -p xsvf -file master_updateable_megarom.xsvf
program -e -v -p 1

quit
