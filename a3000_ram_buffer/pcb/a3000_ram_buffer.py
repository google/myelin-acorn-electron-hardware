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

# ----------------
# a3000_ram_buffer
# ----------------

# by Phillip Pearson

# Buffer board to scope data lines from the A3000 RAM header


PROJECT_NAME = "a3000_ram_buffer"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

def chop_into_groups(group_size, list):
    assert not len(list) % group_size, "list has %d elements, which is not a multiple of %d" % (len(list), group_size)
    return [
        list[i * group_size:(i + 1) * group_size]
        for i in range(len(list) / group_size)
    ]

# (done) Female headers to connect to RAM header on A3000 motherboard -- use long ones that can take a RAM card on top
# 60 pins: 20, big gap, 20, small gap, 20
a3000_ram_header = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:a3000_ram_header",
    identifier="RAM",
    value="Extension socket to connect to RAM header on A3000 motherboard, and mezzanine RAM board",
    pins=[
        # 32 data lines, 8 control lines (bank, oe, wr, ras, 4xcas), four 5V, six GND, 10 address = 60 pins
        Pin( 1, "5V",    "5V"),
        Pin( 2, "Rd1",   "ram_D1"),
        Pin( 3, "Rd0",   "ram_D0"),
        Pin( 4, "Bank",  "ram_BANK"),
        Pin( 5, "Oe2",   "ram_nOE2"),
        Pin( 6, "GND",   "GND"),
        Pin( 7, "Wr2",   "ram_nWR2"),
        Pin( 8, "Ras*",  "ram_nRAS"),
        Pin( 9, "Ra0",   "ram_RA0"),
        Pin(10, "Cas0*", "ram_nCAS0"),
        Pin(11, "Ra1",   "ram_RA1"),
        Pin(12, "5V",    "5V"),
        Pin(13, "Ra8",   "ram_RA8"),
        Pin(14, "Ra3",   "ram_RA3"),
        Pin(15, "Rd27",  "ram_D27"),
        Pin(16, "Cas1*", "ram_nCAS1"),
        Pin(17, "Rd3",   "ram_D3"),
        Pin(18, "GND",   "GND"),
        Pin(19, "Rd2",   "ram_D2"),
        Pin(20, "Rd4",   "ram_D4"),

        Pin(21, "Rd5",   "ram_D5"),
        Pin(22, "Rd7",   "ram_D7"),
        Pin(23, "Rd6",   "ram_D6"),
        Pin(24, "GND",   "GND"),
        Pin(25, "Rd8",   "ram_D8"),
        Pin(26, "Rd9",   "ram_D9"),
        Pin(27, "Rd11",  "ram_D11"),
        Pin(28, "Rd10",  "ram_D10"),
        Pin(29, "Rd12",  "ram_D12"),
        Pin(30, "Rd13",  "ram_D13"),
        Pin(31, "Rd15",  "ram_D15"),
        Pin(32, "Rd14",  "ram_D14"),
        Pin(33, "Cas2*", "ram_nCAS2"),
        Pin(34, "Ra4",   "ram_RA4"),
        Pin(35, "Rd16",  "ram_D16"),
        Pin(36, "GND",   "GND"),
        Pin(37, "Rd17",  "ram_D17"),
        Pin(38, "Rd19",  "ram_D19"),
        Pin(39, "Rd18",  "ram_D18"),
        Pin(40, "Ra5",   "ram_RA5"),
        
        Pin(41, "Rd20",  "ram_D20"),
        Pin(42, "GND",   "GND"),
        Pin(43, "Rd21",  "ram_D21"),
        Pin(44, "Ra9",   "ram_RA9"),
        Pin(45, "Rd23",  "ram_D23"),
        Pin(46, "Ra7",   "ram_RA7"),
        Pin(47, "Ra6",   "ram_RA6"),
        Pin(48, "5V",    "5V"),
        Pin(49, "Ra2",   "ram_RA2"),
        Pin(50, "Cas3*", "ram_nCAS3"),
        Pin(51, "Rd25",  "ram_D25"),
        Pin(52, "Rd24",  "ram_D24"),
        Pin(53, "Rd26",  "ram_D26"),
        Pin(54, "GND",   "GND"),
        Pin(55, "Rd22",  "ram_D22"),
        Pin(56, "Rd29",  "ram_D29"),
        Pin(57, "Rd30",  "ram_D30"),
        Pin(58, "Rd28",  "ram_D28"),
        Pin(59, "Rd31",  "ram_D31"),
        Pin(60, "5V",    "5V"),
    ],
)

