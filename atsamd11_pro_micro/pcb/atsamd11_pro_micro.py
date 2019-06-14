#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ------------------
# atsamd11_pro_micro
# ------------------

# by Phillip Pearson

# A breakout board for the tiny Atmel ATSAMD11C chip, in the form factor of
# the Sparkfun Pro Micro, so I can plug it in to my existing designs without
# having to reroute anything.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Micro USB socket
micro_usb = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:micro_usb_b_smd_molex",
    identifier="USB",
    value="usb",
    desc="Molex 1050170001 (Digikey WM1399CT-ND) surface mount micro USB socket with mounting holes.",
    pins=[
        Pin(1, "V", ["5V"]),
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "ID", ["USB_ID"]),
        Pin(5, "G", ["GND"]),
    ],
)

# SWD header for programming and debug
swd = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch1.27mm_SMD",
    identifier="SWD",
    value="swd",
    pins=[
        # Pin numbers zig-zag:
        # 1 VCC  2 SWDIO
        # 3 GND  4 SWCLK
        # 5 GND  6 NC
        # 7 NC   8 NC
        # 9 NC  10 /RESET
        Pin(1, "VTref", ["3V3"]),
        Pin(2, "SWDIO", ["SWDIO"]),
        Pin(3, "GND", ["GND"]),
        Pin(4, "SWCLK", ["SWCLK"]),
        Pin(5, "GND", ["GND"]),
        Pin(6, "TXD", ["mcu_TXD"]),
        Pin(7, "NC"),
        Pin(8, "RXD", ["mcu_RXD"]),
        Pin(9, "GND", ["GND"]),
        Pin(10, "RESET", ["mcu_RESET"]),
    ],
)

# The ATSAMD11C chip (tiny SO-14 version)
mcu = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="MCU",
    value="atsamd11c",
    desc="IC ARM MCU; https://www.digikey.com/product-detail/en/microchip-technology/ATSAMD11C14A-SSUT/ATSAMD11C14A-SSUTCT-ND",
    pins=[
        # 14 pins: 2 for power, 3 for reset/swd, 2 for USB, leaving 7 GPIO.

        # The standalone_programmer board uses 13 GPIOs, but we can double up some of them.
        # Minimal CPLD comms requires 6 pins: TCK, TDI+MOSI, TDO, TMS/SCK, MISO, /SS

        # The 14-pin SO doesn't give us much choice for SERCOMs.  Only SERCOM0 is fully brought out.

        Pin( 1, "PA05", ["mcu_SS"]),  # sercom0.1/0.2
        Pin( 2, "PA08", ["mcu_MOSI_TDI"]),  # sercom0.2/1.2
        Pin( 3, "PA09", ["mcu_SCK_TMS"]),  # sercom0.3/1.3
        Pin( 4, "PA14", ["mcu_MISO"]),  # sercom0.0/2.0
        Pin( 5, "PA15", ["mcu_GPIO_D18_TDO"]),  # sercom0.1/2.1 == JTAG TDO
        Pin( 6, "PA28_nRESET", ["mcu_RESET"]),
        Pin( 7, "PA30", ["SWCLK"]),
        Pin( 8, "PA31", ["SWDIO"]),
        Pin( 9, "PA24", ["USBDM"]),
        Pin(10, "PA25", ["USBDP"]),
        Pin(11, "GND", ["GND"]),
        Pin(12, "VDD", ["3V3"]),
        Pin(13, "PA02", ["mcu_GPIO_D20_TCK"]),  # only gpio == JTAG TCK
        Pin(14, "PA04", ["mcu_GPIO_D8_nSD_SEL"]),  # sercom0.2/0.0 == /SD_SEL
    ],
)
mcu_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C1")
# SAM D11 has an internal pull-up, so this is optional
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R1")
# The SAM D11 datasheet says a 1k pullup on SWCLK is critical for reliability
mcu_swclk_pullup = myelin_kicad_pcb.R0805("1k", "SWCLK", "3V3", ref="R2")

