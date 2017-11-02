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
# Minus One
# ---------

# by Phillip Pearson

# Simple Plus 1 replacement -- just three cartridge slots, using a CPLD to
# replace all discrete logic.  Implements all the cartridge signals except
# nROMSTB, and maps the third cartridge in as banks 4-5.

# For the next revision:
# - use a 64 or 100 pin CPLD
# - provide a separate nOE2 line for each cartridge
# Wishlist:
# - SD card slot
# - Serial port (or atmega32u4 or lpc11u12 for USB serial + JTAG)

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

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

# Expansion connector to go to the Electron
expansion_connector = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_48pin_expansion_connector",
    identifier="CON_EXP",
    value="expansion port connector",
    pins=[
        Pin(1, "18V_AC"),
        Pin(2, "18V_AC"),
        Pin(3, "AC_RET"),
        Pin(4, "AC_RET"),
        Pin(5, "-5V", ["-5V"]),
        Pin(6, "-5V", ["-5V"]),
        Pin(7, "GND", ["GND"]),
        Pin(8, "GND", ["GND"]),
        Pin(9, "5V", ["5V"]),
        Pin(10, "5V", ["5V"]),
        Pin(11, "SOUND_OUT", ["SOUND_OUT"]),
        Pin(12, "16MHZ", ["16MHZ"]),
        Pin(13, "16MHZ_DIV13"),
        Pin(14, "PHI0", ["PHI0"]),
        Pin(15, "nRST", ["nRST"]),
        Pin(16, "nNMI", ["nNMI"]),
        Pin(17, "nIRQ", ["nIRQ"]),
        Pin(18, "RnW", ["RnW"]),
        Pin(19, "D7", ["D7"]),
        Pin(20, "D6", ["D6"]),
        Pin(21, "D5", ["D5"]),
        Pin(22, "D4", ["D4"]),
        Pin(23, "D3", ["D3"]),
        Pin(24, "D2", ["D2"]),
        Pin(25, "D1", ["D1"]),
        Pin(26, "D0", ["D0"]),
        Pin(27, "nRDY", ["nRDY"]),
        Pin(28, "NC"),
        # --- slot ---
        Pin(31, "A15", ["A15"]),
        Pin(32, "A14", ["A14"]),
        Pin(33, "A13", ["A13"]),
        Pin(34, "A12", ["A12"]),
        Pin(35, "A11", ["A11"]),
        Pin(36, "A10", ["A10"]),
        Pin(37, "A9", ["A9"]),
        Pin(38, "A0", ["A0"]),
        Pin(39, "A1", ["A1"]),
        Pin(40, "A2", ["A2"]),
        Pin(41, "A3", ["A3"]),
        Pin(42, "A4", ["A4"]),
        Pin(43, "A5", ["A5"]),
        Pin(44, "A6", ["A6"]),
        Pin(45, "A7", ["A7"]),
        Pin(46, "A8", ["A8"]),
        Pin(47, "GND", ["GND"]),
        Pin(48, "GND", ["GND"]),
        Pin(49, "5V", ["5V"]),
        Pin(50, "5V", ["5V"]),
    ],
)

slot_0 = myelin_kicad_pcb.Component(
	footprint="myelin-kicad:acorn_electron_cartridge_socket",
	identifier="CART0",
	value="cartridge port",
	pins=[
        Pin("A1", "5V", ["5V"]),
        Pin("A2", "nOE", ["cart0_nOE"]),
        Pin("A3", "nRST", ["nRST"]),
        Pin("A4", "CSRW", ["RnW"]),
        Pin("A5", "A8", ["A8"]),
        Pin("A6", "A13", ["A13"]),
        Pin("A7", "A12", ["A12"]),
        Pin("A8", "PHI0", ["PHI0"]),
        Pin("A9", "-5V", ["-5V"]),
        Pin("A10", "NC"),
        Pin("A11", "nRDY", ["nRDY"]),
        Pin("A12", "nNMI", ["nNMI"]),
        Pin("A13", "nIRQ", ["nIRQ"]),
        Pin("A14", "nINFC", ["cart_nINFC"]),
        Pin("A15", "nINFD", ["cart_nINFD"]),
        Pin("A16", "ROMQA", ["cart_ROMQA"]),
        Pin("A17", "16MHZ", ["16MHZ"]),
        Pin("A18", "nROMSTB", ["cart_nROMSTB"]),
        Pin("A19", "ADOUT", ["SOUND_OUT"]),
        Pin("A20", "AGND", ["GND"]),
        Pin("A21", "ADIN", ["ADIN"]),
        Pin("A22", "GND", ["GND"]),
        Pin("B1", "5V", ["5V"]),
        Pin("B2", "A10", ["A10"]),
        Pin("B3", "D3", ["D3"]),
        Pin("B4", "A11", ["A11"]),
        Pin("B5", "A9", ["A9"]),
        Pin("B6", "D7", ["D7"]),
        Pin("B7", "D6", ["D6"]),
        Pin("B8", "D5", ["D5"]),
        Pin("B9", "D4", ["D4"]),
        Pin("B10", "nOE2", ["cart_nOE2"]),
        Pin("B11", "BA7", ["A7"]),
        Pin("B12", "BA6", ["A6"]),
        Pin("B13", "BA5", ["A5"]),
        Pin("B14", "BA4", ["A4"]),
        Pin("B15", "BA3", ["A3"]),
        Pin("B16", "BA2", ["A2"]),
        Pin("B17", "BA1", ["A1"]),
        Pin("B18", "BA0", ["A0"]),
        Pin("B19", "D0", ["D0"]),
        Pin("B20", "D2", ["D2"]),
        Pin("B21", "D1", ["D1"]),
        Pin("B22", "GND", ["GND"]),
	],
)

