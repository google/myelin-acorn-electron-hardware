#!/usr/bin/python

"""
	Name		: uef2wave
	Author		: Wouter Hobers
	Created		: May 21 2001
	Last edited	: May 23 2001
	Purpose		: Convert tape blocks of UEF files to WAVE files so they can be
			  recorded on tape and used with a real Electron.
	WWW		: http://www.fmf.nl/~xaviar/acorn/
	Email		: xaviar@fmf.nl
"""


import sys, math, gzip

if sys.platform == "mac":
	import macfs


global TRUE
global FALSE
global BAUD

TRUE  = 1 == 1
FALSE = not TRUE

BAUD = 1000000.0/(16.0*52.0)


class UEFParser:

	
	tapeID     = 0x0100
	highToneID = 0x0110
	gapID      = 0x0112
	
	tapeIDList = [highToneID, gapID, tapeID]

	startBit = "0"
	stopBit  = "1"

	buffer = []
	pos    = 0


	def __init__(self,buffer):

		self.buffer = buffer


	def WordAt(self,buffer,pos):
		
		if pos + 1 >= len(buffer):
			return 0

		return ord(buffer[pos]) + ord(buffer[pos+1]) * 256
	

	def LongAt(self,buffer,pos):

		if pos + 3 >= len(buffer):
			return 0
				
		return self.WordAt(buffer,pos) + self.WordAt(buffer,pos+2) * 256 * 256
			

	def ReadBlockID(self):
		
		id = self.WordAt(self.buffer, self.pos)
		self.pos = self.pos + 2
		return id
		

	def FindTapeBlock(self):
		
		id = -1

		while self.pos < len(self.buffer):
			
			id = self.ReadBlockID()
			length = self.LongAt(self.buffer, self.pos)
			
			if id in self.tapeIDList:
				break
				
			self.pos = self.pos + 4 + length

		return id in self.tapeIDList, id
	

	def ToBitString(self,buffer):
		
		power2 = [1,2,4,8,16,32,64,128]

		s = ""

		pos = 0
		while pos < len(buffer):

			s = s + self.startBit

			for i in range(0,8):
				if (ord(buffer[pos]) & power2[i]):
					s = s + "1"
				else:
					s = s + "0"

			s = s + self.stopBit
			
			pos = pos + 1

		return s


	def ReadTapeBlock(self,id):
		
		length   = self.LongAt(self.buffer,self.pos)
		self.pos = self.pos + 4
	
		if id == self.tapeID:
			ret = self.ToBitString(self.buffer[self.pos:self.pos + length])
		elif id == self.gapID:
			ms  = self.WordAt(self.buffer,self.pos)
			ret = int(ms * (BAUD/1000.0)) * " "
		elif id == self.highToneID:
			ms  = self.WordAt(self.buffer,self.pos)
			ret = int(ms * (BAUD/1000.0)) * "1"			
		
		self.pos = self.pos + length
		
		return ret

	
	def ReadAllTapeBlocks(self):
		
		ret = ""
		
		found, id = self.FindTapeBlock()
		while found:
			ret       = ret + self.ReadTapeBlock(id)
			found, id = self.FindTapeBlock()
		
		return ret


