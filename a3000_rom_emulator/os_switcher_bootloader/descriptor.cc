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


#include "arcflash.h"
#include "pb_decode.h"


void parse_descriptor_and_print_menu(uint32_t rom_base, arcflash_FlashDescriptor* desc) {
  // Descriptor is placed at the end of the first 384k of ROM space
  const uint32_t* descriptor_size = (uint32_t*)(rom_base + BOOT_ROM_SIZE - 4);
  // display_printf("descriptor size %08lx\n", *descriptor_size);

  if (*descriptor_size == 0xFFFFFFFFL) {
    display_printf("ERROR: descriptor size not found at 0x%08X - please reprogram flash.\n",
        (uint32_t)descriptor_size);
    while (1);  // Fatal error
  }

  const uint8_t* descriptor_ptr = (uint8_t*)(rom_base + BOOT_ROM_SIZE - 4 - *descriptor_size);
  // display_printf("descriptor at %08lx\n", (uint32_t)descriptor);

  pb_istream_t stream = pb_istream_from_buffer(descriptor_ptr, *descriptor_size);
  if (!pb_decode(&stream, arcflash_FlashDescriptor_fields, desc)) {
    display_printf("ERROR: Failed to decode %u-byte flash descriptor at 0x%08X - please reprogram flash.\n",
        *descriptor_size, (uint32_t)descriptor_ptr);
    while (1);  // Fatal error
  } else {
    char bank_key = 'A';
    // display_printf("hash %s\n", descriptor.hash_sha1);
    // display_printf("bank count %d\n", descriptor.bank_count);

    display_printf("Please select an operating system to boot:\n\n");
    for (int bank_id = 0; bank_id < desc->bank_count; ++bank_id, ++bank_key) {
      arcflash_FlashBank* bank = &desc->bank[bank_id];
      display_printf("    %c: %s [%dM]\n", bank_key, bank->bank_name, bank->bank_size/1048576);
      // display_goto(display_x, display_y+2);
    }

    display_printf("\nHit A-%c to select OS to switch to, then hit RESET to boot into it.\n"
                  "(Currently we have no serial RX so there's no way to confirm that the\n"
                  "flash bank has been selected.  Just wait a second, then hit RESET.)\n\n"
                  "Flash usage: %dk out of %dk; %dk free.\n\n",
                  bank_key-1,
                  (desc->flash_size - desc->free_space) / 1024,
                  desc->flash_size / 1024,
                  desc->free_space / 1024);
  }
}
