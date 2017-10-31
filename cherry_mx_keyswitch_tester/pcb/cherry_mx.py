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
# cherry_mx
# ---------

# by Phillip Pearson

# A little tester board for a couple of Cherry MX keyswitches

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

def cherry_with_diode(a_net, b_net, ref="K?"):
    # SOD-323 = 1.7 x 1.25 x 0.95 mm body
    # c.f. 0805 resistor = 2.032 x 1.27 mm
    d_net = "%s_%s_diode" % (a_net, b_net)
    diode = myelin_kicad_pcb.Component(
        footprint="Diodes_SMD:D_SOD-323_HandSoldering",
        identifier="%sD" % ref,
        value="diode",
        pins=[
            Pin(2, "2", d_net),
            Pin(1, "1", b_net),
        ],
    )
    return myelin_kicad_pcb.Component(
        footprint="myelin-kicad:cherry_mx_pcb_mount",
        identifier=ref,
        value="keyswitch",
        pins=[
            Pin(1, "1", a_net),
            Pin(2, "2", d_net),
        ],
    )

cherry_with_diode("x", "y")

ext = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x04_Pitch2.54mm",
    identifier="EXT",
    value="ext",
    pins=[
        Pin(1, "5V", ["5V"]),
        Pin(2, "X", ["x"]),
        Pin(3, "Y", ["x_y_diode"]),
        Pin(4, "GND", ["y"]),
    ],
)

myelin_kicad_pcb.R0805("10k", "x", "5V")


myelin_kicad_pcb.dump_netlist("cherry_mx.net")
