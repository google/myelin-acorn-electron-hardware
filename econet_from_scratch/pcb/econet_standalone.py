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
        Pin( 4, "D-", ["econet_data_line_N"]),
        Pin( 2, "GND", ["GND"]),
        Pin( 5, "C+", ["econet_clock_line_P"]),
        Pin( 3, "C-", ["econet_clock_line_N"]),
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
    "56R", "bias_M", "econet_data_line_N", ref="R17")

# Line driver
# -----------

line_driver = myelin_kicad_pcb.Component(
    footprint="Housings_SOIC:SOIC-16W_5.3x10.2mm_Pitch1.27mm",
    identifier="U?",
    value="SN65C1168",
    # http://www.ti.com/product/sn65c1168
    # http://www.ti.com/general/docs/lit/getliterature.tsp?genericPartNumber=sn65c1168&fileType=pdf
    pins=[
        # Designed for full duplex, with Y/Z as outputs and A/B as inputs.
        # D is the input to the driver, R is the output from the receiver.
        # Y, A = positive output/input, Z, B = inverted output/input
        Pin( 1, "1B", "econet_data_line_P"),  # TODO(rev2) should be _N
        Pin( 2, "1A", "econet_data_line_N"),  # TODO(rev2) should be _P
        Pin( 3, "1R", "econet_data_R"),
        Pin( 4, "1DE", "econet_data_DE"),
        Pin( 5, "2R", "econet_clock_R"),
        Pin( 6, "2A", "econet_clock_line_N"),  # TODO(rev2) should be _P
        Pin( 7, "2B", "econet_clock_line_P"),  # TODO(rev2) should be _N
        Pin( 8, "GND", "GND"),
        Pin( 9, "2D", "econet_clock_D"),
        Pin(10, "2Y", "econet_clock_line_N"),  # TODO(rev2) should be _P
        Pin(11, "2Z", "econet_clock_line_P"),  # TODO(rev2) should be _N
        Pin(12, "2DE", "econet_clock_DE"),
        Pin(13, "1Z", "econet_data_line_N"),
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
dm_input = myelin_kicad_pcb.R0805("100k", "econet_data_line_N", "econet_dm_div", ref="R3")
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
    buses=["D"],
    pins=[
        Pin(39, "P1.2",       "PA22"),  # PA22
        Pin(40, "P1.5",       "PA19"),  # PA19.  Not connected to an Arduino pin.
        Pin(41, "P1.6",       "PA18"),  # PA18.  Not connected to an Arduino pin.
        Pin(42, "P1.8",       "drive_econet_clock"),  # PA16
        Pin(43, "P1.9-GCK1",  "econet_clock_from_mcu"),  # PA17
        Pin(44, "P1.11-GCK2", "clock_24m"),  # PA15
        Pin( 1, "P1.14-GCK3", "serial_mcu_to_cpld"),  # PA14
        Pin( 2, "P1.15",      "mcu_is_transmitting"),  # PA11
        Pin( 3, "P1.17",      "outputting_frame"),  # PA10
        Pin( 5, "P3.2",       "serial_buffer_empty"),  # PA09
        Pin( 6, "P3.5",       "serial_cpld_to_mcu"),  # PA08
        Pin( 7, "P3.8",       "RnW"),
        Pin( 8, "P3.9",       "nNETINT"),
        Pin(12, "P3.11",      "nADLC"),
        Pin(13, "P3.14",      "PHI2"),
        Pin(14, "P3.15",      "A0"),
        Pin(16, "P3.17",      "A1"),
        Pin(18, "P3.16",      "D0"),
        Pin(19, "P4.2",       "D1"),
        Pin(20, "P4.5",       "D2"),
        Pin(21, "P4.8",       "D3"),
        Pin(22, "P4.11",      "D4"),
        Pin(23, "P4.14",      "D5"),
        Pin(27, "P4.15",      "D6"),
        Pin(28, "P4.17",      "D7"),
        Pin(29, "P2.2",       "nRESET"),
        Pin(30, "P2.5",       "econet_clock_D"),
        Pin(31, "P2.6",       "econet_clock_R"),
        Pin(32, "P2.8",       "econet_clock_DE"),
        Pin(33, "P2.9-GSR",   "econet_data_DE"),
        Pin(34, "P2.11-GTS2", "econet_data_R"),
        Pin(36, "P2.14-GTS1", "econet_data_D"),
        Pin(37, "P2.15",      "collision_detect"),
        Pin(38, "P2.17",      "PA23"),  # PA23

        Pin(4, "GND", ["GND"]),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "TMS", ["cpld_TMS"]),
        Pin(11, "TCK", ["cpld_TCK"]),
        Pin(15, "VCCINT_3V3", ["3V3"]),
        Pin(17, "GND", ["GND"]),
        Pin(24, "TDO", ["cpld_TDO"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(35, "VCCINT_3V3", ["3V3"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C3")
myelin_kicad_pcb.update_xilinx_constraints(cpld, os.path.join(here, PATH_TO_CPLD, "constraints.ucf"))

# cpld_jtag = myelin_kicad_pcb.Component(
#     footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm",
#     identifier="JTAG",
#     value="jtag",
#     pins=[
#         Pin(1, "TCK", ["cpld_TCK"]), # top left
#         Pin(2, "GND", ["GND"]), # top right
#         Pin(3, "TDO", ["cpld_TDO"]),
#         Pin(4, "3V3", ["3V3"]),
#         Pin(5, "TMS", ["cpld_TMS"]),
#         Pin(6, "NC"),
#         Pin(7, "NC"),
#         Pin(8, "NC"),
#         Pin(9, "TDI", ["cpld_TDI"]),
#         Pin(10, "GND", ["GND"]),
#     ],
# )

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

#DONE do we need more than this?  how about bringing out every spare CPLD pin?
# output = myelin_kicad_pcb.Component(
#     footprint="Pin_Headers:Pin_Header_Straight_2x07_Pitch2.54mm",
#     identifier="EXT",
#     value="ext",
#     pins=[
#         Pin(1, "", "ext0"),
#         Pin(2, "GND", "GND"),
#         Pin(3, "", "ext1"),
#         Pin(4, "5V", "5V"),
#         Pin(5, "", "ext2"),
#         Pin(6, "3V3", "3V3"),
#         Pin(7, "", "ext3"),
#         Pin(8, "", "ext4"),
#         Pin(9, "", "ext5"),
#         Pin(10, "", "ext6"),
#         Pin(11, "", "ext7"),
#         Pin(12, "", "ext8"),
#     ],
# )

#DONE atsamd11c pinout + usb micro?  or just as a fifo?
#DONE make this pluggable in as a master module
module = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:bbc_master_econet_module",
    identifier="MOD",
    value="bbc master econet module",
    pins=[
        # PL2; 5 pins that connect to the DIN socket
        Pin("E1", "din_1_D+", "econet_data_line_P"),
        Pin("E2", "din_4_D-", "econet_data_line_N"),
        Pin("E3", "din_2_GND", "GND"),
        Pin("E4", "din_5_C+", "econet_clock_line_P"),
        Pin("E5", "din_3_C-", "econet_clock_line_N"),
        # PL1; 17 pins that connect to the system bus + 2 extras
        # Pin("B", "A2", ""),
        # Pin("A", "A3", ""),
        Pin( 1, "/NETINT", "nNETINT"),
        Pin( 2, "RnW", "RnW"),
        Pin( 3, "/ADLC", "nADLC"),
        Pin( 4, "PHI2", "PHI2"),
        Pin( 5, "A0", "A0"),
        Pin( 6, "A1", "A1"),
        Pin( 7, "D0", "D0"),
        Pin( 8, "D1", "D1"),
        Pin( 9, "D2", "D2"),
        Pin(10, "D3", "D3"),
        Pin(11, "D4", "D4"),
        Pin(12, "D5", "D5"),
        Pin(13, "D6", "D6"),
        Pin(14, "D7", "D7"),
        Pin(15, "/RST", "nRESET"),
        Pin(16, "0V", "GND"),
        Pin(17, "5V", "5V"),
    ],
)

mcu = myelin_kicad_pcb.Component(
    footprint="Housings_QFP:TQFP-32_7x7mm_Pitch0.8mm",
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
        Pin(11, "PA08/NMI/SERCOM2.0/0.0/AIN16", "serial_cpld_to_mcu"), # TXRX0/2 -> cpld
        Pin(12, "PA09/SERCOM2.1/0.1/AIN17", "serial_buffer_empty"), # XCK0/2 -> cpld
        Pin(13, "PA10/SERCOM2.2/0.2/AIN18", "outputting_frame"), # TXRX0/2 -> cpld
        Pin(14, "PA11/SERCOM2.3/0.3/AIN19", "mcu_is_transmitting"), # XCK0/2 -> cpld
        Pin(15, "PA14/XIN/SERCOM4.2/2.2", "serial_mcu_to_cpld"), # TXRX2/4 -> cpld GCK3
        Pin(16, "PA15/XOUT/SERCOM4.3/2.3", "clock_24m"), # XCK2/4 -> cpld GCK2.  Most shielded clock trace.
        Pin(17, "PA16/SERCOM1.0/3.0", "drive_econet_clock"), # TXRX1/3 -> cpld.  Two vias in trace.  Ground this one?
        Pin(18, "PA17/SERCOM1.1/3.1", "econet_clock_from_mcu"), # XCK1/3 -> cpld GCK1
        Pin(19, "PA18/SERCOM1.2/3.2", "PA18"), # TXRX1/3 -> cpld.  Not connected to an Arduino pin.
        Pin(20, "PA19/SERCOM1.3/3.3", "PA19"), # XCK1/3 -> cpld.  Not connected to an Arduino pin.
        Pin(21, "PA22/SERCOM3.0/5.0", "PA22"), # TXRX3/5 -> cpld
        Pin(22, "PA23/SERCOM3.1/5.1/USBSOF", "PA23"), # XCK3/5 -> cpld
        Pin(23, "PA24/USBDM", ["USBDM"]),
        Pin(24, "PA25/USBDP", ["USBDP"]),
        Pin(25, "PA27"),
        Pin(26, "nRESET", ["mcu_RESET"]),
        Pin(27, "PA28"),
        Pin(28, "GND", ["GND"]),
        Pin(29, "VDDCORE", ["VDDCORE"]),  # regulated output, needs cap to GND
        Pin(30, "VDDIN", ["3V3"]),  # decouple to GND
        Pin(31, "PA30/SWCLK", ["SWCLK"]),
        Pin(32, "PA31/SWDIO", ["SWDIO"]),
    ],
)
mcu_cap1 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C10")
mcu_cap2 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C11")
mcu_cap3 = myelin_kicad_pcb.C0805("1u", "GND", "VDDCORE", ref="C12")
# SAM D21 has an internal pull-up, so this is optional
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R18")
# The SAM D21 datasheet says a 1k pullup on SWCLK is critical for reliability
mcu_swclk_pullup = myelin_kicad_pcb.R0805("1k", "SWCLK", "3V3", ref="R19")

# SWD header for programming and debug
swd = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch1.27mm_SMD",
    identifier="SWD",
    value="swd",
    pins=[
        # Pin numbers zig-zag:
        # 1 VCC  2 SWDIO
        # 3 GND  4 SWCLK
        # 5 GND  6 NC
        # 7 NC   8 NC
        # 9 NC  10 /RESET
        Pin(1, "VTref", ["3V3"]),
        Pin(2, "SWDIO", ["SWDIO"]),
        Pin(3, "GND", ["GND"]),
        Pin(4, "SWCLK", ["SWCLK"]),
        Pin(5, "GND", ["GND"]),
        Pin(6, "TXD", ["mcu_debug_TXD"]),
        Pin(7, "NC"),
        Pin(8, "RXD", ["mcu_debug_RXD"]),
        Pin(9, "GND", ["GND"]),
        Pin(10, "RESET", ["mcu_RESET"]),
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

# USB power jumper (to power the board from the micro USB)
power_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="JP1",
    value="USB power",
    pins=[
        Pin(1, "", ["VUSB"]),
        Pin(2, "", ["5V"]),
    ],
)


# Ground plane stapling vias
for n in range(30):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
