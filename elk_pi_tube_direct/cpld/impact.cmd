setMode -bscan
addDevice -p 1 -file elk_pi_tube_direct.jed

setCable -p svf -file elk_pi_tube_direct.svf
program -e -v -p 1

setCable -p xsvf -file elk_pi_tube_direct.xsvf
program -e -v -p 1

quit
