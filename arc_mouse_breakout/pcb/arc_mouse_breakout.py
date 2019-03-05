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

# ------------------
# arc_mouse_breakout
# ------------------

# by Phillip Pearson

# Tiny board to break out the mini DIN socket for an Archimedes mouse


PROJECT_NAME = "arc_mouse_breakout"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

arc_keyboard_din = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:minidin_9_pcb_mount",
    identifier="MOUSE",
    value="CUI-MD90S",
    pins=[
        # Labels are <Acorn label>_<SmallyMouse2 label>
        Pin( 1, "Xr_X2",  "X2"),
        Pin( 2, "SW1_LB", "LB"),
        Pin( 3, "SW2_MB", "MB"),
        Pin( 4, "GND_NC", "GND"),
        Pin( 5, "Xd_X1",  "X1"),
        Pin( 6, "5V",     "5V"),
        Pin( 7, "Yr_Y2",  "Y2"),
        Pin( 8, "SW3_RB", "RB"),
        Pin( 9, "Yd_Y1",  "Y1"),
        # https://www.waitingforfriday.com/?p=827 says pin 4 is NC and shield
        # is GND, so ground the shield too.
        Pin("S1", "GND", "GND"),
    ],
)

# Header that should plug straight into a SmallyMouse2 board
header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical",
    identifier="HDR",
    value="Mouse",
    desc="1x10 0.1 inch male header",
    pins=[
        Pin( 1, "", "X1"),
        Pin( 2, "", "Y1"),
        Pin( 3, "", "X2"),
        Pin( 4, "", "Y2"),
        Pin( 5, "", "LB"),
        Pin( 6, "", "MB"),
        Pin( 7, "", "RB"),
        Pin( 8, "", "GND"),
        Pin( 9, "", "GND"),
        Pin(10, "", "5V"),
    ],
)

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
