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
# limitations under the License.

"""Parse RISC OS 3.71 Makefile to find module source directories."""

import json
import pprint
import re


def parse_makefile(content):
    """Parse makefile content to extract target-to-source directory mapping."""

    target_to_source = {}
    lines = content.splitlines()

    # Regex to find target definitions (e.g., "Kernel:")
    target_regex = re.compile(r"^([a-zA-Z0-9_]+)\s*:")

    # Regex to find the CD command pointing to a SRCDIR subdirectory
    # Looks for '@${CD} ${SRCDIR}.OS_Core.FileSys.CDFS.CDFS' pattern
    cd_srcdir_regex = re.compile(r"^\s*@\${CD}\s+\${SRCDIR}\.(.*?)\s*$")

    for i, line in enumerate(lines):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith("#"):
            continue

        target_match = target_regex.match(line)
        if not target_match:
            continue

        # Found a potential target definition line
        current_target = target_match.group(1)

        # Check subsequent lines for the CD command *within this target's rule block*
        for j in range(i + 1, len(lines)):
            # Stop at empty line.
            if not lines[j].strip():
                break
            # Stop if not indented.
            if not lines[j].startswith((" ", "\t")):
                break
            # Stop if it's another target.
            if target_regex.match(lines[j]):
                break
            # Look for our ${CD} pattern.
            cd_match = cd_srcdir_regex.search(lines[j])
            if not cd_match:
                continue

            # Found the CD command for the current target.
            source_path = cd_match.group(1).strip()

            if source_path:
                target_to_source[current_target] = source_path

            # Done with this target!
            break

    return target_to_source


def main():
    makefile_content = open(
        "riscos-371-opensource/RiscOS_371/BuildSys/Morris4/Makefile"
    ).read()
    source_map = parse_makefile(makefile_content)
    pprint.pprint(source_map)
    with open("module_to_source_mapping.json", "wt") as f:
        json.dump(source_map, f)


if __name__ == "__main__":
    main()
