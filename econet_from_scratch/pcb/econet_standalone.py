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

# -----------------
# econet_standalone
# -----------------

# by Phillip Pearson

# A standalone Econet station, designed to be connected to a microcontroller.

PROJECT_NAME = "econet_standalone"
PATH_TO_CPLD = "../cpld"

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# Power
# -----

ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["3V3"]),
        Pin(3, "", ["5V"]),
    ],
)
power_cap = myelin_kicad_pcb.C0805("10u", "5V", "GND", ref="C9")

# Econet socket
# -------------

econet_socket = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:din_5_econet_pcb_mount",
    identifier="U?",
    value="Econet",
    pins=[
        # DIN-5 pins are numbered weirdly -- 1, 4, 2, 5, 3 around the circle
        Pin( 1, "D+", ["econet_data_line_P"]),
        Pin( 4, "D-", ["econet_data_line_M"]),
        Pin( 2, "GND", ["GND"]),
        Pin( 5, "C+", ["econet_clock_line_P"]),
        Pin( 3, "C-", ["econet_clock_line_M"]),
    ],
)

# Econet data line termination / biasing
# --------------------------------------

# 1k/220R/1k voltage divider drawing 2.25mA and giving 2.25/2.75V on D-/D+

termination_r1 = myelin_kicad_pcb.R0805(
    "1k", "5V", "bias_P", ref="R13")
termination_r2 = myelin_kicad_pcb.R0805(
    "220R", "bias_P", "bias_M", ref="R14")
termination_r3 = myelin_kicad_pcb.R0805(
    "1k", "bias_M", "GND", ref="R15")
termination_r4 = myelin_kicad_pcb.R0805(
    "56R", "bias_P", "econet_data_line_P", ref="R16")
termination_r5 = myelin_kicad_pcb.R0805(
    "56R", "bias_M", "econet_data_line_M", ref="R17")

# Line driver
# -----------

line_driver = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-16W_5.3x10.2mm_Pitch1.27mm",
    identifier="U?",
    value="SN65C1168",
    pins=[
        # Designed for full duplex, with Y/Z as outputs and A/B as inputs.
        # D is the input to the driver, R is the output from the receiver.
        Pin( 1, "1B", "econet_data_line_P"),
        Pin( 2, "1A", "econet_data_line_M"),
        Pin( 3, "1R", "econet_data_R"),
        Pin( 4, "1DE", "econet_data_DE"),
        Pin( 5, "2R", "econet_clock_R"),
        Pin( 6, "2A", "econet_clock_line_M"),
        Pin( 7, "2B", "econet_clock_line_P"),
        Pin( 8, "GND", "GND"),
        Pin( 9, "2D", "econet_clock_D"),
        Pin(10, "2Y", "econet_clock_line_M"),
        Pin(11, "2Z", "econet_clock_line_P"),
        Pin(12, "2DE", "econet_clock_DE"),
        Pin(13, "1Z", "econet_data_line_M"),
        Pin(14, "1Y", "econet_data_line_P"),
        Pin(15, "1D", "econet_data_D"),
        Pin(16, "VCC", "5V"),
    ],
)
line_driver_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C7")

# Collision detection
# -------------------

# 2V reference
vdiv_2v_top = myelin_kicad_pcb.R0805("1k5", "5V", "cd_vdiv_2v", ref="R1")
vdiv_2v_bot = myelin_kicad_pcb.R0805("1k", "cd_vdiv_2v", "GND", ref="R2")
vdiv_2v_bot_c = myelin_kicad_pcb.R0805("10u", "cd_vdiv_2v", "GND", ref="C1")

# D- and D+ are coupled in through 100k resistors and pulled to 2V with 10k
dm_input = myelin_kicad_pcb.R0805("100k", "econet_data_line_M", "econet_dm_div", ref="R3")
dp_input = myelin_kicad_pcb.R0805("100k", "econet_data_line_P", "econet_dp_div", ref="R4")
dm_2v_pull = myelin_kicad_pcb.R0805("10k", "econet_dm_div", "cd_vdiv_2v", ref="R5")
dp_2v_pull = myelin_kicad_pcb.R0805("10k", "econet_dp_div", "cd_vdiv_2v", ref="R6")

# 56k input resistors to lm319
lm319_dm_m = myelin_kicad_pcb.R0805("56k", "econet_dm_div", "lm319_dm_m", ref="R7")
lm319_dp_m = myelin_kicad_pcb.R0805("56k", "econet_dp_div", "lm319_dp_m", ref="R8")
lm319_dm_p = myelin_kicad_pcb.R0805("56k", "econet_dm_div", "econet_centre", ref="R9")
lm319_dp_p = myelin_kicad_pcb.R0805("56k", "econet_dp_div", "econet_centre", ref="R10")

