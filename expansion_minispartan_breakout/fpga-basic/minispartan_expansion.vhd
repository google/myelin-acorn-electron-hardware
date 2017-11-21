-- Copyright 2017 Google Inc.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity minispartan_expansion is
    Port (
        -- miniSpartan LEDs
        MS_LEDS : out std_logic_vector(7 downto 0);

        -- miniSpartan serial port
        MS_SERIAL_TX : out std_logic := '1';
        MS_SERIAL_RTS : out std_logic := '1';
        MS_SERIAL_RX : in std_logic;
        MS_SERIAL_CTS : in std_logic;

        -- miniSpartan SD card
        MS_SD_MOSI : out std_logic := '1';
        MS_SD_MISO : in std_logic;
        MS_SD_SCK : out std_logic := '1';
        MS_SD_SS : out std_logic := '0';

        -- clock inputs from ULA
        elk_16MHZ : in std_logic; -- buffered 16MHZ from ULA
        elk_16MHZ_DIV13 : in std_logic; -- buffered 1.23 MHz from ULA
        elk_PHI0 : in std_logic; -- buffered PHI0 from ULA

        -- reset line from ULA
        elk_nRST : in std_logic; -- buffered nRST from ULA

        -- RDY: pulled up in the ULA
        elk_RDY : in std_logic; -- buffered RDY from elk
        nDEASSERT_RDY : out std_logic := '1'; -- drives RDY=0 if '0'

        -- nNMI: pulled up on the Elk motherboard
        elk_nNMI : in std_logic; -- buffered nNMI from elk
        nASSERT_nNMI : out std_logic := '1'; -- drives nNMI=0 if '0'

        -- nIRQ: pulled up on the Elk motherboard
        elk_nIRQ : in std_logic; -- buffered nIRQ from elk
        nASSERT_nIRQ : out std_logic := '1'; -- drives nIRQ=0 if '0'

        -- RnW: driven by the 6502
        elk_RnW : in std_logic; -- buffered RnW from elk
        RnW_out : out std_logic := '1'; -- RnW that we can drive
        RnW_nOE : out std_logic := '1'; -- fpga drives RnW if '0', high-Z if '1'

        -- bidirectional data bus
        elk_D : inout std_logic_vector(7 downto 0) := (others => 'Z');
        DATA_nOE : out std_logic := '1'; -- '0' to enable data buffer
        DATA_READ : out std_logic := '1'; -- elk->fpga if '1', fpga->elk if '0'

        -- address bus: driven by the 6502
        elk_A : in std_logic_vector(15 downto 0);
        A_DIR : out std_logic := '1' -- elk->fpga if '1', fpga->elk if '0'
    );
end minispartan_expansion;

architecture Behavioural of minispartan_expansion is

    -- '1' when elk_A is in sideways space
    signal SIDEWAYS : std_logic;

    -- '1' when elk_A = FCFx
    signal DEBUG : std_logic;
    signal debug_reg : std_logic_vector(7 downto 0);

    -- '1' when elk_A = FCB1 (Elk User Port for UPURS)
    signal EUP_SERIAL : std_logic;

    -- '1' when elk_A = FC71 (parallel port data reg)
    signal EPP_DATA : std_logic;

    -- '1' when elk_A = FC72 (parallel port status reg)
    signal EPP_STATUS : std_logic;

    -- currently selected memory bank, defaults to BASIC
    signal bank : std_logic_vector(3 downto 0) := x"A";

    -- '1' when we're selected
    signal driving_bus : std_logic;

    -- '1' when reading from the embedded ROM
    signal reading_rom_zero : std_logic;
    -- internal wiring for embedded ROM
    signal rom_zero_D : std_logic_vector(7 downto 0);

    -- '1' when reading from the embedded ROM
    signal reading_rom_upurs : std_logic;
    -- internal wiring for embedded ROM
    signal rom_upurs_D : std_logic_vector(7 downto 0);

    -- '1' when reading from the embedded ROM
    signal reading_rom_mmfs : std_logic;
    -- internal wiring for embedded ROM
    signal rom_mmfs_D : std_logic_vector(7 downto 0);

