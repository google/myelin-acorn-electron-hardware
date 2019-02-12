// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


// Functions to access the Archimedes keyboard
// TODO support Risc PC, which uses a PS/2 keyboard

#include "arcflash.h"

// Globals
int mouse_x = WIDTH / 2, mouse_y = HEIGHT / 2;

// Reset codes
#define HRST 0xff
#define RAK1 0xfe
#define RAK2 0xfd

// ARM->KB ping command: 4 data bits
#define RQPD(data) (0x40 | ((data) & 0x0f))
// KB->ARM echoed data from RQPD
#define PDAT(data) (0xe0 | ((data) & 0x0f))

// ARM->KB request ID
#define RQID 0x20
// KB->ARM keyboard ID
#define KBID(data) (0x80 | ((data) & 0x3f))

// KB->ARM Key down data
#define KDDA(data) (0xc0 | ((data) & 0x0f))
// KB->ARM Key up data
#define KUDA(data) (0xd0 | ((data) & 0x0f))
// ARM->KB request for mouse data
#define RQMP 0x22
// KB->ARM Mouse data
#define MDAT(data) ((data) & 0x7f)

// ARM->KB Ack first byte of a pair
#define BACK 0x3f
// ARM->KB Ack second byte and disable scanning
#define NACK 0x30
// Ack second byte and enable keyboard / disable mouse
#define SACK 0x31
// Ack second byte and disable keyboard / enable mouse
#define MACK 0x32
// Ack second byte and enable keyboard + mouse scanning
#define SMAK 0x33

// ARM->KB set LEDs
#define LEDS(scroll, num, caps) (((scroll) ? 4 : 0) | ((num) ? 2 : 0) | ((caps) ? 1 : 0))

// ARM->KB NOP
#define PRST 0x21

static enum keyboard_state_t {
    KEYBOARD_INIT = 0,
    KEYBOARD_RESET,
    KEYBOARD_RESET_1,
    KEYBOARD_RESET_2,
    KEYBOARD_IDLE,
    KEYBOARD_READING_DAT2
} keyboard_state = KEYBOARD_INIT;

// millis() last time we heard from the keyboard
static uint32_t keyboard_last_comms = 0;
static uint8_t keyboard_data[2];

void keyboard_init() {
    // Set up IOC TIMER3 to drive KART serial clock
    // From the VL86C410 databook: baud rate 31250 Hz is set with latch=1
    IOC_TIMER3_HIGH = 0;
    IOC_TIMER3_LOW = 1;
    IOC_TIMER3_GO = 0;

    // Send hardware reset
    IOC_SERIAL_TX(HRST);
    keyboard_state = KEYBOARD_RESET;
}

__attribute__((section(".ramfunc")))
void keyboard_set_state(keyboard_state_t state) {
    if (keyboard_state < KEYBOARD_IDLE && state >= KEYBOARD_IDLE) {
        display_goto(50, HEIGHT-8);
        display_print("KB OK");
    } else if (state < KEYBOARD_IDLE) {
        display_goto(50, HEIGHT-8);
        display_print("KB ??");
    }
    keyboard_state = state;
}

