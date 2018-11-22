#!/usr/bin/python

# Copyright 2018 Google Inc.
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
# a3000_rom_emulator
# ------------------

# by Phillip Pearson

# A board that replaces the 4 x 512kB ROM chips in the A3000 with a flash chip
# and a big CPLD, to allow it to be updated without removing it from the machine.

PROJECT_NAME = "a3000_rom_emulator"
PATH_TO_CPLD = "../cpld"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# TODO consider DFM - https://rheingoldheavy.com/design-assembly-kicad/
# TODO add 3 x FID
# TODO add soldermask chevrons in 3 corners of board to detect misregistration http://iconnect007.media/index.php/article/47987/soldermask-registration-considerations-for-fine-pitch-area-array-package-ass
# TODO make sure the BOM comes out OK

# (done) can I use BGA?  xc95144 comes in cs144 package, which is 0.8mm 12x12mm (c.f. 22x22mm for TQ144) and flash comes in 1mm pitch 13x11 64-ball BGA

# (done) Figure out how to correctly route the flash.  Can we use a daisy chain with stubs?  Rule of thumb from https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/an/an224.pdf is that TDstub < 1/3 of rise time.  In our case rise time is about 1.5-2ns, so worst case Tdstub should be < 0.5ns, so 7.5cm.

# TODO figure out how to correctly daisy chain all the flash address and control signals through the three BGAs. FLASH2/FLASH3 are the best bet so far: 8 data lines out top and bottom, 26 signals coming out the left side: A0-21 plus four.  need to get these out the right side too.

# TODO read stencil design guidelines in IPC-7525A

# TODO add power diodes so we can power from USB or arc
# TODO add 10k pullup for flash_READY
# TODO add 10k pullup for arc_nROMCS to help when not plugged in
# TODO add jumpers so we can get LA18, LA19 and LA20 from flying leads on pre-A3000 machines (IC28 on A3xx)
# TODO add pin to wire to A21, so we can support 4MB ROMs
# TODO add pin to wire to reset, so we can re-reset the machine once the board is alive
# TODO make footprint for xilinx_csg144
# TODO make footprint for s29 flash
# TODO add USB MCU (atsamd51 or 21?)
# TODO add 96MHz (64MHz?) oscillator footprint, in case we want that clock

# Notes on BGA soldering (I'm using NSMD everywhere):
# - https://forum.kicad.info/t/how-to-build-a-nsmd-footprint-in-kicad/4889/2
# - https://medium.com/supplyframe-hardware/confessions-of-a-pcb-designer-on-solder-mask-e592b45e5483

# (done) figure out what flash to use
    # CHOSEN: BGA-64 version of S29GL064S (cheapest and best).
    # previously picked S29GL064N90TFI040: $3.34, 64mbit, 48tsop,
    # 90+25ns access time, which was good enough, and the quicker
    # version still isn't quick enough for single cycle access on
    # a 12MHz bus (e.g. A5000).

