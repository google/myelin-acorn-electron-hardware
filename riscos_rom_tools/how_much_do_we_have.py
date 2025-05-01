# Copyright 2025 Google LLC
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
# limitations under the License

"""
Walk through `module_list.txt` and `module_to_source_mapping.json` to
find modules we're missing source for.

"""

import json


def main():
    with open("module_list.txt", "rt") as f:
        modules = [l.strip() for l in f.readlines()]
    with open("module_to_source_mapping.json", "rt") as f:
        module_to_source = json.load(f)

    for module in modules:
        if module in module_to_source:
            print(f"- {module}")
        else:
            print(f"MISSING: {module}")

if __name__ == "__main__":
    main()

