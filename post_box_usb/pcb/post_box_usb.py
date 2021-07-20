#!/usr/bin/python

# Copyright 2020 Google LLC
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

# ------------
# post_box_usb
# ------------

# by Phillip Pearson

# A USB interface for the POST connectors found on most Archimedes and Risc PC
# class machines.

# - ATSAMD21 32-pin TQFP
# - SWD header and pullups
# - Power LED
# - Micro USB socket, 3v3 regulator + capacitors
# - LCMXO256 FPGA
# - 74LCX125 hot swap buffer (possibly to replaced by a SI8642 isolator one day)
# - 74HCT125 5V buffer

# The back to back buffers are used to prevent odd things from happening when
# the two sides of the system are powered up or down at different times.  The
# 74HCT125 is powered by the target machine, and everything else is powered
# from USB.  This makes it possible to reset everything by unplugging the USB
# cable, and prevents the target machine from taking power from the output
# buffer.

# ----------------------------------------------------------------------------------
# r1: Brainstorming how to deal with reverse polarity (improved in r2, fixed? in r3)
# ----------------------------------------------------------------------------------

# If the target connector is plugged in backwards, the following happens:

# 1. target 5V    -> GND
# 2. target D0    -> target_reset output (pulls down) from 74HCT125
# 3. testreq      -> testack; output (pulls up) from 74HCT125
# 4. testack      -> testreq; input to 74LCX125
# 5. target reset -> target_D0; 2k2 to GND
# 6. target GND   -> target_5V; 74HCT125 power, one input, two output enables

# Two possible scenarios could occur.

# (A) If the host side is floating w.r.t the target.

# From the POV of the 3.3V side of the POST box, target_5V and the 74HCT125's
# supply are now at -5V.  Its ground protection diodes are still fine, but
# there is now a diode from every pin to -5V (target GND).

# testack_noe_buf_r: 1k to a 74LCX125 output
# testack, which is testreq/LA21: pulled low on the target
# target_reset, which is D0: pulled low on the target

# Another chip to consider is the 74LCX125, which has some target signals
# (testreq and target_5V) as inputs.  target_5V will receive -5V and short
# through the protection diode from ground.  testreq (testack / ROMCS) will be
# at 0V or -5V and be forced high through the diode, which won't hurt anything
# on the remote side.

# (B) If the host and target share a common ground.
# In this case, the target's 5V line is shorted to ground :/

# To mitigate this, will a protection diode from target_5V do?

# 1. target 5V    -> GND (bad if host and target share a common ground)
# 2. target D0    -> target_reset output (pulls down) from 74HCT125
# 3. testreq      -> testack; output (pulls up) from 74HCT125
# 4. testack      -> testreq; input to 74LCX125 (will be pulled up by 74LCX125 protection diode, which is OK)
# 5. target reset -> target_D0; 2k2 to GND (or nowhere if past the protection diode)
# 6. target GND   -> will appear as -5V and be blocked by the protection diode, so target_5V will float

# This will fix things UNLESS the post box and target share a common ground.

# ------------------
# Changes made in r2
# ------------------

# done(r2) clearly indicate POST connector polarity; label signals if they fit
# done(r2) add protection diode (D1) on 5V input for post_box_usb
# done(r2) add protection resistor (R15) for testreq input on post_box_usb
# done(r2) add a weak (1M?) pullup (R23) on testreq to get rid of garbage when disconnected.
# done(r2) add protection resistors on testack (R16) and reset (R17) outputs
# done(r2) add diode (D2) to prevent reset from being pulled up in a reverse polarity condition
# done(r2) separate target_GND and GND, and tie together with a bunch of parallel resistors or a single high power resistor
# done(r2) add correct/reverse polarity indicator LEDs

# Now, in the reverse polarity case:

# 1. target 5V    -> target_GND (45 mA will flow to GND via resistors if host and target share a common ground)
# 2. target D0    -> 68R to target_reset output (pulls down) from 74HCT125
# 3. testreq      -> 68R to target_testack output (pulls up) from 74HCT125
# 4. testack      -> 1k to target_testreq; input to 74LCX125 (diode to GND / target_5V)
# 5. target reset -> target_D0; 2k2 to reversed diode to target_GND
# 6. target GND   -> will appear as -5V and be blocked by the protection diode, so target_5V will float

# If I've worked this through correctly, it should now be safe to leave the
# adapter plugged in backwards indefinitely without damage.

# ------------------
# Changes made in r3
# ------------------

# done(r3) switch power protection to mosfet (PMV65XP,215)
# done(r3) add test points for testreq/testack to make them easy to scope
# done(r3) change testreq resistor to 68R and remove ground shunt (set to 0R)

# -------------------------------------------------
# Things that have been done, or are still to do...
# -------------------------------------------------

# TODO make a test script that can set up a board and validate it by testing the ibx250 or a3000
# TODO add disable mode to post_box_usb firmware, so it doesn't cause machines to hang on boot when there's no serial connection.
# TODO make post_box_usb board.py better at finding the serial port, because it's terrible on windows
# TODO see if i can make the firmware buildable (or at least flashable) without the full arduino system

# TODO(r4) Add a 1k resistor between 5V and GND to stop 10k resistors from pulling 5V up high enough to run LEDs
# TODO(r4) verify that the A5000 reset issue isn't because of the BAT54
# nope(r3) get rid of ground shunt?  or just not fit it?  make a breakable link? -- i'll leave it there but fit a link.
# done(r3) make diode footprint bigger
#  currently using Diode_SMD:D_SOD-323_HandSoldering, but BAT54GW is SOD123!
#  switch to Diode_SMD:D_SOD-123.
# done(r3) make led footprints smaller
#  https://www.we-online.de/katalog/datasheet/150080RS75000.pdf
#  LED package is 2mm wide; recommended land pattern 3.2 wide with 1.1mm wide 1.2mm tall pads.
#  LED_SMD:LED_0805_2012Metric looks right.