# TODO switch to CSG144
cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_csg144",
    identifier="CPLD",
    value="XC95144XL-10CSG144",
    buses=[""],
    pins=[
        Pin( "A1", "",         ""),
        Pin( "A2", "",         ""),
        Pin( "A3", "",         ""),
        Pin( "A4", "",         ""),
        Pin( "A5", "",         ""),
        Pin( "A6", "",         ""),
        Pin( "A7", "",         ""),
        Pin( "A8", "",         ""),
        Pin( "A9", "",         ""),
        Pin("A10", "",         ""),
        Pin("A11", "",         ""),
        Pin("A12", "",         ""),
        Pin("A13", "",         ""),
        Pin( "B1", "",         ""),
        Pin( "B2", "",         ""),
        Pin( "B3", "",         ""),
        Pin( "B4", "",         ""),
        Pin( "B5", "",         ""),
        Pin( "B6", "",         ""),
        Pin( "B7", "",         ""),
        Pin( "B8", "",         ""),
        Pin( "B9", "",         ""),
        Pin("B10", "",         ""),
        Pin("B11", "",         ""),
        Pin("B12", "",         ""),
        Pin("B13", "",         ""),
        Pin( "C1", "",         ""),
        Pin( "C2", "",         ""),
        Pin( "C3", "",         ""),
        Pin( "C4", "",         ""),
        Pin( "C5", "",         ""),
        Pin( "C6", "",         ""),
        Pin( "C7", "",         ""),
        Pin( "C8", "",         ""),
        Pin( "C9", "",         ""),
        Pin("C10", "",         ""),
        Pin("C11", "",         ""),
        Pin("C12", "",         ""),
        Pin("C13", "",         ""),
        Pin( "D1", "",         ""),
        Pin( "D2", "",         ""),
        Pin( "D3", "",         ""),
        Pin( "D4", "",         ""),
        Pin( "D5", "",         ""),
        Pin( "D6", "",         ""),
        Pin( "D7", "",         ""),
        Pin( "D8", "",         ""),
        Pin( "D9", "",         ""),
        Pin("D10", "",         ""),
        Pin("D11", "",         ""),
        Pin("D12", "",         ""),
        Pin("D13", "",         ""),

        Pin( "E1", "",         ""),
        Pin( "E2", "",         ""),
        Pin( "E3", "",         ""),
        Pin( "E4", "",         ""),
        Pin("E10", "",         ""),
        Pin("E11", "",         ""),
        Pin("E12", "",         ""),
        Pin("E13", "",         ""),
        Pin( "F1", "",         ""),
        Pin( "F2", "",         ""),
        Pin( "F3", "",         ""),
        Pin( "F4", "",         ""),
        Pin("F10", "",         ""),
        Pin("F11", "",         ""),
        Pin("F12", "",         ""),
        Pin("F13", "",         ""),
        Pin( "G1", "",         ""),
        Pin( "G2", "",         ""),
        Pin( "G3", "",         ""),
        Pin( "G4", "",         ""),
        Pin("G10", "",         ""),
        Pin("G11", "",         ""),
        Pin("G12", "",         ""),
        Pin("G13", "",         ""),
        Pin( "H1", "",         ""),
        Pin( "H2", "",         ""),
        Pin( "H3", "",         ""),
        Pin( "H4", "",         ""),
        Pin("H10", "",         ""),
        Pin("H11", "",         ""),
        Pin("H12", "",         ""),
        Pin("H13", "",         ""),
        Pin( "J1", "",         ""),
        Pin( "J2", "",         ""),
        Pin( "J3", "",         ""),
        Pin( "J4", "",         ""),
        Pin("J10", "",         ""),
        Pin("J11", "",         ""),
        Pin("J12", "",         ""),
        Pin("J13", "",         ""),

        Pin( "K1", "",         ""),
        Pin( "K2", "",         ""),
        Pin( "K3", "",         ""),
        Pin( "K4", "",         ""),
        Pin( "K5", "",         ""),
        Pin( "K6", "",         ""),
        Pin( "K7", "",         ""),
        Pin( "K8", "",         ""),
        Pin( "K9", "",         ""),
        Pin("K10", "",         ""),
        Pin("K11", "",         ""),
        Pin("K12", "",         ""),
        Pin("K13", "",         ""),
        Pin( "L1", "",         ""),
        Pin( "L2", "",         ""),
        Pin( "L3", "",         ""),
        Pin( "L4", "",         ""),
        Pin( "L5", "",         ""),
        Pin( "L6", "",         ""),
        Pin( "L7", "",         ""),
        Pin( "L8", "",         ""),
        Pin( "L9", "",         ""),
        Pin("L10", "",         ""),
        Pin("L11", "",         ""),
        Pin("L12", "",         ""),
        Pin("L13", "",         ""),
        Pin( "M1", "",         ""),
        Pin( "M2", "",         ""),
        Pin( "M3", "",         ""),
        Pin( "M4", "",         ""),
        Pin( "M5", "",         ""),
        Pin( "M6", "",         ""),
        Pin( "M7", "",         ""),
        Pin( "M8", "",         ""),
        Pin( "M9", "",         ""),
        Pin("M10", "",         ""),
        Pin("M11", "",         ""),
        Pin("M12", "",         ""),
        Pin("M13", "",         ""),
        Pin( "N1", "",         ""),
        Pin( "N2", "",         ""),
        Pin( "N3", "",         ""),
        Pin( "N4", "",         ""),
        Pin( "N5", "",         ""),
        Pin( "N6", "",         ""),
        Pin( "N7", "",         ""),
        Pin( "N8", "",         ""),
        Pin( "N9", "",         ""),
        Pin("N10", "",         ""),
        Pin("N11", "",         ""),
        Pin("N12", "",         ""),
        Pin("N13", "",         ""),
    ],
)