class WaveWriter:
	

	maxVolumeLevel = 127
	minVolumeLevel = 0

	fp     = None
	buffer = ""	

	sine1200Hz = ""
	sine2400Hz = ""


	def __init__(self,fp,buffer):

		self.fp     = fp
		self.buffer = buffer
		
		self.CalcSine()
	

	def Str2(self,i):
		
		return chr(i & 0x00FF) + chr((i & 0xFF00) >> 8)
		
	
	def Str4(self,i):
		
		return self.Str2(i) + self.Str2((i & 0xFFFF0000) >> 16)
		

	def SetVolumeMin(self,volume):
		
		if volume > 0:
			self.minVolumeLevel = volume & 0xFF


	def SetVolumeMax(self,volume):

		if volume > 0:	
			self.maxVolumeLevel = volume & 0xFF


	def CalcSine(self):

		self.sine1200Hz = self.sine2400Hz = ""
		
		amp = (self.maxVolumeLevel - self.minVolumeLevel) / 2.0
		cy  = self.minVolumeLevel + amp

		dx = 2.0 * math.pi / 18.0		
		for i in range(0,18):
			self.sine1200Hz = self.sine1200Hz + chr(int(cy + amp * math.sin(i * dx)))
		
		dx = 4.0 * math.pi / 18.0
		for i in range(0,18):
			self.sine2400Hz = self.sine2400Hz + chr(int(cy + amp * math.sin(i * dx)))


	def WriteWaveHeader(self):
	
		bufferLen = len(self.buffer) * 18
		
		self.fp.write("RIFF")
		self.fp.write(self.Str4(bufferLen + 4 + 4 + 4 + 16 + 4 + 4))
		self.fp.write("WAVE")
		
		self.fp.write("fmt ")
		self.fp.write(self.Str4(16))
		self.fp.write(self.Str2(1))
		self.fp.write(self.Str2(1))
		self.fp.write(self.Str4(22050))
		self.fp.write(self.Str4(22050))
		self.fp.write(self.Str2(0))
		self.fp.write(self.Str2(8))

		self.fp.write("data")
		self.fp.write(self.Str4(bufferLen))
		

	def WriteBit(self,ch):

		if ch == "0":
			
			self.fp.write(self.sine1200Hz)
			
		elif ch == "1":
			
			self.fp.write(self.sine2400Hz)
					
		elif ch == " ":
			
			self.fp.write(18 * chr(self.minVolumeLevel))


	def WriteWave(self):
		
		self.WriteWaveHeader()
		
		pos = 0
		
		while pos < len(self.buffer):
			self.WriteBit(self.buffer[pos])
			pos = pos + 1


class Convertor:


	inFile  = ""
	outFile = ""

	volumeMin = 0
	volumeMax = 0


	def __init__(self,inFile,outFile):

		self.inFile  = inFile
		self.outFile = outFile
		
	
	def SetVolume(self,volume):
	
		self.volumeMax = volume


	def SetVolumeRange(self,min,max):
		
		self.volumeMin = min
		self.volumeMax = max


	def Convert(self):

		try:
			fpIn = open(self.inFile, "rb")
		except IOError:
			raise IOError, "Couldn't open file: " + self.inFile
		
		if fpIn.read(10) != "UEF File!\000":
			fpIn.close()

			try:
				fpIn = gzip.open(self.inFile, "rb")
				if fpIn.read(10) != "UEF File!\000":
					fpIn.close()
					raise IOError, "Not a UEF file: " + self.inFile

			except IOError:
				raise IOError, "Not a UEF file: " + self.inFile

		fpIn.read(2)
		buffer = fpIn.read()
		fpIn.close()
		
		try:
			fpOut = open(self.outFile, "wb")
		except IOError:
			raise IOError, "Couldn't open file: " + self.outFile
		
		parser    = UEFParser(buffer)
		bitStream = parser.ReadAllTapeBlocks()
				
		waver = WaveWriter(fpOut,bitStream)
		if self.volumeMin > 0: waver.SetVolumeMin(self.volumeMin)
		if self.volumeMax > 0: waver.SetVolumeMax(self.volumeMax)
		waver.WriteWave()
		
		fpOut.close()


# main

if sys.platform == "mac":

	# Mac has no command-line (pre OS X)
	
	fsSpecIn, ok = macfs.StandardGetFile()
	if not ok: sys.exit(1)
	
	fsSpecOut, ok = macfs.StandardPutFile("Save wave file as:")
	if not ok: sys.exit(1)
	
	convertor = Convertor(fsSpecIn.as_pathname(), fsSpecOut.as_pathname())
	
else:

	# a command-line is assumed here
	
	if len(sys.argv) != 3:
		print "Syntax:", sys.argv[0], "<inputfile.uef> <outputfile.wav>"
		sys.exit(1)
	
	convertor = Convertor(sys.argv[1], sys.argv[2])
	
convertor.SetVolumeRange(0x30, 0xC0)

try:
	convertor.Convert()
	print "All done."
except IOError, msg:
	print "An error occured:", msg
	sys.exit(1)

sys.exit()
