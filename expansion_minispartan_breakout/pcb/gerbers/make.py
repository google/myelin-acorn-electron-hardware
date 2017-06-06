import os, glob

def cmd(s):
	print "  " + s
	return os.system(s)

files = []
for pat in "*.gbl *.gbs *.gbo *.gm1 *.gtl *.gts *.gto *.drl *.gbp *.gtp".split():
	files += glob.glob(pat)
#print files

# fixing up perms so we don't run into the issue where oshpark can't read our zip files
cmd("chmod 644 %s" % " ".join(files))

print "creating pcb.zip, which contains all design files including paste masks"
cmd("rm -f pcb.zip paste.zip paste-top.zip paste-bottom.zip")
cmd("zip pcb.zip %s" % " ".join(files))

def find(pat):
	print "finding %s in " % pat, files
	return [f for f in files if f.find(pat) != -1]

edge_cuts_file = find("-Edge.Cuts.")[0]
gko_file = os.path.splitext(edge_cuts_file)[0] + ".gko"
open(gko_file, 'w').write(open(edge_cuts_file).read())

paste_bot = find(".gbp")
if len(paste_bot):
	print "we have a bottom paste layer; creating paste-bottom.zip"
	cmd("zip paste-bottom.zip %s %s" % (paste_bot[0], gko_file))
paste_top = find(".gtp")
if len(paste_top):
	print "we have a top paste layer; creating paste-top.zip"
	cmd("zip paste-top.zip %s %s" % (paste_top[0], gko_file))
paste = paste_bot + paste_top
if len(paste) > 1:
	print "combining all paste files into paste.zip"
	cmd("zip paste.zip %s %s" % (" ".join(paste), gko_file))

cmd("rm -f %s" % gko_file)
cmd("git add %s" % " ".join(files))