# done(r2) try programming the FPGA from the MCU

# done(r1) Verify 74HCT125 and 74LCX125 pinout and wiring
# done(r1) Verify that 1k series resistor and 10k pullup are sensible.
# done(r1) move the pull resistors to testack_noe_buf and target_reset_noe_buf so we don't get resistor dividers
# done(r1) connect all /OE pins on the 74LCX125 to an FPGA output and add a 10k pull resistor to 3V3
# done(r1) add a couple of LEDs driven by microcontroller GPIOs
# done(r1) verify that the regulator can handle the power draw of the mcu and fpga - yes, it can do 250 mA which wasn't enough for arcflash but should be fine here.
# done(r1) add lots of staples

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin

PROJECT_NAME = 'post_box_usb'


mcu = myelin_kicad_pcb.Component(
    footprint="Housings_QFP:TQFP-32_7x7mm_Pitch0.8mm",
    identifier="MCU",
    value="ATSAMD21E18A-AU",  # 256k flash, 32k sram, 32 pins
    desc="IC ARM MCU; https://www.digikey.com/products/en?keywords=ATSAMD21E18A-AU-ND",
    pins=[
        # We use a 32.768kHz crystal and the 96MHz FDPLL with some massive
        # multiplier.  This seems a bit weird, but all the ATSAMD21 designs I
        # can find are clocked this way.  The FDPLL has an input divider, so it
        # should be possible to use an 8MHz input, but nobody seems to do that.
        Pin(1, "PA00/XIN32", ["XTAL_IN"]),
        Pin(2, "PA01/XOUT32", ["XTAL_OUT"]),
        Pin(3, "PA02/AIN0", ["PA02"]),
        Pin(4, "PA03/ADC_VREFA/AIN1", ["PA03"]),
        Pin(5, "PA04/SERCOM0.0/AIN4", ["fpga_TDO"]),
        Pin(6, "PA05/SERCOM0.1/AIN5", ["fpga_TCK"]),
        Pin(7, "PA06/SERCOM0.2/AIN6", ["fpga_TMS"]),
        Pin(8, "PA07/SERCOM0.3/AIN7", ["fpga_TDI"]),
        Pin(9, "VDDANA", ["3V3"]),  # decouple to GND
        Pin(10, "GND", ["GND"]),
        Pin(11, "PA08/NMI/SERCOM2.0/AIN16", ["fpga_spi_mosi"]),
        Pin(12, "PA09/SERCOM2.1/AIN17", ["fpga_spi_sck"]),
        Pin(13, "PA10/SERCOM2.2/AIN18", ["fpga_clock_48mhz"]),  # GCLK_IO[4] - clock output for FPGA
        Pin(14, "PA11/SERCOM2.3/AIN19", ["target_power_out"]),  # also GCLK_IO[5] if we want a second clock output
        Pin(15, "PA14/XIN/SERCOM4.2", ["fpga_spi_cs"]),
        Pin(16, "PA15/XOUT/SERCOM4.3", ["fpga_spi_miso"]),
        Pin(17, "PA16/SERCOM1.0", ["PA16"]),
        Pin(18, "PA17/SERCOM1.1", ["PA17"]),
        Pin(19, "PA18/SERCOM1.2", ["PA18"]),
        Pin(20, "PA19/SERCOM1.3", ["PA19"]),
        Pin(21, "PA22/SERCOM3.0", ["mcu_TXD"]),
        Pin(22, "PA23/SERCOM3.1/USBSOF", ["mcu_RXD"]),
        Pin(23, "PA24/USBDM", ["USBDM"]),
        Pin(24, "PA25/USBDP", ["USBDP"]),
        Pin(25, "PA27", ["PA27"]),
        Pin(26, "nRESET", ["mcu_RESET"]),
        Pin(27, "PA28", ["reset_in"]),
        Pin(28, "GND", ["GND"]),
        Pin(29, "VDDCORE", ["VDDCORE"]),  # regulated output, needs cap to GND
        Pin(30, "VDDIN", ["3V3"]),  # decouple to GND
        Pin(31, "PA30/SWCLK", ["mcu_SWCLK"]),
        Pin(32, "PA31/SWDIO", ["mcu_SWDIO"]),
    ],
)
mcu_cap1 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C3")
mcu_cap2 = myelin_kicad_pcb.C0805("100n", "GND", "3V3", ref="C4")
mcu_cap3 = myelin_kicad_pcb.C0805("1u", "GND", "VDDCORE", ref="C5")
# SAM D21 has an internal pull-up, so this is optional
mcu_reset_pullup = myelin_kicad_pcb.R0805("10k", "mcu_RESET", "3V3", ref="R1")
# The SAM D21 datasheet says a 1k pullup on SWCLK is critical for reliability
mcu_swclk_pullup = myelin_kicad_pcb.R0805("1k", "mcu_SWCLK", "3V3", ref="R2")

