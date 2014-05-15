"""
    search/enum.py - enumerate all differentials of a given weight.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import sys
from src.norx import NORX
import src.solver.stp as setup

# solver_t: solver type
# ws: word size
# steps: number of steps
# weight: target weight
# enum_max: maximal number of differentials
# search_t: search type {full,initN,initNK,rate}
# diag: start with a diagonal step {true,false}
def do( solver_t, ws, steps, weight, enum_max, search_t, diag ):

    if solver_t == 'boolector':
        import src.solver.boolector as solver
    elif solver_t == 'stp':
        import src.solver.stp as solver
    else:
        print 'Unknown solver!'
        return

    norx = NORX( ws, steps, weight, search_t, diag )
    i = 1

    solutions = []

    print 'ENUM: {} {} {} {} {} {}'.format( solver_t, search_t, ws, steps, weight, enum_max )
    while i != enum_max:
        print '{}'.format(i),
        sys.stdout.flush()

        # setup search problem for solver
        sp = setup.do( stdin = norx(), flags = setup.TFLAGS[solver_t] )

        # solve
        output = solver.do( stdin = sp )

        if solver.SIGNAL in output:
            print "Done."
            break
        else:
            differential = solver.parse( output )
            x = norx.extract_input( differential )
            z = norx.extract_output( differential )
            norx.exclude( x, z )
            v = [ str(weight) ] + [ x[key] for key in sorted( x.keys() ) ] + [ str(weight) ] + [ z[key] for key in sorted( z.keys() )]
            solutions.append(v)
            i += 1

    return solutions


"""return cvc code only"""
def cvc( solver_t, ws, steps, weight, enum_max, search_t, diag )
    norx = NORX( ws, steps, weight, search_t, diag )
    return norx()

