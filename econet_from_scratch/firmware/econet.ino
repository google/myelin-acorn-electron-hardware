// Copyright 2017 Google Inc.
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

// For pinPeripheral(), so we can change PINMUX
#include "wiring_private.h"

// For libxsvf, so we can program the CPLD
#include "libxsvf.h"

// For libcrc, so we can calculate the CCITT CRC16
extern "C" {
#include "checksum.h"
}

// This code is for the ATSAMD21E18A onboard an econet_from_scratch PCB.
// Functions provided:
// - USB serial interface for all control
// - USB SVF+JTAG interface to program the CPLD
// - Econet clock generation (200kHz with 20% duty cycle)
// - CPLD clock generation (24MHz)
// - USB<->Econet frames (TODO read up on AUN)

// Pinout:

// Pin assignments from the Adafruit Circuit Playground Express (ATSAMD21G18A)
// are used here.  Be careful mapping these to actual pins, because the G18A and
// our E18A have different pinouts.

// Mapping: A(x) = D(x+14), e.g. A0 = D14 and A10 = D24

// CPLD JTAG port

// PA04 - D24 / A10
#define TDO_PIN 24
// PA06 - D16 / A2
#define TMS_PIN 16
// PA05 - D15 / A1
#define TCK_PIN 15
// PA07 - D17 / A3
#define TDI_PIN 17

// CPLD comms


// PA08 - D35 - serial_cpld_to_mcu (RX2)
#define PIN_SERIAL_CPLD_TO_MCU 35
// PA09 - D23 - serial_buffer_empty
#define PIN_SERIAL_BUFFER_EMPTY 23
// PA10 - D34 - outputting_frame
#define PIN_OUTPUTTING_FRAME 34
// PA11 - D22 - mcu_is_transmitting
#define PIN_MCU_IS_TRANSMITTING 22
// PA14 - D5 - serial_mcu_to_cpld (TX2)
#define PIN_SERIAL_MCU_TO_CPLD 5
// PA15 - D7 - clock_24m (XCK2)
#define PIN_CLOCK_24M 7
// PA16 - D30 - drive_econet_clock
#define PIN_DRIVE_ECONET_CLOCK 30
// PA17 - D13
#define PIN_ECONET_CLOCK_FROM_MCU 13
// PA18 - not assigned to an Arduino pin
// PA19 - not assigned to an Arduino pin
// PA22 - D36
// PA23 - D25

//#define NOISY

// libxsvf (xsvftool-arduino) entry point
extern void arduino_play_svf(int tms_pin, int tdi_pin, int tdo_pin, int tck_pin, int trst_pin);

