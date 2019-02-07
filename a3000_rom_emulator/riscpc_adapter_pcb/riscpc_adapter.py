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

# --------------
# riscpc_adapter
# --------------

# by Phillip Pearson

# Adapter board to allow an a3000_rom_emulator board to fit a RISC PC.

# The RISC OS 5 sources (apache.RiscOS.Sources.HAL.IOMD.s.Top) set the ROM up
# for 5-3 MCLK cycle access.  I think MCLK is 16MHz (62.5 ns) on the RPC, so
# that works out as 312.5/187.5ns, which is comfortably within our margins
# (our flash is 70ns/15ns, plus buffer delays of ~30ns, CPLD delays of ~20ns,
# and 8ns setup time for the CPU, we end up with 128ns/73ns, so we should be
# able to handle 3-2 MCLK timing).

# The RPC TRM (ROM Control, 1-14) implies that MCLK is 32MHz, and the 5-3
# timing (initial=010 burst=10) will result in 156.25ns / 93.75ns, which is
# within our capabilities.

PROJECT_NAME = "riscpc_adapter"
PATH_TO_CPLD = "../cpld"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


rom_headers = [
    myelin_kicad_pcb.Component(
        footprint=("myelin-kicad:dip32_rom" if rom_id == 0 else "myelin-kicad:dip32_rom_data_only"),
        identifier="A3KROM%d" % (rom_id + 1),
        value="ROM header",
        desc="Adapter to emulate a 600mil 32-pin DIP, e.g. Digikey ???",
        pins=[
            Pin("13", "D0", "D%d" % (rom_id * 8 + 0)),
            Pin("14", "D1", "D%d" % (rom_id * 8 + 1)),
            Pin("15", "D2", "D%d" % (rom_id * 8 + 2)),
            Pin("16", "GND",  "GND"),
            Pin("17", "D3", "D%d" % (rom_id * 8 + 3)),
            Pin("18", "D4", "D%d" % (rom_id * 8 + 4)),
            Pin("19", "D5", "D%d" % (rom_id * 8 + 5)),
            Pin("20", "D6", "D%d" % (rom_id * 8 + 6)),
            Pin("21", "D7", "D%d" % (rom_id * 8 + 7)),
        ] + ([
            Pin( "1", "A19",    "A19"),
            Pin( "2", "A16",    "A16"),
            Pin( "3", "A15",    "A15"),
            Pin( "4", "A12",    "A12"),
            Pin( "5", "A7",     "A7"),
            Pin( "6", "A6",     "A6"),
            Pin( "7", "A5",     "A5"),
            Pin( "8", "A4",     "A4"),
            Pin( "9", "A3",     "A3"),
            Pin("10", "A2",     "A2"),
            Pin("11", "A1",     "A1"),
            Pin("12", "A0",     "A0"),
            Pin("22", "nROMCS", "nCS"),
            Pin("23", "A10",    "A10"),
            Pin("24", "nOE",    "nOE"),  # grounded on A3000 depending on jumpers
            Pin("25", "A11",    "A11"),
            Pin("26", "A9",     "A9"),
            Pin("27", "A8",     "A8"),
            Pin("28", "A13",    "A13"),
            Pin("29", "A14",    "A14"),
            Pin("30", "A17",    "A17"),
            Pin("31", "A18",    "A18"),
            Pin("32", "VCC",    "5V"),
        ] if rom_id == 0 else []),
    )
    for rom_id in range(4)
]

# To make this board easier, we remap all the address and data lines in the
# CPLD. This function takes a net on the RISC PC ROM pinout and returns the
# A3000 pin it should connect to.

# TODO make sure the cpld still builds with this mapping in place.
# Alternatively we could just pass all the lines through and mangle the data
# written into the flash to match (as long as A1/A0 are correctly mapped, this
# should still work).
def translate_rpc_net(net):
    return net

    # Leaving this in place in case I need it... managed to route everything
    # in copper so it shouldn't be necessary though!
    return {
        "A0":  "A",
        "A1":  "A",
        "A2":  "A",
        "A3":  "A",
        "A4":  "A",
        "A5":  "A",
        "A6":  "A",
        "A7":  "A",
        "A8":  "A",
        "A9":  "A",
        "A10": "A",
        "A11": "A",
        "A12": "A",
        "A13": "A",
        "A14": "A",
        "A15": "A",
        "A16": "A",
        "A17": "A",
        "A18": "A",
        "A19": "A",
        "D0":  "D",
        "D1":  "D",
        "D2":  "D",
        "D3":  "D",
        "D4":  "D",
        "D5":  "D",
        "D6":  "D",
        "D7":  "D",
        "D8":  "D",
        "D9":  "D",
        "D10": "D",
        "D11": "D",
        "D12": "D",
        "D13": "D",
        "D14": "D",
        "D15": "D",
        "D16": "D",
        "D17": "D",
        "D18": "D",
        "D19": "D",
        "D20": "D",
        "D21": "D",
        "D22": "D",
        "D23": "D",
        "D24": "D",
        "D25": "D",
        "D26": "D",
        "D27": "D",
        "D28": "D",
        "D29": "D",
        "D30": "D",
        "D31": "D",
    }.get(net, net)

rpc_headers = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:dip42_rom",
        identifier="%sROM%d" % (machine, rom_id + 1),
        value="ROM header",
        desc="Adapter to emulate a 600mil 42-pin DIP, e.g. Digikey ???",
        pins=[
            Pin(pinid, desc,
                translate_rpc_net("D%d" % (rom_id * 16 + int(desc[1:]))
                    if desc.startswith("D")
                    else desc)
            )
            for pinid, desc in [
                ( 1, "A18"),
                ( 2, "A17"),
                ( 3, "A7"),
                ( 4, "A6"),
                ( 5, "A5"),
                ( 6, "A4"),
                ( 7, "A3"),
                ( 8, "A2"),
                ( 9, "A1"),
                (10, "A0"),
                (11, "nCS"),
                (12, "GND"),
                (13, "nOE"),
                (14, "D0"),
                (15, "D8"),
                (16, "D1"),
                (17, "D9"),
                (18, "D2"),
                (19, "D10"),
                (20, "D3"),
                (21, "D11"),
                (22, "5V"),
                (23, "D4"),
                (24, "D12"),
                (25, "D5"),
                (26, "D13"),
                (27, "D6"),
                (28, "D14"),
                (29, "D7"),
                (30, "D15"),
                (31, "GND"),
                #(32, "BHE"),  # tied to 5V on RPC; pulling low puts the ROM in byte mode
                (33, "A16"),
                (34, "A15"),
                (35, "A14"),
                (36, "A13"),
                (37, "A12"),
                (38, "A11"),
                (39, "A10"),
                (40, "A9"),
                (41, "A8"),
                (42, "A19"),  # NC on 27C800
            ]
            if (rom_id == 0 and (pinid == 12 or pinid > 13))
            or (rom_id == 1 and pinid < 32)
        ],
    )
    for machine in ["RPC"]
    for rom_id in range(2)
]

# Pin to connect up A21 from a Risc PC to a v1 a3000_rom_emulator board
a21_pin = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical",
    identifier="A21",
    value="",
    pins=[Pin(1, "A21", "A19")],
)

# Likewise for nOE
a21_pin = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical",
    identifier="OE",
    value="",
    pins=[Pin(1, "nOE", "nOE")],
)


myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")



