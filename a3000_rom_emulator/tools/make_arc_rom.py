from arcflash.rombuild import *
from glob import glob

# Local paths on the author's machine
classics, = glob("../../../archimedes/classicroms*/")
rpcemu, = glob("../../../archimedes/rpcemu*/")

FlashImage(
    roms=[
        
        # 1MB ROMs

        ROM(
            tag="arctest",
            name="Arc Test ROM",
            files=[classics+'../../a3000/Arc_Test_roms/combined.rom'],
            size=_1M,
            ),
        ROM(
            tag="arthur030",
            name="Arthur 0.30",
            files=[classics+'Arthur/Arthur_030'],  # works if I remove the 4MB RAM card
            size=_1M,
            cmos="arthur030",
            ),
        ROM(
            tag="arthur120",
            name="Arthur 1.20",
            files=[classics+'Arthur/Arthur_120'],  # doesn't work on my A3000 -- may be the bad version IanS mentioned
            size=_1M,
            cmos="arthur120",
            ),
        ROM(
            tag="4cornarthur120",
            name="4corn Arthur 1.20",
            files=[classics+'from_4corn/4corn_arthur_120'],  # suggestion from IanS -- works!
            size=_1M,
            cmos="arthur120",
        ),
        ROM(
            tag="riscos201",
            name="RISC OS 2.01",
            files=[classics+'RISC_OS_2/ROM_201'],
            size=_1M,
            cmos="riscos201",
        ),

        # 2MB ROMs

        ROM(
            tag="riscos311",
            name="RISC OS 3.11",
            files=[classics+'RISC_OS_3/ROM_311'],
            size=_2M,
            cmos="riscos311",
            ),

        ROM(
            tag="riscos319",
            name="RISC OS 3.19 (4corn)",
            files=[classics+'from_4corn/4corn_riscos_319'],  # suggestion from steve3000
            size=_2M,
            cmos="riscos319",
            ),

        # 4MB

        ROM(
            tag="riscos320",
            name="RISC OS 3.20 (in development)",
            files=[classics+'../arculator-src/hostfs/RO320/build/RO320,ffd'],
            size=_4M,
            cmos="riscos320",
            ),
    ],

    # Hack to make this work on an unmodified A310
    # bootloader_512k = True,
)
