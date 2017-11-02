EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:scarab_mini_spartan_6_lx25
LIBS:acorn-electron-expansion-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 4300 1300 0    60   ~ 0
18VAC
Text Label 3800 1300 2    60   ~ 0
18VAC
Text Label 4300 1400 0    60   ~ 0
AC_RETURN
Text Label 3800 1400 2    60   ~ 0
AC_RETURN
Text Label 4300 1500 0    60   ~ 0
-5V
Text Label 3800 1500 2    60   ~ 0
-5V
Text Label 4300 1600 0    60   ~ 0
GND
Text Label 3800 1600 2    60   ~ 0
GND
Text Label 4300 1700 0    60   ~ 0
5V
Text Label 3800 1700 2    60   ~ 0
5V
Text Label 4300 1800 0    60   ~ 0
SOUND_OUT
Text Label 3800 1800 2    60   ~ 0
16MHZ
Text Label 3800 1900 2    60   ~ 0
PHI0
Text Label 3800 2000 2    60   ~ 0
nNMI
Text Label 3800 2100 2    60   ~ 0
RnW
Text Label 3800 2200 2    60   ~ 0
D6
Text Label 3800 2300 2    60   ~ 0
D4
Text Label 3800 2400 2    60   ~ 0
D2
Text Label 3800 2500 2    60   ~ 0
D0
NoConn ~ 3800 2600
Text Label 3800 2700 2    60   ~ 0
A14
Text Label 3800 2800 2    60   ~ 0
A12
Text Label 3800 2900 2    60   ~ 0
A10
Text Label 3800 3400 2    60   ~ 0
A8
Text Label 3800 3300 2    60   ~ 0
A6
Text Label 3800 3200 2    60   ~ 0
A4
Text Label 3800 3000 2    60   ~ 0
A0
Text Label 3800 3100 2    60   ~ 0
A2
Text Label 3800 3500 2    60   ~ 0
GND
Text Label 3800 3600 2    60   ~ 0
5V
Text Label 4300 3600 0    60   ~ 0
5V
Text Label 4300 3500 0    60   ~ 0
GND
Text Label 4300 2700 0    60   ~ 0
A15
Text Label 4300 2800 0    60   ~ 0
A13
Text Label 4300 2900 0    60   ~ 0
A11
Text Label 4300 3000 0    60   ~ 0
A9
Text Label 4300 3100 0    60   ~ 0
A1
Text Label 4300 3200 0    60   ~ 0
A3
Text Label 4300 3300 0    60   ~ 0
A5
Text Label 4300 3400 0    60   ~ 0
A7
Text Label 4300 1900 0    60   ~ 0
nRST
Text Label 4300 2100 0    60   ~ 0
nIRQ
Text Label 4300 2200 0    60   ~ 0
D7
Text Label 4300 2300 0    60   ~ 0
D5
Text Label 4300 2400 0    60   ~ 0
D3
Text Label 4300 2500 0    60   ~ 0
D1
Text Label 4300 2600 0    60   ~ 0
RDY
Text Label 4300 2000 0    60   ~ 0
16MHZ_DIV13
$Comp
L 74HCT245 U2
U 1 1 58D0B9FE
P 6300 1750
F 0 "U2" H 6300 2250 60  0000 C CNN
F 1 "74LVC245 D0-7" V 6300 1750 60  0000 C CNN
F 2 "Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm" H 6300 1050 60  0001 C CNN
F 3 "" H 6300 1750 60  0000 C CNN
	1    6300 1750
	1    0    0    -1  
$EndComp
Text Label 5600 1250 2    60   ~ 0
D0
Text Label 5600 1450 2    60   ~ 0
D2
Text Label 5600 1650 2    60   ~ 0
D4
Text Label 5600 1850 2    60   ~ 0
D6
Text Label 5600 1950 2    60   ~ 0
D7
Text Label 5600 1350 2    60   ~ 0
D1
Text Label 5600 1550 2    60   ~ 0
D3
Text Label 5600 1750 2    60   ~ 0
D5
$Comp
L 74HCT245 U3
U 1 1 58D0BB02
P 6300 3000
F 0 "U3" H 6300 3500 60  0000 C CNN
F 1 "74LVC245 A0-7" V 6300 3000 60  0000 C CNN
F 2 "Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm" H 6300 2300 60  0001 C CNN
F 3 "" H 6300 3000 60  0000 C CNN
	1    6300 3000
	1    0    0    -1  
