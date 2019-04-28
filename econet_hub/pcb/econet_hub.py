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

# ----------
# econet_hub
# ----------

# by Phillip Pearson

PROJECT_NAME = "econet_hub"

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Power
# -----

# Micro USB
micro_usb = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:micro_usb_b_smd_molex",
    identifier="USB",
    value="usb",
    desc="Molex 1050170001 (Digikey WM1399CT-ND) surface mount micro USB socket with mounting holes.",
    pins=[
        Pin(1, "V", ["5V"]),
        Pin(5, "G", ["GND"]),
    ],
)

ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
	desc="1x3 0.1 inch male header",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["5V"]),
        Pin(3, "", ["GND"]),
        Pin(4, "", ["5V"]),
        Pin(5, "", ["GND"]),
        Pin(6, "", ["5V"]),
    ],
)
power_cap = myelin_kicad_pcb.C0805("10u", "5V", "GND", ref="C2")

# Econet data line termination / biasing
# --------------------------------------

# 1k/220R/1k voltage divider drawing 2.25mA and giving 2.25/2.75V on D-/D+

termination_r1 = myelin_kicad_pcb.R0805(
    "1k", "5V", "bias_P", ref="R2")
termination_r2 = myelin_kicad_pcb.R0805(
    "220R", "bias_P", "bias_M", ref="R3")
termination_r3 = myelin_kicad_pcb.R0805(
    "1k", "bias_M", "GND", ref="R4")
termination_r4 = myelin_kicad_pcb.R0805(
    "56R", "bias_P", "econet_data_line_P", ref="R5")
termination_r5 = myelin_kicad_pcb.R0805(
    "56R", "bias_M", "econet_data_line_M", ref="R6")


# Clock
# -----

# This is based on Simon Inns' AVR clock: http://www.waitingforfriday.com/?p=19

avr = myelin_kicad_pcb.Component(
    # r1 got this wrong; the SO attiny85 is a wide-body version, which KiCad
    # calls SOIJ-8.
    footprint="Housings_SOIC:SOIJ-8_5.3x5.3mm_Pitch1.27mm",
    identifier="AVR",
    value="ATTINY85-20SU",
    desc="ATTINY85 in 8S2 package (0.208 inch / 5.3 mm wide SOIC-8)",
    pins=[
        Pin( 1, "/RESET", "avr_nRESET"),
        Pin( 2, "PB3", "econet_clock_line_P"),
        Pin( 3, "PB4", "econet_clock_line_M"),
        Pin( 4, "GND", "GND"),
        Pin( 5, "MOSI", "avr_MOSI"),
        Pin( 6, "MISO", "avr_MISO"),
        Pin( 7, "SCK", "avr_SCK"),
        Pin( 8, "VCC", "5V"),
    ],
)
avr_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C1")
avr_reset_pullup = myelin_kicad_pcb.R0805("10k", "5V", "avr_nRESET", ref="R1")

# AVR programming connector
avr_isp = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm",
    identifier="ISP",
    value="avr isp",
	desc="2x3 0.1 inch header for AVR programming (OPTIONAL)",
    pins=[
        Pin(1, "MISO", "avr_MISO"),
        Pin(2, "VCC", "5V"),
        Pin(3, "SCK", "avr_SCK"),
        Pin(4, "MOSI", "avr_MOSI"),
        Pin(5, "RESET", "avr_nRESET"),
        Pin(6, "GND", "GND"),
    ],
)


# Econet sockets and headers
# --------------------------

econet_headers = [myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x05_Pitch2.54mm",
    identifier="H%d" % header_id,
    value="Econet",
	desc="1x5 0.1 inch male header",
    pins=[
        Pin( 5, "D+", ["econet_data_line_P"]),
        Pin( 4, "D-", ["econet_data_line_M"]),
        Pin( 3, "GND", ["GND"]),
        Pin( 2, "C+", ["econet_clock_line_P"]),
        Pin( 1, "C-", ["econet_clock_line_M"]),
    ],
) for header_id in range(2)]

econet_sockets = [myelin_kicad_pcb.Component(
    footprint="myelin-kicad:din_5_econet_pcb_mount",
    identifier="E%d" % socket_id,
    value="Econet",
    desc=("5-pin DIN socket, as for a MIDI cable, with zig-zag pin layout.  "
          "Compare pinout against PCB because several variants exist."),
    pins=[
        # DIN-5 pins are numbered weirdly -- 1, 4, 2, 5, 3 around the circle
        Pin( 1, "D+", ["econet_data_line_P"]),
        Pin( 4, "D-", ["econet_data_line_M"]),
        Pin( 2, "GND", ["GND"]),
        Pin( 5, "C+", ["econet_clock_line_P"]),
        Pin( 3, "C-", ["econet_clock_line_M"]),

        # Ground all the shield pins
        Pin("S1", "", "GND"),
        Pin("S2", "", "GND"),
        Pin("S3", "", "GND"),
        Pin("S4", "", "GND"),
    ],
) for socket_id in range(5)]

# Ground plane stapling vias
for n in range(5):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)

myelin_kicad_pcb.dump_netlist("cpu_socket_expansion.net")
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
