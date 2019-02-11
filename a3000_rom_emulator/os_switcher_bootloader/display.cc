#include "arcflash.h"

static int display_x = 0, display_y = 0;

// riscosfont is defined in third_party/riscos/riscos_font.s
extern "C" {
	extern const uint8_t riscos_font[8 * 256];
}

void display_goto(int x, int y) {
	display_x = x;
	display_y = y;
}

void display_print(const char* s) {
	for (const uint8_t *sptr = (const uint8_t *)s; *sptr; sptr++) {
		int c = *sptr;
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
		if (display_x > WIDTH) {
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
	}
}
