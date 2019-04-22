#ifndef ARCFLASH
#error Makefile must define ARCFLASH
#endif

#include <stdint.h>
#include "arcregs.h"
#include "arcflash.pb.h"
#include "keyboard.h"


#define STB_SPRINTF_NOUNALIGNED
#define STB_SPRINTF_NOINT64
#define STB_SPRINTF_NOFLOAT
#include "../../third_party/stb/stb_sprintf.h"

// main.cc
extern uint32_t _millis;
inline uint32_t millis() { return _millis; }

// cmos.cc
extern void read_cmos();

// descriptor.cc
extern void parse_descriptor_and_print_menu(uint32_t rom_base, arcflash_FlashDescriptor* desc);

// display.cc
#define WIDTH 640
#define HEIGHT 256
#define WHITE 255
#define BLACK 0
#define SCREEN_ADDR(x, y) (SCREEN + (y) * WIDTH + (x))
#define SCREEN_END SCREEN_ADDR(WIDTH, HEIGHT)
extern int display_x, display_y;
extern void display_goto(int x, int y);
extern void display_print_char(char c);
extern void display_print(const char* s);
extern void display_print_hex(uint32_t v);
extern void display_printf(char const *format, ...);
