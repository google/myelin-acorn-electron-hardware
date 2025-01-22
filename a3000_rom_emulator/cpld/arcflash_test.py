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
from cocotb.handle import Force, Release
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge


def tick():
    return Timer(1, units="ns")


def fmt_byte_array(data):
    return " ".join("%02X" % c for c in data)


async def spi_send_byte(dut, b):
    r = 0
    for _ in range(8):
        dut.cpld_MOSI.value = (b & 0x80) >> 7
        await tick()
        dut.cpld_SCK.value = 1
        await tick()
        dut.cpld_SCK.value = 0
        # dut._log.info(
        #     "spi; cpld_MISO=%s enable_bitbang_serial=%s cpld_SS+%s cpld_MISO_TXD=%s cpld_MISO_int=%s",
        #     dut.cpld_MISO.value,
        #     dut.enable_bitbang_serial,
        #     dut.cpld_SS.value,
        #     dut.cpld_MISO_TXD.value,
        #     dut.cpld_MISO_int.value,
        # )
        r = (r << 1) | dut.cpld_MISO.value
        b = (b << 1) & 0xFF
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
        expected_bits = (expected_bits + 8) % 64
        assert (
            dut.spi_bit_count == expected_bits
        ), "spi_bit_count is %d but expected %d" % (dut.spi_bit_count, expected_bits)
    dut.cpld_SS.value = 1
    await tick()

    dut._log.info(
        "spi transaction: sent %s received %s",
        fmt_byte_array(spi_bytes),
        fmt_byte_array(ret),
    )
    return ret


async def spi_flash_write(dut, addr, data):
    resp = await spi_send(
        dut,
        [
            # 0, RnW, 22 address bits, 40 zeroes.
            (addr & 0x3F0000) >> 16,
            (addr & 0xFF00) >> 8,
            addr & 0xFF,
            (data & 0xFF000000) >> 24,
            (data & 0xFF0000) >> 16,
            (data & 0xFF00) >> 8,
            data & 0xFF,
            0,
        ],
    )


async def spi_flash_read(dut, addr):
    resp = await spi_send(
        dut,
        [
            # 0, RnW, 22 address bits, 40 zeroes.
            ((addr & 0x3F0000) >> 16) | 0x40,
            (addr & 0xFF00) >> 8,
            addr & 0xFF,
            0,
            0,
            0,
            0,
            0,
        ],
    )
    return (resp[-4] << 24) | (resp[-3] << 16) | (resp[-2] << 8) | resp[-1]


def init(dut):
    dut.rom_5V.value = 1
    dut.rom_nCS.value = 0
    dut.flash0_DQ = Release()
    dut.flash1_DQ = Release()
    dut.rom_nOE.value = 0
    dut.cpld_MISO_int.value = 1
    dut.cpld_MISO_TXD.value = 0
    dut.spi_A = 0
    dut.spi_D = 0
    dut.spi_bit_count.value = 0


@cocotb.test()
async def disable_arm_access(dut):
    """Pass initial 0 to SPI, to disable ARM access."""

    init(dut)

    spi_resp = await spi_send(dut, [0x7F, 0xFF, 0xFF, 0xFF])
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


@cocotb.test()
async def read_from_flash(dut):
    """Read a word from flash."""

    init(dut)

    # Read command: 0, 0, 22 address bits, 40 zeroes.
    # Data is in the last four bytes of the SPI response.
    test_word = 0x12345678
    dut.flash1_DQ.value = Force((test_word >> 16) & 0xFFFF)
    dut.flash0_DQ.value = Force(test_word & 0xFFFF)
    read_resp = await spi_flash_read(dut, 0x3BCDEF)
    dut._log.info(
        "Word read: %08X; flash_DQ %X %X",
        read_resp,
        dut.flash1_DQ.value,
        dut.flash0_DQ.value,
    )
    assert (
        dut.allowing_arm_access.value == 0
    ), "Flash read should leave ARM access disabled"
    assert (
        read_resp == test_word
    ), "Flash read returned incorrect data: %08X instead of %08X" % (
        read_resp,
        test_word,
    )
