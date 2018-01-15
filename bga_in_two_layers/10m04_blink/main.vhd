library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity blink_10m04 is
  Port (
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
    c1_18 : inout std_logic;
    c1_19 : inout std_logic;
    c1_20 : inout std_logic;
    c1_22 : inout std_logic;
    c1_23 : inout std_logic;
    c1_24 : inout std_logic;
    c1_25 : inout std_logic;
    c1_26 : inout std_logic;
    c1_27 : inout std_logic;
    c1_28 : inout std_logic;
    c1_29 : inout std_logic;
    c1_30 : inout std_logic;
    c1_31 : inout std_logic;
    c1_33 : inout std_logic;
    c1_34 : inout std_logic;
    c1_36 : inout std_logic;
    c1_37 : inout std_logic;
    c1_38 : inout std_logic;
	 
    c2_1 : inout std_logic;
    c2_3 : inout std_logic;
    c2_4 : inout std_logic;
    c2_5 : inout std_logic;
    c2_8 : inout std_logic;
    c2_12 : inout std_logic;

    c3_1 : inout std_logic;
    c3_2_CLK3n : inout std_logic;
    c3_3 : inout std_logic;
    c3_4 : inout std_logic;
    c3_5_CLK3p : inout std_logic;
    c3_6 : inout std_logic;
    c3_7 : inout std_logic;
    c3_8 : inout std_logic;
    c3_9 : inout std_logic;
    c3_10 : inout std_logic;
    c3_11 : inout std_logic;
    c3_12 : inout std_logic;

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
    c4_28 : inout std_logic;
    c4_30 : inout std_logic;
    c4_31 : inout std_logic;
    c4_32 : inout std_logic;
    c4_33 : inout std_logic;
    c4_34 : inout std_logic;
    c4_35 : inout std_logic;
    c4_36 : inout std_logic;
    c4_37 : inout std_logic;
    c4_38 : inout std_logic;
    c4_39 : inout std_logic;
    c4_40 : inout std_logic
  );
end blink_10m04;

architecture rtl of blink_10m04 is

	component internal_osc is
		port (
			oscena : in  std_logic := 'X'; -- oscena
			clkout : out std_logic         -- clk
		);
	end component internal_osc;

	signal clk : std_logic;  -- 55-115MHz clock from internal oscillator
	signal clk_div_count : std_logic_vector(26 downto 0) := (others => '0');
	signal slow_clk : std_logic;  -- clk/(128*1024*1024), 0.4-0.85 Hz
	
begin

    osc0 : component internal_osc
        port map (
            oscena => '1',
            clkout => clk
        );

    process (clk)
    begin
        if rising_edge(clk) then
            clk_div_count <= std_logic_vector(unsigned(clk_div_count) + 1);
            if unsigned(clk_div_count) = 0 then
                slow_clk <= not slow_clk;
            end if;
        end if;
    end process;

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
    c1_18 <= slow_clk;
    c1_19 <= 'Z';  -- poor solder connection, tristate so we can patch
    c1_20 <= slow_clk;
    c1_22 <= slow_clk;
    c1_23 <= slow_clk;
    c1_24 <= slow_clk;
    c1_25 <= slow_clk;
    c1_26 <= slow_clk;
    c1_27 <= slow_clk;
    c1_28 <= slow_clk;
    c1_29 <= slow_clk;
    c1_30 <= slow_clk;
    c1_31 <= slow_clk;
    c1_33 <= slow_clk;
    c1_34 <= slow_clk;
    c1_36 <= slow_clk;
    c1_37 <= slow_clk;
    c1_38 <= slow_clk;
	 
    c2_1 <= slow_clk;
    c2_3 <= slow_clk;
    c2_4 <= slow_clk;
    c2_5 <= slow_clk;
    c2_8 <= slow_clk;
    c2_12 <= slow_clk;

    c3_1 <= slow_clk;
    c3_2_CLK3n <= slow_clk;
    c3_3 <= slow_clk;
    c3_4 <= slow_clk;
    c3_5_CLK3p <= slow_clk;
    c3_6 <= slow_clk;
    c3_7 <= slow_clk;
    c3_8 <= slow_clk;
    c3_9 <= slow_clk;
    c3_10 <= slow_clk;
    c3_11 <= slow_clk;
    c3_12 <= slow_clk;

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
    c4_28 <= 'Z';  -- poor solder connection, tristate so we can patch
    c4_30 <= slow_clk;
    c4_31 <= slow_clk;
    c4_32 <= slow_clk;
    c4_33 <= slow_clk;
    c4_34 <= slow_clk;
    c4_35 <= slow_clk;
    c4_36 <= slow_clk;
    c4_37 <= slow_clk;
    c4_38 <= slow_clk;
    c4_39 <= 'Z';  -- poor solder connection, tristate so we can patch
    c4_40 <= slow_clk;
	
end rtl;

