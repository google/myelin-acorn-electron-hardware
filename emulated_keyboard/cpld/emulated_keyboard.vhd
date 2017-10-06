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

-- This is part of a converter project that allows using a PS/2 keyboard on a BBC Master.
-- It's inspired by a similar project by Prime on the Stardot forums, which uses an MT8816
-- crosspoint switch to provide a *very* hardware-accurate emulation.  This project uses
-- a CPLD instead, with knowledge of how the keyboard encoder IC on the Master works, to
-- implement it with hardware I already happen to have at home :)

-- It shouldn't be too hard to adapt this to provide a keyboard interface for an Electron,
-- which connects the keyboard directly to the address bus, connects BREAK to /RST, and
-- has four ULA inputs for the keyboard rows, plus one for CAPS LOCK.

-- The BBC Micro works slightly differently, including the keyboard encoder logic
-- on the keyboard PCB itself, so that would require some more changes.

entity emulated_keyboard is 
    Port (
        -- nKBEN: '0' means col_idx is the column being polled, '1' means free running mode
        nkben : in std_logic;
        -- column index, taken straight from PL7
        col_idx : in std_logic_vector(3 downto 0);
        -- column inputs from keyboard encoder IC
        -- On the encoder, these are open collector outputs, so they
        -- need pullups, or the CPLD will see random input.
        --col_input : in std_logic_vector(12 downto 0);
        -- row outputs to keyboard encoder IC; these are pulled up to
        -- 5V on the BBC Master motherboard
        row_output : inout std_logic_vector(7 downto 0);
        -- BREAK output to system /RESET (pulled up to 5V).
        break_output : inout std_logic;

        -- SPI pins to talk to whatever's giving us keyboard information
        spi_clk : in std_logic;
        spi_mosi : in std_logic;
        spi_sel : in std_logic;
        spi_miso : out std_logic := '0'
    );
end emulated_keyboard;

architecture Behavioural of emulated_keyboard is

    -- SPI buffer
    signal spi_buf : std_logic_vector(17 downto 0) := (others => '0');
    -- SPI bit counter
    signal spi_count : std_logic_vector(4 downto 0) := (others => '0');

    -- value to match on the column inputs
    signal col_match_1 : std_logic_vector(3 downto 0) := "0011";
    signal col_match_2 : std_logic_vector(3 downto 0) := (others => '1');
    -- value to output on row outputs when a match occurs
    signal row_value_1 : std_logic_vector(2 downto 0) := "100";
    signal row_value_2 : std_logic_vector(2 downto 0) := (others => '1');
    -- '1' when SHIFT is pressed
    signal shift_pressed : std_logic := '0';
    -- '1' when CTRL is pressed
    signal ctrl_pressed : std_logic := '0';
    -- '1' when BREAK is pressed
    signal break_pressed : std_logic := '0';

    -- '1' when the column input matches col_match_1 or col_match_2, respectively
    signal match_1 : std_logic;
    signal match_2 : std_logic;

    -- '1' when at least one key is pressed
    signal have_keypress : std_logic;

    -- index of currently strobed column
    --signal col_idx : std_logic_vector(3 downto 0);

begin

    -- set col_idx to the index of the column currently pulled low by the keyboard encoder, plus one.
    -- one column will be low at a time, so we can just use multi-input NAND for this.
    -- when no column is being strobed, col_idx will equal "0000".
    -- when column 0 is being strobed, it will be "0001".  for column 12, "1101".
    --col_idx(3) <=
    --    not (col_input(12) and col_input(11) and col_input(10) and col_input(9) and col_input(8) and col_input(7));
    --col_idx(2) <=
    --    not (col_input(12) and col_input(11) and col_input(6) and col_input(5) and col_input(4) and col_input(3));
    --col_idx(1) <=
    --    not (col_input(10) and col_input(9) and col_input(6) and col_input(5) and col_input(2) and col_input(1));
    --col_idx(0) <=
    --    not (col_input(12) and col_input(10) and col_input(8) and col_input(6) and col_input(4) and col_input(2) and col_input(0));

    -- have_keypress = '1' when at least one key is pressed (except shift/ctrl/break)
    have_keypress <= '0' when (col_match_1 = "1111" and col_match_2 = "1111") else '1';

    -- match_1 and match_2 are '1' when their associated column is strobed by the keyboard encoder
    match_1 <= '1' when col_idx = col_match_1 else '0';
    match_2 <= '1' when col_idx = col_match_2 else '0';

    -- pull row outputs low when their columns are matched
    row_output(0) <= '0' when
            (nkben = '1' and have_keypress = '1')
            or (nkben = '0' and (
                (match_1 = '1' and row_value_1 = "000") or (match_2 = '1' and row_value_2 = "000")
            )
        ) else 'Z';
    row_output(1) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "001") or (match_2 = '1' and row_value_2 = "001")
        ) else 'Z';
    row_output(2) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "010") or (match_2 = '1' and row_value_2 = "010")
        ) else 'Z';
    row_output(3) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "011") or (match_2 = '1' and row_value_2 = "011")
        ) else 'Z';
    row_output(4) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "100") or (match_2 = '1' and row_value_2 = "100")
        ) else 'Z';
    row_output(5) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "101") or (match_2 = '1' and row_value_2 = "101")
        ) else 'Z';
    row_output(6) <= '0' when nkben = '0' and (
            (match_1 = '1' and row_value_1 = "110") or (match_2 = '1' and row_value_2 = "110")
        ) else 'Z';
    -- shift and ctrl are special; they have diodes for anti-ghosting
    row_output(7) <= '0' when (col_idx = "0001" and ctrl_pressed = '1')
                           or (col_idx = "0000" and shift_pressed = '1') else 'Z';

    -- break is handled separately
    break_output <= '0' when break_pressed = '1' else 'Z';

    -- SPI interface:
    -- - Idle with spi_sel high
    -- - Bring spi_sel low to start transaction
    -- - Clock in 24 bits on spi_miso (data read on rising edge)
    --   - 4 column bits (index of column to match, for key 1)
    --   - 1 unused bit
    --   - 3 row bits (index of row to return, for key 1)
    --   - 4 column bits (index of column to match, for key 2)
    --   - 1 unused bit
    --   - 3 row bits (index of row to return, for key 2)
    --   - SHIFT state (1 = pressed)
    --   - CTRL state (1 = pressed)
    --   - BREAK state (1 = pressed)
    --   - 5 unused bits
    -- - Data is copied into registers on 24th rising edge on spi_clk
    -- - Return spi_sel high to end transaction / reset for next time
    process (spi_clk)
    begin
        spi_miso <= '0'; -- unused
        if spi_sel = '1' then
            spi_count <= "00000";
        elsif rising_edge(spi_clk) then
            spi_buf <= spi_buf(16 downto 0) & spi_mosi;
            spi_count <= std_logic_vector(unsigned(spi_count) + 1);
            -- copy when we get the 19th bit
            if spi_count = "10010" then
                col_match_1 <= spi_buf(17 downto 14);
                row_value_1 <= spi_buf(12 downto 10);
                col_match_2 <= spi_buf(9 downto 6);
                row_value_2 <= spi_buf(4 downto 2);
                shift_pressed <= spi_buf(1);
                ctrl_pressed <= spi_buf(0);
                break_pressed <= spi_mosi;
            end if;
        end if;
    end process;

end Behavioural;
