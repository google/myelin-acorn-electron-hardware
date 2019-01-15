#! /usr/bin/python

"""
	Name		: UEFtrans.py
	Author		: David Boddie <david@boddie.net>
	Created		: Sun 08th July 2001
	Last updated	: Thu 26th July 2001
	Purpose		: Catalogue UEF archives or add and remove files.
	WWW		: http://www.david.boddie.net/Software/Python/UEFtrans/

	History:

		0.10 (Wed 11th July 2001)
		First release.

		0.11 (Thu 12th July 2001)
		Added various chunks to those recognised by the "chunks" command.
		Insert, extract and remove commands now support operations on
		individual chunks as well as on files.

		0.20 (Fri 13th July 2001)
		Finalised changes to the insert and extract commands.
		Changed the filename format for importing and exporting chunks of
		arbitrary chunk number to requiring a hexadecimal suffix.

		0.21 (Fri 13th July 2001)
		Added the chunk information for changes of baud rate (0x113).

		0.22 (Tue 17th July 2001)
		Changed my e-mail address and WWW address (above).
		Added some comments and help messages.
		Corrected the chunk number for memory to the correct value (0x410). 

		0.23 (Sat 21st July 2001)
		Added the detailed information command (wwwinfo).

		0.24 (Mon 23rd July 2001)
		Made the integer division in the number function explicit.

		0.30 (Tue 24th July 2001)
		Added functionality so that files and chunks can be extracted to
		other UEF files.

		0.31 (Tue 24th July 2001)
		The creator chunk is now automatically written when extracting
		files to a new UEF file.

		0.32 (Wed 25th July 2001)
		Checks the namespace so that the script can be imported as a module.

		0.33 (Thu 26th July 2001)
		Allowed for chunks to have data of zero bytes in length.
		Modified the function to read the creator and emulator information
		to take this possibility into account.

		0.40 (Fri 10th August 2001)
		Corrected the conversion of tape data chunks which included start and
		stop bits (chunk 0x102) when extracting files.

		0.41 (Mon 13th August 2001)
		Added UEF file version information reporting to info and wwwinfo
		commands.
		Fixed the new command so that the keyboard layout is set correctly.
"""
from __future__ import print_function

import sys, string, os, gzip


def number(size, n):
	"""Convert a number to a little endian string of bytes for writing to a binary file."""

	# Little endian writing

	s = ""

	while size > 0:
		i = n % 256
		s = s + chr(i)
#		n = n / 256
		n = n >> 8
		size = size - 1

	return s


def str2num(size, s):
	"""Convert a string of decimal digits to an integer."""

	i = 0
	n = 0
	while i < size:

		n = n | (ord(s[i]) << (i*8))
		i = i + 1

	return n

			
def hex2num(s):
	"""Convert a string of hexadecimal digits to an integer."""

	n = 0

	for i in range(0,len(s)):

		a = ord(s[len(s)-i-1])
		if (a >= 48) & (a <= 57):
			n = n | ((a-48) << (i*4))
		elif (a >= 65) & (a <= 70):
			n = n | ((a-65+10) << (i*4))
		elif (a >= 97) & (a <= 102):
			n = n | ((a-97+10) << (i*4))
		else:
			return None

	return n


# CRC calculation routines (begin)

def rol(n, c):

	n = n << 1

	if (n & 256) != 0:
		carry = 1
		n = n & 255
	else:
		carry = 0

	n = n | c

	return n, carry


def crc(s):

	high = 0
	low = 0

	for i in s:

		high = high ^ ord(i)

		for j in range(0,8):

			a, carry = rol(high, 0)

			if carry == 1:
				high = high ^ 8
				low = low ^ 16

			low, carry = rol(low, carry)
			high, carry = rol(high, carry)

	return high | (low << 8)

# CRC calculation routines (end)


def chunk(f, n, data):
	"""Write a chunk to the file specified by the open file object, chunk number and data supplied."""

	# Chunk ID
	f.write(number(2, n))
	# Chunk length
	f.write(number(4, len(data)))
	# Data
	f.write(data)


def read_block(chunk):
	"""Read a data block from a tape chunk and return the program name, load and execution addresses,
	   block data, block number and whether the block is supposedly the last in the file."""

	# Chunk number and data
	chunk_id = chunk[0]
	data = chunk[1]

	# For the implicit tape data chunk, just read the block as a series
	# of bytes, as before
	if chunk_id == 0x100:

		block = data

	else:	# 0x102

		if UEF_major == 0 and UEF_minor < 9:

			# For UEF file versions earlier than 0.9, the number of
			# excess bits to be ignored at the end of the stream is
			# set to zero implicitly
			ignore = 0
			bit_ptr = 0
		else:
			# For later versions, the number of excess bits is
			# specified in the first byte of the stream
			ignore = data[0]
			bit_ptr = 8

		# Convert the data to the implicit format
		block = []
		write_ptr = 0

		after_end = (len(data)*8) - ignore
		if after_end % 10 != 0:

			# Ensure that the number of bits to be read is a
			# multiple of ten
			after_end = after_end - (after_end % 10)

		while bit_ptr < after_end:

			# Skip start bit
			bit_ptr = bit_ptr + 1

			# Read eight bits of data
			bit_offset = bit_ptr % 8
			if bit_offset == 0:
				# Write the byte to the block
				block[write_ptr] = data[bit_ptr >> 3]
			else:
				# Read the byte containing the first bits
				b1 = data[bit_ptr >> 3]
				# Read the byte containing the rest
				b2 = data[(bit_ptr >> 3) + 1]

				# Construct a byte of data
				# Shift the first byte right by the bit offset
				# in that byte
				b1 = b1 >> bit_offset

				# Shift the rest of the bits from the second
				# byte to the left and ensure that the result
				# fits in a byte
				b2 = (b2 << (8 - bit_offset)) & 0xff

				# OR the two bytes together and write it to
				# the block
				block[write_ptr] = b1 | b2

			# Increment the block pointer
			write_ptr = write_ptr + 1

			# Move the data pointer on eight bits and skip the
			# stop bit
			bit_ptr = bit_ptr + 9

	# Read the block
	name = ''
	a = 1
	while True:
		c = block[a]
		if ord(c) != 0:		# was > 32:
			name = name + c
		a = a + 1
		if ord(c) == 0:
			break

	load = str2num(4, block[a:a+4])
	exec_addr = str2num(4, block[a+4:a+8])
	block_number = str2num(2, block[a+8:a+10])
	last = str2num(1, block[a+12])

	if last & 0x80 != 0:
		last = 1
	else:
		last = 0

	return (name, load, exec_addr, block[a+19:-2], block_number, last)


