#include <stdint.h>
#include "arcregs.h"

// main.cc
extern uint32_t _millis;
inline uint32_t millis() { return _millis; }
extern void keyboard_keydown(uint8_t keycode);
extern void keyboard_keyup(uint8_t keycode);

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

// keyboard.cc
extern int mouse_x, mouse_y;
extern void keyboard_poll();

// Top row - esc, function keys, print/scroll/break
#define KEY_ESC 0x00
#define KEY_F1 0x01
#define KEY_F2 0x02
#define KEY_F3 0x03
#define KEY_F4 0x04
#define KEY_F5 0x05
#define KEY_F6 0x06
#define KEY_F7 0x07
#define KEY_F8 0x08
#define KEY_F9 0x09
#define KEY_F10 0x0a
#define KEY_F11 0x0b
#define KEY_F12 0x0c
#define KEY_PRINT 0x0d
#define KEY_SCROLL 0x0e
#define KEY_BREAK 0x0f

// Top main row - numbers, ins/home/pgup, top row of numpad
#define KEY_TILDE 0x10
#define KEY_1 0x11
#define KEY_2 0x12
#define KEY_3 0x13
#define KEY_4 0x14
#define KEY_5 0x15
#define KEY_6 0x16
#define KEY_7 0x17
#define KEY_8 0x18
#define KEY_9 0x19
#define KEY_0 0x1a
#define KEY_MINUS_UNDERSCORE 0x1b
#define KEY_EQUALS_PLUS 0x1c
#define KEY_POUND_THING 0x1d
#define KEY_BACKSPACE 0x1e
#define KEY_INSERT 0x1f
#define KEY_HOME 0x20
#define KEY_PGUP 0x21
#define KEY_NUMLOCK 0x22
#define KEY_NUM_SLASH 0x23
#define KEY_NUM_STAR 0x24
#define KEY_NUM_HASH 0x25

// Row 2 - qwerty, del/copy/pgdn, num 789
#define KEY_TAB 0x26
#define KEY_Q 0x27
#define KEY_W 0x28
#define KEY_E 0x29
#define KEY_R 0x2a
#define KEY_T 0x2b
#define KEY_Y 0x2c
#define KEY_U 0x2d
#define KEY_I 0x2e
#define KEY_O 0x2f
#define KEY_P 0x30
#define KEY_LEFT_BRACE 0x31
#define KEY_RIGHT_BRACE 0x32
#define KEY_BACKSLASH 0x33
#define KEY_DEL 0x34
#define KEY_COPY 0x35
#define KEY_PGDN 0x36
#define KEY_NUM_7 0x37
#define KEY_NUM_8 0x38
#define KEY_NUM_9 0x39
#define KEY_NUM_MINUS 0x3a

// Row 3 - asdf, num 456
#define KEY_LCTRL 0x3b
#define KEY_A 0x3c
#define KEY_S 0x3d
#define KEY_D 0x3e
#define KEY_F 0x3f
#define KEY_G 0x40
#define KEY_H 0x41
#define KEY_J 0x42
#define KEY_K 0x43
#define KEY_L 0x44
#define KEY_SEMICOLON_COLON 0x45
#define KEY_QUOTE_APOSTROPHE 0x46
#define KEY_RETURN 0x47
#define KEY_NUM_4 0x48
#define KEY_NUM_5 0x49
#define KEY_NUM_6 0x4a
#define KEY_NUM_PLUS 0x4b

// Row 4 - zxcv, cursors, num 123
#define KEY_LSHIFT 0x4c
// 0x4d skipped
#define KEY_Z 0x4e
#define KEY_X 0x4f
#define KEY_C 0x50
#define KEY_V 0x51
#define KEY_B 0x52
#define KEY_N 0x53
#define KEY_M 0x54
#define KEY_COMMA_LT 0x55
#define KEY_DOT_RT 0x56
#define KEY_SLASH 0x57
#define KEY_RSHIFT 0x58
#define KEY_UP 0x59
#define KEY_NUM_1 0x5a
#define KEY_NUM_2 0x5b
#define KEY_NUM_3 0x5c

// Row 5 - modifiers, space bar, bottom num row
#define KEY_CAPS 0x5d
#define KEY_LALT 0x5e
#define KEY_SPACE 0x5f
#define KEY_RALT 0x60
#define KEY_RCTRL 0x61
#define KEY_LEFT 0x62
#define KEY_DOWN 0x63
#define KEY_RIGHT 0x64
#define KEY_NUM_0 0x65
#define KEY_NUM_DOT 0x66
#define KEY_NUM_ENTER 0x67

// Row 7 - mouse
#define MOUSE_LEFT 0x70
#define MOUSE_MIDDLE 0x71
#define MOUSE_RIGHT 0x72
