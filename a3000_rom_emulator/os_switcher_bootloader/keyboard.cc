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
// Part of the Arcflash bootloader.

// TODO support Risc PC, which uses a PS/2 keyboard

// KEYBOARD HAL -- implement these when porting to a different system

#ifdef ARCFLASH

#include "arcflash.h"

// Arcflash: screen position for keyboard debug output
static int kb_display_x = 0, kb_display_y = HEIGHT-8;

// Send byte to keyboard
static void keyboard_tx(uint8_t c) {
    IOC_SERIAL_TX(c);
}

// Receive byte from keyboard
static uint8_t keyboard_rx() {
    // Delay half a bit (1e6 / 31250 / 2 = 16 us) to work around IOC bug
    IOC_DELAY_US(16);

    return IOC_SERIAL;
}

// Check if a byte has been received from the keyboard
static bool keyboard_data_available() {
    return IOC_RX_FULL;
}

// Initialize keyboard serial port
static void keyboard_hw_init() {
    // Set up IOC TIMER3 to drive KART serial clock
    // From the VL86C410 databook: baud rate 31250 Hz is set with latch=1
    IOC_TIMER3_HIGH = 0;
    IOC_TIMER3_LOW = 1;

    // Read receive line to clear any outstanding interrupt. This doesn't seem
    // to be necessary on my A3000, and for some reason prevents the keyboard
    // from working in Arculator, so it's commented out for now.  (And the
    // interrupt will be handled later by keyboard_poll() anyway).

    // (void)IOC_SERIAL;
}

#else // !ARCFLASH

// plat_keyboard.h should define millis()
#include "plat_keyboard.h"
#include "keyboard.h"

extern void keyboard_tx(uint8_t c);
extern uint8_t keyboard_rx();
extern bool keyboard_data_available();
extern void keyboard_hw_init();

#endif // !ARCFLASH

// PLATFORM INDEPENDENT KEYBOARD ROUTINES -- should work on all systems

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

// Global keyboard state
enum keyboard_state_t keyboard_state;

// millis() last time we heard from the keyboard
static uint32_t keyboard_last_comms = 0;
static uint8_t keyboard_data[2];

void keyboard_init() {
    keyboard_hw_init();

    // Send dummy byte to trigger HRST from keyboard
    keyboard_tx(0);

    // Set state to undetermined / initialization
    keyboard_state = KEYBOARD_INIT;
}

static void keyboard_set_state(keyboard_state_t state) {
#ifdef ARCFLASH
    if (keyboard_state < KEYBOARD_IDLE && state >= KEYBOARD_IDLE) {
        display_goto(0, kb_display_y);
        display_print("KB OK ");
    } else if (state < KEYBOARD_IDLE) {
        display_goto(0, kb_display_y);
        display_print("KB ?? ");
    }
    kb_display_x = display_x;
#endif // ARCFLASH
    keyboard_state = state;
}

void keyboard_set_leds(bool scroll, bool num, bool caps) {
    keyboard_tx(LEDS(scroll, num, caps));
}

void keyboard_poll() {
    if (!keyboard_data_available()) {
        // Are we stalled in the reset process?
        if (keyboard_state < KEYBOARD_IDLE && ((millis() - keyboard_last_comms) > 500)) {
            keyboard_tx(0);
            keyboard_set_state(KEYBOARD_INIT);
            keyboard_last_comms = millis();
        }
        // Otherwise we're good
        return;
    }

    keyboard_last_comms = millis();

    // Read keyboard serial port, which clears the RX_FULL flag
    uint8_t data = keyboard_rx();

    // See "Reset Protocol", A3000 TRM p14
    // Send HRST
    // Expect HRST from keyboard
    // Send RAK1
    // Expect RAK1
    // Send RAK2
    // Expect RAK2
    // Send SMAK (enable keyboard and mouse)

#ifdef ARCFLASH
    // debug
    if (kb_display_x > WIDTH-100) kb_display_x = 0;
    display_goto(kb_display_x, kb_display_y);
    display_printf("%x %x ", keyboard_state, data);
#endif // ARCFLASH

    // Handle reset commands at all times
    switch (data) {
        case HRST:
            if (keyboard_state == KEYBOARD_RESET) {
                keyboard_tx(RAK1);
                keyboard_set_state(KEYBOARD_RESET_1);
            } else {
                keyboard_tx(HRST);
                keyboard_set_state(KEYBOARD_RESET);
            }
            return;
        case RAK1:
            if (keyboard_state == KEYBOARD_RESET_1) {
                keyboard_tx(RAK2);
                keyboard_set_state(KEYBOARD_RESET_2);
            } else {
                keyboard_tx(HRST);
                keyboard_set_state(KEYBOARD_RESET);
            }
            return;
        case RAK2:
            if (keyboard_state == KEYBOARD_RESET_2) {
                keyboard_tx(SMAK);
                keyboard_set_state(KEYBOARD_IDLE);
            } else {
                keyboard_tx(HRST);
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
                keyboard_tx(SMAK);
                return;
            }
            if ((data & 0xc0) == 0x80) {
                // KBID
                keyboard_tx(SMAK);
                return;
            }
            if ((data & 0xf0) == 0xc0 || (data & 0xf0) == 0xd0 || (data & 0x80) == 0) {
                // KDDA, KUDA, or MDAT byte 1
                keyboard_data[0] = data;
                keyboard_tx(BACK);
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
                keyboard_tx(SMAK);
                keyboard_set_state(KEYBOARD_IDLE);

                if ((keyboard_data[0] & 0x80) == 0 && (keyboard_data[1] & 0x80) == 0) {
                    // MDAT: 2x7-bit mouse data.  Sign extend and add to our mouse position
                    int mouse_dx = ((int)keyboard_data[0] ^ 0x40) - 0x40;
                    int mouse_dy = ((int)keyboard_data[1] ^ 0x40) - 0x40;
                    keyboard_mousemove(mouse_dx, mouse_dy);
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
#ifdef ARCFLASH
                display_printf("%x %x", keyboard_state, data);
#endif // ARCFLASH
            }
            // Fall through to reset at end of function
            break;
        default:
            // All unknown cases fall through to reset below
            break;
    }

    // Unknown case happened somewhere above: reset
    keyboard_tx(HRST);
    keyboard_set_state(KEYBOARD_RESET);
}
