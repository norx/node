"""
    search/basic.py - basic differential search.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import sys
from src.norx import NORX
import src.solver.stp as setup

"""
    solver_t: solver type
    ws: word size
    steps: number of steps
    w_min: min weight for search
    w_max: max weight for search
    search_t: search type {full,initN,initNK,rate}
    diag: start with a diagonal step {true,false}
    var_t: variable type to fix with differences {'input','output'}
    var_d: difference values
"""
def do( solver_t, ws, steps, w_min, w_max, search_t, diag, var_t, var_d ):

    if solver_t == 'boolector':
        import src.solver.boolector as solver
    elif solver_t == 'cryptominisat':
        import src.solver.cryptominisat as solver
    elif solver_t == 'stp':
        import src.solver.stp as solver
    else:
        print 'unknown solver'
        return

    w = w_min

    solutions = []

    print 'DFS: {} {} {} {}'.format( solver_t, search_t, ws, steps )
    while w <= w_max:
        print '{}'.format( w ),
        sys.stdout.flush()

        norx = NORX( ws, steps, w, search_t, diag )

        if var_t in norx.set_variables.keys():
            norx.set_variables[var_t]( var_d )

        # setup search problem for solver
        sp = setup.do( stdin = norx(), flags = setup.TFLAGS[solver_t] )

        # solve
        output = solver.do( stdin = sp )

        if solver.SIGNAL in output:
            w += 1
        else:
            print "differential found. weight: {}".format( w ),
            v = []
            if solver_t in ['boolector','stp']:
                differential = solver.parse( output )
                x = norx.extract_input( differential )
                z = norx.extract_output( differential )
                v = [ str(w) ] + [ x[key] for key in sorted( x.keys() ) ] + [ str(w) ] + [ z[key] for key in sorted( z.keys() ) ]
            else:
                v = [ str(w), output ]
            solutions.append( v )
            break

    print ''

    return solutions


"""return cvc code only"""
def cvc( solver_t, ws, steps, w_min, w_max, search_t, diag, var_t, var_d ):
    norx = NORX( ws, steps, w_min, search_t, diag )
    return norx()

