-- Copyright 2019 Google LLC
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

entity MGC is
    generic (
        -- Base resource usage: 26MC

        -- Include shift-register based (as well as bit banged) SPI (adds ~20MC)
        -- = 8 bit shifter, 4 bit counter, 1 bit spi_start, 1 bit spi_bit_bang_mode
        IncludeSPIShifter : boolean := true;
        -- Clock the SPI port with CLK16MHz (adds ~8 MC)
        UseFastClockForSPI : boolean := false
    );
    port (
        -- Inputs from the cartridge interface
        PHI : in std_logic;
        CLK16MHz : in std_logic;
        nRESET : in std_logic;
        nPGFC : in std_logic;  -- Low when &FCxx is selected
        QA : in std_logic;  -- Upper/lower bank select
        A : in std_logic_vector(7 downto 0);
        D : inout std_logic_vector(7 downto 0);
        nMASDET : in std_logic;  -- Low on Master, high on Electron

        -- In the Electron Plus 1, Pin A2 is called nOE2 or nOE4 depending
        -- which cartridge slot is in use.  The Plus 1's logic driving nOE2
        -- is:

        -- nOE2 <= not (A15 and not A14
        --              and not FE05(3) and not FE05(2) and FE05(1));

        -- i.e. nOE2 is low when the 6502 is reading or writing the sideways
        -- area and the cartridge is selected.

        -- In the Master 128, Pin A2 is driven by AT13 (IC20 pin 17) or AT15
        -- (IC20 pin 15), which are outputs from the memory controller IC. 
        -- TODO scope this to see how it behaves.
        nOE : in std_logic;  -- Pin A2

        -- Electron: CPU RnW line
        -- Master: AA15 line; IC20 pin 19
        ERnW_MCS : in std_logic;  -- Pin A4

        -- Electron: CPU READY line
        -- Master: BRnW line
        ERDY_MRnW : in std_logic;  -- Pin A11

        -- Power-on reset; low for ~1ms on startup        
        nPWRRST : in std_logic;

        -- Outputs to ROM and RAM chip
        RR_nWE : out std_logic;
        RR_nOE : out std_logic;
        ROM_nCE : out std_logic;
        RAM_nCE : out std_logic;

        -- SPI port
        SD_CS1 : out std_logic := '1';
        SD_CS2 : out std_logic := '1';
        -- SD_CS2 : in std_logic;  -- Disabled as cartridge has CLK16MHz linked in there
        SD_SCK : out std_logic;
        SD_MOSI : out std_logic;
        SD_MISO : in std_logic
    );
end;

architecture rtl of MGC is

    signal nRESET_sync : std_logic;

    -- High to map ROM into the bank, low to map RAM
    signal lower_bank_rom_nram : std_logic := '1';
    signal upper_bank_rom_nram : std_logic := '1';

    signal lower_rom_unlocked : std_logic := '0';
    signal upper_rom_unlocked : std_logic := '0';

    signal inhibit_reset : std_logic := '0';

    signal spi_shift_register_phi : std_logic_vector(7 downto 0) := (others => '0');
    signal spi_shift_register_16 : std_logic_vector(7 downto 0) := (others => '0');
    signal spi_start : std_logic := '0';
    signal spi_start_16 : std_logic := '0';
    signal last_spi_start_16 : std_logic := '0';
    signal spi_counter_phi : std_logic_vector(3 downto 0) := (others => '1');
    signal spi_counter_16 : std_logic_vector(3 downto 0) := (others => '1');
    signal spi_bit_bang_mode : std_logic := '1';
    signal spi_bit_bang_MOSI : std_logic := '1';
    signal spi_bit_bang_SCK : std_logic := '0';

    signal spi_fast_SCK : std_logic := '0';
    signal spi_fast_MOSI : std_logic := '0';

    signal RnW : std_logic;

