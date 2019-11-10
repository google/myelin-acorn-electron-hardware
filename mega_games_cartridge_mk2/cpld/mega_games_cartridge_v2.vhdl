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

entity MGC is
    port (
        nRESET : in std_logic;
        nPGFC : in std_logic;
        A : in std_logic_vector(7 downto 0);
        D : inout std_logic_vector(7 downto 0)
    );
end;

architecture rtl of MGC is

    signal nRESET_sync : std_logic;

    signal lower_rom_ram_visible : std_logic := '0';
    signal upper_rom_ram_visible : std_logic := '0';

    signal lower_rom_locked : std_logic := '0';
    signal upper_rom_locked : std_logic := '0';

    signal inhibit_reset : std_logic := '0';

    signal spi_shift_register : std_logic_vector(7 downto 0) := (others => '0');

    signal RnW : std_logic;

    -- Derive RnW signal
    RnW <= ERnWMCS when nMASDET = '1' else MRnW;

    -- Handle reads from registers
    D <=
        -- Never drive the bus for CPU writes
        x"Z" when RnW = '0'
        -- Read machine type
        else "0000000" & nMASDET when A = x"FCD2"
        -- Read shift register
        else spi_shift_register when A = x"FCD4"
        -- Catchall
        else x"Z";

    elk_clock_process : process(PHI0)
    begin
        if falling_edge(PHI0) then
            -- Synchronize external reset
            nRESET_sync <= nRESET;

            -- Handle writes to registers
            if RnW == '0' then
                if nPGFC = '0' && A == x"D0" then
                    lower_rom_ram_visible <= '1';
                    upper_rom_ram_visible <= '0';
                end if;
                if nPGFC = '0' && A == x"D1" then
                    upper_rom_ram_visible <= '1';
                    lower_rom_ram_visible <= '0';
                end if;
                if nPGFC = '0' && A == x"D3" then
                    inhibit_reset <= '1';
                end if;
                if nPGFC = '0' && A == x"D4" then
                    spi_shift_register <= D;
                    -- TODO trigger SPI transfer
                end if;
                if nPGFC = '0' && A == x"D5" then
                    -- TODO is this necessary?  writing to FCD4 is probably enough.
                end if;
                if nPGFC = '0' && A == x"D8" then
                    spi_nCS <= D(0);
                end if;
                if nPGFC = '0' && A == x"D9" then
                    -- TODO force SPI clock (SPI init?)
                end if;
                if nPGFC = '0' && A == x"DA" then
                    spi_MOSI <= D(0);  -- TODO is this needed?
                end if;
                if nPGFC = '0' && A == x"DC" then
                    lower_rom_locked <= '0';
                end if;
                if nPGFC = '0' && A == x"DD" then
                    lower_rom_locked <= '1';
                end if;
                if nPGFC = '0' && A == x"DE" then
                    upper_rom_locked <= '0';
                end if;
                if nPGFC = '0' && A == x"DF" then
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

end rtl;
