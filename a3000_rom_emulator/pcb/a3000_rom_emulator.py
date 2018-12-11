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
# and a big CPLD, to allow it to be updated without removing it from the
# machine.

# A note on address line numbering.  The ARM provides address lines LA0-LA25,
# which address individual bytes.  The ROM is four bytes wide, so its A0
# connects to LA2. 2MB ROM = 512k x 32; LA2-LA20 connect to ROM A0-18.  On the
# A3000, LA16-18 (A18-20) are wired via jumpers, but on the A3xx, these
# jumpers aren't always fitted, so this board provides headers to solder them
# in (or just jumper them, if your motherboard provides them).

# Design rules for this board:
# JLCPCB 4 layer service: https://jlcpcb.com/capabilities/Capabilities
# - min trace/space: 0.0889mm (3.5mil)
# - min via-to-trace: 0.127mm (5mil)
# - min via: 0.45mm dia, 0.2mm drill
# - vias inside BGA: 0.51mm (20.1 mil) dia, 0.25mm (9.8 mil) drill.

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
# TODO read stencil design guidelines in IPC-7525A

# (done) can I use BGA?  xc95144 comes in cs144 package, which is 0.8mm 12x12mm (c.f. 22x22mm for TQ144) and flash comes in 1mm pitch 13x11 64-ball BGA

# (done) Figure out how to correctly route the flash.  Can we use a daisy chain with stubs?  Rule of thumb from https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/an/an224.pdf is that TDstub < 1/3 of rise time.  In our case rise time is about 1.5-2ns, so worst case Tdstub should be < 0.5ns, so 7.5cm.

# (done) figure out how to correctly daisy chain all the flash address and control signals through the three BGAs. FLASH2/FLASH3 are the best bet so far: 8 data lines out top and bottom, 26 signals coming out the left side: A0-21 plus four.  need to get these out the right side too.

# (done) add 3v3 reg
# (done) use tag-connect instead of SWD, for low profile? -- http://www.tag-connect.com/Materials/TC2030-CTX.pdf
# (done) add power diodes so we can power from USB or arc

# (done) add 10k pullup for Romcs* to help when not plugged in
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "rom_nCS", "5V", ref="R4")
# (done) add jumpers so we can get LA18, LA19 and LA20 from flying leads on pre-A3000 machines (IC28 on A3xx)
# (done) add pin to wire to A21, so we can support 4MB ROMs
# (done) add pin to wire to reset, so we can re-reset the machine once the board is alive
# (done) make footprint for xilinx_csg144
# (done) make footprint for s29 flash
# (done) add USB MCU (atsamd51 or 21?)
# (done) add 96MHz (64MHz?) oscillator footprint, in case we want that clock

osc = myelin_kicad_pcb.Component(
    footprint="Oscillator:Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm_HandSoldering",
    identifier="OSC",
    value="osc",
    # When ordering: double check it's the 3.2x2.5mm package
    # http://ww1.microchip.com/downloads/en/DeviceDoc/20005529B.pdf
    #    DSC100X-C-X-X-096.000-X
    pins=[
        Pin(1, "STANDBY#",  "3V3"),
        Pin(2, "GND",       "GND"),
        Pin(3, "OUT",       "cpld_clock_osc"),
        Pin(4, "VDD",       "3V3"),
    ],
)


# Notes on BGA soldering (I'm using NSMD everywhere):
# - https://forum.kicad.info/t/how-to-build-a-nsmd-footprint-in-kicad/4889/2
# - https://medium.com/supplyframe-hardware/confessions-of-a-pcb-designer-on-solder-mask-e592b45e5483

# (done) figure out what flash to use
    # CHOSEN: BGA-64 version of S29GL064S (cheapest and best).
    # previously picked S29GL064N90TFI040: $3.34, 64mbit, 48tsop,
    # 90+25ns access time, which was good enough, and the quicker
    # version still isn't quick enough for single cycle access on
    # a 12MHz bus (e.g. A5000).

cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_csg144",
    identifier="CPLD",
    value="XC95144XL-10CSG144",
    buses=["rom_A", "rom_D", "flash_A", "flash0_DQ", "flash1_DQ"],
    pins=[
        # cpld has 28 signals out N, 29 out E, 32-4=28 S, 31 W = 116 -- approx correct :)
        # (done) rom_A0-19, rom_nROMCS, arc_D0-31, arc_nRESET (54)
            # 17 pins from directly above cpld, 13 from top right, 24 from right
        # (done) flash_* - A*22, ctl*3, D*32 (57)
        # (done) SPI to MCU x 4 (4)
        # (done) clock -- one from oscillator, one from MCU (separate from SCK)
        # == 117
        # MCU can drive flash_nRESET and read flash_READY
        Pin( "A1", "VCCIO",    "3V3"),
        Pin( "A2", "",         "rom_A13"),
        Pin( "A3", "",         "rom_A7"),
        Pin( "A4", "",         "rom_A19"),
        Pin( "A5", "",         "rom_A11"),
        Pin( "A6", "",         "rom_A10"),
        Pin( "A7", "",         "arc_RESET"),
        Pin( "A8", "",         "rom_A5"),
        Pin( "A9", "",         "rom_A16"),
        Pin("A10", "",         "rom_D6"),
        Pin("A11", "",         "rom_A3"),
        Pin("A12", "",         "rom_D5"),
        Pin("A13", "VCCIO",    "3V3"),
        Pin( "B1", "",         "flash1_DQ3"),
        Pin( "B2", "GND",      "GND"),
        Pin( "B3", "VCCINT",   "3V3"),
        Pin( "B4", "",         "rom_A8"),
        Pin( "B5", "",         "rom_A9"),
        Pin( "B6", "",         "rom_A6"),
        Pin( "B7", "",         "rom_A18"),
        Pin( "B8", "GND",      "GND"),
        Pin( "B9", "",         "rom_A17"),
        Pin("B10", "",         "rom_D7"),
        Pin("B11", "",         "rom_A4"),
        Pin("B12", "GND",      "GND"),
        Pin("B13", "",         "rom_A0"),
        Pin( "C1", "",         "flash1_DQ1"),
        Pin( "C2", "",         "flash1_DQ5"),
        Pin( "C3", "",         "flash1_DQ11"),
        Pin( "C4", "",         "rom_A15"),
        Pin( "C5", "",         "rom_A14"),
        Pin( "C6", "",         "rom_nCS"),
        Pin( "C7", "VCCIO",    "3V3"),
        Pin( "C8", "TDO",      "cpld_TDO"),
        Pin( "C9", "",         "rom_D19"),
        Pin("C10", "GND",      "GND"),
        Pin("C11", "",         "rom_A2"),
        Pin("C12", "",         "rom_A1"),
        Pin("C13", "",         "rom_D1"),
        Pin( "D1", "VCCINT",   "3V3"),
        Pin( "D2", "",         "flash1_DQ9"),
        Pin( "D3", "",         "flash0_DQ3"),
        Pin( "D4", "",         "flash0_DQ11"),
        Pin( "D5", "",         "flash0_DQ5"),
        Pin( "D6", "",         "rom_A12"),
        Pin( "D7", "",         "rom_D4"),
        Pin( "D8", "",         "rom_D3"),
        Pin( "D9", "",         "rom_D10"),
        Pin("D10", "",         "rom_D25"),
        Pin("D11", "",         "rom_D0"),
        Pin("D12", "",         "rom_D2"),
        Pin("D13", "",         "rom_D15"),

        Pin( "E1", "",         "flash1_DQ2"),
        Pin( "E2", "",         "flash1_DQ8"),
        Pin( "E3", "",         "flash_nOE"),
        Pin( "E4", "",         "flash_A4"),
        Pin("E10", "",         "rom_D18"),
        Pin("E11", "GND",      "GND"),
        Pin("E12", "",         "rom_D14"),
        Pin("E13", "",         "rom_D13"),
        Pin( "F1", "",         "flash0_DQ1"),
        Pin( "F2", "",         "flash1_DQ0"),
        Pin( "F3", "",         "flash_A3"),
        Pin( "F4", "",         "flash_A6"),
        Pin("F10", "",         "rom_D20"),
        Pin("F11", "",         "rom_D17"),
        Pin("F12", "",         "rom_D12"),
        Pin("F13", "",         "rom_D11"),
        Pin( "G1", "GND",      "GND"),
        Pin( "G2", "",         "flash0_DQ9"),
        Pin( "G3", "",         "flash_A7"),
        Pin( "G4", "",         "flash_A0"),
        Pin("G10", "",         "rom_D9"),
        Pin("G11", "",         "rom_D26"),
        Pin("G12", "GND",      "GND"),
        Pin("G13", "GND",      "GND"),
        Pin( "H1", "",         "flash0_DQ2"),
        Pin( "H2", "",         "flash0_DQ8"),
        Pin( "H3", "",         "flash_A18"),
        Pin( "H4", "",         "flash_A21"),
        Pin("H10", "",         "rom_D16"),
        Pin("H11", "",         "rom_D28"),
        Pin("H12", "",         "rom_D8"),
        Pin("H13", "",         "rom_D24"),
        Pin( "J1", "",         "flash_nCE"),
        Pin( "J2", "",         "flash0_DQ0"),
        Pin( "J3", "",         "flash_A20"),
        Pin( "J4", "",         "flash_A19"),
        Pin("J10", "",         "flash1_DQ10"),
        Pin("J11", "",         "flash1_DQ4"),
        Pin("J12", "",         "rom_D27"),
        Pin("J13", "VCCINT",   "3V3"),

        Pin( "K1", "GND",      "GND"),
        Pin( "K2", "GCK1",     "cpld_clock_osc"),
        Pin( "K3", "",         "cpld_SS"),
        Pin( "K4", "",         "flash_A11"),
        Pin( "K5", "",         "flash_A9"),
        Pin( "K6", "",         "flash_A14"),
        Pin( "K7", "",         "flash0_DQ14"),
        Pin( "K8", "",         "flash1_DQ7"),
        Pin( "K9", "",         "flash1_DQ14"),
        Pin("K10", "",         "flash1_DQ6"),
        Pin("K11", "",         "rom_D30"),
        Pin("K12", "",         "rom_D29"),
        Pin("K13", "",         "rom_D21"),
        Pin( "L1", "GCK2",     "cpld_SCK"),
        Pin( "L2", "",         "cpld_MISO"),
        Pin( "L3", "",         "flash_A17"),
        Pin( "L4", "VCCINT",   "3V3"),
        Pin( "L5", "",         "flash_A13"),
        Pin( "L6", "",         "flash0_DQ7"),
        Pin( "L7", "VCCIO",    "3V3"),
        Pin( "L8", "",         "flash0_DQ15"),
        Pin( "L9", "TDI",      "cpld_TDI"),
        Pin("L10", "TCK",      "cpld_TCK"),
        Pin("L11", "",         "flash1_DQ12"),
        Pin("L12", "",         "rom_D23"),
        Pin("L13", "",         "rom_D22"),
        Pin( "M1", "",         "cpld_MOSI"),
        Pin( "M2", "GND",      "GND"),
        Pin( "M3", "",         "flash_A1"),
        Pin( "M4", "",         "flash_A2"),
        Pin( "M5", "GND",      "GND"),
        Pin( "M6", "",         "flash_A12"),
        Pin( "M7", "",         "flash_A16"),
        Pin( "M8", "",         "flash0_DQ12"),
        Pin( "M9", "GND",      "GND"),
        Pin("M10", "",         "flash0_DQ10"),
        Pin("M11", "",         "flash1_DQ15"),
        Pin("M12", "GND",      "GND"),
        Pin("M13", "",         "rom_D31"),
        Pin( "N1", "VCCIO",    "3V3"),
        Pin( "N2", "GCK3",     "cpld_clock_from_mcu"),
        Pin( "N3", "",         "flash_A5"),
        Pin( "N4", "",         "flash_nWE"),
        Pin( "N5", "",         "flash_A10"),
        Pin( "N6", "",         "flash_A8"),
        Pin( "N7", "",         "flash_A15"),
        Pin( "N8", "",         "flash0_DQ13"),
        Pin( "N9", "",         "flash0_DQ6"),
        Pin("N10", "TMS",      "cpld_TMS"),
        Pin("N11", "",         "flash0_DQ4"),
        Pin("N12", "",         "flash1_DQ13"),
        Pin("N13", "VCCIO",    "3V3"),
    ],
)
# This chip has a ton of power pins!  Add a ton of capacitors.
cpld_caps = [
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="CC%d" % n)
    for n in range(2)
] + [
    myelin_kicad_pcb.C0402("100n", "3V3", "GND", ref="CC%d" % n)
    for n in range(2, 10)
]
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, PATH_TO_CPLD, "constraints.ucf"))

