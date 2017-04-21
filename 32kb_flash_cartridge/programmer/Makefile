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

all: build wav

build:
	ca65 --cpu 6502 -o out/tester.o tester.asm
	ld65 out/tester.o -o out/tester -C tester.lkr
	da65 --comments 4 --start-addr 0x1100 out/tester > out/tester.list
	python make_inf.py out/tester > out/tester.inf

wav:
	python file_to_wav.py out/tester flash 1100
