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

entity elk_pi_tube_direct is 
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
end elk_pi_tube_direct;

architecture Behavioural of elk_pi_tube_direct is

    -- '0' when A = &FCEx: Tube memory space
    signal nTUBE : std_logic;

    -- '0' when A = &FCFx, for debugging
    signal nDEBUG : std_logic;

    -- Debug counter that is incremented any time the Electron writes to &FCFx
    signal counter : std_logic_vector(4 downto 0) := "00000";

begin

    -- tube /CE signal: A = &FCEx
    nTUBE <= '0' when (elk_nINFC = '0' and elk_A7 = '1' and elk_A6 = '1' and elk_A5 = '1' and elk_A4 = '0') else '1';
    tube_nTUBE <= nTUBE;

    -- debug /CE signal: A = &FCFx
    nDEBUG <= '0' when (elk_nINFC = '0' and elk_A7 = '1' and elk_A6 = '1' and elk_A5 = '1' and elk_A4 = '1') else '1';
    
    -- copy across other signals
    tube_nRST <= elk_nRST;
    tube_RnW <= elk_RnW;
    tube_PHI0 <= elk_PHI0;
    tube_A0 <= elk_A0;
    tube_A1 <= elk_A1;
    tube_A2 <= elk_A2;

    -- data goes both ways
    tube_D <=
        elk_D when (nTUBE = '0' and elk_RnW = '0') else
        "ZZZZZZZZ";
    elk_D <=
        tube_D when (nTUBE = '0' and elk_RnW = '1') else
        counter(3 downto 0) & '0' & elk_A2 & elk_A1 & elk_A0 when (nDEBUG = '0' and elk_RnW = '1') else
        "ZZZZZZZZ";

    -- increment debug counter
    process (elk_PHI0)
    begin
        if falling_edge(elk_PHI0) then
            if nDEBUG = '0' and elk_RnW = '0' then
                -- writing one of the debug registers
                counter <= std_logic_vector(unsigned(counter) + 1);
            end if;
        end if;
    end process;

end Behavioural;
