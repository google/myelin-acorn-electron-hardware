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

# ------------------------
# bga_in_two_layers
# ------------------------

# by Phillip Pearson

# An attempt to make a two layer board for a 169-ball BGA FPGA chip. I imagine
# the chip won't run at full speed without a proper ground plane, but it'll be
# great for my other projects if I can use the 10M08SCU169 on two layer boards.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


fpga = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:lattice_ubga169_smallpads",
    identifier="FPGA",
    value="10M08SCU169",
    pins=[
        # IOs

        # Outer ring -- 45 IOs (4 x 13 - 1 for TMS on G1)
        Pin("A2",  "", "IO0"),
        Pin("A3",  "", "IO1"),
        Pin("A4",  "", "IO2"),
        Pin("A5",  "", "IO3"),
        Pin("A6",  "", "IO4"),
        Pin("A7",  "", "IO5"),
        Pin("A8",  "", "IO6"),
        Pin("A9",  "", "IO7"),
        Pin("A10", "", "IO8"),
        Pin("A11", "", "IO9"),
        Pin("A12", "", "IO10"),
#        Pin("N2",  "", "IO11"),
#        Pin("N3",  "", "IO12"),
        Pin("N4",  "", "IO13"),
        Pin("N5",  "", "IO14"),
        Pin("N6",  "", "IO15"),
        Pin("N7",  "", "IO16"),
        Pin("N8",  "", "IO17"),
        Pin("N9",  "", "IO18"),
        Pin("N10", "", "IO19"),
        Pin("N11", "", "IO20"),
        Pin("N12", "", "IO21"),
        Pin("B1",  "", "IO22"),
        Pin("C1",  "", "IO23"),
        Pin("D1",  "", "IO24"),
        Pin("E1",  "", "IO25"),
        Pin("F1",  "", "IO26"),
        Pin("H1",  "", "IO27"),
        Pin("J1",  "", "IO28"),
        Pin("K1",  "", "IO30"),
        Pin("M1",  "", "IO32"),
        Pin("B13", "", "IO33"),
        Pin("C13", "", "IO34"),
        Pin("D13", "", "IO35"),
        Pin("G13", "", "IO38"),
        Pin("H13", "", "IO39"),
        Pin("J13", "", "IO40"),
        Pin("K13", "", "IO42"),
        Pin("L13", "", "IO43"),
        Pin("M13", "", "IO44"),

        # Next ring in -
        Pin("B2",  "", "IO45"),
        Pin("B3",  "", "IO46"),
        Pin("B4",  "", "IO47"),
        Pin("B5",  "", "IO48"),
        Pin("B6",  "", "IO49"),
        Pin("B7",  "", "IO50"),
        Pin("B10", "", "IO51"),
        Pin("B11", "", "IO52"),
        Pin("M2",  "", "IO53"),
        Pin("M3",  "", "IO54"),
        Pin("M4",  "", "IO55"),
        Pin("M5",  "", "IO56"),
        Pin("M7",  "", "IO57"),
        Pin("M8",  "", "IO58"),
        Pin("M9",  "", "IO59"),
        Pin("M10", "", "IO60"),
        Pin("M11", "", "IO61"),
        Pin("M12", "", "IO62"),

        Pin("C2",  "", "IO63"),
        Pin("H2",  "", "IO65"),
        Pin("J2",  "", "IO66"),
        Pin("K2",  "", "IO67"),
        Pin("L2",  "", "IO68"),
        Pin("L3",  "", "IO69"),
        Pin("C9",  "", "IO70"),
        Pin("C10", "", "IO71"),
        Pin("B12", "", "IO72"),
        Pin("C12", "", "IO73"),
        Pin("D11", "", "IO74"),
        Pin("D12", "", "IO75"),
        Pin("E12", "", "IO76"),
        Pin("F12", "", "IO77"),
        Pin("G12", "", "IO78"),
        Pin("J12", "", "IO79"),
        Pin("K11", "", "IO80"),
        Pin("K12", "", "IO81"),
        Pin("L11", "", "IO82"),
        Pin("L12", "", "IO83"),
        Pin("L10", "", "IO84"),
        Pin("C11", "", "IO85"),
        Pin("E3",  "", "IO86"),
        Pin("L5",  "", "IO87"),

        # Special pins
        Pin("G5", "CLK0n", "CLK0n"),
        Pin("H6", "CLK0p", "CLK0p"),
        Pin("H5", "CLK1n", "CLK1n"),
        Pin("H4", "CLK1p", "CLK1p"),
        # Pin("G10", "CLK2n", "CLK2n"),
        # Pin("G9", "CLK2p", "CLK2p"),
        Pin("E13", "CLK3n", "CLK3n"),
        Pin("F13", "CLK3p", "CLK3p"),
        Pin("N2", "DPCLK0", "DPCLK0"),
        Pin("N3", "DPCLK1", "DPCLK1"),
        Pin("F10", "DPCLK2", "DPCLK2"),
        Pin("F9", "DPCLK3", "DPCLK3"),
        Pin("L1", "VREFB2N0", "VREFB2N0"),

        # JTAG and other config pins
        Pin("E5",  "JTAGEN",     "fpga_JTAGEN"),
        Pin("G1",  "TMS",        "fpga_TMS"),
        Pin("G2",  "TCK",        "fpga_TCK"),
        Pin("F5",  "TDI",        "fpga_TDI"),
        Pin("F6",  "TDO",        "fpga_TDO"),
        Pin("B9",  "DEV_CLRn",   "fpga_DEV_CLRn"),
        Pin("D8",  "DEV_OE",     "fpga_DEV_OE"),
        #Pin("D7",  "CONFIG_SEL", "fpga_CONFIG_SEL"),
        Pin("E7",  "nCONFIG",    "3V3"),  # can be connected straight to VCCIO
        #Pin("D6",  "CRC_ERROR",  "fpga_CRC_ERROR"),
        Pin("C4",  "nSTATUS",    "fpga_nSTATUS"),
        Pin("C5",  "CONF_DONE",  "fpga_CONF_DONE"),

        # Signals used as power/ground to enable vias
        Pin("E4",  "",     "GND"),
        Pin("J5",  "",     "GND"),
        Pin("J6",  "",     "GND"),
        Pin("D6",  "",     "GND"),
        Pin("D7",  "",     "GND"),
        Pin("K10",  "",     "GND"),
        Pin("E10",  "",     "GND"),
        Pin("J10",  "",     "GND"),

        Pin("E8",  "",     "3V3"),
        Pin("H8",  "",     "3V3"),
        Pin("D9",  "",     "3V3"),
        Pin("K7",  "",     "3V3"),
        Pin("K8",  "",     "3V3"),
        Pin("E6",  "",     "3V3"),
        Pin("F8",  "",     "3V3"),
        Pin("G4",  "",     "3V3"),
        Pin("L4",  "",     "3V3"),
        Pin("G9",  "",     "3V3"),
        Pin("G10",  "",     "3V3"),

        # Power and ground
        Pin("D2",  "GND",     "GND"),
        Pin("E2",  "GND",     "GND"),
        Pin("N13", "GND",     "GND"),
        Pin("N1",  "GND",     "GND"),
        Pin("M6",  "GND",     "GND"),
        Pin("L9",  "GND",     "GND"),
        Pin("J4",  "GND",     "GND"),
        Pin("H12", "GND",     "GND"),
        Pin("G7",  "GND",     "GND"),
        Pin("F3",  "GND",     "GND"),
        Pin("E11", "GND",     "GND"),
        Pin("D5",  "GND",     "GND"),
        Pin("C3",  "GND",     "GND"),
        Pin("B8",  "GND",     "GND"),
        Pin("A13", "GND",     "GND"),
        Pin("A1",  "GND",     "GND"),
        Pin("F2",  "VCCIO1A", "3V3"),
        Pin("G3",  "VCCIO1B", "3V3"),
        Pin("K3",  "VCCIO2",  "3V3"),
        Pin("J3",  "VCCIO2",  "3V3"),
        Pin("L8",  "VCCIO3",  "3V3"),
        Pin("L7",  "VCCIO3",  "3V3"),
        Pin("L6",  "VCCIO3",  "3V3"),
        Pin("J11", "VCCIO5",  "3V3"),
        Pin("H11", "VCCIO5",  "3V3"),
        Pin("G11", "VCCIO6",  "3V3"),
        Pin("F11", "VCCIO6",  "3V3"),
        Pin("C8",  "VCCIO8",  "3V3"),
        Pin("C7",  "VCCIO8",  "3V3"),
        Pin("C6",  "VCCIO8",  "3V3"),
        Pin("K4",  "VCCA1",   "3V3"),
        Pin("D10", "VCCA2",   "3V3"),
        Pin("D3",  "VCCA3",   "3V3"),
        Pin("D4",  "VCCA3",   "3V3"),
        Pin("K9",  "VCCA4",   "3V3"),
        Pin("H7",  "VCC_ONE", "3V3"),
        Pin("G8",  "VCC_ONE", "3V3"),
        Pin("G6",  "VCC_ONE", "3V3"),
        Pin("F7",  "VCC_ONE", "3V3"),
    ],
)

