// Copyright 2017 Google Inc.
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

// This is a template file for designs based on the xc9500xl_44_breakout project.

module xc9500(
  // Left pins
  inout wire p34,  // GTS2
  inout wire p35,
  inout wire p36,  // GTS1
  inout wire p37,
  inout wire p38,
  inout wire p39,
  inout wire p40,
  inout wire p41,
  inout wire p42,
  inout wire p43,  // GCK1
  inout wire p44,  // GCK2
  inout wire p1,   // GCK3
  inout wire p2,
  inout wire p3,
  inout wire p5,
  inout wire p6,
  inout wire p7,
  inout wire p8,

  // Right pins
  inout wire p12,
  inout wire p13,
  inout wire p14,
  inout wire p16,
  inout wire p18,
  inout wire p19,
  inout wire p20,
  inout wire p21,
  inout wire p22,
  inout wire p23,
  inout wire p27,
  inout wire p28,
  inout wire p29,
  inout wire p30,
  inout wire p31,
  inout wire p32,
  inout wire p33  // GSR
);

// dummy statement so the template will build; remove this
assign p33 = 1'b1;

endmodule
