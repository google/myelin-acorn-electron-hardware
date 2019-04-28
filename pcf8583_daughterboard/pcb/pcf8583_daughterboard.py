#!/usr/bin/python

# Copyright 2019 Google LLC
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

# ---------------------
# pcf8583_daughterboard
# ---------------------

# by Phillip Pearson

# A board to mount the PCF8583 and crystal, for severely battery-damaged
# motherboard repair.

# This uses a pair of AA batteries, which are easier to mount off board, and
# doesn't attempt to recharge them.  Diodes and resistors protect against
# reverse voltage.

# The standard Acorn circuit looks like this:

#   5V --|>--+-- 180R -- batt -- GND
#            |
#            +-- 47R -- NVR_POWER

# This circuit is designed not to be rechargeable, however, so we do this
# instead:

#   5V --|>-- 47R --+-- NVR_POWER
#                   |
# BATT --|>-- 47R --+

# We could just connect the two cathodes together, but this provides a little
# extra protection against short circuits.

# v2 adds a supercapacitor (or a rechargeable battery if you prefer), so the
# circuit ends up as:

#   5V --|>--+-- 180R (R3) -- supercap (C4) -- GND
#            |
#            +-- 47R (R1)--+-- NVR_POWER
#                          |
#   BATT --|>-- 47R (R2) --+

# This lets us use the same board with either a supercap or rechargeable
# battery in the C4 position, or an off-board nonrechargeable battery
# connected to the BATT header.


PROJECT_NAME = "pcf8583_daughterboard"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

diodes = [
    myelin_kicad_pcb.Component(
        footprint="Diode_SMD:D_SMA",
        identifier="D?",
        value="S1ATR",
        desc="Rectifier diode",
        pins=[
            Pin(1, "1", a),
            Pin(2, "2", k),
        ],
    )
    for a, k in [("5V", "5VD_cat"), ("BATT", "BATTD_cat")]
]

resistors = [
    myelin_kicad_pcb.R0805("47R", "5VD_cat", "NVR_POWER", ref="R1"),
    myelin_kicad_pcb.R0805("47R", "BATTD_cat", "NVR_POWER", ref="R2"),
    myelin_kicad_pcb.R0805("180R", "5VD_cat", "supercap_P", ref="R3"),
]

power_caps = [
    myelin_kicad_pcb.C0805("10u", "GND", "NVR_POWER", ref="C1"),
    myelin_kicad_pcb.C0805("100n", "GND", "NVR_POWER", ref="C2"),
]

supercap = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:dgh255q5r5",
    identifier="C4",
    value="DGH255Q5R5",
    desc="Supercapacitor",
    pins=[
        Pin(1, "1", "supercap_P"),  # positive terminal
        Pin(2, "2", "GND"),  # negative terminal
    ],
)

pcf8583 = [
    myelin_kicad_pcb.Component(
        footprint=fp,
        identifier=ident,
        value="PCF8583",
        pins=[
            Pin( 1, "OSCI", "OSCI"),
            Pin( 2, "OSCO", "OSCO"),
            Pin( 3, "A0",   "GND"),
            Pin( 4, "VSS",  "GND"),
            Pin( 5, "SDA",  "SDA"),
            Pin( 6, "SCL",  "SCL"),
            Pin( 7, "nINT"),
            Pin( 8, "VDD",  "NVR_POWER"),  # TODO battery, not 5V
        ],
    )
    for ident, fp in [
        ("NVRAM", "Package_DIP:DIP-8_W7.62mm"),
        ("NVSMD", "myelin-kicad:so8_pcf8583t_7.5x7.5mm"),
    ]
]

crystal = myelin_kicad_pcb.Component(
    footprint="Crystal:Crystal_AT310_D3.0mm_L10.0mm_Horizontal_1EP_style2",
    identifier="XTAL",
    value="32.768kHz",
    desc="",
    pins=[
        Pin( 1, "", "OSCO"),
        Pin( 2, "", "OSCI"),
        Pin( 3, "", "GND"),
    ],
)

xtal_cap = myelin_kicad_pcb.C0805("15p", "OSCI", "NVR_POWER", ref="C3")

# Batt: three-pin connector with power in the middle and ground on both outer
# pins, to match PL8 on the Master 128

battery = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
    identifier="BATT",
    value="Battery",
    desc="",
    pins=[
        Pin( 1, "BATT-", "GND"),
        Pin( 2, "BATT+", "BATT"),
        Pin( 3, "BATT-", "GND"),
    ],
)

header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
    identifier="HDR",
    value="Ext",
    desc="4 pin 0.1 inch male header",
    pins=[
        # Probably best to run this through ribbon cable, so SCL gets some
        # shielding.
        Pin( 1, "SDA", "SDA"),
        Pin( 2, "GND", "GND"),
        Pin( 3, "SCL", "SCL"),
        Pin( 4, "5V",  "5V"),
    ],
)

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
