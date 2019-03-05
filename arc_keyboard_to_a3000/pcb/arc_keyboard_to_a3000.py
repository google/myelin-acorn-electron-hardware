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

# ----------------
# arc_keyboard_to_a3000
# ----------------

# by Phillip Pearson

# Tiny board to connect an Archimedes keyboard (DIN connector) to the A3000's
# external keyboard header.


PROJECT_NAME = "arc_keyboard_to_a3000"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

arc_keyboard_din = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:minidin_6_ps2_pcb_mount",
    identifier="KB",
    value="CUI-MD60S",
    pins=[
        Pin( 1, "RESET", "RESET"),
        Pin( 2, "NC", "pin2"),
        Pin( 3, "GND", "GND"),
        Pin( 4, "5V", "5V"),
        Pin( 5, "arc KIN / kb TXD", "KIN"),
        Pin( 6, "arc KOUT / kb RXD", "KOUT"),
        # Ground the shield too, just in case
        Pin("S1", "", "GND"),
    ],
)

header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical",
    identifier="HDR",
    value="A3000 KB",
    desc="1x6 0.1 inch male header",
    pins=[
        Pin(1, "RESET",  "RESET"),  # Arc RESET, ps2 DATA
        Pin(2, "NC", "pin2"),       # NC for both Arc and PS2
        Pin(3, "GND",    "GND"),
        Pin(4, "5V",     "5V"),
        Pin(5, "kb TXD", "KIN"),    # Arc KIN, ps2 CLK
        Pin(6, "kb RXD", "KOUT"),   # Arc KOUT, ps2 NC
    ],
)

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
