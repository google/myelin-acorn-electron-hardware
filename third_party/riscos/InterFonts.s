; Copyright 1996 Acorn Computers Ltd
;
; Licensed under the Apache License, Version 2.0 (the "License");
; you may not use this file except in compliance with the License.
; You may obtain a copy of the License at
;
;     http://www.apache.org/licenses/LICENSE-2.0
;
; Unless required by applicable law or agreed to in writing, software
; distributed under the License is distributed on an "AS IS" BASIS,
; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; See the License for the specific language governing permissions and
; limitations under the License.
;
; Inter.s.InterFonts
;
; Characters are now identified by their number in the ISO10646 Universal
; Character Set
;

FontTable

; IF YOU ADD ANY CHARACTERS TO THIS TABLE, REMEMBER TO ADD A REFERENCE IN
; UCSTABLE BELOW, OTHERWISE WE WON'T OFFER IT VIA SERVICE_DEFINEUCS. THANKYOU.

;--------------------------------------------------------------------------------
;  BASIC LATIN
;--------------------------------------------------------------------------------

U_0020 = &00,&00,&00,&00,&00,&00,&00,&00 ;ISO  "space"
U_0021 = &18,&18,&18,&18,&18,&00,&18,&00 ;ISO  "exclamation mark"
U_0022 = &6C,&6C,&6C,&00,&00,&00,&00,&00 ;ISO  "quotation mark"
U_0023 = &36,&36,&7F,&36,&7F,&36,&36,&00 ;ISO  "number sign"
U_0024 = &0C,&3F,&68,&3E,&0B,&7E,&18,&00 ;ISO  "dollar sign"
U_0025 = &60,&66,&0C,&18,&30,&66,&06,&00 ;ISO  "percent sign"
U_0026 = &38,&6C,&6C,&38,&6D,&66,&3B,&00 ;ISO  "ampersand"
U_0027 = &18,&18,&18,&00,&00,&00,&00,&00 ;ISO  "apostrophe" (vertical)
B_0027 = &0C,&18,&30,&00,&00,&00,&00,&00 ;BFNT "apostrophe" (sloped)
U_0028 = &0C,&18,&30,&30,&30,&18,&0C,&00 ;ISO  "left parenthesis"
U_0029 = &30,&18,&0C,&0C,&0C,&18,&30,&00 ;ISO  "right parenthesis"
U_002A = &00,&18,&7E,&3C,&7E,&18,&00,&00 ;ISO  "asterisk"
U_002B = &00,&18,&18,&7E,&18,&18,&00,&00 ;ISO  "plus sign"
U_002C = &00,&00,&00,&00,&00,&18,&18,&30 ;ISO  "comma"
U_002D = &00,&00,&00,&7E,&00,&00,&00,&00 ;ISO  "hyphen-minus"
U_002E = &00,&00,&00,&00,&00,&18,&18,&00 ;ISO  "full stop"
U_002F = &00,&06,&0C,&18,&30,&60,&00,&00 ;ISO  "solidus"
U_0030 = &3C,&66,&6E,&7E,&76,&66,&3C,&00 ;ISO  "digit zero"
U_0031 = &18,&38,&18,&18,&18,&18,&7E,&00 ;ISO  "digit one"
U_0032 = &3C,&66,&06,&0C,&18,&30,&7E,&00 ;ISO  "digit two"
U_0033 = &3C,&66,&06,&1C,&06,&66,&3C,&00 ;ISO  "digit three"
U_0034 = &0C,&1C,&3C,&6C,&7E,&0C,&0C,&00 ;ISO  "digit four"
U_0035 = &7E,&60,&7C,&06,&06,&66,&3C,&00 ;ISO  "digit five"
U_0036 = &1C,&30,&60,&7C,&66,&66,&3C,&00 ;ISO  "digit six"
U_0037 = &7E,&06,&0C,&18,&30,&30,&30,&00 ;ISO  "digit seven"
U_0038 = &3C,&66,&66,&3C,&66,&66,&3C,&00 ;ISO  "digit eight"
U_0039 = &3C,&66,&66,&3E,&06,&0C,&38,&00 ;ISO  "digit nine"
U_003A = &00,&00,&18,&18,&00,&18,&18,&00 ;ISO  "colon"
U_003B = &00,&00,&18,&18,&00,&18,&18,&30 ;ISO  "semicolon"
U_003C = &0C,&18,&30,&60,&30,&18,&0C,&00 ;ISO  "less-than sign"
U_003D = &00,&00,&7E,&00,&7E,&00,&00,&00 ;ISO  "equals sign"
U_003E = &30,&18,&0C,&06,&0C,&18,&30,&00 ;ISO  "greater-than sign"
U_003F = &3C,&66,&0C,&18,&18,&00,&18,&00 ;ISO  "question mark"
U_0040 = &3C,&66,&6E,&6A,&6E,&60,&3C,&00 ;ISO  "commercial at"
U_0041 = &3C,&66,&66,&7E,&66,&66,&66,&00 ;ISO  "Latin capital letter A"
U_0042 = &7C,&66,&66,&7C,&66,&66,&7C,&00 ;ISO  "Latin capital letter B"
U_0043 = &3C,&66,&60,&60,&60,&66,&3C,&00 ;ISO  "Latin capital letter C"
U_0044 = &78,&6C,&66,&66,&66,&6C,&78,&00 ;ISO  "Latin capital letter D"
U_0045 = &7E,&60,&60,&7C,&60,&60,&7E,&00 ;ISO  "Latin capital letter E"
U_0046 = &7E,&60,&60,&7C,&60,&60,&60,&00 ;ISO  "Latin capital letter F"
U_0047 = &3C,&66,&60,&6E,&66,&66,&3C,&00 ;ISO  "Latin capital letter G"
U_0048 = &66,&66,&66,&7E,&66,&66,&66,&00 ;ISO  "Latin capital letter H"
U_0049 = &7E,&18,&18,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I"
U_004A = &3E,&0C,&0C,&0C,&0C,&6C,&38,&00 ;ISO  "Latin capital letter J"
U_004B = &66,&6C,&78,&70,&78,&6C,&66,&00 ;ISO  "Latin capital letter K"
U_004C = &60,&60,&60,&60,&60,&60,&7E,&00 ;ISO  "Latin capital letter L"
U_004D = &63,&77,&7F,&6B,&6B,&63,&63,&00 ;ISO  "Latin capital letter M"
U_004E = &66,&66,&76,&7E,&6E,&66,&66,&00 ;ISO  "Latin capital letter N"
U_004F = &3C,&66,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O"
U_0050 = &7C,&66,&66,&7C,&60,&60,&60,&00 ;ISO  "Latin capital letter P"
U_0051 = &3C,&66,&66,&66,&6A,&6C,&36,&00 ;ISO  "Latin capital letter Q"
U_0052 = &7C,&66,&66,&7C,&6C,&66,&66,&00 ;ISO  "Latin capital letter R"
U_0053 = &3C,&66,&60,&3C,&06,&66,&3C,&00 ;ISO  "Latin capital letter S"
U_0054 = &7E,&18,&18,&18,&18,&18,&18,&00 ;ISO  "Latin capital letter T"
U_0055 = &66,&66,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U"
U_0056 = &66,&66,&66,&66,&66,&3C,&18,&00 ;ISO  "Latin capital letter V"
U_0057 = &63,&63,&6B,&6B,&7F,&77,&63,&00 ;ISO  "Latin capital letter W"
U_0058 = &66,&66,&3C,&18,&3C,&66,&66,&00 ;ISO  "Latin capital letter X"
U_0059 = &66,&66,&66,&3C,&18,&18,&18,&00 ;ISO  "Latin capital letter Y"
U_005A = &7E,&06,&0C,&18,&30,&60,&7E,&00 ;ISO  "Latin capital letter Z"
U_005B = &7C,&60,&60,&60,&60,&60,&7C,&00 ;ISO  "left square bracket"
U_005C = &00,&60,&30,&18,&0C,&06,&00,&00 ;ISO  "reverse solidus"
U_005D = &3E,&06,&06,&06,&06,&06,&3E,&00 ;ISO  "right square bracket"
U_005E = &3C,&66,&00,&00,&00,&00,&00,&00 ;ISO  "circumflex accent"
 [ DoBfont
B_005E = &18,&3C,&66,&42,&00,&00,&00,&00 ;BFNT "hat"
 ]
U_005F = &00,&00,&00,&00,&00,&00,&00,&FF ;ISO  "low line"
U_0060 = &30,&18,&00,&00,&00,&00,&00,&00 ;ISO  "grave accent"
U_0061 = &00,&00,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a"
U_0062 = &60,&60,&7C,&66,&66,&66,&7C,&00 ;ISO  "Latin small letter b"
U_0063 = &00,&00,&3C,&66,&60,&66,&3C,&00 ;ISO  "Latin small letter c"
U_0064 = &06,&06,&3E,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter d"
U_0065 = &00,&00,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e"
U_0066 = &1C,&30,&30,&7C,&30,&30,&30,&00 ;ISO  "Latin small letter f"
U_0067 = &00,&00,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g"
U_0068 = &60,&60,&7C,&66,&66,&66,&66,&00 ;ISO  "Latin small letter h"
U_0069 = &18,&00,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter i"
U_006A = &18,&00,&38,&18,&18,&18,&18,&70 ;ISO  "Latin small letter j"
U_006B = &60,&60,&66,&6C,&78,&6C,&66,&00 ;ISO  "Latin small letter k"
U_006C = &38,&18,&18,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter l"
U_006D = &00,&00,&36,&7F,&6B,&6B,&63,&00 ;ISO  "Latin small letter m"
U_006E = &00,&00,&7C,&66,&66,&66,&66,&00 ;ISO  "Latin small letter n"
U_006F = &00,&00,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin small letter o"
U_0070 = &00,&00,&7C,&66,&66,&7C,&60,&60 ;ISO  "Latin small letter p"
U_0071 = &00,&00,&3E,&66,&66,&3E,&06,&07 ;ISO  "Latin small letter q"
U_0072 = &00,&00,&6C,&76,&60,&60,&60,&00 ;ISO  "Latin small letter r"
U_0073 = &00,&00,&3E,&60,&3C,&06,&7C,&00 ;ISO  "Latin small letter s"
U_0074 = &30,&30,&7C,&30,&30,&30,&1C,&00 ;ISO  "Latin small letter t"
U_0075 = &00,&00,&66,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u"
U_0076 = &00,&00,&66,&66,&66,&3C,&18,&00 ;ISO  "Latin small letter v"
U_0077 = &00,&00,&63,&6B,&6B,&7F,&36,&00 ;ISO  "Latin small letter w"
U_0078 = &00,&00,&66,&3C,&18,&3C,&66,&00 ;ISO  "Latin small letter x"
U_0079 = &00,&00,&66,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y"
U_007A = &00,&00,&7E,&0C,&18,&30,&7E,&00 ;ISO  "Latin small letter z"
U_007B = &0C,&18,&18,&70,&18,&18,&0C,&00 ;ISO  "left curly bracket"
U_007C = &18,&18,&18,&18,&18,&18,&18,&00 ;ISO  "vertical line"
U_007D = &30,&18,&18,&0E,&18,&18,&30,&00 ;ISO  "right curly bracket"
U_007E = &31,&6B,&46,&00,&00,&00,&00,&00 ;ISO  "tilde"


;--------------------------------------------------------------------------------
;  LATIN-1 SUPPLEMENT
;--------------------------------------------------------------------------------

U_00A0 * U_0020                          ;ISO  "no-break space"
U_00A1 = &18,&00,&18,&18,&18,&18,&18,&00 ;ISO  "inverted exclamation mark"
U_00A2 = &08,&3E,&6B,&68,&6B,&3E,&08,&00 ;ISO  "cent sign"
U_00A3 = &1C,&36,&30,&7C,&30,&30,&7E,&00 ;ISO  "pound sign"
U_00A4 = &00,&66,&3C,&66,&66,&3C,&66,&00 ;ISO  "currency sign"
 [ DoBfont
B_00A4 = &00,&7E,&3C,&66,&66,&3C,&7E,&00 ;BFNT "currency sign"
 ]
