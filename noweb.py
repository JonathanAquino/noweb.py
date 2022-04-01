#! /usr/bin/env python3

"""
noweb.py
By Jonathan Aquino (jonathan.aquino@gmail.com)

This program extracts code from a literate programming document in "noweb" format.
It was generated from noweb.py.txt, itself a literate programming document.
For more information, including the original source code and documentation,
see http://jonaquino.blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html
"""

import os, sys, re, argparse
parser = argparse.ArgumentParser(
    prog=os.path.basename(__file__),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__
)
parser.add_argument(
    'filename', metavar='filename', nargs=1,
    help='the source file from which to extract')
parser.add_argument(
    '--ref', '-R',
    required=True,
    help='the root chunk to be extracted',
)
parser.add_argument(
    '--out', '-o',
    help='specify an output file',
)
parser.add_argument(
    '--exectuable', '-x',
    help='if an output file was specified, chmod +x that file',
)
opts = parser.parse_args()
outputChunkName = opts.ref
filename = opts.filename[0]
outfile = open(opts.out, 'w') if opts.out else sys.stdout
file = open(filename)
chunkName = None
pendingChunkName = None
chunks = {}
REFERENCE = "^(\s*)#\*(.*)\*#"
CHUNKNAME = "^\*(.*)\*$"
CHUNKDELIMITER = "^```(\w*)\s+"

for line in file:
    match = re.match(CHUNKNAME, line)
    if match:
        chunkName = None
        pendingChunkName = match.group(1)
        continue
    match = re.match(CHUNKDELIMITER, line)
    if match:
        if pendingChunkName and not chunkName:
            chunkName = pendingChunkName
            pendingChunkName = None
            if not chunkName in chunks:
                chunks[chunkName] = []
        else:
            chunkName = pendingChunkName = None
        continue
    if chunkName:
        chunks[chunkName].append(line)

def expand(chunkName, indent):
    chunkLines = chunks[chunkName]
    expandedChunkLines = []
    for line in chunkLines:
        match = re.match(REFERENCE, line)
        if match:
            more_indent = match.group(1)  # possible future use?
            chunkName = match.group(2)
            expandedChunkLines.extend(expand(
                chunkName,
                indent + more_indent
            ))
        else:
            expandedChunkLines.append(indent + line)
    return expandedChunkLines

for line in expand(outputChunkName, ""):
    print(line.rstrip(), file=outfile)
if opts.out and opts.executable:
    os.system("chmod +x " + opts.out)