# extra signal because we have one more pin :)
ext_signal = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    identifier="EXTSIG",
    value="ext signal",
    desc="1x2 0.1 inch male header",
    pins=[
        Pin(1, "", "GND"),
        Pin(2, "", "ext_signal"),
    ],
)


# 5 x 74LVT245 in SOIC package to minimize trace lengths
buffers = sum([
    [
        myelin_kicad_pcb.Component(
            footprint="Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm",
            identifier="BUF?",
            value="74LVC245",
            pins=[
                Pin( 1, "A->B", "GND"),  # Bn are inputs, An are outputs
                Pin( 2, "A0",   "%s_buf" % signals[0] if signals[0] else ""),
                Pin( 3, "A1",   "%s_buf" % signals[1] if signals[1] else ""),
                Pin( 4, "A2",   "%s_buf" % signals[2] if signals[2] else ""),
                Pin( 5, "A3",   "%s_buf" % signals[3] if signals[3] else ""),
                Pin( 6, "A4",   "%s_buf" % signals[4] if signals[4] else ""),
                Pin( 7, "A5",   "%s_buf" % signals[5] if signals[5] else ""),
                Pin( 8, "A6",   "%s_buf" % signals[6] if signals[6] else ""),
                Pin( 9, "A7",   "%s_buf" % signals[7] if signals[7] else ""),
                Pin(10, "GND",  "GND"),
                Pin(11, "B7",   signals[7] if signals[7] else "GND"),
                Pin(12, "B6",   signals[6] if signals[6] else "GND"),
                Pin(13, "B5",   signals[5] if signals[5] else "GND"),
                Pin(14, "B4",   signals[4] if signals[4] else "GND"),
                Pin(15, "B3",   signals[3] if signals[3] else "GND"),
                Pin(16, "B2",   signals[2] if signals[2] else "GND"),
                Pin(17, "B1",   signals[1] if signals[1] else "GND"),
                Pin(18, "B0",   signals[0] if signals[0] else "GND"),
                Pin(19, "nCE",  "GND"),  # always enable
                Pin(20, "VCC",  "3V3"),
            ],
        ),
        myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="CB?"),
        myelin_kicad_pcb.Component(
            footprint="myelin-kicad:bourns_cat16_j8_resistor_array",
            identifier="RP?",
            value="resistor pack",
            desc="8 x 68R",
            pins=sum([
                [
                    Pin("%dB" % (n+1), "%dB" % (n+1), "%s_buf" % signal if signal else "GND"),
                    Pin("%dA" % (n+1), "%dA" % (n+1), "%s_term" % signal if signal else "GND"),
                ] for n, signal in enumerate(signals)
            ], []),
        ),
        myelin_kicad_pcb.Component(
            footprint="myelin-kicad:via_array_1x7_55mil",
            identifier="STAPLE?",
            value="via array",
            desc=None,
            pins=[
                Pin(n, str(n), "GND")
                for n in range(1, 8)
            ],
        ),
    ]
    for signals in chop_into_groups(8, [
        "ram_D1",
        "ram_D0",
        "ram_BANK",
        "ram_nOE2",
        "ram_nWR2",
        "ram_nRAS",
        "ram_RA0",
        "ram_nCAS0",
        "ram_RA1",
        "ram_RA8",
        "ram_RA3",
        "ram_D27",
        "ram_nCAS1",
        "ram_D3",
        "ram_D2",
        "ram_D4",
        "ram_D5",
        "ram_D7",
        "ram_D6",
        "ram_D8",
        "ram_D9",
        "ram_D11",
        "ram_D10",
        "ram_D12",
        "ram_D13",
        "ram_D15",
        "ram_D14",
        "ram_nCAS2",
        "ram_RA4",
        "ram_D16",
        "ram_D17",
        None,
        "ram_D19",
        "ram_D18",
        "ram_RA5",
        None,
        None,
        "ram_D20",
        "ram_D21",
        "ram_RA9",
        "ram_D23",
        "ram_RA7",
        "ram_RA6",
        None,
        "ram_RA2",
        "ram_nCAS3",
        "ram_D25",
        "ram_D24",
        "ram_D26",
        "ram_D22",
        "ram_D29",
        None,
        "ram_D30",
        "ram_D28",
        "ram_D31",
        "ext_signal",
        # [
        # "ram_D1", "ram_D0", "ram_BANK", "ram_nOE2", "ram_nWR2", "ram_nRAS", "ram_RA0" "ram_nCAS0", "ram_RA1",
        # "ram_RA8", "ram_RA3", "ram_D27", "ram_nCAS1", "ram_D3", "ram_D2", "ram_D4", "ram_D5", 
        # "ram_D7", "ram_D6", "ram_D8", "ram_D9", "ram_D11", "ram_D10", "ram_D12", "ram_D13", 
        # "ram_D15", "ram_D14", "ram_nCAS2", "ram_RA4", "ram_D16", "ram_D17", "ram_D19", "ram_D18", 
        # "ram_RA5", "ram_D20", "ram_D21", "ram_RA9", "ram_D23", "ram_RA7", "ram_RA6", "ram_RA2", 
        # "ram_nCAS3", "ram_D25", "ram_D24", "ram_D26", "ram_D22", "ram_D29", "ram_D30", "ram_D28", "ram_D31",
    ])
], [])

