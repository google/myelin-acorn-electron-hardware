-- Copyright 2017 Google Inc.
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

entity master_updateable_megarom is
    Port (
        D : inout std_logic_vector(7 downto 0);
        bbc_A : in std_logic_vector(16 downto 0);
        bbc_nCS : in std_logic;
        flash_A : out std_logic_vector(18 downto 0);
        --flash_nCE : out std_logic;
        flash_nOE : out std_logic;
        flash_nWE : out std_logic;
        cpld_SCK : in std_logic;
        cpld_MOSI : in std_logic;
        cpld_SS : in std_logic;
        cpld_MISO : out std_logic;
        cpld_JP : in std_logic_vector(1 downto 0)
    );
end master_updateable_megarom;

architecture Behavioural of master_updateable_megarom is

    signal A : std_logic_vector(18 downto 0);
    signal Dout : std_logic_vector(7 downto 0);

    -- these two are set
    signal allowing_bbc_access : std_logic := '1';
    signal accessing_memory : std_logic := '0';
    signal rnw : std_logic := '0';

    -- SPI temp vars --
    -- the value clocked out of D<7> on the falling SCK edge
    signal last_d7 : std_logic := '0';
    signal last_mosi : std_logic := '0';
    -- flag to say if we're clocking through D/A/RnW or not (so we don't mess with them during the flash access period)
    signal clocking_spi_data : std_logic := '0';
    -- counts up to 50; need 6 bits
    signal spi_bit_count : unsigned(5 downto 0) := "000000";

begin

    -- We're either passing bbc_A through to flash_A, with D tristated, or we're
    -- controlling both and ignoring bbc_A.

    flash_A <= "00" & bbc_A when (allowing_bbc_access = '1') else A;
    -- assert OE
    flash_nOE <= '0' when (allowing_bbc_access = '1'
                           or (accessing_memory = '1' and rnw = '1')) else '1';
    -- leave flash enabled all the time (TODO maybe just enable when /OE or /WE is active)
    flash_nCE <= '0';
    -- assert WE and D when the BBC is disabled and we're doing a memory write
    flash_nWE <= '0' when (allowing_bbc_access = '0'
                           and (accessing_memory = '1' and rnw = '0')) else '1';
    -- drive D when writing
    D <= Dout when (allowing_bbc_access = '0'
                    and (accessing_memory = '1' and rnw = '0')) else "ZZZZZZZZ";

    -- MISO always gets the last thing we clocked out of Dout
    cpld_MISO <= last_d7;

    process (cpld_SS, cpld_SCK)
    begin
        if cpld_SS = '1' then
            clocking_spi_data <= '1';
            accessing_memory <= '0';
            spi_bit_count <= "000000";
        elsif rising_edge(cpld_SCK) then
            -- the master device should bring cpld_SS high between every transaction.
            -- to block out the BBC and enable flash access: send 32 bits of zeros.
            -- to reenable the BBC, send 32 bits of ones.
            -- message format: 17 address bits, rnw, 8 data bits, 6 zeros (32 bits total) then 8 clocks to retrieve data
            -- to get out of flash update mode, pass "000001" instead of the 6 zeros.  (the last bit gets copied into allowing_bbc_access.)

            -- we use the trailing zeros to perform the access to the flash chip.
            -- the flash chip only needs a 40ns low pulse on /CE + /WE, and its read access time is 55-70ns;
            -- there's another cycle time which is around 150ns also.
            -- if we want the same timings as on the bbc (250ns), that means we're OK with an SPI clock up to maybe 24 MHz.

            -- Example read, with RnW = 1:
            --  SCK ___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___/^^^\___
            -- MOSI X  D1  X   D0  X   0   X   0   X   0   X   0   X   0   X   0   X
            -- MISO                                                                X   D7  X   D6  X ...

            -- Because we have to clock D on falling edges, we're stuck doing that every time.

            -- TODO switch it around so the count increments on the falling edge,
            -- which lets us stop clocking as soon as we've got the last bit into D,
            -- and start our memory access a half-cycle after bit 26 is in

            if clocking_spi_data = '1' then
                last_mosi <= cpld_MOSI;
                A <= A(17 downto 0) & rnw;
                rnw <= last_d7;  -- change to use D(7) if we end up off by one here
            end if;

            -- stop clocking after the 26th bit, i.e. when count=25, and start again after bit 32
            if spi_bit_count = 25 then
                clocking_spi_data <= '0';
                accessing_memory <= '1';
            end if;
            if spi_bit_count = 32 then
                allowing_bbc_access <= cpld_MOSI;
                accessing_memory <= '0';
                clocking_spi_data <= '1';
            end if;

            spi_bit_count <= spi_bit_count + 1;
        end if;
    end process;

    process (cpld_SS, cpld_SCK)
    begin
        if cpld_SS = '1' then
        elsif falling_edge(cpld_SCK) then
            if clocking_spi_data = '1' then
                last_d7 <= Dout(7);
                Dout <= D(6 downto 0) & last_mosi;
            elsif accessing_memory = '1' and rnw = '1' then
                Dout <= D;
            end if;
        end if;
    end process;

end Behavioural;
