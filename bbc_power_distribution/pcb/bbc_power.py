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

# ---------
# bbc_power
# ---------

# by Phillip Pearson

# A simple PCB to distribute power from an external 5V supply to a BBC or Master
# motherboard.

PROJECT_NAME = "bbc_power"

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Barrel jack
barrel = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:dc10a_barrel_jack",
    identifier="VIN",
    value="5V input",
    pins={
        "TIP": "5V",
        "RING": "GND",
    },
)

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

# Power LED
power_led_r = myelin_kicad_pcb.R0805("330R", "5V", "power_led_anode", ref="R1")
power_led = myelin_kicad_pcb.DSOD323("led", "GND", "power_led_anode", ref="L1")

# Outputs for 3 x GND
# Outputs for 3 x 5V
# Output for -5V
power_outputs = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:pin_60mil",
        identifier="P?",
        value="5V",
        pins=[Pin(1, "", "5V")],
    ) for out_id in range(3)
] + [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:pin_60mil",
        identifier="P?",
        value="GND",
        pins=[Pin(1, "", "GND")],
    ) for out_id in range(3)
] + [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:pin_60mil",
        identifier="P?",
        value="-5V",
        pins=[Pin(1, "", "-5V")],
    )
]

# Pair of mounting holes I can put a zip tie through, for strain relief
mounting_holes = [myelin_kicad_pcb.Component(
    footprint="myelin-kicad:pin_100_120mil",
    identifier="M?",
    value="hole",
) for hole_id in range(2)]

# Footprint for LTC1983 + caps
charge_pump = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-23-6_Handsoldering",
    identifier="U1",
    value="Charge pump",
    pins=[
        Pin(1, "VCC", ["5V"]),
        Pin(2, "VOUT", ["-5V"]),
        Pin(3, "C+", ["Cfly_plus"]),
        Pin(4, "C-", ["Cfly_minus"]),
        Pin(5, "GND", ["GND"]),
        Pin(6, "/SHDN", ["5V"]),
    ]
)
charge_pump_c1 = myelin_kicad_pcb.R0805("10u", "5V", "GND", ref="C1")
charge_pump_c2 = myelin_kicad_pcb.R0805("10u", "-5V", "GND", ref="C2")
charge_pump_c3 = myelin_kicad_pcb.R0805("1u", "Cfly_plus", "Cfly_minus", ref="C3")

# 5V/GND/-5V header to go to external dmx-isolated2 board
# A bunch of 5V/GND/-5V test points so I can connect more stuff if necessary
# (floppy drive emulator, 1MHz bus devices, ...)
ext_5v = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x06_Pitch2.54mm",
    identifier="EXT5V",
    value="5v",
    pins=[
        Pin(1, "", ["5V"]),
        Pin(2, "", ["5V"]),
        Pin(3, "", ["5V"]),
        Pin(4, "", ["5V"]),
        Pin(5, "", ["5V"]),
        Pin(6, "", ["5V"]),
    ],
)
ext_gnd = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x06_Pitch2.54mm",
    identifier="EXTGND",
    value="0v",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["GND"]),
        Pin(3, "", ["GND"]),
        Pin(4, "", ["GND"]),
        Pin(5, "", ["GND"]),
        Pin(6, "", ["GND"]),
    ],
)
ext_neg_5v = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x06_Pitch2.54mm",
    identifier="EXT-5V",
    value="-5v",
    pins=[
        Pin(1, "", ["-5V"]),
        Pin(2, "", ["-5V"]),
        Pin(3, "", ["-5V"]),
        Pin(4, "", ["-5V"]),
        Pin(5, "", ["-5V"]),
        Pin(6, "", ["-5V"]),
    ],
)

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
