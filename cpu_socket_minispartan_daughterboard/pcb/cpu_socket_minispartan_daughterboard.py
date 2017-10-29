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

# ------------------------------------
# cpu_socket_minispartan_daughterboard
# ------------------------------------

# by Phillip Pearson

# This plugs into a cpu_socket_expansion board and allows a Scarab
# miniSpartan6+ board to be plugged in on top.  It will almost certainly
# prevent the Electron's case from closing.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


connector = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x20_Pitch2.54mm",
    identifier="CON",
    value="2x20 connector for daughterboard",
    pins=[
        Pin( "1", "", ["ext_GP0"]),
        Pin( "2", "", ["ext_GP1"]),
        Pin( "3", "", ["ext_GP2"]),
        Pin( "4", "", ["ext_GP3"]),
        Pin( "5", "", ["ext_GP4"]),
        Pin( "6", "", ["ext_GP5"]),
        Pin( "7", "", ["ext_GP6"]),
        Pin( "8", "", ["ext_GP7"]),
        Pin( "9", "", ["ext_GP8"]),
        Pin("10", "", ["ext_GP9"]),
        Pin("11", "", ["ext_GP10"]),
        Pin("12", "", ["ext_GP11"]),
        Pin("13", "", ["ext_GP12"]),
        Pin("14", "", ["GND"]),
        Pin("15", "", ["ext_3V3"]),
        Pin("16", "", ["ext_5V"]),
        Pin("17", "", ["ext_D0"]),
        Pin("18", "", ["ext_D1"]),
        Pin("19", "", ["ext_D2"]),
        Pin("20", "", ["ext_D3"]),
        Pin("21", "", ["ext_D4"]),
        Pin("22", "", ["ext_D5"]),
        Pin("23", "", ["ext_D6"]),
        Pin("24", "", ["ext_D7"]),
        Pin("25", "", ["ext_A0"]),
        Pin("26", "", ["ext_A1"]),
        Pin("27", "", ["ext_A2"]),
        Pin("28", "", ["ext_A3"]),
        Pin("29", "", ["ext_A4"]),
        Pin("30", "", ["ext_A5"]),
        Pin("31", "", ["ext_A6"]),
        Pin("32", "", ["ext_A7"]),
        Pin("33", "", ["ext_A8"]),
        Pin("34", "", ["ext_A9"]),
        Pin("35", "", ["ext_A10"]),
        Pin("36", "", ["ext_A11"]),
        Pin("37", "", ["ext_A12"]),
        Pin("38", "", ["ext_A13"]),
        Pin("39", "", ["ext_A14"]),
        Pin("40", "", ["ext_A15"]),
    ],
)

minispartan_5v_connector = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="MSP",
    value="bbc to minispartan 5v",
    pins=[
        Pin("1", "", ["minispartan_5v"]),
        Pin("2", "", ["ext_5V"]),
    ],
)

gpio = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x14_Pitch2.54mm",
    identifier="GPIO",
    value="some GPIO pins",
    pins=[
        Pin( "1", "", ["GND"]),
        Pin( "2", "", ["minispartan_C11"]),
        Pin( "3", "", ["minispartan_C9"]),
        Pin( "4", "", ["minispartan_C7"]),
        Pin( "5", "", ["minispartan_3V3e"]),
        Pin( "6", "", ["minispartan_C5"]),
        Pin( "7", "", ["minispartan_C3"]),
        Pin( "8", "", ["minispartan_C1"]),
        Pin( "9", "", ["GND"]),
        Pin("10", "", ["minispartan_B11"]),
        Pin("11", "", ["minispartan_B9"]),
        Pin("12", "", ["minispartan_B7"]),
        Pin("13", "", ["minispartan_3V3c"]),
        Pin("14", "", ["minispartan_B5"]),
    ],
)

