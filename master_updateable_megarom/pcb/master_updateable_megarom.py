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

# -------------------------
# master_updateable_megarom
# -------------------------

# by Phillip Pearson

# A board that replaces the 128KB ROM in the BBC with a flash chip and some
# buffers, to allow it to be updated without removing it from the machine.

# This won't work if you plug it into a normal ROM socket, but you can fix that
# by soldering a wire between pin 20 (/CE) of the ROM socket and one of the
# jumper pins (pin 2 or 3 of JP).  This will need the CPLD to be configured
# differently, of course.

# Size constraints
# ----------------

# If we want to keep this about the same size as a RetroClinic DualOS board,
# it has to fit in about a 40 x 42mm rectangle.  40mm is the distance from one
# edge of the MOS ROM to the other edge of the adjacent ROM, and 42mm is about
# how far we can extend into the motherboard without running into a decoupling
# capacitor.

#  +---------+ |
#  | MOS ROM | |
#  +---------+ | 40 mm
#  +---------+ |
#  |  IC 37  | |
#  +---------+ |
#  -----------
#     42 mm

# If it's OK to bend a couple of capacitors over, it's probably safe to extend
# 100mm or more into the motherboard.

#                 +---------+ |
#                 | MOS ROM | |
#                 +---------+ | 40 mm
#                 +---------+ |
#                 |  IC 37  | |
#                 +---------+ |
#  --------------------------
#             100 mm

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Xilinx XC9572XL CPLD, in 64-pin 0.5mm TQFP package
cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg64",
    identifier="CPLD",
    value="XC9572XL-64VQG",
    desc="Xilinx XC9572XL in 64-pin 0.5mm TQFP package.  Any speed or temperature grade is OK.",
    buses=["bbc_A", "flash_A", "D", "cpld_JP"],
    pins=[
        # 52 user pins
        # 17 used by bbc_A
        # 19 used by flash_A
        # 8 used by D
        # flash_nCE, flash_nWE, flash_nOE
        # bbc_nCE
        # 4 used by cpld_SCK, cpld_MISO, cpld_MOSI, cpld_SS

        # it would be nice if we had two more to allow external selection of flash bank.
        # we could wire flash_nCE low and ignore bbc_nCE.
        Pin(1,  "P2.10",   ["D6"]),
        Pin(2,  "GTS2",    ["D7"]),
        Pin(4,  "P2.12",   ["bbc_A0"]),
        Pin(5,  "GTS1",    ["bbc_A1"]),
        Pin(6,  "P2.15",   ["bbc_A2"]),
        Pin(7,  "P2.17",   ["bbc_A3"]),
        Pin(8,  "P1.2",    ["bbc_A10"]),
        Pin(9,  "P1.5",    ["bbc_A4"]),
        Pin(10, "P1.6",    ["bbc_A16"]),
        Pin(11, "P1.8",    ["bbc_A5"]),
        Pin(12, "P1.3",    ["bbc_A11"]),
        Pin(13, "P1.4",    ["bbc_A6"]),
        Pin(15, "P1.GCK1", ["bbc_A9"]),  # Should have put SCK on one of these!
        Pin(16, "P1.GCK2", ["bbc_A7"]),  # Try drilling out one of the tracks and
        Pin(17, "P1.GCK3", ["bbc_A8"]),  # using it as a spare GCK pin.
        Pin(18, "P1.10",   ["bbc_A12"]),
        Pin(19, "P1.15",   ["cpld_JP1"]),  # TODO(r2) shuffle pins around so
        Pin(20, "P1.17",   ["bbc_A15"]),   # cpld_SCK ends up on a GCK.
        Pin(22, "P3.2",    ["cpld_JP0"]),
        Pin(23, "P1.12",   ["bbc_A13"]),
        Pin(24, "P3.5",    ["bbc_A14"]),
        Pin(25, "P3.8",    ["cpld_MISO"]),
        Pin(27, "P3.9",    ["cpld_MOSI"]),
        Pin(31, "P3.3",    ["cpld_SCK"]),
        Pin(32, "P3.4",    ["cpld_SS"]),
        Pin(33, "P3.11",   ["flash_A0"]),
        Pin(34, "P3.6",    ["flash_A1"]),
        Pin(35, "P3.14",   ["flash_A2"]),
        Pin(36, "P3.15",   ["flash_A3"]),
        Pin(38, "P3.17",   ["flash_A4"]),
        Pin(39, "P3.10",   ["flash_A5"]),
        Pin(40, "P3.12",   ["flash_A6"]),
        Pin(42, "P3.16",   ["flash_A7"]),
        Pin(43, "P4.2",    ["flash_A12"]),
        Pin(44, "P4.5",    ["flash_A15"]),
        Pin(45, "P4.8",    ["flash_A16"]),
        Pin(46, "P4.3",    ["flash_A18"]),
        Pin(47, "P4.4",    ["flash_nWE"]),
        Pin(48, "P4.11",   ["flash_A17"]),
        Pin(49, "P4.6",    ["flash_A14"]),
        Pin(50, "P4.14",   ["flash_A13"]),
        Pin(51, "P4.10",   ["flash_A8"]),
        Pin(52, "P4.12",   ["flash_A9"]),
        Pin(56, "P4.15",   ["flash_A11"]),
        Pin(57, "P4.17",   ["flash_nOE"]),
        Pin(58, "P2.3",    ["flash_A10"]),
        Pin(59, "P2.4",    ["D0"]),
        Pin(60, "P2.2",    ["D2"]),
        Pin(61, "P2.5",    ["D3"]),
        Pin(62, "P2.6",    ["D4"]),
        Pin(63, "P2.8",    ["D1"]),
        Pin(64, "P2.GSR",  ["D5"]),

        # 8 power pins
        Pin(3,  "VCCINT_3V3",    ["3V3"]),
        Pin(14, "GND",           ["GND"]),
        Pin(21, "GND",           ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(37, "VCCINT_3V3",    ["3V3"]),
        Pin(41, "GND",           ["GND"]),
        Pin(54, "GND",           ["GND"]),
        Pin(55, "VCCIO_2V5_3V3", ["3V3"]),

        # 4 JTAG programming interface pins
        Pin(28, "TDI", ["cpld_TDI"]),
        Pin(29, "TMS", ["cpld_TMS"]),
        Pin(30, "TCK", ["cpld_TCK"]),
        Pin(53, "TDO", ["cpld_TDO"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C1")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
cpld_cap3 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C3")
cpld_cap4 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C4")
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, "../cpld/constraints.ucf"))

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

cpld_spi = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x05_Pitch2.54mm",
    identifier="SPI",
    value="spi",
    desc="1x3 0.1 inch male header",
    pins=[
        Pin(1, "GND", ["GND"]),
        Pin(2, "SCK", ["cpld_SCK"]),
        Pin(3, "nSS", ["cpld_SS"]),
        Pin(4, "MISO", ["cpld_MOSI"]),
        Pin(5, "MOSI", ["cpld_MISO"]),
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

flash = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:sst_plcc32_nh",
    identifier="MEM",
    value="SST39SF010A/020A/040",
    desc="128kB/256kB/512kB flash chip in SST 'NH' PLCC-32 package: SST39SF040-XX-XX-NHE, SST39SF020A-XX-XX-NHE, or SST39SF010A-XX-XX-NHE",
    pins=[
        Pin(1, "A18",  ["flash_A18"]),
        Pin(2, "A16",  ["flash_A16"]),
        Pin(3, "A15",  ["flash_A15"]),
        Pin(4, "A12",  ["flash_A12"]),
        Pin(5, "A7",   ["flash_A7"]),
        Pin(6, "A6",   ["flash_A6"]),
        Pin(7, "A5",   ["flash_A5"]),
        Pin(8, "A4",   ["flash_A4"]),
        Pin(9, "A3",   ["flash_A3"]),
        Pin(10, "A2",  ["flash_A2"]),
        Pin(11, "A1",  ["flash_A1"]),
        Pin(12, "A0",  ["flash_A0"]),
        Pin(13, "D0",  ["D0"]),
        Pin(14, "D1",  ["D1"]),
        Pin(15, "D2",  ["D2"]),
        Pin(16, "VSS", ["GND"]),
        Pin(17, "D3",  ["D3"]),
        Pin(18, "D4",  ["D4"]),
        Pin(19, "D5",  ["D5"]),
        Pin(20, "D6",  ["D6"]),
        Pin(21, "D7",  ["D7"]),
        Pin(22, "nCE", ["GND"]),  # flash chip permanently enabled
        Pin(23, "A10", ["flash_A10"]),
        Pin(24, "nOE", ["flash_nOE"]),
        Pin(25, "A11", ["flash_A11"]),
        Pin(26, "A9",  ["flash_A9"]),
        Pin(27, "A8",  ["flash_A8"]),
        Pin(28, "A13", ["flash_A13"]),
        Pin(29, "A14", ["flash_A14"]),
        Pin(30, "A17", ["flash_A17"]),
        Pin(31, "nWE", ["flash_nWE"]),
        Pin(32, "VDD", ["5V"]),
    ],
)
flash_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C5")

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

myelin_kicad_pcb.dump_netlist("master_updateable_megarom.net")
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")


# Keeping these around just in case I do decide to switch over to using a
# PSoC4 chip (CY8C4245) instead of the 64-pin XC9572XL one day!
# -----------------------------------------------------------------------

# # unidirectional buffer for address lines, cpu -> expansion connector
# addr_buf_lo = myelin_kicad_pcb.Component(
#     footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
#     identifier="ABUFL",
#     value="74LVC245",
#     pins=[
#         Pin( 1, "A->B", ["abuf_ext_to_cpu"]),
#         Pin( 2, "A0", ["ext_A0"]),
#         Pin( 3, "A1", ["ext_A1"]),
#         Pin( 4, "A2", ["ext_A2"]),
#         Pin( 5, "A3", ["ext_A3"]),
#         Pin( 6, "A4", ["ext_A4"]),
#         Pin( 7, "A5", ["ext_A5"]),
#         Pin( 8, "A6", ["ext_A6"]),
#         Pin( 9, "A7", ["ext_A7"]),
#         Pin(10, "GND", ["GND"]),
#         Pin(11, "B7", ["cpu_A7"]),
#         Pin(12, "B6", ["cpu_A6"]),
#         Pin(13, "B5", ["cpu_A5"]),
#         Pin(14, "B4", ["cpu_A4"]),
#         Pin(15, "B3", ["cpu_A3"]),
#         Pin(16, "B2", ["cpu_A2"]),
#         Pin(17, "B1", ["cpu_A1"]),
#         Pin(18, "B0", ["cpu_A0"]),
#         Pin(19, "nCE", ["abuf_nCE"]),
#         Pin(20, "VCC", ["3V3"]),
#     ],
# )
# addr_buf_lo_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C5")

# addr_buf_hi = myelin_kicad_pcb.Component(
#     footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
#     identifier="ABUFH",
#     value="74LVC245",
#     pins=[
#         Pin( 1, "A->B", ["abuf_ext_to_cpu"]),
#         Pin( 2, "A0", ["ext_A8"]),
#         Pin( 3, "A1", ["ext_A9"]),
#         Pin( 4, "A2", ["ext_A10"]),
#         Pin( 5, "A3", ["ext_A11"]),
#         Pin( 6, "A4", ["ext_A12"]),
#         Pin( 7, "A5", ["ext_A13"]),
#         Pin( 8, "A6", ["ext_A14"]),
#         Pin( 9, "A7", ["ext_A15"]),
#         Pin(10, "GND", ["GND"]),
#         Pin(11, "B7", ["cpu_A15_2"]),
#         Pin(12, "B6", ["cpu_A14_2"]),
#         Pin(13, "B5", ["cpu_A13_2"]),
#         Pin(14, "B4", ["cpu_A12"]),
#         Pin(15, "B3", ["cpu_A11"]),
#         Pin(16, "B2", ["cpu_A10"]),
#         Pin(17, "B1", ["cpu_A9"]),
#         Pin(18, "B0", ["cpu_A8"]),
#         Pin(19, "nCE", ["abuf_nCE"]),
#         Pin(20, "VCC", ["3V3"]),
#     ],
# )
# addr_buf_hi_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C6")

# psoc = myelin_kicad_pcb.Component(
#     footprint="??? tqfp44 10mm",
#     identifier="MCU",
#     value="CY8C4245AXI",
#     pins=[
#         Pin( 1, "VSS",    ["GND"]),
#         Pin( 2, "P2.0",   [""]),
#         Pin( 3, "P2.1",   [""]),
#         Pin( 4, "P2.2",   [""]),
#         Pin( 5, "P2.3",   [""]),
#         Pin( 6, "P2.4",   [""]),
#         Pin( 7, "P2.5",   [""]),
#         Pin( 8, "P2.6",   [""]),
#         Pin( 9, "P2.7",   [""]),
#         Pin(10, "VSS",    ["GND"]),
#         Pin(11, "P3.0",   [""]),
#         Pin(12, "P3.1",   [""]),
#         Pin(13, "P3.2",   [""]),
#         Pin(14, "P3.3",   [""]),
#         Pin(15, "P3.4",   [""]),
#         Pin(16, "P3.5",   [""]),
#         Pin(17, "P3.6",   [""]),
#         Pin(18, "P3.7",   [""]),
#         Pin(19, "VDDD",   ["5V"]),
#         Pin(20, "P4.0",   [""]),
#         Pin(21, "P4.1",   [""]),
#         Pin(22, "P4.2",   [""]),
#         Pin(23, "P4.3",   [""]),
#         Pin(24, "P0.0",   [""]),
#         Pin(25, "P0.1",   [""]),
#         Pin(26, "P0.2",   [""]),
#         Pin(27, "P0.3",   [""]),
#         Pin(28, "P0.4",   [""]),
#         Pin(29, "P0.5",   [""]),
#         Pin(30, "P0.6",   [""]),
#         Pin(31, "P0.7",   [""]),
#         Pin(32, "nRESET", ["mcu_nreset"]),
#         Pin(33, "VCCD",   ["mcu_vccd"]),  # regulated supply; connect to 1uF cap or 1.8V
#         Pin(34, "VDDD",   ["5V"]),
#         Pin(35, "VDDA",   ["5V"]),
#         Pin(36, "VSSA",   ["GND"]),
#         Pin(37, "P1.0",   [""]),
#         Pin(38, "P1.1",   [""]),
#         Pin(39, "P1.2",   [""]),
#         Pin(40, "P1.3",   [""]),
#         Pin(41, "P1.4",   [""]),
#         Pin(42, "P1.5",   [""]),
#         Pin(43, "P1.6",   [""]),
#         Pin(44, "P1.7",   [""]),
#     ],
# )
# cpld_cap1 = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C7")
# cpld_cap2 = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C8")
# cpld_cap3 = myelin_kicad_pcb.C0805("1u", "mcu_vccd", "GND", ref="C9")
#myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, "../cpld/constraints.ucf"))
