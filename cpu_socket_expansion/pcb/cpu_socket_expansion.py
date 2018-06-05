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

# --------------------
# cpu_socket_expansion
# --------------------

# by Phillip Pearson

# TODO check if I need to enlarge the holes on the CPU socket, because the
# 220-1-40-006 datasheet says to have 0.9mm holes.  The pins are 0.46mm dia
# though, so 0.8 should probably be OK.

# A board to make it easier to piggyback on the 6502's pins in an Electron or
# BBC Micro. This converts all the 5V signals to 3.3V, for compatibility with
# FPGAs and newer MCUs.

# I spent ages trying to decide whether this should *only* be to piggyback on
# the pins, or whether it should also enable completely replacing the CPU with
# an FPGA, and eventually settled on the latter, using a small CPLD.

# CPU signals (37 signal pins + 3 power pins)
# - D x 8
# - A x 16
# - Inputs: PHI0_IN
# - Inputs that we can pull low: nSO, nRESET, RDY, nIRQ, nNMI
# - Outputs: PHI1_OUT, PHI2_OUT, SYNC, RNW
# - Ignored: NC_XTLO (crystal connection on some chips), NC_BE, NC_nML

# I'm keeping the expansion connector as vague as possible for now.  It
# definitely needs 3 power pins, 8 data pins, and 16 address pins, leaving 13
# more pins that should just connect into the CPLD and be defined later.

# To let us tristate the bus for shadow RAM, we want to be able to drive
# A15:13 to 110 on the motherboard (after removing the socketed OS/BASIC ROM),
# which requires 6 pins on the CPLD.

# CPLD pin usage (max 34):
# - clk_16MHz tap from somewhere on the motherboard
# - 13 GPIO on the connector
# - 10 signals on the CPU
# - 6: A13 x 2, A14 x 2, A15 x 2
# - 4: dbuf and abuf /CE and A->B

# Size constraints
# ----------------

# The board can extend past the top of the 6502 about 1" before hitting the
# top of the Electron's case. In the Electron, the keyboard connector is in
# line with pin 13 of the 6502, and starts 59mm to the left of the left row of
# 6502 pins, and has 22 pins with 0.1" spacing, so is 2.2" (55.88mm) long. The
# RF circuitry starts just after pin 13, so ending the board there is probably
# a good plan.

# In the BBC, the keyboard connector is in line with the bottom of the 6502.

# When making a board to plug into this, if you put a
# Pin_Header_Angled_2x20_Pitch2.54mm at (128.7, 78.54), so the left row of
# pins is at x=128.7, and draw a 3mm thick line left from (102.23, 108.96),
# that should be pretty accurate, including space for the connector in between
# the angled headers... i.e. you have 26.47 mm between the left row of your
# connector and the edge of the keyboard connector, and will probably need an
# L-shaped board.  The top of the board can extend up to y=53.14, so you have
# about 55mm from the keyboard connector to the top of the case.  The RF
# circuitry means the left side of the board has to finish around (102.23 -
# 25.4 * 1.3) = 69.21.

# Daughterboards
# --------------

# I have two ideas right now.  #1 is something to let me plug in my
# miniSpartan6+.  #2 is a MachXO-based RAM/flash/SD card board that might
# possibly also include a PiTubeDirect socket.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


