OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH("arm")
ENTRY(_start)

MEMORY {
	ROM (rx)  : ORIGIN = 0x3800000, LENGTH = 2M
	RAM (rwx) : ORIGIN = 0x2000000, LENGTH = 512k
}

C_STACK_SIZE = 16384;

SECTIONS {
	/* reset code, runs from zero */
	. = 0x0;
	.reset : {
		*start.o (.text)
		. = ALIGN(0x4);
	} >ROM

	/* main code, runs from rom */
	.text : {
		*(.text .text* .gnu.linkonce.t.*)
		*(.rodata .rodata* .gnu.linkonce.r.*)
		. = ALIGN(0x4);
		_etext = .;  /* used to locate initial values for .data */
	} >ROM

	/* data is copied from rom to ram */
	.data : {
		_data = .;
		*(.data)
		. = ALIGN(0x4);
		_edata = .;
	} >RAM AT>ROM

	/* bss only exists in ram */
	.bss : {
		__bss_start__ = .;
		*(.bss)
		. = ALIGN(0x4);
		__bss_end__ = .;
	} >RAM

	/* stack also only exists in ram */
	.stack : {
		__stack_start = .;
		. += C_STACK_SIZE;
		. = ALIGN(0x4);
		__stack_end = .;
	}

	/* heap start */
	_end = .;
	__end__ = _end;
	PROVIDE(end = .);

}