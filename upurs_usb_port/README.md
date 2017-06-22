This is an Arduino sketch, to be run on a Pro Micro board, that turns it into
a USB serial adapter for UPURS.  Unfortunately the closest hardware baud rates
possible to the 115200 that UPURS expects are 111111 and 117647; we use the
latter here, which only works if you modify your UPURS ROM.