$EndComp
$Comp
L 74HCT245 U4
U 1 1 58D0BB33
P 6300 4250
F 0 "U4" H 6300 4750 60  0000 C CNN
F 1 "74LVC245 A8-15" V 6300 4250 60  0000 C CNN
F 2 "Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm" H 6300 3550 60  0001 C CNN
F 3 "" H 6300 4250 60  0000 C CNN
	1    6300 4250
	1    0    0    -1  
$EndComp
$Comp
L 74HCT245 U5
U 1 1 58D0BB70
P 6300 5500
F 0 "U5" H 6300 6000 60  0000 C CNN
F 1 "74LVC245" V 6300 5500 60  0000 C CNN
F 2 "Housings_SSOP:SSOP-20_4.4x6.5mm_Pitch0.65mm" H 6300 4800 60  0001 C CNN
F 3 "" H 6300 5500 60  0000 C CNN
	1    6300 5500
	1    0    0    -1  
$EndComp
Text Label 5600 3750 2    60   ~ 0
A0
Text Label 5600 3200 2    60   ~ 0
A1
Text Label 5600 3100 2    60   ~ 0
A2
Text Label 5600 3000 2    60   ~ 0
A3
Text Label 5600 2900 2    60   ~ 0
A4
Text Label 5600 2800 2    60   ~ 0
A5
Text Label 5600 2700 2    60   ~ 0
A6
Text Label 5600 2600 2    60   ~ 0
A7
Text Label 5600 2500 2    60   ~ 0
A8
Text Label 5600 3850 2    60   ~ 0
A9
Text Label 5600 3950 2    60   ~ 0
A10
Text Label 5600 4050 2    60   ~ 0
A11
Text Label 5600 4150 2    60   ~ 0
A12
Text Label 5600 4250 2    60   ~ 0
A13
Text Label 5600 4350 2    60   ~ 0
A14
Text Label 5600 4450 2    60   ~ 0
A15
Text Label 5600 5500 2    60   ~ 0
16MHZ
Text Label 5600 5300 2    60   ~ 0
PHI0
Text Label 5600 5200 2    60   ~ 0
16MHZ_DIV13
Text Label 5600 5100 2    60   ~ 0
RnW
Text Label 5600 5400 2    60   ~ 0
nRST
Text Label 2100 5250 2    60   ~ 0
nNMI
Text Label 2100 5550 2    60   ~ 0
nIRQ
Text Label 3200 5650 0    60   ~ 0
RDY
$Comp
L 74hct125d U1
U 1 1 58D0BE30
P 2650 5250
F 0 "U1" H 2650 5500 60  0000 C CNN
F 1 "74hct125d" V 2650 5100 60  0000 C CNN
F 2 "Housings_SOIC:SOIC-14_3.9x8.7mm_Pitch1.27mm" H 2650 4650 60  0001 C CNN
F 3 "" H 2650 5250 60  0000 C CNN
	1    2650 5250
	1    0    0    -1  