# Xilinx XC95144XL CPLD, in 144-pin 0.5mm TQFP package
# cpld = myelin_kicad_pcb.Component(
#     footprint="myelin-kicad:xilinx_tqg144",
#     identifier="CPLD1",
#     value="XC95144XL-10TQG144",
#     buses=[""],
#     pins=[
#         Pin(  1, "VCCIO_2V5_3V3", "3V3"),
#         Pin(  2, "P2.5-I/O/GTS3", "I/O/GTS3"),
#         Pin(  3, "P2.6-I/O/GTS4", "I/O/GTS4"),
#         Pin(  4, "P2.4", [""]),
#         Pin(  5, "P2.8-I/O/GTS1", "I/O/GTS1"),
#         Pin(  6, "P2.9-I/O/GTS2", "I/O/GTS2"),
#         Pin(  7, "P2.10", [""]),
#         Pin(  8, "VCCINT_3V3", "3V3"),
#         Pin(  9, "P2.11", [""]),
#         Pin( 10, "P2.12", [""]),
#         Pin( 11, "P2.14", [""]),
#         Pin( 12, "P2.13", [""]),
#         Pin( 13, "P2.15", [""]),
#         Pin( 14, "P2.16", [""]),
#         Pin( 15, "P2.17", [""]),
#         Pin( 16, "P1.2", [""]),
#         Pin( 17, "P1.3", [""]),
#         Pin( 18, "GND", "GND"),
#         Pin( 19, "P1.5", [""]),
#         Pin( 20, "P1.6", [""]),
#         Pin( 21, "P1.8", [""]),
#         Pin( 22, "P1.9", [""]),
#         Pin( 23, "P1.1", [""]),
#         Pin( 24, "P1.11", [""]),
#         Pin( 25, "P1.4", [""]),
#         Pin( 26, "P1.12", [""]),
#         Pin( 27, "P1.14", [""]),
#         Pin( 28, "P1.15", [""]),
#         Pin( 29, "GND", "GND"),
#         Pin( 30, "P1.17-I/O/GCK1", "I/O/GCK1"),
#         Pin( 31, "P1.10", [""]),
#         Pin( 32, "P3.2-I/O/GCK2", "I/O/GCK2"),
#         Pin( 33, "P3.5", [""]),
#         Pin( 34, "P3.6", [""]),
#         Pin( 35, "P1.16", [""]),
#         Pin( 36, "GND", "GND"),
#         Pin( 37, "VCCIO_2V5_3V3", "3V3"),
#         Pin( 38, "P3.8-I/O/GCK3", "I/O/GCK3"),
#         Pin( 39, "P3.1", [""]),
#         Pin( 40, "P3.9", [""]),
#         Pin( 41, "P3.3", [""]),
#         Pin( 42, "VCCINT_3V3", "3V3"),
#         Pin( 43, "P3.11", [""]),
#         Pin( 44, "P3.4", [""]),
#         Pin( 45, "P3.12", [""]),
#         Pin( 46, "P3.7", [""]),
#         Pin( 47, "GND", "GND"),
#         Pin( 48, "P3.10", [""]),
#         Pin( 49, "P3.14", [""]),
#         Pin( 50, "P3.15", [""]),
#         Pin( 51, "P3.17", [""]),
#         Pin( 52, "P5.2", [""]),
#         Pin( 53, "P5.5", [""]),
#         Pin( 54, "P5.6", [""]),
#         Pin( 55, "VCCIO_2V5_3V3", "3V3"),
#         Pin( 56, "P5.8", [""]),
#         Pin( 57, "P5.9", [""]),
#         Pin( 58, "P5.11", [""]),
#         Pin( 59, "P5.3", [""]),
#         Pin( 60, "P5.12", [""]),
#         Pin( 61, "P5.14", [""]),
#         Pin( 62, "GND", "GND"),
#         Pin( 63, "TDI", "cpld_TDI"),
#         Pin( 64, "P5.15", [""]),
#         Pin( 65, "TMS", "cpld_TMS"),
#         Pin( 66, "P5.7", [""]),
#         Pin( 67, "TCK", "cpld_TCK"),
#         Pin( 68, "P5.10", [""]),
#         Pin( 69, "P5.17", [""]),
#         Pin( 70, "P5.13", [""]),
#         Pin( 71, "P7.2", [""]),
#         Pin( 72, "GND", "GND"),
#         Pin( 73, "VCCIO_2V5_3V3", "3V3"),
#         Pin( 74, "P7.5", [""]),
#         Pin( 75, "P7.3", [""]),
#         Pin( 76, "P7.6", [""]),
#         Pin( 77, "P7.7", [""]),
#         Pin( 78, "P7.8", [""]),
#         Pin( 79, "P7.10", [""]),
#         Pin( 80, "P7.9", [""]),
#         Pin( 81, "P7.13", [""]),
#         Pin( 82, "P7.11", [""]),
#         Pin( 83, "P7.16", [""]),
#         Pin( 84, "VCCINT_3V3", "3V3"),
#         Pin( 85, "P7.12", [""]),
#         Pin( 86, "P7.14", [""]),
#         Pin( 87, "P7.15", [""]),
#         Pin( 88, "P7.17", [""]),
#         Pin( 89, "GND", "GND"),
#         Pin( 90, "GND", "GND"),
#         Pin( 91, "P8.2", [""]),
#         Pin( 92, "P8.5", [""]),
#         Pin( 93, "P8.6", [""]),
#         Pin( 94, "P8.8", [""]),
#         Pin( 95, "P8.3", [""]),
#         Pin( 96, "P8.9", [""]),
#         Pin( 97, "P8.4", [""]),
#         Pin( 98, "P8.11", [""]),
#         Pin( 99, "GND", "GND"),
#         Pin(100, "P8.12", [""]),
#         Pin(101, "P8.10", [""]),
#         Pin(102, "P8.14", [""]),
#         Pin(103, "P8.13", [""]),
#         Pin(104, "P8.15", [""]),
#         Pin(105, "P8.17", [""]),
#         Pin(106, "P6.2", [""]),
#         Pin(107, "P8.16", [""]),
#         Pin(108, "GND", "GND"),
#         Pin(109, "VCCIO_2V5_3V3", "3V3"),
#         Pin(110, "P6.5", [""]),
#         Pin(111, "P6.4", [""]),
#         Pin(112, "P6.6", [""]),
#         Pin(113, "P6.8", [""]),
#         Pin(114, "GND", "GND"),
#         Pin(115, "P6.10", [""]),
#         Pin(116, "P6.9", [""]),
#         Pin(117, "P6.16", [""]),
#         Pin(118, "P4.1", [""]),
#         Pin(119, "P6.11", [""]),
#         Pin(120, "P6.12", [""]),
#         Pin(121, "P6.14", [""]),
#         Pin(122, "TDO", "cpld_TDO"),
#         Pin(123, "GND", "GND"),
#         Pin(124, "P6.15", [""]),
#         Pin(125, "P6.17", [""]),
#         Pin(126, "P4.2", [""]),
#         Pin(127, "VCCIO_2V5_3V3", "3V3"),
#         Pin(128, "P4.5", [""]),
#         Pin(129, "P4.6", [""]),
#         Pin(130, "P4.8", [""]),
#         Pin(131, "P4.9", [""]),
#         Pin(132, "P4.11", [""]),
#         Pin(133, "P4.3", [""]),
#         Pin(134, "P4.12", [""]),
#         Pin(135, "P4.10", [""]),
#         Pin(136, "P4.14", [""]),
#         Pin(137, "P4.13", [""]),
#         Pin(138, "P4.15", [""]),
#         Pin(139, "P4.16", [""]),
#         Pin(140, "P4.17", [""]),
#         Pin(141, "VCCINT_3V3", "3V3"),
#         Pin(142, "P2.1", [""]),
#         Pin(143, "P2.2-I/O/GSR", "I/O/GSR"),
#         Pin(144, "GND", "GND"),
#     ],
# )
# This chip has a ton of power pins!  Add a ton of capacitors.
cpld_caps = [
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="CC%d" % n)
    for n in range(10)
]
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, PATH_TO_CPLD, "constraints.ucf"))