# pull to 5V so econet_centre is slightly above the midway point
econet_centre_pull = myelin_kicad_pcb.R0805("1M5", "econet_centre", "5V", ref="R11")

# Dual OC comparator that will pull low if there is more than approx 0.25V
# difference between D- and D+.
lm319 = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="U?",
    value="LM319",
    pins=[
        Pin( 1, "NC"),
        Pin( 2, "NC"),
        Pin( 3, "GND1", ["GND"]),
        Pin( 4, "+IN1", ["econet_centre"]),
        Pin( 5, "-IN1", ["lm319_dp_m"]),
        Pin( 6, "V-", ["GND"]),
        Pin( 7, "OUT2", ["collision_detect"]),
        Pin( 8, "GND2", ["GND"]),
        Pin( 9, "+IN2", ["econet_centre"]),
        Pin(10, "-IN2", ["lm319_dm_m"]),
        Pin(11, "V+", ["5V"]),
        Pin(12, "OUT1", ["collision_detect"]),
        Pin(13, "NC"),
        Pin(14, "NC"),
    ],
)
lm319_cap = myelin_kicad_pcb.C0805("100n", "5V", "GND", ref="C8")

# pullup (lm319 is OC)
cd_pullup = myelin_kicad_pcb.R0805("1k", "collision_detect", "5V", ref="R12")
cd_pullup_c = myelin_kicad_pcb.C0805("10n", "collision_detect", "5V", ref="C6")

# CPLD
# ----

# Signals we need here:

# - collision_detect
# - econet_data_R
# - econet_data_D
# - econet_data_DE
# - econet_clock_R
# - econet_clock_D
# - econet_clock_DE
# - serial connection to MCU (5 pins that can be USRT or SPI)

cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="U4",
    value="XC9572XL",
    pins=[
        Pin(39, "P1.2", [""]),
        Pin(40, "P1.5", [""]),
        Pin(41, "P1.6", [""]),
        Pin(42, "P1.8", [""]),
        Pin(43, "P1.9-GCK1", [""]),
        Pin(44, "P1.11-GCK2", [""]),
        Pin(1, "P1.14-GCK3", ["collision_detect"]),
        Pin(2, "P1.15", ["econet_data_D"]),
        Pin(3, "P1.17", ["econet_data_R"]),
        Pin(4, "GND", ["GND"]),
        Pin(5, "P3.2", ["econet_clock_DE"]),
        Pin(6, "P3.5", ["econet_data_DE"]),
        Pin(7, "P3.8", ["econet_clock_D"]),
        Pin(8, "P3.9", ["econet_clock_R"]),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "TMS", ["cpld_TMS"]),
        Pin(11, "TCK", ["cpld_TCK"]),
        Pin(12, "P3.11", [""]),
        Pin(13, "P3.14", [""]),
        Pin(14, "P3.15", [""]),
        Pin(15, "VCCINT_3V3", ["3V3"]),
        Pin(16, "P3.17", [""]),
        Pin(17, "GND", ["GND"]),
        Pin(18, "P3.16", [""]),
        Pin(19, "P4.2", [""]),
        Pin(20, "P4.5", [""]),
        Pin(21, "P4.8", [""]),
        Pin(22, "P4.11", [""]),
        Pin(23, "P4.14", [""]),
        Pin(24, "TDO", ["cpld_TDO"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(27, "P4.15", [""]),
        Pin(28, "P4.17", [""]),
        Pin(29, "P2.2", [""]),
        Pin(30, "P2.5", [""]),
        Pin(31, "P2.6", [""]),
        Pin(32, "P2.8", [""]),
        Pin(33, "P2.9-GSR", [""]),
        Pin(34, "P2.11-GTS2", [""]),
        Pin(35, "VCCINT_3V3", ["3V3"]),
        Pin(36, "P2.14-GTS1", [""]),
        Pin(37, "P2.15", [""]),
        Pin(38, "P2.17", [""]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C3")
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, PATH_TO_CPLD, "constraints.ucf"))

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
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="U5",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "5V", "GND", ref="C4")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C5")

#TODO do we need more than this?  how about bringing out every spare CPLD pin?
output = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x07_Pitch2.54mm",
    identifier="EXT",
    value="ext",
    pins=[
        Pin(1, "", "ext0"),
        Pin(2, "GND", "GND"),
        Pin(3, "", "ext1"),
        Pin(4, "5V", "5V"),
        Pin(5, "", "ext2"),
        Pin(6, "3V3", "3V3"),
        Pin(7, "", "ext3"),
        Pin(8, "", "ext4"),
        Pin(9, "", "ext5"),
        Pin(10, "", "ext6"),
        Pin(11, "", "ext7"),
        Pin(12, "", "ext8"),
    ],
)

#TODO atsamd11c pinout + usb micro?  or just as a fifo?
#TODO make this pluggable in as a master module

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
