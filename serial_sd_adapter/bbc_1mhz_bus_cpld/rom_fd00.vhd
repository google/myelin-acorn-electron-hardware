library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- (Up to) 256 bytes of ROM
entity RomFD00 is
    port (
        A : in std_logic_vector(7 downto 0);
        D : out std_logic_vector(7 downto 0)
    );
end;

architecture Behavioural of RomFD00 is

begin

    process(A)
    begin
        case A is
          -- These are all dummy values for now; to be replaced with actual
          -- data later
          when x"00" => D <= x"12";
          when x"01" => D <= x"d7";
          when x"02" => D <= x"9f";
          when x"03" => D <= x"6c";
          when x"04" => D <= x"2a";
          when x"05" => D <= x"42";
          when x"06" => D <= x"ff";
          when x"07" => D <= x"99";
          when x"08" => D <= x"ca";
          when x"09" => D <= x"d5";
          when x"0a" => D <= x"a7";
          when x"0b" => D <= x"46";
          when x"0c" => D <= x"87";
          when x"0d" => D <= x"a2";
          when x"0e" => D <= x"b7";
          when x"0f" => D <= x"dd";
          when x"10" => D <= x"92";
          when x"11" => D <= x"f7";
          when x"12" => D <= x"44";
          when x"13" => D <= x"c3";
          when x"14" => D <= x"16";
          when x"15" => D <= x"7a";
          when x"16" => D <= x"ec";
          when x"17" => D <= x"5d";
          --when x"18" => D <= x"d9";
          --when x"19" => D <= x"a2";
          --when x"1a" => D <= x"f3";
          --when x"1b" => D <= x"0a";
          --when x"1c" => D <= x"2c";
          --when x"1d" => D <= x"87";
          --when x"1e" => D <= x"3e";
          --when x"1f" => D <= x"44";
          when x"fe" => D <= x"00";
          when x"ff" => D <= x"fd";
          when others => D <= "--------";
        end case;
    end process;

end Behavioural;
