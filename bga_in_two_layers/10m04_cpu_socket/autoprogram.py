from __future__ import print_function
# Copyright 2018 Google LLC
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

import os, stat, hashlib, time

src = 'output_files/10m04_blink.svf'

def hash(fn):
    return hashlib.sha1(open(fn).read()).hexdigest()
def prog():
    os.system("openocd")
    prog.last_prog_time = time.time()

last = hash(src)
prog()
while True:
    now = hash(src)
    if now != last:
        print("changed hash to %s" % now)
        prog()
        last = now
    print("%s programmed %.2f mins ago" % (now, float(time.time() - prog.last_prog_time) / 60.0))
    time.sleep(1)
