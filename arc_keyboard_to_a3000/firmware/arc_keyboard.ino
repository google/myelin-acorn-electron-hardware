/*
 * A3000 keyboard header LK3:
 *
 * 1 - reset -- connect to pin 4
 * 2 - NC (12V on A310)
 * 3 - GND -- connect to GND
 * 4 - 5V -- connect to RAW
 * 5 - KIN / Krx* (data from keyboard) -- connect to pin 0 (RXI)
 * 6 - KOUT / Ktx* (data to keyboard) -- connect to pin 1 (TXO)
 *
 * Note that the pin numbers on LK3 match the pin numbers on the DIN plug.
 *
 */

#include <SoftwareSerial.h>
#include "keyboard.h"

#define PIN_RESET 4

#define USE_SOFTWARE_SERIAL

#ifdef USE_SOFTWARE_SERIAL
// Inverted logic (idle low)
#define PIN_TX 8
#define PIN_RX 9
SoftwareSerial KBSerial(PIN_RX, PIN_TX, true);
#else
// Hardware serial with normal logic (idle high)
// TX = pin 1, RX = pin 0
#define KBSerial Serial1
#endif

// Send byte to keyboard -- callback from keyboard.cc
void keyboard_tx(uint8_t c) {
    if (c < 0xfd && Serial.dtr()) {
        // Output debug info but not during initial handshake, otherwise
        // SoftwareSerial will be too slow to catch the keyboard's response
        Serial.print("KB TX: ");
        Serial.println(c, HEX);
    }
    KBSerial.write(c);
}

// Receive byte from keyboard -- callback from keyboard.cc
uint8_t keyboard_rx() {
    uint8_t c = KBSerial.read();
    if (c < 0xfd && Serial.dtr()) {
        // Output debug info but not during initial handshake, otherwise
        // SoftwareSerial will be too slow to catch the keyboard's response
        Serial.print("KB RX: ");
        Serial.println(c, HEX);
    }
    return c;
}

// Check if a byte has been received from the keyboard -- callback from keyboard.cc
bool keyboard_data_available() {
    return KBSerial.available();
}

// Initialize keyboard serial port -- callback from keyboard.cc
void keyboard_hw_init() {
    // Init hardware serial on pins 0, 1
    // 8 data bits, 1 start bit, 2 stop bits
#ifdef USE_SOFTWARE_SERIAL
    // SoftwareSerial doesn't have the stop bit option --
    // we need to be careful to not write too fast
    KBSerial.begin(31250);
#else
    KBSerial.begin(31250, SERIAL_8N2);
#endif
}

// Key pressed -- callback from keyboard.cc
void keyboard_keydown(uint8_t keycode) {
    Serial.print("Key down: ");
    Serial.println(keycode, HEX);
}

// Key released -- callback from keyboard.cc
void keyboard_keyup(uint8_t keycode) {
    Serial.print("Key up: ");
    Serial.println(keycode, HEX);
}

// Mouse moved -- callback from keyboard.cc
void keyboard_mousemove(int mouse_dx, int mouse_dy) {
    Serial.print("Mouse move: ");
    Serial.print(mouse_dx);
    Serial.print(", ");
    Serial.println(mouse_dy);
}

void setup() {
    // USB serial port
    Serial.begin(9600);

    // Init reset pin
    pinMode(PIN_RESET, INPUT_PULLUP);

    // And start up the keyboard
    keyboard_init();
}

// Timestamp when RESET first noticed low
static long reset_down_millis = 0;

// Registered state of reset button
static bool reset_state = false;

void loop() {
    // This will call the keyboard_* functions above
    keyboard_poll();

    static long last_leds = 0;
    static int keyboard_which_led = 0;
    if (millis() - last_leds > 1000) {
        last_leds = millis();
        if (keyboard_state >= KEYBOARD_IDLE) {
            keyboard_which_led = (keyboard_which_led + 1) % 3;
            keyboard_set_leds(keyboard_which_led == 0, keyboard_which_led == 1, keyboard_which_led == 2);
        }
    }

    // Check reset line
    int reset = digitalRead(PIN_RESET);
    if (reset == HIGH) {
        // Reset not pressed
        if (reset_state) {
            Serial.println("RESET released");
            keyboard_init();
        }
        reset_down_millis = 0;
        reset_state = false;
    } else if (reset_down_millis == 0) {
        // Reset just pressed; debounce
        reset_down_millis = millis();
    } else if (!reset_state && millis() - reset_down_millis > 30) {
        // Down for 30 ms
        reset_state = true;
        Serial.println("RESET pressed");
    }
}
