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

# ------------------
# bbc_1mhz_serial_sd
# ------------------

# by Phillip Pearson

# BBC Micro 1MHz Bus expansion to provide a fast serial port and SD card
# interface.

# TODO(rev2) Figure out if I need a pullup on MOSI (CMD) for the SD card, or if
# that's just an MMC thing.

# TODO(rev2) Replace the Pro Micro with a USB-capable ARM chip (ATSAMD21
# probably, or maybe an ATSAMG55 to make it easy to implement HostFS)

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

# 1MHz Bus connector
bus = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:bbc_1mhz_bus_board",
    identifier="BUS1",
    value="2x17 connector for 1mhz bus",
    pins=[
        # Pin 1 is on the far left, at the bottom, looking into
        # the connector pins with the bbc micro flipped upside down.

        # Given how the body of the BBC slopes upwards, I'm pretty
        # sure it'll be easier to mount the connector on the underside
        # of the board.  This should give us some clearance for tall
        # components (Pro Micro or SD socket) there too.

        # Kjell Sundby's PiTubeDirect under-BBC signal converter
        # manages to work with the connector on the top of the board
        # (even with the BBC mounting screw in the way!), so that's
        # an option if mounting it on the bottom isn't.

        # If mounted on the bottom, I imagine the pin layout will
        # look like this from the top:

        # --- board edge ---
        # [ 2 4 6 8 ... 34 ]
        # [ 1 3 5 7 ... 33 ]

        # In total here we have 23 signals: 8 data + 8 address + 7 control
        # We need four pins for the SD card's SPI signals
        # Plus six pins for the BBC comms
        # = 32, leaving one free.
        # Send this through to the AVR just in case, and bring *everything*
        # out as GPIO so we can just not fit the AVR and micro SD card if we
        # want a pure GPIO board.

        Pin("1", "GND", ["GND"]),
        Pin("2", "RnW", ["bbc_RnW"]),
        Pin("3", "GND", ["GND"]),
        Pin("4", "1MHZE", ["bbc_1MHZE"]),
        Pin("5", "GND", ["GND"]),
        Pin("6", "nNMI", ["bbc_nNMI"]),
        Pin("7", "GND", ["GND"]),
        Pin("8", "nIRQ", ["bbc_nIRQ"]),
        Pin("9", "GND", ["GND"]),
        Pin("10", "nPGFC", ["bbc_nPGFC"]),
        Pin("11", "GND", ["GND"]),
        Pin("12", "nPGFD", ["bbc_nPGFD"]),
        Pin("13", "GND", ["GND"]),
        Pin("14", "nRESET", ["bbc_nRESET"]),
        Pin("15", "GND", ["GND"]),
        Pin("16", "AUDIO_IN_OUT"),
        Pin("17", "GND", ["GND"]),
        Pin("18", "D0", ["bbc_D0"]),
        Pin("19", "D1", ["bbc_D1"]),
        Pin("20", "D2", ["bbc_D2"]),
        Pin("21", "D3", ["bbc_D3"]),
        Pin("22", "D4", ["bbc_D4"]),
        Pin("23", "D5", ["bbc_D5"]),
        Pin("24", "D6", ["bbc_D6"]),
        Pin("25", "D7", ["bbc_D7"]),
        Pin("26", "GND", ["GND"]),
        Pin("27", "A0", ["bbc_A0"]),
        Pin("28", "A1", ["bbc_A1"]),
        Pin("29", "A2", ["bbc_A2"]),
        Pin("30", "A3", ["bbc_A3"]),
        Pin("31", "A4", ["bbc_A4"]),
        Pin("32", "A5", ["bbc_A5"]),
        Pin("33", "A6", ["bbc_A6"]),
        Pin("34", "A7", ["bbc_A7"]),
    ],
)