U_00A5 = &66,&3C,&18,&18,&7E,&18,&18,&00 ;ISO  "yen sign"
U_00A6 = &18,&18,&18,&00,&18,&18,&18,&00 ;ISO  "broken bar"
U_00A7 = &3C,&60,&3C,&66,&3C,&06,&3C,&00 ;ISO  "section sign"
U_00A8 = &66,&00,&00,&00,&00,&00,&00,&00 ;ISO  "diaeresis"
U_00A9 = &3C,&42,&99,&A1,&A1,&99,&42,&3C ;ISO  "copyright sign"
U_00AA = &1C,&06,&1E,&36,&1E,&00,&3E,&00 ;ISO  "feminine ordinal indicator"
U_00AB = &00,&33,&66,&CC,&CC,&66,&33,&00 ;ISO  "left-pointing double angle quotation mark"
U_00AC = &7E,&06,&00,&00,&00,&00,&00,&00 ;ISO  "not sign"
U_00AD * U_002D                          ;ISO  "soft hyphen"
U_00AE = &3C,&42,&B9,&A5,&B9,&A5,&42,&3C ;ISO  "registered sign"
U_00AF = &7E,&00,&00,&00,&00,&00,&00,&00 ;ISO  "macron"
U_00B0 = &3C,&66,&3C,&00,&00,&00,&00,&00 ;ISO  "degree sign"
U_00B1 = &18,&18,&7E,&18,&18,&00,&7E,&00 ;ISO  "plus-minus sign"
U_00B2 = &38,&04,&18,&20,&3C,&00,&00,&00 ;ISO  "superscript two"
U_00B3 = &38,&04,&18,&04,&38,&00,&00,&00 ;ISO  "superscript three"
U_00B4 = &0C,&18,&00,&00,&00,&00,&00,&00 ;ISO  "acute accent"
U_00B5 = &00,&00,&33,&33,&33,&33,&3E,&60 ;ISO  "micro sign"
U_00B6 = &03,&3E,&76,&76,&36,&36,&3E,&00 ;ISO  "pilcrow sign"
U_00B7 = &00,&00,&00,&18,&18,&00,&00,&00 ;ISO  "middle dot"
U_00B8 = &00,&00,&00,&00,&00,&00,&18,&30 ;ISO  "cedilla"
U_00B9 = &10,&30,&10,&10,&38,&00,&00,&00 ;ISO  "superscript one"
U_00BA = &1C,&36,&36,&36,&1C,&00,&3E,&00 ;ISO  "masculine ordinal indicator"
U_00BB = &00,&CC,&66,&33,&33,&66,&CC,&00 ;ISO  "right-pointing double angle quotation mark"
U_00BC = &40,&C0,&40,&48,&48,&0A,&0F,&02 ;ISO  "vulgar fraction one quarter"
U_00BD = &40,&C0,&40,&4F,&41,&0F,&08,&0F ;ISO  "vulgar fraction one half"
U_00BE = &E0,&20,&E0,&28,&E8,&0A,&0F,&02 ;ISO  "vulgar fraction three quarters"
U_00BF = &18,&00,&18,&18,&30,&66,&3C,&00 ;ISO  "inverted question mark"
 [ NewAccents
U_00C0 = &30,&18,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with grave"
U_00C1 = &0C,&18,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with acute"
U_00C2 = &18,&66,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with circumflex"
U_00C3 = &36,&6C,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with tilde"
U_00C4 = &66,&00,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with diaeresis"
U_00C5 = &3C,&66,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with ring above"
 |
U_00C0 = &30,&18,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with grave"
U_00C1 = &0C,&18,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with acute"
U_00C2 = &3C,&66,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with circumflex"
U_00C3 = &36,&6C,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with tilde"
U_00C4 = &66,&66,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with diaeresis"
U_00C5 = &3C,&66,&3C,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with ring above"
 ]
U_00C6 = &3F,&66,&66,&7F,&66,&66,&67,&00 ;ISO  "Latin capital letter AE (ash)"
 [ NewAccents
U_00C7 = &3C,&66,&60,&60,&60,&66,&3C,&60 ;ISO  "Latin capital letter C with cedilla"
 |
U_00C7 = &3C,&66,&60,&60,&66,&3C,&30,&60 ;ISO  "Latin capital letter C with cedilla"
 ]
U_00C8 = &30,&18,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with grave"
U_00C9 = &0C,&18,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with acute"
U_00CA = &3C,&66,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with circumflex"
U_00CB = &66,&00,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with diaeresis"
 [ NewAccents
U_00CC = &30,&18,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with grave"
U_00CD = &0C,&18,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with acute"
U_00CE = &3C,&66,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with circumflex"
U_00CF = &66,&00,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with diaeresis"
 |
U_00CC = &30,&18,&00,&7E,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with grave"
U_00CD = &0C,&18,&00,&7E,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with acute"
U_00CE = &3C,&66,&00,&7E,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with circumflex"
U_00CF = &66,&66,&00,&7E,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with diaeresis"
 ]
U_00D0 = &78,&6C,&66,&F6,&66,&6C,&78,&00 ;ISO  "Latin capital letter ETH"
 [ NewAccents
U_00D1 = &36,&6C,&66,&76,&7E,&6E,&66,&00 ;ISO  "Latin capital letter N with tilde"
 |
U_00D1 = &36,&6C,&00,&66,&76,&6E,&66,&00 ;ISO  "Latin capital letter N with tilde"
 ]
U_00D2 = &30,&18,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with grave"
U_00D3 = &0C,&18,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with acute"
U_00D4 = &18,&66,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with circumflex"
U_00D5 = &36,&6C,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with tilde"
U_00D6 = &66,&00,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with diaeresis"
U_00D7 = &00,&63,&36,&1C,&1C,&36,&63,&00 ;ISO  "multiply sign"
U_00D8 = &3D,&66,&6E,&7E,&76,&66,&BC,&00 ;ISO  "Latin capital letter O with slash"
U_00D9 = &30,&18,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with grave"
U_00DA = &0C,&18,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with acute"
U_00DB = &3C,&66,&00,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with circumflex"
U_00DC = &66,&00,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with diaeresis"
U_00DD = &0C,&18,&66,&66,&3C,&18,&18,&00 ;ISO  "Latin capital letter Y with acute"
U_00DE = &F0,&60,&7C,&66,&7C,&60,&F0,&00 ;ISO  "Latin capital letter THORN"
U_00DF = &3C,&66,&66,&6C,&66,&66,&6C,&C0 ;ISO  "Latin small letter sharp s"
U_00E0 = &30,&18,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with grave"
U_00E1 = &0C,&18,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with acute"
U_00E2 = &18,&66,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with circumflex"
U_00E3 = &36,&6C,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with tilde"
U_00E4 = &66,&00,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with diaeresis"
U_00E5 = &3C,&66,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with ring above"
U_00E6 = &00,&00,&3F,&0D,&3F,&6C,&3F,&00 ;ISO  "Latin small letter ae (ash)"
U_00E7 = &00,&00,&3C,&66,&60,&66,&3C,&60 ;ISO  "Latin small letter c with cedilla"
U_00E8 = &30,&18,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with grave"
U_00E9 = &0C,&18,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with acute"
U_00EA = &3C,&66,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with cirumflex"
U_00EB = &66,&00,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with diaeresis"
U_00EC = &30,&18,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with grave"
U_00ED = &0C,&18,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with acute"
U_00EE = &3C,&66,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with circumflex"
 [ NewAccents
U_00EF = &66,&00,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter i with diaeresis"
 |
U_00EF = &66,&00,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with diaeresis"
 ]
U_00F0 = &18,&3E,&0C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter eth"
U_00F1 = &36,&6C,&00,&7C,&66,&66,&66,&00 ;ISO  "Latin small letter n with tilde"
U_00F2 = &30,&18,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with grave"
U_00F3 = &0C,&18,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with acute"
U_00F4 = &3C,&66,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with circumflex"
U_00F5 = &36,&6C,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with tilde"
U_00F6 = &66,&00,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with diaeresis"
U_00F7 = &00,&18,&00,&FF,&00,&18,&00,&00 ;ISO  "divide sign"
U_00F8 = &00,&02,&3C,&6E,&76,&66,&BC,&00 ;ISO  "Latin small letter o with slash"
 [ NewAccents
U_00F9 = &30,&18,&66,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with grave"
U_00FA = &0C,&18,&66,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with acute"
 |
U_00F9 = &30,&18,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with grave"
U_00FA = &0C,&18,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with acute"
 ]
U_00FB = &3C,&66,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with circumflex"
U_00FC = &66,&00,&66,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with diaeresis"
U_00FD = &0C,&18,&66,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y with acute"
U_00FE = &60,&60,&7C,&66,&7C,&60,&60,&00 ;ISO  "Latin small letter thorn"
U_00FF = &66,&00,&66,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y with diaeresis"


;--------------------------------------------------------------------------------
;  LATIN EXTENDED-A
;--------------------------------------------------------------------------------

U_0100 = &7E,&00,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with macron"
U_0101 = &7E,&00,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with macron"
 [ NewAccents
U_0102 = &46,&3C,&3C,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter A with breve"
 |
U_0102 = &46,&3C,&00,&3C,&66,&7E,&66,&00 ;ISO  "Latin capital letter A with breve"
 ]
U_0103 = &26,&1C,&3C,&06,&3E,&66,&3E,&00 ;ISO  "Latin small letter a with breve"
 [ NewAccents
U_0104 = &3C,&66,&66,&7E,&66,&66,&04,&03 ;ISO  "Latin capital letter A with ogonek"
 |
U_0104 = &00,&3C,&66,&7E,&66,&66,&04,&03 ;ISO  "Latin capital letter A with ogonek"
 ]
U_0105 = &00,&3C,&06,&3E,&66,&3E,&04,&03 ;ISO  "Latin small letter a with ogonek"
U_0106 = &0C,&18,&3E,&60,&60,&60,&3E,&00 ;ISO  "Latin capital letter C with acute"
U_0107 = &0C,&18,&3C,&66,&60,&66,&3C,&00 ;ISO  "Latin small letter c with acute"
U_0108 = &3C,&66,&3E,&60,&60,&60,&3E,&00 ;ISO  "Latin capital letter C with circumflex"
U_0109 = &3C,&66,&3C,&66,&60,&66,&3C,&00 ;ISO  "Latin small letter c with circumflex"
U_010A = &18,&00,&3E,&60,&60,&60,&3E,&00 ;ISO  "Latin capital letter C with dot above"
U_010B = &18,&00,&3C,&66,&60,&66,&3C,&00 ;ISO  "Latin small letter c with dot above"
U_010C = &66,&18,&3E,&60,&60,&60,&3E,&00 ;ISO  "Latin capital letter C with caron"
U_010D = &66,&18,&3C,&66,&60,&66,&3C,&00 ;ISO  "Latin small letter c with caron"
U_010E = &66,&18,&7C,&66,&66,&66,&7C,&00 ;ISO  "Latin capital letter D with caron"
U_010F = &03,&06,&3E,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter d with caron"
U_0110 * U_00D0                          ;ISO  "Latin capital letter D with stroke"
U_0111 = &06,&0F,&06,&3E,&66,&66,&3E,&00 ;ISO  "Latin small letter d with stroke"
U_0112 = &7E,&00,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with macron"
U_0113 = &7E,&00,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with macron"
U_0114 = &46,&3C,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with breve"
U_0115 = &46,&3C,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with breve"
U_0116 = &18,&00,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with dot above"
U_0117 = &18,&00,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with dot above"
U_0118 = &00,&7E,&60,&7C,&60,&7E,&18,&0C ;ISO  "Latin capital letter E with ogonek"
U_0119 = &00,&3C,&66,&7E,&60,&3C,&18,&0C ;ISO  "Latin small letter e with ogonek"
U_011A = &66,&18,&7E,&60,&7C,&60,&7E,&00 ;ISO  "Latin capital letter E with caron"
U_011B = &66,&18,&3C,&66,&7E,&60,&3C,&00 ;ISO  "Latin small letter e with caron"
U_011C = &3C,&66,&3C,&60,&6E,&66,&3C,&00 ;ISO  "Latin capital letter G with circumflex"
U_011D = &3C,&66,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with circumflex"
 [ NewAccents
U_011E = &46,&3C,&3C,&60,&6E,&66,&3C,&00 ;ISO  "Latin capital letter G with breve"
U_011F = &26,&1C,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with breve"
 |
U_011E = &66,&18,&3C,&60,&6E,&66,&3C,&00 ;ISO  "Latin capital letter G with breve"
U_011F = &66,&18,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with breve"
 ]
U_0120 = &18,&00,&3C,&60,&6E,&66,&3C,&00 ;ISO  "Latin capital letter G with dot above"
U_0121 = &18,&00,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with dot above"
U_0122 = &3C,&66,&60,&6E,&66,&66,&3C,&60 ;ISO  "Latin capital letter G with cedilla"
U_0123 = &0C,&18,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with cedilla"
U_0124 = &3C,&66,&00,&66,&7E,&66,&66,&00 ;ISO  "Latin capital letter H with circumflex"
U_0125 = &3C,&66,&60,&60,&7C,&66,&66,&00 ;ISO  "Latin small letter h with circumflex"
U_0126 = &66,&FF,&66,&7E,&66,&66,&66,&00 ;ISO  "Latin capital letter H with stroke"
U_0127 = &60,&F0,&60,&7C,&66,&66,&66,&00 ;ISO  "Latin small letter h with stroke"
 [ NewAccents
U_0128 = &36,&6C,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with tilde"
 |
U_0128 = &36,&6C,&00,&7E,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with tilde"
 ]
