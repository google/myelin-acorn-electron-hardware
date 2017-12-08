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
# rom_socket_level_shifter
# ------------------------

# by Phillip Pearson

# Simple board that sits in a BBC ROM socket and provides 3.3V access to all the
# signals.

# Buffers for the A bus, nOE, and nCS are always active, and are inputs on the
# ROM socket and outputs on the expansion header.

# Buffers for the D bus are inputs on the expansion header and outputs on the
# ROM socket, and are activated by pulling ext_dbuf_nCE low.

# Expansion header signals:
# - A0-13: address bus (output)
# - nCS, nOE: active-low chip selects (output)
# - D0-7: data bus (input)
# - 5V, 3V3, GND
# Total 27 pins.  7x4 header will give 28, so we can throw in an extra ground.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


rom = myelin_kicad_pcb.Component(
    footprint="Housings_DIP:DIP-28_W15.24mm",
    identifier="ROM",
    value="BBC ROM",
    pins=[
        Pin( 1, "VPP"),
        Pin( 2, "", "A12"),
        Pin( 3, "", "A7"),
        Pin( 4, "", "A6"),
        Pin( 5, "", "A5"),
        Pin( 6, "", "A4"),
        Pin( 7, "", "A3"),
        Pin( 8, "", "A2"),
        Pin( 9, "", "A1"),
        Pin(10, "", "A0"),
        Pin(11, "", "D0"),
        Pin(12, "", "D1"),
        Pin(13, "", "D2"),
        Pin(14, "GND", "GND"),
        Pin(15, "", "D3"),
        Pin(16, "", "D4"),
        Pin(17, "", "D5"),
        Pin(18, "", "D6"),
        Pin(19, "", "D7"),
        Pin(20, "", "nCS"),
        Pin(21, "", "A10"),
        Pin(22, "", "nOE"),
        Pin(23, "", "A11"),
        Pin(24, "", "A9"),
        Pin(25, "", "A8"),
        Pin(26, "", "A13"),
        Pin(27, "A14"),
        Pin(28, "VCC", "5V"),

    ],
)

# 3v3 regulator for buffers and whatever's on the other side of the connector
regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="REG",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C2", handsoldering=False)
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C3", handsoldering=False)

