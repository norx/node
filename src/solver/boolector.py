"""
    solver/boolector.py - a python wrapper for boolector.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import subprocess
import re

NAME = 'boolector'
SPATH = './bin/boolector'
SIGNAL = 'unsat'
SFLAGS = ['--model','--hex']
TFLAGS = None

# call boolector
def do( stdin = '', flags = SFLAGS, path = SPATH ):
    popen = subprocess.Popen( [ path ] + flags, stdout = subprocess.PIPE, stdin = subprocess.PIPE )
    return popen.communicate( input = stdin )[0]

# parse output from boolector
def parse( output ):
    x = {}
    for line in output.split('\n'):
        key = re.search( '\|(\w)*\|', line )
        val = re.search( ' (\w)*',line )
        if key != None and val != None:
            x[ key.group(0)[1:-1] ] = '0x{}'.format( val.group(0)[1:] )
    return x