# Diode and rectifier calculations:
# - CPLD uses max 250mA, realistically 60-120mA.
# - MCU uses max 10mA
# - flash uses max 60mA during erase and 80mA during powerup (so 120-160 mA)
# So 190-290 mA for the whole board.

# 1A diode: Diode_SMD:D_SMA package for S1ATR diode -- https://www.digikey.com/product-detail/en/S1ATR/1655-1502-1-ND/6022947/?itemSeq=278232946
diodes = [
    myelin_kicad_pcb.Component(
        footprint="Diode_SMD:D_SMA",
        identifier="D?",
        value="S1ATR",
        desc="Rectifier diode",
        pins=[
            Pin(1, "1", "5V"),
            Pin(2, "2", src),
        ],
    )
    for src in ("rom_5V", "VUSB")
]

# 10uf capacitor on 5V input
power_in_cap = myelin_kicad_pcb.C0805("10u", "GND", "5V", ref="C1")

# Power regulation from 5V down to 3.3V.
# Power comes through a diode, so we have 4.3V, which means max Vdo is 1V.

# MCP1700 is good but maxes out at 250 mA.
# Use the AP7365 instead.  0.3Vdo (max 0.4Vdo) at 600mA, which means 0.18W (0.24W max).
# At 190mA 57mW, at 290mA 87mW
# Thermal resistance in SOT-89 package is 133 C/W, so 0.24W->32C, 0.18W->24C, 0.087W->12C, 0.057->8C.
# Thermal protection kicks in when junction hits 145C, so we're OK as long as ambient < 113C :)
# Pinout: Y: 1=out 2=gnd 3=in; YR: 1=gnd 2=in 3=out.