# Original plan: 74LVT16245 x 2 to buffer signals, output to sig{A, B}{1-16}_pre
# Keeping this because I'll need 16245 for the MEMC buffer board.
# buffers = [
#     myelin_kicad_pcb.Component(
#         footprint="Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm",
#         identifier="BUFA",
#         value="74LVT16245",
#         pins=[
#             Pin( 1, "1DIR", ""),
#             Pin( 2, "1B0",  ""),
#             Pin( 3, "1B1",  ""),
#             Pin( 4, "GND",  "GND"),
#             Pin( 5, "1B2",  ""),
#             Pin( 6, "1B3",  ""),
#             Pin( 7, "VCC",  "3V3"),
#             Pin( 8, "1B4",  ""),
#             Pin( 9, "1B5",  ""),
#             Pin(10, "GND",  "GND"),
#             Pin(11, "1B6",  ""),
#             Pin(12, "1B7",  ""),
#             Pin(13, "2B0",  ""),
#             Pin(14, "2B1",  ""),
#             Pin(15, "GND",  "GND"),
#             Pin(16, "2B2",  ""),
#             Pin(17, "2B3",  ""),
#             Pin(18, "VCC",  "3V3"),
#             Pin(19, "2B4",  ""),
#             Pin(20, "2B5",  ""),
#             Pin(21, "GND",  "GND"),
#             Pin(22, "2B6",  ""),
#             Pin(23, "2B7",  ""),
#             Pin(24, "2DIR", ""),
#             Pin(25, "2nOE", ""),
#             Pin(26, "2A7",  ""),
#             Pin(27, "2A6",  ""),
#             Pin(28, "GND",  "GND"),
#             Pin(29, "2A5",  ""),
#             Pin(30, "2A4",  ""),
#             Pin(31, "VCC",  "3V3"),
#             Pin(32, "2A3",  ""),
#             Pin(33, "2A2",  ""),
#             Pin(34, "GND",  "GND"),
#             Pin(35, "2A1",  ""),
#             Pin(36, "2A0",  ""),
#             Pin(37, "1A7",  ""),
#             Pin(38, "1A6",  ""),
#             Pin(39, "GND",  "GND"),
#             Pin(40, "1A5",  ""),
#             Pin(41, "1A4",  ""),
#             Pin(42, "VCC",  "3V3"),
#             Pin(43, "1A3",  ""),
#             Pin(44, "1A2",  ""),
#             Pin(45, "GND",  "GND"),
#             Pin(46, "1A1",  ""),
#             Pin(47, "1A0",  ""),
#             Pin(48, "1nOE", ""),
#         ],
#     ),
# ]
# buffer_caps = [
#     myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C4"),
#     myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C5"),
# ]