$EndComp
Text Label 3200 5550 0    60   ~ 0
GND
Text Label 3200 5250 0    60   ~ 0
RnW_OUT_3V
Text Label 2100 5150 2    60   ~ 0
GND
Text Label 2100 5450 2    60   ~ 0
GND
Text Label 2100 5650 2    60   ~ 0
GND
Text Label 3200 5050 0    60   ~ 0
5V
Text Label 1925 1300 0    60   ~ 0
18VAC
Text Label 1425 1300 2    60   ~ 0
18VAC
Text Label 1925 1400 0    60   ~ 0
AC_RETURN
Text Label 1425 1400 2    60   ~ 0
AC_RETURN
Text Label 1925 1500 0    60   ~ 0
-5V
Text Label 1425 1500 2    60   ~ 0
-5V
Text Label 1925 1600 0    60   ~ 0
GND
Text Label 1425 1600 2    60   ~ 0
GND
Text Label 1925 1700 0    60   ~ 0
5V
Text Label 1425 1700 2    60   ~ 0
5V
Text Label 1425 1800 2    60   ~ 0
SOUND_OUT
Text Label 1925 1800 0    60   ~ 0
16MHZ
Text Label 1925 1900 0    60   ~ 0
PHI0
Text Label 1925 2000 0    60   ~ 0
nNMI
Text Label 1925 2100 0    60   ~ 0
RnW
Text Label 1925 2200 0    60   ~ 0
D6
Text Label 1925 2300 0    60   ~ 0
D4
Text Label 1925 2400 0    60   ~ 0
D2
Text Label 1925 2500 0    60   ~ 0
D0
NoConn ~ 1925 2600
$Comp
L acorn_electron_expansion_connector P1
U 1 1 58D0C9A5
P 1675 2450
F 0 "P1" H 1675 3700 50  0000 C CNN
F 1 "Acorn Electron Expansion Connector (fit connector underneath PCB)" V 1675 2450 50  0000 C CNN
F 2 "myelin-kicad:acorn_electron_48pin_expansion_connector" H 1650 1100 50  0000 C CNN
F 3 "" H 1675 1650 50  0000 C CNN
	1    1675 2450
	1    0    0    -1  
$EndComp
Text Label 1925 2700 0    60   ~ 0
A14
Text Label 1925 2800 0    60   ~ 0
A12
Text Label 1925 2900 0    60   ~ 0
A10
Text Label 1925 3400 0    60   ~ 0
A8
Text Label 1925 3300 0    60   ~ 0
A6
Text Label 1925 3200 0    60   ~ 0
A4
Text Label 1925 3000 0    60   ~ 0
A0
Text Label 1925 3100 0    60   ~ 0
A2
Text Label 1925 3500 0    60   ~ 0
GND
Text Label 1925 3600 0    60   ~ 0
5V
Text Label 1425 3600 2    60   ~ 0
5V
Text Label 1425 3500 2    60   ~ 0
GND
Text Label 1425 2700 2    60   ~ 0
A15
Text Label 1425 2800 2    60   ~ 0
A13
Text Label 1425 2900 2    60   ~ 0
A11
Text Label 1425 3000 2    60   ~ 0
A9
Text Label 1425 3100 2    60   ~ 0
A1
Text Label 1425 3200 2    60   ~ 0
A3
Text Label 1425 3300 2    60   ~ 0
A5
Text Label 1425 3400 2    60   ~ 0
A7
Text Label 1425 1900 2    60   ~ 0
nRST
Text Label 1425 2100 2    60   ~ 0
nIRQ
Text Label 1425 2200 2    60   ~ 0
D7
Text Label 1425 2300 2    60   ~ 0
D5
Text Label 1425 2400 2    60   ~ 0
D3
Text Label 1425 2500 2    60   ~ 0
D1
Text Label 1425 2600 2    60   ~ 0
RDY
Text Label 1425 2000 2    60   ~ 0
16MHZ_DIV13
$Comp
L CONN_02X24 P2
U 1 1 58D0CA5C
P 4050 2450
F 0 "P2" H 4050 3700 50  0000 C CNN
F 1 "CONN_02X24" V 4050 2450 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x24_Pitch2.54mm" H 4050 1150 50  0000 C CNN
F 3 "" H 4050 1650 50  0000 C CNN
	1    4050 2450
	1    0    0    -1  
