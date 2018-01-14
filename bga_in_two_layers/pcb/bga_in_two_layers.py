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
        Pin("A2",  "", "C1_11"),
        Pin("A3",  "", "C1_9"),
        Pin("A4",  "", "C1_14"),
        Pin("A5",  "", "C1_19"),  # failed on first board?  nc
        Pin("A6",  "", "C1_17"),
        Pin("A7",  "", "C1_23"),
        Pin("A8",  "", "C1_16"),
        Pin("A9",  "", "C1_20"),
        Pin("A10", "", "C1_26"),
        Pin("A11", "", "C1_25"),
        Pin("A12", "", "C1_30"),
#        Pin("N2",  "", "IO11"),
#        Pin("N3",  "", "IO12"),
        Pin("N4",  "", "C4_17"),  # failed on first board?  nc
        Pin("N5",  "", "C4_19"),
        Pin("N6",  "", "C4_24"),
        Pin("N7",  "", "C4_25"),
        Pin("N8",  "", "C4_22"),
        Pin("N9",  "", "C4_28"),  # failed on first board?  low drive / poor connection?
        Pin("N10", "", "C4_26"),
        Pin("N11", "", "C4_31"),
        Pin("N12", "", "C4_36"),
        Pin("B1",  "", "C1_2"),  # failed on first board?  nc
        Pin("C1",  "", "C1_1"),
        Pin("D1",  "", "C2_1"),
        Pin("E1",  "", "C2_5"),
        Pin("F1",  "", "C2_8"),
        Pin("H1",  "", "C1_3"),
        Pin("J1",  "", "C4_4"),
        Pin("K1",  "", "C2_12"),
        Pin("M1",  "", "C4_12"),
        Pin("B13", "", "C1_36"),
        Pin("C13", "", "C1_33"),
        Pin("D13", "", "C1_37"),
        Pin("G13", "", "C3_4"),
        Pin("H13", "", "C4_34"),
        Pin("J13", "", "C3_10"),
        Pin("K13", "", "C4_35"),
        Pin("L13", "", "C4_37"),
        Pin("M13", "", "C4_39"),  # failed on first board?  nc

        # Next ring in -
        Pin("B2",  "", "C1_6"),
        Pin("B3",  "", "C1_5"),
        Pin("B4",  "", "C1_10"),
        Pin("B5",  "", "C1_13"),
        Pin("B6",  "", "C1_18"),
        Pin("B7",  "", "C1_12"),
        Pin("B10", "", "C1_24"),
        Pin("B11", "", "C1_31"),
        Pin("M2",  "", "C4_11"),
        Pin("M3",  "", "C4_13"),
        Pin("M4",  "", "C4_14"),
        Pin("M5",  "", "C4_20"),
        Pin("M7",  "", "C4_21"),
        Pin("M8",  "", "C4_23"),  # failed on first board?  nc
        Pin("M9",  "", "C4_33"),
        Pin("M10", "", "C4_27"),
        Pin("M11", "", "C4_30"),
        Pin("M12", "", "C4_38"),

        Pin("C2",  "", "C2_4"),
        Pin("H2",  "", "C1_7"),
        Pin("J2",  "", "C4_7"),
        Pin("K2",  "", "C4_8"),
        Pin("L2",  "", "C4_6"),
        Pin("L3",  "", "C4_10"),
        Pin("C9",  "", "C1_22"),
        Pin("C10", "", "C1_27"),
        Pin("B12", "", "C1_29"),
        Pin("C12", "", "C1_34"),
        Pin("D11", "", "C1_38"),
        Pin("D12", "", "C3_3"),
        Pin("E12", "", "C3_1"),
        Pin("F12", "", "C3_6"),
        Pin("G12", "", "C3_8"),
        Pin("J12", "", "C3_7"),
        Pin("K11", "", "C3_12"),
        Pin("K12", "", "C3_9"),
        Pin("L11", "", "C3_11"),
        Pin("L12", "", "C4_40"),
        Pin("L10", "", "C4_32"),
        Pin("C11", "", "C1_28"),
        Pin("E3",  "", "C2_3"),
        Pin("L5",  "", "C4_18"),

        # Special pins
        Pin("G5", "CLK0n", "CLK0n"),
        Pin("H6", "CLK0p", "CLK0p"),
        Pin("H5", "CLK1n", "CLK1n"),
        Pin("H4", "CLK1p", "CLK1p"),
        # Pin("G10", "CLK2n", "CLK2n"),
        # Pin("G9", "CLK2p", "CLK2p"),
        Pin("E13", "CLK3n", "C3_2_CLK3n"),
        Pin("F13", "CLK3p", "C3_5_CLK3p"),
        Pin("N2", "DPCLK0", "C4_16_DPCLK0"),
        Pin("N3", "DPCLK1", "C4_15_DPCLK1"),
        Pin("F10", "DPCLK2", "DPCLK2"),
        Pin("F9", "DPCLK3", "DPCLK3"),
        Pin("L1", "VREFB2N0", "C4_3_VREFB2N0"),

        # JTAG and other config pins
        Pin("E5",  "JTAGEN",     "fpga_JTAGEN"),
        Pin("G1",  "TMS",        "fpga_TMS"),
        Pin("G2",  "TCK",        "fpga_TCK"),
        Pin("F5",  "TDI",        "fpga_TDI"),
        Pin("F6",  "TDO",        "fpga_TDO"),
        Pin("B9",  "DEV_CLRn",   "fpga_DEV_CLRn"),  # measures high on first soldered board
        Pin("D8",  "DEV_OE",     "fpga_DEV_OE"),
        Pin("D7",  "CONFIG_SEL", "GND"),  # unused, so connected to GND
        Pin("E7",  "nCONFIG",    "3V3"),  # can be connected straight to VCCIO
        Pin("D6",  "CRC_ERROR",  "GND"),  # WARNING: disable Error Detection CRC option
        Pin("C4",  "nSTATUS",    "fpga_nSTATUS"),  # measures high on first soldered board
        Pin("C5",  "CONF_DONE",  "fpga_CONF_DONE"),  # measures high on first soldered board

        # Signals used as power/ground to enable vias
        Pin("E4",  "",     "GND"),
        Pin("J5",  "",     "GND"),
        Pin("J6",  "",     "GND"),
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
            Pin( 1, "", "C1_1"),
            Pin( 2, "", "C1_2"),
            Pin( 3, "", "C1_3"),
            Pin( 4, "", "GND"),
            Pin( 5, "", "C1_5"),
            Pin( 6, "", "C1_6"),
            Pin( 7, "", "C1_7"),
            Pin( 8, "", "GND"),
            Pin( 9, "", "C1_9"),
            Pin(10, "", "C1_10"),
            Pin(11, "", "C1_11"),
            Pin(12, "", "C1_12"),
            Pin(13, "", "C1_13"),
            Pin(14, "", "C1_14"),
            Pin(15, "", "fpga_CONF_DONE"),
            Pin(16, "", "C1_16"),
            Pin(17, "", "C1_17"),
            Pin(18, "", "C1_18"),
            Pin(19, "", "C1_19"),
            Pin(20, "", "C1_20"),
            Pin(21, "", "fpga_DEV_CLRn"),
            Pin(22, "", "C1_22"),
            Pin(23, "", "C1_23"),
            Pin(24, "", "C1_24"),
            Pin(25, "", "C1_25"),
            Pin(26, "", "C1_26"),
            Pin(27, "", "C1_27"),
            Pin(28, "", "C1_28"),
            Pin(29, "", "C1_29"),
            Pin(30, "", "C1_30"),
            Pin(31, "", "C1_31"),
            Pin(32, "", "3V3"),
            Pin(33, "", "C1_33"),
            Pin(34, "", "C1_34"),
            Pin(35, "", "3V3"),
            Pin(36, "", "C1_36"),
            Pin(37, "", "C1_37"),
            Pin(38, "", "C1_38"),
            Pin(39, "5V", "NC-1-39"),
            Pin(40, "", "GND"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_2x06_100mil",
        identifier="CON2",
        value="left",
        pins=[
            Pin( 1, "", "C2_1"),
            Pin( 2, "", "fpga_nSTATUS"),
            Pin( 3, "", "C2_3"),
            Pin( 4, "", "C2_4"),
            Pin( 5, "", "C2_5"),
            Pin( 6, "", "GND"),
            Pin( 7, "", "fpga_TCK"),
            Pin( 8, "", "C2_8"),
            Pin( 9, "", "fpga_TDI"),
            Pin(10, "", "fpga_TDO"),
            Pin(11, "", "fpga_TMS"),
            Pin(12, "", "C2_12"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_2x06_100mil",
        identifier="CON3",
        value="right",
        pins=[
            Pin( 1, "", "C3_1"),
            Pin( 2, "", "C3_2_CLK3n"),
            Pin( 3, "", "C3_3"),
            Pin( 4, "", "C3_4"),
            Pin( 5, "", "C3_5_CLK3p"),
            Pin( 6, "", "C3_6"),
            Pin( 7, "", "C3_7"),
            Pin( 8, "", "C3_8"),
            Pin( 9, "", "C3_9"),
            Pin(10, "", "C3_10"),
            Pin(11, "", "C3_11"),
            Pin(12, "", "C3_12"),
        ],
    ),
    myelin_kicad_pcb.Component(
        footprint="header_4x10_100mil",
        identifier="CON4",
        value="bottom",
        pins=[
            Pin( 1, "", "3V3"),
            Pin( 2, "", "GND"),
            Pin( 3, "", "C4_3_VREFB2N0"),
            Pin( 4, "", "C4_4"),
            Pin( 5, "", "3V3"),
            Pin( 6, "", "C4_6"),
            Pin( 7, "", "C4_7"),
            Pin( 8, "", "C4_8"),
            Pin( 9, "", "GND"),
            Pin(10, "", "C4_10"),
            Pin(11, "", "C4_11"),
            Pin(12, "", "C4_12"),
            Pin(13, "", "C4_13"),
            Pin(14, "", "C4_14"),
            Pin(15, "", "C4_15_DPCLK1"),
            Pin(16, "", "C4_16_DPCLK0"),
            Pin(17, "", "C4_17"),
            Pin(18, "", "C4_18"),
            Pin(19, "", "C4_19"),
            Pin(20, "", "C4_20"),
            Pin(21, "", "C4_21"),
            Pin(22, "", "C4_22"),
            Pin(23, "", "C4_23"),
            Pin(24, "", "C4_24"),
            Pin(25, "", "C4_25"),
            Pin(26, "", "C4_26"),
            Pin(27, "", "C4_27"),
            Pin(28, "", "C4_28"),
            Pin(29, "5V", "NC-4-29"),
            Pin(30, "", "C4_30"),
            Pin(31, "", "C4_31"),
            Pin(32, "", "C4_32"),
            Pin(33, "", "C4_33"),
            Pin(34, "", "C4_34"),
            Pin(35, "", "C4_35"),
            Pin(36, "", "C4_36"),
            Pin(37, "", "C4_37"),
            Pin(38, "", "C4_38"),
            Pin(39, "", "C4_39"),
            Pin(40, "", "C4_40"),

        ],
    ),
]

myelin_kicad_pcb.dump_netlist("bga_in_two_layers.net")
