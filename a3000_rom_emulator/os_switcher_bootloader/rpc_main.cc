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


// Main C++ entrypoint for Risc PC bootloader.

#include "arcflash.h"

// Decoded descriptor proto, from flash
arcflash_FlashDescriptor descriptor;

// Print a string to the screen using OS_Write0
void display_print(const char* s) {
#define BUF_LEN 500
  register char* ptr asm("r0") = (char*)s;
  char buf[BUF_LEN];

  // Replace \n with \r\n
  char* bptr = buf;
  while (*ptr && bptr < buf + BUF_LEN - 3) {
    if (*ptr == '\n') {
      *bptr++ = '\r';
    }
    *bptr++ = *ptr++;
  }
  *bptr = '\0';

  // Call OS_Write0 with ptr to s in r0
  ptr = buf;
  asm volatile(
    "swi 2\n\t"   // OS_Write0
    : "+r" (ptr)  // r0 = ptr to null terminated string, and
                  // will be replaced with ptr to byte after null.
  );
}

// Blocking char read using OS_ReadC
char os_readc() {
  register char c asm("r0");
  asm volatile(
    "swi 4\n\t"  // OS_ReadC
    : "+r" (c)   // r0 = char read
  );
  return c;
}

extern "C" void main_program() {
  display_printf("\n\n\n\nArcflash - http://myelin.nz/arcflash\n\n");

  parse_descriptor_and_print_menu(RPC_ROM_BASE, &descriptor);

  while (1) {
    char c = os_readc() | 32;
    if (c < 'a' || c > 'z') continue;
    
    display_printf("you pressed: %c\n", c);
  }

  while (1);
}
