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

-- Adapter component so that elk_interface doesn't have to deal directly with
-- the ext_* signals on the cpu_socket_expansion board.

entity main_to_elk is
  port (
    -- 55-116MHz clock for FPGA's internal flash
    fast_clock : in std_logic;

    debug_uart_txd : out std_logic;
    debug_a : out std_logic;
    debug_b : out std_logic;
    ext_uart_rxd : in std_logic;
    ext_uart_txd : out std_logic;

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
    ext_GP11 : out std_logic := '1'; -- dbuf_driven_by_cpu
    ext_GP12 : in std_logic
  );
end main_to_elk;

architecture rtl of main_to_elk is

  component elk_interface is
    port (
      debug_uart_txd : out std_logic;
      debug_a : out std_logic;
      debug_b : out std_logic;
      ext_uart_rxd : in std_logic;
      ext_uart_txd : out std_logic;
      fast_clock : in std_logic; -- pass through for FPGA's internal flash
      elk_A : in std_logic_vector(15 downto 0);
      elk_D : inout std_logic_vector(7 downto 0);
      elk_PHI0 : in std_logic;
      elk_16MHz : in std_logic;
      elk_nEN : out std_logic; -- global enable
      elk_nDBUF_OE : out std_logic; -- /OE for DBUF chip
      elk_nSHADOW : out std_logic; -- '0' when shadowing memory
      elk_nCPU_IS_EXTERNAL : out std_logic; -- '0' for external cpu
      elk_RnW : in std_logic; -- input
      elk_nRESET : in std_logic; -- input
      elk_READY : in std_logic; -- input
      elk_nNMI : in std_logic; -- input
      elk_nIRQ : in std_logic; -- input
      elk_CPU_DBUF : out std_logic -- '0' when we're driving the bus, '1' when the cpu is
    );
  end component;

begin

  exp0: component elk_interface port map (
    debug_uart_txd => debug_uart_txd,
    debug_a => debug_a,
    debug_b => debug_b,
    ext_uart_txd => ext_uart_txd,
    ext_uart_rxd => ext_uart_rxd,
    fast_clock => fast_clock,
    elk_A => ext_A,
    elk_D => ext_D,
    elk_PHI0 => ext_GP0,
    elk_nEN => ext_GP1,
    elk_16MHz => ext_GP2,
    elk_nDBUF_OE => ext_GP3,
    elk_nSHADOW => ext_GP4,
    elk_nCPU_IS_EXTERNAL => ext_GP5,
    elk_RnW => ext_GP6,
    elk_nRESET => ext_GP7,
    elk_READY => ext_GP8,
    elk_nNMI => ext_GP9,
    elk_nIRQ => ext_GP10,
    elk_CPU_DBUF => ext_GP11
  );

end rtl;