# CPLD glue: Xilinx XC9572XL-10VQG44
# https://www.xilinx.com/support/documentation/data_sheets/ds057.pdf
# VQ44 package: https://www.xilinx.com/support/documentation/package_specs/vq44.pdf
cpld = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:xilinx_vqg44",
    identifier="PL1",
    value="XC9572XL",
    # Prefixes used by update_xilinx_constraints to turn pin names like elk_D0 into
    # signal IDs like elk_D<0> in constraints.ucf:
    buses=["bbc_D", "bbc_A"],
    pins=[
        Pin(39, "P1.2", ["bbc_RnW"]),
        Pin(40, "P1.5", ["sd_nSS"]),
        Pin(41, "P1.6", ["sd_MOSI"]),
        Pin(42, "P1.8", ["sd_SCK"]),
        Pin(43, "P1.9-GCK1", ["bbc_1MHZE"]),
        Pin(44, "P1.11-GCK2", ["sd_MISO"]),
        Pin(1, "P1.14-GCK3", ["avr_MISC1"]),
        Pin(2, "P1.15", ["avr_nSD_SEL"]),
        Pin(3, "P1.17", ["avr_nSS"]),
        Pin(4, "GND", ["GND"]),
        Pin(5, "P3.2", ["avr_SCK"]),
        Pin(6, "P3.5", ["avr_MISO"]),
        Pin(7, "P3.8", ["avr_MOSI"]),
        Pin(8, "P3.9", ["avr_INT"]),
        Pin(9, "TDI", ["cpld_TDI"]),
        Pin(10, "TMS", ["cpld_TMS"]),
        Pin(11, "TCK", ["cpld_TCK"]),
        Pin(12, "P3.11", ["bbc_A7"]),
        Pin(13, "P3.14", ["bbc_A6"]),
        Pin(14, "P3.15", ["bbc_A5"]),
        Pin(15, "VCCINT_3V3", ["3V3"]),
        Pin(16, "P3.17", ["bbc_A4"]),
        Pin(17, "GND", ["GND"]),
        Pin(18, "P3.16", ["bbc_A3"]),
        Pin(19, "P4.2", ["bbc_A2"]),
        Pin(20, "P4.5", ["bbc_A1"]),
        Pin(21, "P4.8", ["bbc_A0"]),
        Pin(22, "P4.11", ["bbc_D7"]),
        Pin(23, "P4.14", ["bbc_D6"]),
        Pin(24, "TDO", ["cpld_TDO"]),
        Pin(25, "GND", ["GND"]),
        Pin(26, "VCCIO_2V5_3V3", ["3V3"]),
        Pin(27, "P4.15", ["bbc_D5"]),
        Pin(28, "P4.17", ["bbc_D4"]),
        Pin(29, "P2.2", ["bbc_D3"]),
        Pin(30, "P2.5", ["bbc_D2"]),
        Pin(31, "P2.6", ["bbc_D1"]),
        Pin(32, "P2.8", ["bbc_D0"]),
        Pin(33, "P2.9-GSR", ["bbc_nRESET"]),
        Pin(34, "P2.11-GTS2", ["bbc_nPGFD"]),
        Pin(35, "VCCINT_3V3", ["3V3"]),
        Pin(36, "P2.14-GTS1", ["bbc_nPGFC"]),
        Pin(37, "P2.15", ["bbc_nIRQ"]),
        Pin(38, "P2.17", ["bbc_nNMI"]),
    ],
)
cpld_cap1 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C1")
cpld_cap2 = myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C2")
myelin_kicad_pcb.update_xilinx_constraints(
    cpld, os.path.join(here, "../bbc_1mhz_bus_cpld/constraints.ucf"))

# altera jtag header, like in the lc-electronics xc9572xl board
# left column: tck tdo tms nc tdi
# right column: gnd vcc nc nc gnd
cpld_jtag = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm",
    identifier="JTAG1",
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

# 5V input from one of the other ports
ext_power = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
    identifier="EXTPWR",
    value="ext pwr",
    pins=[
        Pin(1, "A", ["GND"]),
        Pin(2, "B", ["3V3"]),
        Pin(3, "C", ["5V"]),
    ],
)

regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="U?",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C3")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C4")