# altera jtag header, like in the lc-electronics xc9572xl board
# left column: tck tdo tms nc tdi
# right column: gnd vcc nc nc gnd
cpld_jtag = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm",
    identifier="JTAG1",
    value="jtag",
    desc="2x5 header for JTAG programming.  Use generic 0.1 inch header strip or Digikey ED1543-ND.",
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


# to allow a user to select which flash block to use
cpld_jumpers = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x04_Pitch2.54mm",
    identifier="JP",
    value="jumpers",
    desc="1x4 0.1 inch male header",
    pins=[
        Pin(1, "GND", ["GND"]),
        Pin(2, "JP0", ["cpld_JP0"]),
        Pin(3, "JP1", ["cpld_JP1"]),
        Pin(4, "3V3", ["5V"]),
    ],
)


# 3v3 regulator for buffers and whatever's on the other side of the connector
regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="REG",
    value="MCP1700T-3302E/MB",
    desc="3.3V LDO regulator, e.g. Digikey MCP1700T3302EMBCT-ND.  Search for the exact part number because there are many variants.",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C6")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C7")

# Helpful power input/output
ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
    desc="1x3 0.1 inch male header",
    pins=[
        Pin(1, "A", ["GND"]),
        Pin(2, "B", ["3V3"]),
        Pin(3, "C", ["5V"]),
    ],
)

