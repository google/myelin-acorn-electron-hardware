-- Copyright 2019 Google LLC
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

entity MGC is
    port (
        PHI : in std_logic;
        CLK16MHz : in std_logic;
        nRESET : in std_logic;
        nPGFC : in std_logic;
        ERnWMCS : in std_logic;
        MRnW : in std_logic;
        nMASDET : in std_logic;
        A : in std_logic_vector(7 downto 0);
        D : inout std_logic_vector(7 downto 0);

        spi_nCS : out std_logic := '1';
        spi_SCK : out std_logic := '0';
        spi_MOSI : out std_logic := '1';
        spi_MISO : in std_logic
    );
end;

architecture rtl of MGC is

    signal nRESET_sync : std_logic;

    signal lower_rom_ram_visible : std_logic := '0';
    signal upper_rom_ram_visible : std_logic := '0';

    signal lower_rom_locked : std_logic := '0';
    signal upper_rom_locked : std_logic := '0';

    signal inhibit_reset : std_logic := '0';

    signal spi_shift_register_load : std_logic_vector(7 downto 0) := (others => '0');
    signal spi_shift_register_16 : std_logic_vector(7 downto 0) := (others => '0');
    signal spi_start : std_logic := '0';
    signal spi_start_16 : std_logic := '0';
    signal last_spi_start_16 : std_logic := '0';
    signal spi_counter_16 : std_logic_vector(3 downto 0) := (others => '1');
    signal spi_bit_bang_mode : std_logic := '1';
    signal spi_bit_bang_MOSI : std_logic := '1';
    signal spi_bit_bang_SCK : std_logic := '0';

    signal spi_fast_SCK : std_logic := '0';
    signal spi_fast_MOSI : std_logic := '0';

    signal RnW : std_logic;

begin

    -- Derive RnW signal
    RnW <= ERnWMCS when nMASDET = '1' else MRnW;

    -- Handle reads from registers
    D <=
        -- Never drive the bus for CPU writes
        "ZZZZZZZZ" when RnW = '0'
        -- Read machine type
        else "0000000" & nMASDET when A = x"FCD2"
        -- Read shift register
        else spi_shift_register_16 when A = x"FCD4"
        -- Catchall
        else "ZZZZZZZZ";

    -- Multiplex fast and bitbang SPI
    spi_SCK <= spi_bit_bang_SCK when spi_bit_bang_mode = '1' else spi_fast_SCK;
    spi_MOSI <= spi_bit_bang_MOSI when spi_bit_bang_mode = '1' else spi_fast_MOSI;

    -- CPU clock process
    elk_clock_process : process(PHI)
    begin
        if falling_edge(PHI) then
            -- Synchronize external reset
            nRESET_sync <= nRESET;

            -- Reset all one pulse outputs
            spi_start <= '0';

            -- Handle writes to registers
            if RnW = '0' then
                if nPGFC = '0' and A = x"D0" then
                    lower_rom_ram_visible <= '1';
                    upper_rom_ram_visible <= '0';
                end if;
                if nPGFC = '0' and A = x"D1" then
                    upper_rom_ram_visible <= '1';
                    lower_rom_ram_visible <= '0';
                end if;
                if nPGFC = '0' and A = x"D3" then
                    inhibit_reset <= '1';
                end if;
                if nPGFC = '0' and A = x"D4" then
                    -- Copy D into load register and trigger SPI
                    spi_shift_register_load <= D;
                    spi_start <= '1';
                    spi_bit_bang_mode <= '0';
                end if;
                if nPGFC = '0' and A = x"D8" then
                    -- TODO figure out the best bits to use for MMFS
                    spi_nCS <= D(0);
                    --spi_bit_bang_mode <= D(1);
                    --spi_bit_bang_MOSI <= D(2);
                    --spi_bit_bang_SCK <= D(3);
                end if;
                if nPGFC = '0' and A = x"D9" then
                    spi_bit_bang_SCK <= D(0);  -- TODO consolidate with FCD8
                    spi_bit_bang_mode <= '1';
                end if;
                if nPGFC = '0' and A = x"DA" then
                    spi_bit_bang_MOSI <= D(0);  -- TODO consolidate with FCD8
                    spi_bit_bang_mode <= '1';
                end if;
                if nPGFC = '0' and A = x"DC" then
                    lower_rom_locked <= '0';
                end if;
                if nPGFC = '0' and A = x"DD" then
                    lower_rom_locked <= '1';
                end if;
                if nPGFC = '0' and A = x"DE" then
                    upper_rom_locked <= '0';
                end if;
                if nPGFC = '0' and A = x"DF" then
                    upper_rom_locked <= '1';
                end if;
            end if;
            if nRESET_sync = '0' then
                inhibit_reset <= '0';
                lower_rom_ram_visible <= '1';
                upper_rom_ram_visible <= '1';
                lower_rom_locked <= '1';
                upper_rom_locked <= '1';
            end if;
        end if;
    end process;

    -- High speed (16MHz on Electron, 8MHz on Master) clock process
    fast_clock_process : process(CLK16MHZ)
    begin
        if rising_edge(CLK16MHZ) then

            -- Synchronize spi_start
            last_spi_start_16 <= spi_start_16;
            spi_start_16 <= spi_start;

            if spi_start_16 = '1' and last_spi_start_16 = '0' then
                -- start spi transaction
                spi_counter_16 <= "0000";
                -- initialize MOSI with the MSB right now, and update it on the falling
                -- edge of spi_fast_SCK.
                spi_fast_MOSI <= spi_shift_register_load(7);
                spi_shift_register_16 <= spi_shift_register_load;
            end if;

            if spi_counter_16(3) = '0' then
                -- spi active!
                if spi_fast_SCK = '0' then
                    spi_fast_SCK <= '1';
                    spi_shift_register_16 <= spi_shift_register_16(6 downto 0) & spi_MISO;
                else
                    spi_fast_SCK <= '0';
                    spi_fast_MOSI <= spi_shift_register_16(7);
                end if;
                spi_counter_16 <= std_logic_vector(unsigned(spi_counter_16) + 1);
            end if;
        end if;
    end process;

end rtl;
