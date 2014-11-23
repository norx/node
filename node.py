#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    node.py
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

__author__ = 'Philipp Jovanovic'
__email__ = 'philipp@jovanovic.io'
__version__ = 'v20141009'
__license__ = 'BSD (3-Clause)'
__description__='NODE: the (NO)RX (D)ifferential-Search (E)ngine'

import sys
import argparse
import src.utils as utils
import config.cmd as cmd

def main():

    p = argparse.ArgumentParser(description='{} ({})'.format(__description__,__version__))
    p.add_argument('-d',help="set type of search database",required=True,choices=['basic','enum','bit'])
    p.add_argument('-e',help="set type of search problem (see config.json)",required=True)
    p.add_argument('-p',help="print the CVC code and return",action='store_true')
    args = p.parse_args()

    path = './tmp/'
    f = path + '{}-{}-{}.csv'.format(args.d,args.e,utils.timestamp())

    if args.d == 'basic':
        import src.search.basic as search
        cmds = cmd.basic
    elif args.d == 'enum':
        import src.search.enum as search
        cmds = cmd.enum
    elif args.d == 'bit':
        import src.search.bit as search
        cmds = cmd.bit

    """ check if stp and solver are in PATH or node/bin """
    stp = utils.which('stp')
    solver = utils.which(cmds[args.e][0])
    if stp == None:
        print "stp not found in PATH or in node/bin"
        return 1
    if solver == None:
        print "solver {} not found in PATH or in node/bin".format(cmds[args.e][0])
        return 1

    if not args.p:
        """ start search """
        solutions = search.do(*cmds[args.e])
        if solutions != None:
            utils.to_csv( solutions, f )
            print "Solution(s) written to {}".format(f)
    else:
        """ print CVC code """
        print search.cvc(*cmds[args.e])


if __name__ == '__main__':
    sys.exit(main())