# chip won't init unless this is pulled high
conf_done_pullup = myelin_kicad_pcb.R0805("10k", "fpga_CONF_DONE", "3V3", ref="R1", handsoldering=False)

# chip goes into error state if this is pulled low
nstatus_pullup = myelin_kicad_pcb.R0805("10k", "fpga_nSTATUS", "3V3", ref="R2", handsoldering=False)

# prevent spurious jtag clocks
tck_pulldown = myelin_kicad_pcb.R0805("1-10k", "fpga_TCK", "GND", ref="R3", handsoldering=False)

# fpga_nCONFIG doesn't need a pullup, just connect straight to 3V3

# fpga_CONFIG_SEL is connected to GND because we don't use this

decoupling = [
    myelin_kicad_pcb.C0402("100n", "3V3", "GND", ref="C%d" % r)
    for r in range(10, 24)
]
bulk = [
    myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C%d" % r, handsoldering=False)
    for r in range(8, 10)
]

# connectors

connectors = [
    myelin_kicad_pcb.Component(
        footprint="header_4x10_100mil",
        identifier="CON1",
        value="top",
        pins=[
            Pin( 1, "", "IO23"),
            Pin( 2, "", "IO22"),
            Pin( 3, "", "IO27"),
            Pin( 4, "", "GND"),
            Pin( 5, "", "pin5"),
            Pin( 6, "", "IO45"),
            Pin( 7, "", "IO65"),
            Pin( 8, "", "GND"),
            Pin( 9, "", "pin9"),
            Pin(10, "", "pin10"),
            Pin(11, "", "IO46"),
            Pin(12, "", "pin12"),
            Pin(13, "", "pin13"),
            Pin(14, "", "pin14"),
            Pin(15, "", "pin15"),
            Pin(16, "", "pin16"),
            Pin(17, "", "pin17"),
            Pin(18, "", "pin18"),
            Pin(19, "", "pin19"),
            Pin(20, "", "pin20"),
            Pin(21, "", "pin21"),
            Pin(22, "", "pin22"),
            Pin(23, "", "pin23"),
            Pin(24, "", "pin24"),
            Pin(25, "", "pin25"),
            Pin(26, "", "pin26"),
            Pin(27, "", "pin27"),
            Pin(28, "", "pin28"),
            Pin(29, "", "pin29"),
            Pin(30, "", "pin30"),
            Pin(31, "", "pin31"),
            Pin(32, "", "3V3"),
            Pin(33, "", "pin33"),
            Pin(34, "", "pin34"),
            Pin(35, "", "3V3"),
            Pin(36, "", "pin36"),
            Pin(37, "", "pin37"),
            Pin(38, "", "pin38"),
            Pin(39, "5V", "NC-1-39"),
            Pin(40, "", "GND"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_2x06_100mil",
        identifier="CON2",
        value="left",
        pins=[
            Pin( 1, "", "IO24"),
            Pin( 2, "", "fpga_nSTATUS"),
            Pin( 3, "", "IO86"),
            Pin( 4, "", "IO63"),
            Pin( 5, "", "IO25"),
            Pin( 6, "", "GND"),
            Pin( 7, "", "fpga_TCK"),
            Pin( 8, "", "fpga_TDI"),
            Pin( 9, "", "fpga_TDO"),
            Pin(10, "", "IO66"),
            Pin(11, "", "IO28"),
            Pin(12, "", "VREFB2N0"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_2x06_100mil",
        identifier="CON3",
        value="right",
        pins=[
            Pin( 1, "", "pin1"),
            Pin( 2, "", "pin2"),
            Pin( 3, "", "pin3"),
            Pin( 4, "", "pin4"),
            Pin( 5, "", "pin5"),
            Pin( 6, "", "pin6"),
            Pin( 7, "", "pin7"),
            Pin( 8, "", "pin8"),
            Pin( 9, "", "pin9"),
            Pin(10, "", "pin10"),
            Pin(11, "", "pin11"),
            Pin(12, "", "pin12"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_4x10_100mil",
        identifier="CON4",
        value="bottom",
        pins=[
            Pin( 1, "", "3V3"),
            Pin( 2, "", "GND"),
            Pin( 3, "", "IO67"),
            Pin( 4, "", "IO30"),
            Pin( 5, "", "3V3"),
            Pin( 6, "", "IO69"),
            Pin( 7, "", "IO53"),
            Pin( 8, "", "IO32"),
            Pin( 9, "", "GND"),
            Pin(10, "", "pin10"),
            Pin(11, "", "pin11"),
            Pin(12, "", "pin12"),
            Pin(13, "", "pin13"),
            Pin(14, "", "pin14"),
            Pin(15, "", "pin15"),
            Pin(16, "", "pin16"),
            Pin(17, "", "pin17"),
            Pin(18, "", "pin18"),
            Pin(19, "", "pin19"),
            Pin(20, "", "pin20"),
            Pin(21, "", "pin21"),
            Pin(22, "", "pin22"),
            Pin(23, "", "pin23"),
            Pin(24, "", "pin24"),
            Pin(25, "", "pin25"),
            Pin(26, "", "pin26"),
            Pin(27, "", "pin27"),
            Pin(28, "", "pin28"),
            Pin(29, "5V", "NC-4-29"),
            Pin(30, "", "pin30"),
            Pin(31, "", "pin31"),
            Pin(32, "", "pin32"),
            Pin(33, "", "pin33"),
            Pin(34, "", "pin34"),
            Pin(35, "", "pin35"),
            Pin(36, "", "pin36"),
            Pin(37, "", "pin37"),
            Pin(38, "", "pin38"),
            Pin(39, "", "pin39"),
            Pin(40, "", "pin40"),

        ],
    ),
]

# time to tidy up!

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(7)
]

myelin_kicad_pcb.dump_netlist("bga_in_two_layers.net")
