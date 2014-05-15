"""
    solver/cryptominisat.py - a python wrapper for cryptominisat.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import subprocess

NAME = 'cryptominisat'
SPATH = './bin/cryptominisat'
SIGNAL = 'UNSATISFIABLE'
SFLAGS = ['--threads=1','output_0.cnf']
TFLAGS = None

# call cryptominisat
def do( stdin = '', flags = SFLAGS, path = SPATH ):
    popen = subprocess.Popen( [ path ] + flags, stdout = subprocess.PIPE, stdin = subprocess.PIPE )
    return popen.communicate()[0]

# output of cryptominisat can't be parsed
def parse( output ):
    return output
