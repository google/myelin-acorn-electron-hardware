// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


module a3000_rom_emulator(
  
  // ground this to reset the machine
  inout wire arc_RESET,

  // connections to archimedes motherboard
  inout wire [31:0] rom_D,
  input wire [19:0] rom_A,
  input wire rom_nCS,

  // connections to two flash chips
  output wire [21:0] flash_A,
  inout wire [15:0] flash0_DQ,
  inout wire [15:0] flash1_DQ,
  output wire flash_nCE,
  output wire flash_nOE,
  output wire flash_nWE,

  // possible clocks (unused)
  input wire cpld_clock_from_mcu,
  input wire cpld_clock_osc,
  
  // SPI connection to MCU
  input wire cpld_MOSI,
  input wire cpld_SS,
  input wire cpld_SCK,
  output reg cpld_MISO = 1'b1
);

assign arc_RESET = 1'bZ;

// Dumb initial setup: no programming, just connect flash to motherboard
assign flash_A = {2'b0, rom_A};
assign rom_D = (rom_nCS == 1'b0) ? {flash1_DQ, flash0_DQ} : 32'bZ;
assign flash_nCE = rom_nCS;
assign flash_nOE = rom_nCS;
assign flash_nWE = 1'b1;

endmodule