# SWD header for programming and debug using a Tag-Connect TC2030-CTX
swd = myelin_kicad_pcb.Component(
    footprint="Tag-Connect_TC2030-IDC-FP_2x03_P1.27mm_Vertical",
    identifier="SWD",
    value="swd",
    desc="SWD header - Tag-Connect TC2030",
    exclude_from_bom=True,
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


# SWD header for programming and debug
swd2 = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD",
    identifier="SWD2",
    value="swd",
    desc="SWD header - ARM standard",
    pins=[
        # Pin numbers zig-zag:
        # 1 VCC  2 SWDIO
        # 3 GND  4 SWCLK
        # 5 GND  6 NC
        # 7 NC   8 NC
        # 9 NC  10 /RESET
        Pin(1, "VTref", "3V3"),
        Pin(2, "SWDIO", "mcu_SWDIO"),
        Pin(3, "GND",   "GND"),
        Pin(4, "SWCLK", "mcu_SWCLK"),
        Pin(5, "GND",   "GND"),
        Pin(6, "NC"),
        Pin(7, "NC"),
        Pin(8, "NC"),
        Pin(9, "GND",   "GND"),
        Pin(10, "RESET", "mcu_RESET"),
    ],
)

# yellow LED that lights when the USB side of the board is powered
power_led_r = myelin_kicad_pcb.R0805("330R", "3V3", "power_led_anode", ref="R3")
power_led = myelin_kicad_pcb.LED0805("power", "GND", "power_led_anode", ref="L1", jlc_part="C2296")  # JLC: 17-21SUYC/TR8

# multicolor LED - TBD
multicolor_led = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:WS2812B_PP",
    identifier="L2",
    value="WS2812B-V5",  # Need V5 for 3.3V compatibility on DI pin
    desc="RGB LED",
    pins=[
        Pin(1, "5V", "5V"),
        Pin(2, "DO", ""),
        Pin(3, "GND", "GND"),
        Pin(4, "DI", "PA19"),
    ],
)

# yellow LED that lights when the USB serial port is connected (and flashes on traffic)
mcu_txd_led_r = myelin_kicad_pcb.R0805("330R", "3V3", "mcu_txd_led_anode", ref="R13")
mcu_txd_led = myelin_kicad_pcb.LED0805("link/act", "mcu_TXD", "mcu_txd_led_anode", ref="L3", jlc_part="C2296")  # JLC: 17-21SUYC/TR8

# green LED to indicate that target is powered
target_power_led_r = myelin_kicad_pcb.R0805("330R", "target_5V_ext", "target_power_led_anode", ref="R21")
target_power_led = myelin_kicad_pcb.LED0805("target pwr", "target_GND", "target_power_led_anode", ref="L4", jlc_part="C63855")  # JLC: 17-21/GHC-XS1T2M/3T

# red LED mounted in reverse: this will light when the POST connector is plugged in backwards
target_power_reversed_led_r = myelin_kicad_pcb.R0805("330R", "target_GND", "target_power_reversed_led_anode", ref="R22")
target_power_reversed_led = myelin_kicad_pcb.LED0805("POLARITY", "target_5V_ext", "target_power_reversed_led_anode", ref="L5", jlc_part="C72037")  # JLC: 17-21SURC/S530-A3/TR8

# Micro USB socket, mounted on the bottom of the board
micro_usb = myelin_kicad_pcb.Component(
    footprint="Connector_USB:USB_Micro-B_Molex-105017-0001",
    identifier="USB",
    value="usb",
    jlc_part="C132563",  # Amphenol 10118194-0001LF
    link="https://www.digikey.com/en/products/detail/molex/1050170001/2350832",
    desc="Surface mount micro USB socket with mounting holes",
    pins=[
        Pin(1, "V", ["5V"]),  # input from host
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "ID", ["USB_ID"]),
        Pin(5, "G", ["GND"]),
    ],
)

# USB-A (host) socket
usb_host = myelin_kicad_pcb.Component(
    footprint="Connectors:USB_A",
    identifier="HOST",
    value="NF usb host",
    desc="USB-A socket",
    pins=[
        Pin(1, "V", ["5V"]),  # output to device
        Pin(2, "-", ["USBDM"]),
        Pin(3, "+", ["USBDP"]),
        Pin(4, "G", ["GND"]),
    ],
)

# MC-146 32.768000 kHz crystal
# load capacitance 12.5pF
# CL = (C1 * C2) / (C1 + C2) + Cstray
#    = C1*C1 / 2*C1 + Cstray
# 12.5pF = C1/2 + 5pF
# C1 = 2(12.5pF - 5pF)
#    = 15pF
# So we should use two 15pF caps
xtal = myelin_kicad_pcb.Component(
    footprint="Crystals:Crystal_SMD_SeikoEpson_MC146-4pin_6.7x1.5mm_HandSoldering",
    identifier="X1",
    desc="Crystal 32726Hz",
    value="NF MC146 32768Hz",
    pins=[
        Pin(1, "X1", ["XTAL_IN"]),
        Pin(4, "X2", ["XTAL_OUT"]),
    ],
)
xtal_cap1 = myelin_kicad_pcb.C0805("NF 15p", "GND", "XTAL_IN", ref="C6")
xtal_cap1 = myelin_kicad_pcb.C0805("NF 15p", "GND", "XTAL_OUT", ref="C7")

regulator = myelin_kicad_pcb.Component(
    footprint="TO_SOT_Packages_SMD:SOT-89-3",
    identifier="U1",
    desc="Voltage regulator 3.3V",
    value="MCP1700T-3302E/MB",
    pins=[
        Pin(2, "VIN", ["5V"]),
        Pin(3, "VOUT", ["3V3"]),
        Pin(1, "GND", ["GND"]),
    ],
)
reg_in_cap = myelin_kicad_pcb.C0805("1u", "GND", "5V", ref="C1")
reg_out_cap = myelin_kicad_pcb.C0805("1u", "3V3", "GND", ref="C2")

# 24 pins total:
# - 20 x gpio
# - 3v3, 5v, GND
# - /reset
# skipping: 2nd 3v3/gnd, usbdb/usbdp, swdio/swclk, xtalin/xtalout