U_0129 = &36,&6C,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with tilde"
U_012A = &7E,&00,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with macron"
U_012B = &7E,&00,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter i with macron"
U_012C = &46,&3C,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with breve"
U_012D = &46,&3C,&00,&38,&18,&18,&3C,&00 ;ISO  "Latin small letter i with breve"
U_012E = &7E,&18,&18,&18,&18,&7E,&18,&0C ;ISO  "Latin capital letter I with ogonek"
U_012F = &18,&00,&38,&18,&18,&3C,&18,&0C ;ISO  "Latin small letter i with ogonek"
U_0130 = &18,&00,&7E,&18,&18,&18,&7E,&00 ;ISO  "Latin capital letter I with dot above"
U_0131 = &00,&00,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter i without dot"
U_0132 = &FF,&66,&66,&66,&66,&76,&FC,&00 ;ISO  "Latin capital ligature IJ"
U_0133 = &66,&00,&EE,&66,&66,&66,&F6,&1C ;ISO  "Latin small ligature ij"
 [ NewAccents
U_0134 = &3C,&66,&3E,&0C,&0C,&6C,&38,&00 ;ISO  "Latin capital letter J with circumflex"
 |
U_0134 = &3C,&66,&00,&3E,&0C,&6C,&38,&00 ;ISO  "Latin capital letter J with circumflex"
 ]
U_0135 = &3C,&66,&00,&38,&18,&18,&18,&70 ;ISO  "Latin small letter j with circumflex"
U_0136 = &66,&6C,&78,&78,&6C,&66,&0C,&06 ;ISO  "Latin capital letter K with cedilla"
U_0137 = &60,&66,&6C,&78,&6C,&66,&0C,&06 ;ISO  "Latin small letter k with cedilla"
U_0138 = &00,&00,&66,&6C,&78,&6C,&66,&00 ;ISO  "Latin small letter kra"
U_0139 = &0C,&18,&60,&60,&60,&60,&7E,&00 ;ISO  "Latin capital letter L with acute"
U_013A = &0C,&18,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter l with acute"
U_013B = &60,&60,&60,&60,&60,&7E,&18,&0C ;ISO  "Latin capital letter L with cedilla"
U_013C = &38,&18,&18,&18,&18,&18,&3C,&06 ;ISO  "Latin small letter l with cedilla"
U_013D = &66,&18,&60,&60,&60,&60,&7E,&00 ;ISO  "Latin capital letter L with caron"
U_013E = &66,&18,&38,&18,&18,&18,&3C,&00 ;ISO  "Latin small letter l with caron"
U_013F = &60,&60,&60,&66,&60,&60,&7E,&00 ;ISO  "Latin capital letter L with middle dot"
U_0140 = &38,&18,&18,&1A,&18,&18,&3C,&00 ;ISO  "Latin small letter l with middle dot"
U_0141 = &60,&60,&60,&78,&E0,&60,&7E,&00 ;ISO  "Latin capital letter L with stroke"
U_0142 = &38,&18,&18,&1E,&78,&18,&3C,&00 ;ISO  "Latin small letter l with stroke"
 [ NewAccents
U_0143 = &0C,&18,&66,&76,&7E,&6E,&66,&00 ;ISO  "Latin capital letter N with acute"
 |
U_0143 = &0C,&18,&00,&66,&76,&6E,&66,&00 ;ISO  "Latin capital letter N with acute"
 ]
U_0144 = &0C,&18,&7C,&66,&66,&66,&66,&00 ;ISO  "Latin small letter n with acute"
U_0145 = &66,&76,&7E,&6E,&66,&66,&0C,&06 ;ISO  "Latin capital letter N with cedilla"
U_0146 = &00,&00,&7C,&66,&66,&66,&0C,&06 ;ISO  "Latin small letter n with cedilla"
 [ NewAccents
U_0147 = &66,&18,&66,&76,&7E,&6E,&66,&00 ;ISO  "Latin capital letter N with caron"
U_0148 = &66,&18,&7C,&66,&66,&66,&66,&00 ;ISO  "Latin small letter n with caron"
 |
U_0147 = &66,&18,&00,&66,&76,&6E,&66,&00 ;ISO  "Latin capital letter N with caron"
U_0148 = &66,&18,&00,&7C,&66,&66,&66,&00 ;ISO  "Latin small letter n with caron"
 ]
U_0149 = &00,&C0,&FE,&B3,&33,&33,&33,&00 ;ISO  "Latin small letter n preceded by apostrophe"
U_014A = &66,&76,&7E,&6E,&66,&66,&06,&1C ;ISO  "Latin capital letter ENG"
U_014B = &00,&00,&7C,&66,&66,&66,&06,&1C ;ISO  "Latin small letter eng"
U_014C = &7E,&00,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with macron"
U_014D = &7E,&00,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with macron"
U_014E = &46,&3C,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with breve"
U_014F = &46,&3C,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with breve"
U_0150 = &33,&66,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter O with double acute"
U_0151 = &33,&66,&00,&3C,&66,&66,&3C,&00 ;ISO  "Latin small letter o with double acute"
U_0152 = &77,&CC,&CC,&CF,&CC,&CC,&77,&00 ;ISO  "Latin capital ligature OE"
U_0153 = &00,&00,&6E,&DB,&DF,&D8,&6E,&00 ;ISO  "Latin small ligature oe"
U_0154 = &0C,&18,&7C,&66,&7C,&6C,&66,&00 ;ISO  "Latin capital letter R with acute"
U_0155 = &0C,&18,&6C,&76,&60,&60,&60,&00 ;ISO  "Latin small letter r with acute"
U_0156 = &7C,&66,&66,&7C,&6C,&66,&66,&30 ;ISO  "Latin capital letter R with cedilla"
U_0157 = &00,&00,&6C,&76,&60,&60,&78,&0C ;ISO  "Latin small letter r with cedilla"
U_0158 = &66,&18,&7C,&66,&7C,&6C,&66,&00 ;ISO  "Latin capital letter R with caron"
U_0159 = &66,&18,&6C,&76,&60,&60,&60,&00 ;ISO  "Latin small letter r with caron"
U_015A = &0C,&18,&3E,&60,&3C,&06,&7C,&00 ;ISO  "Latin capital letter S with acute"
U_015B = &0C,&18,&3C,&60,&3C,&06,&3C,&00 ;ISO  "Latin small letter s with acute"
U_015C = &3C,&66,&3E,&60,&3C,&06,&7C,&00 ;ISO  "Latin capital letter S with circumflex"
U_015D = &3C,&66,&3C,&60,&3C,&06,&3C,&00 ;ISO  "Latin small letter s with circumflex"
U_015E = &00,&3E,&60,&3C,&06,&7C,&06,&0C ;ISO  "Latin capital letter S with cedilla"
U_015F = &00,&3C,&60,&3C,&06,&3C,&06,&0C ;ISO  "Latin small letter s with cedilla"
U_0160 = &66,&18,&3E,&60,&3C,&06,&7C,&00 ;ISO  "Latin capital letter S with caron"
U_0161 = &66,&18,&3C,&60,&3C,&06,&3C,&00 ;ISO  "Latin small letter s with caron"
U_0162 = &7E,&18,&18,&18,&18,&18,&18,&30 ;ISO  "Latin capital letter T with cedilla"
U_0163 = &30,&30,&7C,&30,&30,&30,&1C,&30 ;ISO  "Latin small letter t with cedilla"
U_0164 = &66,&18,&7E,&18,&18,&18,&18,&00 ;ISO  "Latin capital letter T with caron"
U_0165 = &66,&18,&30,&7C,&30,&30,&1C,&00 ;ISO  "Latin small letter t with caron"
U_0166 = &7E,&18,&18,&18,&7E,&18,&18,&00 ;ISO  "Latin capital letter T with stroke"
U_0167 = &30,&30,&7C,&30,&FC,&30,&1C,&00 ;ISO  "Latin small letter t with stroke"
U_0168 = &36,&6C,&00,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with tilde"
U_0169 = &36,&6C,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with tilde"
U_016A = &7E,&00,&66,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with macron"
 [ NewAccents
U_016B = &7E,&00,&66,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with macron"
 |
U_016B = &7E,&00,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with macron"
 ]
U_016C = &46,&3C,&00,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with breve"
U_016D = &46,&3C,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with breve"
U_016E = &3C,&66,&3C,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with ring above"
U_016F = &3C,&66,&3C,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with ring above"
U_0170 = &33,&66,&00,&66,&66,&66,&3C,&00 ;ISO  "Latin capital letter U with double acute"
U_0171 = &33,&66,&00,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter u with double acute"
 [ NewAccents
U_0172 = &66,&66,&66,&66,&66,&66,&3C,&06 ;ISO  "Latin capital letter U with ogonek"
U_0173 = &00,&00,&66,&66,&66,&66,&3E,&03 ;ISO  "Latin small letter u with ogonek"
U_0174 = &1C,&36,&00,&63,&6B,&7F,&63,&00 ;ISO  "Latin capital letter W with circumflex"
 |
U_0172 = &00,&00,&66,&66,&66,&66,&3C,&06 ;ISO  "Latin capital letter U with ogonek"
U_0173 = &00,&00,&00,&66,&66,&66,&3E,&03 ;ISO  "Latin small letter u with ogonek"
U_0174 = &1C,&63,&6B,&6B,&7F,&77,&63,&00 ;ISO  "Latin capital letter W with circumflex"
 ]
U_0175 = &1C,&36,&00,&6B,&6B,&7F,&36,&00 ;ISO  "Latin small letter w with circumflex"
 [ NewAccents
U_0176 = &3C,&66,&00,&66,&3C,&18,&18,&00 ;ISO  "Latin capital letter Y with circumflex"
U_0177 = &3C,&66,&00,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y with circumflex"
 |
U_0176 = &3C,&66,&42,&66,&3C,&18,&18,&00 ;ISO  "Latin capital letter Y with circumflex"
U_0177 = &3C,&66,&00,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y with circumflex"
 ]
U_0178 = &66,&00,&66,&66,&3C,&18,&18,&00 ;ISO  "Latin capital letter Y with diaeresis"
U_0179 = &0C,&18,&7E,&0C,&18,&30,&7E,&00 ;ISO  "Latin capital letter Z with acute"
U_017A = &0C,&18,&00,&7E,&0C,&30,&7E,&00 ;ISO  "Latin small letter z with acute"
U_017B = &18,&00,&7E,&0C,&18,&30,&7E,&00 ;ISO  "Latin capital letter Z with dot above"
U_017C = &18,&00,&00,&7E,&0C,&30,&7E,&00 ;ISO  "Latin small letter z with dot above"
U_017D = &66,&18,&7E,&0C,&18,&30,&7E,&00 ;ISO  "Latin capital letter Z with caron"
U_017E = &66,&18,&00,&7E,&0C,&30,&7E,&00 ;ISO  "Latin small letter z with caron"
U_017F = &1C,&30,&30,&70,&30,&30,&30,&00 ;ISO  "Latin small letter long s"

;--------------------------------------------------------------------------------
;  LATIN EXTENDED-B
;--------------------------------------------------------------------------------

U_0192 = &1C,&30,&30,&7C,&30,&30,&30,&60 ;ISO  "Latin small letter f with hook"
U_01B7 = &7C,&18,&30,&7C,&06,&66,&3C,&00 ;ISO  "Latin capital letter EZH"
U_01E4 = &3C,&66,&60,&6E,&6F,&66,&3C,&00 ;ISO  "Latin capital letter G with stroke"
U_01E5 = &00,&00,&3E,&66,&66,&3E,&0F,&3C ;ISO  "Latin small letter g with stroke"
U_01E6 = &66,&18,&3C,&60,&6E,&66,&3C,&00 ;ISO  "Latin capital letter G with caron"
U_01E7 = &66,&18,&3E,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter g with caron"
U_01E8 = &66,&18,&66,&6C,&78,&6C,&66,&00 ;ISO  "Latin capital letter K with caron"
U_01E9 = &66,&18,&60,&66,&7C,&7C,&66,&00 ;ISO  "Latin small letter k with caron"
U_01EE = &66,&FC,&30,&7C,&06,&66,&3C,&00 ;ISO  "Latin capital latter EZH with caron"
U_01EF = &66,&18,&7C,&18,&30,&7C,&06,&3C ;ISO  "Latin small letter ezh with caron"
U_0218 * U_015E                          ;ISO  "Latin capital letter S with comma below"
U_0219 * U_015F                          ;ISO  "Latin small letter s with comma below"
U_021A * U_0162                          ;ISO  "Latin capital letter T with comma below"
U_021B * U_0163                          ;ISO  "Latin small letter t with comma below"

;--------------------------------------------------------------------------------
;  IPA EXTENSIONS
;--------------------------------------------------------------------------------

