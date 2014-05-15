"""
    utils.py
    ------

    This file is part of NODE - the NORX Differential-Search Engine

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import time

def init_csv( header, path, mode = 'w' ):
    with open( path, mode ) as f:
        f.write( '{}\n'.format(header) )
    assert f.closed

def to_csv( l, path, mode = 'a' ):
    with open( path, mode  ) as f:
        for line in l:
            s = ','.join( line )
            f.write( '{}\n'.format( s ) )
    assert f.closed


def timestamp():
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())
