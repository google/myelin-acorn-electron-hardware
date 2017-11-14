default:
	make -C 32kb_flash_cartridge/pcb-common
	make -C atsamd11_pro_micro/pcb
	make -C atsamd21_usb_host/pcb
	make -C bbc_power_distribution/pcb
	make -C cpu_socket_expansion/pcb
	make -C cpu_socket_minispartan_daughterboard/pcb
	make -C econet_from_scratch/pcb
	make -C elk_pi_tube_direct/pcb
	make -C master_updateable_megarom/pcb
	make -C minus_one/pcb
	make -C serial_sd_adapter/bbc_1mhz_bus_pcb
	make -C standalone_cartridge_programmer/pcb

rebuild:
	make -C 32kb_flash_cartridge/pcb-common rebuild
	make -C atsamd11_pro_micro/pcb rebuild
	make -C atsamd21_usb_host/pcb rebuild
	make -C bbc_power_distribution/pcb rebuild
	make -C cpu_socket_expansion/pcb rebuild
	make -C cpu_socket_minispartan_daughterboard/pcb rebuild
	make -C econet_from_scratch/pcb rebuild
	make -C elk_pi_tube_direct/pcb rebuild
	make -C master_updateable_megarom/pcb rebuild
	make -C minus_one/pcb rebuild
	make -C serial_sd_adapter/bbc_1mhz_bus_pcb rebuild
	make -C standalone_cartridge_programmer/pcb rebuild