U_0258 = &00,&00,&3C,&66,&7E,&06,&3C,&00 ;ISO  "Latin small letter reversed e"
U_0261 = &00,&00,&3C,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter script g"
U_0283 = &0E,&18,&18,&18,&18,&18,&18,&70 ;ISO  "Latin small letter esh"
U_0292 = &00,&00,&7C,&18,&30,&7C,&06,&3C ;ISO  "Latin small letter ezh"


;--------------------------------------------------------------------------------
;  SPACING MODIFIER LETTERS
;--------------------------------------------------------------------------------

U_02BC = &0C,&0C,&18,&00,&00,&00,&00,&00 ;ISO  "modifier letter apostrophe"
U_02BD = &18,&18,&0C,&00,&00,&00,&00,&00 ;ISO  "modifier letter reversed comma"
U_02C6 * U_005E                          ;ISO  "modifier letter circumflex accent"
U_02C7 = &66,&18,&00,&00,&00,&00,&00,&00 ;ISO  "caron"
U_02D8 = &46,&3C,&00,&00,&00,&00,&00,&00 ;ISO  "breve"
U_02D9 = &18,&00,&00,&00,&00,&00,&00,&00 ;ISO  "dot above"
U_02DA * U_00B0                          ;ISO  "ring above"
U_02DB = &00,&00,&00,&00,&00,&18,&30,&18 ;ISO  "ogonek"
U_02DC = &36,&6C,&00,&00,&00,&00,&00,&00 ;ISO  "small tilde"
U_02DD = &66,&CC,&00,&00,&00,&00,&00,&00 ;ISO  "double acute accent"


;--------------------------------------------------------------------------------
;  BASIC GREEK
;--------------------------------------------------------------------------------

U_037A = &00,&00,&00,&00,&00,&00,&18,&0C ;ISO  "Greek ypogegrammeni"
U_037E = &00,&18,&18,&00,&00,&18,&18,&30 ;ISO  "Greek question mark"
U_0384 * U_00B4                          ;ISO  "Greek tonos"
U_0385 = &0C,&18,&66,&00,&00,&00,&00,&00 ;ISO  "Greek dialytika tonos"
U_0386 = &CC,&DE,&B3,&33,&3F,&33,&33,&00 ;ISO  "Greek capital letter ALPHA with tonos"
U_0387 * U_00B7                          ;ISO  "Greek ano teleia"
U_0388 = &FF,&DB,&98,&1E,&18,&1B,&3F,&00 ;ISO  "Greek capital letter EPSILON with tonos"
U_0389 = &FB,&DB,&9B,&1F,&1B,&1B,&3B,&00 ;ISO  "Greek capital letter ETA with tonos"
U_038A = &DE,&CC,&8C,&0C,&0C,&0C,&1E,&00 ;ISO  "Greek capital letter IOTA with tonos"
U_038C = &DE,&F3,&B3,&33,&33,&33,&1E,&00 ;ISO  "Greek capital letter OMICRON with tonos"
U_038E = &F3,&F3,&B3,&1E,&0C,&0C,&1E,&00 ;ISO  "Greek capital letter UPSILON with tonos"
U_038F = &BE,&E3,&E3,&63,&36,&36,&63,&00 ;ISO  "Greek capital letter OMEGA with tonos"
U_0390 = &0C,&18,&42,&18,&18,&18,&0C,&00 ;ISO  "Greek small letter iota with dialytika and tonos"
U_0391 = &1C,&36,&63,&63,&7F,&63,&63,&00 ;ISO  "Greek capital letter ALPHA"
U_0392 = &7E,&33,&33,&3E,&33,&33,&7E,&00 ;ISO  "Greek capital letter BETA"
U_0393 = &7F,&63,&60,&60,&60,&60,&60,&00 ;ISO  "Greek capital letter GAMMA"
U_0394 = &1C,&1C,&36,&36,&63,&63,&7F,&00 ;ISO  "Greek capital letter DELTA"
U_0395 = &7F,&33,&30,&3E,&30,&33,&7F,&00 ;ISO  "Greek capital letter EPSILON"
U_0396 = &7E,&66,&0C,&18,&30,&66,&7E,&00 ;ISO  "Greek capital letter ZETA"
U_0397 = &77,&33,&33,&3F,&33,&33,&77,&00 ;ISO  "Greek capital letter ETA"
U_0398 = &3E,&63,&63,&7F,&63,&63,&3E,&00 ;ISO  "Greek capital letter THETA"
U_0399 = &3C,&18,&18,&18,&18,&18,&3C,&00 ;ISO  "Greek capital letter IOTA"
U_039A = &63,&66,&6C,&78,&6C,&66,&63,&00 ;ISO  "Greek capital letter KAPPA"
U_039B = &1C,&1C,&36,&36,&63,&63,&63,&00 ;ISO  "Greek capital letter LAMDA"
U_039C = &63,&77,&7F,&6B,&63,&63,&63,&00 ;ISO  "Greek capital letter MU"
U_039D = &63,&73,&7B,&6F,&67,&63,&63,&00 ;ISO  "Greek capital letter NU"
U_039E = &7E,&00,&00,&3C,&00,&00,&7E,&00 ;ISO  "Greek capital letter XI"
U_039F = &3E,&63,&63,&63,&63,&63,&3E,&00 ;ISO  "Greek capital letter OMICRON"
U_03A0 = &7F,&36,&36,&36,&36,&36,&36,&00 ;ISO  "Greek capital letter PI"
U_03A1 = &7E,&33,&33,&3E,&30,&30,&78,&00 ;ISO  "Greek capital letter RHO"
U_03A3 = &7F,&63,&30,&18,&30,&63,&7F,&00 ;ISO  "Greek capital letter SIGMA"
U_03A4 = &7E,&5A,&18,&18,&18,&18,&18,&00 ;ISO  "Greek capital letter TAU"
U_03A5 = &66,&66,&66,&3C,&18,&18,&3C,&00 ;ISO  "Greek capital letter UPSILON"
U_03A6 = &3E,&08,&3E,&6B,&3E,&08,&3E,&00 ;ISO  "Greek capital letter PHI"
U_03A7 = &63,&63,&36,&1C,&36,&63,&63,&00 ;ISO  "Greek capital letter CHI"
U_03A8 = &3E,&08,&6B,&6B,&3E,&08,&3E,&00 ;ISO  "Greek capital letter PSI"
U_03A9 = &3E,&63,&63,&63,&36,&36,&63,&00 ;ISO  "Greek capital letter OMEGA"
U_03AA = &66,&00,&3C,&18,&18,&18,&3C,&00 ;ISO  "Greek capital letter IOTA with dialytika"
U_03AB = &66,&00,&66,&3C,&18,&18,&3C,&00 ;ISO  "Greek capital letter UPSILON with dialytika"
U_03AC = &0C,&18,&3B,&6E,&66,&6E,&3B,&00 ;ISO  "Greek small letter alpha with tonos"
U_03AD = &0C,&18,&1E,&30,&1C,&30,&1E,&00 ;ISO  "Greek small letter epsilon with tonos"
U_03AE = &0C,&18,&7C,&66,&66,&66,&06,&06 ;ISO  "Greek small letter eta with tonos"
U_03AF = &0C,&18,&00,&18,&18,&18,&0C,&00 ;ISO  "Greek small letter iota with tonos"
U_03B0 = &0C,&18,&66,&00,&73,&33,&1E,&00 ;ISO  "Greek small letter upsilon with dialytika and tonos"
U_03B1 = &00,&00,&3B,&6E,&66,&6E,&3B,&00 ;ISO  "Greek small letter alpha"
U_03B2 = &1E,&33,&33,&3E,&33,&33,&3E,&60 ;ISO  "Greek small letter beta"
U_03B3 = &00,&00,&66,&36,&1C,&18,&30,&30 ;ISO  "Greek small letter gamma"
U_03B4 = &3C,&60,&30,&3C,&66,&66,&3C,&00 ;ISO  "Greek small letter delta"
U_03B5 = &00,&00,&1E,&30,&1C,&30,&1E,&00 ;ISO  "Greek small letter epsilon"
U_03B6 = &3E,&0C,&18,&30,&60,&60,&3E,&06 ;ISO  "Greek small letter zeta"
U_03B7 = &00,&00,&7C,&66,&66,&66,&06,&06 ;ISO  "Greek small letter eta"
U_03B8 = &3C,&66,&66,&7E,&66,&66,&3C,&00 ;ISO  "Greek small letter theta"
U_03B9 = &00,&00,&18,&18,&18,&18,&0C,&00 ;ISO  "Greek small letter iota"
U_03BA = &00,&00,&66,&6C,&78,&6C,&66,&00 ;ISO  "Greek small letter kappa"
U_03BB = &60,&30,&18,&1C,&36,&63,&63,&00 ;ISO  "Greek small letter lamda"
U_03BC = &00,&00,&33,&33,&33,&33,&3E,&60 ;ISO  "Greek small letter mu"
U_03BD = &00,&00,&63,&33,&1B,&1E,&1C,&00 ;ISO  "Greek small letter nu"
U_03BE = &0C,&3E,&60,&3C,&60,&3E,&06,&0C ;ISO  "Greek small letter xi"
U_03BF = &00,&00,&3E,&63,&63,&63,&3E,&00 ;ISO  "Greek small letter omicron"
U_03C0 = &00,&00,&7F,&36,&36,&36,&36,&00 ;ISO  "Greek small letter pi"
U_03C1 = &00,&00,&3C,&66,&66,&7C,&60,&60 ;ISO  "Greek small letter rho"
U_03C2 = &00,&00,&3E,&63,&38,&0C,&78,&00 ;ISO  "Greek small letter final sigma"
U_03C3 = &00,&00,&3F,&66,&66,&66,&3C,&00 ;ISO  "Greek small letter sigma"
U_03C4 = &00,&00,&7E,&18,&18,&18,&0C,&00 ;ISO  "Greek small letter tau"
U_03C5 = &00,&00,&73,&33,&33,&33,&1E,&00 ;ISO  "Greek small letter upsilon"
U_03C6 = &00,&00,&3E,&6B,&6B,&3E,&18,&18 ;ISO  "Greek small letter phi"
U_03C7 = &00,&00,&66,&36,&1C,&1C,&36,&33 ;ISO  "Greek small letter chi"
U_03C8 = &00,&00,&63,&6B,&6B,&3E,&18,&18 ;ISO  "Greek small letter psi"
U_03C9 = &00,&00,&63,&63,&6B,&7F,&36,&00 ;ISO  "Greek small letter omega"
U_03CA = &66,&00,&18,&18,&18,&18,&0C,&00 ;ISO  "Greek small letter iota with dialytika"
U_03CB = &66,&00,&73,&33,&33,&33,&1E,&00 ;ISO  "Greek small letter upsilon with dialytika"
U_03CC = &0C,&18,&3E,&63,&63,&63,&3E,&00 ;ISO  "Greek small letter omicron with tonos"
U_03CD = &0C,&18,&73,&33,&33,&33,&1E,&00 ;ISO  "Greek small letter upsilon with tonos"
U_03CE = &0C,&18,&63,&63,&6B,&7F,&36,&00 ;ISO  "Greek small letter omega with tonos"


;--------------------------------------------------------------------------------
;  CYRILLIC
;--------------------------------------------------------------------------------

