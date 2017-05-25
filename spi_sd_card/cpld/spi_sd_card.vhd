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

entity spi_sd_card is 
    Port (
        elk_D : inout std_logic_vector(7 downto 0);

        elk_nINFC : in std_logic;
        elk_A7 : in std_logic;
        elk_A6 : in std_logic;
        elk_A5 : in std_logic;
        elk_A4 : in std_logic;
        elk_A2 : in std_logic;
        elk_A1 : in std_logic;
        elk_A0 : in std_logic;

        elk_nRST : in std_logic;
        elk_RnW : in std_logic;
        elk_PHI0 : in std_logic;

        tube_A0 : out std_logic;
        tube_A1 : out std_logic;
        tube_A2 : out std_logic;

        tube_D : inout std_logic_vector(7 downto 0);

        tube_nRST : out std_logic;
        tube_nTUBE : out std_logic;
        tube_RnW : out std_logic;
        tube_PHI0 : out std_logic
    );
end spi_sd_card;

architecture Behavioural of spi_sd_card is

    -- SPI signals
    signal MOSI : std_logic := '1';
    signal MISO : std_logic;
    signal SCK : std_logic := '1';
    signal nSS : std_logic := '0';

    signal A_lower : std_logic_vector(7 downto 0);

    ---- Memory mapped SPI registers ----

    -- chip selects
    signal nSPI : std_logic; -- '0' when A = &FCD0
    signal nSPI_STATUS : std_logic; -- '0' when A = &FCD1

    -- data register
    signal REG : std_logic_vector(7 downto 0) := x"00";

    -- transfer in progress when '1'
    signal transfer_in_progress : std_logic := '0';

    -- transfer bit counter
    signal bit_count : std_logic_vector(3 downto 0) := (others => '0');

    -- delay bit, to make everything slower
    signal delay : std_logic_vector(3 downto 0) := (others => '0');

    ---- Plus 1 workalike registers ----

    -- chip selects
    signal nDATA : std_logic; -- '0' when A = &FC71
    signal nSTATUS : std_logic; -- '0' when A = &FC72

begin

    -- mappings to actual pins
    tube_D(5) <= nSS;
    tube_D(6) <= MOSI;
    tube_D(7) <= SCK;
    MISO <= tube_D(0);

    -- address comparison convenience (note missing A3 in elk_pi_tube_direct r1)
    A_lower <= elk_A7 & elk_A6 & elk_A5 & elk_A4 & '0' & elk_A2 & elk_A1 & elk_A0;

    ---- Memory-mapped SPI ----

    nSPI <= '0' when (elk_nINFC = '0' and A_lower = x"D0") else '1';
    nSPI_STATUS <= '0' when (elk_nINFC = '0' and A_lower = x"D1") else '1';

    ---- Plus 1 parallel port emulation ----

    nDATA <= '0' when (elk_nINFC = '0' and A_lower = x"71") else '1';
    nSTATUS <= '0' when (elk_nINFC = '0' and A_lower = x"72") else '1';

    ---- Data bus ----

    elk_D <=
        -- Memory-mapped SPI
        x"4" & bit_count when (nSPI = '0' and elk_RnW = '1' and transfer_in_progress = '1') else
        REG when (nSPI = '0' and elk_RnW = '1') else
        "0000000" & transfer_in_progress when (nSPI_STATUS = '0' and elk_RnW = '1') else
        -- Plus 1 parallel port
        MISO & "0000000" when (nSTATUS = '0' and elk_RnW = '1') else
        -- default
        "ZZZZZZZZ";

    -- handle writes
    process (elk_PHI0)
    begin
        if falling_edge(elk_PHI0) then
            -- Memory-mapped and bit-banged SPI
            if transfer_in_progress = '1' then
                -- first priority: service any current SPI transfers
                if delay /= "0000" then
                    delay <= std_logic_vector(unsigned(delay) + 1);
                else
                    delay <= "0000"; -- 0000 for no delay, 1111 for 1 cycle, ..., 0001 for 15 cycles
                    if SCK = '1' then
                        -- change MOSI on falling edge
                        MOSI <= REG(7);
                        SCK <= '0';
                    else
                        -- read MISO on rising edge
                        SCK <= '1';
                        REG <= REG(6 downto 0) & MISO;
                        if bit_count = "0111" then
                            transfer_in_progress <= '0';
                        else
                            bit_count <= std_logic_vector(unsigned(bit_count) + 1);
                        end if;
                    end if;
                end if;
            elsif nSPI = '0' and elk_RnW = '0' then
                -- the Electron is writing to &FCD0 to start a transfer
                REG <= elk_D;
                transfer_in_progress <= '1';
                bit_count <= "0000";
                SCK <= '1';
            elsif nDATA = '0' and elk_RnW = '0' then
                -- handle write to &FC71
                MOSI <= elk_D(0);
                SCK <= elk_D(1);
            end if;
        end if;
    end process;

end Behavioural;