def write_block(f, name, load, exe, length, n):
	"""Read data from a file and write it to a string as a file data block in preparation to be written
	as chunk data to a UEF file."""

	block = f.read(256)

	# Write the alignment character
	out = "*"+name[:10]+"\000"

	# Load address
	out = out + number(4, load)

	# Execution address
	out = out + number(4, exe)

	# Block number
	out = out + number(2, n)

	# Block length
	out = out + number(2, len(block))

	# Block flag (last block)
	if f.tell() == length:
		out = out + number(1, 128)
		last = 1
	else:
		if len(block) == 256:
			out = out + number(1, 0)
			last = 0
		else:
			out = out + number(1, 128) # shouldn't be needed 
			last = 1 

	# Next address
	out = out + number(2, 0)

	# Unknown
	out = out + number(2, 0)

	# Header CRC
	out = out + number(2, crc(out[1:]))

	out = out + block

	# Block CRC
	out = out + number(2, crc(block))

	return out, last


def get_leafname(path):
	"""Get the leafname of the specified file."""

	pos = string.rfind(path, os.sep)
	if pos != -1:
		return path[pos+1:]
	else:
		return path


def find_next_chunk(chunks, pos, IDs):
	"""Find the next chunk from the position specified which has an ID in the list of IDs given."""

	while pos < len(chunks):

		if chunks[pos][0] in IDs:

			# Found a chunk with ID in the list
			return pos, chunks[pos]

		# Otherwise continue looking
		pos = pos + 1

	return None, None


def find_next_block(chunks, pos):
	"""Find the next file block in the list of chunks."""

	while pos < len(chunks):

		pos, chunk = find_next_chunk(chunks, pos, [0x100, 0x102])

#		if chunks[pos][0] == 0x100 or chunks[pos][0] == 0x102:

#			if len(chunks[pos][1]) > 1:

		if pos == None:

			return None
		else:
			if len(chunk[1]) > 1:

				# Found a block, return this position
				return pos

		# Otherwise continue looking
		pos = pos + 1

	return None


def find_file_start(chunks, pos):
	"""Find a chunk before the one specified which is not a file block."""

	pos = pos - 1
	while pos > 0:

		if chunks[pos][0] != 0x100 and chunks[pos][0] != 0x102:

			# This is not a block
			return pos

		else:
			pos = pos - 1

	return pos


def find_file_end(chunks, pos):
	"""Find a chunk after the one specified which is not a file block."""

	pos = pos + 1
	while pos < len(chunks)-1:

		if chunks[pos][0] != 0x100 and chunks[pos][0] != 0x102:

			# This is not a block
			return pos

		else:
			pos = pos + 1

	return pos


def read_uef_details(chunks):
	"""Return details about the UEF file and its contents."""

	pos, chunk = find_next_chunk(chunks, 0, [0x0])

	if pos == None:

		originator = 'Unknown'

	elif chunk[1] == '':

		originator = 'Unknown'
	else:
		originator = chunk[1]

	pos, chunk = find_next_chunk(chunks, 0, [0x5])

	if pos == None:

		machine, keyboard = 'Unknown', 'Unknown'

	else:

		machines = ('BBC Model A', 'Electron', 'BBC Model B', 'BBC Master')
		keyboards = ('Any layout', 'Physical layout', 'Remapped')

		machine = ord(chunk[1][0]) & 0x0f
		keyboard = (ord(chunk[1][0]) & 0xf0) >> 4

		if machine < len(machines):
			machine = machines[machine]
		else:
			machine = 'Unknown'

		if keyboard < len(keyboards):
			keyboard = keyboards[keyboard]
		else:
			keyboard = 'Unknown'

	pos, chunk = find_next_chunk(chunks, 0, [0xff00])

	if pos == None:

		emulator = 'Unknown'

	elif chunk[1] == '':

		emulator = 'Unknown'
	else:
		emulator = chunk[1]


	# Remove trailing null bytes
	while originator[-1] == '\000':

		originator = originator[:-1]

	while emulator[-1] == '\000':

		emulator = emulator[:-1]

	features = ''
	if find_next_chunk(chunks, 0, [0x1])[0] != None:
		features = features + '\n' + 'Instructions'
	if find_next_chunk(chunks, 0, [0x2])[0] != None:
		features = features + '\n' + 'Credits'
	if find_next_chunk(chunks, 0, [0x3])[0] != None:
		features = features + '\n' + 'Inlay'

	return originator, machine, keyboard, emulator, features


def write_uef_header(file, major, minor):
	"""Write the UEF file header and version number to a file."""

	# Write the UEF file header
	file.write('UEF File!\000')

	# Minor and major version numbers
	file.write(number(1, minor) + number(1, major))


def write_uef_creator(file, originator):
	"""Write a creator chunk to a file."""

	origin = originator + '\000'

	if (len(origin) % 4) != 0:
		origin = origin + ('\000'*(4-(len(origin) % 4)))

	# Write the creator chunk
	chunk(file, 0, origin)


def write_machine_info(file, machine, keyboard):
	"""Write the target machine and keyboard layout information to a file."""

	machines = {'BBC Model A': 0, 'Electron': 1, 'BBC Model B': 2, 'BBC Master':3}
	keyboards = {'any': 0, 'physical': 1, 'logical': 2}

	if machine in machines:

		machine = machines[target_machine]
	else:
		machine = 0

	if keyboard in keyboards:

		keyboard = keyboards[keyboard_layout]
	else:
		keyboard = 0

	chunk(file, 5, number(1, machine | (keyboard << 4) ))


def write_chunks(file, chunks):
	"""Write all the chunks in the list to a file. Saves having loops in other functions to do this."""

	for c in chunks:

		chunk(file, c[0], c[1])