# 3v3 regulator for buffers and whatever's on the other side of the connector
regulator = myelin_kicad_pcb.Component(
    footprint="Package_TO_SOT_SMD:SOT-89-3",
    identifier="REG",
    value="AP7365-33YG-XX",  # 600 mA, 0.3V dropout
    desc="3.3V LDO regulator, e.g. Digikey AP7365-33YG-13DICT-ND.  Search for the exact part number because there are many variants.",
    # TODO verify pinout on PCB against datasheet
    pins=[
        # MCP1700 and AP7365-YR: GND VIN VOUT
        # Pin(1, "GND", ["GND"]),
        # Pin(2, "VIN", ["5V"]),  # sot-89 tab
        # Pin(3, "VOUT", ["3V3"]),
        # AP7365-Y: VOUT GND VIN  AP7365-33YG-...
        Pin(1, "VOUT", ["3V3"]),
        Pin(2, "GND", ["GND"]),  # sot-89 tab
        Pin(3, "VIN", ["5V"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C6")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C7")

# Helpful power input/output
ext_power = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
    identifier="EXTPWR",
    value="ext pwr",
    desc="1x3 0.1 inch male header",
    pins=[
        Pin(1, "A", ["GND"]),
        Pin(2, "B", ["3V3"]),
        Pin(3, "C", ["rom_5V"]),
    ],
)

# Flash (low halfword)
flash = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:cypress_lae064_fbga",
        identifier="FLASH%d" % flash_id,
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
            Pin("A4", "RY/BY#",  "flash_READY"),
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
        ],
    )
    for flash_id in (0, 1)
]
# Three capacitors per chip (2 x Vio, 1 x Vcc)
flash_caps = [
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="FC%d" % n)
    for n in range(6)
]

