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


// Acorn A3000 era system registers

////////// MEMC REGISTERS //////////

static void write_memc(
  int os_mode, int sound_dma, int video_dma, int dram_refresh,
  int high_rom_speed, int low_rom_speed, int page_size) {

  // 0000 0011
  // 011X 111X
  // XX0<os mode> <sound dma enable> <video dma enable> <dram refresh:2>
  // <high rom;2> <low rom:2> <page size:2> XX
  *((volatile uint32_t *)(0x036E0000L
    + ((uint32_t)(os_mode & 1) << 12)
    + ((uint32_t)(sound_dma & 1) << 11)
    + ((uint32_t)(video_dma & 1) << 10)
    + ((uint32_t)(dram_refresh & 3) << 8)
    + ((uint32_t)(high_rom_speed & 3) << 6)
    + ((uint32_t)(low_rom_speed & 3) << 4)
    + ((uint32_t)(page_size & 3) << 2)
  )) = 0;
}

////////// VIDC REGISTERS //////////

// Writes to anywhere in 0x3400000-0x35FFFFF activate the ~VIDW output from MEMC
// volatile uint32_t* VIDCR = (uint32_t *)0x3400000L;
#define VIDCR (*((volatile uint32_t *)0x3400000L))

// Screen memory pointer
#define SCREEN ((volatile uint8_t *)0x2000000)

