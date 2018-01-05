-- Copyright 2017 Google LLC
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

-- This assumes that the board only has an FX2 fitted, and not a Raspberry
-- Pi.  It also assumes that it's connected to an Electron, and the 16MHz
-- clock is present.  This will not work yet when plugged into a BBC Micro's
-- Tube interface, and has not yet been tested as a BBC Master cartridge.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity fx2_tube_cartridge_adapter is 
    Port (
        cpu_D : inout std_logic_vector(7 downto 0);

        cpu_A7 : in std_logic;
        cpu_A6 : in std_logic;
        cpu_A5 : in std_logic;
        cpu_A4 : in std_logic;
        cpu_A2 : in std_logic;
        cpu_A1 : in std_logic;
        cpu_A0 : in std_logic;

        cpu_RnW : in std_logic;
        cpu_CLK : in std_logic;

        elk_nINFC : in std_logic;
        elk_16MHz : in std_logic;
        bbc_nTUBE : inout std_logic;

        tube_A0 : out std_logic;
        tube_A1 : out std_logic;
        tube_A2 : out std_logic;

        tube_D : inout std_logic_vector(7 downto 0);

        tube_nRST : in std_logic; -- driven by a diode and resistor
        tube_nTUBE : out std_logic;
        tube_RnW : out std_logic;
        tube_CLK : out std_logic
    );
end fx2_tube_cartridge_adapter;

architecture Behavioural of fx2_tube_cartridge_adapter is

    -- '0' when A = &FCEx: Tube memory space
    signal nTUBE : std_logic;

    -- true when the Pi can drive the bus
    signal pi_may_drive_bus : boolean;

    -- Reconstructed clock
    signal out_CLK : std_logic;
    signal clean_CLK : std_logic := '0';
    signal clean_CLK_ignore : std_logic := '0';

    -- Flag to say we should wait to drive the bus until the next rising clock edge
    signal wait_for_pi_to_drop_bus : boolean := false;

    -- Small counter to check for presence of 16MHz clock on the cartridge port
    signal cart_detect_count : std_logic_vector(2 downto 0) := (others => '0');

    -- Indicates cartridge port being used, rather than tube interface
    signal cart_detect : std_logic;

begin

    -- tube /CE signal: A = &FCEx
    nTUBE <= '0' when cart_detect = '1' and elk_nINFC = '0' and cpu_A7 = '1' and cpu_A6 = '1' and cpu_A5 = '1' and cpu_A4 = '0' else
             '0' when cart_detect = '0' and bbc_nTUBE = '0' else
             '1';

    tube_nTUBE <= nTUBE;

    pi_may_drive_bus <= (nTUBE = '0' and cpu_RnW = '1');

    -- copy across other signals
    tube_RnW <= cpu_RnW;
    tube_CLK <= out_CLK;
    tube_A0 <= cpu_A0;
    tube_A1 <= cpu_A1;
    tube_A2 <= cpu_A2;

    -- For PiTubeDirect: data goes both ways
    -- See http://stardot.org.uk/forums/viewtopic.php?f=3&t=11325&p=189382#p189382
    tube_D <=
        -- Drop the bus when the Pi might be driving it
        "ZZZZZZZZ" when wait_for_pi_to_drop_bus or pi_may_drive_bus else
        -- Otherwise copy over the CPU bus for the FX2 to monitor
        cpu_D;
    cpu_D <=
        tube_D when pi_may_drive_bus and out_CLK = '1' else
        "ZZZZZZZZ";

    -- Track when PiTubeDirect might possibly be still driving the bus
    process (out_CLK)
    begin
        if rising_edge(out_CLK) then
            wait_for_pi_to_drop_bus <= pi_may_drive_bus;
        end if;
    end process;

    -- clean up cpu_CLK by ignoring falling edges for a while after a rising edge
    process (elk_16MHz)
    begin
        -- 16MHz clock has period 62.5 ns, so two clocks = 125 ns and three clocks = 187.5 ns
        -- Electron clock has min high time 250ns, and glitches for about 100ns sometimes.
        -- So our process should be to set clean_CLK high as soon as cpu_CLK goes high, and
        -- ignore any high-to-low transitions that happen in the next 16MHz clock cycle.

        if rising_edge(elk_16MHz) then
            if cart_detect = '0' then
                cart_detect_count <= cart_detect_count + 1;
            end if;
            if clean_CLK_ignore = '1' then
                clean_CLK_ignore <= '0';
            else
                if clean_CLK = '0' and cpu_CLK = '1' then
                    clean_CLK_ignore <= '1';
                end if;
                clean_CLK <= cpu_CLK;
            end if;
        end if;
    end process;

    cart_detect <= cart_detect_count(cart_detect_count'high);

    out_CLK <= clean_CLK when cart_detect = '1' else cpu_CLK; -- mux with cpu_CLK if elk_16MHz isn't present

end Behavioural;