__attribute__((section(".ramfunc")))  // so this can run while ROM is inaccessible
void keyboard_poll() {
    if (!IOC_RX_FULL) {
        // Are we stalled in the reset process?
        if (keyboard_state < KEYBOARD_IDLE && ((millis() - keyboard_last_comms) > 1000)) {
            IOC_SERIAL_TX(HRST);
            keyboard_set_state(KEYBOARD_RESET);
            keyboard_last_comms = millis();
        }
        // Otherwise we're good
        return;
    }

    keyboard_last_comms = millis();

    // Delay half a bit (1e6 / 31250 / 2 = 16 us) to work around IOC bug
    IOC_DELAY_US(16);

    // Read keyboard serial port, which clears the RX_FULL flag
    uint8_t data = IOC_SERIAL;

    // See "Reset Protocol", A3000 TRM p14
    // Send HRST
    // Expect HRST from keyboard
    // Send RAK1
    // Expect RAK1
    // Send RAK2
    // Expect RAK2
    // Send SMAK (enable keyboard and mouse)

    // debug
    display_print_hex(keyboard_state);
    display_print(" ");
    display_print_hex(data);
    display_print(" ");


    // Handle reset commands at all times
    switch (data) {
        case HRST:
            if (keyboard_state == KEYBOARD_RESET) {
                IOC_SERIAL_TX(RAK1);
                keyboard_set_state(KEYBOARD_RESET_1);
            } else {
                IOC_SERIAL_TX(HRST);
                keyboard_set_state(KEYBOARD_RESET);
            }
            return;
        case RAK1:
            if (keyboard_state == KEYBOARD_RESET_1) {
                IOC_SERIAL_TX(RAK2);
                keyboard_set_state(KEYBOARD_RESET_2);
            } else {
                IOC_SERIAL_TX(HRST);
                keyboard_set_state(KEYBOARD_RESET);
            }
            return;
        case RAK2:
            if (keyboard_state == KEYBOARD_RESET_2) {
                IOC_SERIAL_TX(SMAK);
                keyboard_set_state(KEYBOARD_IDLE);
            } else {
                IOC_SERIAL_TX(HRST);
                keyboard_set_state(KEYBOARD_RESET);
            }
            return;
        default:
            // all unhandled states fall through to next switch
            break;
    }

    switch (keyboard_state) {
        case KEYBOARD_IDLE:
            // Can receive PDAT (single byte echo), KBID (single byte keyboard encoding ID),
            // or first byte of KDDA, KUDA, or MDAT.
            if ((data & 0xf0) == 0xe0) {
                // PDAT
                IOC_SERIAL_TX(SMAK);
                return;
            }
            if ((data & 0xc0) == 0x80) {
                // KBID
                IOC_SERIAL_TX(SMAK);
                return;
            }
            if ((data & 0xf0) == 0xc0 || (data & 0xf0) == 0xd0 || (data & 0x80) == 0) {
                // KDDA, KUDA, or MDAT byte 1
                keyboard_data[0] = data;
                IOC_SERIAL_TX(BACK);
                keyboard_set_state(KEYBOARD_READING_DAT2);
                return;
            }
            // Fall through to reset at end of function
            break;
        case KEYBOARD_READING_DAT2:
            // Receiving second byte of KDDA, KUDA, or MDAT.
            if ((data & 0xf0) == 0xc0 || (data & 0xf0) == 0xd0 || (data & 0x80) == 0) {
                // KDDA, KUDA, or MDAT byte 2
                keyboard_data[1] = data;
                IOC_SERIAL_TX(SMAK);
                keyboard_set_state(KEYBOARD_IDLE);

                if ((keyboard_data[0] & 0x80) == 0 && (keyboard_data[1] & 0x80) == 0) {
                    // MDAT: 2x7-bit mouse data.  Sign extend and add to our mouse position
                    mouse_x += ((int)keyboard_data[0] ^ 0x40) - 0x40;
                    mouse_y -= ((int)keyboard_data[1] ^ 0x40) - 0x40;
                    if (mouse_x < 0) mouse_x = 0;
                    if (mouse_x >= WIDTH) mouse_x = WIDTH - 1;
                    if (mouse_y < 0) mouse_y = 0;
                    if (mouse_y >= HEIGHT) mouse_y = HEIGHT - 1;
                    *SCREEN_ADDR(mouse_x, mouse_y) = WHITE;
                    return;
                }

                if ((keyboard_data[0] & 0xf0) == 0xc0 && (keyboard_data[1] & 0xf0) == 0xc0) {
                    // KDDA: 2x4-bit key down code
                    uint8_t keycode = ((keyboard_data[0] & 0x0f) << 4) | (keyboard_data[1] & 0x0f);
                    keyboard_keydown(keycode);
                    return;
                }

                if ((keyboard_data[0] & 0xf0) == 0xd0 && (keyboard_data[1] & 0xf0) == 0xd0) {
                    // KUDA: 2x4-bit key up code
                    uint8_t keycode = ((keyboard_data[0] & 0x0f) << 4) | (keyboard_data[1] & 0x0f);
                    keyboard_keyup(keycode);
                    return;
                }

                // Unknown or mismatched 2-byte code - fall through to reset
                display_print_hex(keyboard_state);
                display_print(" ");
                display_print_hex(data);
                display_print(" ");
            }
            // Fall through to reset at end of function
            break;
        default:
            // All unknown cases fall through to reset below
            break;
    }

    // Unknown case happened somewhere above: reset
    IOC_SERIAL_TX(HRST);
    keyboard_set_state(KEYBOARD_RESET);
}