# Flash (low halfword)
flash = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:cypress_lae064_fbga",
        identifier="FLASH%d" % flash_id,
#        value="S29GL064N90TFI040",  # Note that pinout differs a lot between the suffixes; only 03 and 04 are OK
        value="S29GL064S70DHI010",  # 64-ball FBGA, 1mm pitch, 9x9mm (c.f. 20x14 in TQFP)
        buses=[""],
        pins=[
            Pin("F1", "Vio",     "3V3"),
            Pin("A2", "A3",      "flash_A3"),
            Pin("B2", "A4",      "flash_A4"),
            Pin("C2", "A2",      "flash_A2"),
            Pin("D2", "A1",      "flash_A1"),
            Pin("E2", "A0",      "flash_A0"),
            Pin("F2", "CE#",     "flash_nCE"),
            Pin("G2", "OE#",     "flash_nOE"),
            Pin("H2", "VSS",     "GND"),
            Pin("A3", "A7",      "flash_A7"),
            Pin("B3", "A17",     "flash_A17"),
            Pin("C3", "A6",      "flash_A6"),
            Pin("D3", "A5",      "flash_A5"),
            Pin("E3", "DQ0",     "flash%d_DQ0" % flash_id),
            Pin("F3", "DQ8",     "flash%d_DQ8" % flash_id),
            Pin("G3", "DQ9",     "flash%d_DQ9" % flash_id),
            Pin("H3", "DQ1",     "flash%d_DQ1" % flash_id),
            Pin("A4", "RY/BY#",  "flash_READY"),  # open drain
            Pin("B4", "WP#/ACC"),  # contains an internal pull-up so we can leave it NC
            Pin("C4", "A18",     "flash_A18"),
            Pin("D4", "A20",     "flash_A20"),
            Pin("E4", "DQ2",     "flash%d_DQ2" % flash_id),
            Pin("F4", "DQ10",    "flash%d_DQ10" % flash_id),
            Pin("G4", "DQ11",    "flash%d_DQ11" % flash_id),
            Pin("H4", "DQ3",     "flash%d_DQ3" % flash_id),
            Pin("A5", "WE#",     "flash_nWE"),
            Pin("B5", "RESET#",  "flash_nRESET"),
            Pin("C5", "A21",     "flash_A21"),
            Pin("D5", "A19",     "flash_A19"),
            Pin("E5", "DQ5",     "flash%d_DQ5" % flash_id),
            Pin("F5", "DQ12",    "flash%d_DQ12" % flash_id),
            Pin("G5", "Vcc",     "3V3"),
            Pin("H5", "DQ4",     "flash%d_DQ4" % flash_id),
            Pin("A6", "A9",      "flash_A9"),
            Pin("B6", "A8",      "flash_A8"),
            Pin("C6", "A10",     "flash_A10"),
            Pin("D6", "A11",     "flash_A11"),
            Pin("E6", "DQ7",     "flash%d_DQ7" % flash_id),
            Pin("F6", "DQ14",    "flash%d_DQ14" % flash_id),
            Pin("G6", "DQ13",    "flash%d_DQ13" % flash_id),
            Pin("H6", "DQ6",     "flash%d_DQ6" % flash_id),
            Pin("A7", "A13",     "flash_A13"),
            Pin("B7", "A12",     "flash_A12"),
            Pin("C7", "A14",     "flash_A14"),
            Pin("D7", "A15",     "flash_A15"),
            Pin("E7", "A16",     "flash_A16"),
            Pin("F7", "BYTE#",   "3V3"),  # always in word mode
            Pin("G7", "DQ15",    "flash%d_DQ15" % flash_id),
            Pin("H7", "VSS",     "GND"),
            Pin("D8", "Vio",     "3V3"),
            Pin("E8", "VSS",     "GND"),
            # Pin(  1, "A15",     "flash_A15"),
            # Pin(  2, "A14",     "flash_A14"),
            # Pin(  3, "A13",     "flash_A13"),
            # Pin(  4, "A12",     "flash_A12"),
            # Pin(  5, "A11",     "flash_A11"),
            # Pin(  6, "A10",     "flash_A10"),
            # Pin(  7, "A9",      "flash_A9"),
            # Pin(  8, "A8",      "flash_A8"),
            # Pin(  9, "A19",     "flash_A19"),
            # Pin( 10, "A20",     "flash_A20"),
            # Pin( 11, "WE#",     "flash_nWE"),
            # Pin( 12, "RESET#",  "flash_nRESET"),
            # Pin( 13, "A21",     "flash_A21"),
            # Pin( 14, "WP#/ACC", "flash_nWP"),  # TODO probably tie to 3V3 (low=WP#, 12V=accelerate)
            # Pin( 15, "RY/BY#",  "flash_RY"),  # TODO pull up to 3V3 (open drain)
            # Pin( 16, "A18",     "flash_A18"),
            # Pin( 17, "A17",     "flash_A17"),
            # Pin( 18, "A7",      "flash_A7"),
            # Pin( 19, "A6",      "flash_A6"),
            # Pin( 20, "A5",      "flash_A5"),
            # Pin( 21, "A4",      "flash_A4"),
            # Pin( 22, "A3",      "flash_A3"),
            # Pin( 23, "A2",      "flash_A2"),
            # Pin( 24, "A1",      "flash_A1"),
            # Pin( 25, "A0",      "flash_A0"),
            # Pin( 26, "CE#",     "flash_nCE"),
            # Pin( 27, "VSS",     "GND"),
            # Pin( 28, "OE#",     "flash_nOE"),
            # Pin( 29, "DQ0",     "flash%d_DQ0" % flash_id),
            # Pin( 30, "DQ8",     "flash%d_DQ8" % flash_id),
            # Pin( 31, "DQ1",     "flash%d_DQ1" % flash_id),
            # Pin( 32, "DQ9",     "flash%d_DQ9" % flash_id),
            # Pin( 33, "DQ2",     "flash%d_DQ2" % flash_id),
            # Pin( 34, "DQ10",    "flash%d_DQ10" % flash_id),
            # Pin( 35, "DQ3",     "flash%d_DQ3" % flash_id),
            # Pin( 36, "DQ11",    "flash%d_DQ11" % flash_id),
            # Pin( 37, "VCC",     "3V3"),
            # Pin( 38, "DQ4",     "flash%d_DQ4" % flash_id),
            # Pin( 39, "DQ12",    "flash%d_DQ12" % flash_id),
            # Pin( 40, "DQ5",     "flash%d_DQ5" % flash_id),
            # Pin( 41, "DQ13",    "flash%d_DQ13" % flash_id),
            # Pin( 42, "DQ6",     "flash%d_DQ6" % flash_id),
            # Pin( 43, "DQ14",    "flash%d_DQ14" % flash_id),
            # Pin( 44, "DQ7",     "flash%d_DQ7" % flash_id),
            # Pin( 45, "DQ15",    "flash%d_DQ15" % flash_id),
            # Pin( 46, "VSS",     "GND"),
            # Pin( 47, "BYTE#",   "3V3"),  # tied high for permanent word config
            # Pin( 48, "A16",     "flash0_A16"),
        ],
    )
    for flash_id in (0, 1, 2, 3, 4, 5)
]
# Three capacitors per chip (2 x Vio, 1 x Vcc)
flash_caps = [
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="FC%d" % n)
    for n in range(6)
]

