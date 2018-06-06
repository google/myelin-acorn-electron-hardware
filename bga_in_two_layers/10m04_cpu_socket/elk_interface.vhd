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

-- This file contains code for the stuff that the Electron will actually see:
--

-- Sideways banks:
-- 0+1, 2+3, 4+5 = cartridges on the Minus One
-- 6 = "rom zero", implemented here
-- 7 = sideways RAM, implemented here
-- 8+9 = keyboard
-- 10+11 = BASIC ROM
-- 12, 13, 14, 15 = unused

entity elk_interface is
  port (
    debug_uart_txd : out std_logic;  -- 2MHz trace uart transmitter
    debug_a : out std_logic;
    debug_b : out std_logic;
    ext_uart_rxd : in std_logic;  -- 115k2 sideways ram input
    ext_uart_txd : out std_logic;  -- 115k2 debug output

    fast_clock : in std_logic;  -- 82MHz internal oscillator clock

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
end elk_interface;

architecture rtl of elk_interface is

  -- '1' when elk_A is in sideways space
  signal SIDEWAYS : std_logic;

  -- '1' when elk_A = FCFx
  signal DEBUG : std_logic;
  signal debug_reg : std_logic_vector(7 downto 0) := "10101100";  -- &AC

  -- currently selected memory bank, defaults to BASIC
  signal bank : std_logic_vector(3 downto 0) := x"A";

  -- '1' when we're selected
  signal driving_bus : std_logic;

  -- '1' when reading from the embedded ROM
  signal reading_rom_zero : std_logic;
  -- internal wiring for embedded ROM
  signal rom_zero_D : std_logic_vector(7 downto 0);

  -- '1' when reading/writing sideways ram
  signal accessing_sideways_ram : std_logic;
  signal sideways_ram_D : std_logic_vector(7 downto 0);

  -- synchronous sideways ram signals
  signal sideways_ram_data : std_logic_vector(7 downto 0) := (others => '0');
  signal sideways_ram_address : std_logic_vector(13 downto 0) := (others => '0');
  signal sideways_ram_rd : std_logic := '0';
  signal sideways_ram_rd2 : std_logic := '0';
  signal sideways_ram_we : std_logic := '0';
  signal sideways_ram_q : std_logic_vector(7 downto 0);

  component uart is
    generic (
      divide_count : integer
    );
    port (
      clock : in std_logic;  -- main clock
      txd : out std_logic := '1';
      tx_data : in std_logic_vector(23 downto 0);
      tx_empty : out std_logic; -- '1' when tx_data can take a new byte
      transmit : in std_logic -- pulse '1' when tx_data is valid
    );
  end component;

  component uart_rx is
    generic (
      divide_count : integer
    );
    port (
      clock : in std_logic;  -- main clock
      rxd : in std_logic := '1';
      rx_data : out std_logic_vector(7 downto 0);
      rx_full : out std_logic; -- '1' when rx_data is valid
      ack : in std_logic -- pulse '1' when rx_data has been read
    );
  end component;

  -- 2MHz debug uart
  signal uart_txd : std_logic;
  signal uart_tx_data : std_logic_vector(23 downto 0);
  signal uart_tx_empty : std_logic;
  signal uart_transmit : std_logic;

  -- byte received from external uart to fill sideways ram
  signal uart_rx_data : std_logic_vector(7 downto 0);
  signal uart_rx_full : std_logic;
  signal uart_rx_ack : std_logic := '1';
  -- when loading ram via the uart, keep track of the address
  signal uart_rx_address : unsigned(13 downto 0) := (others => '1');

  -- 115k2 debug uart
  signal ext_uart_tx_data : std_logic_vector(23 downto 0) := x"644266";
  signal ext_uart_tx_empty : std_logic;
  signal ext_uart_tx_transmit : std_logic := '0';

  signal sync_PHI0 : std_logic_vector(2 downto 0) := "000";
  type three_word_array is array(2 downto 0) of std_logic_vector(15 downto 0);
  signal sync_A : three_word_array;
  type three_byte_array is array(2 downto 0) of std_logic_vector(7 downto 0);
  signal sync_D : three_byte_array;
  signal sync_RESET : std_logic_vector(2 downto 0) := "000";

  -- elk_A sampled on the rising PHI0 edge
  signal sampled_A : std_logic_vector(15 downto 0) := x"0000";

  -- FIFO so we can capture addr + data
  component uart_fifo
    PORT
    (
      clock   : IN STD_LOGIC ;
      data    : IN STD_LOGIC_VECTOR (23 DOWNTO 0);
      rdreq   : IN STD_LOGIC ;
      wrreq   : IN STD_LOGIC ;
      empty   : OUT STD_LOGIC ;
      full    : OUT STD_LOGIC ;
      q   : OUT STD_LOGIC_VECTOR (23 DOWNTO 0);
      usedw   : OUT STD_LOGIC_VECTOR (8 DOWNTO 0)
    );
  end component;


  signal uart_fifo_read_req : std_logic;
  signal uart_fifo_write_req : std_logic;
  signal uart_fifo_empty : std_logic;
  signal uart_fifo_empty_sync : std_logic;
  signal uart_fifo_full : std_logic;
  signal uart_fifo_input : std_logic_vector(23 downto 0);
  signal uart_fifo_output : std_logic_vector(23 downto 0);
  signal uart_fifo_usedw : std_logic_vector(8 downto 0);

  signal capturing : std_logic := '0';

  -- count of the number of words we think we've sent to the uart.
  -- this resets when we start a new transfer.
  signal n_words_sent_to_uart : unsigned(31 downto 0) := x"00000000";

begin

  -- global settings
  elk_nEN <= '0';
  elk_nSHADOW <= '1';
  elk_nCPU_IS_EXTERNAL <= '1';

  -- '0' to buffer from us to CPU, '1' to buffer from CPU to us
  elk_CPU_DBUF <= not driving_bus;

  -- only drive buffers during high clock period, when
  -- either the cpu is writing, or we're selected and
  -- the cpu is reading
  elk_nDBUF_OE <= '0' when (
      elk_PHI0 = '1' -- always buffer inward so we can track stuff
      or elk_RnW = '0' -- extend out past the falling edge to give some hold time
    ) else '1';

  -- sideways address space
  SIDEWAYS <= '1' when elk_A(15 downto 14) = "10" else '0';

  -- rom "zero" in bank 6 (the name comes from way back when I had it in bank 0)
  --reading_rom_zero <= '1' when SIDEWAYS = '1' and bank = x"6" else '0';
  --DEBUG: put it in &FDxx as well
  reading_rom_zero <= '1' when
    (SIDEWAYS = '1' and bank = x"6") or (elk_A(15 downto 8) = x"FD")
    else '0';

  -- sideways ram in bank 7 (or bank 0, depending)
  accessing_sideways_ram <= '1' when SIDEWAYS = '1' and bank = x"7" else '0';
  --DEBUG: put it in &FDxx as well
  --accessing_sideways_ram <= '1' when
  --  (SIDEWAYS = '1' and bank = x"7") or (elk_A(15 downto 8) = x"FD")
  --  else '0';

  -- debug register
  DEBUG <= '1' when sampled_A(15 downto 4) = x"FCF" else '0';

  -- data bus access
  driving_bus <=
    -- never during low clock period
    '0' when elk_PHI0 = '0' else
    -- never when cpu is writing
    '0' when elk_RnW = '0' else
    ---- cases when we do drive the bus follow:
    '1' when (
      -- drive when reading embedded memory
      (
        accessing_sideways_ram = '1'
        or reading_rom_zero = '1'
      )
      -- drive when reading registers
      or (
        DEBUG = '1'
      )
    ) else
    -- we're not selected
    '0';

  -- data bus
  elk_D <=
    "ZZZZZZZZ" when driving_bus = '0' else
    -- -- reading from tube
    -- tube_D when tube_access = '1' else
    -- reading data from the embedded ROM
    rom_zero_D when reading_rom_zero = '1' else
    sideways_ram_D when accessing_sideways_ram = '1' else
    -- reading debug register
    debug_reg when DEBUG = '1' and elk_A(3 downto 0) = x"0" else
    "0000" & bank when DEBUG = '1' and elk_A(3 downto 0) = x"1" else
    elk_A(3 downto 0) & elk_A(3 downto 0) when DEBUG = '1' else
    -- -- reading SPI status
    -- MS_SD_MISO & "0000000" when EPP_STATUS = '1' else
    -- -- reading serial RX
    -- MS_SERIAL_RX & "11111" & MS_SERIAL_CTS & "1" when EUP_SERIAL = '1' else
    -- default: this should never happen
    "10101010";

  -- Handle writes from Electron
  process (elk_nRESET, elk_PHI0)
  begin
    if elk_nRESET = '0' then

      -- default to BASIC ROM
      bank <= x"A";

    elsif falling_edge(elk_PHI0) then

      -- set sideways bank
      if (
        elk_RnW = '0' and
        elk_A(15 downto 8) & elk_A(3 downto 0) = x"FE5" and
        elk_D(7 downto 4) = x"0"
      ) then
        bank <= elk_D(3 downto 0);
      end if;

      -- debugging
      if elk_RnW = '0' and DEBUG = '1' then
        debug_reg <= elk_D;
      end if;

    end if;
  end process;

  -- Instantiate hardcoded ROM using 16k of block memory
  rom_zero0: entity work.elk_user_flash port map (
    slow_clock => elk_PHI0,
    fast_clock => fast_clock,
    reset_n => sync_RESET(2),
    address => elk_A(13 downto 0), --debug_reg(5 downto 0) & elk_A(7 downto 0),
    en => '1',
    data_out => rom_zero_D
  );

  -- 16k synchronous block ram
  ram0: entity work.sideways_ram port map (
    clock => fast_clock,
    data => sideways_ram_data,
    address => sideways_ram_address,
    we => sideways_ram_we,
    q => sideways_ram_q
  );

  -- debug uart
  uart0: component uart
    generic map (
      -- divide_count => 712 -- 115.2 kHz (= 82MHz / 712)
      divide_count => 41 -- 2 MHz (= 82 MHz / 41)
      -- divide_count => 20 -- ~2 MHz with 41MHz clock
    )
    port map (
      clock => fast_clock,
      txd => uart_txd,
      tx_data => uart_tx_data,
      tx_empty => uart_tx_empty,
      transmit => uart_transmit
    );
  debug_uart_txd <= uart_txd;

  ext_uart_rx0: component uart_rx
    generic map (
      divide_count => 178 -- 115200 bps or so
    )
    port map (
      clock => fast_clock,
      rxd => ext_uart_rxd,
      rx_data => uart_rx_data,
      rx_full => uart_rx_full,
      ack => uart_rx_ack
    );

  ext_uart_tx0: component uart
    generic map (
      divide_count => 712 -- 115200 bps or so
    )
    port map (
      clock => fast_clock,
      txd => ext_uart_txd,
      tx_data => ext_uart_tx_data,
      tx_empty => ext_uart_tx_empty,
      transmit => ext_uart_tx_transmit
    );

  uart_fifo_inst : uart_fifo PORT MAP (
    clock  => fast_clock,

    empty  => uart_fifo_empty,
    full   => uart_fifo_full,

    data   => uart_fifo_input,
    wrreq  => uart_fifo_write_req,

    q      => uart_fifo_output,
    rdreq  => uart_fifo_read_req,

    usedw  => uart_fifo_usedw
  );

  -- generic debug pins

  -- debug_a <= uart_fifo_full;
  debug_a <= '1' when sampled_A(15 downto 4) = x"FCF" else '0';

  --debug_b <= capturing;
  --debug_b <= '1' when sampled_A(15 downto 8) = x"FE" else '0';
  debug_b <= '1' when elk_A(15 downto 4) = x"FCF" else '0';

  process (fast_clock)
  begin
    if rising_edge(fast_clock) then

      -- detect PHI0 rising and falling edge and capture data bus in time
      sync_PHI0 <= sync_PHI0(1 downto 0) & elk_PHI0;
      sync_A(2) <= sync_A(1);
      sync_A(1) <= sync_A(0);
      sync_A(0) <= elk_A;
      sync_D(2) <= sync_D(1);
      sync_D(1) <= sync_D(0);
      sync_D(0) <= elk_D;

      -- Sample 6502 address on rising PHI0 edge
      if sync_PHI0(2) = '0' and sync_PHI0(1) = '1' then
        sampled_A <= elk_A;
      end if;

      ---------------------------------------------------
      -- sideways ram, incl reading data from ext_uart --
      ---------------------------------------------------

      sideways_ram_rd <= '0';
      sideways_ram_rd2 <= '0';
      sideways_ram_we <= '0';
      uart_rx_ack <= '0';
      ext_uart_tx_transmit <= '0';

      -- latch byte from read started in previous clock cycle
      if sideways_ram_rd = '1' then
        sideways_ram_rd2 <= '1';
      end if;
      if sideways_ram_rd2 = '1' then
        sideways_ram_D <= sideways_ram_q;
      end if;

      -- rising PHI0
      if sync_PHI0(2) = '0' and sync_PHI0(1) = '1' then

        -- trigger read
        if accessing_sideways_ram = '1' then
          sideways_ram_address <= elk_A(13 downto 0);
          sideways_ram_rd <= '1';
        end if;

      -- falling PHI0
      elsif sync_PHI0(2) = '1' and sync_PHI0(1) = '0' then

        -- trigger write
        if accessing_sideways_ram = '1' and elk_RnW = '0' then
          sideways_ram_address <= sampled_A(13 downto 0);
          sideways_ram_we <= '1';
          sideways_ram_data <= elk_D;
        end if;

        -- reset RAM load address on writes to &FC90
        if elk_RnW = '0' and elk_A = x"FC90" then
          uart_rx_address <= (others => '0');
        end if;

      -- not on a clock edge: poll uart_rx_full
      elsif uart_rx_full = '1' and uart_rx_ack = '0' then

        -- write a byte from the uart into sideways ram
        sideways_ram_address <= std_logic_vector(uart_rx_address);
        uart_rx_address <= uart_rx_address + 1;
        sideways_ram_we <= '1';
        sideways_ram_data <= uart_rx_data;
        uart_rx_ack <= '1';

        -- send something out the debug uart too
        ext_uart_tx_data <= "00" & std_logic_vector(uart_rx_address) & uart_rx_data;
        ext_uart_tx_transmit <= '1';
      end if;

      -----------------------------------
      -- fifo-filling and uart-feeding --
      -----------------------------------

      -- default: don't send a byte to the uart
      uart_transmit <= '0';
      -- default: don't read or write fifo
      uart_fifo_read_req <= '0';
      uart_fifo_write_req <= '0';

      -- Capture data bus on falling PHI0 edge
      if sync_PHI0(2) = '1' and sync_PHI0(1) = '0' then

        -- start capture right after RESET
        sync_RESET <= sync_RESET(1 downto 0) & elk_nRESET;

        -- default: don't capture
        capturing <= '0';

        -- start capturing from an FExx access when the fifo is empty
        if uart_fifo_full = '0' and -- stop when fifo fills up
          (capturing = '1' -- continue if capturing
            or (sync_RESET(2) = '0' and sync_RESET(1) = '1')
            or (accessing_sideways_ram = '1' and uart_fifo_empty_sync = '1')
            -- or DEBUG = '1' -- one shot capture after DEBUG access
            -- or (sampled_A(15 downto 4) = x"FCF") -- capture any FCFx access
            or (sampled_A(15 downto 4) = x"FCF" and uart_fifo_empty_sync = '1') -- start condition
            -- or (sampled_A(15 downto 8) = x"FE" and uart_fifo_empty_sync = '1') -- start condition
          )
        then

          -- continue capturing until the fifo is full
          capturing <= '1'; -- comment this out to just capture accesses that match the start condition

          -- pass in A and D from just before the falling clock edge
          uart_fifo_input <= sync_A(2) & sync_D(2);
          uart_fifo_write_req <= '1';

          -- reset our counter and pass in a debug start word
          if capturing = '0' then
            n_words_sent_to_uart <= x"00000000";
            --uart_fifo_input <= x"123456";
          end if;
        end if;

      end if; -- falling PHI0 edge

      -- feed from fifo into uart
      uart_fifo_empty_sync <= uart_fifo_empty;
      if uart_tx_empty = '1' and uart_fifo_empty_sync = '0' and uart_transmit = '0' then
        if uart_fifo_read_req = '0' then
          -- request a byte from the fifo
          uart_fifo_read_req <= '1';
        else
          -- process byte from the fifo
          uart_tx_data <= uart_fifo_output;
          -- debug: output 16 bites from fifo and a counter word
          -- uart_tx_data <= std_logic_vector(n_words_sent_to_uart(7 downto 0)) & uart_fifo_output(23 downto 8);
          uart_transmit <= '1';
          n_words_sent_to_uart <= n_words_sent_to_uart + 1;
        end if;
      end if;

    end if; -- rising fast_clock edge
  end process;

end rtl;
