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

MODULE=standalone_programmer
PART=xc9572xl-10-VQ44

default: all

all:
	make -f Makefile.remote clean
	rsync -avrzu --progress --delete --delete-excluded --exclude=.git . xilinx:${MODULE}/
	ssh xilinx ". /opt/Xilinx/14.7/ISE_DS/settings64.sh && cd ${MODULE} && make -f Makefile.remote clean && make -f Makefile.remote MODULE=${MODULE} PART=${PART}" 2>&1 | tee out/build.log
	rsync -avrzu xilinx:"${MODULE}/*.jed ${MODULE}/*_html" out/
	open out/${MODULE}_html/fit/index.htm
	xc3sprog -v -c jlink out/${MODULE}.jed
