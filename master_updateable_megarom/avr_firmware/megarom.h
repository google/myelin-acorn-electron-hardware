// Copyright 2018 Google LLC
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


// Definitions shared between megarom.ino and sst39sf0x0.cpp

#include <SPI.h>

// We use the standard SPI port, plus one GPIO for /SS
#define SPI_SS_PIN 10

// values for the largest part in the series, SST39SF040
#define CHIP_SIZE (512 * 1024L)
#define SECTOR_SIZE (4096L)
#define SECTOR_MASK ((CHIP_SIZE - 1) & ~(SECTOR_SIZE - 1))

extern uint8_t identify_chip();
extern uint32_t chip_size();
extern uint8_t read_byte(uint32_t address);
extern uint8_t read_byte_and_unlock(uint32_t address);
extern void erase_sector(uint32_t address);
extern void program_byte(uint32_t address, uint8_t data);