def create_chunks(file_names):
	"""Traverse the list of filenames to insert, reading the relevant information, creating suitable chunks, and inserting them into
	the list of chunks."""

	new_chunks = []

	for name in file_names:

		# Find the .inf file and read the details stored within
		try:
			details = open(name + suffix + 'inf', 'r').readline()
		except IOError:

			try:
				details = open(name + suffix + 'INF', 'r').readline()
			except IOError:
				print("Couldn't open information file, %s" % name+suffix+'inf')
				sys.exit()

		# Parse the details
		details = [string.rstrip(details)]

		splitters = [' ', '\011']

		# Split the details up where certain whitespace characters occur
		for s in splitters:

			new_details = []

			# Split up each substring (list entry)
			for d in details:

				new_details = new_details + string.split(d, s)

			details = new_details

		# We should have details about the load and execution addresses

		# Open the file
		try:
			in_file = open(name, 'rb')
		except IOError:
			print("Couldn't open file, %s" % name)
			sys.exit()

		# Find the length of the file (don't rely on the .inf file)
		in_file.seek(0, 2)
		length = in_file.tell()
		in_file.seek(0, 0)

		# Examine the name entry and take the load and execution addresses
		dot_at = string.find(details[0], '.')
		if dot_at != -1:
			real_name = details[0][dot_at+1:]
			load, exe = details[1], details[2]
		else:
			real_name = get_leafname(name)
			load, exe = details[0], details[1]

		load = hex2num(load)
		exe = hex2num(exe)

		if load == None or exe == None:
			print('Problem with %s: information is possibly incorrect.' % name+suffix+'inf')
			sys.exit()

		# Reset the block number to zero
		block_number = 0

		# Long gap
		gap = 1
	
		# Write block details
		while True:
			block, last = write_block(in_file, real_name, load, exe, length, block_number)

			if gap == 1:
				new_chunks.append((0x110, number(2,0x05dc)))
				gap = 0
			else:
				new_chunks.append((0x110, number(2,0x0258)))

			# Write the block to the list of new chunks

			# For old versions, just write the block
			if UEF_major == 0 and UEF_minor < 9:
				new_chunks.append((0x100, block))
			else:
				new_chunks.append((0x100, block))

			if last == 1:
				break

			# Increment the block number
			block_number = block_number + 1

		# Close the input file
		in_file.close()

	# Write some finishing bytes to the list of new chunks
#	new_chunks.append((0x110, number(2,0x0258)))
#	new_chunks.append((0x112, number(2,0x0258)))

	# Return the list of new chunks
	return new_chunks


def encode_chunks(file_names):

	# Use a convention for determining the chunk number to be used:
	# If the filename is a hexadecimal number (beginning with 0x) then
	# that is used as the chunk number, and the contents of the file is
	# used as the chunk data.
	# Certain filenames are converted to chunk numbers and their
	# contents inserted as the chunk data. These are listed in the
	# encode_as dictionary.

	encode_as = {'creator': 0x0, 'originator': 0x0, 'instructions': 0x1, 'manual': 0x1,
	             'credits': 0x2, 'inlay': 0x3, 'target': 0x5, 'machine': 0x5,
	             'multi': 0x6, 'multiplexing': 0x6, 'palette': 0x7,
	             'tone': 0x110, 'dummy': 0x111, 'gap': 0x112, 'baud': 0x113,
	             'position': 0x120,
	             'discinfo': 0x200, 'discside': 0x201, 'rom': 0x300,
	             '6502': 0x400, 'ula': 0x401, 'wd1770': 0x402, 'memory': 0x410,
	             'emulator': 0xff00}

	new_chunks = []

	for name in file_names:

		leafname = get_leafname(name)

		hexsuffix = string.find(leafname, suffix+'0x')

		if hexsuffix != -1:

			# Hexadecimal number
			try:
				new_chunks.append( (hex2num(leafname[hexsuffix+3:]), open(name, 'rb').read()) )
			except IOError:
				print("Couldn't insert file %s as chunk." % name)
				sys.exit()
		else:
			# Attempt to convert filename into a chunk number
			try:
				number = encode_as[string.lower(leafname)]

				new_chunks.append( (number, open(name, 'rb').read()) )

			except KeyError:
				print("Couldn't find suitable chunk number for file %s" % name)
				sys.exit()

			except IOError:
				print("Couldn't insert file %s as chunk." % name)
				sys.exit()

	# Return the list of new chunks
	return new_chunks


def export_file(out_path, chunks, name, write_name, load, exe, length):

	out_file = inf_file = None

	try:
		out_file = open(out_path + os.sep + write_name, 'wb')
	except IOError:
		print("Couldn't open file %s" % out_path+os.sep+name)

	if out_file == None:

		# Try to open the file with a generic stem and put the
		# real name in the .inf file
		print('Trying to create %s' % out_path+os.sep+stem+str(new_file))
		try:
			out_file = open(out_path + os.sep + stem + str(new_file), 'wb')

			# New name with the stem and number
			write_name = stem + str(new_file)
			new_file = new_file + 1
		except IOError:
			print("Couldn't open file %s" % out_path+os.sep+stem+str(new_file))

	if out_file != None:

		# Open the .inf file
		try:
			inf_file = open(out_path + os.sep + write_name + suffix + 'inf', 'w')
		except IOError:
			print("Couldn't open file %s" % out_path+os.sep+name+suffix+'inf')

	if inf_file != None:

		# Write information to the .inf file
		inf_file.write('$.'+name+'\t' + string.upper(
							hex(load)[2:]+'\t'+
							hex(exe)[2:]+'\t'+
							hex(length)[2:]
						)+'\n')

		# Read the blocks from the UEF file and write
		# them to the file
		position = 0
		end_pos = len(chunks)
		while position < end_pos:

			# Find the next block
			position = find_next_block(chunks, position)

			if position == None:

				break

			else:
				# Read the block information
				name, load, exec_addr, data, block_number, last = read_block(chunks[position])

				# Store the data in the file
				out_file.write(data)

			position = position + 1

		# Close the file
		out_file.close()


def decode_chunk(out_path, chunk_info, position):

	# Write a file depending on the chunk number using a convention similar to that used for encoding
	# chunks.
	decode_as = {0x0: 'creator', 0x1: 'manual', 0x2: 'credits', 0x3: 'inlay',
	             0x5: 'machine', 0x6: 'multiplexing', 0x7: 'palette',
	             0x110: 'tone', 0x111: 'dummy', 0x112: 'gap', 0x113: 'baud',
	             0x120: 'position',
	             0x200: 'discinfo', 0x201: 'discside', 0x300: 'rom',
	             0x400: '6502', 0x401: 'ula', 0x402: 'wd1770', 0x410: 'memory',
	             0xff00: 'emulator'}

	# If the chunk number is not in the dictionary then write a file with name constructed
	# from the hexadecimal form of the chunk number beginning with 0x.
	if chunk_info[0] in decode_as:

		name = decode_as[chunk_info[0]]

	else:

		# Attempt to save the chunk in a file with a name made up from the position of the chunk
		# in the list with a hexadecimal suffix
		name = str(position)+suffix+hex(chunk_info[0])

	# Write file
	try:
		open(out_path+os.sep+name, 'wb').write(chunk_info[1])

	except IOError:
		print("Couldn't write file %s for chunk number %s." % (name, hex(chunk_info[0])))


