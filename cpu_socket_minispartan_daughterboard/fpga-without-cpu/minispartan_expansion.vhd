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

        -- connections to the cpu_socket_expansion board
        ext_A : in std_logic_vector(15 downto 0);
        ext_D : inout std_logic_vector(7 downto 0);

        ext_GP0 : in std_logic; -- PHI2
        ext_GP1 : out std_logic := '1'; -- n_global_enable
        ext_GP2 : in std_logic; -- 16MHz
        ext_GP3 : out std_logic := '1'; -- dbuf_nOE
        ext_GP4 : out std_logic := '1'; -- n_accessing_shadow_ram
        ext_GP5 : in std_logic := '1'; -- n_cpu_is_external
        ext_GP6 : in std_logic; -- RnW
        ext_GP7 : in std_logic; -- nRESET
        ext_GP8 : in std_logic; -- READY
        ext_GP9 : in std_logic; -- /NMI
        ext_GP10 : in std_logic; -- /IRQ
        ext_GP11 : out std_logic := '1'; -- dbuf_driven_by_cpu
        ext_GP12 : in std_logic;

        -- connections to the Raspberry Pi
        tube_PHI0 : out std_logic := '1';
        tube_D : inout std_logic_vector(7 downto 0);
        tube_A : out std_logic_vector(2 downto 0);
        tube_RnW : out std_logic := '1';
        tube_nTUBE : out std_logic := '1';
        tube_nRST : out std_logic := '1'

        --TODO figure out directions here
        --pi_serial_RX : in std_logic;
        --pi_serial_TX : in std_logic;

    );
end minispartan_expansion;

architecture Behavioural of minispartan_expansion is

    -- '1' when ext_A is in sideways space
    signal SIDEWAYS : std_logic;

    -- '1' when ext_A = FCFx
    signal DEBUG : std_logic;
    signal debug_reg : std_logic_vector(7 downto 0);

    -- '1' when ext_A = FCB1 (Elk User Port for UPURS)
    signal EUP_SERIAL : std_logic;

    -- '1' when ext_A = FC71 (parallel port data reg)
    signal EPP_DATA : std_logic;

    -- '1' when ext_A = FC72 (parallel port status reg)
    signal EPP_STATUS : std_logic;

    -- '1' when tube addresses are being accessed
    signal tube_access : std_logic;

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

    signal elk_PHI0 : std_logic;
    signal n_global_enable : std_logic := '1';
    signal DATA_nOE : std_logic := '1';
    signal n_accessing_shadow_ram : std_logic := '1';
    signal n_cpu_is_external : std_logic := '1';
    signal elk_RnW : std_logic;
    signal elk_nRST : std_logic;