$EndComp
Text Label 7000 2100 0    60   ~ 0
3V3
Text Label 7000 2200 0    60   ~ 0
GND
Text Label 7000 5850 0    60   ~ 0
3V3
Text Label 7000 5950 0    60   ~ 0
GND
Text Label 7000 1250 0    60   ~ 0
D0_3V
Text Label 7000 1350 0    60   ~ 0
D1_3V
Text Label 7000 1450 0    60   ~ 0
D2_3V
Text Label 7000 1550 0    60   ~ 0
D3_3V
Text Label 7000 1650 0    60   ~ 0
D4_3V
Text Label 7000 1750 0    60   ~ 0
D5_3V
Text Label 7000 1850 0    60   ~ 0
D6_3V
Text Label 7000 1950 0    60   ~ 0
D7_3V
Text Label 7000 2500 0    60   ~ 0
A8_3V
Text Label 7000 2600 0    60   ~ 0
A7_3V
Text Label 7000 2700 0    60   ~ 0
A6_3V
Text Label 7000 2800 0    60   ~ 0
A5_3V
Text Label 7000 2900 0    60   ~ 0
A4_3V
Text Label 7000 3000 0    60   ~ 0
A3_3V
Text Label 7000 3100 0    60   ~ 0
A2_3V
Text Label 7000 3200 0    60   ~ 0
A1_3V
Text Label 7000 3350 0    60   ~ 0
3V3
Text Label 7000 3450 0    60   ~ 0
GND
Text Label 7000 3750 0    60   ~ 0
A0_3V
Text Label 7000 3850 0    60   ~ 0
A9_3V
Text Label 7000 3950 0    60   ~ 0
A10_3V
Text Label 7000 4050 0    60   ~ 0
A11_3V
Text Label 7000 4150 0    60   ~ 0
A12_3V
Text Label 7000 4250 0    60   ~ 0
A13_3V
Text Label 7000 4350 0    60   ~ 0
A14_3V
Text Label 7000 4450 0    60   ~ 0
A15_3V
Text Label 7000 4600 0    60   ~ 0
3V3
Text Label 7000 4700 0    60   ~ 0
GND
Text Label 5600 3500 2    60   ~ 0
GND
Text Label 5600 4750 2    60   ~ 0
GND
Text Label 5600 6000 2    60   ~ 0
GND
Text Label 7000 5100 0    60   ~ 0
RnW_3V
Text Label 7000 5200 0    60   ~ 0
16MHZ_DIV13_3V
Text Label 7000 5300 0    60   ~ 0
PHI0_3V
Text Label 7000 5400 0    60   ~ 0
nRST_3V
Text Label 7000 5500 0    60   ~ 0
16MHZ_3V
Text Label 5600 5900 2    60   ~ 0
3V3
Text Label 5600 4650 2    60   ~ 0
A_DIR
Text Label 5600 3400 2    60   ~ 0
A_DIR
$Comp
L R0805 R4
U 1 1 58D0D6B7
P 5025 2400
F 0 "R4" V 5105 2400 50  0000 C CNN
F 1 "10k" V 5025 2400 50  0000 C CNN
F 2 "myelin-kicad:R0805_nosilkscreen" V 4955 2400 50  0001 C CNN
F 3 "" H 5025 2400 50  0000 C CNN
	1    5025 2400
	-1   0    0    1   
$EndComp
Text Label 5600 2150 2    60   ~ 0
DATA_READ
Text Label 5025 2550 3    60   ~ 0
3V3
Wire Wire Line
	5025 2150 5600 2150
Text Label 2100 5050 2    60   ~ 0
nASSERT_nNMI
Text Label 3200 5450 0    60   ~ 0
nDEASSERT_RDY
Text Label 2100 5350 2    60   ~ 0
nASSERT_nIRQ
$Comp
L R0805 R1
U 1 1 58D0DA38
P 1225 5050
F 0 "R1" V 1305 5050 50  0000 C CNN
F 1 "10k" V 1225 5050 50  0000 C CNN
F 2 "myelin-kicad:R0805_nosilkscreen" V 1155 5050 50  0001 C CNN
F 3 "" H 1225 5050 50  0000 C CNN
	1    1225 5050
	0    -1   -1   0   
