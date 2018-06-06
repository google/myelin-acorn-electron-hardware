library IEEE;
use IEEE.std_logic_1164.all;

-- Simple send-only UART

entity uart is
  generic (
    divide_count : integer
  );
  port (
    clock : in std_logic;  -- main clock
    txd : out std_logic := '1';
    tx_data : in std_logic_vector(7 downto 0);
    tx_empty : out std_logic; -- '1' when tx_data can take a new byte
    transmit : in std_logic -- pulse '1' when tx_data is valid
  );
end uart;

architecture rtl of uart is

  signal divider : integer := 0;
  signal shifter : std_logic_vector(8 downto 0);
  signal shift_count : integer range 0 to 10 := 0;
  signal tx_empty_int : std_logic := '1';

begin
  tx_empty_int <= '1' when shift_count = 0 else '0';
  tx_empty <= tx_empty_int;

  process (clock)
  begin
    if rising_edge(clock) then

      -- transmit a bit on divider expiry
      if divider = 0 and shift_count /= 0 then
        txd <= shifter(0);
        shifter <= '1' & shifter(8 downto 1);
        shift_count <= shift_count - 1;
      end if;

      -- accept a new byte to send
      if tx_empty_int = '1' and transmit = '1' then
        shifter <= tx_data & '0';
        shift_count <= 10;
      end if;

      -- divider divides clock down to the serial bit rate (x 4 for reception?)
      if divider = divide_count then
        divider <= 0;
      else
        divider <= divider + 1;
      end if;

    end if;
  end process;

end rtl;
