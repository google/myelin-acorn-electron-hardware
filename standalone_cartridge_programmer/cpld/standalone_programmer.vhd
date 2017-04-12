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

entity standalone_programmer is 
  Port (
    -- cartridge address
    cart_nINFC,
    cart_nINFD,
    cart_ROMQA : out std_logic;
    cart_A : out std_logic_vector (13 downto 0);

    -- cartridge data
    cart_D : inout std_logic_vector(7 downto 0);

    -- cartridge clock and memory control
    cart_PHI0,
    cart_16MHZ,
    cart_RnW,
    cart_nOE,
    cart_nOE2 : out std_logic;

    -- avr SPI signals
    avr_MOSI,
    avr_SCK,
    cpld_SS : in std_logic;
    avr_MISO : out std_logic
  );
end standalone_programmer;

architecture Behavioural of standalone_programmer is

  -- 
  signal CTL : std_logic_vector (7 downto 0);
  signal A : std_logic_vector (15 downto 0);
  signal D : std_logic_vector (7 downto 0);
  signal spi_bit_count : std_logic_vector (4 downto 0) := "00000";
  signal memory_access : std_logic := '0';
  signal read_nwrite : std_logic := '1';

begin

  -- hackily using the AVR's SPI clock for both the PHI0 and 16MHZ lines, but inverted so we can do the reads and writes at the right time
  cart_PHI0 <= not avr_SCK;
  cart_16MHZ <= not avr_SCK;

  -- always drive A, only drive D/nOE/nOE2 during memory access
  cart_ROMQA <= A(14);
  cart_A <= A(13 downto 0);
  cart_RnW <= read_nwrite;
  cart_nINFC <= '1';
  cart_nINFD <= '1';

  -- nOE for A(15:14) in "00", "01"
  cart_nOE <= '0' when memory_access = '1' and A(15) = '0' else '1';
  -- nOE2 for A(15:14) = "10"
  cart_nOE2 <= '0' when memory_access = '1' and A(15 downto 14) = "10" else '1';
  -- D driven on writes, tristated on reads
  cart_D <= D when memory_access = '1' and read_nwrite = '0' else "ZZZZZZZZ";

  process (avr_SCK, cpld_SS)
  begin
    if cpld_SS = '1' then

      -- asynchronous reset (must not happen on an avr_SCK edge)
      spi_bit_count <= "00000";
      memory_access <= '0';
      A <= "0000000000000000";
      D <= "00000000";

    elsif rising_edge(avr_SCK) then

      -- to read: clock in 0x80 A15-8 A7-0 0x00, and the data byte will come out in the 4th byte
      -- this is implemented

      -- to write: clock in 0x81 A15-8 A7-0 D, and the byte will be written on the final clock.
      memory_access <= '0';
      read_nwrite <= '1';

      -- increment the count each time
      spi_bit_count <= std_logic_vector(unsigned(spi_bit_count) + 1);

      -- clock in a bit, depending on spi_bit_count
      if spi_bit_count(4 downto 3) = "00" then
        -- reading CTL
        CTL <= CTL(6 downto 0) & avr_MOSI;
      elsif spi_bit_count(4 downto 3) = "01" or spi_bit_count(4 downto 3) = "10" then
        -- reading A
        A <= A(14 downto 0) & avr_MOSI;
        if spi_bit_count = "10111" and CTL = "10000001" then
          -- doing a memory read this cycle.
          memory_access <= '1';
          read_nwrite <= '1';
        end if;
      else
        -- reading or writing data; spi_bit_count(4 downto 3) = "11"
        if memory_access = '1' and read_nwrite = '1' then
          avr_MISO <= cart_D(7);
          D <= cart_D(6 downto 0) & '0';
        else
          avr_MISO <= D(7);
          D <= D(6 downto 0) & avr_MOSI;
        end if;
        if spi_bit_count = "11111" and CTL = "10000000" then
          -- execute a memory write, now that we have the whole 8 bits
          memory_access <= '1';
          read_nwrite <= '0';
        end if;
      end if;
    end if;
  end process;

end Behavioural;