U_0401 * U_00CB                          ;ISO  "Cyrillic capital letter IO"
U_0402 = &7E,&5A,&18,&1E,&1B,&1B,&03,&0E ;ISO  "Cyrillic capital letter DJE"
U_0403 = &0C,&18,&7E,&66,&60,&60,&60,&00 ;ISO  "Cyrillic capital letter GJE"
U_0404 = &1C,&36,&60,&78,&60,&36,&1C,&00 ;ISO  "Cyrillic capital letter Ukrainian IE"
U_0405 = &3C,&66,&60,&18,&06,&66,&3C,&00 ;ISO  "Cyrillic capital letter DZE"
U_0406 * U_0399                          ;ISO  "Cyrillic capital letter Byelorussian-Ukrainian I"
U_0407 * U_03AA                          ;ISO  "Cyrillic capital letter YI"
U_0408 = &1E,&0C,&0C,&0C,&0C,&6C,&38,&00 ;ISO  "Cyrillic capital letter JE"
U_0409 = &78,&58,&58,&5E,&5B,&DB,&9E,&00 ;ISO  "Cyrillic capital letter LJE"
U_040A = &D8,&D8,&D8,&FE,&DB,&DB,&DE,&00 ;ISO  "Cyrillic capital letter NJE"
U_040B = &7E,&5A,&18,&1E,&1B,&1B,&1B,&00 ;ISO  "Cyrillic capital letter TSHE"
U_040C = &0C,&18,&6E,&6C,&78,&6C,&6E,&00 ;ISO  "Cyrillic capital letter KJE"
U_040E = &66,&00,&66,&66,&7E,&06,&7C,&00 ;ISO  "Cyrillic capital letter short U"
U_040F = &66,&66,&66,&66,&66,&66,&7E,&08 ;ISO  "Cyrillic capital letter DZHE"
U_0410 = &3C,&66,&66,&66,&7E,&66,&66,&00 ;ISO  "Cyrillic capital letter A"
U_0411 = &7E,&60,&60,&7C,&66,&66,&7C,&00 ;ISO  "Cyrillic capital letter BE"
U_0412 = &7C,&66,&66,&78,&66,&66,&7C,&00 ;ISO  "Cyrillic capital letter VE"
U_0413 = &7E,&66,&60,&60,&60,&60,&60,&00 ;ISO  "Cyrillic capital letter GHE"
U_0414 = &1E,&36,&36,&36,&36,&7F,&63,&00 ;ISO  "Cyrillic capital letter DE"
U_0415 = &7E,&62,&60,&7C,&60,&62,&7E,&00 ;ISO  "Cyrillic capital letter IE"
U_0416 = &6B,&6B,&2A,&1C,&2A,&6B,&6B,&00 ;ISO  "Cyrillic capital letter ZHE"
U_0417 = &3E,&66,&06,&1C,&06,&66,&3E,&00 ;ISO  "Cyrillic capital letter ZE"
U_0418 = &63,&63,&67,&6B,&73,&63,&63,&00 ;ISO  "Cyrillic capital letter I"
U_0419 = &6B,&63,&67,&6B,&73,&63,&63,&00 ;ISO  "Cyrillic capital letter short I"
U_041A = &67,&66,&6C,&78,&6C,&66,&67,&00 ;ISO  "Cyrillic capital letter KA"
U_041B = &1F,&33,&33,&33,&33,&33,&63,&00 ;ISO  "Cyrillic capital letter EL"
U_041C = &63,&77,&6B,&6B,&63,&63,&63,&00 ;ISO  "Cyrillic capital letter EM"
U_041D = &63,&63,&7F,&63,&63,&63,&63,&00 ;ISO  "Cyrillic capital letter EN"
U_041E = &3E,&66,&66,&66,&66,&66,&7C,&00 ;ISO  "Cyrillic capital letter O"
U_041F = &7E,&66,&66,&66,&66,&66,&66,&00 ;ISO  "Cyrillic capital letter PE"
U_0420 = &7E,&66,&66,&7C,&60,&60,&60,&00 ;ISO  "Cyrillic capital letter ER"
U_0421 = &3E,&66,&60,&60,&60,&66,&7C,&00 ;ISO  "Cyrillic capital letter ES"
U_0422 = &7E,&5A,&18,&18,&18,&18,&18,&00 ;ISO  "Cyrillic capital letter TE"
U_0423 = &66,&66,&66,&7E,&06,&06,&7C,&00 ;ISO  "Cyrillic capital letter U"
U_0424 = &08,&7F,&6B,&6B,&6B,&6B,&7F,&08 ;ISO  "Cyrillic capital letter EF"
U_0425 = &66,&66,&24,&18,&24,&66,&66,&00 ;ISO  "Cyrillic capital letter HA"
U_0426 = &6C,&6C,&6C,&6C,&6C,&7E,&06,&00 ;ISO  "Cyrillic capital letter TSE"
U_0427 = &66,&66,&66,&3E,&06,&06,&06,&00 ;ISO  "Cyrillic capital letter CHE"
U_0428 = &6B,&6B,&6B,&6B,&6B,&6B,&7F,&00 ;ISO  "Cyrillic capital letter SHA"
U_0429 = &6B,&6B,&6B,&6B,&6B,&6B,&7F,&03 ;ISO  "Cyrillic capital letter SHCHA"
U_042A = &78,&58,&18,&1E,&1B,&1B,&1E,&00 ;ISO  "Cyrillic capital letter HARD SIGN"
U_042B = &C3,&C3,&C3,&F3,&DB,&DB,&F3,&00 ;ISO  "Cyrillic capital letter YERU"
U_042C = &60,&60,&60,&7C,&66,&66,&7C,&00 ;ISO  "Cyrillic capital letter SOFT SIGN"
U_042D = &38,&6C,&06,&1E,&06,&6C,&38,&00 ;ISO  "Cyrillic capital letter E"
U_042E = &CE,&DB,&DB,&FB,&DB,&DB,&CE,&00 ;ISO  "Cyrillic capital letter YU"
U_042F = &3E,&66,&66,&3E,&36,&66,&66,&00 ;ISO  "Cyrillic capital letter YA"
U_0430 = &00,&00,&3E,&06,&3E,&66,&3E,&00 ;ISO  "Cyrillic small letter a"
U_0431 = &0E,&38,&60,&7C,&66,&66,&3C,&00 ;ISO  "Cyrillic small letter be"
U_0432 = &00,&00,&7C,&66,&7C,&66,&7C,&00 ;ISO  "Cyrillic small letter ve"
U_0433 = &00,&00,&7E,&66,&60,&60,&60,&00 ;ISO  "Cyrillic small letter ghe"
U_0434 = &00,&00,&1C,&2C,&2C,&7E,&66,&00 ;ISO  "Cyrillic small letter de"
U_0435 = &00,&00,&3C,&66,&7E,&60,&3E,&00 ;ISO  "Cyrillic small letter ie"
U_0436 = &00,&00,&6B,&6B,&3E,&6B,&6B,&00 ;ISO  "Cyrillic small letter zhe"
U_0437 = &00,&00,&3C,&66,&0C,&66,&3C,&00 ;ISO  "Cyrillic small letter ze"
U_0438 = &00,&00,&63,&6F,&7B,&63,&63,&00 ;ISO  "Cyrillic small letter i"
U_0439 = &00,&08,&63,&6F,&7B,&63,&63,&00 ;ISO  "Cyrillic small letter short i"
U_043A = &00,&00,&66,&6C,&78,&6C,&66,&00 ;ISO  "Cyrillic small letter ka"
U_043B = &00,&00,&1F,&33,&33,&33,&63,&00 ;ISO  "Cyrillic small letter el"
U_043C = &00,&00,&63,&77,&6B,&63,&63,&00 ;ISO  "Cyrillic small letter em"
U_043D = &00,&00,&66,&66,&7E,&66,&66,&00 ;ISO  "Cyrillic small letter en"
U_043E = &00,&00,&3E,&66,&66,&66,&7C,&00 ;ISO  "Cyrillic small letter o"
U_043F = &00,&00,&7E,&66,&66,&66,&66,&00 ;ISO  "Cyrillic small letter pe"
U_0440 = &00,&00,&7E,&66,&66,&7C,&60,&60 ;ISO  "Cyrillic small letter er"
U_0441 = &00,&00,&3E,&66,&60,&66,&7C,&00 ;ISO  "Cyrillic small letter es"
U_0442 = &00,&00,&7E,&5A,&18,&18,&18,&00 ;ISO  "Cyrillic small letter te"
U_0443 = &00,&00,&66,&66,&66,&7E,&06,&3C ;ISO  "Cyrillic small letter u"
U_0444 = &00,&08,&7F,&6B,&6B,&6B,&7F,&08 ;ISO  "Cyrillic small letter ef"
U_0445 = &00,&00,&66,&3C,&18,&3C,&66,&00 ;ISO  "Cyrillic small letter ha"
U_0446 = &00,&00,&66,&66,&66,&66,&7F,&03 ;ISO  "Cyrillic small letter tse"
U_0447 = &00,&00,&66,&66,&3E,&06,&06,&00 ;ISO  "Cyrillic small letter che"
U_0448 = &00,&00,&6B,&6B,&6B,&6B,&7F,&00 ;ISO  "Cyrillic small letter sha"
U_0449 = &00,&00,&6B,&6B,&6B,&6B,&7F,&01 ;ISO  "Cyrillic small letter shcha"
U_044A = &00,&00,&70,&30,&3C,&36,&3C,&00 ;ISO  "Cyrillic small letter hard sign"
U_044B = &00,&00,&C3,&C3,&F3,&DB,&F3,&00 ;ISO  "Cyrillic small letter yeru"
U_044C = &00,&00,&60,&60,&7C,&66,&7C,&00 ;ISO  "Cyrillic small letter soft sign"
U_044D = &00,&00,&3C,&66,&0E,&66,&3C,&00 ;ISO  "Cyrillic small letter e"
U_044E = &00,&00,&4E,&5B,&7B,&5B,&4E,&00 ;ISO  "Cyrillic small letter yu"
U_044F = &00,&00,&3E,&66,&3E,&66,&66,&00 ;ISO  "Cyrillic small letter ya"
U_0451 = &66,&00,&3C,&66,&7E,&60,&3E,&00 ;ISO  "Cyrillic small letter io"
U_0452 = &60,&FC,&60,&7C,&66,&66,&66,&0C ;ISO  "Cyrillic small letter dje"
U_0453 = &0C,&18,&00,&7E,&66,&60,&60,&00 ;ISO  "Cyrillic small letter gje"
U_0454 = &00,&00,&3C,&66,&70,&66,&3C,&00 ;ISO  "Cyrillic small letter Ukrainian ie"
U_0455 = &00,&00,&3E,&60,&18,&06,&7C,&00 ;ISO  "Cyrillic small letter dze"
U_0456 = &18,&00,&38,&18,&18,&18,&18,&00 ;ISO  "Cyrillic small letter Byelorussian-Ukrainian i"
U_0457 = &66,&00,&38,&18,&18,&18,&18,&00 ;ISO  "Cyrillic small letter yi"
U_0458 = &18,&00,&18,&18,&18,&18,&18,&70 ;ISO  "Cyrillic small letter je"
U_0459 = &00,&00,&78,&58,&5E,&5B,&9E,&00 ;ISO  "Cyrillic small letter lje"
U_045A = &00,&00,&58,&58,&7E,&5B,&5E,&00 ;ISO  "Cyrillic small letter nje"
U_045B = &60,&FC,&60,&7C,&66,&66,&66,&00 ;ISO  "Cyrillic small letter tshe"
U_045C = &0C,&18,&66,&6C,&78,&6C,&66,&00 ;ISO  "Cyrillic small letter kje"
U_045E = &66,&00,&66,&66,&66,&7E,&06,&3C ;ISO  "Cyrillic small letter short u"
U_045F = &00,&00,&66,&66,&66,&66,&7E,&08 ;ISO  "Cyrillic small letter dzhe"


;--------------------------------------------------------------------------------
;  BASIC HEBREW
;--------------------------------------------------------------------------------

U_05D0 = &00,&33,&1B,&3F,&36,&33,&00,&00 ;ISO  "Hebrew letter ALEPH"
U_05D1 = &00,&3E,&06,&06,&06,&3F,&00,&00 ;ISO  "Hebrew letter BET"
U_05D2 = &00,&3F,&03,&0F,&1B,&33,&00,&00 ;ISO  "Hebrew letter GIMEL"
U_05D3 = &00,&3F,&06,&06,&06,&06,&00,&00 ;ISO  "Hebrew letter DALET"
U_05D4 = &00,&3F,&03,&33,&33,&33,&00,&00 ;ISO  "Hebrew letter HE"
U_05D5 = &00,&1E,&06,&06,&06,&06,&00,&00 ;ISO  "Hebrew letter VAV"
U_05D6 = &00,&1C,&0F,&0C,&0C,&0C,&00,&00 ;ISO  "Hebrew letter ZAYIN"
U_05D7 = &00,&3F,&33,&33,&33,&33,&00,&00 ;ISO  "Hebrew letter HET"
U_05D8 = &00,&37,&3B,&33,&33,&3F,&00,&00 ;ISO  "Hebrew letter TET"
U_05D9 = &00,&1E,&06,&06,&00,&00,&00,&00 ;ISO  "Hebrew letter YOD"
U_05DA = &00,&3F,&03,&03,&03,&03,&03,&03 ;ISO  "Hebrew letter FINAL KAF"
U_05DB = &00,&3F,&03,&03,&03,&3F,&00,&00 ;ISO  "Hebrew letter KAF"
U_05DC = &30,&3F,&03,&06,&0C,&18,&00,&00 ;ISO  "Hebrew letter LAMED"
U_05DD = &00,&3F,&33,&33,&33,&3F,&00,&00 ;ISO  "Hebrew letter FINAL MEM"
U_05DE = &00,&37,&1B,&33,&03,&3F,&00,&00 ;ISO  "Hebrew letter MEM"
U_05DF = &00,&1E,&06,&06,&06,&06,&06,&06 ;ISO  "Hebrew letter FINAL NUN"
U_05E0 = &00,&1E,&06,&06,&06,&3E,&00,&00 ;ISO  "Hebrew letter NUN"
U_05E1 = &00,&3F,&33,&33,&33,&1E,&00,&00 ;ISO  "Hebrew letter SAMEKH"
U_05E2 = &00,&1B,&1B,&1B,&0F,&3F,&00,&00 ;ISO  "Hebrew letter AYIN"
U_05E3 = &00,&3F,&33,&3B,&03,&03,&03,&03 ;ISO  "Hebrew letter FINAL PE"
U_05E4 = &00,&3F,&33,&3B,&03,&3F,&00,&00 ;ISO  "Hebrew letter PE"
U_05E5 = &00,&33,&36,&3C,&30,&30,&30,&30 ;ISO  "Hebrew letter FINAL TSADI"
U_05E6 = &00,&33,&1B,&0C,&03,&3F,&00,&00 ;ISO  "Hebrew letter TSADI"
U_05E7 = &00,&3F,&03,&33,&36,&30,&30,&00 ;ISO  "Hebrew letter QOF"
U_05E8 = &00,&3F,&03,&03,&03,&03,&00,&00 ;ISO  "Hebrew letter RESH"
U_05E9 = &00,&5B,&5B,&5F,&43,&3E,&00,&00 ;ISO  "Hebrew letter SHIN"
U_05EA = &00,&1F,&1B,&1B,&1B,&3B,&00,&00 ;ISO  "Hebrew letter TAV"