begin

    -- sideways address space
    SIDEWAYS <= '1' when elk_A(15 downto 14) = "10" else '0';

    -- debug register
    DEBUG <= '1' when elk_A(15 downto 4) = x"FCF" else '0';

    -- EUP serial and MMFS parallel
    EUP_SERIAL <= '1' when elk_A = x"FCB1" else '0';
    EPP_DATA <= '1' when elk_A = x"FC71" else '0';
    EPP_STATUS <= '1' when elk_A = x"FC72" else '0';

    -- '1' when reading from the embedded ROM
    reading_rom_zero <= '1' when SIDEWAYS = '1' and bank = x"0" else '0';
    reading_rom_upurs <= '1' when SIDEWAYS = '1' and bank = x"6" else '0';
    reading_rom_mmfs <= '1' when SIDEWAYS = '1' and bank = x"7" else '0';

    -- the actual embedded rom
    rom_zero : entity work.RomZero
    port map (
        CLK => elk_PHI0,
        A => elk_A(13 downto 0),
        D => rom_zero_D,
        CS => reading_rom_zero
    );
    rom_upurs : entity work.RomUPURS
    port map (
        CLK => elk_PHI0,
        A => elk_A(13 downto 0),
        D => rom_upurs_D,
        CS => reading_rom_upurs
    );
    rom_mmfs : entity work.RomMMFS
    port map (
        CLK => elk_PHI0,
        A => elk_A(13 downto 0),
        D => rom_mmfs_D,
        CS => reading_rom_mmfs
    );

    -- data bus access
    driving_bus <=
        -- never when cpu is writing
        '0' when elk_RnW = '0' else
        -- drive when reading embedded rom
        '1' when reading_rom_zero = '1' or reading_rom_upurs = '1' or reading_rom_mmfs = '1' else
        -- drive when reading registers
        '1' when DEBUG = '1' or EUP_SERIAL = '1' or EPP_STATUS = '1' else
        -- we're not selected
        '0';

    -- only drive buffers during high clock period and
    -- either the cpu is writing, or we're selected and
    -- the cpu is reading
    DATA_nOE <= '0' when (
        elk_PHI0 = '1' and (elk_RnW = '0' or driving_bus = '1')
        ) else '1';

    -- data direction matches elk_RnW
    DATA_READ <= '0' when elk_RnW = '1' else '1';

    -- data bus
    elk_D <=
        -- failsafe: tristate when the buffers are pointing elk->fpga
        "ZZZZZZZZ" when (elk_PHI0 = '0' or elk_RnW = '0' or driving_bus = '0') else
        -- reading data from the embedded ROM
        rom_zero_D when reading_rom_zero = '1' else
        rom_upurs_D when reading_rom_upurs = '1' else
        rom_mmfs_D when reading_rom_mmfs = '1' else
        -- reading debug register
        debug_reg when elk_A = x"FCF0" else
        elk_A(3 downto 0) & elk_A(3 downto 0) when DEBUG = '1' else
        -- reading SPI status
        MS_SD_MISO & "0000000" when EPP_STATUS = '1' else
        -- reading serial RX
        MS_SERIAL_RX & "11111" & MS_SERIAL_CTS & "1" when EUP_SERIAL = '1' else
        -- default: this should never happen
        "10101010";

    process (--elk_nRST,
    elk_PHI0)
    begin
        -- TODO figure out why nRST is going low.
        -- multimeter shows it at ~2.3V; is it shorted to PHI0?  PORTA5
        --if elk_nRST = '0' then
        --    -- default to BASIC ROM
        --    bank <= x"A";
        --    MS_LEDS <= x"55";
        --els
        if falling_edge(elk_PHI0) then
            -- set sideways bank
            if (
                elk_RnW = '0' and
                elk_A(15 downto 8) & elk_A(3 downto 0) = x"FE5" and
                elk_D(7 downto 4) = x"0"
            ) then
                bank <= elk_D(3 downto 0);
            end if;
            -- set serial output
            if elk_RnW = '0' and EUP_SERIAL = '1' then
                MS_SERIAL_RTS <= elk_D(6);
                MS_SERIAL_TX <= elk_D(0);
            end if;
            -- set SPI output
            if elk_RnW = '0' and EPP_DATA = '1' then
                MS_SD_MOSI <= elk_D(0);
                MS_SD_SCK <= elk_D(1);
            end if;
            -- set leds on minispartan board by writing to FCFx
            if elk_RnW = '0' and DEBUG = '1' then
                MS_LEDS <= elk_D;
                debug_reg <= elk_D;
            end if;
        end if;
    end process;

end Behavioural;