pin_header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x13_P2.54mm_Vertical",
    identifier="CON",
    value="NF pins",
    desc="Pin header 0.1 inch 2x13",
    pins=[
        Pin(1, "", ["3V3"]),
        Pin(2, "", ["GND"]),
        Pin(3, "", ["fpga_TDO"]),
        Pin(4, "", ["PA03"]),
        Pin(5, "", ["fpga_TMS"]),
        Pin(6, "", ["fpga_TCK"]),
        Pin(7, "", ["PA02"]),
        Pin(8, "", ["fpga_TDI"]),
        Pin(9, "", ["fpga_spi_sck"]),
        Pin(10, "", ["fpga_spi_mosi"]),
        Pin(11, "", ["target_power_out"]),
        Pin(12, "", ["fpga_clock_48mhz"]),
        Pin(13, "", ["fpga_spi_miso"]),
        Pin(14, "", ["fpga_spi_cs"]),
        Pin(15, "", ["PA27"]),
        Pin(16, "", ["reset_in"]),
        Pin(17, "", ["PA17"]),
        Pin(18, "", ["PA16"]),
        Pin(19, "", ["PA19"]),
        Pin(20, "", ["PA18"]),
        Pin(21, "", ["mcu_RXD"]),
        Pin(22, "", ["mcu_TXD"]),
        Pin(23, "", ["GND"]),
        Pin(24, "", ["3V3"]),
        Pin(25, "", ["GND"]),
        Pin(26, "", ["5V"]),
    ],
)

power_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="PWR",
    value="NF power",
    desc="Pin header 0.1 inch 1x2",
    pins=[
        Pin(1, "", ["3V3"]),
        Pin(2, "", ["5V"]),
    ],
)

reset_header = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm",
    identifier="RST",
    value="NF reset",
    desc="Pin header 0.1 inch 1x2",
    pins=[
        Pin(1, "", ["GND"]),
        Pin(2, "", ["mcu_RESET"]),
    ],
)