;--------------------------------------------------------------------------------
;  LATIN EXTENDED ADDITIONAL
;--------------------------------------------------------------------------------

U_1E02 = &18,&00,&7C,&66,&7C,&66,&7C,&00 ;ISO  "Latin capital letter B with dot above"
U_1E03 = &6C,&60,&7C,&66,&66,&66,&7C,&00 ;ISO  "Latin small letter b with dot above"
U_1E0A = &18,&00,&7C,&66,&66,&66,&7C,&00 ;ISO  "Latin capital letter D with dot above"
U_1E0B = &36,&06,&3E,&66,&66,&66,&3E,&00 ;ISO  "Latin small letter d with dot above"
U_1E1E = &18,&00,&7E,&60,&7C,&60,&60,&00 ;ISO  "Latin capital letter F with dot above"
U_1E1F = &18,&00,&1C,&30,&7C,&30,&30,&00 ;ISO  "Latin small letter f with dot above"
U_1E40 = &18,&00,&63,&77,&7F,&6B,&63,&00 ;ISO  "Latin capital letter M with dot above"
U_1E41 = &18,&00,&36,&7F,&6B,&6B,&63,&00 ;ISO  "Latin small letter m with dot above"
U_1E56 = &18,&00,&7C,&66,&7C,&60,&60,&00 ;ISO  "Latin capital letter P with dot above"
U_1E57 = &18,&00,&7C,&66,&66,&7C,&60,&60 ;ISO  "Latin small letter p with dot above"
U_1E60 = &18,&00,&3E,&60,&3C,&06,&7C,&00 ;ISO  "Latin capital letter S with dot above"
U_1E61 = &18,&00,&3C,&60,&3C,&06,&3C,&00 ;ISO  "Latin small letter s with dot above"
U_1E6A = &18,&00,&7E,&18,&18,&18,&18,&00 ;ISO  "Latin capital letter T with dot above"
U_1E6B = &18,&00,&30,&7C,&30,&30,&1C,&00 ;ISO  "Latin small letter t with dot above"
U_1E80 = &18,&0C,&63,&6B,&7F,&77,&63,&00 ;ISO  "Latin capital letter W with grave"
U_1E81 = &18,&0C,&63,&6B,&6B,&7F,&36,&00 ;ISO  "Latin small letter w with grave"
U_1E82 = &0C,&18,&63,&6B,&7F,&77,&63,&00 ;ISO  "Latin capital letter W with acute"
U_1E83 = &0C,&18,&63,&6B,&6B,&7F,&36,&00 ;ISO  "Latin small letter w with acute"
U_1E84 = &36,&00,&63,&6B,&7F,&77,&63,&00 ;ISO  "Latin capital letter W with diaeresis"
U_1E85 = &36,&00,&63,&6B,&6B,&7F,&36,&00 ;ISO  "Latin small letter w with diaeresis"
U_1ECD = &00,&00,&3C,&66,&66,&3C,&00,&18 ;ISO  "Latin small letter o with dot below"
U_1EEF = &6F,&DB,&01,&CC,&CC,&CC,&7C,&00 ;ISO  "Latin small letter u with horn and tilde"
U_1EF1 = &03,&03,&CD,&CC,&CC,&7C,&00,&30 ;ISO  "Latin small letter u with horn and dot below"
U_1EF2 = &30,&18,&66,&66,&3C,&18,&18,&00 ;ISO  "Latin capital letter Y with grave"
U_1EF3 = &30,&18,&66,&66,&66,&3E,&06,&3C ;ISO  "Latin small letter y with grave"


;--------------------------------------------------------------------------------
;  GENERAL PUNCTUATION
;--------------------------------------------------------------------------------

U_2000 * U_0020                          ;ISO  "en quad"
U_2001 * U_0020                          ;ISO  "em quad"
U_2002 * U_0020                          ;ISO  "en space"
U_2003 * U_0020                          ;ISO  "em space"
U_2004 * U_0020                          ;ISO  "three-per-em space"
U_2005 * U_0020                          ;ISO  "four-per-em space"
U_2006 * U_0020                          ;ISO  "six-per-em space"
U_2007 * U_0020                          ;ISO  "figure space"
U_2008 * U_0020                          ;ISO  "punctuation space"
U_2009 * U_0020                          ;ISO  "thin space"
U_200A * U_0020                          ;ISO  "hair space"
U_200E = &FF,&F7,&F3,&81,&F3,&F7,&FF,&FF ;ISO  "left-to-right mark"
U_200F = &FF,&EF,&CF,&81,&CF,&EF,&FF,&FF ;ISO  "right-to-left mark"
U_2010 * U_002D                          ;ISO  "hyphen"
U_2011 * U_002D                          ;ISO  "non-breaking hyphen"
U_2012 * U_002D                          ;ISO  "figure dash"
U_2013 = &00,&00,&00,&3C,&00,&00,&00,&00 ;ISO  "en dash"
U_2014 = &00,&00,&00,&FF,&00,&00,&00,&00 ;ISO  "em dash"
U_2015 * U_2014                          ;ISO  "horizontal bar"
U_2016 = &36,&36,&36,&36,&36,&36,&36,&00 ;ISO  "double vertical line"
U_2017 = &00,&00,&00,&00,&00,&FF,&00,&FF ;ISO  "double low line"
U_2018 = &0C,&18,&18,&00,&00,&00,&00,&00 ;ISO  "left single quotation mark"
U_2019 * U_02BC                          ;ISO  "right single quotation mark"
U_201A * U_002C                          ;ISO  "single low-9 quotation mark"
U_201B * U_02BD                          ;ISO  "single high-reversed-9 quotation mark"
U_201C = &1B,&36,&36,&00,&00,&00,&00,&00 ;ISO  "left double quotation mark"
U_201D = &36,&36,&6C,&00,&00,&00,&00,&00 ;ISO  "right double quotation mark"
U_201E = &00,&00,&00,&00,&00,&36,&36,&6C ;ISO  "double low-9 quotation mark"
U_201F = &36,&36,&1B,&00,&00,&00,&00,&00 ;ISO  "double high-reversed-9 quotation mark"
U_2020 = &18,&18,&7E,&18,&18,&18,&18,&18 ;ISO  "dagger"
 [ DoBfont
B_2020 = &18,&7E,&18,&18,&18,&18,&18,&00 ;BFNT "dagger"
 ]
U_2021 = &18,&18,&7E,&18,&7E,&18,&18,&18 ;ISO  "double dagger"
 [ DoBfont
B_2021 = &18,&7E,&18,&18,&18,&7E,&18,&00 ;BFNT "double dagger"
 ]
U_2022 = &00,&00,&3C,&7E,&7E,&3C,&00,&00 ;ISO  "bullet"
U_2023 = &00,&00,&00,&18,&3C,&7E,&00,&00 ;ISO  "triangular bullet"
U_2024 * U_002E                          ;ISO  "one dot leader"
U_2025 = &00,&00,&00,&00,&00,&66,&66,&00 ;ISO  "two dot leader"
U_2026 = &00,&00,&00,&00,&00,&DB,&DB,&00 ;ISO  "horizontal ellipsis"
U_2027 * U_00B7                          ;ISO  "hyphenation point"
U_202A = &FF,&CF,&C7,&C3,&C7,&CF,&FF,&FF ;ISO  "left-to-right embedding"
U_202B = &FF,&F3,&E3,&C3,&E3,&F3,&FF,&FF ;ISO  "right-to-left embedding"
U_202C = &FF,&83,&99,&99,&83,&9F,&9F,&FF ;ISO  "pop directional formatting"
U_202D = &FF,&E7,&83,&F9,&83,&E7,&FF,&FF ;ISO  "left-to-right override"
U_202E = &FF,&E7,&C1,&9F,&C1,&E7,&FF,&FF ;ISO  "right-to-left override"
U_2030 = &C0,&CC,&18,&30,&60,&DB,&1B,&00 ;ISO  "per mille sign"
U_2031 = &C0,&CC,&18,&30,&60,&DF,&1F,&00 ;ISO  "per ten thousand sign"
U_2032 * B_0027                          ;ISO  "prime"
U_2033 = &33,&66,&CC,&00,&00,&00,&00,&00 ;ISO  "double prime"
U_2034 = &6D,&DB,&B6,&00,&00,&00,&00,&00 ;ISO  "triple prime"
U_2035 = &30,&18,&0C,&00,&00,&00,&00,&00 ;ISO  "reversed prime"
U_2036 = &CC,&66,&33,&00,&00,&00,&00,&00 ;ISO  "reversed double prime"
U_2037 = &B6,&DB,&6D,&00,&00,&00,&00,&00 ;ISO  "reversed triple prime"
U_2038 = &00,&00,&00,&00,&00,&00,&18,&66 ;ISO  "caret"
U_2039 = &00,&0C,&18,&30,&30,&18,&0C,&00 ;ISO  "single left-pointing angle quotation mark"
U_203A = &00,&30,&18,&0C,&0C,&18,&30,&00 ;ISO  "single right-pointing angle quotation mark"
U_203B = &99,&42,&24,&99,&99,&24,&42,&99 ;ISO  "reference mark"
U_203C = &66,&66,&66,&66,&66,&00,&66,&00 ;ISO  "double exclamation mark"
U_203D = &3C,&7E,&1C,&18,&18,&00,&18,&00 ;ISO  "interrobang"
U_203E = &FF,&00,&00,&00,&00,&00,&00,&00 ;ISO  "overline"
U_203F = &00,&00,&00,&00,&00,&00,&81,&7E ;ISO  "undertie"
U_2040 = &7E,&81,&00,&00,&00,&00,&00,&00 ;ISO  "character tie"
U_2041 = &00,&00,&00,&00,&00,&06,&18,&66 ;ISO  "caret insertion point"
U_2042 = &00,&18,&3C,&18,&66,&FF,&66,&00 ;ISO  "asterism"
U_2043 = &00,&00,&00,&3C,&3C,&00,&00,&00 ;ISO  "hyphen bullet"
U_2044 = &03,&06,&0C,&18,&30,&60,&00,&00 ;ISO  "fraction slash"
U_2045 = &7C,&60,&60,&78,&60,&60,&7C,&00 ;ISO  "left square bracket with quill"
U_2046 = &3E,&06,&06,&1E,&06,&06,&3E,&00 ;ISO  "right square bracket with quill"


;--------------------------------------------------------------------------------
;  SUPERSCRIPTS AND SUBSCRIPTS
;--------------------------------------------------------------------------------