void setup() {
  // Set pin directions for CPLD JTAG.  This board doesn't
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, OUTPUT);
	digitalWrite(TDI_PIN, HIGH);
  pinMode(TMS_PIN, OUTPUT);
	digitalWrite(TMS_PIN, HIGH);
  pinMode(TCK_PIN, OUTPUT);
	digitalWrite(TCK_PIN, LOW);

  // Set up USB serial port
  Serial.begin(9600);

  // Initialize SERCOM2 as UART at max speed (we'll switch to USRT later)
  sercom2.initUART(UART_INT_CLOCK, SAMPLE_RATE_x8, 3000000ul);

  // Set up 9-bit frame type
  sercom2.initFrame(UART_CHAR_SIZE_9_BITS,
                    LSB_FIRST,
                    SERCOM_NO_PARITY,
                    SERCOM_STOP_BIT_1);

  // Configure pads within SERCOM2
  // RXD = PA08 = SERCOM2/PAD[0] (rx can be pad 0, 1, 2, 3)
  // TXD = PA14 = SERCOM2/PAD[2] (tx can be pad 0, 2)
  // XCK = PA15 = SERCOM2/PAD[3] (valid: xck=1 + tx=0, or xck=3 + tx=2)
  sercom2.initPads(UART_TX_PAD_2, SERCOM_RX_PAD_0);

  // Configure pinmux
  // RXD = PA08 = option D / SERCOM-ALT
  pinPeripheral(PIN_SERIAL_CPLD_TO_MCU, PIO_SERCOM_ALT);
  // TXD = PA14 = option C / SERCOM
  pinPeripheral(PIN_SERIAL_MCU_TO_CPLD, PIO_SERCOM);
  // XCK = PA15 = option C / SERCOM
  pinPeripheral(PIN_CLOCK_24M, PIO_SERCOM);

  // Switch to USRT
  SERCOM2->USART.CTRLA.reg |=
    SERCOM_USART_CTRLA_MODE(1) |  // internal clock
    SERCOM_USART_CTRLA_CMODE |  // synchronous
    SERCOM_USART_CTRLA_CPOL;  // data valid on rising XCK edge

  // Configure clock divider
  // fbaud = fref(2 * (BAUD + 1))
  // SERCOM2->USART.BAUD.reg = 0;  // 24 MHz
  SERCOM2->USART.BAUD.reg = 1;  // 12 MHz

  // Disable all the interrupts, because Arduino won't handle them properly
  SERCOM2->USART.INTENCLR.reg = 0xFF;

  // Clear interrupt flags as well, just in case
  SERCOM2->USART.INTFLAG.reg = 0xFF;

  // And we're ready to go!
  sercom2.enableUART();

  // Initialize timer/counter to generate 200kHz PWM w/ 20% duty cycle
  // divide main clock by 48 to get 1MHz, then set transitions at 0/1/5
  //TODO verify this
  //TODO we may be able to just kick this off with an analogWrite, then change CC[1] and PER

  // Enable clock for TCC2
  GCLK->CLKCTRL.reg = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCM_TCC2_TC3);
  while (GCLK->STATUS.bit.SYNCBUSY == 1);

  // Set pin function to TCC2/WO[1]
  pinPeripheral(PIN_ECONET_CLOCK_FROM_MCU, PIO_TIMER);

  // Disable
  TCC2->CTRLA.bit.ENABLE = 0;
  while (TCC2->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);
  // Normal PWM
  TCC2->WAVE.reg |= TCC_WAVE_WAVEGEN_NPWM;
  while (TCC2->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);
  // Set compare channel to 1us (48 clocks)
  TCC2->CC[1].reg = 48;
  while (TCC2->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);
  // Set PER to 5us (5 * 48 clocks)
  TCC2->PER.reg = 5 * 48;
  while (TCC2->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);
  // Enable
  TCC2->CTRLA.bit.ENABLE = 1;
  while (TCC2->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);

  // Set econet clock pin directions
  // pinMode(PIN_ECONET_CLOCK_FROM_MCU, OUTPUT);
  // digitalWrite(PIN_ECONET_CLOCK_FROM_MCU, HIGH);
  pinMode(PIN_DRIVE_ECONET_CLOCK, OUTPUT);
  digitalWrite(PIN_DRIVE_ECONET_CLOCK, HIGH);

  // CPLD runs in transmit mode when we drive this high
  pinMode(PIN_MCU_IS_TRANSMITTING, OUTPUT);
  digitalWrite(PIN_MCU_IS_TRANSMITTING, LOW);

  // CPLD drives this high when we can write to it
  pinMode(PIN_SERIAL_BUFFER_EMPTY, INPUT);
}

uint8_t serial_get_uint8() {
  while (!Serial.available());
  return (uint8_t)Serial.read();
}

uint16_t serial_read_addr() {
  uint16_t addr = (uint16_t)serial_get_uint8() << 8;
  addr |= (uint16_t)serial_get_uint8();
  return addr;
}

/* CRC calculation:

polynomial = x^16 + x^12 + x^5 + 1
-> 1000 1000 0001 0000
or 0001 0000 0010 0001 <-- CRC-CCITT
transmitter and receiver polynomial registers are initialized to all '1's prior to calculation
FCS = complement of remainder after calculating FCS on all bits of message
receiver performs FCS calculation on message + FCS, and result should be F0B8.

Using libcrc to do this.  Some notes:

https://stardot.org.uk/forums/viewtopic.php?p=125428#p125428
"It looks as though the 68B54 chip is specified for use in a big endian system (with D0 being the most significant bit), but Acorn have wired it up little endian (with D0 being the least significant bit). This means that, in the CRC calculation, all the bytes need to be bit-flipped before adding, and the result needs to be flipped back again!"

Probably need to snoop some packets on the wire to see how this works!

*/

// Disable USB serial commands (CPLD programming etc) by commenting this out:
#define ENABLE_USB_SERIAL

uint16_t buffer[256];
uint16_t buf_pos = 0;
uint16_t buf_crc = CRC_START_CCITT_FFFF;