# Lattice lcmxo256 MachXO FPGA, in 100-pin TQFP package
fpga = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:lattice_tn100",  # 14x14mm 100-pin TQFP
    identifier="FPGA",
    value="LCMXO256",
    desc="FPGA 256 LUT",
    pins=[
        Pin(  1, "PL2A",         "fpga_GPIO47"),
        Pin(  2, "PL2B",         "fpga_GPIO44"),
        Pin(  3, "PL3A",         "fpga_GPIO45"),
        Pin(  4, "PL3B",         "fpga_GPIO42"),
        Pin(  5, "PL3C",         "fpga_GPIO43"),
        Pin(  6, "PL3D",         "fpga_GPIO40"),
        Pin(  7, "PL4A",         "fpga_GPIO41"),
        Pin(  8, "PL4B",         "fpga_GPIO38"),
        Pin(  9, "PL5A",         "fpga_GPIO39"),
        Pin( 10, "VCCIO1",       ["3V3"]),
        Pin( 11, "PL5B",         "fpga_GPIO36"),
        Pin( 12, "GNDIO1",       ["GND"]),
        Pin( 13, "PL5C",         ""),
        Pin( 14, "PL5D_GSRN",    "fpga_GPIO37"),
        Pin( 15, "PL6A",         "fpga_GPIO34"),
        Pin( 16, "PL6B_TSALL",   "fpga_GPIO35"),
        Pin( 17, "PL7A",         ""),
        Pin( 18, "PL7B",         ""),
        Pin( 19, "PL7C",         ""),
        Pin( 20, "PL7D",         ""),
        Pin( 21, "PL8A",         ""),
        Pin( 22, "PL8B",         ""),
        Pin( 23, "PL9A",         "testack_noe"),
        Pin( 24, "VCCIO1",       ["3V3"]),
        Pin( 25, "GNDIO1",       ["GND"]),
        Pin( 26, "TMS",          ["fpga_TMS"]),  # has an internal pull-up resistor
        Pin( 27, "PL9B",         "target_power_3v"),
        Pin( 28, "TCK",          ["fpga_TCK"]),  # needs external 4k7 pull-DOWN resistor
        Pin( 29, "PB2A",         "target_reset_noe"),
        Pin( 30, "PB2B",         "hotswap_noe"),
        Pin( 31, "TDO",          ["fpga_TDO"]),  # has an internal pull-up resistor
        Pin( 32, "PB2C",         "testreq_3v"),
        Pin( 33, "TDI",          ["fpga_TDI"]),  # has an internal pull-up resistor
        Pin( 34, "PB2D",         "fpga_GPIO0"),
        Pin( 35, "VCC",          ["3V3"]),
        Pin( 36, "PB3A_PCLK1_1", "fpga_GPIO1"),
        Pin( 37, "PB3B",         "fpga_GPIO2"),
        Pin( 38, "PB3C_PCLK1_0", "fpga_OSC_in"),
        Pin( 39, "PB3D",         "fpga_GPIO3"),
        Pin( 40, "GND",          ["GND"]),
        Pin( 41, "VCCIO1",       ["3V3"]),
        Pin( 42, "GNDIO1",       ["GND"]),
        Pin( 43, "PB4A",         "fpga_GPIO4"),
        Pin( 44, "PB4B",         "fpga_GPIO5"),
        Pin( 45, "PB4C",         "fpga_GPIO6"),
        Pin( 46, "PB4D",         "fpga_GPIO7"),
        Pin( 47, "PB5A",         "fpga_GPIO8"),
        Pin( 48, "SLEEPN",       ["SLEEPN"]),  # needs external 4k7 pull-up resistor
        Pin( 49, "PB5C",         "fpga_GPIO9"),
        Pin( 50, "PB5D",         "fpga_GPIO10"),
        Pin( 51, "PR9B",         "fpga_GPIO11"),
        Pin( 52, "PR9A",         "fpga_GPIO12"),
        Pin( 53, "PR8B",         "fpga_GPIO13"),
        Pin( 54, "PR8A",         "fpga_GPIO14"),
        Pin( 55, "PR7D",         "fpga_GPIO15"),
        Pin( 56, "PR7C",         "fpga_GPIO16"),
        Pin( 57, "PR7B",         "fpga_GPIO17"),
        Pin( 58, "PR7A",         "fpga_GPIO18"),
        Pin( 59, "PR6B",         "fpga_GPIO19"),
        Pin( 60, "VCCIO0",       ["3V3"]),
        Pin( 61, "PR6A",         "fpga_GPIO20"),
        Pin( 62, "GNDIO0",       ["GND"]),
        Pin( 63, "PR5D",         "fpga_GPIO21"),
        Pin( 64, "PR5C",         "fpga_GPIO22"),
        Pin( 65, "PR5B",         "fpga_GPIO23"),
        Pin( 66, "PR5A",         "fpga_GPIO24"),
        Pin( 67, "PR4B",         "fpga_GPIO25"),
        Pin( 68, "PR4A",         "fpga_GPIO26"),
        Pin( 69, "PR3D",         "fpga_GPIO27"),
        Pin( 70, "PR3C",         "fpga_GPIO28"),
        Pin( 71, "PR3B",         "fpga_GPIO29"),
        Pin( 72, "PR3A",         "fpga_GPIO30"),
        Pin( 73, "PR2B",         "fpga_GPIO31"),
        Pin( 74, "VCCIO0",       ["3V3"]),
        Pin( 75, "GNDIO0",       ["GND"]),
        Pin( 76, "PR2A",         "fpga_GPIO32"),
        Pin( 77, "PT5C",         "fpga_GPIO33"),
        Pin( 78, "PT5B",         "mcu_RXD"),
        Pin( 79, "PT5A",         "mcu_TXD"),
        Pin( 80, "PT4F",         "PA19"),
        Pin( 81, "PT4E",         "PA18"),
        Pin( 82, "PT4D",         "PA17"),
        Pin( 83, "PT4C",         "PA16"),
        Pin( 84, "GND",          ["GND"]),
        Pin( 85, "PT4B_PCLK0_1", ["target_power_out"]),
        Pin( 86, "PT4A_PCLK0_0", ["fpga_clock_48mhz"]),
        Pin( 87, "PT3D",         "PA27"),
        Pin( 88, "VCCAUX",       ["3V3"]),
        Pin( 89, "PT3C",         "reset_in"),
        Pin( 90, "VCC",          ["3V3"]),
        Pin( 91, "PT3B",         "fpga_spi_miso"),
        Pin( 92, "VCCIO0",       ["3V3"]),
        Pin( 93, "GNDIO0",       ["GND"]),
        Pin( 94, "PT3A",         "fpga_spi_cs"),
        Pin( 95, "PT2F",         "fpga_spi_sck"),
        Pin( 96, "PT2E",         "fpga_spi_mosi"),
        Pin( 97, "PT2D",         "PA02"),
        Pin( 98, "PT2C",         "PA03"),
        Pin( 99, "PT2B",         ""),
        Pin(100, "PT2A",         "fpga_GPIO46"),
    ],
)
machxo_sleepn_pullup = myelin_kicad_pcb.R0805("4k7", "SLEEPN", "3V3", ref="R4")
machxo_tck_pulldown = myelin_kicad_pcb.R0805("4k7", "fpga_TCK", "GND", ref="R5")

lpf_fn = '%s.lpf' % PROJECT_NAME
with open(lpf_fn, 'w') as fpga_lpf:
    for pin in fpga.pins:
        nets = [net for net in pin.nets if net and net not in ('GND', '3V3', 'fpga_TMS', 'fpga_TCK', 'fpga_TDI', 'fpga_TDO', 'SLEEPN')]
        if not nets: continue
        net, = nets
        print('LOCATE COMP "%s" SITE "%d" ;' % (net, pin.number), file=fpga_lpf)
        print('IOBUF PORT "%s" IO_TYPE=LVCMOS33 PULLMODE=NONE DRIVE=NA SLEWRATE=FAST OPENDRAIN=OFF INF=OFF ;' % (net,), file=fpga_lpf)
    print("Wrote Lattice-formatted pinout suitable for copying into project .lpf as %s" % lpf_fn)

# The LCMXO256 has a ton of power/gnd pairs!
fpga_caps = [
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C8"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C9"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C10"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C11"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C12"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C13", handsoldering=False),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C14"),
    myelin_kicad_pcb.C0805("100n", "3V3", "GND", ref="C15"),
]

# MachXO/MachXO2 JTAG header, Lattice format
# See: https://github.com/google/myelin-acorn-electron-hardware/blob/master/notes/pld_programming_and_jtag.md
fpga_jtag = myelin_kicad_pcb.Component(
    footprint="Connector_Multicomp:Multicomp_MC9A12-1034_2x05_P2.54mm_Vertical",
    identifier="FPGA_JTAG",
    value="NF lattice jtag",
    desc="Pin header 0.1 inch 2x5 for JTAG programming.  Use generic 0.1 inch header strip or Digikey ED1543-ND.",
    pins=[
        Pin( 1, "TCK",  "fpga_TCK"), # top left
        Pin( 2, "GND",  "GND"),      # top right
        Pin( 3, "TMS",  "fpga_TMS"),
        Pin( 4, "GND",  "GND"),
        Pin( 5, "TDI",  "fpga_TDI"),
        Pin( 6, "VCC",  "3V3"),
        Pin( 7, "TDO",  "fpga_TDO"),
        Pin( 8, "INIT", ""),  # INITN on machxo2, NC on machxo
        Pin( 9, "TRST", ""),  # DONE on machxo2, NC on machxo
        Pin(10, "PROG", ""),  # PROGRAMN on machxo2, NC on machxo
    ],
)

