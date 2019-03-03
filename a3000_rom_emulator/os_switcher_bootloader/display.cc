// include sprintf implementation when arcflash pulls in stb_sprintf.h
#define STB_SPRINTF_IMPLEMENTATION

#include "arcflash.h"
#include <stdarg.h>

int display_x = 0, display_y = 0;

// riscosfont is defined in third_party/riscos/riscos_font.s
extern "C" {
	extern const uint8_t riscos_font[8 * 256];
}

__attribute__((section(".ramfunc")))
void display_goto(int x, int y) {
	display_x = x;
	display_y = y;
}

__attribute__((section(".ramfunc")))
static void newline() {
	display_x = 0;
	display_y += 8;
	if (display_y > HEIGHT - 1) {
		// copy entire page up 8 rows
		for (volatile uint32_t *ptr = (volatile uint32_t *)SCREEN;
			ptr < (volatile uint32_t *)SCREEN_ADDR(0, HEIGHT - 8);
			ptr++)
		{
			*ptr = *(volatile uint32_t *)((volatile uint8_t *)ptr + WIDTH * 8);
		}
		display_y -= 8;
	}
}

__attribute__((section(".ramfunc")))
void display_print_char(char c) {
	switch (c) {
		case '\r':
			display_x = 0;
			return;
		case '\n':
			newline();
			return;
	}

	const uint8_t *patternptr = &riscos_font[8 * c];
	volatile uint8_t *displayptr = SCREEN + display_x + display_y * 640;
	for (int y = 0; y < 8; ++y) {
		uint8_t pattern = *patternptr++;
		for (int x = 0; x < 8; ++x) {
			SCREEN[(y + display_y) * WIDTH + (x + display_x)] = (pattern & 0x80) ? WHITE : BLACK;
			pattern <<= 1;
		}
		displayptr += 640 - 8;
	}
	display_x += 8;
	if (display_x >= WIDTH) {
		newline();
	}
}

__attribute__((section(".ramfunc")))
void display_print(const char* s) {
	for (const uint8_t *sptr = (const uint8_t *)s; *sptr; sptr++) {
		display_print_char(*sptr);
	}
}

__attribute__((section(".ramfunc")))
char hex_digit(int v) {
	if (v < 10)
		return '0' + v;
	if (v < 16)
		return 'A' + v - 10;
	return 'X';
}

__attribute__((section(".ramfunc")))
void display_print_hex(uint32_t v) {
	char s[9];
	int digits = 1;
	while (digits < 8 && v > (1 << (digits * 4))) {
		++digits;
	}
	uint32_t shift = (digits - 1) * 4;
	uint32_t mask = 15 << shift;
	for (int i = 0; i < digits; ++i) {
		s[i] = hex_digit((v & mask) >> shift);
		mask >>= 4;
		shift -= 4;
	}
	s[digits] = 0;
	display_print(s);
}

__attribute__((section(".ramfunc")))
void display_printf(char const *format, ...) {
	va_list ap;
	va_start(ap, format);
	char buf[200];
	int ret = stbsp_vsnprintf(buf, 200, format, ap);
	if (ret < 0) {
		display_print("printf error");
	} else {
		display_print(buf);
	}
	va_end(ap);
}
