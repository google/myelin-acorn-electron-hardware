from __future__ import print_function
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

from gerber import load_layer
from gerber.render import GerberCairoContext, RenderSettings, theme
from glob import glob
import os
import sys

def generate_previews(fab_output_path, preview_output_path):

    def read(pattern):
        files = glob(os.path.join(fab_output_path, pattern))
        if not files:
            print("WARNING: Nothing found matching %s" % pattern)
            return None
        return load_layer(files[0])

    def save(name):
        path = os.path.join(preview_output_path, "%s.png" % name)
        print("Saving preview to %s" % path)
        ctx.dump(path)

    def render(pattern, **kw):
        layer = read(pattern)
        if layer is None:
            print("Not rendering %s" % pattern)
            return
        ctx.render_layer(layer, **kw)

    # Rendering context
    ctx = GerberCairoContext(scale=10)
    ctx.color = (80./255, 80/255., 154/255.)
    ctx.drill_color = ctx.color

    # Edges
    render("*.gm1")
    # Copper
    render("*.gtl")
    # Mask
    render("*.gts")
    # Silk
    render("*.gto", settings=RenderSettings(color=theme.COLORS['white'], alpha=0.85))
    # Drills
    render("*.drl")

    save("pcb-front")
    ctx.clear()

    # Edges
    render("*.gm1")
    # Copper
    render("*.gbl")
    # Mask
    render("*.gbs")
    # Silk
    render("*.gbo", settings=RenderSettings(color=theme.COLORS['white'], alpha=0.85))
    # Drills
    render("*.drl")

    save("pcb-back")


if __name__ == '__main__':
    generate_previews('gerber_tmp', '.')