slot_2 = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_cartridge_socket",
    identifier="CART2",
    value="cartridge port",
    pins=[
        Pin("A1", "5V", ["5V"]),
        Pin("A2", "nOE", ["cart2_nOE"]),
        Pin("A3", "nRST", ["nRST"]),
        Pin("A4", "CSRW", ["RnW"]),
        Pin("A5", "A8", ["A8"]),
        Pin("A6", "A13", ["A13"]),
        Pin("A7", "A12", ["A12"]),
        Pin("A8", "PHI0", ["PHI0"]),
        Pin("A9", "-5V", ["-5V"]),
        Pin("A10", "NC"),
        Pin("A11", "nRDY", ["nRDY"]),
        Pin("A12", "nNMI", ["nNMI"]),
        Pin("A13", "nIRQ", ["nIRQ"]),
        Pin("A14", "nINFC", ["cart_nINFC"]),
        Pin("A15", "nINFD", ["cart_nINFD"]),
        Pin("A16", "ROMQA", ["cart_ROMQA"]),
        Pin("A17", "16MHZ", ["16MHZ"]),
        Pin("A18", "nROMSTB", ["cart_nROMSTB"]),
        Pin("A19", "ADOUT", ["SOUND_OUT"]),
        Pin("A20", "AGND", ["GND"]),
        Pin("A21", "ADIN", ["ADIN"]),
        Pin("A22", "GND", ["GND"]),
        Pin("B1", "5V", ["5V"]),
        Pin("B2", "A10", ["A10"]),
        Pin("B3", "D3", ["D3"]),
        Pin("B4", "A11", ["A11"]),
        Pin("B5", "A9", ["A9"]),
        Pin("B6", "D7", ["D7"]),
        Pin("B7", "D6", ["D6"]),
        Pin("B8", "D5", ["D5"]),
        Pin("B9", "D4", ["D4"]),
        Pin("B10", "nOE2", ["cart_nOE2"]),
        Pin("B11", "BA7", ["A7"]),
        Pin("B12", "BA6", ["A6"]),
        Pin("B13", "BA5", ["A5"]),
        Pin("B14", "BA4", ["A4"]),
        Pin("B15", "BA3", ["A3"]),
        Pin("B16", "BA2", ["A2"]),
        Pin("B17", "BA1", ["A1"]),
        Pin("B18", "BA0", ["A0"]),
        Pin("B19", "D0", ["D0"]),
        Pin("B20", "D2", ["D2"]),
        Pin("B21", "D1", ["D1"]),
        Pin("B22", "GND", ["GND"]),
    ],
)

slot_4 = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_cartridge_socket",
    identifier="CART4",
    value="cartridge port",
    pins=[
        Pin("A1", "5V", ["5V"]),
        Pin("A2", "nOE", ["cart4_nOE"]),
        Pin("A3", "nRST", ["nRST"]),
        Pin("A4", "CSRW", ["RnW"]),
        Pin("A5", "A8", ["A8"]),
        Pin("A6", "A13", ["A13"]),
        Pin("A7", "A12", ["A12"]),
        Pin("A8", "PHI0", ["PHI0"]),
        Pin("A9", "-5V", ["-5V"]),
        Pin("A10", "NC"),
        Pin("A11", "nRDY", ["nRDY"]),
        Pin("A12", "nNMI", ["nNMI"]),
        Pin("A13", "nIRQ", ["nIRQ"]),
        Pin("A14", "nINFC", ["cart_nINFC"]),
        Pin("A15", "nINFD", ["cart_nINFD"]),
        Pin("A16", "ROMQA", ["cart_ROMQA"]),
        Pin("A17", "16MHZ", ["16MHZ"]),
        Pin("A18", "nROMSTB", ["cart_nROMSTB"]),
        Pin("A19", "ADOUT", ["SOUND_OUT"]),
        Pin("A20", "AGND", ["GND"]),
        Pin("A21", "ADIN", ["ADIN"]),
        Pin("A22", "GND", ["GND"]),
        Pin("B1", "5V", ["5V"]),
        Pin("B2", "A10", ["A10"]),
        Pin("B3", "D3", ["D3"]),
        Pin("B4", "A11", ["A11"]),
        Pin("B5", "A9", ["A9"]),
        Pin("B6", "D7", ["D7"]),
        Pin("B7", "D6", ["D6"]),
        Pin("B8", "D5", ["D5"]),
        Pin("B9", "D4", ["D4"]),
        Pin("B10", "nOE2", ["cart_nOE2"]),
        Pin("B11", "BA7", ["A7"]),
        Pin("B12", "BA6", ["A6"]),
        Pin("B13", "BA5", ["A5"]),
        Pin("B14", "BA4", ["A4"]),
        Pin("B15", "BA3", ["A3"]),
        Pin("B16", "BA2", ["A2"]),
        Pin("B17", "BA1", ["A1"]),
        Pin("B18", "BA0", ["A0"]),
        Pin("B19", "D0", ["D0"]),
        Pin("B20", "D2", ["D2"]),
        Pin("B21", "D1", ["D1"]),
        Pin("B22", "GND", ["GND"]),
    ],
)