fpga_gpio = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical",
    identifier="FPGA_IO",
    value="NF pins",
    desc="Pin header 0.1 inch 2x20",
    pins=[
        Pin( 1, "", ["GND"]),
        Pin( 2, "", ["3V3"]),
        Pin( 3, "", ["fpga_GPIO0"]),
        Pin( 4, "", ["fpga_GPIO1"]),
        Pin( 5, "", ["fpga_GPIO2"]),
        Pin( 6, "", ["fpga_GPIO3"]),
        Pin( 7, "", ["fpga_GPIO4"]),
        Pin( 8, "", ["fpga_GPIO5"]),
        Pin( 9, "", ["fpga_GPIO6"]),
        Pin(10, "", ["fpga_GPIO7"]),
        Pin(11, "", ["fpga_GPIO8"]),
        Pin(12, "", ["fpga_GPIO9"]),
        Pin(13, "", ["fpga_GPIO10"]),
        Pin(14, "", ["fpga_GPIO11"]),
        Pin(15, "", ["fpga_GPIO12"]),
        Pin(16, "", ["fpga_GPIO13"]),
        Pin(17, "", ["fpga_GPIO14"]),
        Pin(18, "", ["fpga_GPIO15"]),
        Pin(19, "", ["fpga_GPIO16"]),
        Pin(20, "", ["fpga_GPIO17"]),
        Pin(21, "", ["fpga_GPIO18"]),
        Pin(22, "", ["fpga_GPIO19"]),
        Pin(23, "", ["fpga_GPIO20"]),
        Pin(24, "", ["fpga_GPIO21"]),
        Pin(25, "", ["fpga_GPIO22"]),
        Pin(26, "", ["fpga_GPIO23"]),
        Pin(27, "", ["fpga_GPIO24"]),
        Pin(28, "", ["fpga_GPIO25"]),
        Pin(29, "", ["fpga_GPIO26"]),
        Pin(30, "", ["fpga_GPIO27"]),
        Pin(31, "", ["fpga_GPIO28"]),
        Pin(32, "", ["fpga_GPIO29"]),
        Pin(33, "", ["fpga_GPIO30"]),
        Pin(34, "", ["fpga_GPIO31"]),
        Pin(35, "", ["fpga_GPIO32"]),
        Pin(36, "", ["fpga_GPIO33"]),
        Pin(37, "", ["GND"]),
        Pin(38, "", ["3V3"]),
        Pin(39, "", ["GND"]),
        Pin(40, "", ["5V"]),
    ],
)

fpga_gpio_top = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_2x08_P2.54mm_Vertical",
    identifier="FPGA_IO2",
    value="NF pins",
    desc="Pin header 0.1 inch 2x8",
    pins=[
        Pin( 1, "", ["GND"]),
        Pin( 2, "", ["3V3"]),
        Pin( 3, "", ["fpga_GPIO34"]),
        Pin( 4, "", ["fpga_GPIO35"]),
        Pin( 5, "", ["fpga_GPIO36"]),
        Pin( 6, "", ["fpga_GPIO37"]),
        Pin( 7, "", ["fpga_GPIO38"]),
        Pin( 8, "", ["fpga_GPIO39"]),
        Pin( 9, "", ["fpga_GPIO40"]),
        Pin(10, "", ["fpga_GPIO41"]),
        Pin(11, "", ["fpga_GPIO42"]),
        Pin(12, "", ["fpga_GPIO43"]),
        Pin(13, "", ["fpga_GPIO44"]),
        Pin(14, "", ["fpga_GPIO45"]),
        Pin(15, "", ["fpga_GPIO46"]),
        Pin(16, "", ["fpga_GPIO47"]),
    ],
)

# 74LCX buffer, powered by the 3V side.  This is here to provide some hot swap
# tolerance; its inputs and outputs go high impedance when it's unpowered, so
# the 3V side won't end up parasitically powered if the unit is connected to a
# powered target but not a USB port.

# An alternative here could have been to not draw power from the USB port, but
# it's nice to be able to have the unit accessible even when not attached to a
# target.

# The ordering code for 74LCX125 in SO-14 is a bit of a mystery.  Every
# datasheet seems to list different codes, but the one from the onsemi.com
# page lists -M as 0.15" wide SO-14, and -MX as the same except on tape/reel.

