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

# --------------------
# xc9500xl_44_breakout
# --------------------

# by Phillip Pearson

# Simple breakout board for xc9500xl CPLDs in the vqg44 package.  I have a
# bunch of XC9536XL-VQG44 chips that would come in handy as level shifters
# and so on.


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="CPLD",
    value="XC9572XL-10VQG44C",
    desc="IC CPLD Xilinx 72MC 44-pin; https://www.digikey.com/products/en?keywords=122-1448-ND",
    pins=[
        Pin(39, "P1.2",          "pin39"),
        Pin(40, "P1.5",          "pin40"),
        Pin(41, "P1.6",          "pin41"),
        Pin(42, "P1.8",          "pin42"),
        Pin(43, "P1.9-GCK1",     "pin43_gck1"),
        Pin(44, "P1.11-GCK2",    "pin44_gck2"),
        Pin( 1, "P1.14-GCK3",    "pin1_gck3"),
        Pin( 2, "P1.15",         "pin2"),
        Pin( 3, "P1.17",         "pin3"),
        Pin( 4, "GND",           "GND"),
        Pin( 5, "P3.2",          "pin5"),
        Pin( 6, "P3.5",          "pin6"),
        Pin( 7, "P3.8",          "pin7"),
        Pin( 8, "P3.9",          "pin8"),
        Pin( 9, "TDI",           "TDI"),
        Pin(10, "TMS",           "TMS"),
        Pin(11, "TCK",           "TCK"),
        Pin(12, "P3.11",         "pin12"),
        Pin(13, "P3.14",         "pin13"),
        Pin(14, "P3.15",         "pin14"),
        Pin(15, "VCCINT_3V3",    "3V3"),
        Pin(16, "P3.17",         "pin16"),
        Pin(17, "GND",           "GND"),
        Pin(18, "P3.16",         "pin18"),
        Pin(19, "P4.2",          "pin19"),
        Pin(20, "P4.5",          "pin20"),
        Pin(21, "P4.8",          "pin21"),
        Pin(22, "P4.11",         "pin22"),
        Pin(23, "P4.14",         "pin23"),
        Pin(24, "TDO",           "TDO"),
        Pin(25, "GND",           "GND"),
        Pin(26, "VCCIO_2V5_3V3", "3V3"),
        Pin(27, "P4.15",         "pin27"),
        Pin(28, "P4.17",         "pin28"),
        Pin(29, "P2.2",          "pin29"),
        Pin(30, "P2.5",          "pin30"),
        Pin(31, "P2.6",          "pin31"),
        Pin(32, "P2.8",          "pin32"),
        Pin(33, "P2.9-GSR",      "pin33_GSR"),
        Pin(34, "P2.11-GTS2",    "pin34_GTS2"),
        Pin(35, "VCCINT_3V3",    "3V3"),
        Pin(36, "P2.14-GTS1",    "pin36_GTS1"),
        Pin(37, "P2.15",         "pin37"),
        Pin(38, "P2.17",         "pin38"),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C1", handsoldering=False)
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2", handsoldering=False)
cpld_cap3 = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C3", handsoldering=False)

regulator = myelin_kicad_pcb.Component(
    footprint="Package_TO_SOT_SMD:SOT-89-3",
    identifier="REG",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C4")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C5")

cpld_jtag = myelin_kicad_pcb.Component(
    footprint="Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical",
    identifier="JTAG",
    value="jtag",
    pins=[
        Pin( 1, "TCK", "TCK"),
        Pin( 2, "GND", "GND"),
        Pin( 3, "TDO", "TDO"),
        Pin( 4, "3V3", "3V3"),
        Pin( 5, "TMS", "TMS"),
        Pin( 6, "NC"),
        Pin( 7, "NC"),
        Pin( 8, "NC"),
        Pin( 9, "TDI", "TDI"),
        Pin(10, "GND", "GND"),
    ],
)

cpld_io = [
    myelin_kicad_pcb.Component(
        footprint="Connector_PinHeader_2.54mm:PinHeader_2x17_P2.54mm_Vertical",
        identifier="IO1",
        value="CPLD IO",
        pins=[
            Pin( 2, "", "pin34_GTS2"),
            Pin( 4, "", "pin36_GTS1"),
            Pin( 6, "", "pin37"),
            Pin( 8, "", "pin38"),
            Pin(10, "", "pin39"),
            Pin(12, "", "pin40"),
            Pin(14, "", "pin41"),
            Pin(16, "", "pin42"),
            Pin(18, "", "pin43_gck1"),
            Pin(20, "", "pin44_gck2"),
            Pin(22, "", "pin1_gck3"),
            Pin(24, "", "pin2"),
            Pin(26, "", "pin3"),
            Pin(28, "", "pin5"),
            Pin(30, "", "pin6"),
            Pin(32, "", "pin7"),
            Pin(34, "", "pin8"),
        ] + [
            Pin(n, "", "GND")
            for n in range(1, 34, 2)
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="Connector_PinHeader_2.54mm:PinHeader_2x17_P2.54mm_Vertical",
        identifier="IO2",
        value="CPLD IO",
        pins=[
            Pin( 1, "", "pin33_GSR"),
            Pin( 3, "", "pin32"),
            Pin( 5, "", "pin31"),
            Pin( 7, "", "pin30"),
            Pin( 9, "", "pin29"),
            Pin(11, "", "pin28"),
            Pin(13, "", "pin27"),
            Pin(15, "", "pin23"),
            Pin(17, "", "pin22"),
            Pin(19, "", "pin21"),
            Pin(21, "", "pin20"),
            Pin(23, "", "pin19"),
            Pin(25, "", "pin18"),
            Pin(27, "", "pin16"),
            Pin(29, "", "pin14"),
            Pin(31, "", "pin13"),
            Pin(33, "", "pin12"),
        ] + [
            Pin(n, "", "GND")
            for n in range(2, 35, 2)
        ],
    ),
]


# Just in case we want to connect up an ext PSU for CPLD programming
ext_power = [
    myelin_kicad_pcb.Component(
        footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
        identifier="EXTPWR%d" % (n+1),
        value="ext pwr",
        pins=[
            Pin(1, "A", "GND"),
            Pin(2, "B", "3V3"),
            Pin(3, "C", "5V"),
        ],
    )
    for n in range(3)
]

for n in range(19):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

myelin_kicad_pcb.dump_netlist("xc9500xl_44_breakout.net")