# via arrays to stable top/bottom GND planes together!
for n in (1, 2):
    stapler = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_zigzag_1x44_2.54mm",
        identifier="staple%d" % n,
        value="",
        pins=[Pin(n+1, "GND", ["GND"]) for n in range(44)],
    )
for n in range(33):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

# cpld needs:
# A15-8, A3-0 (nice to have 7-4 too)
# looks like plus 1 doesn't look at A7-4.  writing bank happens when D7-4="0000".
# D7-0
# PHI0, RnW
# cart0_nOE, cart2_nOE, cart_nOE2, cart_ROMQA, cart_nROMSTB, cart_nINFC, cart_nINFD
# that's 33 so far incl A7-4, so we're okay.  could add one more cart, or two if we skip A7-4.

cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="CPLD",
    value="XC9572XL",
    # Prefixes used by update_xilinx_constraints to turn pin names like elk_D0 into
    # signal IDs like elk_D<0> in constraints.ucf:
    buses=["D"],
    pins=[
        Pin(39, "P1.2", ["cart_nINFC"]),
        Pin(40, "P1.5", ["RnW"]),
        Pin(41, "P1.6", ["cart2_nOE"]),
        Pin(42, "P1.8", ["A11"]),
        Pin(43, "P1.9-GCK1", ["PHI0"]), # pin-locked ### crosstalk-sensitive
        Pin(44, "P1.11-GCK2", ["A10"]),
        Pin(1, "P1.14-GCK3", ["cart_nOE2"]),
        Pin(2, "P1.15", ["A3"]),
        Pin(3, "P1.17", ["A2"]),
        Pin(4, "GND", ["GND"]),
        Pin(5, "P3.2", ["A1"]),
        Pin(6, "P3.5", ["A0"]),
        Pin(7, "P3.8", ["A8"]),
        Pin(8, "P3.9", ["A13"]),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "TMS", ["cpld_TMS"]),
        Pin(11, "TCK", ["cpld_TCK"]), ### crosstalk-sensitive
        Pin(12, "P3.11", ["A12"]),
        Pin(13, "P3.14", ["cart_nROMSTB"]),
        Pin(14, "P3.15", ["cart_ROMQA"]),
        Pin(15, "VCCINT_3V3", ["3V3"]),
        Pin(16, "P3.17", ["A9"]),
        Pin(17, "GND", ["GND"]),
        Pin(18, "P3.16", ["cart4_nOE"]),
        Pin(19, "P4.2", ["A15"]),
        Pin(20, "P4.5", ["A14"]),
        Pin(21, "P4.8", ["GPIO1"]),
        Pin(22, "P4.11", ["GPIO2"]),
        Pin(23, "P4.14", ["GPIO3"]),
        Pin(24, "TDO", ["cpld_TDO"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(27, "P4.15", ["cart0_nOE"]),
        Pin(28, "P4.17", ["D0"]),
        Pin(29, "P2.2", ["D1"]),
        Pin(30, "P2.5", ["D2"]),
        Pin(31, "P2.6", ["D3"]),
        Pin(32, "P2.8", ["D4"]),
        Pin(33, "P2.9-GSR", ["nRST"]), # pin-locked ### crosstalk-sensitive
        Pin(34, "P2.11-GTS2", ["D5"]),
        Pin(35, "VCCINT_3V3", ["3V3"]),
        Pin(36, "P2.14-GTS1", ["D6"]),
        Pin(37, "P2.15", ["D7"]),
        Pin(38, "P2.17", ["cart_nINFD"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C1")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
cpld_cap3 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C3")
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, "../cpld/constraints.ucf"))

cpld_jtag = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm",
    identifier="JTAG",
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

regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT89-3_Housing",
    identifier="REG",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "5V", "GND", ref="C4")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C5")

myelin_kicad_pcb.dump_netlist("minus_one.net")
