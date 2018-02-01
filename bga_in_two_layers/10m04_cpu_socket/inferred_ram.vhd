-- Copyright 2018 Google LLC
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

-- simple 16k single port block RAM that runs as fast as you like

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity sideways_ram is
  port (
    clock: in std_logic;
    data: in std_logic_vector(7 downto 0);
    address: in std_logic_vector(13 downto 0);
    -- TODO add a read enable
    we: in std_logic;
    q: out std_logic_vector(7 downto 0)
);
end sideways_ram;

architecture rtl of sideways_ram is

  type ramblock is array(0 TO 16383) of std_logic_vector(7 downto 0);
  signal ram: ramblock;

begin

  process (clock)
  begin
    if rising_edge(clock) then
      q <= ram(to_integer(unsigned(address)));

      if we = '1' then
        ram(to_integer(unsigned(address))) <= data;
      end if;
      
    end if;
  end process;

end rtl;
