setMode -bs
setCable -port auto
identify
assignFile -p 1 -file "MGC-xc9536xl-10-VQ44.jed"
erase -p 1
program -p 1
quit