minispartan = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:scarab_mini_spartan_6_lx25",
    identifier="FPGA",
    value="miniSpartan6+ board",
    pins=[
        # power
        Pin("5V0", "", ["minispartan_5v"]),
        Pin("3V3e", "", ["minispartan_3V3e"]),
        Pin("3V3c", "", ["minispartan_3V3c"]),
        Pin("GNDa", "", ["GND"]),
        Pin("GNDb", "", ["GND"]),
        Pin("GNDc", "", ["GND"]),
        Pin("GNDd", "", ["GND"]),
        Pin("GNDe", "", ["GND"]),
        Pin("GNDf", "", ["GND"]),
        Pin("GNDg", "", ["GND"]),
        Pin("GNDh", "", ["GND"]),
        Pin("GNDi", "", ["GND"]),
        Pin("GNDj", "", ["GND"]),
        Pin("GNDk", "", ["GND"]),
        Pin("GNDl", "", ["GND"]),
        Pin("GNDm", "", ["GND"]),
        Pin("GNDn", "", ["GND"]),

        # gpio connections
        Pin("C11", "", ["minispartan_C11"]),
        Pin("C9", "", ["minispartan_C9"]),
        Pin("C7", "", ["minispartan_C7"]),
        Pin("C5", "", ["minispartan_C5"]),
        Pin("C3", "", ["minispartan_C3"]),
        Pin("C1", "", ["minispartan_C1"]),
        Pin("B11", "", ["minispartan_B11"]),
        Pin("B9", "", ["minispartan_B9"]),
        Pin("B7", "", ["minispartan_B7"]),
        Pin("B5", "", ["minispartan_B5"]),


        # connections to the right hand side of the connector
        Pin("F11", "", ["ext_GP0"]),
        Pin("F9", "", ["ext_GP1"]),
        Pin("F7", "", ["ext_GP2"]),
        Pin("F5", "", ["ext_GP3"]),
        Pin("F3", "", ["ext_GP4"]),
        Pin("F1", "", ["ext_GP5"]),
        Pin("E11", "", ["ext_GP7"]),
        # Pin("E7", "", ["ext_GP7"]),
        Pin("E3", "", ["ext_GP9"]),
        Pin("E1", "", ["ext_GP11"]),
        Pin("D3", "", ["ext_D1"]),
        Pin("D1", "", ["ext_D3"]),

        # left connector from minispartan
        Pin("C10", "", ["ext_GP6"]),
        Pin("C8", "", ["ext_GP8"]),
        Pin("C6", "", ["ext_GP10"]),
        Pin("C4", "", ["ext_GP12"]),
        Pin("C2", "", ["ext_D0"]),
        Pin("C0", "", ["ext_D2"]),
        Pin("B10", "", ["ext_D5"]),
        Pin("B8", "", ["ext_D4"]),
        Pin("B6", "", ["ext_D7"]),
        Pin("B4", "", ["ext_D6"]),
        Pin("B3", "", ["ext_A0"]),
        Pin("B2", "", ["ext_A1"]),
        Pin("B1", "", ["ext_A2"]),
        Pin("B0", "", ["ext_A3"]),
        Pin("A11", "", ["ext_A4"]),
        Pin("A10", "", ["ext_A5"]),
        Pin("A9", "", ["ext_A6"]),
        Pin("A8", "", ["ext_A7"]),
        Pin("A7", "", ["ext_A8"]),
        Pin("A6", "", ["ext_A9"]),
        Pin("A5", "", ["ext_A10"]),
        Pin("A4", "", ["ext_A11"]),
        Pin("A3", "", ["ext_A12"]),
        Pin("A2", "", ["ext_A13"]),
        Pin("A1", "", ["ext_A14"]),
        Pin("A0", "", ["ext_A15"]),

        # right hand side: connections to PiTubeDirect
        Pin("F10", "", ["tube_A1"]),
        Pin("F8", "", ["tube_A2"]),
        Pin("F6", "", ["tube_nRST"]),
        Pin("F4", "", ["pi_serial_TX"]),
        Pin("F2", "", ["pi_serial_RX"]),
        Pin("F0", "", ["tube_nTUBE"]),
        Pin("E10", "", ["tube_RnW"]),
        Pin("E8", "", ["tube_A0"]),
        Pin("E9", "", ["tube_D4"]),
        Pin("E6", "", ["tube_D5"]),
        Pin("E7", "", ["tube_D6"]),
        Pin("E4", "", ["tube_D2"]),
        Pin("E5", "", ["tube_D1"]),
        Pin("E2", "", ["tube_D7"]),
        Pin("E0", "", ["tube_D3"]),
        Pin("D2", "", ["tube_D0"]),
        Pin("D0", "", ["tube_PHI0"]),
    ],
)

pi = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:raspberry_pi_zero_flipped",
    identifier="PI",
    value="Raspberry Pi Zero",
    pins=[
        #Pin(1, "3V3", ["3V3"]),
        #Pin(2, "5V", ["5V"]),
        Pin(3, "GPIO0-2", ["tube_A1"]),
        Pin(4, "5V", ["5V"]),
        Pin(5, "GPIO1-3", ["tube_A2"]),
        Pin(6, "ser_GND", ["pi_serial_GND"]),
        Pin(7, "GPIO4", ["tube_nRST"]),
        Pin(8, "ser_TX", ["pi_serial_TX"]),
        Pin(9, "GND", ["GND"]),
        Pin(10, "ser_RX", ["pi_serial_RX"]),
        Pin(11, "GPIO17", ["tube_nTUBE"]),
        Pin(12, "GPIO18", ["tube_RnW"]),
        Pin(13, "GPIO21-27", ["tube_A0"]),
        Pin(14, "GND", ["GND"]),
        Pin(15, "GPIO22", ["tube_D4"]),
        Pin(16, "GPIO23", ["tube_D5"]),
        Pin(17, "3V3", ["3V3"]),
        Pin(18, "GPIO24", ["tube_D6"]),
        Pin(19, "GPIO10", ["tube_D2"]),
        Pin(20, "GND", ["GND"]),
        Pin(21, "GPIO9", ["tube_D1"]),
        Pin(22, "GPIO25", ["tube_D7"]),
        Pin(23, "GPIO11", ["tube_D3"]),
        Pin(24, "GPIO8", ["tube_D0"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "GPIO7", ["tube_PHI0"]),
    ],
)

myelin_kicad_pcb.dump_netlist("cpu_socket_minispartan_daughterboard.net")
