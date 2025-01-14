#!/usr/bin/env python3

# Copyright 2025 Google Inc.
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


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge

def tick():
    return Timer(1, units="ns")


async def spi_send_byte(dut, b):
    r = 0
    for _ in range(8):
        dut.cpld_MOSI.value = (b & 0x80) >> 7
        await tick()
        dut.cpld_SCK.value = 1
        await tick()
        dut.cpld_SCK.value = 0
        r = (r << 1) | dut.cpld_MISO.value
    return r


async def spi_send(dut, spi_bytes):
    await tick()
    dut.cpld_SS.value = 0
    dut.cpld_SCK.value = 0
    await tick()
    ret = []
    expected_bits = 0
    for b in spi_bytes:
        ret.append(await spi_send_byte(dut, b))
        expected_bits += 8
        assert dut.spi_bit_count == expected_bits
    dut.cpld_SS.value = 1
    await tick()

    return ret


def init(dut):
    dut.rom_5V.value = 1
    dut.rom_nCS.value = 0
    dut.rom_nOE.value = 0


@cocotb.test()
async def disable_arm_access(dut):
    """Pass initial 0 to SPI, to disable ARM access."""

    init(dut)

    spi_resp = await spi_send(dut, [0x7F, 0xFF, 0xFF, 0xFF])
    dut._log.info("spi response: %s", spi_resp)
    dut._log.info("allowing_arm_access: %s", dut.allowing_arm_access.value)
    dut._log.info(
        "flash nCE %s nOE %s nWE %s",
        dut.flash_nCE.value,
        dut.flash_nOE.value,
        dut.flash_nWE.value,
    )
    assert dut.allowing_arm_access.value == 0
    assert dut.flash_nCE.value == 1
    assert dut.flash_nOE.value == 1
    assert dut.flash_nWE.value == 1


@cocotb.test()
async def enable_arm_access(dut):
    """Pass initial 1 to SPI, to enable ARM access."""

    init(dut)

    spi_resp = await spi_send(dut, [0xFF, 0xFF, 0xFF, 0xFF])
    dut._log.info("spi response: %s", spi_resp)
    dut._log.info("allowing_arm_access: %s", dut.allowing_arm_access.value)
    dut._log.info(
        "flash nCE %s nOE %s nWE %s",
        dut.flash_nCE.value,
        dut.flash_nOE.value,
        dut.flash_nWE.value,
    )
    assert dut.allowing_arm_access.value == 1
    assert dut.flash_nCE.value == 0
    assert dut.flash_nOE.value == 0
    assert dut.flash_nWE.value == 1
