#include <stdint.h>
#include "arcregs.h"

// display.cc
#define WIDTH 640
#define HEIGHT 256
#define WHITE 255
#define BLACK 0
#define SCREEN_ADDR(x, y) (SCREEN + (y) * WIDTH + (x))
#define SCREEN_END SCREEN_ADDR(WIDTH, HEIGHT)
extern void display_goto(int x, int y);
extern void display_print(const char* s);
extern void display_print_hex(uint32_t v);