# cpu socket and header -- pass through, so same pinout
# cpu_1 / CPU1 / cpu_Axx_1 = connection to motherboard
# cpu_2 / PU2 / cpu_Axx_2 = socketed 6502
cpu_1, cpu_2 = [
    myelin_kicad_pcb.Component(
        footprint="Housings_DIP:DIP-40_W15.24mm",
        identifier="CPU%d" % (cpuid + 1),
        value="6502",
        desc=(
            "adapter to emulate a 600mil 40-pin DIP, e.g. Digikey 1175-1527-5-ND"
            if cpuid == 0
            else "600mil 40-pin DIP socket, e.g. Digikey 609-4716-ND"
        ),
        pins=[
            # Need to disconnect pin 1 on W65C02S; add a jumper between these two nets
            Pin( 1, "VSS", ["cpu_GND_VPB_2" if cpuid else "GND"]),
            Pin( 2, "RDY", ["cpu_RDY"]),
            Pin( 3, "PHI1_OUT", ["cpu_PHI1_OUT"]),
            Pin( 4, "nIRQ", ["cpu_nIRQ"]),  # pulled up on the motherboard
            # Pin 5 is NC on R6502, /ML on W65C02S; only used in multiprocessor systems
            Pin( 5, "NC_nML"),  # Isolate this
            Pin( 6, "nNMI", ["cpu_nNMI"]),  # pulled up on the motherboard
            Pin( 7, "SYNC", ["cpu_SYNC"]),
            Pin( 8, "VCC", ["5V"]),
            Pin( 9, "A0", ["cpu_A0"]),
            Pin(10, "A1", ["cpu_A1"]),
            Pin(11, "A2", ["cpu_A2"]),
            Pin(12, "A3", ["cpu_A3"]),
            Pin(13, "A4", ["cpu_A4"]),
            Pin(14, "A5", ["cpu_A5"]),
            Pin(15, "A6", ["cpu_A6"]),
            Pin(16, "A7", ["cpu_A7"]),
            Pin(17, "A8", ["cpu_A8"]),
            Pin(18, "A9", ["cpu_A9"]),
            Pin(19, "A10", ["cpu_A10"]),
            Pin(20, "A11", ["cpu_A11"]),
            Pin(21, "VSS", ["GND"]),
            Pin(22, "A12", ["cpu_A12"]),
            Pin(23, "A13", ["cpu_A13_%d" % (cpuid + 1)]),
            Pin(24, "A14", ["cpu_A14_%d" % (cpuid + 1)]),
            Pin(25, "A15", ["cpu_A15_%d" % (cpuid + 1)]),
            Pin(26, "D7", ["cpu_D7"]),
            Pin(27, "D6", ["cpu_D6"]),
            Pin(28, "D5", ["cpu_D5"]),
            Pin(29, "D4", ["cpu_D4"]),
            Pin(30, "D3", ["cpu_D3"]),
            Pin(31, "D2", ["cpu_D2"]),
            Pin(32, "D1", ["cpu_D1"]),
            Pin(33, "D0", ["cpu_D0"]),
            Pin(34, "RnW", ["cpu_RnW"]),
            Pin(35, "NC_XTLO", ["cpu_NC_XTLO"]),
            Pin(36, "NC_BE", ["cpu_NC_BE"]),  # NC on R6502, BE on W65C02S; WDC says to tie to VDD
            Pin(37, "PHI0_IN", ["cpu_PHI0_IN"]),  # PHI2_IN on W65C02S
            Pin(38, "nSO", ["cpu_nSO"]),
            Pin(39, "PHI2_OUT", ["cpu_PHI2_OUT"]),
            Pin(40, "nRESET", ["cpu_nRESET"]),
        ],
    ) for cpuid in range(2)]
cpu_cap = myelin_kicad_pcb.C0805("100n", "GND", "5V", ref="C1")
cpu_VPB_jumper = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="JP1",
	desc="1x2 0.1 inch male header",
    value="VPB",
    pins=[
        Pin(1, "A", ["cpu_GND_VPB_2"]),
        Pin(2, "B", ["GND"]),
    ],
)
cpu_BE_pullup = myelin_kicad_pcb.R0805("4k7", "cpu_NC_BE", "5V", ref="R1")
cpld_16MHz_port = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="M16",
	desc="1x2 0.1 inch male header",
    value="16MHz",
    pins=[
        Pin(1, "A", ["clk_16MHz"]),
        Pin(2, "B", ["GND"]),
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
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C2")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C3")

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