def printable(s):

	new = ''
	for i in s:

		if ord(i) < 32:
			new = new + '?'
		else:
			new = new + i

	return new


def browsable(s):

	new = ''
	for i in s:

		if ord(i) < 32:
			new = new + '?'
		elif i == '&':
			new = new + '&amp;'
		elif i == '<':
			new = new + '&lt;'
		elif i == '>':
			new = new + '&gt;'
		elif ord(i) == 169:
			new = new + '&copy;'
		elif ord(i) > 126:
			new = new + '?'
		else:
			new = new + i

	return new


def print_help(command):

	if command == 'general':

		print(syntax)
		print()
		print('UEFtrans version '+version)
		print()
		print('This program allows the user to perform operations on UEF archives.')
		print('The operations supported may take arguments and are as follows:')
		print()
		print('        info')
		print('        wwwinfo <directory>')
		print('        new <machine> <keyboard>')
		print('        cat')
		print('        append <files>')
		print('        insert <position> <files/chunks>')
		print('        remove <positions>')
		print('        extract <positions> <directory>')
		print('        chunks')
		print()
		print('In addition, the help command provides information on any command')
		print('and uses the special syntax:')
		print()
		print('        UEFtrans'+suffix+'py help <command>')
		print()

	elif command == 'info':

		print(info_syntax)
		print()
		print('        Provides general information on the target machine,')
		print('        keyboard layout, file creator and target emulator.')
		print()

	elif command == 'new':

		print(new_syntax)
		print()
		print('        Creates a new UEF file of the name given specified as')
		print('        being for a particular machine which is one of the')
		print('        following:')
		print()
		print('        BBC Model A, Electron, BBC Model B, BBC Master')
		print()
		print('        The keyboard layout is  "any", "physical" or "logical".')
		print()
		print('        UEF version is a number of the form x.y corresponding to')
		print('        the relevant version of the UEF file format specification.')
		print()

	elif command == 'cat':

		print(cat_syntax)
		print()
		print('        Lists the names of the files in the archive.')
		print()

	elif command == 'append':

		print(append_syntax)
		print()
		print('        Add the files in the order given to the end of the')
		print('        archive. Each file requires an associated .inf file.')
		print()

	elif command == 'insert':

		print(insert_syntax)
		print()
		print('        Insert files/chunks in the order given into the archive')
		print('        at the position specified.')
		print()
		print('        To insert files, the position given is the number of a file')
		print('        in the archive catalogue before which you wish the files to')
		print('        be placed. Note that 0 is the number of the first file in')
		print('        the archive.')
		print()
		print('        To insert chunks, the position given is that of the chunk')
		print('        before which the inserted chunks will appear. This number')
		print('        must be prefixed by "c" to indicate that the files to be')
		print('        inserted contain chunk data. Since there is no version of')
		print('        the append command for chunks, you should append them by')
		print('        specifying a position which is one greater than the last')
		print('        chunk in the file.')
		print()
		print('Type "'+help_syntax[8:-9]+'numbers" for information on chunk numbers.')
		print()

	elif command == 'numbers':

		print()
		print('        Files containing chunk data are given the correct chunk')
		print('        number if they have a filename which is one of the')
		print('        following:')
		print()
		print('        creator (0x0)     manual (0x1)      credits (0x2)')
		print('        inlay (0x3)       machine (0x5)     multiplexing (0x6)')
		print('        palette (0x7)     tone (0x110)      dummy (0x111)')
		print('        gap (0x112)       baud (0x113)      position (0x120)')
		print('        discinfo (0x200)  discside (0x201)  rom (0x300)')
		print('        6502 (0x400)      ula (0x401)       wd1770 (0x402)')
		print('        memory (0x403)    emulator (0xff00)')
		print()
		print('        To insert chunks with numbers other than those recognized,')
		print('        add a suffix to the filenames in the form of hexadecimal')
		print('        numbers corresponding to the chunk numbers required,')
		print()
		print('        e.g. a_data_block'+suffix+'0x100')
		print()

	elif command == 'remove':

		print(remove_syntax)
		print()
		print('        Remove files/chunks at the positions specified,')
		print('        separating the numbers by commas.')
		print()
		print('        To remove files, use the numbers of the file in the archive')
		print('        catalogue. To remove chunks, supply the positions of the')
		print('        chunks which you wish to remove prefixed by "c".')
		print()
		print('Type "'+help_syntax[8:-9]+'numbers" for information on chunk numbers.')
		print()

	elif command == 'extract':

		print(extract_syntax)
		print()
		print('        Extract files/chunks at the comma separated positions')
		print('        specified and either save them in the directory given with')
		print('        .inf files or add them to the end of the UEF file given.')
		print()
		print('        To extract files, use the numbers of the file in the')
		print('        archive catalogue. To extract chunks, supply the positions')
		print('        of the chunks which you wish to extract prefixed by "c".')
		print()
		print('Type "'+help_syntax[8:-9]+'numbers" for information on chunk numbers.')
		print()

	elif command == 'chunks':

		print(chunks_syntax)
		print()
		print('        Display the chunks in the UEF file in a table format')
		print('        with the following symbols denoting each type of')
		print('        chunk:')
		print('                O        Originator information            (0x0)')
		print('                I        Instructions/manual               (0x1)')
		print('                C        Author credits                    (0x2)')
		print('                S        Inlay scan                        (0x3)')
		print('                M        Target machine information        (0x5)')
		print('                X        Multiplexing information          (0x6)')
		print('                P        Extra palette                     (0x7)')
		print()
		print('                #, *     File data block             (0x100,0x102)')
		print('                #x, *x   Multiplexed block           (0x101,0x103)')
		print('                -        High tone (inter-block gap)       (0x110)')
		print('                +        High tone with dummy byte         (0x111)')
		print('                _        Gap (silence)                     (0x112)')
		print('                B        Change of baud rate               (0x113)')
		print('                !        Position marker                   (0x120)')
		print('                D        Disc information                  (0x200)')
		print('                d        Standard disc side                (0x201)')
		print('                dx       Multiplexed disc side             (0x202)')
		print('                R        Standard machine ROM              (0x300)')
		print('                Rx       Multiplexed machine ROM           (0x301)')
		print('                6        6502 standard state               (0x400)')
		print('                U        Electron ULA state                (0x401)')
		print('                W        WD1770 state                      (0x402)')
		print('                m        Standard memory data              (0x410)')
		print('                mx       Multiplexed memory data           (0x410)')
		print()
		print('                E        Emulator identification string    (0xff00)')
		print('                ?        Unknown (unsupported chunk)')
		print()

	elif command == 'wwwinfo':

		print(wwwinfo_syntax)
		print()
		print('        Extracts information about the contents of the UEF file and')
		print('        writes an HTML document with relevant images to the')
		print('        directory specified.')
		print()

	elif command == 'help':

		print(help_syntax)
		print()
		print('        Provides help on the command specified using the special')
		print('        syntax as shown. In addition asking for help on "general"')
		print('        will show the list of commands available.')
		print()

	else:
		print('No help is available on that command.')
		print()