# I've also seen -D for SOIC and -DT for TSSOP, so that might be an option too.
hotswap_buf = [
    [
        myelin_kicad_pcb.Component(
            footprint="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm",
            identifier=ident,
            value="74LCX125M",
            jlc_part="C238953",  # Extended, min qty 2500 if they don't have it in stock
            # https://www.onsemi.com/products/standard-logic/buffers/74lcx125
            desc="IC buffer 4-bit OC hot swap",
            link="https://www.digikey.com/product-detail/en/on-semiconductor/74LCX125MX/74LCX125MXCT-ND/965496",
            pins=[
                Pin( 1, "1nOE", conn[0][0]),
                Pin( 2, "1A",   conn[0][1]),
                Pin( 3, "1Y",   conn[0][2]),
                Pin( 4, "2nOE", conn[1][0]),
                Pin( 5, "2A",   conn[1][1]),
                Pin( 6, "2Y",   conn[1][2]),
                Pin( 7, "GND",  "GND"),
                Pin( 8, "3Y",   conn[2][2]),
                Pin( 9, "3A",   conn[2][1]),
                Pin(10, "3nOE", conn[2][0]),
                Pin(11, "4Y",   conn[3][2]),
                Pin(12, "4A",   conn[3][1]),
                Pin(13, "4nOE", conn[3][0]),
                Pin(14, "VCC",  power),
            ],
        ),
        myelin_kicad_pcb.C0805("100n", "GND", power, ref="DC?"),
    ]
    for ident, power, conn in [
        (
            "HSBUF",
            "3V3",
            [
                # [nOE, input, output]
                ["hotswap_noe", "testack_noe",      "testack_noe_buf"],
                ["hotswap_noe", "target_testreq",   "testreq_3v"],
                ["hotswap_noe", "target_5V_r",      "target_power_3v"],
                ["hotswap_noe", "target_reset_noe", "target_reset_noe_buf"],
            ]
        )
    ]
]

# Isolator, from an earlier attempt at r2 which completely isolated the USB
# and target sides of the board, rather than just tying the grounds together
# with resistors.

# isolator = myelin_kicad_pcb.Component(
#     footprint="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm",
#     identifier="ISO",
#     value="SI8642EC-B-IS1",
#     desc="https://www.digikey.com/product-detail/en/silicon-labs/SI8642EC-B-IS1/336-2094-5-ND/2623342",
#     pins=[

#         # SI8642 buffers:
#         # A1 -> B1
#         # A2 -> B2
#         # B3 -> A3
#         # B4 -> A4

#         Pin( 1, "VDD1",  "target_5V"),
#         Pin( 2, "GND1",  "target_GND"),
#         Pin( 3, "A1in",  "target_GND"),
#         Pin( 4, "A2in",  "target_testreq_protected"),
#         Pin( 5, "A3out", "target_testack_noe"),
#         Pin( 6, "A4out", "target_reset_noe"),
#         Pin( 7, "EN1",   "target_5V"),
#         Pin( 8, "GND1",  "target_GND"),
#         Pin( 9, "GND2",  "GND"),
#         Pin(10, "EN2",   "3V3"),
#         Pin(11, "B4in",  "target_reset_noe_3V"),
#         Pin(12, "B3in",  "target_testack_noe_3V"),
#         Pin(13, "B2out", "target_testreq_3V"),
#         Pin(14, "B1out", "target_power_3V_n"),
#         Pin(15, "GND2",  "GND"),
#         Pin(16, "VDD2",  "3V3"),
#     ],
# )

# Not sure if I've gotten this right, but the 74LCX125's datasheet says that
# all /OE pins need to be pulled to VCC to preserve the high impedance on
# power off behavior.  This is driven low by the FPGA when it starts up.
hotswap_noe_pullup = myelin_kicad_pcb.R0805("10k", "hotswap_noe", "3V3", "R11")

# These resistors prevent the 5V side of things from being powered by the
# outputs from the 74LCX125.
testack_inter_buf_r = myelin_kicad_pcb.R0805("1k", "testack_noe_buf", "testack_noe_buf_r", ref="R7")
target_reset_inter_buf_r = myelin_kicad_pcb.R0805("1k", "target_reset_noe_buf", "target_reset_noe_buf_r", ref="R8")

# These resistors prevent the 74HCT125 on the 5V side from driving testack or
# reset when the 3V side is unpowered.  (They're connected to the outputs of
# the 74LCX125 buffer rather than the inputs to the 74HCT125 so we don't
# accidentally get a voltage divider.)
testack_noe_pullup = myelin_kicad_pcb.R0805("10k", "testack_noe_buf", "target_5V", "R9")
target_reset_pullup = myelin_kicad_pcb.R0805("10k", "target_reset_noe_buf", "target_5V", "R10")

# 75HCT125 buffer, powered by the 5V side
out_buf = [
    [
        myelin_kicad_pcb.Component(
            footprint="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm",
            identifier=ident,
            value="74HCT125D",
            jlc_part="C5962",
            desc="IC buffer 4-bit OC",
            link="https://www.digikey.com/product-detail/en/nexperia-usa-inc/74HCT125D-653/1727-2834-1-ND/763401",
            pins=[
                Pin( 1, "1nOE", conn[0][0]),
                Pin( 2, "1A",   conn[0][1]),
                Pin( 3, "1Y",   conn[0][2]),
                Pin( 4, "2nOE", conn[1][0]),
                Pin( 5, "2A",   conn[1][1]),
                Pin( 6, "2Y",   conn[1][2]),
                Pin( 7, "GND",  "target_GND"),
                Pin( 8, "3Y",   conn[2][2]),
                Pin( 9, "3A",   conn[2][1]),
                Pin(10, "3nOE", conn[2][0]),
                Pin(11, "4Y",   conn[3][2]),
                Pin(12, "4A",   conn[3][1]),
                Pin(13, "4nOE", conn[3][0]),
                Pin(14, "VCC",  power),
            ],
        ),
        myelin_kicad_pcb.C0805("100n", "target_GND", power, ref="DC?"),
    ]
    for ident, power, conn in [
        (
            "OUTBUF",
            "target_5V",
            [
                # [nOE, input, output]
                ["testack_noe_buf_r",      "target_5V",  "target_testack"],
                ["target_reset_noe_buf_r", "target_GND", "target_reset"],
                ["target_5V",              "target_GND", ""],
                ["target_5V",              "target_GND", ""],
            ]
        )
    ]
]

