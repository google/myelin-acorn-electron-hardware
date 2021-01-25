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

#include <SPI.h>
#include <avr/power.h>

// This code is for the Pro Micro onboard a serial_sd_mcu PCB.
// It talks to the CPLD over SPI, and provides a USB serial interface.

// It also has some code from standalone_programmer/mcu/mcu.ino to support
// programming the CPLD, but this isn't wired up at the moment.

// Pinout:

// CPLD JTAG port

// TDO = D18 (PF7)
#define TDO_PIN 18
// TMS = D19 (PF6)
#define TMS_PIN 19
// TCK = D20 (PF5)
#define TCK_PIN 20
// TDI = D21 (PF4)
#define TDI_PIN 21

// CPLD SPI port

// Good to put this one on a PCINT pin, i.e. PB*.
// PB0-3 are the SPI port, leaving PB4=D8, PB5=D9, PB6=D10, PB7=D11.
#define cpld_INT 10
#define cpld_MOSI 16
#define cpld_MISO 14
#define cpld_SCK 15

// These two used to be A0/A1 so need to be moved on the Electron version
// before they'll work
#define cpld_SS 9
#define cpld_SD_SEL 8

// This is connected to the CPLD but unused in the BBC version
#define cpld_MISC1 6

//#define NOISY

void setup() {
  // For some reason the caterina bootloader on Pro Micro clones
  // doesn't always set the clock prescaler properly.
  clock_prescale_set(clock_div_1);

  // Set pullups for unused pins
  pinMode(cpld_MISC1, INPUT_PULLUP);

  // Set pin directions for CPLD JTAG
  pinMode(TDO_PIN, INPUT);
  pinMode(TDI_PIN, INPUT_PULLUP);
  pinMode(TMS_PIN, INPUT_PULLUP);
  // Ideally we would pull this down, but we don't want a conflict
  // with an attached JTAG probe
  pinMode(TCK_PIN, INPUT);
  // In future we'll set TDI, TMS, and TCK as outputs, set TDI=1 and
  // TMS=1, and pulse TCK 5 times to reset the CPLD.

  // Set up USB serial port
  Serial.begin(9600);

  // Set up CPLD SPI interface
  pinMode(cpld_INT, INPUT);
  pinMode(cpld_SS, OUTPUT);
  digitalWrite(cpld_SS, HIGH);
  pinMode(cpld_SD_SEL, OUTPUT);
  digitalWrite(cpld_SD_SEL, HIGH);  // HIGH = select fast serial port; LOW = select SD card
  SPI.begin();
  SPI.beginTransaction(SPISettings(16000000L, MSBFIRST, SPI_MODE0));

  // Unused as yet, but if we ever want to try to implement a serial port on the
  // CPLD, this should set up Timer4 to provide a 115200x4 clock on PC6/D5.  See
  // comments in serial_sd_adapter.vhd for more detail.

  // TCCR4A = 0x82;  // COM4A = b'10, FOC4A = 0, PWM4A = 1
  // TCCR4B = 0x01;  // No prescaling -- clock ==
  // TCCR4D = 0x00;  // Fast PWM
  // OCR4C = 139;  // Timer period = 64 MHz / 139 = 460431.65 Hz, i.e. 115107.91 Hz * 4
  // OCR4A = 139 / 2; // Clear OC4A around halfway through the clock cycle
}

void loop() {
  digitalWrite(cpld_SD_SEL, HIGH);  // Select fast serial port
  digitalWrite(cpld_SS, LOW);  // Initiate transfer

  // First byte is a status byte
  uint8_t avr_status =
    // bit 1 = 1 if we have a byte to send
    (Serial.available() ? 0x02 : 0x00)
    // bit 0 = 1 if we have buffer space
    | (Serial.availableForWrite() ? 0x01 : 0x00);

  uint8_t cpld_status = SPI.transfer(avr_status);
  // bit 0 of cpld_status = 1 if the cpld has buffer space
  // bit 1 of cpld_status = 1 if the cpld has a byte to send

  uint8_t avr_data = 0;
  if ((cpld_status & 0x01) && (avr_status & 0x02)) {
    // If the CPLD told us it has buffer space,
    // and we told it that we have a byte to send,
    // then send a byte.
    avr_data = (uint8_t)Serial.read();
  }

  uint8_t cpld_data = SPI.transfer(avr_data);
  if ((cpld_status & 0x02) && (avr_status & 0x01)) {
    // If the CPLD told us it has a byte to send,
    // and we told it we have buffer space, then
    // we just received a byte.
    Serial.write(cpld_data);
  }

  // Close transfer
  digitalWrite(cpld_SS, HIGH);
}