# (done) 68R pack x 4 to terminate outbound signals
# source_termination = [
#     myelin_kicad_pcb.Component(
#         footprint="myelin-kicad:bourns_cat16_j8_resistor_array",
#         identifier="RP%d" % packid,
#         value="resistor pack",
#         desc="8 x 68R",
#         pins=sum([
#             [
#                 Pin("%dA" % (n+1), "%dA" % (n+1), "sig%s%d_buf" % (bank, n+start)),
#                 Pin("%dB" % (n+1), "%dB" % (n+1), "sig%s%d_term" % (bank, n+start)),
#             ] for n in range(8)
#         ], []),
#     )
#     for packid, bank, start in [
#         (1, "A", 1),
#         (2, "A", 9),
#         (3, "B", 1),
#         (4, "B", 9),
#     ]
# ]

# (done) 34 way header x 2 for outgoing signals
signal_headers = [
    myelin_kicad_pcb.Component(
        footprint="Connector_Multicomp:Multicomp_MC9A12-3434_2x17_P2.54mm_Vertical",
        identifier="SIG%s" % bank,
        value="signal header %s" % bank,
        desc="2x17 0.1 inch male header",
        pins=[
            Pin(n * 2 + 1, str(n * 2 + 1), ("%s_term" % signals[n]) if signals[n] else "GND")
            for n in range(17)
        ] + [
            Pin( n,  str(n), "GND")
            for n in range(2, 36, 2)
        ]
    )
    for bank, signals in [
        ("RAMD1", ["ram_D1", "ram_D0", "ram_D27", "ram_D3", "ram_D2", "ram_D4", "ram_D5", "ram_D7",
            "ram_D6", "ram_D8", "ram_D9", "ram_D11", "ram_D10", "ram_D12", "ram_D13", "ram_D15", "ram_BANK"]),
        ("RAMD2", ["ram_D14", "ram_D16", "ram_D17", "ram_D19", "ram_D18", "ram_D20", "ram_D21", "ram_D23",
            "ram_D25", "ram_D24", "ram_D26", "ram_D22", "ram_D29", "ram_D30", "ram_D28", "ram_D31", "ram_nOE2"]),
        ("RAMCS", ["ram_nWR2", "ram_nRAS", "ram_RA0", "ram_nCAS0", "ram_RA1", "ram_RA8", "ram_RA3", "ram_nCAS1",
            "ram_nCAS2", "ram_RA4", "ram_RA5", "ram_RA9", "ram_RA7", "ram_RA6", "ram_RA2", "ram_nCAS3", "ext_signal"]),
    ]
]

"""
"ram_nWR2", "ram_nRAS", "ram_RA0", "ram_nCAS0", "ram_RA1", "ram_RA8", "ram_RA3", "ram_nCAS1", "ram_nCAS2", "ram_RA4", "ram_RA5", "ram_RA9", "ram_RA7", "ram_RA6", "ram_RA2", "ram_nCAS3",
"""

# 10uf capacitor on 5V input
power_in_cap = myelin_kicad_pcb.C0805("10u", "GND", "5V", ref="C1")

# 3v3 regulator for buffers and whatever's on the other side of the connector
regulator = myelin_kicad_pcb.Component(
    footprint="Package_TO_SOT_SMD:SOT-89-3",  # (done) check still works with mcp1700t
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
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
    identifier="EXTPWR",
    value="ext pwr",
    desc="1x3 0.1 inch male header",
    pins=[
        Pin(1, "A", ["GND"]),
        Pin(2, "B", ["3V3"]),
        Pin(3, "C", ["5V"]),
    ],
)

staples = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )
    for n in range(36)
]

fiducials = [
    myelin_kicad_pcb.Component(
        footprint="Fiducial:Fiducial_1mm_Dia_2mm_Outer",
        identifier="FID%d" % (n+1),
        value="FIDUCIAL",
        pins=[],
    )
    for n in range(4)
]


myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")
