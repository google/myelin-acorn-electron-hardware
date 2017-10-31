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
    --DEBUG avr_MISO2 : in std_logic
  );
end standalone_programmer;

architecture Behavioural of standalone_programmer is

  --DEBUG signal avr_MISO : std_logic; --DEBUG
  -- 
  signal CTL : std_logic_vector (6 downto 0);
  signal A : std_logic_vector (15 downto 0);
  signal D_from_SPI : std_logic_vector(7 downto 0);
  signal D_from_cart : std_logic_vector (7 downto 0);
  signal spi_bit_count : std_logic_vector (4 downto 0) := "00000";
  signal memory_access : std_logic := '0';
  signal read_nwrite : std_logic := '1';

begin

  -- hackily using the AVR's SPI clock for both the PHI0 and 16MHZ lines.
  cart_PHI0 <= avr_SCK;
  cart_16MHZ <= avr_SCK;

  -- always drive A, only drive D/nOE/nOE2 during memory access
  cart_ROMQA <= A(14);
  cart_A <= A(13 downto 0);
  cart_RnW <= read_nwrite;

  -- nINFC and nINFD for when we're accessing &FCxx or &FDxx
  cart_nINFC <= '0' when (memory_access = '1' and A(15 downto 8) = x"FC" and avr_SCK = '1') else '1';
  cart_nINFD <= '0' when (memory_access = '1' and A(15 downto 8) = x"FD" and avr_SCK = '1') else '1';

  -- nOE for A(15:14) in "00", "01"
  cart_nOE <= '0' when (memory_access = '1' and A(15) = '0' and avr_SCK = '1') else '1';
  -- nOE2 for A(15:14) = "10"
  cart_nOE2 <= '0' when (memory_access = '1' and A(15 downto 14) = "10" and avr_SCK = '1') else '1';
  -- D driven on writes, tristated on reads
  cart_D <= D_from_SPI when memory_access = '1' and read_nwrite = '0' else "ZZZZZZZZ";

  -- AVR sends 0x80 for read, 0x00 for write
  read_nwrite <= CTL(6);

  process (avr_SCK, cpld_SS)
  begin

    -- SPI timing with AVR defaults: CPOL=0, CPHA=0
    -- Sample on SCK rising edge, setup on SCK falling edge.

    --   SS \_____________________________________________________________________________...
    --  SCK ___/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__/^^\__
    -- MOSI x00000111111222222333333444444555555666666777777000000111111222222333333444444...
    -- MISO x00000111111222222333333444444555555666666777777000000111111222222333333444444...

    -- This means we get barely any time to think in between bytes -- just the high period of
    -- SCK after the 8th bit.  We need to set up MISO on the falling edge of avr_SCK.

    if cpld_SS = '1' then

      -- asynchronous reset (must not happen on an avr_SCK edge)
      CTL <= "1111111";
      spi_bit_count <= "00000";
      A <= "0000000000000000";
      D_from_SPI <= "00000000";

    elsif rising_edge(avr_SCK) then

      -- to read: clock in "1000000" & A15, A14-7, A6-0 & 0, 0x00, and the data byte will come out in the 4th byte
      -- to write: clock in "0000000" & A15, A14-7 A6-0 & 0, D, and the byte will be written on the final clock.

      -- increment the count each time
      spi_bit_count <= std_logic_vector(unsigned(spi_bit_count) + 1);

      -- clock in a bit, depending on spi_bit_count
      if spi_bit_count(4 downto 3) = "00" then
        -- reading CTL (outputting 1 on MISO) and A15
        CTL <= CTL(5 downto 0) & A(15);
        A(15) <= avr_MOSI;
      elsif spi_bit_count(4 downto 3) = "01" or spi_bit_count(4 downto 3) = "10" then
        -- reading A (outputting 0 on MISO)
        if spi_bit_count /= "10111" then
          A(14 downto 0) <= A(13 downto 0) & avr_MOSI;
        end if;
      else
        -- reading or writing data; spi_bit_count(4 downto 3) = "11"
        D_from_SPI <= D_from_SPI(6 downto 0) & avr_MOSI;
        if spi_bit_count = "11111" then
          -- we've just received the last bit of the data byte, which means we should 
        end if;
      end if;
    end if;

    if cpld_SS = '1' then

      avr_MISO <= '0';
      D_from_cart <= "10101010";
      memory_access <= '0';

    elsif falling_edge(avr_SCK) then

      -- We always update MISO on an avr_SCK falling edge.

      -- memory_access is set to 1 on the falling edge when the avr is setting up
      -- the final bit of the address, then back to 0 on the next falling edge.
      -- This is so we generate a clean pulse on cart_nOE and cart_nOE2, by ANDing
      -- with avr_SCK.
      memory_access <= '0';

      if spi_bit_count(4 downto 3) = "00" then
        -- reading CTL, outputting 1
        avr_MISO <= '1';
      elsif spi_bit_count(4 downto 3) = "01" or spi_bit_count(4 downto 3) = "10" then
        -- reading A, outputting 0
        avr_MISO <= '0';
        if spi_bit_count = "10110" and read_nwrite = '1' then
          -- the AVR is setting up a 0 bit (it's finished sending us the address), so we set
          -- memory_access = '1', and the access will occur once avr_SCK goes high again.
          memory_access <= '1';
        elsif spi_bit_count = "10111" and read_nwrite = '1' then
          D_from_cart <= cart_D; -- actually perform the read
        end if;
      else
        -- reading out data register (happens even when nothing is going on)
        avr_MISO <= D_from_cart(7);
        D_from_cart <= D_from_cart(6 downto 0) & '0';
        if spi_bit_count = "11111" and read_nwrite = '0' then
          -- we're about to receive the last data bit, and we're doing a write, so we need
          -- to get ready to enable nOE etc.
          memory_access <= '1';
        end if;
      end if;

    end if;
  end process;

end Behavioural;
