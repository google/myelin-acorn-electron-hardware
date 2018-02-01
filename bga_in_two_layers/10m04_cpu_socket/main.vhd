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

entity cpu_socket_fpga is
  port (
    c1_1 : inout std_logic;
    c1_2 : inout std_logic;
    c1_3 : inout std_logic;
    c1_5 : inout std_logic;
    c1_6 : inout std_logic;
    c1_7 : inout std_logic;
    c1_9 : inout std_logic;
    c1_10 : inout std_logic;
    c1_11 : inout std_logic;
    c1_12 : inout std_logic;
    c1_13 : inout std_logic;
    c1_14 : inout std_logic;
    c1_16 : inout std_logic;
    c1_17 : inout std_logic;
    c1_18 : in std_logic;  -- ext_GP6
    c1_19 : inout std_logic;  -- BAD
    c1_20 : in std_logic;  -- ext_GP0
    c1_22 : in std_logic;  -- ext_GP8
    c1_23 : in std_logic;  -- ext_GP2
    c1_24 : out std_logic;  -- ext_GP1
    c1_25 : in std_logic;  -- ext_GP10
    c1_26 : in std_logic;  -- ext_GP7
    c1_27 : out std_logic;  -- ext_GP4
    c1_28 : out std_logic;  -- ext_GP3
    c1_29 : out std_logic;  -- ext_GP11
    c1_30 : in std_logic;  -- ext_GP9
    c1_31 : out std_logic;  -- ext_GP5
    c1_33 : inout std_logic;  -- ext_D2
    c1_34 : inout std_logic;  -- ext_D0
    c1_36 : in std_logic;  -- ext_GP12
    c1_37 : inout std_logic;  -- ext_D3
    c1_38 : inout std_logic;  -- ext_D1

    c2_1 : inout std_logic;
    c2_3 : inout std_logic;
    c2_4 : inout std_logic;
    c2_5 : inout std_logic;
    c2_8 : inout std_logic;
    c2_12 : inout std_logic;

    c3_1 : inout std_logic;  -- ext_D4
    c3_2_CLK3n : inout std_logic;  -- ext_D5
    c3_3 : inout std_logic;  -- ext_D6
    c3_4 : inout std_logic;  -- ext_D7
    c3_5_CLK3p : in std_logic;  -- ext_A0
    c3_6 : in std_logic;  -- ext_A1
    c3_7 : in std_logic;  -- ext_A2
    c3_8 : in std_logic;  -- ext_A3
    c3_9 : in std_logic;  -- ext_A4
    c3_10 : in std_logic;  -- ext_A5
    c3_11 : in std_logic;  -- ext_A6
    c3_12 : in std_logic;  -- ext_A7

    c4_3_VREFB2N0 : inout std_logic;
    c4_4 : inout std_logic;
    c4_6 : inout std_logic;
    c4_7 : inout std_logic;
    c4_8 : inout std_logic;
    c4_10 : inout std_logic;
    c4_11 : inout std_logic;
    c4_12 : inout std_logic;
    c4_13 : inout std_logic;
    c4_14 : inout std_logic;
    c4_15_DPCLK1 : inout std_logic;
    c4_16_DPCLK0 : inout std_logic;
    c4_17 : inout std_logic;
    c4_18 : inout std_logic;
    c4_19 : inout std_logic;
    c4_20 : inout std_logic;
    c4_21 : inout std_logic;
    c4_22 : inout std_logic;
    c4_23 : inout std_logic;
    c4_24 : inout std_logic;
    c4_25 : inout std_logic;
    c4_26 : inout std_logic;
    c4_27 : inout std_logic;
    c4_28 : out std_logic;  -- ext_uart_txd (plug in white cable from Adafruit adapter)
    c4_30 : inout std_logic;
    c4_31 : inout std_logic;  -- ext_A11 on first try board, which has bad c4_39
    c4_32 : in std_logic;  -- ext_uart_rxd (plug in green cable from Adafruit adapter)
    c4_33 : in std_logic;  -- ext_A14
    c4_34 : in std_logic;  -- ext_A12
    c4_35 : in std_logic;  -- ext_A10
    c4_36 : in std_logic;  -- ext_A8
    c4_37 : in std_logic;  -- ext_A15
    c4_38 : in std_logic;  -- ext_A13
    c4_39 : in std_logic;  -- ext_A11, bad on first try board
    c4_40 : in std_logic  -- ext_A9
  );
