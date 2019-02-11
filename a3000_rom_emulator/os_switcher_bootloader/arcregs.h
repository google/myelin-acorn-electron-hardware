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

#define REG_ADDR(addr) (*((volatile uint32_t *)(addr)))

////////// MEMC REGISTERS //////////

static void write_memc(
  int os_mode, int sound_dma, int video_dma, int dram_refresh,
  int high_rom_speed, int low_rom_speed, int page_size) {

  // 0000 0011
  // 011X 111X
  // XX0<os mode> <sound dma enable> <video dma enable> <dram refresh:2>
  // <high rom;2> <low rom:2> <page size:2> XX
  REG_ADDR(0x036E0000L
    + ((uint32_t)(os_mode & 1) << 12)
    + ((uint32_t)(sound_dma & 1) << 11)
    + ((uint32_t)(video_dma & 1) << 10)
    + ((uint32_t)(dram_refresh & 3) << 8)
    + ((uint32_t)(high_rom_speed & 3) << 6)
    + ((uint32_t)(low_rom_speed & 3) << 4)
    + ((uint32_t)(page_size & 3) << 2)
  ) = 0;
}

////////// VIDC REGISTERS //////////

// Writes to anywhere in 0x3400000-0x35FFFFF activate the ~VIDW output from MEMC
// volatile uint32_t* VIDCR = (uint32_t *)0x3400000L;
#define VIDCR REG_ADDR(0x3400000L)

// Screen memory pointer
#define SCREEN ((volatile uint8_t *)0x2000000)

////////// IOC REGISTERS //////////

// IOC, unlike MEMC and VIDC, has both address and data connections, to La and D.

#define IOC_BASE 0x3000000
// La21 = IOC CS
#define IOC_CS (1<<21)
// La20:19 = IOC T (speed select: 0=slow, 1=med, 2=fast, 3=sync)
#define IOC_T(v) (((v) & 3) << 19)
#define IOC_T_FAST IOC_T(2)
// LA18:16 = IOC B (bank select: 0=IOC internal)
#define IOC_B(v) (((v) & 7) << 16)
#define IOC_B_INTERNAL IOC_B(0)
// La6:2 = IOC A

// IOC internal registers.
// Note that when writing to IOC, D23:16 are connected to Bd7:0, so everything needs
// to be left-shifted 16 bits.
#define IOC_REG(addr) REG_ADDR(IOC_BASE | IOC_CS | IOC_T_FAST | IOC_B_INTERNAL | ((addr) & 0x7C))

// Control register
#define IOC_CTRL          IOC_REG(0x00)
// KART serial TX/RX
#define IOC_SERIAL        IOC_REG(0x04)
#define IOC_SERIAL_TX(v) do { IOC_SERIAL = (v) << 16; } while (0)

// IRQ A
#define IOC_IRQ_STATUS_A  IOC_REG(0x10)
#define IOC_IRQ_STATUS_A_TM1 (1 << 6)
#define IOC_TM1 (IOC_IRQ_STATUS_A & IOC_IRQ_STATUS_A_TM1)
#define IOC_IRQ_STATUS_A_TM0 (1 << 5)
#define IOC_TM0 (IOC_IRQ_STATUS_A & IOC_IRQ_STATUS_A_TM0)
#define IOC_IRQ_STATUS_A_POR (1 << 4)
#define IOC_IRQ_STATUS_A_IR  (1 << 3)
#define IOC_IRQ_STATUS_A_TF  (1 << 2)
#define IOC_IRQ_STATUS_A_TL7 (1 << 1)
#define IOC_IRQ_STATUS_A_TL6 (1 << 0)

#define IOC_IRQ_REQUEST_A IOC_REG(0x14)

#define IOC_IRQ_MASK_A    IOC_REG(0x18)

// Bits are << 16 because this is a write-only register
#define IOC_IRQ_CLEAR     IOC_REG(0x14)
#define IOC_IRQ_CLEAR_TM1 ((1 << 6) << 16)
#define IOC_CLEAR_TM1()   do { IOC_IRQ_CLEAR = IOC_IRQ_CLEAR_TM1; } while (0)
#define IOC_IRQ_CLEAR_TM0 ((1 << 5) << 16)
#define IOC_CLEAR_TM0()   do { IOC_IRQ_CLEAR = IOC_IRQ_CLEAR_TM0; } while (0)
#define IOC_IRQ_CLEAR_POR ((1 << 4) << 16)
#define IOC_IRQ_CLEAR_IR  ((1 << 3) << 16)
#define IOC_IRQ_CLEAR_TF  ((1 << 2) << 16)

// IRQ B
#define IOC_IRQ_STATUS_B  IOC_REG(0x20)
#define IOC_IRQ_STATUS_B_TX_EMPTY (1 << 6)
#define IOC_TX_EMPTY (IOC_IRQ_STATUS_B & IOC_IRQ_STATUS_B_TX_EMPTY)
#define IOC_IRQ_STATUS_B_RX_FULL (1 << 7)
#define IOC_RX_FULL (IOC_IRQ_STATUS_B & IOC_IRQ_STATUS_B_RX_FULL)
#define IOC_IRQ_REQUEST_B IOC_REG(0x24)
#define IOC_IRQ_MASK_B    IOC_REG(0x28)

// FIRQ
#define IOC_FIRQ_STATUS   IOC_REG(0x30)
#define IOC_FIRQ_REQUEST  IOC_REG(0x34)
#define IOC_FIRQ_MASK     IOC_REG(0x38)

// Timer 0: general purpose interval timer
#define IOC_TIMER0_LOW    IOC_REG(0x40)
#define IOC_TIMER0_HIGH   IOC_REG(0x44)
#define IOC_TIMER0_GO     IOC_REG(0x48)
#define IOC_TIMER0_LATCH  IOC_REG(0x4c)
#define SETUP_IOC_TIMER0(ticks) do { \
    IOC_TIMER0_HIGH = ((ticks) & 0xFF00) << 8; \
    IOC_TIMER0_LOW = ((ticks) & 0xFF) << 16; \
  } while (0)

// Timer 1: general purpose interval timer
#define IOC_TIMER1_LOW    IOC_REG(0x50)
#define IOC_TIMER1_HIGH   IOC_REG(0x54)
#define IOC_TIMER1_GO     IOC_REG(0x58)
#define IOC_TIMER1_LATCH  IOC_REG(0x5c)
#define IOC_TICKS_PER_US 2
#define SETUP_IOC_TIMER1(ticks) do { \
    IOC_TIMER1_HIGH = ((ticks) & 0xFF00) << 8; \
    IOC_TIMER1_LOW = ((ticks) & 0xFF) << 16; \
  } while (0)
#define IOC_DELAY_US(us) do { \
    SETUP_IOC_TIMER1((us) * IOC_TICKS_PER_US); \
    IOC_TIMER1_GO = 0; \
    IOC_CLEAR_TM1(); \
    while (!IOC_TM1); \
  } while (0)

// Timer 2: external BAUD pin
#define IOC_TIMER2_LOW    IOC_REG(0x60)
#define IOC_TIMER2_HIGH   IOC_REG(0x64)
#define IOC_TIMER2_GO     IOC_REG(0x68)
#define IOC_TIMER2_LATCH  IOC_REG(0x6c)

// Timer 3: KART BAUD rate
#define IOC_TIMER3_LOW    IOC_REG(0x70)
#define IOC_TIMER3_HIGH   IOC_REG(0x74)
#define IOC_TIMER3_GO     IOC_REG(0x78)
#define IOC_TIMER3_LATCH  IOC_REG(0x7c)
