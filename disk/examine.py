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

# Code to walk through an ADFS disk image

import sys

# turn this on to get a verbose dump of everything we look at, including file contents
NOISY = 0

# to save space, this can be a bitfield in C.
# 1280 sectors = 160 bytes
# 2560 sectors = 320 bytes
class FreeSpaceMap:
    def __init__(self):
        self.map = []
    def add_space(self, start, length):
        while len(self.map) < start + length:
            self.map.append(0)
        for x in range(start, start + length):
            if self.map[x]:
                print("WARNING: sector %d is listed twice in the free map" % x)
            self.map[x] = 1
    def count(self):
        return sum(1 if x else 0 for x in self.map)
    def last(self):
        return len(self.map)

# standard checksum algorithm for 255 bytes of data
def checksum(chunk):
    assert len(chunk) == 255
    s = 255
    for a in range(254, -1, -1):
        if s > 255: s = (s + 1) % 256
        s += ord(chunk[a])
    return s % 256

# chop a string at the first \x00 or \x0d
def adfs_string(chunk):
    s = ''
    for c in chunk:
        c = chr(ord(c) & 0x7f)
        if c in '\x00\x0d':
            break
        s += c
    return s

class Disk(object):
    def __init__(self, fn):
        self.image = open(fn).read()

    def read1(self, ptr):
        return ord(self.image[ptr])

    def read2(self, ptr):
        return (ord(self.image[ptr+1]) << 8) | (ord(self.image[ptr]))

    def read3(self, ptr):
        return (ord(self.image[ptr+2]) << 16) | (ord(self.image[ptr+1]) << 8) | (ord(self.image[ptr]))

    def read4(self, ptr):
        return ((ord(self.image[ptr+3]) << 24)
            | (ord(self.image[ptr+2]) << 16)
            | (ord(self.image[ptr+1]) << 8)
            | (ord(self.image[ptr])))