# Main program

if __name__ == '__main__':

	# Determine the platform on which the program is running
	
	sep = os.sep
	
	if sys.platform == 'RISCOS':
		suffix = '/'
	else:
		suffix = '.'
	
	version = '0.41 (Mon 13th August 2001)'
	
	# Syntax information
	base_syntax = 'Syntax: UEFtrans'+suffix+'py <UEF file> '
	syntax = base_syntax + '<command> [arguments]'
	new_syntax = base_syntax + 'new <machine> <keyboard> [UEF version]'
	add_syntax = base_syntax + 'add <files>'
	insert_syntax = base_syntax + 'insert <position> <files>'
	append_syntax = base_syntax + 'append <files>'
	remove_syntax = base_syntax + 'remove <positions>'
	extract_syntax = base_syntax + 'extract <positions> <directory/UEF file>'
	info_syntax = base_syntax + 'info'
	cat_syntax = base_syntax + 'cat'
	chunks_syntax = base_syntax + 'chunks'
	wwwinfo_syntax = base_syntax + 'wwwinfo <directory>'
	
	# Help syntax is different to the others since it does not require the user
	# to specify a UEF file.
	help_syntax = 'Syntax: UEFtrans'+suffix+'py help <command>'
	
	args = sys.argv[1:]
	
	# If there are no arguments then print the help text
	if len(args) < 2:
	
		# Incomplete help command
		if len(args) == 1:
		
			if args[0] == 'help':
		
				print(help_syntax)
	
			else:
				print_help('general')
	
			# Exit
			sys.exit()
	
		else:
	
			# No arguments
			print_help('general')
			sys.exit()
	
	
	# Complete help command
	
	if args[0] == 'help':
	
		# Pass argument to help function
		print_help(args[1])
		
		# Exit
		sys.exit()
	
	
	
	# Determine the UEF file to be modified
	
	uef_file = args[0]
	
	# Determine the command to be executed
	
	command = args[1]
	
	# Remove these from the arguments list
	
	args = args[2:]
	
	
	# Originator, target machine and keyboard layout is initially undefined
	originator = taget_machine = keyboard_layout = 'Unknown'
	
	# New command (create the file with the name given)
	
	if command == 'new':
	
		# If there is an argument specifying the machine type then add
		# a chunk for this
		if len(args) == 2:
	
			target_machine = args[0]
			keyboard_layout = args[1]
			write_version = '0.9'

		elif len(args) == 3:

			target_machine = args[0]
			keyboard_layout = args[1]
			write_version = args[2]

		else:
			print(new_syntax)
			sys.exit()
	
		# Determine the major and minor version numbers to write
		numbers = string.split(write_version, '.')
		try:
			major = int(numbers[0])
			minor = int(numbers[1])
		except ValueError:
			print('Invalid version number.')
			sys.exit()

		# Open file for writing
		uef = gzip.open(uef_file, 'wb')
	
		# Write the UEF file header
		write_uef_header(uef, major, minor)
		write_uef_creator(uef, 'UEFtrans '+version)
		write_machine_info(uef, target_machine, keyboard_layout)
	
		# Close the file
		uef.close()
	
		# Exit
		sys.exit()
	
	
	# Open the input file
	try:
		in_f = open(uef_file, 'rb')
	except IOError:
		print('The input file, '+uef_file+' could not be found.')
		sys.exit()
	
	# Is it gzipped?
	if in_f.read(10) != 'UEF File!\000':
	
		in_f.close()
		in_f = gzip.open(uef_file, 'rb')
	
		try:
			if in_f.read(10) != 'UEF File!\000':
				print('The input file, '+uef_file+' is not a UEF file.')
				in_f.close()
				sys.exit()
		except:
			print('The input file, '+uef_file+' could not be read.')
			in_f.close()
			sys.exit()
	
	# Read version number of the file format
	UEF_minor = str2num(1, in_f.read(1))
	UEF_major = str2num(1, in_f.read(1))

	# Extract files (directory organisation before the UEF file is actually read)
	
	if command == 'extract':
	
		if len(args) < 2:
	
			print(extract_syntax)
			sys.exit()
	
		# Check whether the output path is a directory or a UEF file
		if string.lower(args[1][-4:]) == suffix+'uef':
	
			# Check whether the file already exists
			try:
				open(args[1]).close()
	
			except IOError:
	
				try:
					dest_uef = gzip.open(args[1], 'wb')
				except IOError:
					print("Couldn't open file %s for writing." % args[1])
					sys.exit()
	
				# Write the header for the file and the creator
				write_uef_header(dest_uef, UEF_major, UEF_minor)
				write_uef_creator(dest_uef, 'UEFtrans '+version)
	#			uef.close()
	
		else:
			# Get the leafname of the output path
			leafname = get_leafname(args[1])
		
			# See if the output directory exists
			try:
				os.listdir(args[1])
			except:
				try:
					os.mkdir(args[1])
					print('Created directory '+args[1])
				except:
					print("Couldn't create directory %s" % leafname)
					sys.exit()
	
	# Detailed information
	
	if command == 'wwwinfo':
	
		if len(args) < 1:
	
			print(wwwinfo_syntax)
			sys.exit()
	
		# Get the leafname of the output path
		leafname = get_leafname(args[0])
	
		# See if the output directory exists
		try:
			os.listdir(args[0])
		except:
			try:
				os.mkdir(args[0])
				print('Created directory '+args[0])
			except:
				print("Couldn't create directory %s" % leafname)
				sys.exit()
	
	
	# Decode the UEF file --------------------------------------------------
	
	eof = 0			# End of file flag
	write_file = ''		# Write the file using this name
	file_length = 0		# File length
	
	# List of chunks
	chunks = []
	
	# Unnamed file counter
	n = 1
	
	# Read chunks
	
	while eof == 0:
	
		# Read chunk ID
		chunk_id = in_f.read(2)
		if not chunk_id:
			eof = 1
			break
	
		chunk_id = str2num(2, chunk_id)
	
		length = str2num(4, in_f.read(4))
	
		if length != 0:
			chunks.append((chunk_id, in_f.read(length)))
		else:
			chunks.append((chunk_id, ''))

	# Close the input file
	in_f.close()
	
	
	# Chunks command
	
	if command == 'chunks':
	
		print('Chunks in %s' % uef_file)
	
		n = 0
	
		for c in chunks:
	
			if n % 16 == 0:
				sys.stdout.write(string.rjust('%i: '% n, 8))
	
			if c[0] == 0x0:
	
				# Originator
				sys.stdout.write('O ')
	
			elif c[0] == 0x1:
	
				# Instructions/manual
				sys.stdout.write('I ')
	
			elif c[0] == 0x2:
	
				# Author credits
				sys.stdout.write('C ')
	
			elif c[0] == 0x3:
	
				# Inlay scan
				sys.stdout.write('S ')
	
			elif c[0] == 0x5:
	
				# Target machine info
				sys.stdout.write('M ')
	
			elif c[0] == 0x6:
	
				# Multiplexing information
				sys.stdout.write('X ')
	
			elif c[0] == 0x7:
	
				# Extra palette
				sys.stdout.write('P ')
	
			elif c[0] == 0x100:
	
				# Block information (implicit start/stop bit)
				sys.stdout.write('# ')
	
			elif c[0] == 0x101:
	
				# Multiplexed (as 0x100)
				sys.stdout.write('#x')
	
			elif c[0] == 0x102:
	
				# Generic block information
				sys.stdout.write('* ')
	
			elif c[0] == 0x103:
	
				# Multiplexed generic block (as 0x102)
				sys.stdout.write('*x')
	
			elif c[0] == 0x110:
	
				# High pitched tone
				sys.stdout.write('- ')
	
			elif c[0] == 0x111:
	
				# High pitched tone with dummy byte
				sys.stdout.write('+ ')
	
			elif c[0] == 0x112:
	
				# Gap (silence)
				sys.stdout.write('_ ')
	
			elif c[0] == 0x113:
	
				# Change of baud rate
				sys.stdout.write('B ')
	
			elif c[0] == 0x120:
	
				# Position marker
				sys.stdout.write('! ')
	
			elif c[0] == 0x200:
	
				# Disc information
				sys.stdout.write('D ')
	
			elif c[0] == 0x201:
	
				# Standard disc side
				sys.stdout.write('d ')
	
			elif c[0] == 0x202:
	
				# Multiplexed disc side
				sys.stdout.write('dx')
	
			elif c[0] == 0x300:
	
				# Standard machine ROM
				sys.stdout.write('R ')
	
			elif c[0] == 0x301:
	
				# Multiplexed machine ROM
				sys.stdout.write('Rx')
	
			elif c[0] == 0x400:
	
				# 6502 standard state
				sys.stdout.write('6 ')
	
			elif c[0] == 0x401:
	
				# Electron ULA state
				sys.stdout.write('U ')
	
			elif c[0] == 0x402:
	
				# WD1770 state
				sys.stdout.write('W ')
	
			elif c[0] == 0x410:
	
				# Standard memory data
				sys.stdout.write('m ')
	
			elif c[0] == 0x411:
	
				# Multiplexed memory data
				sys.stdout.write('mx')
	
			elif c[0] == 0xff00:
	
				# Emulator identification string
				sys.stdout.write('E ')
	
			else:
				# Unknown
				sys.stdout.write('? ')
	
			if n % 16 == 15:
				sys.stdout.write('\n')
	
			n = n + 1
	
		print()
	
		# Exit
		sys.exit()
	
	
	# UEF file information
	originator, target_machine, keyboard_layout, emulator, features = read_uef_details(chunks)
	
	# Info command
	
	if command == 'info':
	
		# Split paragraphs
		originator = string.split(originator, '\012')
	
		print('File originator:')
		for line in originator:
			print(line)
		print()
		print('File format version: %i.%i' % (UEF_major, UEF_minor))
		print()
		print('Target machine : '+target_machine)
		print('Keyboard layout: '+keyboard_layout)
		print('Emulator       : '+emulator)
		print()
		if features != '':

			print('Contains:')
			print(features)
			print()

		# Exit
		sys.exit()
	
	
	# Find the positions of files in the list of chunks
	
	# List of files
	contents = []
	
	current_file = {}
	
	position = 0
	
	while True:
	
		position = find_next_block(chunks, position)
	
		if position == None:
	
			# No more blocks, so store the details of the last file in
			# the contents list
			if current_file != {}:
				contents.append(current_file)
			break
	
		else:
	
			# Read the block information
			name, load, exec_addr, data, block_number, last = read_block(chunks[position])
	
			if current_file == {}:
	
				# No current file, so store details
				current_file = {'name': name, 'load': load, 'exec': exec_addr, 'blocks': block_number, 'data': data}
	
				# Locate the first non-block chunk before the block
				# and store the position of the file
				current_file['position'] = find_file_start(chunks, position)
				# This may also be the position of the last chunk related to
				# this file in the archive
				current_file['last position'] = position
			else:
	
				# Current file exists
				if block_number == 0:
	
					# New file, so write the previous one to the
					# contents list, but before doing so, find the next
					# non-block chunk and mark that as the last chunk in
					# the file
