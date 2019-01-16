# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

MODULE=a3000_rom_emulator
PART=xc95144xl-10-cs144
# Use low power mode.  Ideally would use "auto" (timing-driven), but that only
# puts a few macrocells in low power mode.  Setting POWER=low still seems to
# work fine timing wise.
POWER=low

SHARED_PATH ?= ../../common
include ${SHARED_PATH}/Makefile.xilinx
