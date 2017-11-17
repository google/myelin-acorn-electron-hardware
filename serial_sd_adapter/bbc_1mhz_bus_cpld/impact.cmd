setMode -bscan
addDevice -p 1 -file serial_sd_adapter.jed

setCable -p svf -file serial_sd_adapter.svf
program -e -v -p 1

setCable -p xsvf -file serial_sd_adapter.xsvf
program -e -v -p 1

quit
