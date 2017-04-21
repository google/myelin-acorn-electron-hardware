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
# elk_pi_tube_direct
# ----------------------------------------------

# by Phillip Pearson

# Acorn Electron cartridge providing address decoding and level shifting for a
# Raspberry Pi running PiTubeDirect.

# This turned out to be super simple... my favourite CPLD (XC9572XL) has just
# enough pins that we don't need an external level shifter, and the Pi Zero
# will regulate the 5V power supply down to 3.3V for us, so we don't even need
# a regulator :)

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Cartridge connector
cart = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_cartridge_edge_connector",
    identifier="CART1",
    value="edge connector",
    pins=[
        # front of cartridge / bottom layer of PCB
        Pin("B1", "5V", ["elk_5V"]),
        Pin("B2", "A10"),
        Pin("B3", "D3", ["elk_D3"]),
        Pin("B4", "A11"),
        Pin("B5", "A9"),
        Pin("B6", "D7", ["elk_D7"]),
        Pin("B7", "D6", ["elk_D6"]),
        Pin("B8", "D5", ["elk_D5"]),
        Pin("B9", "D4", ["elk_D4"]),
        Pin("B10", "nOE2"),
        Pin("B11", "BA7", ["elk_A7"]),
        Pin("B12", "BA6", ["elk_A6"]),
        Pin("B13", "BA5", ["elk_A5"]),
        Pin("B14", "BA4", ["elk_A4"]),
        Pin("B15", "BA3"),
        Pin("B16", "BA2", ["elk_A2"]),
        Pin("B17", "BA1", ["elk_A1"]),
        Pin("B18", "BA0", ["elk_A0"]),
        Pin("B19", "D0", ["elk_D0"]),
        Pin("B20", "D2", ["elk_D2"]),
        Pin("B21", "D1", ["elk_D1"]),
        Pin("B22", "GND", ["GND"]),
        # rear of cartridge / top layer of PCB
        Pin("A1", "5V", ["elk_5V"]),
        Pin("A2", "nOE"),
        Pin("A3", "nRST", ["elk_nRST"]),
        Pin("A4", "RnW", ["elk_RnW"]),
        Pin("A5", "A8"),
        Pin("A6", "A13"),
        Pin("A7", "A12"),
        Pin("A8", "PHI0", ["elk_PHI0"]),
        Pin("A9", "-5V"),
        Pin("A10", "NC"),
        Pin("A11", "nRDY"),
        Pin("A12", "nNMI"),
        Pin("A13", "nIRQ"),
        Pin("A14", "nINFC", ["elk_nINFC"]),
        Pin("A15", "nINFD"),
        Pin("A16", "ROMQA"),
        Pin("A17", "16MHZ"),
        Pin("A18", "nROMSTB"),
        Pin("A19", "ADOUT"),
        Pin("A20", "ADGND"),
        Pin("A21", "ADIN"),
        Pin("A22", "GND", ["GND"]),
    ],
)