U_2070 = &18,&24,&24,&24,&18,&00,&00,&00 ;ISO  "superscript zero"
U_2074 = &08,&18,&28,&3C,&08,&00,&00,&00 ;ISO  "superscript four"
U_2075 = &3C,&20,&38,&04,&38,&00,&00,&00 ;ISO  "superscript five"
U_2076 = &18,&20,&38,&24,&18,&00,&00,&00 ;ISO  "superscript six"
U_2077 = &3C,&04,&04,&08,&08,&00,&00,&00 ;ISO  "superscript seven"
U_2078 = &18,&24,&18,&24,&18,&00,&00,&00 ;ISO  "superscript eight"
U_2079 = &18,&24,&1C,&04,&18,&00,&00,&00 ;ISO  "superscript nine"
U_207A = &00,&10,&38,&10,&00,&00,&00,&00 ;ISO  "superscript plus sign"
U_207B = &00,&00,&38,&00,&00,&00,&00,&00 ;ISO  "superscript minus"
U_207C = &00,&38,&00,&38,&00,&00,&00,&00 ;ISO  "superscript equals sign"
U_207D = &08,&10,&10,&10,&08,&00,&00,&00 ;ISO  "superscript left parenthesis"
U_207E = &10,&08,&08,&08,&10,&00,&00,&00 ;ISO  "superscript right parenthesis"
U_207F = &00,&38,&24,&24,&24,&00,&00,&00 ;ISO  "superscript latin small letter n"
U_2080 = &00,&00,&00,&18,&24,&24,&24,&18 ;ISO  "subscript zero"
U_2081 = &00,&00,&00,&10,&30,&10,&10,&38 ;ISO  "subscript one"
U_2082 = &00,&00,&00,&38,&04,&18,&20,&3C ;ISO  "subscript two"
U_2083 = &00,&00,&00,&38,&04,&18,&04,&38 ;ISO  "subscript three"
U_2084 = &00,&00,&00,&08,&18,&28,&3C,&08 ;ISO  "subscript four"
U_2085 = &00,&00,&00,&3C,&20,&38,&04,&38 ;ISO  "subscript five"
U_2086 = &00,&00,&00,&18,&20,&38,&24,&18 ;ISO  "subscript six"
U_2087 = &00,&00,&00,&3C,&04,&04,&08,&08 ;ISO  "subscript seven"
U_2088 = &00,&00,&00,&18,&24,&18,&24,&18 ;ISO  "subscript eight"
U_2089 = &00,&00,&00,&18,&24,&1C,&04,&18 ;ISO  "subscript nine"
U_208A = &00,&00,&00,&00,&10,&38,&10,&00 ;ISO  "subscript plus sign"
U_208B = &00,&00,&00,&00,&00,&38,&00,&00 ;ISO  "subscript minus"
U_208C = &00,&00,&00,&00,&38,&00,&38,&00 ;ISO  "subscript equals sign"
U_208D = &00,&00,&00,&08,&10,&10,&10,&08 ;ISO  "subscript left parenthesis"
U_208E = &00,&00,&00,&10,&08,&08,&08,&10 ;ISO  "subscript right parenthesis"


;--------------------------------------------------------------------------------
;  CURRENCY SYMBOLS
;--------------------------------------------------------------------------------

U_20AC = &3C,&66,&60,&F8,&60,&66,&3C,&00 ;ISO  "euro sign"
U_20AF = &78,&6C,&66,&66,&66,&6B,&7B,&02 ;ISO  "drachma sign"


;--------------------------------------------------------------------------------
;  LETTERLIKE SYMBOLS
;--------------------------------------------------------------------------------

U_2116 = &92,&95,&D5,&F5,&B2,&90,&97,&00 ;ISO  "numero sign"
U_2122 = &F1,&5B,&55,&51,&00,&00,&00,&00 ;ISO  "trade mark sign"
U_2126 * U_03A9                          ;ISO  "Ohm sign"


;--------------------------------------------------------------------------------
;  NUMBER FORMS
;--------------------------------------------------------------------------------
U_215B = &40,&C0,&40,&4F,&49,&0F,&09,&0F ;ISO  "vulgar fraction one eighth"
U_215C = &E0,&20,&E0,&2F,&E9,&0F,&09,&0F ;ISO  "vulgar fraction three eighths"
U_215D = &E0,&80,&E0,&2F,&E9,&0F,&09,&0F ;ISO  "vulgar fraction five eighths"
U_215E = &E0,&20,&20,&2F,&29,&0F,&09,&0F ;ISO  "vulgar fraction seven eighths"


;--------------------------------------------------------------------------------
;  ARROWS
;--------------------------------------------------------------------------------

U_2190 = &00,&18,&38,&7F,&38,&18,&00,&00 ;ISO  "leftwards arrow"
U_2191 = &00,&18,&3C,&7E,&18,&18,&18,&18 ;ISO  "upwards arrow"
U_2192 = &00,&18,&1C,&FE,&1C,&18,&00,&00 ;ISO  "rightwards arrow"
U_2193 = &18,&18,&18,&18,&7E,&3C,&18,&00 ;ISO  "downwards arrow"


;--------------------------------------------------------------------------------
;  MATHEMATICAL OPERATORS
;--------------------------------------------------------------------------------

U_2202 = &38,&0C,&06,&3E,&66,&66,&3C,&00 ;ISO  "partial differential"
U_2205 = &3E,&63,&67,&6B,&73,&63,&3E,&00 ;ISO  "empty set"
U_2206 * U_0394                          ;ISO  "increment"
U_2207 = &7F,&63,&63,&36,&36,&1C,&1C,&00 ;ISO  "nabla"
U_220F * U_03A0                          ;ISO  "n-ary product"
U_2211 * U_03A3                          ;ISO  "n-ary summation"
U_2212 = &00,&00,&00,&7E,&00,&00,&00,&00 ;ISO  "minus sign"
U_2213 = &00,&7E,&00,&18,&18,&7E,&18,&18 ;ISO  "minus-or-plus sign"
U_2219 * U_2022                          ;ISO  "bullet operator"
U_221A = &03,&03,&06,&06,&76,&1C,&0C,&00 ;ISO  "square root"
U_2229 = &00,&3C,&66,&66,&66,&66,&66,&00 ;ISO  "intersection"
U_222A = &00,&66,&66,&66,&66,&66,&3C,&00 ;ISO  "union"
U_2243 = &00,&31,&6B,&46,&00,&7F,&00,&00 ;ISO  "asymptotically equal to"
U_2248 = &00,&39,&4E,&00,&39,&4E,&00,&00 ;ISO  "almost equal to"
U_2260 = &06,&0C,&7E,&18,&7E,&30,&60,&00 ;ISO  "not equal to"
U_2261 = &00,&7E,&00,&7E,&00,&7E,&00,&00 ;ISO  "identical to"
U_2264 = &07,&1C,&70,&1C,&07,&00,&7F,&00 ;ISO  "less-than or equal to"
U_2265 = &70,&1C,&07,&1C,&70,&00,&7F,&00 ;ISO  "greater-than or equal to"
U_2266 * U_2264                          ;ISO  "less-than over equal to"
U_2267 * U_2265                          ;ISO  "greater-than over equal to"


;--------------------------------------------------------------------------------
;  MISCELLANEOUS TECHNICAL
;--------------------------------------------------------------------------------

U_2320 = &00,&0E,&18,&18,&18,&18,&18,&18 ;ISO  "top half integral"
U_2321 = &18,&18,&18,&18,&18,&18,&70,&00 ;ISO  "bottom half integral"


;--------------------------------------------------------------------------------
;  BOX DRAWING
;--------------------------------------------------------------------------------

U_2500 = &00,&00,&00,&FF,&00,&00,&00,&00 ;ISO  "box drawings light horizontal"
U_2502 = &18,&18,&18,&18,&18,&18,&18,&18 ;ISO  "box drawings light vertical"
U_250C = &00,&00,&00,&1F,&18,&18,&18,&18 ;ISO  "box drawings light down and right"
U_2510 = &00,&00,&00,&F8,&18,&18,&18,&18 ;ISO  "box drawings light down and left"
U_2514 = &18,&18,&18,&1F,&00,&00,&00,&00 ;ISO  "box drawings light up and right"
U_2518 = &18,&18,&18,&F8,&00,&00,&00,&00 ;ISO  "box drawings light up and left"
U_251C = &18,&18,&18,&1F,&18,&18,&18,&18 ;ISO  "box drawings light vertical and right"
U_2524 = &18,&18,&18,&F8,&18,&18,&18,&18 ;ISO  "box drawings light vertical and left"
U_252C = &00,&00,&00,&FF,&18,&18,&18,&18 ;ISO  "box drawings light down and horizontal"
U_2534 = &18,&18,&18,&FF,&00,&00,&00,&00 ;ISO  "box drawings light up and horizontal"
U_253C = &18,&18,&18,&FF,&18,&18,&18,&18 ;ISO  "box drawings light vertical and horizontal"
U_256D = &00,&00,&00,&07,&0C,&18,&18,&18 ;ISO  "box drawings light arc down and right"
U_256E = &00,&00,&00,&E0,&30,&18,&18,&18 ;ISO  "box drawings light arc down and left"
U_256F = &18,&18,&30,&E0,&00,&00,&00,&00 ;ISO  "box drawings light arc up and left"
U_2570 = &18,&18,&0C,&07,&00,&00,&00,&00 ;ISO  "box drawings light arc up and right"
U_2574 = &00,&00,&00,&F8,&00,&00,&00,&00 ;ISO  "box drawings light left"
U_2575 = &18,&18,&18,&18,&00,&00,&00,&00 ;ISO  "box drowings light up"
U_2576 = &00,&00,&00,&1F,&00,&00,&00,&00 ;ISO  "box drawings light right"
U_2577 = &00,&00,&00,&18,&18,&18,&18,&18 ;ISO  "box drawings light down"
U_2580 = &FF,&FF,&FF,&FF,&00,&00,&00,&00 ;ISO  "upper half block"
U_2584 = &00,&00,&00,&00,&FF,&FF,&FF,&FF ;ISO  "lower half block"
U_2588 = &FF,&FF,&FF,&FF,&FF,&FF,&FF,&FF ;ISO  "full block"
U_258C = &F0,&F0,&F0,&F0,&F0,&F0,&F0,&F0 ;ISO  "left half block"
U_2590 = &0F,&0F,&0F,&0F,&0F,&0F,&0F,&0F ;ISO  "right half block"
U_2591 = &88,&22,&88,&22,&88,&22,&88,&22 ;ISO  "light shade"
U_2592 = &AA,&55,&AA,&55,&AA,&55,&AA,&55 ;ISO  "medium shade"
U_2593 = &EE,&BB,&EE,&BB,&EE,&BB,&EE,&BB ;ISO  "dark shade"


;--------------------------------------------------------------------------------
;  GEOMETRIC SHAPES
;--------------------------------------------------------------------------------
U_25A0 = &00,&00,&00,&3C,&3C,&00,&00,&00 ;ISO  "black square"
U_25EF = &00,&3C,&7E,&7E,&7E,&7E,&3C,&00 ;ISO  "large circle"

;--------------------------------------------------------------------------------
;  MISCELLANEOUS SYMBOLS
;--------------------------------------------------------------------------------
U_266A = &18,&1C,&1E,&1A,&18,&78,&70,&00 ;ISO  "eighth note"


;--------------------------------------------------------------------------------
;  ALPHABETIC PRESENTATION FORMS
;--------------------------------------------------------------------------------

U_FB01 = &3C,&66,&60,&F6,&66,&66,&66,&00 ;ISO  "Latin small ligature fi"
U_FB02 = &3E,&66,&66,&F6,&66,&66,&66,&00 ;ISO  "Latin small ligature fl"


;--------------------------------------------------------------------------------
;  SPECIALS
;--------------------------------------------------------------------------------

U_FFFD = &FF,&C3,&99,&F3,&E7,&FF,&E7,&FF ;ISO  "replacement character"


;================================================================================
;  Table to look up character number->definition
;================================================================================

        MACRO
        NEWUCS  $base, $top
        DCD     $base
        [ "$top" <> ""
        DCD     $top
        |
        DCD     $base
        ]
        MEND

        MACRO
        UCSEntry $name
        [ "$name"<> "UNK001"
        DCW     $name-FontTable
        |
        DCW     &FFFF
        ]
        MEND

        MACRO
        UCS     $f0, $f1, $f2, $f3, $f4, $f5, $f6, $f7
        [ "$f0"<>""
        UCSEntry $f0
        ]
        [ "$f1"<>""
        UCSEntry $f1
        ]
        [ "$f2"<>""
        UCSEntry $f2
        ]
        [ "$f3"<>""
        UCSEntry $f3
        ]
        [ "$f4"<>""
        UCSEntry $f4
        ]
        [ "$f5"<>""
        UCSEntry $f5
        ]
        [ "$f6"<>""
        UCSEntry $f6
        ]
        [ "$f7"<>""
        UCSEntry $f7
        ]
        MEND

