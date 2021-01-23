BOARD_TAG = leonardo
ARDUINO_LIBS = libxsvf
USER_LIB_PATH = ./src

# Copy libxsvf into libraries/libxsvf before the rest of the script executes
$(info $(shell ./prepare_libraries.sh))

include ../../third_party/Arduino-Makefile/Arduino.mk
