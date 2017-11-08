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

# ------------
# atsamd21_usb
# ------------

# by Phillip Pearson

# A breakout board for the ATSAMD21 MCU, with USB host and device functionality.

# - ATSAMD21 32-pin TQFP
# - SWD header and pullups
# - Power LED
# - Micro USB socket, 3v3 regulator + capacitors
# - USB-A host socket, crystal + capacitors
# - Pin headers: gnd/3v3/5v, gpios

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


mcu = myelin_kicad_pcb.Component(
    footprint="Housings_QFP:TQFP-32_7x7mm_Pitch0.8mm",
    identifier="MCU",
    value="ATSAMD21E18A",  # 256k flash, 32k sram, 32 pins
    pins=[
        # We use a 32.768kHz crystal and the 96MHz FDPLL with some massive
        # multiplier.  This seems a bit weird, but all the ATSAMD21 designs I
        # can find are clocked this way.  The FDPLL has an input divider, so it
        # should be possible to use an 8MHz input, but nobody seems to do that.
        Pin(1, "PA00/XIN32", ["XTAL_IN"]),
        Pin(2, "PA01/XOUT32", ["XTAL_OUT"]),
        Pin(3, "PA02/AIN0", ["PA02"]),
        Pin(4, "PA03/ADC_VREFA/AIN1", ["PA03"]),
        Pin(5, "PA04/SERCOM0.0/AIN4", ["PA04"]),
        Pin(6, "PA05/SERCOM0.1/AIN5", ["PA05"]),
        Pin(7, "PA06/SERCOM0.2/AIN6", ["PA06"]),
        Pin(8, "PA07/SERCOM0.3/AIN7", ["PA07"]),
        Pin(9, "VDDANA", ["3V3"]),  # decouple to GND
        Pin(10, "GND", ["GND"]),
        Pin(11, "PA08/NMI/SERCOM2.0/AIN16", ["PA08"]),
        Pin(12, "PA09/SERCOM2.1/AIN17", ["PA09"]),
        Pin(13, "PA10/SERCOM2.2/AIN18", ["PA10"]),
        Pin(14, "PA11/SERCOM2.3/AIN19", ["PA11"]),
        Pin(15, "PA14/XIN/SERCOM4.2", ["PA14"]),
        Pin(16, "PA15/XOUT/SERCOM4.3", ["PA15"]),
        Pin(17, "PA16/SERCOM1.0", ["PA16"]),
        Pin(18, "PA17/SERCOM1.1", ["PA17"]),
        Pin(19, "PA18/SERCOM1.2", ["PA18"]),
        Pin(20, "PA19/SERCOM1.3", ["PA19"]),
        Pin(21, "PA22/SERCOM3.0", ["mcu_TXD"]),
        Pin(22, "PA23/SERCOM3.1/USBSOF", ["mcu_RXD"]),
        Pin(23, "PA24/USBDM", ["USBDM"]),
        Pin(24, "PA25/USBDP", ["USBDP"]),
        Pin(25, "PA27", ["PA27"]),
        Pin(26, "nRESET", ["mcu_RESET"]),
        Pin(27, "PA28", ["PA28"]),
        Pin(28, "GND", ["GND"]),
        Pin(29, "VDDCORE", ["VDDCORE"]),  # regulated output, needs cap to GND
        Pin(30, "VDDIN", ["3V3"]),  # decouple to GND
        Pin(31, "PA30/SWCLK", ["SWCLK"]),
        Pin(32, "PA31/SWDIO", ["SWDIO"]),
    ],
)
mcu_cap1 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C3")
mcu_cap2 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C4")
mcu_cap3 = myelin_kicad_pcb.C0805("1u", "GND", "VDDCORE", ref="C5")
# SAM D21 has an internal pull-up, so this is optional
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R1")
# The SAM D21 datasheet says a 1k pullup on SWCLK is critical for reliability
mcu_swclk_pullup = myelin_kicad_pcb.R0805("1k", "SWCLK", "3V3", ref="R2")

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

power_led_r = myelin_kicad_pcb.R0805("330R", "3V3", "power_led_anode", ref="R3")
power_led = myelin_kicad_pcb.DSOD323("led", "GND", "power_led_anode", ref="L1")

# Micro USB socket, mounted on the bottom of the board
micro_usb = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:micro_usb_b_smd_molex",
    identifier="USB",
    value="usb",
    pins=[
        Pin(1, "V", ["5V"]),  # input from host
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "ID", ["USB_ID"]),
        Pin(5, "G", ["GND"]),
    ],
)

# USB-A (host) socket
usb_host = myelin_kicad_pcb.Component(
    footprint="Connectors:USB_A",
    identifier="HOST",
    value="usb host",
    pins=[
        Pin(1, "V", ["5V"]),  # output to device
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "G", ["GND"]),
    ],
)

# MC-146 32.768000 kHz crystal
# load capacitance 12.5pF
# CL = (C1 * C2) / (C1 + C2) + Cstray
#    = C1*C1 / 2*C1 + Cstray
# 12.5pF = C1/2 + 5pF
# C1 = 2(12.5pF - 5pF)
#    = 15pF
# So we should use two 15pF caps
xtal = myelin_kicad_pcb.Component(
    footprint="Crystals:Crystal_SMD_SeikoEpson_MC146-4pin_6.7x1.5mm_HandSoldering",
    identifier="X1",
    value="MC146 32768Hz",
    pins=[
        Pin(1, "X1", ["XTAL_IN"]),
        Pin(4, "X2", ["XTAL_OUT"]),
    ],
)
xtal_cap1 = myelin_kicad_pcb.C0805("15p", "GND", "XTAL_IN", ref="C6")
xtal_cap1 = myelin_kicad_pcb.C0805("15p", "GND", "XTAL_OUT", ref="C7")

regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="U1",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C1")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C2")

# 24 pins total:
# - 20 x gpio
# - 3v3, 5v, GND
# - /reset
# skipping: 2nd 3v3/gnd, usbdb/usbdp, swdio/swclk, xtalin/xtalout

pin_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x13_Pitch2.54mm",
    identifier="CON",
    value="pins",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["GND"]),
        Pin(3, "", ["PA04"]),
        Pin(4, "", ["PA03"]),
        Pin(5, "", ["PA06"]),
        Pin(6, "", ["PA05"]),
        Pin(7, "", ["PA02"]),
        Pin(8, "", ["PA07"]),
        Pin(9, "", ["PA09"]),
        Pin(10, "", ["PA08"]),
        Pin(11, "", ["PA11"]),
        Pin(12, "", ["PA10"]),
        Pin(13, "", ["PA15"]),
        Pin(14, "", ["PA14"]),
        Pin(15, "", ["PA27"]),
        Pin(16, "", ["PA28"]),
        Pin(17, "", ["PA17"]),
        Pin(18, "", ["PA16"]),
        Pin(19, "", ["PA19"]),
        Pin(20, "", ["PA18"]),
        Pin(21, "", ["mcu_RXD"]),
        Pin(22, "", ["mcu_TXD"]),
        Pin(23, "", ["GND"]),
        Pin(24, "", ["3V3"]),
        Pin(25, "", ["GND"]),
        Pin(26, "", ["5V"]),
    ],
)

power_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="PWR",
    value="reset",
    pins=[
        Pin(1, "", ["3V3"]),
        Pin(2, "", ["5V"]),
    ],
)

reset_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="RST",
    value="reset",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["mcu_RESET"]),
    ],
)

for n in range(20):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )


myelin_kicad_pcb.dump_netlist("atsamd21_usb.net")
