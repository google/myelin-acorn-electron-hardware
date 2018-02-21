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

MODULE=master_updateable_megarom
PART=xc9572xl-10-VQ64

default: all

all:
	make -f Makefile.remote clean
	rsync -arzu --progress --delete --delete-excluded --exclude=.git . xilinx:${MODULE}/
	ssh xilinx ". /opt/Xilinx/14.7/ISE_DS/settings64.sh && cd ${MODULE} && make -f Makefile.remote clean && make -f Makefile.remote MODULE=${MODULE} PART=${PART}" 2>&1 | tee out/build.log
	rsync -arzu xilinx:"${MODULE}/*.jed ${MODULE}/*.svf ${MODULE}/*.xsvf ${MODULE}/*_html" out/
	open out/${MODULE}_html/fit/index.htm
	mv out/${MODULE}.jed out/${MODULE}.svf .
	xc3sprog -v -c jlink ${MODULE}.jed

test:
	iverilog -o $(MODULE)_tb.vvp $(MODULE)_tb.v
	vvp $(MODULE)_tb.vvp

test_show: test
	open -a Scansion $(MODULE)_tb.vcd