# bidirectional buffer for data lines, with direction fed by RnW and /OE passed to the expansion connector
# so the CPLD on the other side can signal when data is valid.
data_buf = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="DBUF",
    value="74LVC245APW",
    desc="74LVC245 in TSSOP20 with 4.4mm body width, e.g. Digikey 1727-3105-1-ND",
    pins=[
        Pin( 1, "A->B", ["dbuf_ext_to_cpu"]),
        Pin( 2, "A0", ["ext_D7"]),
        Pin( 3, "A1", ["ext_D6"]),
        Pin( 4, "A2", ["ext_D5"]),
        Pin( 5, "A3", ["ext_D4"]),
        Pin( 6, "A4", ["ext_D3"]),
        Pin( 7, "A5", ["ext_D2"]),
        Pin( 8, "A6", ["ext_D1"]),
        Pin( 9, "A7", ["ext_D0"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["cpu_D0"]),
        Pin(12, "B6", ["cpu_D1"]),
        Pin(13, "B5", ["cpu_D2"]),
        Pin(14, "B4", ["cpu_D3"]),
        Pin(15, "B3", ["cpu_D4"]),
        Pin(16, "B2", ["cpu_D5"]),
        Pin(17, "B1", ["cpu_D6"]),
        Pin(18, "B0", ["cpu_D7"]),
        Pin(19, "nCE", ["dbuf_nCE"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
dbuf_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C4")
dbuf_nCE_pullup = myelin_kicad_pcb.R0805("10k", "dbuf_nCE", "3V3", ref="R2")

# unidirectional buffer for address lines, cpu -> expansion connector
# *** maybe make this bidirectional for future expansion
addr_buf_lo = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="ABUFL",
    value="74LVC245APW",
    desc="74LVC245 in TSSOP20 with 4.4mm body width, e.g. Digikey 1727-3105-1-ND",
    pins=[
        Pin( 1, "A->B", ["abuf_ext_to_cpu"]),
        Pin( 2, "A0", ["ext_A0"]),
        Pin( 3, "A1", ["ext_A1"]),
        Pin( 4, "A2", ["ext_A2"]),
        Pin( 5, "A3", ["ext_A3"]),
        Pin( 6, "A4", ["ext_A4"]),
        Pin( 7, "A5", ["ext_A5"]),
        Pin( 8, "A6", ["ext_A6"]),
        Pin( 9, "A7", ["ext_A7"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["cpu_A7"]),
        Pin(12, "B6", ["cpu_A6"]),
        Pin(13, "B5", ["cpu_A5"]),
        Pin(14, "B4", ["cpu_A4"]),
        Pin(15, "B3", ["cpu_A3"]),
        Pin(16, "B2", ["cpu_A2"]),
        Pin(17, "B1", ["cpu_A1"]),
        Pin(18, "B0", ["cpu_A0"]),
        Pin(19, "nCE", ["abuf_nCE"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
addr_buf_lo_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C5")
abuf_nCE_pullup = myelin_kicad_pcb.R0805("10k", "abuf_nCE", "3V3", ref="R3")

addr_buf_hi = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="ABUFH",
    value="74LVC245APW",
    desc="74LVC245 in TSSOP20 with 4.4mm body width, e.g. Digikey 1727-3105-1-ND",
    pins=[
        Pin( 1, "A->B", ["abuf_ext_to_cpu"]),
        Pin( 2, "A0", ["ext_A8"]),
        Pin( 3, "A1", ["ext_A9"]),
        Pin( 4, "A2", ["ext_A10"]),
        Pin( 5, "A3", ["ext_A11"]),
        Pin( 6, "A4", ["ext_A12"]),
        Pin( 7, "A5", ["ext_A13"]),
        Pin( 8, "A6", ["ext_A14"]),
        Pin( 9, "A7", ["ext_A15"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["cpu_A15_2"]),
        Pin(12, "B6", ["cpu_A14_2"]),
        Pin(13, "B5", ["cpu_A13_2"]),
        Pin(14, "B4", ["cpu_A12"]),
        Pin(15, "B3", ["cpu_A11"]),
        Pin(16, "B2", ["cpu_A10"]),
        Pin(17, "B1", ["cpu_A9"]),
        Pin(18, "B0", ["cpu_A8"]),
        Pin(19, "nCE", ["abuf_nCE"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
addr_buf_hi_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C6")

# CPLD to deal with all the other signals, allowing various different
# hardware modules to plug in.

# For an expansion which doesn't include a CPU, the option lines are:
# - 1 data valid output (to enble expansion to write to the data bus)
# - 8 control/flag inputs
#   - RDY
#   - nIRQ
#   - nNMI
#   - SYNC
#   - RnW
#   - PHI2_OUT
#   - 16MHz
# - 4 OC outputs: RDY, /SO, /NMI, /IRQ

# For an expansion which *does* include a CPU (i.e. a big FPGA board):
# - nIRQ, nNMI, RDY, nSO inputs
# - SYNC output
# - RnW output, which also controls D bus direction
# - PHI0_IN input, PHI1_OUT and PHI2_OUT outputs
# - 16MHz input
# + 3 spares

cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="PLD",
    value="XC9572XL-10VQG44C",
	desc="Xilinx XC9572XL in 44-pin 0.8mm TQFP package.  Any speed or temperature grade is OK.",
    buses=[],
    pins=[
        Pin(39, "P1.2",          ["cpu_RDY"]),
        Pin(40, "P1.5",          ["dbuf_ext_to_cpu"]),
        Pin(41, "P1.6",          ["cpu_PHI1_OUT"]),
        Pin(42, "P1.8",          ["abuf_nCE"]),
        Pin(43, "P1.9-GCK1",     ["cpu_nIRQ"]),
        Pin(44, "P1.11-GCK2",    ["dbuf_nCE"]),
        Pin(1,  "P1.14-GCK3",    ["cpu_RnW"]),
        Pin(2,  "P1.15",         ["cpu_SYNC"]),
        Pin(3,  "P1.17",         ["cpu_nNMI"]),
        Pin(4,  "GND",           ["GND"]),
        Pin(5,  "P3.2",          ["cpu_PHI0_IN"]),
        Pin(6,  "P3.5",          ["cpu_nSO"]),
        Pin(7,  "P3.8",          ["cpu_PHI2_OUT"]),
        Pin(8,  "P3.9",          ["cpu_nRESET"]),
        Pin(9,  "TDI",           ["cpld_TDI"]),
        Pin(10, "TMS",           ["cpld_TMS"]),
        Pin(11, "TCK",           ["cpld_TCK"]),
        Pin(12, "P3.11",         ["cpu_A15_1"]),
        Pin(13, "P3.14",         ["cpu_A15_2"]),
        Pin(14, "P3.15",         ["cpu_A14_1"]),
        Pin(15, "VCCINT_3V3",    ["3V3"]),
        Pin(16, "P3.17",         ["cpu_A14_2"]),
        Pin(17, "GND",           ["GND"]),
        Pin(18, "P3.16",         ["cpu_A13_1"]),
        Pin(19, "P4.2",          ["cpu_A13_2"]),
        Pin(20, "P4.5",          ["clk_16MHz"]),
        Pin(21, "P4.8",          ["ext_GP0"]),
        Pin(22, "P4.11",         ["ext_GP2"]),
        Pin(23, "P4.14",         ["ext_GP1"]),
        Pin(24, "TDO",           ["cpld_TDO"]),
        Pin(25, "GND",           ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(27, "P4.15",         ["ext_GP3"]),
        Pin(28, "P4.17",         ["ext_GP4"]),
        Pin(29, "P2.2",          ["ext_GP5"]),
        Pin(30, "P2.5",          ["ext_GP6"]),
        Pin(31, "P2.6",          ["ext_GP7"]),
        Pin(32, "P2.8",          ["ext_GP8"]),
        Pin(33, "P2.9-GSR",      ["ext_GP9"]),
        Pin(34, "P2.11-GTS2",    ["ext_GP12"]),
        Pin(35, "VCCINT_3V3",    ["3V3"]),
        Pin(36, "P2.14-GTS1",    ["ext_GP11"]),
        Pin(37, "P2.15",         ["ext_GP10"]),
        Pin(38, "P2.17",         ["abuf_ext_to_cpu"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C7")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C8")
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

# Expansion connector
# - 5v, 3v3, gnd (input)
# - 16 address lines (input)
# - 8 data lines (i/o)
# - 13 configurable lines, depending on the CPLD firmware.

connector = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x20_Pitch2.54mm",
    identifier="CON",
    value="2x20 connector for daughterboard",
	desc="2x20 0.1 inch male header",
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
        Pin("15", "", ["3V3"]),
        Pin("16", "", ["5V"]),
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
gp1_pullup = myelin_kicad_pcb.R0805("10k", "ext_GP1", "3V3", ref="R4")
gp3_pullup = myelin_kicad_pcb.R0805("10k", "ext_GP3", "3V3", ref="R5")
gp4_pullup = myelin_kicad_pcb.R0805("10k", "ext_GP4", "3V3", ref="R6")


staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(33)
]

myelin_kicad_pcb.dump_netlist("cpu_socket_expansion.net")
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
