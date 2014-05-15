"""
    solver/stp.py - a python wrapper for stp.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import subprocess
import re
from src.utils import which

NAME = 'stp'
SIGNAL = 'Valid'
SFLAGS = ['--cryptominisat']
TFLAGS = { 'boolector': ['--print-back-SMTLIB2'], 'cryptominisat': ['--output-CNF', '--exit-after-CNF'], 'stp': ['--return'] }

"""call stp"""
def do( stdin = '', flags = SFLAGS ):
    if flags == ['--return']:
        return stdin
    try:
        popen = subprocess.Popen( [ which(NAME) ] + flags, stdout = subprocess.PIPE, stdin = subprocess.PIPE )
        return popen.communicate( input = stdin )[0]
    except AttributeError as e:
        raise e

"""parse output from stp"""
def parse( output ):
    x = {}
    for line in output.split( '\n' ):
        key = re.search( '(\w)* =', line )
        val = re.search( '0x(\w)*', line )
        if key != None and val != None:
            x[ key.group(0)[:-2] ] = val.group(0)
    return x
