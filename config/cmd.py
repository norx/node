"""
    config.py
    ---------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE

"""

import db

# solver_t, ws, steps, w_min, w_max, search_t, diag, var_t, var_d

basic = {
     "std32": [       "stp", 32, 3,   1,  30,    "full", False,         None,          [] ],
   "initN32": [ "boolector", 32, 2,  58,  70,  "init_N", False,         None,          [] ],
  "initNK32": [       "stp", 32, 2,   1,  30, "init_NK", False,         None,          [] ],
    "rate32": [       "stp", 32, 2,   1,  30,    "rate", False,         None,          [] ],
     "col32": [ "boolector", 32, 2,   1, 256,    "full", False,        "input", db.d32[0] ],
    "iter32": [ "boolector", 32, 2, 512, 512,    "full", False, "input=output",        [] ],
     "fwd32": [ "boolector", 32, 1,   1, 256,   "full",   True,        "input", db.d32[5] ],
     "bwd32": [ "boolector", 32, 1,   1, 256,   "full",  False,       "output", db.d32[8] ],
    "1bit32": [ "boolector", 32, 2,   1, 256,   "full",  False,        "input", db.d32[1] ],

     "std64": [       "stp", 64, 3,   1,  30,    "full", False,         None,          [] ],
   "initN64": [       "stp", 64, 1,   1,  30,  "init_N", False,         None,          [] ],
  "initNK64": [       "stp", 64, 2,   1,  30, "init_NK", False,         None,          [] ],
    "rate64": [       "stp", 64, 2,   1,  30,    "rate", False,         None,          [] ],
     "col64": [ "boolector", 64, 2,   1, 256,    "full", False,        "input", db.d64[0] ],
    "iter64": [ "boolector", 64, 2, 843, 843,    "full", False, "input=output",        [] ],
    "1bit64": [ "boolector", 64, 2,   1, 256,   "full",  False,        "input", db.d64[2] ],

    "test64": [       "stp", 64, 1,   0,   0,    "full", False,         None,          [] ],
}

# enumerates all differentials for a given number of steps and weight
enum = {
    "enum32": [ "boolector", 32, 3, 12, 0, "full", False ],
    "enum64": [ "boolector", 64, 3, 12, 0, "full", False ],
}

bit = {
    "bit32": [ "boolector", 32, 2, 1, 80, "init_N", False ],
    "bit64": [ "boolector", 64, 2, 1, 80, "full", False ],
}

