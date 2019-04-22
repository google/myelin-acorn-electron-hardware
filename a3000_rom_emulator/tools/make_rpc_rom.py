from arcflash.rombuild import *
from glob import glob

# Local paths on the author's machine
classics, = glob("../../../archimedes/classicroms*/")
rpcemu, = glob("../../../archimedes/rpcemu*/")

FlashImage(

    # Flip pairs of bytes to match the wiring in the Risc PC adapter PCB v1
    # https://github.com/google/myelin-acorn-electron-hardware/tree/master/a3000_rom_emulator/riscpc_adapter_pcb
    byte_order = "2301",

    # Skip the bootloader until it works on Risc PC
    skip_bootloader = True,

    # ROM images to include -- excluding the bootloader right onw
    roms=[

        ROM(
            tag="riscos402",
            name="RISC OS 4.02 (saved from my Risc PC)",
            files=[rpcemu+'riscos_402_from_riscpc,fe5'],
            size=_4M,
            cmos="riscos4xx",
            ),

        ROM(
            tag="riscos5xx",
            name="RISC OS 5.xx (open source)",
            files=[rpcemu+'iomd32_527,fe5'],
            size=_4M,
            cmos="riscos5xx",
            ),

        ROM(
            tag="riscos360",
            name="RISC OS 3.60 (3QD Classic ROMs)",
            files=[classics+'RiscPC_A7000/RO_360/ROM_360'],
            size=_4M,
            cmos="riscos360",
            ),

        ROM(
            tag="riscos371",
            name="RISC OS 3.71 (3QD Classic ROMs)",
            files=[classics+'RiscPC_A7000/RO_370/ROM_371'],
            size=_4M,
            cmos="riscos360",
            ),

    ]
)