$EndComp
Text Label 1075 5050 2    60   ~ 0
3V3
Wire Wire Line
	1375 5050 2100 5050
$Comp
L R0805 R2
U 1 1 58D0DB2D
P 1225 5350
F 0 "R2" V 1305 5350 50  0000 C CNN
F 1 "10k" V 1225 5350 50  0000 C CNN
F 2 "myelin-kicad:R0805_nosilkscreen" V 1155 5350 50  0001 C CNN
F 3 "" H 1225 5350 50  0000 C CNN
	1    1225 5350
	0    -1   -1   0   
$EndComp
Text Label 1075 5350 2    60   ~ 0
3V3
Wire Wire Line
	1375 5350 2100 5350
$Comp
L R0805 R3
U 1 1 58D0DBA3
P 4025 5450
F 0 "R3" V 4105 5450 50  0000 C CNN
F 1 "10k" V 4025 5450 50  0000 C CNN
F 2 "myelin-kicad:R0805_nosilkscreen" V 3955 5450 50  0001 C CNN
F 3 "" H 4025 5450 50  0000 C CNN
	1    4025 5450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3200 5450 3875 5450
Text Label 4175 5450 0    60   ~ 0
3V3
Text Label 5600 5000 2    60   ~ 0
RDY
Text Label 7000 5000 0    60   ~ 0
RDY_3V
Text Label 5600 5600 2    60   ~ 0
nIRQ
Text Label 5600 5700 2    60   ~ 0
nNMI
Text Label 3200 5150 0    60   ~ 0
RnW_nOE
$Comp
L C0805 C1
U 1 1 58D21967
P 2200 4450
F 0 "C1" H 2225 4550 50  0000 L CNN
F 1 "100n" H 2225 4350 50  0000 L CNN
F 2 "myelin-kicad:C0805_nosilkscreen" H 2238 4300 50  0001 C CNN
F 3 "" H 2200 4450 50  0000 C CNN
	1    2200 4450
	1    0    0    -1  
$EndComp
Text Label 2200 4300 0    60   ~ 0
5V
Text Label 2200 4600 2    60   ~ 0
GND
Text Label 8025 1600 0    60   ~ 0
3V3
$Comp
L C0805 C2
U 1 1 58D21AC9
P 8025 1750
F 0 "C2" H 8050 1850 50  0000 L CNN
F 1 "100n" H 8050 1650 50  0000 L CNN
F 2 "myelin-kicad:C0805_nosilkscreen" H 8063 1600 50  0001 C CNN
F 3 "" H 8025 1750 50  0000 C CNN
	1    8025 1750
	1    0    0    -1  
$EndComp
Text Label 8025 1900 2    60   ~ 0
GND
Text Label 8100 2850 0    60   ~ 0
3V3
$Comp
L C0805 C3
U 1 1 58D21BC6
P 8100 3000
F 0 "C3" H 8125 3100 50  0000 L CNN
F 1 "100n" H 8125 2900 50  0000 L CNN
F 2 "myelin-kicad:C0805_nosilkscreen" H 8138 2850 50  0001 C CNN
F 3 "" H 8100 3000 50  0000 C CNN
	1    8100 3000
	1    0    0    -1  
$EndComp
Text Label 8100 3150 2    60   ~ 0
GND
Text Label 8100 4050 0    60   ~ 0
3V3
$Comp
L C0805 C4
U 1 1 58D21C56
P 8100 4200
F 0 "C4" H 8125 4300 50  0000 L CNN
F 1 "100n" H 8125 4100 50  0000 L CNN
F 2 "myelin-kicad:C0805_nosilkscreen" H 8138 4050 50  0001 C CNN
F 3 "" H 8100 4200 50  0000 C CNN
	1    8100 4200
	1    0    0    -1  
