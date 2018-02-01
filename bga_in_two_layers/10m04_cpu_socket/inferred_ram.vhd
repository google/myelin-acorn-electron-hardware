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

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity sideways_ram is
  port (
    clock: in std_logic;
    fast_clock: in std_logic;
    data: in std_logic_vector(7 downto 0);
    address: in std_logic_vector(13 downto 0);
    we: in std_logic;
    q: out std_logic_vector(7 downto 0)
);
end sideways_ram;

architecture rtl of sideways_ram is

  type ramblock is array(0 TO 16383) of std_logic_vector(7 downto 0);
  signal ram: ramblock;

  signal address_sync : integer range 0 to 16383;
  signal we_sync : std_logic := '0';
  signal sync_clk : std_logic_vector(2 downto 0) := "000";
  signal debug_reg : std_logic_vector(7 downto 0) := x"23";

begin

  -- The 6502 expects us to latch data on the falling clock edge, but
  -- most block ram expects it on the rising edge instead, so we sync
  -- everything to fast_clock.

  process (fast_clock)
  begin
    if rising_edge(fast_clock) then
      sync_clk <= sync_clk(1 downto 0) & clock;

      if sync_clk(2) = '0' and sync_clk(1) = '1' then
        -- rising edge on clock: latch address and provide data
        address_sync <= to_integer(unsigned(address));
        we_sync <= we;
      end if;

      -- update q on every rising fast_clock edge
      --q <= debug_reg;
      q <= ram(address_sync);

      -- write on falling clock edge
      if we_sync = '1' and sync_clk(2) = '1' and sync_clk(1) = '0' then
        ram(address_sync) <= data;
        debug_reg <= data;
      end if;
      
    end if;
  end process;

  --process (clock)
  --begin
  --  if falling_edge(clock) then
  --    if we = '1' then
  --      debug_reg <= data;
  --    end if;
  --  end if;
  --end process;

end rtl;
