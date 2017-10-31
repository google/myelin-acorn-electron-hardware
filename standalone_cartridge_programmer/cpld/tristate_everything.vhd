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

begin

  cart_nINFC <= 'Z';
  cart_nINFD <= 'Z';
  cart_ROMQA <= 'Z';
  cart_A <= "ZZZZZZZZZZZZZZ";

  cart_D <= "ZZZZZZZZ";

  cart_PHI0 <= 'Z';
  cart_16MHZ <= 'Z';
  cart_RnW <= 'Z';
  cart_nOE <= 'Z';
  cart_nOE2 <= 'Z';

  avr_MISO <= 'Z';

end Behavioural;
