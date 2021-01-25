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

-- This implements a fast serial port with help from an AVR.  It also includes
-- some code from spi_sd_card.vhd to support MMFS (bit-banged SD card interface)
-- and UPURS (bit-banged serial)

entity serial_sd_adapter is
    Port (
        -- Pins that connect to the Electron bus

        elk_D : inout std_logic_vector(7 downto 0);

        elk_nINFC : in std_logic;
        elk_A7 : in std_logic;
        elk_A6 : in std_logic;
        elk_A5 : in std_logic;
        elk_A4 : in std_logic;
        elk_A2 : in std_logic;
        elk_A1 : in std_logic;
        elk_A0 : in std_logic;

        elk_nRST : in std_logic;
        elk_RnW : in std_logic;
        elk_PHI0 : in std_logic;

        -- Pins that would normally connect to the Raspberry Pi,
        -- but are repurposed here for SPI to the AVR, SPI to the
        -- SD card, and serial for UPURS.

        -- AVR interface: MISO, MOSI, SCK, /SS, INT.
        -- The first four are a standard SPI port, with the AVR as
        -- controller and CPLD as peripheral.  INT is an output from the CPLD
        -- that goes high when we have a byte to send to the AVR.
        --
        -- Future plans:
        --
        -- * Add a clock line so the AVR can provide a 2 or 4MHz clock
        --   to the CPLD.  4M/35 = 114.285kHz, which is probably within
        --   UPURS's acceptable range.  See below.

        -- SD interface: MISO, MOSI, SCK, /SS

        -- UPURS interface: RXD, TXD
        -- This mostly works for the UPURS suite of tools when attached
        -- to an AVR running upurs_usb_port.ino (in this repo), but
        -- is unreliable against HostFS:UPURS.  An interesting experiment
        -- might be to handle the serial port in the CPLD (with the AVR
        -- providing a 2MHz or 4MHz clock for timing).

        -- We could use the AVR's 64MHz PLL clock divided by 139, which
        -- would give us 115108 Hz * 4, i.e. just about perfect to drive
        -- the UART.  OC4A and /OC4A are PC6 (D5) and PC7 (D13).  See
        -- comments in serial_sd_mcu.ino for more detail.

        -- (Alternatively we can provide the entire serial port, ignore
        -- the rate entirely, and just clock a shift register when we get
        -- a read or write, but that wouldn't work with unmodified UPURS.)

        -- Pins without comments below are unused.

        tube_A0 : out std_logic; -- avr MISO
        tube_A1 : out std_logic; -- serial TXD
        tube_A2 : in std_logic; -- serial RXD

        tube_D : inout std_logic_vector(7 downto 0);
        -- D0 = sd MISO
        -- D1 = avr /SD_SS
        -- D2 = avr /SS  = /SD_SEL
        -- D3
        -- D4 = avr SCK
        -- D5 = sd /SS
        -- D6 = sd MOSI
        -- D7 = sd SCK

        tube_nRST : out std_logic; -- serial RTS
        tube_nTUBE : out std_logic; -- avr INT (1 when we want attention from the AVR)
        tube_RnW : in std_logic; -- avr MOSI
        tube_PHI0 : in std_logic
    );
end serial_sd_adapter;

architecture Behavioural of serial_sd_adapter is

    ---- Globals ----

    signal A_lower : std_logic_vector(7 downto 0);

    ---- Fast SPI port (peripheral, for AVR) ----

    signal avr_MOSI : std_logic; -- input from AVR
    signal avr_MISO : std_logic; -- output to AVR
    signal avr_SCK : std_logic; -- input from AVR
    signal avr_nSS : std_logic; -- input from AVR
    signal avr_INT : std_logic; -- output to AVR
    signal avr_nSD_SEL : std_logic; -- input from AVR

    signal nAVR_SPI : std_logic; -- '0' when A = &FCA0;
    signal nAVR_SPI_STATUS : std_logic; -- '0' when A = &FCA1;

    -- we use a toggle synchronizer to know if the buffer is full or empty.
    -- RECEPTION FROM AVR TO CPLD+ELK:
    -- on the avr side, it's safe to receive a byte if avr_RXD_state = elk_RXD_state_sync
    -- on the elk side, it's safe to read a byte if elk_RXD_state != avr_RXD_state_sync
    -- we just use a single flip flop to synchronize in each case, because there's always
    -- a longish settling time.
    -- TRANSMISSION FROM ELK+CPLD TO AVR:
    -- it's safe to accept a byte from the elk for transmission if elk_TXD_state == avr_TXD_state_sync
    -- it's safe to transmit a byte to the avr if avr_TXD_state != elk_TXD_state_sync

    signal avr_RXD_state : std_logic := '0'; -- toggles whenever the CPLD receives a byte from the AVR
    signal avr_RXD_state_sync : std_logic := '0'; -- avr_RXD_state synchronized to elk_PHI0
    signal elk_RXD_state : std_logic := '0'; -- toggles when the elk reads a byte
    signal elk_RXD_state_sync : std_logic := '0'; -- elk_RXD_state synchronized to avr_SCK

    signal avr_TXD_state : std_logic := '0'; -- toggles whenever the CPLD sends a byte to the AVR
    signal avr_TXD_state_sync : std_logic := '0'; -- avr_TXD_state synchronized to elk_PHI0
    signal elk_TXD_state : std_logic := '0'; -- toggles when the elk writes a byte
    signal elk_TXD_state_sync : std_logic := '0'; -- elk_TXD_state synchronized to avr_SCK

    signal avr_RXD : std_logic_vector(7 downto 0); -- byte received from AVR
    signal avr_TXD : std_logic_vector(7 downto 0); -- next byte to transmit / being transmitted to AVR

    -- signals used during an SPI transaction
    signal avr_spi_SHIFT : std_logic_vector(7 downto 0); -- SPI shift register
    signal avr_spi_bit_count : std_logic_vector(3 downto 0); -- SPI bit counter for transfers
    signal avr_spi_receiving : std_logic := '0'; -- copy bits into avr_RXD and toggle avr_RXD_state when done
    signal avr_spi_transmitting : std_logic := '0'; -- toggle avr_TXD_state when done

    ---- Serial port ----

    signal TXD : std_logic := '1'; -- output from CPLD/Electron
    signal RXD : std_logic; -- input to CPLD/Electron
    signal RTS : std_logic := '1'; -- request for data from PC
    signal CTS : std_logic; -- PC is allowing us to send
    signal invert_serial : std_logic := '0'; -- invert serial port for UPURS

    -- chip selects
    signal nSERIAL_IO : std_logic; -- '0' when A = &FCB1

    ---- SPI (controller, for SD card) ---

    signal MOSI : std_logic := '1';
    signal MISO : std_logic;
    signal SCK : std_logic := '1';
    signal nSS : std_logic := '0';

    ---- Plus 1 workalike registers ----

    -- chip selects
    signal nDATA : std_logic; -- '0' when A = &FC71
    signal nSTATUS : std_logic; -- '0' when A = &FC72

begin

    -- mappings to actual pins

    avr_MOSI <= tube_RnW;
    tube_A0 <= 'Z' when avr_nSS = '1' else
        MISO when avr_nSD_SEL = '0' else
        avr_MISO;
    avr_SCK <= tube_D(4);
    avr_nSS <= tube_D(2);
    avr_nSD_SEL <= tube_D(2);
    tube_nTUBE <= avr_INT;

    tube_D(5) <= avr_nSS when avr_nSD_SEL = '0' else nSS;
    tube_D(6) <= avr_MOSI when avr_nSD_SEL = '0' else MOSI;
    tube_D(7) <= avr_SCK when avr_nSD_SEL = '0' else SCK;
    MISO <= tube_D(0);

    tube_A1 <= TXD; -- tx output
    RXD <= tube_A2; -- rx input
    tube_nRST <= RTS; -- permit remote station to send when RTS=1
    CTS <= '1'; -- assume we can always send to the remote station

    -- address comparison convenience (note missing A3 in elk_pi_tube_direct r1)
    A_lower <= elk_A7 & elk_A6 & elk_A5 & elk_A4 & '0' & elk_A2 & elk_A1 & elk_A0;

    ---- Fast SPI peripheral for AVR ---

    nAVR_SPI <= '0' when (elk_nINFC = '0' and A_lower = x"A0") else '1';
    nAVR_SPI_STATUS <= '0' when (elk_nINFC = '0' and A_lower = x"A1") else '1';

    avr_INT <= '1' when (elk_TXD_state /= avr_TXD_state_sync) else '0';

    ---- Bit-banged serial port for UPURS ---

    nSERIAL_IO <= '0' when (elk_nINFC = '0' and A_lower = x"B1") else '1';

    ---- Plus 1 parallel port emulation ----

    nDATA <= '0' when (elk_nINFC = '0' and A_lower = x"71") else '1';
    nSTATUS <= '0' when (elk_nINFC = '0' and A_lower = x"72") else '1';

    ---- Data bus ----

    elk_D <=
        -- AVR SPI data
        avr_RXD when (nAVR_SPI = '0' and elk_RnW = '1') else
        -- AVR SPI status
        "000000" & (elk_TXD_state xnor avr_TXD_state_sync) & (elk_RXD_state xor avr_RXD_state_sync)
            when (nAVR_SPI_STATUS = '0' and elk_RnW = '1') else
        -- Serial port
        (RXD xor invert_serial) & "11111" & CTS & "1" when (nSERIAL_IO = '0' and elk_RnW = '1') else
        -- Plus 1 parallel port
        MISO & "0000000" when (nSTATUS = '0' and elk_RnW = '1') else
        -- default
        "ZZZZZZZZ";

    -- AVR SPI clock domain
    process (avr_nSS, avr_SCK)
    begin

        -- RISING EDGE of avr_SCK: read avr_MOSI
        if avr_nSS = '1' then

            -- asynchronous reset (must not happen on an avr_SCK edge)
            avr_spi_bit_count <= x"0";

        elsif rising_edge(avr_SCK) then

            -- increment the count each time
            avr_spi_bit_count <= std_logic_vector(unsigned(avr_spi_bit_count) + 1);

            -- clock in a bit, depending on avr_spi_bit_count
            if avr_spi_bit_count = x"0" then
                -- synchronize elk_RXD_state and elk_TXD_state
                elk_RXD_state_sync <= elk_RXD_state;
                elk_TXD_state_sync <= elk_TXD_state;
            elsif avr_spi_bit_count = x"6" then
                -- SPI is big-endian, so we want to ignore incoming bits 0-5.
                -- bit 6 (1) tells us if the remote wants to send a byte
                avr_spi_receiving <= (
                    avr_MOSI -- '1' if the remote has a byte for us
                    and (avr_RXD_state xnor elk_RXD_state_sync) -- '1' if we have room in our buffer
                );
            elsif avr_spi_bit_count = x"7" then
                -- bit 7 (0) tells us if the remote is capable of receiving a byte
                avr_spi_transmitting <= (
                    avr_MOSI -- '1' if the remote has buffer space
                    and (avr_TXD_state xor elk_TXD_state_sync) -- '1' if we have a byte to transmit
                );
                -- copy avr_TXD into the shift register if it's safe
                if avr_TXD_state /= elk_TXD_state_sync then
                    avr_spi_SHIFT <= avr_TXD;
                end if;
            elsif avr_spi_bit_count(3) = '1' then
                -- clock in a bit if we have buffer space
                avr_spi_SHIFT <= avr_spi_SHIFT(6 downto 0) & avr_MOSI;
                if avr_spi_bit_count = x"F" then
                    if avr_spi_receiving = '1' then
                        avr_RXD_state <= not avr_RXD_state;
                        avr_RXD <= avr_spi_SHIFT(6 downto 0) & avr_MOSI;
                    end if;
                    if avr_spi_transmitting = '1' then
                        avr_TXD_state <= not avr_TXD_state;
                    end if;
                end if;
            end if;

        end if;

        -- FALLING EDGE of avr_SCK: write avr_MISO
        if avr_nSS = '1' then

        elsif falling_edge(avr_SCK) then

            -- We always update MISO on an avr_SCK falling edge.

            if avr_spi_bit_count = x"6" then
                -- '1' if we have a byte to send to the AVR
                avr_MISO <= avr_TXD_state xor elk_TXD_state_sync;
            elsif avr_spi_bit_count = x"7" then
                -- '1' if we can accept a byte from the AVR
                avr_MISO <= avr_RXD_state xnor elk_RXD_state_sync;
            elsif avr_spi_bit_count(3) = '1' then
                avr_MISO <= avr_spi_SHIFT(7);
            end if;
        end if;

    end process;

    -- Electron clock domain
    process (elk_PHI0)
    begin
        if falling_edge(elk_PHI0) then
            -- AVR SPI registers
            avr_RXD_state_sync <= avr_RXD_state;
            avr_TXD_state_sync <= avr_TXD_state;
            if nAVR_SPI = '0' and elk_RnW = '0' and elk_TXD_state = avr_TXD_state_sync then
                -- we're writing to the TXD register
                avr_TXD <= elk_D;
                elk_TXD_state <= not elk_TXD_state;
            end if;
            if nAVR_SPI = '0' and elk_RnW = '1' and elk_RXD_state /= avr_RXD_state_sync then
                -- the electron just read avr_RXD
                elk_RXD_state <= not elk_RXD_state;
            end if;
            if nAVR_SPI_STATUS = '0' and elk_RnW = '0' then
                -- we never write to the status register
            end if;

            -- Serial port: Electron is writing RTS and TXD bits
            if nSERIAL_IO = '0' and elk_RnW = '0' then
                RTS <= elk_D(6);
                TXD <= elk_D(0) xor invert_serial;
            end if;

            -- Bit-banged SPI
            if nDATA = '0' and elk_RnW = '0' then
                -- handle write to &FC71
                MOSI <= elk_D(0);
                SCK <= elk_D(1);
            end if;
        end if;
    end process;

end Behavioural;