begin

    -- DEBUG
    -- SD_CS2 <= spi_bit_bang_MOSI;
    -- SD_CS2 <= spi_bit_bang_SCK;
    -- SD_CS2 <= nPGFC;
    -- SD_CS2 <= '1' when nPGFC = '0' and PHI = '1' and RnW = '0' else '0';  -- writing to &FCxx
    -- SD_CS2 <= D(1);

    -- Derive RnW signal
    RnW <= ERnW_MCS when nMASDET = '1' else ERDY_MRnW;

    -- ROM/RAM output enable
    RR_nOE <= '0' when
        nOE = '0'      -- cartridge selected
        and RnW = '1'  -- cpu is reading
        else '1';

    -- ROM/RAM write strobe
    -- /WE is also gated with the high clock period, as D isn't held for 
    -- long past the falling edge.  It should go low when PHI0 is high and
    -- RnW is low.
    RR_nWE <= '0' when 
        nOE = '0'   -- cartridge selected
        and RnW = '0'  -- cpu is writing
        and PHI = '1'  -- high clock period
        and ((QA = '0' and lower_rom_unlocked = '1')      -- lower bank unlocked
             or (QA = '1' and upper_rom_unlocked = '1'))  -- upper bank unlocked
        else '1';

    -- ROM chip select
    ROM_nCE <= '0' when
        nOE = '0'  -- cartridge selected
        and ((QA = '0' and lower_bank_rom_nram = '1')      -- lower bank is ROM
             or (QA = '1' and upper_bank_rom_nram = '1'))  -- upper bank is ROM
        else '1';

    -- RAM chip select
    RAM_nCE <= '0' when
        nOE = '0'  -- cartridge selected
        and ((QA = '0' and lower_bank_rom_nram = '0')      -- lower bank is RAM
             or (QA = '1' and upper_bank_rom_nram = '0'))  -- upper bank is RAM
        else '1';

    -- Handle reads from registers
    D <=
        -- Never drive the bus for CPU writes
        "ZZZZZZZZ" when RnW = '0'
        -- Read machine type
        else "0000000" & nMASDET when nPGFC = '0' and A = x"D2"
        -- Read shift register
        else spi_shift_register_phi when nPGFC = '0' and A = x"D4" and IncludeSPIShifter and not UseFastClockForSPI
        else spi_shift_register_16 when nPGFC = '0' and A = x"D4" and IncludeSPIShifter and UseFastClockForSPI
        -- Read MISO
        else SD_MISO & "00000" & spi_bit_bang_SCK & spi_bit_bang_MOSI when nPGFC = '0' and A = x"D8"
        -- Catchall
        else "ZZZZZZZZ";

    -- Multiplex fast and bitbang SPI
    SD_SCK <= spi_bit_bang_SCK when (spi_bit_bang_mode = '1' or not UseFastClockForSPI) else spi_fast_SCK;
    SD_MOSI <= spi_bit_bang_MOSI when (spi_bit_bang_mode = '1' or not UseFastClockForSPI) else spi_fast_MOSI;

    -- CPU clock process
    elk_clock_process : process(PHI)
    begin
        if falling_edge(PHI) then
            -- Synchronize external reset
            nRESET_sync <= nRESET;

            -- Reset all one pulse outputs
            spi_start <= '0';

            -- Handle writes to registers
            if nPGFC = '0' and A = x"D0" then
                lower_bank_rom_nram <= not RnW;  -- TODO did I get this right?  reading sets it to ram?
            end if;
            if nPGFC = '0' and A = x"D1" then
                upper_bank_rom_nram <= not RnW;  -- TODO did I get this right?  reading sets it to ram?
            end if;
            if RnW = '0' then
                if nPGFC = '0' and A = x"D3" then
                    inhibit_reset <= '1';
                end if;
                if nPGFC = '0' and A = x"D4" and IncludeSPIShifter then
                    -- Copy D into load register and trigger SPI
                    if UseFastClockForSPI then
                        -- Pass contents of D over to CLK16MHz process
                        spi_shift_register_phi <= D;
                        spi_start <= '1';
                        spi_bit_bang_mode <= '0';  -- Output 16MHz SPI registers
                    else
                        -- Start shifting immediately; shifter is running off PHI
                        spi_counter_phi <= "0000";
                        -- initialize MOSI with the MSB right now, and update it on the falling
                        -- edge of spi_fast_SCK.
                        spi_bit_bang_MOSI <= spi_shift_register_phi(7);
                    end if;
                end if;
                if nPGFC = '0' and A = x"D8" then
                    spi_bit_bang_MOSI <= D(0);
                    spi_bit_bang_SCK <= D(1);
                end if;
                if nPGFC = '0' and A = x"D9" then
                    SD_CS1 <= D(0);
                    -- SD_CS2 <= D(1);
                    spi_bit_bang_mode <= '1';
                end if;
                if nPGFC = '0' and A = x"DC" then
                    lower_rom_unlocked <= '1';
                end if;
                if nPGFC = '0' and A = x"DD" then
                    lower_rom_unlocked <= '0';
                end if;
                if nPGFC = '0' and A = x"DE" then
                    upper_rom_unlocked <= '1';
                end if;
                if nPGFC = '0' and A = x"DF" then
                    upper_rom_unlocked <= '0';
                end if;
            end if;
            if nRESET_sync = '0' then
                inhibit_reset <= '0';
                lower_bank_rom_nram <= '1';
                upper_bank_rom_nram <= '1';
                lower_rom_unlocked <= '0';
                upper_rom_unlocked <= '0';
            end if;

            -- 1-2 MHz SPI
            if IncludeSPIShifter and not UseFastClockForSPI then
                if spi_counter_phi(3) = '0' then
                    -- spi active!
                    if spi_bit_bang_SCK = '0' then
                        spi_bit_bang_SCK <= '1';
                        spi_shift_register_phi <= spi_shift_register_phi(6 downto 0) & SD_MISO;
                    else
                        spi_bit_bang_SCK <= '0';
                        spi_bit_bang_MOSI <= spi_shift_register_phi(7);
                        spi_counter_phi <= std_logic_vector(unsigned(spi_counter_phi) + 1);
                    end if;
                end if;
            end if;
        end if;
    end process;

    -- High speed (16MHz on Electron, 8MHz on Master) clock process
    fast_clock_process : process(CLK16MHZ)
    begin
        if rising_edge(CLK16MHZ) then

            if IncludeSPIShifter and UseFastClockForSPI then
                -- Synchronize spi_start
                last_spi_start_16 <= spi_start_16;
                spi_start_16 <= spi_start;

                if spi_start_16 = '1' and last_spi_start_16 = '0' then
                    -- start spi transaction
                    spi_counter_16 <= "0000";
                    -- initialize MOSI with the MSB right now, and update it on the falling
                    -- edge of spi_fast_SCK.
                    spi_fast_MOSI <= spi_shift_register_phi(7);
                    spi_shift_register_16 <= spi_shift_register_phi;
                end if;

                if spi_counter_16(3) = '0' then
                    -- spi active!
                    if spi_fast_SCK = '0' then
                        spi_fast_SCK <= '1';
                        spi_shift_register_16 <= spi_shift_register_16(6 downto 0) & SD_MISO;
                    else
                        spi_fast_SCK <= '0';
                        spi_fast_MOSI <= spi_shift_register_16(7);
                        spi_counter_16 <= std_logic_vector(unsigned(spi_counter_16) + 1);
                    end if;
                end if;
            end if;
        end if;
    end process;

end rtl;