void loop() {

  // Forward bytes from CPLD through to USB serial port
  while (sercom2.availableDataUART()) {
    uint16_t rd = SERCOM2->USART.DATA.bit.DATA;  // sercom2.readDataUART()
    if (rd == 0x17E) {
      if (buf_pos) {
        // We just got a frame; dump it to the serial port
        Serial.print("Frame:");
        for (uint16_t i = 0; i < buf_pos; ++i) {
          Serial.print(" ");
          if (buffer[i] < 16) Serial.print("0");
          Serial.print(buffer[i], HEX);
        }
        Serial.print("; CRC ");
        Serial.print(buf_crc, HEX);
        if (buf_crc == 0xf0b8) {
          Serial.print(" (ok)");
        } else {
          Serial.print(" (BAD)");
        }
        Serial.print("\r\n");
        buf_pos = 0;  // Ready for next frame
        buf_crc = CRC_START_CCITT_FFFF;  // Reset CRC
      } else {
        // Ignore -- repeated flag byte
      }
    } else {
      // Data byte
      if (buf_pos < 250) {
        buffer[buf_pos++] = rd;
        buf_crc = update_crc_econet(buf_crc, (uint8_t)rd);
      }
    }
  }

  // static uint8_t econet_clock_state = 0;
  // digitalWrite(PIN_ECONET_CLOCK_FROM_MCU, econet_clock_state ? HIGH : LOW);
  // econet_clock_state = !econet_clock_state;

  // static uint8_t serial_state = 0;
  // static unsigned long serial_state_time = 0;
  static int chars_to_write = 0, is_first_char = 0;
  static unsigned long last_char_write = 0;

  // wait 50ms between frames
  // if (!chars_to_write && (last_char_write - millis()) > 50) {
  //   chars_to_write = 20;
  //   is_first_char = 1;
  // }

  if (sercom2.isDataRegisterEmptyUART()
      && digitalRead(PIN_SERIAL_BUFFER_EMPTY) == HIGH
      && chars_to_write > 0
  ) {
    // TODO drop PIN_MCU_IS_TRANSMITTING once we're done writing the packet
    // -- probably have to wait for PIN_OUTPUTTING_FRAME to go low
    digitalWrite(PIN_MCU_IS_TRANSMITTING, HIGH);
  //   serial_state = 1;
  //   serial_state_time = millis();
  // }
  // if (serial_state == 1 && millis() > serial_state_time + 1) {
    // sercom2.writeDataUART() casts our input to uint8_t, so we have
    // to go straight to the register here.
    chars_to_write --;
    // start and end with flag, and transmit lots of 0x42 in between
    SERCOM2->USART.DATA.reg = (is_first_char || !chars_to_write) ? (uint16_t)0x17E : (uint16_t)0x42;
    is_first_char = 0;
    last_char_write = millis();
  //   serial_state = 2;
  }
  // if (serial_state == 2 && millis() > serial_state_time + 11) {
  //   digitalWrite(PIN_MCU_IS_TRANSMITTING, LOW);
  //   serial_state = 3;
  // }
  // if (serial_state == 3 && millis() > serial_state_time + 21) {
  //   serial_state = 0;
  // }

#ifdef ENABLE_USB_SERIAL
  static uint8_t serial_active = 0;
  static unsigned long serial_active_when = 0;
  if (!Serial.dtr()) {
    if (serial_active) {
      serial_active = 0;
    }
  } else if (!serial_active) {
    // USB serial connection is active
    serial_active_when = millis();
    serial_active = 1;
  } else if (serial_active == 1 && millis() - serial_active_when > 10) {
    // Serial port should have settled by now
    Serial.println(SystemCoreClock);
    serial_active = 2;
  } else if (serial_active == 2) {
    // Serial port is actually open.
  }

  // turn it on and off to make sure the _DE input is functioning
  // static uint8_t econet_clock_drive = 0;
  // ++ econet_clock_drive;
  // if (econet_clock_drive == 10) {
  //   digitalWrite(PIN_DRIVE_ECONET_CLOCK, LOW);
  // } else if (econet_clock_drive == 20) {
  //   digitalWrite(PIN_DRIVE_ECONET_CLOCK, HIGH);
  //   econet_clock_drive = 0;
  // }

  if (Serial.available()) {
    int c = Serial.read();
    switch (c) {
      case 'C': {
        // program CPLD
        Serial.println("SEND SVF");
        arduino_play_svf(TMS_PIN, TDI_PIN, TDO_PIN, TCK_PIN, -1);
        Serial.println("SVF DONE");
        break;
      }
      case 'Z': {
        // USB test
        Serial.println("USB TEST");
        bool fail = false;
        for (uint32_t i = 0; i < 128 * 1024L; ++i) {
          // Serial.println(i);
          unsigned long now = millis();
          while (!Serial.available()) {
            if (millis() - now > 1000) {
              Serial.println("Failing b/c no input for 1000 ms");
              fail = true;
              break;
            }
          }
          if (fail) {
            Serial.println("fail");
            break;
          }

          Serial.write(Serial.read());
          if (i && !(i % 8192)) {
            // simulate delay every 8k
            delay(1000);
          }
        }
        Serial.println("TEST DONE");
        break;
      }
      default: {
        Serial.print("Unknown: ");
        Serial.println((char)c);
        break;
      }
    }
  }
#endif // ENABLE_USB_SERIAL

}