post_header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical",
    identifier="POST",
    value="pins",
    desc="Pin header 0.1 inch 1x6",
    pins=[
        Pin(1, "", "target_5V_ext"),
        Pin(2, "", "target_D0"),
        Pin(3, "", "target_testreq_ext"),
        Pin(4, "", "target_testack_ext"),
        Pin(5, "", "target_reset_ext"),
        Pin(6, "", "target_GND"),
    ],
)

test_header = myelin_kicad_pcb.Component(
    footprint="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical",
    identifier="TEST",
    value="NF pins",
    desc="Pin header 0.1 inch 1x6",
    pins=[
        Pin(1, "", "target_5V_ext"),
        Pin(2, "", "target_D0"),
        Pin(3, "", "target_testreq_ext"),
        Pin(4, "", "target_testack_ext"),
        Pin(5, "", "target_reset_ext"),
        Pin(6, "", "target_GND"),
    ],
)

# Fuses, from an earlier attempt at r2 which put fuses on target_5V and
# target_GND rather than a protection diode and some resistors.

# fuse_blow_diodes = [
#     myelin_kicad_pcb.Component(
#         footprint="Diode_SMD:D_SMA",
#         identifier="D3",  # to blow F2 on reverse connection
#         value="S1ATR",
#         desc="Diode Rectifier; https://www.digikey.com/products/en?keywords=1655-1502-1-ND",
#         pins=[
#             Pin(1, "1", "target_5V"),
#             Pin(2, "2", "target_GND_unfused"),
#         ],
#     ),
#     myelin_kicad_pcb.Component(
#         footprint="Diode_SMD:D_SMA",
#         identifier="D2",  # to blow F1 on reverse connection
#         value="S1ATR NF",
#         desc="Diode Rectifier; https://www.digikey.com/products/en?keywords=1655-1502-1-ND",
#         pins=[
#             Pin(1, "1", "target_5V_unfused"),
#             Pin(2, "2", "target_GND"),
#         ],
#     ),
# ]

target_5V_mosfet = myelin_kicad_pcb.Component(
    footprint="Package_TO_SOT_SMD:SOT-23",
    identifier="U2",
    desc="P-MOSFET",
    value="PMV65XP,215",
    jlc_part="C75561",
    pins=[
        Pin(1, "G", "target_GND"),
        Pin(2, "S", "target_5V"),
        Pin(3, "D", "target_5V_ext"),
    ],
)

# What is the footprint for an appropriate polyfuse here?
# target_5V_fuse = myelin_kicad_pcb.R0805("PTC", "target_5V_unfused", "target_5V_fused", ref="F2")
# target_GND_fuse = myelin_kicad_pcb.R0805("PTC", "target_GND_unfused", "target_GND", ref="F1")

# Pulldown on target_5V_ext so L4 doesn't light due to parasitic current through R7 and R8.
# Split into two to be extra careful about heat dissipation.
target_5V_ext_pulldowns = [
    myelin_kicad_pcb.R0805("1k", "target_5V_ext", "target_GND", ref="R24"),
    myelin_kicad_pcb.R0805("1k", "target_5V_ext", "target_GND", ref="R25"),
]

target_5V_protection = myelin_kicad_pcb.R0805("1k", "target_5V", "target_5V_r", ref="R14")  # for LCX input

target_D0_pullup = myelin_kicad_pcb.R0805("2k2", "target_D0", "target_5V", ref="R6")

# Weak pullup on testreq to prevent garbage when disconnected from a target
target_testreq_pullup = myelin_kicad_pcb.R0805("100k", "target_testreq", "target_5V", ref="R23")

# Protection resistors and diodes from req/ack/reset lines
target_testreq_protection = myelin_kicad_pcb.R0805("68R", "target_testreq_ext", "target_testreq", ref="R15")  # for LCX input
target_testack_protection = myelin_kicad_pcb.R0805("68R", "target_testack_ext", "target_testack", ref="R16")
target_reset_protection = myelin_kicad_pcb.R0805("68R", "target_reset_ext", "target_reset_prediode", ref="R17")
target_reset_diode = myelin_kicad_pcb.DSOD123("BAT54", "target_reset", "target_reset_prediode", ref="D2", jlc_part="C152458")  # prediode ->|- reset

# The following resistors are just shunted out, as 110R between the grounds
# turned out to cause random failures :(

# If the host machine happens to share a ground with the target and the test
# connector is plugged in backwards, the target's 5V rail will be connected to
# target_GND.  These resistors limit the current flowing in this case.

# 0805 resistors are typically rated at 0.1 W, i.e. 5^2/0.1 = 250 ohms is the lowest they can be.
# Three 330R in parallel is 110R, so 45 mA will flow in a short condition, which will be fine.
ground_connection = [
    myelin_kicad_pcb.R0805("NF 0R", "target_GND", "GND", ref="R18"),
    myelin_kicad_pcb.R0805("NF 0R", "target_GND", "GND", ref="R19"),
    myelin_kicad_pcb.R0805("0R", "target_GND", "GND", ref="R20"),
]

for n in range(50):
    single_staple = myelin_kicad_pcb.Component(
        footprint="myelin-kicad:via_single",
        identifier="staple_single%d" % (n+1),
        value="",
        pins=[Pin(1, "GND", ["GND"])],
    )


myelin_kicad_pcb.dump_netlist("%s.net" % PROJECT_NAME)
myelin_kicad_pcb.dump_bom("bill_of_materials.txt",
                          "readable_bill_of_materials.txt",
                          jlc_fn="%s_jlc_pcba_bom.csv" % PROJECT_NAME)