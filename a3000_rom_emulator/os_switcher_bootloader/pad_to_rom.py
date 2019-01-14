from __future__ import print_function
# Copyright 2019 Google LLC
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


import sys

ROM_SIZE = 2 * 1024 * 1024

src, dest = sys.argv[1:]

print("Padding %s with 0xFF to create a ROM file %s" % (src, dest))

data = open(src, "rb").read()

print(len(data), ROM_SIZE - len(data))
data += "\xFF" * (ROM_SIZE - len(data))
print(len(data))

open(dest, "wb").write(data)
