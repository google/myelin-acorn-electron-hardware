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

const char* foo = "this is a test";

#define BUF_SIZE 512
uint32_t buf[BUF_SIZE];

extern "C" void main_program() {
  // set border color to white: 40:8 X:11 supreme:1 blue:4 green:4 red:4
  // white = 0001 1111 1111 1111
  VIDCR = 0x40001FFFL;

  // TODO set up screen mode; presumably this involves allocating memory and setting up MEMC DMA

  // DEBUG some loops, to validate that text/rodata/data/bss have been linked properly:
  buf[0] = 0;
  uint32_t i = 1;
  for (; i < 15; ++i) {
    buf[i] = foo[i];
  }
  for (; i < BUF_SIZE; ++i) {
    buf[i] = buf[i-1] + 42;
  }

  // TODO draw something...

  // TODO init IOC and check keyboard
}
