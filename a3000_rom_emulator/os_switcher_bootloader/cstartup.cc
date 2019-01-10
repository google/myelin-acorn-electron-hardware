// Copyright 2019 Google LLC
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


// Program starts at _start in start.s, which calls cstart(), which calls main_program().

extern "C" {

  extern void main_program();

  void cstart() __attribute__((naked));

  void cstart() {
    // jump into c++ code
    main_program();

    // nowhere to go after this -- just hang!
    while (1);
  }

}
