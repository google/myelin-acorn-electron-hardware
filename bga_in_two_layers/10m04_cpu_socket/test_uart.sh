set -uex

iverilog -o uart_rx_tb.vvp uart_rx_tb.v
vvp uart_rx_tb.vvp
open -a Scansion uart_rx_tb.vcd