# address and data buffers
data_buf = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="DBUF",
    value="74LVC245",
    pins=[
        Pin( 1, "A->B", ["GND"]),
        Pin( 2, "A0", ["D2"]),
        Pin( 3, "A1", ["D1"]),
        Pin( 4, "A2", ["D0"]),
        Pin( 5, "A3", ["D7"]),
        Pin( 6, "A4", ["D6"]),
        Pin( 7, "A5", ["D5"]),
        Pin( 8, "A6", ["D4"]),
        Pin( 9, "A7", ["D3"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["ext_D2"]),
        Pin(12, "B6", ["ext_D1"]),
        Pin(13, "B5", ["ext_D0"]),
        Pin(14, "B4", ["ext_D7"]),
        Pin(15, "B3", ["ext_D6"]),
        Pin(16, "B2", ["ext_D5"]),
        Pin(17, "B1", ["ext_D4"]),
        Pin(18, "B0", ["ext_D3"]),
        # Ideally we would generate this ourselves, but it needs to be
        # !nOE NAND !nCS, which needs extra logic.
        Pin(19, "nCE", ["ext_dbuf_nCE"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
dbuf_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C4", handsoldering=False)
dbuf_nCE_pullup = myelin_kicad_pcb.R0805("19k", "ext_dbuf_nCE", "3V3", ref="R1", handsoldering=False)


addr_buf_lo = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="ABUFL",
    value="74LVC245",
    pins=[
        Pin( 1, "A->B", ["3V3"]),
        Pin( 2, "A0", ["A0"]),
        Pin( 3, "A1", ["A1"]),
        Pin( 4, "A2", ["A2"]),
        Pin( 5, "A3", ["A3"]),
        Pin( 6, "A4", ["A11"]),
        Pin( 7, "A5", ["nOE"]),
        Pin( 8, "A6", ["A10"]),
        Pin( 9, "A7", ["nCS"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["ext_A0"]),
        Pin(12, "B6", ["ext_A1"]),
        Pin(13, "B5", ["ext_A2"]),
        Pin(14, "B4", ["ext_A3"]),
        Pin(15, "B3", ["ext_A11"]),
        Pin(16, "B2", ["ext_nOE"]),
        Pin(17, "B1", ["ext_A10"]),
        Pin(18, "B0", ["ext_nCS"]),
        Pin(19, "nCE", ["GND"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
addr_buf_lo_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C5", handsoldering=False)

addr_buf_hi = myelin_kicad_pcb.Component(
    footprint="Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm",
    identifier="ABUFH",
    value="74LVC245",
    pins=[
        Pin( 1, "A->B", ["3V3"]),
        Pin( 2, "A0", ["A4"]),
        Pin( 3, "A1", ["A5"]),
        Pin( 4, "A2", ["A6"]),
        Pin( 5, "A3", ["A7"]),
        Pin( 6, "A4", ["A12"]),
        Pin( 7, "A5", ["A13"]),
        Pin( 8, "A6", ["A8"]),
        Pin( 9, "A7", ["A9"]),
        Pin(10, "GND", ["GND"]),
        Pin(11, "B7", ["ext_A4"]),
        Pin(12, "B6", ["ext_A5"]),
        Pin(13, "B5", ["ext_A6"]),
        Pin(14, "B4", ["ext_A7"]),
        Pin(15, "B3", ["ext_A12"]),
        Pin(16, "B2", ["ext_A13"]),
        Pin(17, "B1", ["ext_A8"]),
        Pin(18, "B0", ["ext_A9"]),
        Pin(19, "nCE", ["GND"]),
        Pin(20, "VCC", ["3V3"]),
    ],
)
addr_buf_hi_cap = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C6", handsoldering=False)

# 3.3V connectors
conns = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:header_2x07_100mil",
        identifier="CON1",
        value="3.3V #1",
        pins=[
            Pin( "1", "", ["3V3"]),
            Pin( "2", "", ["ext_nCS"]),
            Pin( "3", "", ["GND"]),
            Pin( "4", "", ["ext_A9"]),
            Pin( "5", "", ["ext_A8"]),
            Pin( "6", "", ["ext_A13"]),
            Pin( "7", "", ["ext_A12"]),
            Pin( "8", "", ["ext_A7"]),
            Pin( "9", "", ["ext_A6"]),
            Pin("10", "", ["ext_A5"]),
            Pin("11", "", ["ext_D1"]),
            Pin("12", "", ["ext_A4"]),
            Pin("13", "", ["5V"]),
            Pin("14", "", ["ext_D2"]),
        ]
    ),
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:header_2x07_100mil",
        identifier="CON2",
        value="3.3V #2",
        pins=[
            Pin( "1", "", ["ext_dbuf_nCE"]),
            Pin( "2", "", ["ext_A10"]),
            Pin( "3", "", ["ext_D3"]),
            Pin( "4", "", ["ext_nOE"]),
            Pin( "5", "", ["ext_D4"]),
            Pin( "6", "", ["ext_A11"]),
            Pin( "7", "", ["ext_A3"]),
            Pin( "8", "", ["ext_D5"]),
            Pin( "9", "", ["ext_A2"]),
            Pin("10", "", ["ext_D6"]),
            Pin("11", "", ["ext_D0"]),
            Pin("12", "", ["ext_D7"]),
            Pin("13", "", ["ext_A0"]),
            Pin("14", "", ["ext_A1"]),
        ]
    ),
]

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(7)
]

myelin_kicad_pcb.dump_netlist("rom_socket_level_shifter.net")