# 28-pin ROM footprint, to plug into the BBC Master motherboard
connector = myelin_kicad_pcb.Component(
    footprint="Housings_DIP:DIP-28_W15.24mm",
    identifier="ROM",
    value="MOS ROM",
    desc="Adapter to emulate a 600mil 28-pin DIP, e.g. Digikey 1175-1525-5-ND",
    pins=[
        Pin( "1", "A15", ["bbc_A15"]),
        Pin( "2", "A12", ["bbc_A12"]),
        Pin( "3", "A7",  ["bbc_A7"]),
        Pin( "4", "A6",  ["bbc_A6"]),
        Pin( "5", "A5",  ["bbc_A5"]),
        Pin( "6", "A4",  ["bbc_A4"]),
        Pin( "7", "A3",  ["bbc_A3"]),
        Pin( "8", "A2",  ["bbc_A2"]),
        Pin( "9", "A1",  ["bbc_A1"]),
        Pin("10", "A0",  ["bbc_A0"]),
        Pin("11", "D0",  ["D0"]),
        Pin("12", "D1",  ["D1"]),
        Pin("13", "D2",  ["D2"]),
        Pin("14", "VSS", ["GND"]),
        Pin("15", "D3",  ["D3"]),
        Pin("16", "D4",  ["D4"]),
        Pin("17", "D5",  ["D5"]),
        Pin("18", "D6",  ["D6"]),
        Pin("19", "D7",  ["D7"]),
        Pin("20", "nCS", ),  # bbc /CS ignored because it's tied to GND on the motherboard
        Pin("21", "A10", ["bbc_A10"]),
        Pin("22", "A16", ["bbc_A16"]),
        Pin("23", "A11", ["bbc_A11"]),
        Pin("24", "A9",  ["bbc_A9"]),
        Pin("25", "A8",  ["bbc_A8"]),
        Pin("26", "A13", ["bbc_A13"]),
        Pin("27", "A14", ["bbc_A14"]),
        Pin("28", "VCC", ["5V"]),
    ],
)

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(10)
]

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")

