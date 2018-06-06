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

-- Convert altera_onchip_flash signals to something that works more like an
-- ordinary flash chip at 2MHz.  altera_onchip_flash is designed to run at a
-- super high clock rate, but requires a few clock cycles to return data.

-- From the Max 10 UFM User Guide:

-- 10M04SC only has the UFM0 sector -- no UFM1, or CFM{0, 1, 2}.
-- UFM0 has 8 x 16kb (2kB) pages, for a total of 16kB of user flash.
-- Either a whole sector, or an individual page, can be erased.

-- csr_addr = '0' => read-only status register
--   "1111111111111111111111" & sp5 & sp4 & sp3 & sp2 & sp1 & es & ws & rs & busy[2]
-- csr_addr = '1' => read/write control register
--   "1111" & wp5 & wp4 & wp3 & wp2 & wp1 & se[3] & pe[20]

entity elk_user_flash is
  port (
    slow_clock : in std_logic;  -- 2MHz clock
    fast_clock : in std_logic;  -- 116MHz clock
    reset_n : in std_logic;
    address : std_logic_vector(13 downto 0);
    en : in std_logic;  -- active-high read enable
    data_out : out std_logic_vector(7 downto 0)
  );
end elk_user_flash;

architecture rtl of elk_user_flash is

  signal slow_clock_sync : std_logic_vector(2 downto 0);
  signal address_reg : std_logic_vector(13 downto 0);
  signal data_reg : std_logic_vector(7 downto 0) := x"75";

  signal flash_read : std_logic := '0';
  signal flash_readdatavalid : std_logic;
  signal flash_readdata : std_logic_vector(31 downto 0);
  signal flash_waitrequest : std_logic;
  signal csr_readdata : std_logic_vector(31 downto 0);

  -- 10M04 internal flash
  component internal_flash is
    port (
      clock                   : in  std_logic                     := 'X';             -- clk
      reset_n                 : in  std_logic                     := 'X';             -- reset_n
      avmm_data_addr          : in  std_logic_vector(11 downto 0) := (others => 'X'); -- address
      avmm_data_read          : in  std_logic                     := 'X';             -- read
      avmm_data_writedata     : in  std_logic_vector(31 downto 0) := (others => 'X'); -- writedata
      avmm_data_write         : in  std_logic                     := 'X';             -- write
      avmm_data_readdata      : out std_logic_vector(31 downto 0);                    -- readdata
      avmm_data_waitrequest   : out std_logic;                                        -- waitrequest
      avmm_data_readdatavalid : out std_logic;                                        -- readdatavalid
      avmm_data_burstcount    : in  std_logic_vector(3 downto 0)  := (others => 'X'); -- burstcount
      avmm_csr_addr           : in  std_logic                     := 'X';             -- address
      avmm_csr_read           : in  std_logic                     := 'X';             -- read
      avmm_csr_writedata      : in  std_logic_vector(31 downto 0) := (others => 'X'); -- writedata
      avmm_csr_write          : in  std_logic                     := 'X';             -- write
      avmm_csr_readdata       : out std_logic_vector(31 downto 0)                     -- readdata
    );
  end component internal_flash;


begin

  -- latched data from the last successful read
  data_out <= data_reg;

  -- everything is synchronous to the flash clock
  process (fast_clock)
  begin
    if rising_edge(fast_clock) then

      -- clear read pulse from last clock
      flash_read <= '0';

      -- sync and edge detect on elk clock
      slow_clock_sync <= slow_clock_sync(1 downto 0) & slow_clock;
      if slow_clock_sync(2) = '1' and slow_clock_sync(1) = '0' and en = '1' then
        -- rising edge of elk clock and we're enabled: start a read
        address_reg <= address;
        flash_read <= '1';
      end if;

      -- this will take 5-6 clocks, i.e. ~75 ns plus the time to register flash_read and data_reg

      -- register flash output when we get a successful read
      if flash_readdatavalid = '1' then
        case address_reg(1 downto 0) is
          when "00" => data_reg <= flash_readdata(7 downto 0);
          when "01" => data_reg <= flash_readdata(15 downto 8);
          when "10" => data_reg <= flash_readdata(23 downto 16);
          when "11" => data_reg <= flash_readdata(31 downto 24);
        end case;
      end if;

    end if;
  end process;

  -- Max 10 internal flash
  flash0 : component internal_flash
    port map (
      clock                   => fast_clock,          --    clk.clk
      reset_n                 => reset_n,             -- nreset.reset_n
      avmm_data_addr          => address_reg(13 downto 2),             --   data.address
      avmm_data_read          => flash_read,          --       .read
      avmm_data_writedata     => (others => '0'),     --       .writedata
      avmm_data_write         => '0',                 --       .write
      avmm_data_readdata      => flash_readdata,      --       .readdata
      avmm_data_waitrequest   => flash_waitrequest,                 --       .waitrequest
      avmm_data_readdatavalid => flash_readdatavalid, --       .readdatavalid
      avmm_data_burstcount    => std_logic_vector(to_unsigned(1, 4)),                   --       .burstcount
      avmm_csr_addr           => '0',             --    csr.address
      avmm_csr_read           => '0',                   --       .read
      avmm_csr_writedata      => (others => '0'),     --       .writedata
      avmm_csr_write          => '0',                   --       .write
      avmm_csr_readdata       => csr_readdata      --       .readdata
    );

end rtl;
