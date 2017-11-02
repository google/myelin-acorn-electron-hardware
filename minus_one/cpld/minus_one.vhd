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

entity minus_one is
    Port (
        -- can't use a std_logic_vector here because we're missing A7-4 :(
        A15 : in std_logic;
        A14 : in std_logic;
        A13 : in std_logic;
        A12 : in std_logic;
        A11 : in std_logic;
        A10 : in std_logic;
        A9 : in std_logic;
        A8 : in std_logic;
        A3 : in std_logic;
        A2 : in std_logic;
        A1 : in std_logic;
        A0 : in std_logic;

        D : in std_logic_vector(7 downto 0);

        nRST : in std_logic;
        PHI0 : in std_logic;
        RnW : in std_logic;

        cart0_nOE : out std_logic;
        cart2_nOE : out std_logic;
        cart4_nOE : out std_logic;

        cart_nOE2 : out std_logic;

        cart_ROMQA : out std_logic;

        cart_nINFC : out std_logic;
        cart_nINFD : out std_logic;

        cart_nROMSTB : out std_logic;

        GPIO1 : in std_logic;
        GPIO2 : in std_logic;
        GPIO3 : in std_logic
    );
end minus_one;

architecture Behavioural of minus_one is

    -- '1' when A = &8000-BFFF, i.e. sideways address space
    signal sideways_select : std_logic;

    -- high byte on the address bus
    signal A_high : std_logic_vector(7 downto 0);

    -- low nybble on the address bus
    signal A_low : std_logic_vector(3 downto 0);

    -- register: currently selected bank
    signal bank : std_logic_vector(3 downto 0) := "1101";

begin

    A_high <= A15 & A14 & A13 & A12 & A11 & A10 & A9 & A8;
    A_low <= A3 & A2 & A1 & A0;

    -- '1' when A = &8000-BFFF
    sideways_select <= '1' when (A15 & A14 = "10") else '0';

    -- nOE for all cartridges
    cart0_nOE <= '0' when sideways_select = '1' and (bank(3 downto 1) = "000") else '1';
    cart2_nOE <= '0' when sideways_select = '1' and (bank(3 downto 1) = "001") else '1';
    cart4_nOE <= '0' when sideways_select = '1' and (bank(3 downto 1) = "010") else '1';

    -- bank select within cartridge address space
    cart_ROMQA <= bank(0);

    -- nOE2 (shared by all cartridges)
    cart_nOE2 <= '0' when sideways_select = '1' and bank = "1101" else '1';

    -- '0' when A = FCxx
    cart_nINFC <= '0' when (A_high = x"FC") else '1';

    -- '0' when A = FDxx
    cart_nINFD <= '0' when (A_high = x"FD") else '1';

    -- nROMSTB is not implemented
    cart_nROMSTB <= '1';

    process (PHI0)
    begin
        if nRST = '0' then
            -- default to something that'll deactivate all cartridges
            bank <= "1010";
        elsif falling_edge(PHI0) then
            -- ROM bank is selected by writing "0000xxxx" to &FEx5
            if RnW = '0' and A_high = x"FE" and A_low = x"5" and D(7 downto 4) = "0000" then
                bank <= D(3 downto 0);
            end if;
        end if;
    end process;

end Behavioural;