# 4 x 32-pin ROM footprint, to plug into the A3000 motherboard
# 32 pins = D0-7, A0-18, CS, OE, WE, 5V, GND.
rom_headers = [
    myelin_kicad_pcb.Component(
        footprint=("myelin-kicad:dip32_rom" if rom_id == 0 else "myelin-kicad:dip32_rom_data_only"),
        identifier="ROM%d" % (rom_id + 1),
        value="ROM header",
        desc="Adapter to emulate a 600mil 32-pin DIP, e.g. Digikey ???",
        pins=[
            Pin("13", "D0", "rom_D%d" % (rom_id * 8 + 0)),
            Pin("14", "D1", "rom_D%d" % (rom_id * 8 + 1)),
            Pin("15", "D2", "rom_D%d" % (rom_id * 8 + 2)),
            Pin("16", "GND",  "GND"),
            Pin("17", "D3", "rom_D%d" % (rom_id * 8 + 3)),
            Pin("18", "D4", "rom_D%d" % (rom_id * 8 + 4)),
            Pin("19", "D5", "rom_D%d" % (rom_id * 8 + 5)),
            Pin("20", "D6", "rom_D%d" % (rom_id * 8 + 6)),
            Pin("21", "D7", "rom_D%d" % (rom_id * 8 + 7)),
        ] + ([
            Pin( "1", "Vpp"),  # On A5000 this can be A12; safest to leave NC
            Pin( "2", "A16",    "rom_A16_ext"),
            Pin( "3", "A15",    "rom_A15"),
            Pin( "4", "A12",    "rom_A12"),
            Pin( "5", "A7",     "rom_A7"),
            Pin( "6", "A6",     "rom_A6"),
            Pin( "7", "A5",     "rom_A5"),
            Pin( "8", "A4",     "rom_A4"),
            Pin( "9", "A3",     "rom_A3"),
            Pin("10", "A2",     "rom_A2"),
            Pin("11", "A1",     "rom_A1"),
            Pin("12", "A0",     "rom_A0"),
            Pin("22", "nROMCS", "rom_nCS"),
            Pin("23", "A10",    "rom_A10"),
            Pin("24", "nOE"),  # grounded on A3000 depending on jumpers
            Pin("25", "A11",    "rom_A11"),
            Pin("26", "A9",     "rom_A9"),
            Pin("27", "A8",     "rom_A8"),
            Pin("28", "A13",    "rom_A13"),
            Pin("29", "A14",    "rom_A14"),
            Pin("30", "A17",    "rom_A17_ext"),
            Pin("31", "A18",    "rom_A18_ext"),
            Pin("32", "VCC",    "rom_5V"),
        ] if rom_id == 0 else []),
    )
    for rom_id in range(4)
]

# Jumpers / connectors for address lines not present on all boards
address_jumpers = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical",
    identifier="AEXT",
    value="Extras",
    pins=[
        # ARM LA18 / ROM A16
        Pin(1, "arc_A16_LA18",   "rom_A16_ext"),  
        Pin(2, "cpld_A16_LA18",  "rom_A16"),
        # ARM LA19 / ROM A17
        Pin(3, "arc_A17_LA19",   "rom_A17_ext"),
        Pin(4, "cpld_A17_LA19",  "rom_A17"),
        # ARM LA20 / ROM A18
        Pin(5, "arc_A18_LA20",   "rom_A18_ext"),
        Pin(6, "cpld_A18_LA20",  "rom_A18"),
        # ARM LA21 / ROM A19 (optional extra, for 4MB ROM space)
        Pin(7, "cpld_A19_LA21",  "rom_A19"),
        # Resetter -- so we can reset the system once everything has started up (if necessary).
        # This can go to LK3 pin 1 (reset from ext keyboard), or IC35 pin 2, or IC47 pin 13.
        Pin(8, "reset",          "arc_RESET"),
    ],
)