# TODO: footprint for pi zero
# https://www.adafruit.com/products/2222
# 2x20 female socket, for the pi to plug into (upside down probably?)
pi_zero = myelin_kicad_pcb.Component(
	footprint="myelin-kicad:raspberry_pi_zero_flipped",
	identifier="PI1",
	value="Raspberry Pi Zero",
	pins=[
		Pin(1, "3V3", ["3V3"]),
		Pin(2, "5V", ["5V"]),
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

serial_port = myelin_kicad_pcb.Component(
	footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
	identifier="SERIAL1",
	value="Pi Serial",
	pins=[
		Pin(1, "GND", ["pi_serial_GND"]),
		Pin(2, "TX", ["pi_serial_TX"]),
		Pin(3, "RX", ["pi_serial_RX"]),
	],
)

# CPLD glue: Xilinx XC9572XL-10VQG44
# https://www.xilinx.com/support/documentation/data_sheets/ds057.pdf
# VQ44 package: https://www.xilinx.com/support/documentation/package_specs/vq44.pdf
cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="PL1",
    value="XC9572XL",
    # Prefixes used by update_xilinx_constraints to turn pin names like elk_D0 into
    # signal IDs like elk_D<0> in constraints.ucf:
    buses=["elk_D", "tube_D"],
    pins=[
        # change ../cpld/constraints.ucf if any pinouts change

        # when prototyping on the lc-technology xc9572xl board, P1 (clk) - P23 are on
        # one side, and P27 - P44 are on the other.

        # colours of wires connecting to CPLD prototype board:

        # data:
        # 0 purple
        # 1 blue
        # 2 green
        # 3 yellow
        # 4 orange
        # 5 red
        # 6 brown
        # 7 black

        # addr:
        # 0 white
        # 1 grey
        # 2 purple
        # 4 blue
        # 5 green
        # 6 yellow
        # 7 orange

        # reset white
        # phi0 grey
        # ninfc brown
        # rnw red

        # NET LED2 LOC = P34; # tube_RnW
        # NET LED3 LOC = P33; # tube_nTUBE
        # NET LED4 LOC = P32; # tube_A0
        # NET LED5 LOC = P31; # tube_D5

        Pin(39, "P1.2", ["elk_D3"]),
        Pin(40, "P1.5", ["elk_nRST"]),
        Pin(41, "P1.6", ["elk_RnW"]),
        Pin(42, "P1.8", ["elk_D7"]),
        Pin(43, "P1.9-GCK1", ["elk_D6"]),
        Pin(44, "P1.11-GCK2", ["elk_D5"]),
        Pin(1, "P1.14-GCK3", ["elk_PHI0"]),
        Pin(2, "P1.15", ["elk_D4"]),
        Pin(3, "P1.17", ["elk_A7"]),
        Pin(4, "GND", ["GND"]),
        Pin(5, "P3.2", ["elk_A6"]),
        Pin(6, "P3.5", ["elk_A5"]),
        Pin(7, "P3.8", ["elk_A4"]),
        Pin(8, "P3.9", ["elk_nINFC"]),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "TMS", ["cpld_TMS"]),
        Pin(11, "TCK", ["cpld_TCK"]),
        Pin(12, "P3.11", ["elk_A2"]),
        Pin(13, "P3.14", ["elk_A1"]),
        Pin(14, "P3.15", ["elk_A0"]),
        Pin(15, "VCCINT_3V3", ["3V3"]),
        Pin(16, "P3.17", ["elk_D0"]),
        Pin(17, "GND", ["GND"]),
        Pin(18, "P3.16", ["elk_D2"]),
        Pin(19, "P4.2", ["elk_D1"]),
        Pin(20, "P4.5", ["tube_PHI0"]),
        Pin(21, "P4.8", ["tube_D3"]),
        Pin(22, "P4.11", ["tube_D0"]),
        Pin(23, "P4.14", ["tube_D1"]),
        Pin(24, "TDO", ["cpld_TDO"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(27, "P4.15", ["tube_D7"]),
        Pin(28, "P4.17", ["tube_D2"]),
        Pin(29, "P2.2", ["tube_D6"]),
        Pin(30, "P2.5", ["tube_D4"]),
        Pin(31, "P2.6", ["tube_D5"]),
        Pin(32, "P2.8", ["tube_A0"]),
        Pin(33, "P2.9-GSR", ["tube_nTUBE"]),
        Pin(34, "P2.11-GTS2", ["tube_RnW"]),
        Pin(35, "VCCINT_3V3", ["3V3"]),
        Pin(36, "P2.14-GTS1", ["tube_nRST"]),
        Pin(37, "P2.15", ["tube_A2"]),
        Pin(38, "P2.17", ["tube_A1"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C1")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
cpld_cap3 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C5")
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, "../cpld/constraints.ucf"))

# altera jtag header, like in the lc-electronics xc9572xl board
# left column: tck tdo tms nc tdi
# right column: gnd vcc nc nc gnd
cpld_jtag = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm",
    identifier="JTAG1",
    value="jtag",
    pins=[
        Pin(1, "TCK", ["cpld_TCK"]), # top left
        Pin(2, "GND", ["GND"]), # top right
        Pin(3, "TDO", ["cpld_TDO"]),
        Pin(4, "3V3", ["3V3"]),
        Pin(5, "TMS", ["cpld_TMS"]),
        Pin(6, "NC"),
        Pin(7, "NC"),
        Pin(8, "NC"),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "GND", ["GND"]),
    ],
)

# Jumper to connect 5v power from the Electron to the Pi Zero.
# Plus 1 cartridges aren't meant to draw more than 50 mA, and the Pi Zero
# typically needs ~150 mA, so this should probably be left unconnected,
# with a separate PSU supplying the Pi.
power_jumper = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="POWER1",
    value="Elk-Pi 5V",
    pins=[
        Pin(1, "A", ["5V"]),
        Pin(2, "B", ["elk_5V"]),
    ],
)

# Just in case we want to connect up an ext PSU for CPLD programming
ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
    pins=[
        Pin(1, "A", ["GND"]),
        Pin(2, "B", ["3V3"]),
        Pin(3, "C", ["5V"]),
    ],
)

myelin_kicad_pcb.dump_netlist("elk_pi_tube_direct.net")
