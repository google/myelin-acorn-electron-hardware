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

    -- Memory mapped SPI registers (TODO)

    -- our own chip select: Elk is reading/writing &FCD0
    --signal nSPI : std_logic; -- '0' when A = &FCD0

    -- our data register
    --signal REG : std_logic_vector(7 downto 0) := x"00";

    -- transfer in progress when '1'
    --signal transfer_in_progress : std_logic := '0';

    -- transfer bit counter
    --signal bit_count : std_logic_vector(3 downto 0) := (others => '0');

    -- Simple version to work with MMFS ElkPlus1 interface

    -- '0' when the Elk is accessing parallel port registers
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

    -- Memory-mapped SPI version (TODO)

    -- /CE signal: A = &FCD0 (or FCD8 because we don't have A3, but this will get fixed in future hardware)
    --nSPI <= '0' when (elk_nINFC = '0' and A_lower = x"D0") else '1';

    -- allow the electron to read our buffer
    --elk_D <=
    --    REG when (nSPI = '0' and elk_RnW = '1') else
    --    "ZZZZZZZZ";

    -- Simple version to work with MMFS ElkPlus1 interface

    nDATA <= '0' when (elk_nINFC = '0' and A_lower = x"71") else '1';
    nSTATUS <= '0' when (elk_nINFC = '0' and A_lower = x"72") else '1';

    -- read status register at &FC72
    elk_D <=
        MISO & "0000000" when (nSTATUS = '0' and elk_RnW = '1') else
        "ZZZZZZZZ";

    -- handle writes
    process (elk_PHI0)
    begin
        if falling_edge(elk_PHI0) then
            -- handle writes to &FC71
            if nDATA = '0' and elk_RnW = '0' then
                MOSI <= elk_D(0);
                SCK <= elk_D(1);
            end if;
        end if;
    end process;

end Behavioural;
