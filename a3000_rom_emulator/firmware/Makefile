BOARD_TAG = adafruit_circuitplayground_m0
ARDUINO_LIBS = libxsvf SPI
USER_LIB_PATH = ./libraries

# OPTIMIZATION_LEVEL = 2

# Copy libxsvf into libraries/libxsvf before the rest of the script executes
$(info $(shell ./prepare_libraries.sh))

include ../../third_party/Arduino-Makefile/Sam.mk