end cpu_socket_fpga;

architecture rtl of cpu_socket_fpga is

  component main_to_elk is
    port (
      debug_uart_txd : out std_logic;
      debug_a : out std_logic;
      debug_b : out std_logic;
      ext_uart_rxd : in std_logic;
      ext_uart_txd : out std_logic;
      fast_clock : in std_logic; -- pass through for FPGA's internal flash

      -- connections to the cpu_socket_expansion board
      ext_A : in std_logic_vector(15 downto 0);
      ext_D : inout std_logic_vector(7 downto 0);

      ext_GP0 : in std_logic; -- PHI2
      ext_GP1 : out std_logic; -- n_global_enable
      ext_GP2 : in std_logic; -- 16MHz
      ext_GP3 : out std_logic; -- dbuf_nOE
      ext_GP4 : out std_logic; -- n_accessing_shadow_ram
      ext_GP5 : out std_logic; -- n_cpu_is_external
      ext_GP6 : in std_logic; -- RnW
      ext_GP7 : in std_logic; -- nRESET
      ext_GP8 : in std_logic; -- READY
      ext_GP9 : in std_logic; -- /NMI
      ext_GP10 : in std_logic; -- /IRQ
      ext_GP11 : out std_logic; -- dbuf_driven_by_cpu
      ext_GP12 : in std_logic
    );
  end component;

  component internal_osc is
  	port (
  		clkout : out std_logic;        -- clkout.clk
  		oscena : in  std_logic := '0'  -- oscena.oscena
  	);
  end component;

	signal clk : std_logic;  -- 55-115MHz clock from internal oscillator
	signal clk_div_count : std_logic_vector(26 downto 0) := (others => '0');
	signal slow_clk : std_logic;  -- clk/(128*1024*1024), 0.4-0.85 Hz

