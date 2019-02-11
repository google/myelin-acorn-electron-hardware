#include <stdint.h>
#include "arcregs.h"

// main.cc
extern uint32_t _millis;
inline uint32_t millis() { return _millis; }

// display.cc
#define WIDTH 640
#define HEIGHT 256
#define WHITE 255
#define BLACK 0
#define SCREEN_ADDR(x, y) (SCREEN + (y) * WIDTH + (x))
#define SCREEN_END SCREEN_ADDR(WIDTH, HEIGHT)
extern int display_x, display_y;
extern void display_goto(int x, int y);
extern void display_print(const char* s);
extern void display_print_hex(uint32_t v);

// keyboard.cc
extern int mouse_x, mouse_y;
extern void keyboard_poll();
