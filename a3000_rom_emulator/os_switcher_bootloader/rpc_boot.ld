OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH("arm")
ENTRY(_start)

MEMORY {
	/* This is easy for the Risc PC bootloader, because we're in RAM right
	 * from the start.  All we need to do is clear bss and we're ready to go. */
	RAM (rwx) : ORIGIN = 0x8000, LENGTH = 512k
}

C_STACK_SIZE = 65536;

SECTIONS {
	/* reset code */
	. = 0x8000;
	.reset : {
		_text = .;  /* relocation to RAM in rpc_start.s starts here */
		*rpc_start.o (.text)
		. = ALIGN(0x4);
	} >RAM

	/* code and read-only vars */
	.text : {
		*(.text .text* .gnu.linkonce.t.*)
		*(.rodata .rodata* .gnu.linkonce.r.*)
		. = ALIGN(0x4);
		_etext = .;  /* used to locate initial values for .data */
	} >RAM

	/* writable data */
	.data : {
		_data = .;
		*(.data)
		*(.ramfunc)
		. = ALIGN(0x4);
		_edata = .;  /* relocation to RAM in rpc_start.s ends here */
	} >RAM

	/* zero-initialized data */
	.bss : {
		__bss_start__ = .;
		*(.bss)
		. = ALIGN(0x4);
		__bss_end__ = .;
	} >RAM

	/* the stack */
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
