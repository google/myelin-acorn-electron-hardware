Electron ULA study and analysis notes
=====================================

Revaldinho has shot and stitched a number of high-res photos of the Electron's 12C021M ULA,
from which I'm attempting to extract a description of the internal structure.

The photo itself (TODO flickr link and full size link) is distributed under the GPL.

The chip appears to use the ULA6000 logic cell, as in the Tube ULA.

It has:

- three crossunders
- three resistors
- two transistor pairs, joined at the collectors
- a dual current source

Grid structure
--------------

The wires appear to only run horizontally and vertically.  From one point on a
cell to the same point on a cell below, there are 15 traces and 15 spaces.  From
one point on a cell to the same point on a cell to the right, it's the same.  So
each cell's interconnects can be described by a 30x30 grid of empty/solid
squares.

Each sector (on the 4x3 grid) has 9 cells across and 11 cells down (99 cells),
so image processing this should thus hopefully result in about a 270x330 grid
per sector, plus a bit for the interconnects on the sides.

The full chip image I have is ~165x165 per cell, so traces and spaces are about 5.5px
wide and 5.5px tall.

The photo is very well straightened, but still gains or loses a row or two on sector
boundaries, so I've written some code to allow grid lines to be drawn in.

Current source
--------------

Every cell appears to have a big rectangle in the center-right, which grounds the collector.

If there's a vertical bar just to the left, that's connecting B to Rcs.

If there's a little arrow pointing southeast in the top right hand corner, that's connecting Vs to the other end of Rcs (and one end of RL).

Vs is almost always connected to the right hand side of the second RL (the one not connected to Rcs).

Top right corner of the bottom right sector
-------------------------------------------

The top left interconnect on the grid below is the top terminal of the top left
crossunder.

X crossunder
B base
C collector
E emitter
G ground
V Vs
. metallizable grid location
\- metalizable grid location inside a component
| metalizable grid location inside a component

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
. . X . . . R - - - - - - - R . V . R - - - - - - - R . . .
.   |   .   .   .   .   .   .   .   .   .   .   .   |   .  
. . | . . . . . . . . . . . . . . . . . . . . . V . | . . .
.   |   .   .   .   .   .   .   .   .   .   .   .   |   .  
. . | . . . C . . . . . . . . . . . . . . . . . . . | . . .
.   |   .   |   .   .   .   .   .   .   .   .   .   |   .  
. . | . . . . - . . . . . . E E E . B . C G G . . . | . . .
.   |   .   .   |   .   .   .   .   B   C G G   .   |   .  
. . X . . . . . B . . . . . E E E . B . C G G . . . R . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
. . . . . . . . E . . . . . . . . . . . . . . . . . . . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
. . C - - - - - . . . . . . . . . . . . . . . - - - C . . .
.   .   .   .   .   .   .   .   .   .   .   |   .   .   .  
. . . . . . . . E . . . . . . . . . . - - - . . . . . . . .
.   .   .   .   .   .   .   .   .   |   .   .   .   .   .  
. . X . . . . . B . . . . . B . E . . . E . B . . . X . . .
.   |   .   .   |   .   .   .   .   |   .   .   .   |   .  
. . | . . . . . . - . . . . . . . - . . . . . . . . | . . .
.   |   .   .   .   |   .   .   |   .   .   .   .   |   .  
. . . - . . . . . . . - . . . . | . . . . . . . . - . . . .
.   .   |   .   .   .   |   .   |   .   .   .   |   .   .  
. . . . . - - - X . . . C . . . C . . . X - - - . . . . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
.   .   .   .   .   .   .   .   .   .   .   .   .   .   .  
