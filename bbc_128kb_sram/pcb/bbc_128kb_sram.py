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

# --------------
# bbc_128kb_sram
# --------------

# by Phillip Pearson

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

quad_nand = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="U1",
    value="74HCT00",
    pins=[
        Pin(1,  "1A",  ["bbc_n2MHzE"]),
        Pin(2,  "1B",  ["bbc_n2MHzE"]),
        Pin(3,  "1Y",  ["bbc_nn2MHzE"]),
        Pin(4,  "2A",  ["bbc_nn2MHzE"]),
        Pin(5,  "2B",  ["bbc_RnW"]),
        Pin(6,  "2Y",  ["flash_nOE"]),
        Pin(7,  "GND", ["GND"]),
        Pin(8,  "3Y",  ["flash_nWE"]),
        Pin(9,  "3A",  ["bbc_nn2MHzE"]),
        Pin(10, "3B",  ["bbc_nRnW"]),
        Pin(11, "4Y",  ["flash_CS"]),
        Pin(12, "4A",  ["bbc_nCS0"]),
        Pin(13, "4B",  ["bbc_nCS1"]),
        Pin(14, "VCC", ["5V"]),
    ],
)
nand_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C1")

# 128kB SRAM chip
# ---------------
# 17 address lines, 8 data lines, 3 control lines, 1 unused, 1 NC, 2 power
#   - 28 digital, 4 misc, total 32 pins.
sram = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:issi_32l_450mil_sop",
    identifier="RAM",
    value="IS62C1024 128kB SRAM",
    pins=[
        # left side, top to bottom
        Pin(1,  "NC"),
        Pin(2,  "A16",  ["A12"]),
        Pin(3,  "A14",  ["A7"]),
        Pin(4,  "A12",  ["A13"]),
        Pin(5,  "A7",   ["A6"]),
        Pin(6,  "A6",   ["A8"]),
        Pin(7,  "A5",   ["A5"]),
        Pin(8,  "A4",   ["A9"]),
        Pin(9,  "A3",   ["A4"]),
        Pin(10, "A2",   ["A11"]),
        Pin(11, "A1",   ["A2"]),
        Pin(12, "A0",   ["A1"]),
        Pin(13, "IO0",  ["D7"]),
        Pin(14, "IO1",  ["D0"]),
        Pin(15, "IO2",  ["D6"]),
        Pin(16, "GND",  ["GND"]),
        # right side, bottom to top
        Pin(17, "IO3",  ["D3"]),
        Pin(18, "IO4",  ["D4"]),
        Pin(19, "IO5",  ["D2"]),
        Pin(20, "IO6",  ["D5"]),
        Pin(21, "IO7",  ["D1"]),
        Pin(22, "nCE1", ["GND"]),  # we use the active-high CE2 instead here
        Pin(23, "A10",  ["A15"]),
        Pin(24, "nOE",  ["sram_nOE"]),  # = !(!n2MHzE && RnW)
        Pin(25, "A11",  ["bbc_nCS1"]),
        Pin(26, "A9",   ["A14"]),
        Pin(27, "A8",   ["A0"]),
        Pin(28, "A13",  ["A10"]),
        Pin(29, "nWE",  ["sram_nWE"]),  # = !(!n2MHzE && !RnW)
        Pin(30, "CE2",  ["sram_CE"]),  # = !(bbc_nCS0 && bbc_nCS1)
        Pin(31, "A15",  ["A3"]),
        Pin(32, "VDD",  ["5V"]),
    ],
)
sram_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C2")
sram_cap2 = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C3")
sram_cap3 = myelin_kicad_pcb.C0805("10u", "5V", "GND", ref="C4")

# 28-pin ROM footprint, to plug into the BBC motherboard
connector = myelin_kicad_pcb.Component(
    footprint="Housings_DIP:DIP-28_W15.24mm",
    identifier="ROM",
    value="ROM chip",
    desc="Adapter to emulate a 600mil 28-pin DIP, e.g. Digikey 1175-1525-5-ND",
    pins=[
        Pin( "1", "A15/5V"),
        Pin( "2", "A12", ["A12"]),
        Pin( "3", "A7",  ["A7"]),
        Pin( "4", "A6",  ["A6"]),
        Pin( "5", "A5",  ["A5"]),
        Pin( "6", "A4",  ["A4"]),
        Pin( "7", "A3",  ["A3"]),
        Pin( "8", "A2",  ["A2"]),
        Pin( "9", "A1",  ["A1"]),
        Pin("10", "A0",  ["A0"]),
        Pin("11", "D0",  ["D0"]),
        Pin("12", "D1",  ["D1"]),
        Pin("13", "D2",  ["D2"]),
        Pin("14", "VSS", ["GND"]),
        Pin("15", "D3",  ["D3"]),
        Pin("16", "D4",  ["D4"]),
        Pin("17", "D5",  ["D5"]),
        Pin("18", "D6",  ["D6"]),
        Pin("19", "D7",  ["D7"]),
        Pin("20", "nCS", ["bbc_nCS0"]),
        Pin("21", "A10", ["A10"]),
        Pin("22", "nOE", ["bbc_n2MHzE"]),
        Pin("23", "A11", ["A11"]),
        Pin("24", "A9",  ["A9"]),
        Pin("25", "A8",  ["A8"]),
        Pin("26", "A13", ["A13"]),
        Pin("27", "A14/5V"),
        Pin("28", "VCC", ["5V"]),
    ],
)

bbc_ncs1_connector = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:pin_32_60mil",
    identifier="CS1",
    value="",
    pins=[Pin(1, "nCS", "bbc_nCS1")],
)

flying_leads = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x04_Pitch2.54mm",
    identifier="LEADS",
    value="flying leads",
    desc="1x4 0.1 inch male header",
    pins=[
        Pin(1, "RnW", ["RnW"]),
        Pin(2, "WnR", ["nRnW"]),
        Pin(3, "BANK2", ["A14"]),
        Pin(4, "BANK3", ["A15"]),
    ],
)

ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
    desc="1x2 0.1 inch male header",
    pins=[
        Pin(1, "GND", ["GND"]),
        Pin(2, "5V", ["5V"]),
    ],
)

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(0)
]

myelin_kicad_pcb.dump_netlist("bbc_128kb_sram.net")
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
