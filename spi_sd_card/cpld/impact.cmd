setMode -bscan
addDevice -p 1 -file spi_sd_card.jed

setCable -p svf -file spi_sd_card.svf
program -e -v -p 1

setCable -p xsvf -file spi_sd_card.xsvf
program -e -v -p 1

quit
