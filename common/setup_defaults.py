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

# This script sets up various expected files in the current folder

import os

name = os.environ['NAME']
output_name = os.environ['OUTPUT_NAME']

pro = "%s.pro" % name
pcb = "%s.kicad_pcb" % name
zip = "%s.zip" % output_name

# Setup .gitignore
ignore = [x.strip() for x in open(".gitignore").readlines()] if os.path.exists(".gitignore") else []
for pattern in ("gerber_tmp", zip):
    if pattern not in ignore:
        ignore.append(pattern)
open(".gitignore", "w").writelines("%s\n" % x for x in sorted(ignore))

# Create/replace fp-lib-table
print>>open("fp-lib-table", "w"), """(fp_lib_table
  (lib (name myelin-kicad)(type Github)(uri https://github.com/myelin/myelin-kicad.pretty)(options allow_pretty_writing_to_this_dir=${KIPRJMOD}/../../third_party/myelin-kicad.pretty)(descr ""))
)"""

# Create empty .pro if it doesn't exist
if not os.path.exists(pro):
    open(pro, "w").close()

# No need to create a .sch file

# Add default .kicad_pcb if there isn't one
if not os.path.exists(pcb):
    print>>open(pcb, "w"), """(kicad_pcb (version 4) (host pcbnew 4.0.6)

  (general
    (links 6)
    (no_connects 4)
    (area 134.949999 110.949999 157.050001 129.050001)
    (thickness 1.6)
    (drawings 8)
    (tracks 24)
    (zones 0)
    (modules 4)
    (nets 6)
  )

  (page A4)
  (layers
    (0 F.Cu signal)
    (31 B.Cu signal)
    (32 B.Adhes user)
    (33 F.Adhes user)
    (34 B.Paste user)
    (35 F.Paste user)
    (36 B.SilkS user)
    (37 F.SilkS user)
    (38 B.Mask user)
    (39 F.Mask user)
    (40 Dwgs.User user)
    (41 Cmts.User user)
    (42 Eco1.User user)
    (43 Eco2.User user)
    (44 Edge.Cuts user)
    (45 Margin user)
    (46 B.CrtYd user)
    (47 F.CrtYd user)
    (48 B.Fab user hide)
    (49 F.Fab user hide)
  )

  (setup
    (last_trace_width 0.1778)
    (user_trace_width 0.254)
    (user_trace_width 0.508)
    (user_trace_width 0.762)
    (user_trace_width 1.016)
    (user_trace_width 1.27)
    (trace_clearance 0.1778)
    (zone_clearance 0.508)
    (zone_45_only no)
    (trace_min 0.1778)
    (segment_width 0.2)
    (edge_width 0.1)
    (via_size 0.8128)
    (via_drill 0.3302)
    (via_min_size 0.8128)
    (via_min_drill 0.3302)
    (user_via 0.8128 0.3302)
    (user_via 1.016 0.635)
    (uvia_size 0.8128)
    (uvia_drill 0.3302)
    (uvias_allowed no)
    (uvia_min_size 0.8128)
    (uvia_min_drill 0.3302)
    (pcb_text_width 0.2)
    (pcb_text_size 1.0 1.0)
    (mod_edge_width 0.15)
    (mod_text_size 1 1)
    (mod_text_width 0.15)
    (pad_size 1.5 1.5)
    (pad_drill 0.6)
    (pad_to_mask_clearance 0)
    (aux_axis_origin 0 0)
    (visible_elements FFFFFF7F)
    (pcbplotparams
      (layerselection 0x010fc_80000001)
      (usegerberextensions true)
      (excludeedgelayer true)
      (linewidth 0.100000)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15)
      (hpglpenoverlay 2)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (padsonsilk false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 0)
      (scaleselection 1)
      (outputdirectory gerbers/))
  )

  (net_class Default "This is the default net class."
    (clearance 0.1778)
    (trace_width 0.1778)
    (via_dia 0.8128)
    (via_drill 0.3302)
    (uvia_dia 0.8128)
    (uvia_drill 0.3302)
  )
)"""
