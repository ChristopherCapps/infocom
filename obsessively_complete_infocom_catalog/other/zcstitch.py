#!/usr/bin/env python3

# Combine a set of split disk files back into a Z-code game file.
#
# As part of their release process, Infocom would split a large game
# file into several disk images. (This seems to have been done only for
# v6 games, so it was probably supported only by the v6 interpreters.)
#
# If you see a set of files like "journey.d1" through "journey.d5",
# they are probably split disk images of this sort. You can do
#
#   zcstitch.py journey.d* -o journey.z6
#
# ...to reconstruct the original file.
#
# This process pads the game file to a block boundary (multiple of 512 bytes).
# Use the --trim option to trim the padding to the Z-code's encoded length.

import sys
import struct
import optparse

popt = optparse.OptionParser()

popt.add_option('-o', '--out',
                action='store', dest='destfile', default='out.dat',
                help='write game file here')
popt.add_option('-t', '--trim',
                action='store_true', dest='trim',
                help='trim game file to encoded length')
popt.add_option('-v', '--verbose',
                action='store_true', dest='verbose',
                help='print verbose output')

(opts, args) = popt.parse_args()

filenames = args
if not filenames:
    print('usage: zcstitch.py game.d1 game.d2...')
    sys.exit()

def readword(dat, pos):
    val = dat[ pos*2 : pos*2+2 ]
    return struct.unpack('>H', val)[0]

dats = []
for filename in filenames:
    fl = open(filename, 'rb')
    dat = fl.read()
    fl.close()
    dats.append(dat)
dat = None

firstdat = dats[0]

diskcount = readword(firstdat, 1)
if diskcount != len(filenames):
    print('%d files supplied but the first one has a count of %d' % (len(filenames), diskcount,))
    sys.exit()

# The file data is measured in "blocks" of 200 bytes (100 words).
    
result = bytearray()

indexpos = 12

for disknum, dat in enumerate(dats):
    rangecount = readword(firstdat, indexpos)
    for rx in range(rangecount):
        srcstart = readword(firstdat, indexpos+rx*3+2)
        srcend = readword(firstdat, indexpos+rx*3+3)
        deststart = readword(firstdat, indexpos+rx*3+4)
        count = (srcend-srcstart+1)*0x200
        if deststart*0x200+count > len(dat):
            raise Exception('Attempted to read past file end')
        while len(result) < (srcend+1) * 0x200:
            result.append(0)
        if opts.verbose:
            print('Copying %d bytes from disk %d, pos %d to pos %d' % (count, disknum, srcstart*0x200, deststart*0x200))
        result[srcstart*0x200 : srcstart*0x200+count] = dat[deststart*0x200 : deststart*0x200+count]
    indexpos += 3*rangecount+4

zversion = int(result[0])
release = int(0x100 * result[2] + result[3])
serial = result[18:24].decode('latin-1')

length = int(0x100 * result[26] + result[27])
if zversion <= 3:
    length *= 2
elif zversion <= 5:
    length *= 4
else:
    length *= 8

print('z%d release %s serial %s' % (zversion, release, serial,))
print('desired length %d, actual length %d' % (length, len(result),))
if opts.trim and len(result) > length:
    print('(trimming to %d)' % (length,))
    del result[ length : ]

if opts.destfile:
    fl = open(opts.destfile, 'wb')
    fl.write(result)
    fl.close()

    print('Wrote %s (%d bytes)' % (opts.destfile, len(result),))