#					current_file['last position'] = find_file_end(chunks, position)
	
					if current_file != {}:
						contents.append(current_file)
	
					# Store details of this new file
					current_file = {'name': name, 'load': load, 'exec': exec_addr, 'blocks': block_number, 'data': data}
	
					# Locate the first non-block chunk before the block
					# and store the position of the file
					current_file['position'] = find_file_start(chunks, position)
					# This may also be the position of the last chunk related to
					# this file in the archive
					current_file['last position'] = position
				else:
					# Not a new file, so update the number of
					# blocks and append the block data to the
					# data entry
					current_file['blocks'] = block_number
					current_file['data'] = current_file['data'] + data
	
					# Update the last position information to mark the end of the file
					current_file['last position'] = position
	
		# Increase the position
		position = position + 1
	
	
	
	# We now have a contents list which tells us
	# 1) the names of files in the archive
	# 2) the load and execution addresses of them
	# 3) the number of blocks they contain
	# 4) their data, and from this their length
	# 5) their start position (chunk number) in the archive
	
	# Catalogue command
	
	if command == 'cat':
	
		if contents == []:
	
			print('No files in '+uef_file)
	
		else:
	
			print('Contents of %s:' % uef_file)
	
			file_number = 0
	
			for file in contents:
	
				# Converts non printable characters in the filename
				# to ? symbols
				new_name = printable(file['name'])
	
				print(string.expandtabs(string.ljust(str(file_number), 3)+': '+
							string.ljust(new_name, 16)+
							string.upper(
								string.ljust(hex(file['load'])[2:], 10) +'\t'+
								string.ljust(hex(file['exec'])[2:], 10) +'\t'+
								string.ljust(hex(len(file['data']))[2:], 6)
							) +'\t'+
							'chunks %i to %i' % (file['position'], file['last position']) ))
	
				file_number = file_number + 1
	
		# Exit
		sys.exit()
	
	
	# Detailed information command (wwwinfo)
	
	if command == 'wwwinfo':
	
		# Attempt to open the index file
		index_file = args[0]+os.sep+'index'+suffix+'html'
		try:
			index = open(index_file, 'w')
	
		except IOError:
			print("Couldn't open the index file %s" % index_file)
			sys.exit()
	
		# The leafname variable is the leafname of the input file
		leafname = get_leafname(uef_file)
	
		# Write the HTML header
		index.write('<html>\n<head>\n<title>Information on %s</title>\n</html>\n\n<body>\n<h1>Information on %s</h1>\n' % (browsable(leafname), browsable(leafname)))
	
		# Write useful information to the index file
	
		index.write('[Full path: %s]\n' % browsable(uef_file))

		index.write('<h2>File creator:</h2>\n')

		# Split paragraphs
		originator = string.split(originator, '\012')
	
		for paragraph in originator:
	
			index.write('<p>\n%s\n</p>\n' % browsable(paragraph))
	
		index.write('<p>\nFile format version: %i.%i\n</p>\n' % (UEF_major, UEF_minor))

		index.write('<p>\n<strong>Target machine: %s</strong>\n</p>\n' % browsable(target_machine))
		index.write('<p>\n<strong>Keyboard layout: %s</strong>\n</p>\n' % browsable(keyboard_layout))
		index.write('<p>\n<strong>Emulator: %s</strong>\n</p>\n' % browsable(emulator))
	
		index.write('\n')
	
		# Catalogue of files
	
		index.write('<h2>Contents of %s:</h2>\n' % browsable(leafname))
	
		if contents == []:
	
			index.write('<p>No files.</p>\n')
	
		else:
	
			index.write('<pre>\n')
	
			file_number = 0
	
			for file in contents:
	
				# Converts non printable characters in the filename
				# to ? symbols
				new_name = browsable(file['name'])
	
				index.write(
						string.expandtabs(
							string.ljust(str(file_number), 3)+': '+
							string.ljust(new_name, 16)+
							string.upper(
								string.ljust(hex(file['load'])[2:], 10) +'\t'+
								string.ljust(hex(file['exec'])[2:], 10) +'\t'+
								string.ljust(hex(len(file['data']))[2:], 6)
							) +'\t'+
							'chunks %i to %i' % (file['position'], file['last position'])
						) + '\n'
					)
	
				file_number = file_number + 1
	
			index.write('</pre>\n')
	
		index.write('\n')
	
		# Find other content (credits, inlay scans, instructions, etc.)
	
		pos, instructions = find_next_chunk(chunks, 0, [0x1])
	
		if instructions != None:
	
			# Take chunk data
			if instructions[1] != '':

				instructions = instructions[1]
			else:
				instructions = '<strong>[Instructions are missing.]</strong>'
	
			# Remove trailing null bytes
			while instructions[-1] == '\000':
	
				instructions = instructions[:-1]
	
			index.write('<h2>Instructions</h2>\n')
	
			# Write the instructions to the index file
			# Split paragraphs
			instructions = string.split(instructions, '\012')
	
			for paragraph in instructions:
	
				index.write('<p>\n%s</p>\n' % browsable(paragraph))
	
			index.write('\n')
	
		pos, credits = find_next_chunk(chunks, 0, [0x2])
	
		if credits != None:
	
			# Take chunk data
			if credits[1] != '':

				credits = credits[1]
			else:
				credits = '<strong>[Credits are missing.]</strong>'
	
			# Remove trailing null bytes
			while credits[-1] == '\000':
	
				credits = credits[:-1]
	
			# Write the credits to the index file
			index.write('<h2>Credits</h2>\n')
	
			# Split paragraphs
			credits = string.split(credits, '\012')
	
			for paragraph in credits:
	
				index.write('<p>\n%s\n</p>\n' % browsable(paragraph))
	
			index.write('\n')
	
		pos, inlay = find_next_chunk(chunks, 0, [0x3])
	
		if inlay != None:
	
			# There is an inlay. Let's assume it is in a format which
			# can be rendered satisfactorily in a WWW browser.
			index.write('<h2>Inlay</h2>\n')
			inlay_path = args[0] + os.sep + 'inlay'
			index.write('<p align="center">\n<a href="inlay"><img src="inlay"></a>\n</p>\n')
	
			# Write the inlay to the destination directory
			try:
				open(inlay_path, 'wb').write(inlay[1])
			except IOError:
				print("Couldn't write the inlay to the file %s" % inlay_path)
	
			index.write('\n')
	
		# End the index file and close it
		index.write('</body>\n</html>\n')
		index.close()
	
		# Exit
		sys.exit()
	
	
	# Insert files at a particular position
	
	if command == 'insert':
	
		if len(args) < 2:
	
			# Must have two arguments to this command
			print(insert_syntax)
			sys.exit()
	
		# There are two versions of this command: one inserts files, the other inserts chunks.
		# The first argument determines which version is used:
		#
		#         1) If the position has a "c" at the beginning then we interpret the second
		#            argument as a list of files to be treated as chunks.
		#
		#         2) If the position doesn't have a "c" at the beginning then we interpret the
		#            second argument as a file position and have to determine the chunk
		#            position before we can insert the files.
	
		if args[0][0] == 'c':
	
			# We are inserting chunks
			try:
				position = int(args[0][1:])
			except ValueError:
				print(insert_syntax)
				sys.exit()
	
			if position < 0:
		
				print('Position must be zero or greater.')
				sys.exit()
	
			# Names of files to insert as chunks (comma-separated list)
			file_names = string.split(args[1], ',')
	
			# Insert the chunks in the list at the specified position
			chunks = chunks[:position] + encode_chunks(file_names) + chunks[position:]
	
		else:
	
			# We are inserting files
	
			# File position
			try:
				file_position = int(args[0])
			except ValueError:
				print(insert_syntax)
				sys.exit()
	
			if file_position < 0:
		
				print('Position must be zero or greater.')
				sys.exit()
		
			# Find the chunk position which corresponds to the file_position
			if contents != []:
		
				# There are files already present
				if file_position >= len(contents):
			
					# Position the new files after the end of the last file
					position = contents[-1]['last position'] + 1
			
				else:
			
					# Position the new files before the end of the file
					# specified
					position = contents[file_position]['position']
			else:
				# There are no files present in the archive, so put them after
				# all the other chunks
				position = len(chunks)
	
			# Names of files to insert (comma-separated list)
			file_names = string.split(args[1], ',')
	
			# Insert the chunks in the list at the specified position
			chunks = chunks[:position] + create_chunks(file_names) + chunks[position:]
	
		# Open the UEF file for writing
		try:
			uef = gzip.open(uef_file, 'wb')
		except IOError:
			print("Couldn't open %s for writing." % uef_file)
			sys.exit()
	
		# Write the UEF file header
		write_uef_header(uef, UEF_major, UEF_minor)
	
		# Write the chunks to the file
		write_chunks(uef, chunks)
	
		# Close the file
		uef.close()
	
		# Exit
		sys.exit()
	
	
	# Append command
	
	if command == 'append':
	
		if len(args) < 1:
	
			# Must have one arguments to this command
			print(append_syntax)
			sys.exit()
	
		# Names of files to insert (comma-separated list)
		file_names = string.split(args[0], ',')
	
		# Put the new file chunks after all the other chunks
		chunks = chunks + create_chunks(file_names)
	
		# Open the UEF file for writing
		try:
			uef = gzip.open(uef_file, 'wb')
		except IOError:
			print("Couldn't open %s for writing." % uef_file)
			sys.exit()
	
		# Write the UEF file header
		write_uef_header(uef, UEF_major, UEF_minor)
	
		# Write the chunks to the file
		write_chunks(uef, chunks)
	
		# Close the file
		uef.close()
	
		# Exit
		sys.exit()
	
	
	if command == 'extract':
	
		# File positions of files to extract
		positions = string.split(args[0], ',')
	
		# Destination path in which to put the files (any directories
		# should have already been created)
		out_path = args[1]
	
		# This command will extract chunks from the list of chunks using a chunk position given and
		# extract files using the file position which is converted to a chunk position first.
	
