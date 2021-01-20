setMode -bscan
addDevice -p 1 -file a3000_rom_emulator.jed

setCable -p svf -file a3000_rom_emulator.svf
program -e -v -p 1

setCable -p xsvf -file a3000_rom_emulator.xsvf
program -e -v -p 1

quit