# # The ATSAMD11D chip (larger SO-20 version, which I'll probably never use because ATSAMD21 is better and smaller)
# mcu = myelin_kicad_pcb.Component(
#     footprint="Housings_SOIC:SOIC-20W_7.5x12.8mm_Pitch1.27mm",
#     identifier="MCU",
#     value="atsamd11d",
#     pins=[
#         Pin(1, "PA05", [""]),
#         Pin(2, "PA06", [""]),
#         Pin(3, "PA07", [""]),
#         Pin(4, "PA08", [""]),
#         Pin(5, "PA09", [""]),
#         Pin(6, "PA14", [""]),
#         Pin(7, "PA15", [""]),
#         Pin(8, "PA16", [""]),
#         Pin(9, "PA22", [""]),
#         Pin(10, "PA23", [""]),
#         Pin(11, "PA28_nRESET", ["mcu_RESET"]),
#         Pin(12, "PA30", ["SWCLK"]),
#         Pin(13, "PA31", ["SWDIO"]),
#         Pin(14, "PA24", ["USBDM"]),
#         Pin(15, "PA25", ["USBDP"]),
#         Pin(16, "GND", ["GND"]),
#         Pin(17, "VDD", ["3V3"]),
#         Pin(18, "PA02", [""]),
#         Pin(19, "PA03", [""]),
#         Pin(20, "PA04", [""]),
#     ],
# )
# mcu_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C?")
# mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R?")

# 3V3 regulator, because this chip doesn't run on 5V
regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="U?",
    value="MCP1700T-3302E/MB",
    desc="IC LDO 3.3V regulator; https://www.digikey.com/products/en?keywords=MCP1700T3302EMBCT-ND",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C2")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C3")

# Pro Micro footprint
pro_micro = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:pro_micro",
    # footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="PRO",
    value="Pro Micro 5V",
    pins=[
        Pin( 1, "D1_TX_PD3",        ),
        Pin( 2, "D0_RX_PD2",        ),
        Pin( 3, "GND",              ["GND"]),
        Pin( 4, "GND",              ["GND"]),
        Pin( 5, "D2_SDA_PD1",       ),
        Pin( 6, "D3_SCL_OC0B_PD0",  ),
        Pin( 7, "D4_A6_PD4",        ),
        Pin( 8, "D5_nOC4A_PC6",     ),
        Pin( 9, "D6_A7_OC4D_PD7",   ),
        Pin(10, "D7_PE6",           ),
        Pin(11, "D8_A8_PB4",        ["mcu_GPIO_D8_nSD_SEL"]),  # /SD_SEL
        Pin(12, "D9_A9_nOC4B_PB5",  ["mcu_SS"]),   # /SS
        Pin(13, "D10_A10_OC4B_PB6", ),
        Pin(14, "D16_MOSI_PB2",     ["mcu_MOSI_TDI"]), # SPI (shared with JTAG)
        Pin(15, "D14_MISO_PB3",     ["mcu_MISO"]),     # SPI
        Pin(16, "D15_SCK_PB1",      ["mcu_SCK_TMS"]),  # SPI (shared with JTAG)
        Pin(17, "D18_A0_PF7",       ["mcu_GPIO_D18_TDO"]), # JTAG TDO
        Pin(18, "D19_A1_PF6",       ["mcu_SCK_TMS"]),  # JTAG (shared with SPI)
        Pin(19, "D20_A2_PF5",       ["mcu_GPIO_D20_TCK"]), # JTAG TCK
        Pin(20, "D21_A3_PF4",       ["mcu_MOSI_TDI"]), # JTAG (shared with SPI)
        Pin(21, "VCC",              ["3V3"]),
        Pin(22, "RST",              ["mcu_RESET"]),
        Pin(23, "GND",              ["GND"]),
        Pin(24, "VRAW",             ["5V"]),
    ],
)

# Ground plane stapling vias
for n in range(15):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

myelin_kicad_pcb.dump_netlist("atsamd11_pro_micro.net")