# Second address hookup area, nearer ICs on A310/A3000
address_hookup_2 = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
    identifier="AEXT2",
    value="Addresses",
    pins=[
        # ARM LA18 / ROM A16
        Pin(1, "cpld_A16_LA18",  "rom_A16"),
        # ARM LA19 / ROM A17
        Pin(2, "cpld_A17_LA19",  "rom_A17"),
        # ARM LA20 / ROM A18
        Pin(3, "cpld_A18_LA20",  "rom_A18"),
        # ARM LA21 / ROM A19 (optional extra, for 4MB ROM space)
        Pin(4, "cpld_A19_LA21",  "rom_A19"),
    ],
)


# Micro USB socket
micro_usb = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:micro_usb_b_smd_molex",
    identifier="USB",
    value="usb",
    desc="Molex 1050170001 (Digikey WM1399CT-ND) surface mount micro USB socket with mounting holes.",
    pins=[
        Pin(1, "V", ["VUSB"]),
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "ID", ["USB_ID"]),
        Pin(5, "G", ["GND"]),
    ],
)


mcu = myelin_kicad_pcb.Component(
    footprint="Package_QFP:TQFP-32_7x7mm_P0.8mm",
    identifier="MCU",
    value="ATSAMD21E18A",  # 256k flash, 32k sram, 32 pins
    pins=[
        # It looks like SECOM4 and SERCOM5 don't exist on the D21E, so we only
        # have SERCOM0-3.

        Pin(1, "PA00/XIN32/SERCOM1.0", "mcu_debug_TXD"),
        Pin(2, "PA01/XOUT32/SERCOM1.1", "mcu_debug_RXD"),
        Pin(3, "PA02/AIN0/DAC_OUT"),
        Pin(4, "PA03/ADC_VREFA/AIN1"),
        Pin(5, "PA04/SERCOM0.0/AIN4", "cpld_TDO"), # sercom0 is mcu comms
        Pin(6, "PA05/SERCOM0.1/AIN5", "cpld_TCK"),
        Pin(7, "PA06/SERCOM0.2/AIN6", "cpld_TMS"), # TXD0/RXD0
        Pin(8, "PA07/SERCOM0.3/AIN7", "cpld_TDI"), # XCK0
        Pin(9, "VDDANA", ["3V3"]),  # decouple to GND
        Pin(10, "GND", ["GND"]),
        Pin(11, "PA08/NMI/SERCOM2.0/0.0/AIN16", "cpld_MOSI"), # TXRX0/2 -> cpld
        Pin(12, "PA09/SERCOM2.1/0.1/AIN17", "cpld_SCK"), # XCK0/2 -> cpld
        Pin(13, "PA10/SERCOM2.2/0.2/AIN18", "cpld_SS"), # TXRX0/2 -> cpld
        Pin(14, "PA11/SERCOM2.3/0.3/AIN19", "cpld_MISO"), # XCK0/2 -> cpld
        Pin(15, "PA14/XIN/SERCOM4.2/2.2", "flash_nRESET"), # TXRX2/4 -> cpld GCK
        Pin(16, "PA15/XOUT/SERCOM4.3/2.3", "flash_READY"), # XCK2/4 -> cpld GCK
        Pin(17, "PA16/SERCOM1.0/3.0", "mcu_GPIO5"), # TXRX1/3
        Pin(18, "PA17/SERCOM1.1/3.1", "mcu_GPIO4"), # XCK1/3 -> cpld GCK
        Pin(19, "PA18/SERCOM1.2/3.2", "mcu_GPIO3"), # TXRX1/3.  Not connected to an Arduino pin.
        Pin(20, "PA19/SERCOM1.3/3.3", "mcu_GPIO2"), # XCK1/3.  Not connected to an Arduino pin.
        Pin(21, "PA22/SERCOM3.0/5.0", "mcu_GPIO1"), # TXRX3/5
        Pin(22, "PA23/SERCOM3.1/5.1/USBSOF", "mcu_GPIO0"), # XCK3/5
        Pin(23, "PA24/USBDM", ["USBDM"]),
        Pin(24, "PA25/USBDP", ["USBDP"]),
        Pin(25, "PA27"),
        Pin(26, "nRESET", ["mcu_RESET"]),
        Pin(27, "PA28", "cpld_clock_from_mcu"), # probably unused, extra GCK connection
        Pin(28, "GND", ["GND"]),
        Pin(29, "VDDCORE", ["VDDCORE"]),  # regulated output, needs cap to GND
        Pin(30, "VDDIN", ["3V3"]),  # decouple to GND
        Pin(31, "PA30/SWCLK", ["mcu_SWCLK"]),
        Pin(32, "PA31/SWDIO", ["mcu_SWDIO"]),
    ],
)
mcu_cap1 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C10")
mcu_cap2 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C11")
mcu_cap3 = myelin_kicad_pcb.C0805("1u", "GND", "VDDCORE", ref="C12")
# SAM D21 has an internal pull-up, so this is optional
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R1")
# The SAM D21 datasheet says a 1k pullup on SWCLK is critical for reliability
mcu_swclk_pullup = myelin_kicad_pcb.R0805("1k", "mcu_SWCLK", "3V3", ref="R2")