$EndComp
Text Label 8100 4350 2    60   ~ 0
GND
Text Label 8175 5300 0    60   ~ 0
3V3
$Comp
L C0805 C5
U 1 1 58D21C5E
P 8175 5450
F 0 "C5" H 8200 5550 50  0000 L CNN
F 1 "100n" H 8200 5350 50  0000 L CNN
F 2 "myelin-kicad:C0805_nosilkscreen" H 8213 5300 50  0001 C CNN
F 3 "" H 8175 5450 50  0000 C CNN
	1    8175 5450
	1    0    0    -1  
$EndComp
Text Label 8175 5600 2    60   ~ 0
GND
Text Label 5600 2250 2    60   ~ 0
DATA_nOE
Wire Wire Line
	5025 2250 5025 2150
$Comp
L R0805 R5
U 1 1 58D2266D
P 5225 2400
F 0 "R5" V 5305 2400 50  0000 C CNN
F 1 "10k" V 5225 2400 50  0000 C CNN
F 2 "myelin-kicad:R0805_nosilkscreen" V 5155 2400 50  0001 C CNN
F 3 "" H 5225 2400 50  0000 C CNN
	1    5225 2400
	-1   0    0    1   
$EndComp
Text Label 5225 2550 3    60   ~ 0
3V3
Wire Wire Line
	5225 2250 5600 2250
$Comp
L scarab_mini_spartan_6_lx25 U6
U 1 1 58D25E8C
P 9775 4800
F 0 "U6" H 9775 7300 60  0000 C CNN
F 1 "scarab_mini_spartan_6_lx25" V 9775 6400 60  0000 C CNN
F 2 "myelin-kicad:scarab_mini_spartan_6_lx25" V 10075 6350 60  0000 C CNN
F 3 "" H 8825 4650 60  0000 C CNN
	1    9775 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	9925 4100 9925 6050
Connection ~ 9925 4250
Connection ~ 9925 4400
Connection ~ 9925 4550
Connection ~ 9925 4700
Connection ~ 9925 4850
Connection ~ 9925 5000
Connection ~ 9925 5150
Connection ~ 9925 5300
Connection ~ 9925 5450
Connection ~ 9925 5600
Connection ~ 9925 5750
Connection ~ 9925 5900
Connection ~ 9725 950 
Connection ~ 9725 1100
Connection ~ 9725 1250
Connection ~ 9725 1400
Connection ~ 9725 1550
Connection ~ 9725 1700
Connection ~ 9725 1850
Text Label 9725 800  2    60   ~ 0
3V3
Text Label 9925 4850 0    60   ~ 0
GND
Wire Wire Line
	9725 2000 9725 800 
Text Label 9725 2150 3    60   ~ 0
5V_scarab
Text Label 9075 800  2    60   ~ 0
nDEASSERT_RDY
Text Label 9075 950  2    60   ~ 0
nASSERT_nIRQ
Text Label 9075 1100 2    60   ~ 0
nASSERT_nNMI
Text Label 9075 1850 2    60   ~ 0
RnW_3V
Text Label 9075 1700 2    60   ~ 0
16MHZ_DIV13_3V
Text Label 9075 1400 2    60   ~ 0
PHI0_3V
Text Label 9075 1550 2    60   ~ 0
nRST_3V
Text Label 9075 1250 2    60   ~ 0
16MHZ_3V
Text Label 9075 2000 2    60   ~ 0
RDY_3V
Text Label 9075 3200 2    60   ~ 0
D0_3V
Text Label 9075 3050 2    60   ~ 0
D1_3V
Text Label 9075 2900 2    60   ~ 0
D2_3V
Text Label 9075 2750 2    60   ~ 0
D3_3V
Text Label 9075 2600 2    60   ~ 0
D4_3V
Text Label 9075 2450 2    60   ~ 0
D5_3V
Text Label 9075 2300 2    60   ~ 0
D6_3V
Text Label 9075 2150 2    60   ~ 0
D7_3V
Text Label 9075 3650 2    60   ~ 0
A15_3V
Text Label 9075 3800 2    60   ~ 0
A14_3V
Text Label 9075 3950 2    60   ~ 0
A13_3V
Text Label 9075 4100 2    60   ~ 0
A12_3V
Text Label 9075 4250 2    60   ~ 0
A11_3V
Text Label 9075 4400 2    60   ~ 0
A10_3V
Text Label 9075 4550 2    60   ~ 0
A9_3V
Text Label 9075 4700 2    60   ~ 0
A0_3V
Text Label 9075 3350 2    60   ~ 0
DATA_nOE
Text Label 9075 3500 2    60   ~ 0
DATA_READ
Text Label 9075 5900 2    60   ~ 0
A8_3V
Text Label 9075 5750 2    60   ~ 0
A7_3V
Text Label 9075 5600 2    60   ~ 0
A6_3V
Text Label 9075 5450 2    60   ~ 0
A5_3V
Text Label 9075 5300 2    60   ~ 0
A4_3V
Text Label 9075 5150 2    60   ~ 0
A3_3V
Text Label 9075 5000 2    60   ~ 0
A2_3V
Text Label 9075 4850 2    60   ~ 0
A1_3V
Text Label 4600 6775 0    60   ~ 0
5V_scarab
Text Label 4600 6675 0    60   ~ 0
5V
$Comp
L CONN_01X02 P3
U 1 1 58D25ACD
P 4400 6725
F 0 "P3" H 4400 6875 50  0000 C CNN
F 1 "5V / 5V0" V 4500 6725 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 4350 7000 50  0000 C CNN
F 3 "" H 4400 6725 50  0000 C CNN
	1    4400 6725
	-1   0    0    1   