begin

    -- global settings
    n_global_enable <= '0';
    n_accessing_shadow_ram <= '1';
    n_cpu_is_external <= '1';

    -- translate ext_GP* to convenience names
    elk_PHI0 <= ext_GP0;
    ext_GP1 <= n_global_enable;
    --clk_16MHz <= ext_GP2;
    ext_GP3 <= DATA_nOE;
    ext_GP4 <= n_accessing_shadow_ram;
    ext_GP4 <= n_cpu_is_external;
    elk_RnW <= ext_GP6;
    elk_nRST <= ext_GP7;
    --elk_READY <= ext_GP8;
    --elk_nNMI <= ext_GP9;
    --elk_nIRQ <= ext_GP10;
    ext_GP11 <= not driving_bus; -- '0' to buffer from us to CPU

    -- sideways address space
    SIDEWAYS <= '1' when ext_A(15 downto 14) = "10" else '0';

    -- debug register
    DEBUG <= '1' when ext_A(15 downto 4) = x"FCF" else '0';

    -- EUP serial and MMFS parallel
    EUP_SERIAL <= '1' when ext_A = x"FCB1" else '0';
    EPP_DATA <= '1' when ext_A = x"FC71" else '0';
    EPP_STATUS <= '1' when ext_A = x"FC72" else '0';

    -- Tube (&FCEx)
    tube_access <= '1' when ext_A(15 downto 4) = x"FCE" else '0';
    tube_D <= ext_D when elk_RnW = '0' else "ZZZZZZZZ";
    tube_A <= ext_A(2 downto 0);
    tube_PHI0 <= elk_PHI0;
    tube_RnW <= elk_RnW;
    tube_nTUBE <= not tube_access;
    tube_nRST <= elk_nRST;

    -- '1' when reading from the embedded ROM
    reading_rom_zero <= '0'; --'1' when SIDEWAYS = '1' and bank = x"0" else '0';
    reading_rom_upurs <= '1' when SIDEWAYS = '1' and bank = x"6" else '0';
    reading_rom_mmfs <= '1' when SIDEWAYS = '1' and bank = x"7" else '0';

    -- the actual embedded rom
    rom_zero : entity work.RomZero
    port map (
        CLK => elk_PHI0,
        A => ext_A(13 downto 0),
        D => rom_zero_D,
        CS => reading_rom_zero
    );
    rom_upurs : entity work.RomUPURS
    port map (
        CLK => elk_PHI0,
        A => ext_A(13 downto 0),
        D => rom_upurs_D,
        CS => reading_rom_upurs
    );
    rom_mmfs : entity work.RomMMFS
    port map (
        CLK => elk_PHI0,
        A => ext_A(13 downto 0),
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
        '1' when DEBUG = '1' or EUP_SERIAL = '1' or EPP_STATUS = '1' or tube_access = '1' else
        -- we're not selected
        '0';

    -- only drive buffers during high clock period and
    -- either the cpu is writing, or we're selected and
    -- the cpu is reading
    DATA_nOE <= '0' when (
        elk_PHI0 = '1' and (elk_RnW = '0' or driving_bus = '1')
        ) else '1';

    -- data bus
    ext_D <=
        -- failsafe: tristate when the buffers are pointing elk->fpga
        "ZZZZZZZZ" when (elk_PHI0 = '0' or elk_RnW = '0' or driving_bus = '0') else
        -- reading from tube
        tube_D when tube_access = '1' else
        -- reading data from the embedded ROM
        rom_zero_D when reading_rom_zero = '1' else
        rom_upurs_D when reading_rom_upurs = '1' else
        rom_mmfs_D when reading_rom_mmfs = '1' else
        -- reading debug register
        debug_reg when ext_A = x"FCF0" else
        ext_A(3 downto 0) & ext_A(3 downto 0) when DEBUG = '1' else
        -- reading SPI status
        MS_SD_MISO & "0000000" when EPP_STATUS = '1' else
        -- reading serial RX
        MS_SERIAL_RX & "11111" & MS_SERIAL_CTS & "1" when EUP_SERIAL = '1' else
        -- default: this should never happen
        "10101010";

    -- Micro SD port debugging
    MS_LEDS(2) <= MS_SD_MISO;

    process (elk_nRST, elk_PHI0)
    begin
        if elk_nRST = '0' then
            -- default to BASIC ROM
            bank <= x"A";
            MS_LEDS(7 downto 3) <= "10101";
            MS_LEDS(1 downto 0) <= "00";
        elsif falling_edge(elk_PHI0) then
            -- set sideways bank
            if (
                elk_RnW = '0' and
                ext_A(15 downto 8) & ext_A(3 downto 0) = x"FE5" and
                ext_D(7 downto 4) = x"0"
            ) then
                bank <= ext_D(3 downto 0);
            end if;
            -- set serial output
            if elk_RnW = '0' and EUP_SERIAL = '1' then
                MS_SERIAL_RTS <= ext_D(6);
                MS_SERIAL_TX <= ext_D(0);
            end if;
            -- set SPI output
            if elk_RnW = '0' and EPP_DATA = '1' then
                MS_SD_MOSI <= ext_D(0);
                MS_SD_SCK <= ext_D(1);
                MS_LEDS(1 downto 0) <= ext_D(1 downto 0);
            end if;
            -- set leds on minispartan board by writing to FCFx
            if elk_RnW = '0' and DEBUG = '1' then
                MS_LEDS(7 downto 3) <= ext_D(7 downto 3);
                debug_reg <= ext_D;
            end if;
        end if;
    end process;

end Behavioural;