# SWD header for programming and debug using a Tag-Connect TC2030-CTX
swd = myelin_kicad_pcb.Component(
    footprint="Tag-Connect_TC2030-IDC-FP_2x03_P1.27mm_Vertical",
    identifier="SWD",
    value="swd",
    pins=[
        # Tag-Connect SWD layout: http://www.tag-connect.com/Materials/TC2030-CTX.pdf
        Pin(1, "VCC",       "3V3"),
        Pin(2, "SWDIO/TMS", "mcu_SWDIO"),
        Pin(3, "nRESET",    "mcu_RESET"),
        Pin(4, "SWCLK/TCK", "mcu_SWCLK"),
        Pin(5, "GND",       "GND"),
        Pin(6, "SWO/TDO"),  # NC because Cortex-M0 doesn't use these
    ],
)

# 0.1" SWD header so people can debug without a Tag-Connect
swd_alt = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical",
    identifier="SWD2",
    value="swd",
    pins=[
        Pin(1, "SWDIO/TMS", "mcu_SWDIO"),
        Pin(2, "VCC",       "3V3"),
        Pin(3, "SWCLK/TCK", "mcu_SWCLK"),
        Pin(4, "GND",       "GND"),
        Pin(5, "nRESET",    "mcu_RESET"),
        Pin(6, "GND",       "GND"),
        Pin(7, "TXD",       "mcu_debug_TXD"),
        Pin(8, "RXD",       "mcu_debug_RXD"),
    ],
)

# 0.1" header for a few more MCU pins
mcu_gpio = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical",
    identifier="GPIO",
    value="gpio",
    pins=[
        Pin(1, "GND",    "GND"),
        Pin(2, "VCC",    "3V3"),
        Pin(3, "GPIO0",  "mcu_GPIO0"),
        Pin(4, "GPIO1",  "mcu_GPIO1"),
        Pin(5, "GPIO2",  "mcu_GPIO2"),
        Pin(6, "GPIO3",  "mcu_GPIO3"),
        Pin(7, "GPIO4",  "mcu_GPIO4"),
        Pin(8, "GPIO5",  "mcu_GPIO5"),
    ],
)

# Extra holes near ROM4 to provide mechanical stability for the USB connector (suggestion from IanS)
mechanical_holes = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:dip_rom_single_pin",
        identifier="mech_pin%d" % (n+1),
        value="",
        pins=[Pin(1, "")],
    )
    for n in range(8)
]

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(30)
]


myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")