begin

  elk0: component main_to_elk port map (
    
    debug_uart_txd => c2_1,
    debug_a => c2_3,
    debug_b => c2_5,

    ext_uart_txd => c4_28,
    ext_uart_rxd => c4_32,

    fast_clock => clk,
    -- fast_clock => clk_div_count(0),

    ext_A(0) => c3_5_CLK3p,
    ext_A(1) => c3_6,
    ext_A(2) => c3_7,
    ext_A(3) => c3_8,
    ext_A(4) => c3_9,
    ext_A(5) => c3_10,
    ext_A(6) => c3_11,
    ext_A(7) => c3_12,
    ext_A(8) => c4_36,
    ext_A(9) => c4_40,
    ext_A(10) => c4_35,
    ext_A(11) => c4_39,  -- c4_31 on first try board, c4_39 on second
    ext_A(12) => c4_34,
    ext_A(13) => c4_38,
    ext_A(14) => c4_33,
    ext_A(15) => c4_37,

    ext_D(0) => c1_34,
    ext_D(1) => c1_38,
    ext_D(2) => c1_33,
    ext_D(3) => c1_37,
    ext_D(4) => c3_1,
    ext_D(5) => c3_2_CLK3n,
    ext_D(6) => c3_3,
    ext_D(7) => c3_4,

    ext_GP0 => c1_20,
    ext_GP1 => c1_24,
    ext_GP2 => c1_23,
    ext_GP3 => c1_28,
    ext_GP4 => c1_27,
    ext_GP5 => c1_31,
    ext_GP6 => c1_18,
    ext_GP7 => c1_26,
    ext_GP8 => c1_22,
    ext_GP9 => c1_30,
    ext_GP10 => c1_25,
    ext_GP11 => c1_29,
    ext_GP12 => c1_36
  );

  -- Max 10 internal oscillator
	int_osc_0 : component internal_osc port map (
		oscena => '1',
		clkout => clk
	);

  -- Divide clock down to ~1Hz
  process (clk)
  begin
    if rising_edge(clk) then
      clk_div_count <= std_logic_vector(unsigned(clk_div_count) + 1);
      if unsigned(clk_div_count) = 0 then
        slow_clk <= not slow_clk;
      end if;
    end if;
  end process;

  -- Output 1Hz clock on all unused pins
  c1_1 <= slow_clk;
  c1_2 <= 'Z';  -- poor solder connection, tristate so we can patch
  c1_3 <= slow_clk;
  c1_5 <= slow_clk;
  c1_6 <= slow_clk;
  c1_7 <= slow_clk;
  c1_9 <= slow_clk;
  c1_10 <= slow_clk;
  c1_11 <= slow_clk;
  c1_12 <= slow_clk;
  c1_13 <= slow_clk;
  c1_14 <= slow_clk;
  c1_16 <= slow_clk;
  c1_17 <= slow_clk;
  -- c1_18 <= slow_clk;
  c1_19 <= 'Z';  -- poor solder connection, tristate so we can patch
  -- c1_20 <= slow_clk;
  -- c1_22 <= slow_clk;
  -- c1_23 <= slow_clk;
  -- c1_24 <= slow_clk;
  -- c1_25 <= slow_clk;
  -- c1_26 <= slow_clk;
  -- c1_27 <= slow_clk;
  -- c1_28 <= slow_clk;
  -- c1_29 <= slow_clk;
  -- c1_30 <= slow_clk;
  -- c1_31 <= slow_clk;
  -- c1_33 <= slow_clk;
  -- c1_34 <= slow_clk;
  -- c1_36 <= slow_clk;
  -- c1_37 <= slow_clk;
  -- c1_38 <= slow_clk;

  -- c2_1 <= slow_clk; -- debug uart tx
  -- c2_3 <= slow_clk; -- debug a
  c2_4 <= slow_clk;
  -- c2_5 <= slow_clk; -- debug b
  c2_8 <= slow_clk;
  c2_12 <= slow_clk;

  -- c3_1 <= slow_clk;
  -- c3_2_CLK3n <= slow_clk;
  -- c3_3 <= slow_clk;
  -- c3_4 <= slow_clk;
  -- c3_5_CLK3p <= slow_clk;
  -- c3_6 <= slow_clk;
  -- c3_7 <= slow_clk;
  -- c3_8 <= slow_clk;
  -- c3_9 <= slow_clk;
  -- c3_10 <= slow_clk;
  -- c3_11 <= slow_clk;
  -- c3_12 <= slow_clk;

  c4_3_VREFB2N0 <= slow_clk;
  c4_4 <= slow_clk;
  c4_6 <= slow_clk;
  c4_7 <= slow_clk;
  c4_8 <= slow_clk;
  c4_10 <= slow_clk;
  c4_11 <= slow_clk;
  c4_12 <= slow_clk;
  c4_13 <= slow_clk;
  c4_14 <= slow_clk;
  c4_15_DPCLK1 <= slow_clk;
  c4_16_DPCLK0 <= slow_clk;
  c4_17 <= 'Z';  -- poor solder connection, tristate so we can patch
  c4_18 <= slow_clk;
  c4_19 <= slow_clk;
  c4_20 <= slow_clk;
  c4_21 <= slow_clk;
  c4_22 <= slow_clk;
  c4_23 <= 'Z';  -- poor solder connection, tristate so we can patch
  c4_24 <= slow_clk;
  c4_25 <= slow_clk;
  c4_26 <= slow_clk;
  c4_27 <= slow_clk;
  -- c4_28 <= 'Z';  -- poor solder connection, tristate so we can patch
  c4_30 <= slow_clk;
  c4_31 <= 'Z';  -- patched over c4_39 on first try board; leaving Z in case i program the old board by mistake
  -- c4_32 <= slow_clk;
  -- c4_33 <= slow_clk;
  -- c4_34 <= slow_clk;
  -- c4_35 <= slow_clk;
  -- c4_36 <= slow_clk;
  -- c4_37 <= slow_clk;
  -- c4_38 <= slow_clk;
  -- c4_39 <= 'Z';  -- poor solder connection on try 1 board, tristated so we can patch
  -- c4_40 <= slow_clk;

end rtl;
