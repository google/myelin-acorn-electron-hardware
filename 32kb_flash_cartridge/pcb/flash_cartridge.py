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

# ----------------------------------------------
# 32kb_flash_cartridge
# ----------------------------------------------

# by Phillip Pearson

# Acorn Electron cartridge providing two 16kB flash banks.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Cartridge connector
cart_front = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_cartridge_edge_connector",
    identifier="CART",
    value="edge connector",
    pins=[
        # front of cartridge / bottom layer of PCB
        Pin("B1", "5V", ["5V"]),
        Pin("B2", "A10", ["elk_A10"]),
        Pin("B3", "D3", ["elk_D3"]),
        Pin("B4", "A11", ["elk_A11"]),
        Pin("B5", "A9", ["elk_A9"]),
        Pin("B6", "D7", ["elk_D7"]),
        Pin("B7", "D6", ["elk_D6"]),
        Pin("B8", "D5", ["elk_D5"]),
        Pin("B9", "D4", ["elk_D4"]),
        Pin("B10", "nOE2"),
        Pin("B11", "BA7", ["elk_A7"]),
        Pin("B12", "BA6", ["elk_A6"]),
        Pin("B13", "BA5", ["elk_A5"]),
        Pin("B14", "BA4", ["elk_A4"]),
        Pin("B15", "BA3", ["elk_A3"]),
        Pin("B16", "BA2", ["elk_A2"]),
        Pin("B17", "BA1", ["elk_A1"]),
        Pin("B18", "BA0", ["elk_A0"]),
        Pin("B19", "D0", ["elk_D0"]),
        Pin("B20", "D2", ["elk_D2"]),
        Pin("B21", "D1", ["elk_D1"]),
        Pin("B22", "GND", ["GND"]),
        # rear of cartridge / top layer of PCB
        Pin("A1", "5V", ["5V"]),
        Pin("A2", "nOE", ["elk_nOE"]),
        Pin("A3", "nRST"),
        Pin("A4", "RnW", ["elk_RnW"]),
        Pin("A5", "A8", ["elk_A8"]),
        Pin("A6", "A13", ["elk_A13"]),
        Pin("A7", "A12", ["elk_A12"]),
        Pin("A8", "PHI0", ["elk_PHI0"]),
        Pin("A9", "-5V"),
        Pin("A10", "NC"),
        Pin("A11", "nRDY"),
        Pin("A12", "nNMI"),
        Pin("A13", "nIRQ"),
        Pin("A14", "nINFC"),
        Pin("A15", "nINFD"),
        Pin("A16", "ROMQA", ["elk_ROMQA"]),
        Pin("A17", "16MHZ"),
        Pin("A18", "nROMSTB"),
        Pin("A19", "ADOUT"),
        Pin("A20", "ADGND"),
        Pin("A21", "ADIN"),
        Pin("A22", "GND", ["GND"]),
    ],
)

bulk_cap = myelin_kicad_pcb.C0805("10u", "5V", "GND", ref="C3")

flash = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:sst_plcc32_nh",
    identifier="U2",
    value="SST39SF010A",
    pins=[
        Pin(1, "NC"), # A18 on -040A
        Pin(2, "A16", ["elk_ROMQA"]),
        Pin(3, "A15", ["GND"]),
        Pin(4, "A12", ["elk_A12"]),
        Pin(5, "A7", ["elk_A7"]),
        Pin(6, "A6", ["elk_A6"]),
        Pin(7, "A5", ["elk_A5"]),
        Pin(8, "A4", ["elk_A4"]),
        Pin(9, "A3", ["elk_A3"]),
        Pin(10, "A2", ["elk_A2"]),
        Pin(11, "A1", ["elk_A1"]),
        Pin(12, "A0", ["elk_A0"]),
        Pin(13, "D0", ["elk_D0"]),
        Pin(14, "D1", ["elk_D1"]),
        Pin(15, "D2", ["elk_D2"]),
        Pin(16, "VSS", ["GND"]),
        Pin(17, "D3", ["elk_D3"]),
        Pin(18, "D4", ["elk_D4"]),
        Pin(19, "D5", ["elk_D5"]),
        Pin(20, "D6", ["elk_D6"]),
        Pin(21, "D7", ["elk_D7"]),
        Pin(22, "nCE", ["flash_nCE"]),
        Pin(23, "A10", ["elk_A10"]),
        Pin(24, "nOE", ["flash_nOE"]),
        Pin(25, "A11", ["elk_A11"]),
        Pin(26, "A9", ["elk_A9"]),
        Pin(27, "A8", ["elk_A8"]),
        Pin(28, "A13", ["elk_A13"]),
        Pin(29, "A14", ["elk_A12"]),
        Pin(30, "NC"), # A17 on -020A and -040A
        Pin(31, "nWE", ["elk_RnW"]),
        Pin(32, "VDD", ["5V"]),
    ],
)
flash_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C2")

quad_nand = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="U1",
    value="74HCT00",
    pins=[
        Pin(1,  "1A",  ["elk_nOE"]),
        Pin(2,  "1B",  ["elk_nOE"]),
        Pin(3,  "1Y",  ["not_elk_nOE"]),
        Pin(4,  "2A",  ["not_elk_nOE"]),
        Pin(5,  "2B",  ["elk_PHI0"]),
        Pin(6,  "2Y",  ["flash_nCE"]),
        Pin(7,  "GND", ["GND"]),
        Pin(8,  "3Y"), # unused gate
        Pin(9,  "3A",  ["GND"]), # unused gate
        Pin(10, "3B",  ["GND"]), # unused gate
        Pin(11, "4Y",  ["flash_nOE"]),
        Pin(12, "4A",  ["elk_RnW"]),
        Pin(13, "4B",  ["elk_RnW"]),
        Pin(14, "VCC", ["5V"]),
    ],
)
nand_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C1")

myelin_kicad_pcb.dump_netlist("flash_cartridge.net")