#		# Generate a list of chunk positions based on the file positions
#		if contents == []:
#	
#			print 'There are no files to extract.'
#			sys.exit()
	
		# There are files already present
	
		# Stem for unknown filenames
		created = []
		stem = 'noname'
		new_file = 0
	
		for position in positions:
	
			if position[0] == 'c':
	
				# Extracting chunk, not file
				position = int(position[1:])
	
				if string.lower(out_path[-4:]) == suffix+'uef':
			
					# Writing a file in the archive to another archive
					# Append chunk to the specified output file
					try:
#						write_chunks(gzip.open(out_path, 'ab'), chunks[position:position+1])
						write_chunks(dest_uef, chunks[position:position+1])
	
					except IOError:
						print("Couldn't write to file %s for chunk %i." % (out_path, position))
				else:
					try:
						# Send chunk to a decoding function
						decode_chunk(out_path, chunks[position], position)
	
					except ValueError:
						print(extract_syntax)
						sys.exit()
	
			else:
				# Export the file
	
				try:
					file_position = int(position)
				except ValueError:
					print(extract_syntax)
					sys.exit()
	
				# Find the chunk position which corresponds to the file position
				if file_position < 0 or file_position >= len(contents):
		
					print('File position %i does not correspond to an actual file.' % file_position)
				else:
					# Find the start and end positions
					start_pos = contents[file_position]['position']
					end_pos = contents[file_position]['last position']
	
					if string.lower(out_path[-4:]) == suffix+'uef':
			
						# Writing a file in the archive to another archive
						try:
