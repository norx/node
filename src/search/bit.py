
import src.search.basic as basic

def do( solver_t, ws, steps, w_min, w_max, search_t, diag ):

    db = []

    print solver_t, ws, steps, w_min, w_max, search_t, diag

    var_d = [ "0x" + "0"*(ws/4) for _ in xrange(16) ]

    fmt = "{:0"+ str(ws/2) + "X}"

    w_best = w_max
    v_best = None
    nr = 0

    for i in xrange(2*ws-1,-1,-1):
        for j in xrange(i):
            print nr, i, j, "best:", w_best, v_best
            v = fmt.format( (1 << i) + (1 << j) )
            var_d[1] = "0x" + v[:ws/4]
            var_d[2] = "0x" + v[ws/4:]
            r = basic.do( solver_t, ws, steps, w_min, w_best, search_t, diag, "input", var_d )
            if r != [] and int(r[0][0]) < w_best:
                w_best = int(r[0][0])
                v_best = (var_d[1],var_d[2])
            nr += 1