# Just in case we want another hardware serial port
avr_serial = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm",
    identifier="SERIAL",
    value="serial",
    pins=[
        Pin(1, "GND", ["GND"]),
        Pin(2, "TX", ["avr_TXD"]),
        Pin(3, "RX", ["avr_RXD"]),
    ],
)

# Sparkfun Pro Micro
pro_micro = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:pro_micro",
    # footprint="Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm",
    identifier="U?",
    value="Pro Micro 5V",
    pins=[
        # two rows of 12 pins, counter clockwise with pin 1 at top left
        Pin(1, "D1_TX_PD3", ["avr_TXD"]),
        Pin(2, "D0_RX_PD2", ["avr_RXD"]),
        Pin(3, "GND", ["GND"]),
        Pin(4, "GND", ["GND"]),
        Pin(5, "D2_SDA_PD1"),
        Pin(6, "D3_SCL_OC0B_PD0",),
        Pin(7, "D4_A6_PD4"),
        Pin(8, "D5_nOC4A_PC6"),
        Pin(9, "D6_A7_OC4D_PD7", ["avr_MISC1"]),
        Pin(10, "D7_PE6"),
        Pin(11, "D8_A8_PB4", ["avr_nSD_SEL"]),
        Pin(12, "D9_A9_nOC4B_PB5", ["avr_nSS"]), # pull this one up
        Pin(13, "D10_A10_OC4B_PB6", ["avr_INT"]),
        Pin(14, "D16_MOSI_PB2", ["avr_MOSI"]),
        Pin(15, "D14_MISO_PB3", ["avr_MISO"]),
        Pin(16, "D15_SCK_PB1", ["avr_SCK"]),
        Pin(17, "D18_A0_PF7", ["cpld_TDO"]),
        Pin(18, "D19_A1_PF6", ["cpld_TMS"]),
        Pin(19, "D20_A2_PF5", ["cpld_TCK"]),
        Pin(20, "D21_A3_PF4", ["cpld_TDI"]),
        Pin(21, "VCC"), # NC - power supplied by the board
        Pin(22, "RST"),
        Pin(23, "GND", ["GND"]),
        Pin(24, "VRAW"), # NC - power supplied by the board
    ],
)

# Micro SD socket, because a full size SD card socket won't fit in the tiny
# amount of space we have available!
sd_card = myelin_kicad_pcb.Component(
    # footprint="myelin-kicad:fci_sd_card_socket",
    footprint="myelin-kicad:hirose_micro_sd_card_socket",
    identifier="SD1",
    value="SD Socket",
    pins=[
        # Pin("WP", "WP"),  # full size SD only
        Pin(8, "DAT1"),
        Pin(7, "DAT0_MISO", ["sd_MISO"]),
        Pin(6, "VSS", ["GND"]),
        Pin(5, "CLK_SCK", ["sd_SCK"]),
        Pin(4, "VDD", ["3V3"]),
        # Pin(3, "VSS"),  # full size SD only
        # Pin("CD", "CD"),  # full size SD only
        Pin(3, "CMD_MOSI", ["sd_MOSI"]),  # pin 3 on micro SD, 2 on full SD
        Pin(2, "CD_DAT3_CS", ["sd_nSS"]),  # pin 2 on micro SD, 1 on full SD
        Pin(1, "DAT2"),  # pin 1 on micro SD, 9 on full SD
        Pin("SH1", "GND"),
        Pin("SH2", "GND"),
    ],
)
#TODO figure out if this is necessary -- might only be with MMC cards
#sd_cmd_pullup = myelin_kicad_pcb.R0805("10k", "3V3", "sd_MOSI")

# In case we want to use an external SD adapter
ext_sd = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm",
    identifier="EXTSD",
    value="ext sd",
    pins=[
        Pin(1, "1", ["sd_nSS"]),
        Pin(2, "2", ["sd_MOSI"]),
        Pin(3, "3", ["3V3"]),
        Pin(4, "4", ["sd_SCK"]),
        Pin(5, "5", ["GND"]),
        Pin(6, "6", ["sd_MISO"]),
    ],
)

for n in range(7):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )

myelin_kicad_pcb.dump_netlist("bbc_1mhz_serial_sd.net")