#							write_chunks(gzip.open(out_path, 'ab'), chunks[start_pos:end_pos+1])
							write_chunks(dest_uef, chunks[start_pos:end_pos+1])
						except IOError:
							print("Couldn't write file %i to archive %s" % (file_position, out_path))
					else:
						# Writing a file in the archive to a file in a directory
	
						# Create a file with the correct name in the
						# output directory
						name = contents[file_position]['name']
						write_name = printable(name)
						load = contents[file_position]['load']
						exe = contents[file_position]['exec']
						length = len(contents[file_position]['data'])
	
						export_file(out_path, chunks[start_pos:end_pos+1], name, write_name, load, exe, length)
	
		if string.lower(out_path[-4:]) == suffix+'uef':
	
			# Close destination UEF file
			dest_uef.close()
	
		# Exit
		sys.exit()
	
	
	if command == 'remove':
	
		if len(args) < 1:
	
			# One argument required
			print(remove_syntax)
			sys.exit()
	
		# As with the insert command, there are two versions of this command. The first will remove
		# chunks from the list using a chunk position given, the second will remove files using the
		# file position which is converted to a chunk position first.
	
		# File positions of files to extract
		file_positions = string.split(args[0], ',')
	
#		# Generate a list of chunk positions based on the file positions
#		if contents == []:
#	
#			print 'There are no files to remove.'
#			sys.exit()
	
		positions = []
		for file_position in file_positions:
	
			if file_position[0][0] == 'c':
	
				# Removing chunk, not file
				try:
					# Append the chunk number to the list of chunks to leave out
					positions.append(int(file_position[1:]))
	
				except ValueError:
					print(extract_syntax)
					sys.exit()
	
			else:
				try:
					file_position = int(file_position)
	
				except ValueError:
					print(extract_syntax)
					sys.exit()
	
				# Find the chunk position which corresponds to the file position
				if file_position < 0 or file_position >= len(contents):
			
					print('File position %i does not correspond to an actual file.' % file_position)
		
				else:
					# Add the chunk positions within each file to the list of positions
					positions = positions + range(contents[file_position]['position'],
					                              contents[file_position]['last position'] + 1)
	
		# Create a new list of chunks without those in the positions list
		new_chunks = []
		for c in range(0, len(chunks)): 
	
			if c not in positions:
				new_chunks.append(chunks[c])
	
		# Open the UEF file for writing
		try:
			uef = gzip.open(uef_file, 'wb')
		except IOError:
			print("Couldn't open %s for writing." % uef_file)
			sys.exit()
	
		# Write the UEF file header
		write_uef_header(uef, UEF_major, UEF_minor)
	
		# Write the chunks to the file
		write_chunks(uef, new_chunks)
	
		# Close the file
		uef.close()
	
		# Exit
		sys.exit()
	
	
	# Not a recognised command
	print_help('general')
	
	# Exit
	sys.exit()