UCSTable
        NEWUCS  &20, &7E
        UCS     U_0020, U_0021, U_0022, U_0023, U_0024, U_0025, U_0026, U_0027
        UCS     U_0028, U_0029, U_002A, U_002B, U_002C, U_002D, U_002E, U_002F
        UCS     U_0030, U_0031, U_0032, U_0033, U_0034, U_0035, U_0036, U_0037
        UCS     U_0038, U_0039, U_003A, U_003B, U_003C, U_003D, U_003E, U_003F
        UCS     U_0040, U_0041, U_0042, U_0043, U_0044, U_0045, U_0046, U_0047
        UCS     U_0048, U_0049, U_004A, U_004B, U_004C, U_004D, U_004E, U_004F
        UCS     U_0050, U_0051, U_0052, U_0053, U_0054, U_0055, U_0056, U_0057
        UCS     U_0058, U_0059, U_005A, U_005B, U_005C, U_005D, U_005E, U_005F
        UCS     U_0060, U_0061, U_0062, U_0063, U_0064, U_0065, U_0066, U_0067
        UCS     U_0068, U_0069, U_006A, U_006B, U_006C, U_006D, U_006E, U_006F
        UCS     U_0070, U_0071, U_0072, U_0073, U_0074, U_0075, U_0076, U_0077
        UCS     U_0078, U_0079, U_007A, U_007B, U_007C, U_007D, U_007E

        NEWUCS  &A0, &17F
        UCS     U_00A0, U_00A1, U_00A2, U_00A3, U_00A4, U_00A5, U_00A6, U_00A7
        UCS     U_00A8, U_00A9, U_00AA, U_00AB, U_00AC, U_00AD, U_00AE, U_00AF
        UCS     U_00B0, U_00B1, U_00B2, U_00B3, U_00B4, U_00B5, U_00B6, U_00B7
        UCS     U_00B8, U_00B9, U_00BA, U_00BB, U_00BC, U_00BD, U_00BE, U_00BF
        UCS     U_00C0, U_00C1, U_00C2, U_00C3, U_00C4, U_00C5, U_00C6, U_00C7
        UCS     U_00C8, U_00C9, U_00CA, U_00CB, U_00CC, U_00CD, U_00CE, U_00CF
        UCS     U_00D0, U_00D1, U_00D2, U_00D3, U_00D4, U_00D5, U_00D6, U_00D7
        UCS     U_00D8, U_00D9, U_00DA, U_00DB, U_00DC, U_00DD, U_00DE, U_00DF
        UCS     U_00E0, U_00E1, U_00E2, U_00E3, U_00E4, U_00E5, U_00E6, U_00E7
        UCS     U_00E8, U_00E9, U_00EA, U_00EB, U_00EC, U_00ED, U_00EE, U_00EF
        UCS     U_00F0, U_00F1, U_00F2, U_00F3, U_00F4, U_00F5, U_00F6, U_00F7
        UCS     U_00F8, U_00F9, U_00FA, U_00FB, U_00FC, U_00FD, U_00FE, U_00FF
        UCS     U_0100, U_0101, U_0102, U_0103, U_0104, U_0105, U_0106, U_0107
        UCS     U_0108, U_0109, U_010A, U_010B, U_010C, U_010D, U_010E, U_010F
        UCS     U_0110, U_0111, U_0112, U_0113, U_0114, U_0115, U_0116, U_0117
        UCS     U_0118, U_0119, U_011A, U_011B, U_011C, U_011D, U_011E, U_011F
        UCS     U_0120, U_0121, U_0122, U_0123, U_0124, U_0125, U_0126, U_0127
        UCS     U_0128, U_0129, U_012A, U_012B, U_012C, U_012D, U_012E, U_012F
        UCS     U_0130, U_0131, U_0132, U_0133, U_0134, U_0135, U_0136, U_0137
        UCS     U_0138, U_0139, U_013A, U_013B, U_013C, U_013D, U_013E, U_013F
        UCS     U_0140, U_0141, U_0142, U_0143, U_0144, U_0145, U_0146, U_0147
        UCS     U_0148, U_0149, U_014A, U_014B, U_014C, U_014D, U_014E, U_014F
        UCS     U_0150, U_0151, U_0152, U_0153, U_0154, U_0155, U_0156, U_0157
        UCS     U_0158, U_0159, U_015A, U_015B, U_015C, U_015D, U_015E, U_015F
        UCS     U_0160, U_0161, U_0162, U_0163, U_0164, U_0165, U_0166, U_0167
        UCS     U_0168, U_0169, U_016A, U_016B, U_016C, U_016D, U_016E, U_016F
        UCS     U_0170, U_0171, U_0172, U_0173, U_0174, U_0175, U_0176, U_0177
        UCS     U_0178, U_0179, U_017A, U_017B, U_017C, U_017D, U_017E, U_017F

        NEWUCS  &192
        UCS                     U_0192
        NEWUCS  &1B7
        UCS                                                             U_01B7
        NEWUCS  &1E4, &1EF
        UCS                                     U_01E4, U_01E5, U_01E6, U_01E7
        UCS     U_01E8, U_01E9, UNK001, UNK001, UNK001, UNK001, U_01EE, U_01EF
        NEWUCS  &218, &21B
        UCS     U_0218, U_0219, U_021A, U_021B

        NEWUCS  &258
        UCS     U_0258
        NEWUCS  &261
        UCS             U_0261
        NEWUCS  &283
        UCS                             U_0283
        NEWUCS  &292
        UCS                     U_0292

        NEWUCS  &2BC, &2BD
        UCS                                     U_02BC, U_02BD

        NEWUCS  &2C6, &2C7
        UCS                                                     U_02C6, U_02C7
        NEWUCS  &2D8, &2DD
        UCS     U_02D8, U_02D9, U_02DA, U_02DB, U_02DC, U_02DD

        NEWUCS  &37A, &3CE
        UCS                     U_037A, UNK001, UNK001, UNK001, U_037E, UNK001
        UCS     UNK001, UNK001, UNK001, UNK001, U_0384, U_0385, U_0386, U_0387
        UCS     U_0388, U_0389, U_038A, UNK001, U_038C, UNK001, U_038E, U_038F
        UCS     U_0390, U_0391, U_0392, U_0393, U_0394, U_0395, U_0396, U_0397
        UCS     U_0398, U_0399, U_039A, U_039B, U_039C, U_039D, U_039E, U_039F
        UCS     U_03A0, U_03A1, UNK001, U_03A3, U_03A4, U_03A5, U_03A6, U_03A7
        UCS     U_03A8, U_03A9, U_03AA, U_03AB, U_03AC, U_03AD, U_03AE, U_03AF
        UCS     U_03B0, U_03B1, U_03B2, U_03B3, U_03B4, U_03B5, U_03B6, U_03B7
        UCS     U_03B8, U_03B9, U_03BA, U_03BB, U_03BC, U_03BD, U_03BE, U_03BF
        UCS     U_03C0, U_03C1, U_03C2, U_03C3, U_03C4, U_03C5, U_03C6, U_03C7
        UCS     U_03C8, U_03C9, U_03CA, U_03CB, U_03CC, U_03CD, U_03CE

        NEWUCS  &401, &45F
        UCS             U_0401, U_0402, U_0403, U_0404, U_0405, U_0406, U_0407
        UCS     U_0408, U_0409, U_040A, U_040B, U_040C, UNK001, U_040E, U_040F
        UCS     U_0410, U_0411, U_0412, U_0413, U_0414, U_0415, U_0416, U_0417
        UCS     U_0418, U_0419, U_041A, U_041B, U_041C, U_041D, U_041E, U_041F
        UCS     U_0420, U_0421, U_0422, U_0423, U_0424, U_0425, U_0426, U_0427
        UCS     U_0428, U_0429, U_042A, U_042B, U_042C, U_042D, U_042E, U_042F
        UCS     U_0430, U_0431, U_0432, U_0433, U_0434, U_0435, U_0436, U_0437
        UCS     U_0438, U_0439, U_043A, U_043B, U_043C, U_043D, U_043E, U_043F
        UCS     U_0440, U_0441, U_0442, U_0443, U_0444, U_0445, U_0446, U_0447
        UCS     U_0448, U_0449, U_044A, U_044B, U_044C, U_044D, U_044E, U_044F
        UCS     UNK001, U_0451, U_0452, U_0453, U_0454, U_0455, U_0456, U_0457
        UCS     U_0458, U_0459, U_045A, U_045B, U_045C, UNK001, U_045E, U_045F

        NEWUCS  &5D0, &5EA
        UCS     U_05D0, U_05D1, U_05D2, U_05D3, U_05D4, U_05D5, U_05D6, U_05D7
        UCS     U_05D8, U_05D9, U_05DA, U_05DB, U_05DC, U_05DD, U_05DE, U_05DF
        UCS     U_05E0, U_05E1, U_05E2, U_05E3, U_05E4, U_05E5, U_05E6, U_05E7
        UCS     U_05E8, U_05E9, U_05EA

        NEWUCS  &1E02, &1E03
        UCS                     U_1E02, U_1E03
        NEWUCS  &1E0A, &1E0B
        UCS                     U_1E0A, U_1E0B
        NEWUCS  &1E1E, &1E1F
        UCS                                                     U_1E1E, U_1E1F
        NEWUCS  &1E40, &1E41
        UCS     U_1E40, U_1E41
        NEWUCS  &1E56, &1E57
        UCS                                                     U_1E56, U_1E57
        NEWUCS  &1E60, &1E61
        UCS     U_1E60, U_1E61
        NEWUCS  &1E6A, &1E6B
        UCS                     U_1E6A, U_1E6B
        NEWUCS  &1E80, &1E85
        UCS     U_1E80, U_1E81, U_1E82, U_1E83, U_1E84, U_1E85
        NEWUCS  &1ECD
        UCS                                             U_1ECD
        NEWUCS  &1EEF, &1EF3
        UCS                                                             U_1EEF
        UCS     UNK001, U_1EF1, U_1EF2, U_1EF3

        NEWUCS  &2000, &2046
        UCS     U_2000, U_2001, U_2002, U_2003, U_2004, U_2005, U_2006, U_2007
        UCS     U_2008, U_2009, U_200A, UNK001, UNK001, UNK001, U_200E, U_200F
        UCS     U_2010, U_2011, U_2012, U_2013, U_2014, U_2015, U_2016, U_2017
        UCS     U_2018, U_2019, U_201A, U_201B, U_201C, U_201D, U_201E, U_201F
        UCS     U_2020, U_2021, U_2022, U_2023, U_2024, U_2025, U_2026, U_2027
        UCS     UNK001, UNK001, U_202A, U_202B, U_202C, U_202D, U_202E, UNK001
        UCS     U_2030, U_2031, U_2032, U_2033, U_2034, U_2035, U_2036, U_2037
        UCS     U_2038, U_2039, U_203A, U_203B, U_203C, U_203D, U_203E, U_203F
        UCS     U_2040, U_2041, U_2042, U_2043, U_2044, U_2045, U_2046

        NEWUCS  &2070, &208E
        UCS     U_2070, UNK001, UNK001, UNK001, U_2074, U_2075, U_2076, U_2077
        UCS     U_2078, U_2079, U_207A, U_207B, U_207C, U_207D, U_207E, U_207F
        UCS     U_2080, U_2081, U_2082, U_2083, U_2084, U_2085, U_2086, U_2087
        UCS     U_2088, U_2089, U_208A, U_208B, U_208C, U_208D, U_208E

        NEWUCS  &20AC, &20AF
        UCS                                     U_20AC, UNK001, UNK001, U_20AF

        NEWUCS  &2116
        UCS                                                     U_2116
        NEWUCS  &2122, &2126
        UCS                     U_2122, UNK001, UNK001, UNK001, U_2126

        NEWUCS  &215B, &215E
        UCS                             U_215B, U_215C, U_215D, U_215E

        NEWUCS  &2190, &2193
        UCS     U_2190, U_2191, U_2192, U_2193

        NEWUCS  &2202, &2207
        UCS                     U_2202, UNK001, UNK001, U_2205, U_2206, U_2207
        NEWUCS  &220F, &2213
        UCS                                                             U_220F
        UCS     UNK001, U_2211, U_2212, U_2213
        NEWUCS  &2219, &221A
        UCS             U_2219, U_221A
        NEWUCS  &2229, &222A
        UCS             U_2229, U_222A
        NEWUCS  &2248
        UCS     U_2248
        NEWUCS  &2260, &2267
        UCS     U_2260, U_2261, UNK001, UNK001, U_2264, U_2265, U_2266, U_2267

        NEWUCS  &2320, &2321
        UCS     U_2320, U_2321

        NEWUCS  &2500, &2502
        UCS     U_2500, UNK001, U_2502
        NEWUCS  &250C, &251C
        UCS                                     U_250C, UNK001, UNK001, UNK001
        UCS     U_2510, UNK001, UNK001, UNK001, U_2514, UNK001, UNK001, UNK001
        UCS     U_2518, UNK001, UNK001, UNK001, U_251C
        NEWUCS  &2524
        UCS                                     U_2524
        NEWUCS  &252C
        UCS                                     U_252C
        NEWUCS  &2534
        UCS                                     U_2534
        NEWUCS  &253C
        UCS                                     U_253C
        NEWUCS  &256D, &2577
        UCS                                             U_256D, U_256E, U_256F
        UCS     U_2570, UNK001, UNK001, UNK001, U_2574, U_2575, U_2576, U_2577
        NEWUCS  &2580, &2593
        UCS     U_2580, UNK001, UNK001, UNK001, U_2584, UNK001, UNK001, UNK001
        UCS     U_2588, UNK001, UNK001, UNK001, U_258C, UNK001, UNK001, UNK001
        UCS     U_2590, U_2591, U_2592, U_2593

        NEWUCS  &25A0
        UCS     U_25A0

        NEWUCS  &25EF
        UCS                                                             U_25EF

        NEWUCS  &266A
        UCS                     U_266A

        NEWUCS  &FB01, &FB02
        UCS             U_FB01, U_FB02

        NEWUCS  &FFFD
        UCS                                             U_FFFD

        DCD     &FFFFFFFF

        LNK     UCSTables.s