$EndComp
Text Label 9075 6050 2    60   ~ 0
A_DIR
$Comp
L R0805 R6
U 1 1 59370791
P 8500 6050
F 0 "R6" V 8605 6050 50  0000 C CNN
F 1 "10k" V 8500 6050 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 8430 6050 50  0001 C CNN
F 3 "" H 8500 6050 50  0000 C CNN
	1    8500 6050
	0    -1   -1   0   
$EndComp
Text Label 8350 6050 2    60   ~ 0
3V3
Wire Wire Line
	8650 6050 9075 6050
Text Label 3200 5350 0    60   ~ 0
RnW
$Comp
L R0805 R7
U 1 1 59371B96
P 4025 5150
F 0 "R7" V 4105 5150 50  0000 C CNN
F 1 "10k" V 4025 5150 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3955 5150 50  0001 C CNN
F 3 "" H 4025 5150 50  0000 C CNN
	1    4025 5150
	0    -1   -1   0   
$EndComp
Text Label 4175 5150 0    60   ~ 0
3V3
Text Notes 2850 4875 0    60   ~ 0
U1.4 drives RnW when the Electron's\n6502 is removed and the miniSpartan\nis providing the processor.  Otherwise\nRnW_nOE = 3V3 and RnW is not driven\nby U1.
Text Notes 1650 6125 0    60   ~ 0
nNMI, nIRQ, and RDY are all pulled up on the Electron\nmotherboard or inside the Electron ULA.  We only\never pull them down here.
Text Notes 5025 1000 0    60   ~ 0
U2 buffers the data bus from Elk->FPGA when DATA_READ=1, and\nFPGA->Elk when DATA_READ=0.  U3 and U4 buffer Elk->FPGA\nwhen A_DIR=1 (6502 fitted in Elk) and FPGA->Elk when A_DIR=0\n(6502 emulated in FPGA).
Text Notes 5325 6375 0    60   ~ 0
U5 buffers signals from ULA->FPGA, plus RnW, RDY,\nnNMI, and nIRQ, which can also be driven by U1.
Wire Wire Line
	3875 5150 3200 5150
Text Label 7000 5600 0    60   ~ 0
nIRQ_3V
Text Label 7000 5700 0    60   ~ 0
nNMI_3V
Text Label 10575 3350 0    60   ~ 0
nIRQ_3V
Text Label 10575 3050 0    60   ~ 0
nNMI_3V
Text Label 10575 2750 0    60   ~ 0
RnW_nOE
Text Label 10575 2450 0    60   ~ 0
RnW_OUT_3V
$EndSCHEMATC