class ADFSDisk(Disk):
    def __init__(self, fn):
        super(ADFSDisk, self).__init__(fn)

        # Known ADFS formats:
        # S = 160kB, 1 side, 40 tracks, 16 x 256-byte sectors/track
        # M = 320kB, 1 side, 80 tracks, 16 x 256-byte sectors/track
        # L = 640kB, 2 sides, 80 tracks/side, 16 x 256-byte sectors/track
        # D, E = 800kB, 2 sides, 80 tracks/side, 5 x 1024-byte sectors/track

        print("%d bytes" % len(self.image))
        sectors = len(self.image) / 256
        print("%d sectors total" % sectors)
        tracks = sectors / 16
        print("%d tracks total" % tracks)

        print(repr(self.image[:256]))

        # first two tracks are the free space map and header

        # 0f6-0f8 = l3 fileserver sec1 partition
        # 0f9-0fb = risc os disk name

        # 0fc-0fe = total # of sectors
        self.sector_count = self.read2(0xfc)
        print("total sector count %d" % self.sector_count)

        self.format = {
            640: 'S',
            1280: 'M',
            2560: 'L',
            }.get(self.sector_count, None)
        if self.format is None:
            print("Unrecognized format: %d sectors" % sectors)
        else:
            print("ADFS '%s' format disk image" % self.format)

        # 0ff = checksum
        print("checksum %x; calculated as %x" % (self.read1(0xff), checksum(self.image[0:255])))

        # 1f6-1f8 = l3 fileserver sec2 partition
        # 1f9-1fa = risc os disk name

        # 1fb-1fc = disk ID
        print("disk ID %x" % self.read2(0x1fb))

        # 1fd = boot option (*opt 4)
        print("boot option %x" % self.read1(0x1fd))

        # 1fe = ptr to end of free space list (= 3 * number of blocks)
        end_free_space_list = self.read1(0x1fe)
        if NOISY: print("free space list ends at %x" % end_free_space_list)

        # 1ff = checksum
        print("checksum %x; calculated as %x" % (self.read1(0x1ff), checksum(self.image[256:511])))

        self.sectors_used = FreeSpaceMap()
        self.sectors_used.add_space(0, 2)  # disk header

        # free space list
        latest_ref = 0
        bytes_free = 0
        self.fsm = FreeSpaceMap()
        for offset in range(0, end_free_space_list, 3):
            start_sector, length = self.read3(offset), self.read3(offset + 256)
            self.fsm.add_space(start_sector, length)
            self.sectors_used.add_space(start_sector, length)
            if length:
                print("free space: sector %06x-%06x (%d bytes)" % (
                    start_sector, start_sector + length, length * 256))
                if start_sector + length > latest_ref: latest_ref = start_sector + length
                bytes_free += length * 256
        if bytes_free != 256 * self.fsm.count():
            print("WARNING: dupes in free space list")
        print("%d bytes free.  latest sector mentioned = 0x%x / %d (so disk is at least %d bytes)" % (
            256 * self.fsm.count(), latest_ref, latest_ref, latest_ref * 256))
        assert latest_ref == self.fsm.last()

        # now walk directories!
        self.walk(2, '$')

        sectors_seen = self.sectors_used.count()
        print("sectors seen: %d" % sectors_seen)
        if sectors_seen != self.sector_count:
            print("WARNING: seen only %d sectors out of %d; maybe some are skipped as bad blocks?" % (
                sectors_seen, self.sector_count))

    def walk(self, dir_sector, dir_name):
        print("%s: Walking directory, starting from sector %d" % (dir_name, dir_sector))
        self.sectors_used.add_space(dir_sector, 5)  # 5 sectors for a dir
        start = dir_sector * 256
        # header at 0:5
        main_seq_1 = self.read1(start + 0x4fa)
        print("%s: sequence number: %d" % (dir_name, main_seq_1))
        header = self.image[start+1:start+5]
        if header != 'Hugo': print("WARNING: bad header: %s" % repr(header))
        # footer at 4cb:500
        if NOISY: print("should be 0: %d" % self.read1(start + 0x4cb))
        dir_name2 = adfs_string(self.image[start + 0x4cc:start + 0x4d6])
        print("%s: dir name: %s" % (dir_name, repr(dir_name2)))
        if dir_name2 != dir_name.rsplit(".", 1)[-1]:
            print("WARNING: dir name %s doesn't match name from parent %s" % (
                repr(dir_name2), repr(dir_name)))
        if NOISY: print("parent dir sector: %d" % self.read3(start + 0x4d6))
        dir_title = adfs_string(self.image[start + 0x4d9:start + 0x4ec])
        print("%s: dir title: %s" % (dir_name, repr(dir_title)))
        # 4ec-4f9 reserved
        main_seq_2 = self.read1(start + 0x4fa)
        if main_seq_1 != main_seq_2: print("WARNING: main seq mismatch; broken directory")
        identifier = self.image[start + 0x4fb:start + 0x4ff]
        if identifier != 'Hugo': print("WARNING: bad identifier: %s" % repr(identifier))
        if NOISY: print("checksum: 0x%x" % self.read1(start + 0x4ff))

        # entries at 5, 1f, 39, ..., 4b1
        for entry_start in range(start + 5, start + 0x4cb, 0x1a):
            if NOISY: print("DIR ENTRY at 0x%x" % entry_start)
            name_attr = self.image[entry_start:entry_start+10]
            name = adfs_string(name_attr)
            if name == '':
                continue
            attr = ''
            if ord(name_attr[0]) & 0x80: attr += 'R'
            if ord(name_attr[1]) & 0x80: attr += 'W'
            if ord(name_attr[2]) & 0x80: attr += 'L'
            if ord(name_attr[3]) & 0x80: attr += 'D'
            if ord(name_attr[4]) & 0x80: attr += 'E'
            load = self.read4(entry_start + 0xa)
            exec_addr = self.read4(entry_start + 0xe)
            file_len = self.read4(entry_start + 0x12)
            start_sec = self.read3(entry_start + 0x16)
            file_seq = self.read1(entry_start + 0x19)
            print("%s: %s %s attr %s load %x exec %x length %x start sector %x sequence %d" % (
                dir_name,
                "DIR" if 'D' in attr else "FILE",
                name,
                attr,
                load,
                exec_addr,
                file_len,
                start_sec,
                file_seq,
                ))

            if 'D' in attr:
                subdir_name = "%s.%s" % (dir_name, name)
                #print "RECURSE INTO FOLDER %s\n" % subdir_name
                self.walk(start_sec, subdir_name)
                #print "\nRETURN FROM FOLDER %s" % subdir_name
            else:
                self.sectors_used.add_space(start_sec, (file_len + 255) // 256)
                if NOISY:
                    # dump file contents
                    file_start = start_sec * 256
                    for ptr in range(0, file_len, 256):
                        print("%s.%s %x: %s" % (
                            dir_name,
                            name,
                            ptr,
                            repr(self.image[file_start + ptr:min(file_start + ptr + 256, file_start + file_len)]),
                        ))

class DFSDisk(Disk):
    def __init__(self, fn):
        super(DFSDisk, self).__init__(fn)

        print("DFS disk, %d bytes" % len(self.image))

        print("title %s" % repr(adfs_string(self.image[0:8] + self.image[0x100:0x104])))

        print("cycle %x" % self.read1(0x104))

        self.sectors_used = FreeSpaceMap()
        self.sectors_used.add_space(0, 2)  # disk header

        self.sector_count = ((self.read1(0x106) & 3) << 8) | self.read1(0x107)
        print("sector count %d, i.e. total size %d" % (
            self.sector_count, self.sector_count * 256))

        self.boot_opt = ((self.read1(0x106) & 0x30) >> 4)
        print("boot option %d" % self.boot_opt)

        last_cat_entry = self.read1(0x105)
        for ptr in range(0x08, last_cat_entry + 8, 8):
            file_entry = self.image[ptr:ptr+8]
            file_info = [ord(x) for x in self.image[0x100 + ptr:0x108 + ptr]]
            # print "file entry %s %s ---" % (
            #     `file_entry`,
            #     ' '.join('%02x' % c for c in file_info),
            #     ),
            names = ''.join(chr(ord(x) & 0x7f) for x in file_entry)
            filename = names[:7].rstrip()
            dirname = names[7]
            locked = ord(file_entry[7]) & 0x80
            start_sec = file_info[7] | ((file_info[6] & 0x03) << 8)
            load_addr = file_info[0] | (file_info[1] << 8) | ((file_info[6] & 0x0c) << 14)
            length = file_info[4] | (file_info[5] << 8) | ((file_info[6] & 0x30) << 12)
            sectors_used = (length + 0xff) // 0x100
            exec_addr = file_info[2] | (file_info[3] << 8) | ((file_info[6] & 0xc0) << 10)
            end_sec = start_sec + sectors_used - 1
            print("%02x: %s.%s sector %x-%x load %x length %x exec %x %s" % (
                ptr,
                dirname,
                filename,
                start_sec,
                end_sec,
                load_addr,
                length,
                exec_addr,
                "LOCKED" if locked else "unlocked",
            ))
            self.sectors_used.add_space(start_sec, sectors_used)

        print("sectors seen: %d / %d; bytes free %d used %d total %d" % (
            self.sectors_used.count(),
            self.sector_count,
            (self.sector_count - self.sectors_used.count()) * 245,
            self.sectors_used.count() * 256,
            self.sector_count * 256,
            ))

if __name__ == '__main__':
    fn, = sys.argv[1:]
    if fn.endswith(".adf"):
        print("%s ends with .adf so processing as adfs" % fn)
        ADFSDisk(fn)
    else:
        DFSDisk(fn)
