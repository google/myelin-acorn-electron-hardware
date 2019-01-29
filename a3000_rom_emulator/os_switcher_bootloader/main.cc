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


// Main C++ entrypoint.  By the time this is called, we know the memory is
// working, and everything necessary to execute C++ code has been done.

#include <stdint.h>

#include "arcregs.h"

#define BUF_SIZE 512
uint32_t buf[BUF_SIZE];

void write_serial_tx(int b) __attribute__((section(".ramfunc")));
void write_serial_tx(int b) {
  volatile uint32_t *ptr = (volatile uint32_t *)(0x3fffff0L + ((b & 1) ? 4 : 0));
  // force compiler to read *ptr even though we don't care about the result
  asm volatile ("" : "=m" (*ptr) : "r" (*ptr));
}

int read_serial_rx() __attribute__((section(".ramfunc")));
int read_serial_rx() {
  return (*(volatile uint32_t *)0x3fffff8L) & 1;
}

__attribute__((section(".ramfunc")))
void write_serial_byte(uint8_t c) {
  volatile uint32_t *zero = (volatile uint32_t *)0x3fffff0L;
  volatile uint32_t *one = (volatile uint32_t *)0x3fffff4L;

  // TODO -- this is incomplete
  asm volatile (
    // send start bit
    "ldr r0, [%[zero]]\n\t"
    "" // wait
    // loop over 8 bits
    "mov r0, #0\n\t"
    "serial_tx_loop:\n\t"
    "and r1, %[data], #1\n\t"
    // next
    "add r0, r0, #1\n\t"
    "cmp r0, #8\n\t"
    "blo serial_tx_loop\n\t"
    // send stop bit
    "ldr r0, [%[one]]\n\t"
    "" // wait
    : // outputs
    : // inputs
      [zero] "r" (zero),
      [one] "r" (one),
      [data] "r" (c)
    : // clobbers
      "r0",
      "r1"  // TODO
    );
}

#define WIDTH 640
#define HEIGHT 256
#define WHITE 255
#define BLACK 0
#define SCREEN_ADDR(x, y) (SCREEN + (y) * WIDTH + (x))
#define SCREEN_END SCREEN_ADDR(WIDTH, HEIGHT)

__attribute__((section(".ramfunc")))
void reflect_serial_port() {
  volatile uint8_t *pixptr = SCREEN_END;
  while (1) {
    int b = read_serial_rx();
    write_serial_tx(b);
    // output to screen
    if (pixptr >= SCREEN_ADDR(0, 200)) {
      pixptr = SCREEN_ADDR(0, 100);
    }
    *pixptr++ = b ? WHITE : BLACK;
  }
}

extern "C" void main_program() {
  // set border color: 40:8 X:11 supreme:1 blue:4 green:4 red:4
  // VIDCR = 0x40001FFFL;  // white
  // VIDCR = 0x40000F00L;  // blue
  VIDCR = 0x40000777L;  // grey

  // Draw something on screen
  uint8_t c = 0;
  for (uint32_t y = 24; y < HEIGHT; ++y) {
    for (uint32_t x = 0; x < WIDTH; ++x) {
      SCREEN[y * WIDTH + x] = c++;
    }
  }

  // TODO init IOC and check keyboard

  // Bit-banged serial port
  // DEBUG: just echo RXD (cpld_MOSI, 0x3fffff8) back to TXD (cpld_MISO, 0x3fffff0 + (bit ? 4 : 0))
  // if (0) {
  //   volatile uint8_t *pixptr = SCREEN_END;
  //   volatile uint8_t *screen_mid = SCREEN_ADDR(0, HEIGHT/2), *screen_end = SCREEN_END;
  //   uint32_t readaddr = 0x3fffff8L, sendone = 0x3fffff4L, sendzero = 0x3fffff0L, black = 0, white = 136;  // 256=white 136=blue 21=red
  //   asm volatile(
  //     "next:\n\t"
  //     "  cmp %[pixptr], %[screen_end]\n\t"
  //     "  movhi %[pixptr], %[screen_mid]\n\t"
  //     "  ldr r0, [%[readaddr]]\n\t"
  //     "  tst r0, #1\n\t"
  //     "  beq one\n\t"
  //     "  ldr r1, [%[sendone]]\n\t"
  //     "  strb %[white], [%[pixptr]]\n\t"
  //     "  add %[pixptr], %[pixptr], #1\n\t"
  //     "  b next\n\t"
  //     "one:\n\t"
  //     "  ldr r1, [%[sendzero]]\n\t"
  //     "  strb %[black], [%[pixptr]]\n\t"
  //     "  add %[pixptr], %[pixptr], #1\n\t"
  //     "  b next\n\t"
  //     : [pixptr] "+r" (pixptr)
  //     : [readaddr] "r" (readaddr),
  //       [sendone] "r" (sendone),
  //       [sendzero] "r" (sendzero),
  //       [screen_end] "r" (screen_end),
  //       [screen_mid] "r" (screen_mid),
  //       [black] "r" (black),
  //       [white] "r" (white)
  //     : "r0", "r1");
  // }
  reflect_serial_port();
}
