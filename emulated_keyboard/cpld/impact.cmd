setMode -bscan
addDevice -p 1 -file emulated_keyboard.jed

setCable -p svf -file emulated_keyboard.svf
program -e -v -p 1

setCable -p xsvf -file emulated_keyboard.xsvf
program -e -v -p 1

quit
