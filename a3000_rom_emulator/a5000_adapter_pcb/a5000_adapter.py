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

# -------------
# a5000_adapter
# -------------

# by Phillip Pearson

# Adapter board to allow an a3000_rom_emulator board to fit an A5000.

PROJECT_NAME = "a5000_adapter"
PATH_TO_CPLD = "../cpld"


import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

rom_headers = [
    myelin_kicad_pcb.Component(
        footprint="myelin-kicad:dip32_rom" if machine == 'A3K' else "myelin-kicad:dip32_rom_bottom",
        identifier="%sROM%d" % (machine, rom_id + 1),
        value="ROM header",
        desc="Adapter to emulate a 600mil 32-pin DIP, e.g. Digikey ???",
        pins=[
            Pin(str(pin_id), str(pin_id), "rom%d_pin%d" % (rom_id + 1, pin_id))
            for pin_id in range(40)
        ],
    )
    for machine in ("A5K", "A3K")
    for rom_id in range(4)
]

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt")



