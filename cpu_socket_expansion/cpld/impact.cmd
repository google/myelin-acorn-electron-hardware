setMode -bscan
addDevice -p 1 -file cpu_socket_expansion.jed

setCable -p svf -file cpu_socket_expansion.svf
program -e -v -p 1

setCable -p xsvf -file cpu_socket_expansion.xsvf
program -e -v -p 1

quit
