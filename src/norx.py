"""
    norx.py - STP code generator for differential search in the NORX permutation.
    ------

    This file is part of NODE - the NORX Differential-Search Engine.

    :copyright: (c) 2014 Philipp Jovanovic <philipp@jovanovic.io>
    :license: BSD (3-Clause), see LICENSE
"""

import math

class NORX:

    """ hamming weight constants """
    HWC = { 32: ('0x55555555',
                 '0x33333333',
                 '0x0f0f0f0f',
                 '0x00ff00ff',
                 '0x0000ffff'),

            64: ('0x5555555555555555',
                 '0x3333333333333333',
                 '0x0f0f0f0f0f0f0f0f',
                 '0x00ff00ff00ff00ff',
                 '0x0000ffff0000ffff',
                 '0x00000000ffffffff') }

    """ rotation constants """
    ROT = { 32: (8,11,16,31), 64: (8,19,40,63) }

    """ search types """
    SEARCH_T = { 'init_N':  [0,3,4,5,6,7,8,9,10,11,12,13,14,15],
                 'init_NK': [0,3,8,9,10,11,12,13,14,15],
                 'rate':    [10,11,12,13,14,15],
                 'full':    [] }

    def __init__( self, w, steps, dp, st, start_diag = False ):
        self.w = w
        self.wlog2 = int( math.log( w, 2 ) )
        self.dp = dp
        self.steps = steps
        self.variables = {} # key: (name,id); elements: list of all variables with name and id-nr
        self.stp_variables = self.init_stp_variables()
        self.stp_hw = self.init_stp_hw()
        self.stp_code = self.init_stp_code( start_diag )
        self.stp_exclude = self.init_stp_exclude()
        self.stp_search_type = self.init_stp_search_type( st )
        self.set_variables = {
            'input': self.set_input_vars,
            'output': self.set_output_vars,
            'input=output': self.set_input_vars_to_output_vars
        }

    def __call__( self ):
        return self.stp_variables + '\n' + \
               self.stp_hw + '\n' + \
               self.stp_code + '\n' + \
               self.stp_exclude + '\n' + \
               'QUERY(FALSE);\nCOUNTEREXAMPLE;'

    def init_stp_variables( self ):
        s = ''
        s += '% step variables\n'
        s += self.init_vars( 'x', 0, 0, 16 ) # input variables
        s += ''.join( [ self.init_vars( 'y', i, 0, 16 ) for i in xrange( 2 * self.steps - 1 ) ] ) # internal variables
        s += self.init_vars( 'z', 0, 0, 16 ) # output variables
        s += '\n% helper variables for computation of differential probabilities\n'
        s += ''.join( [ self.init_vars( 'w', i, 0, 16 ) for i in xrange( self.steps ) ] )
        s += '\n% variable for differential probability\n'
        s += 'dp : BITVECTOR({:d});\n'.format( self.w )
        return s

    def init_stp_hw( self ):
        m = [ 'm{:02d}'.format(2**(i)) for i in xrange( self.wlog2 ) ]
        s = ''
        s += '% helper variables for hamming weight computation \n'
        s += ', '.join( m )
        s += ' : BITVECTOR({:s});\n\n'.format(  str(self.w) )
        s += ''.join( [ self.init_vars( 'h', i, 0, self.wlog2 ) for i in xrange( self.steps * 16 ) ] )
        s += '\n'
        s += ''.join( [ 'ASSERT( {} = {} );\n'.format( x,y ) for x,y in zip( m, self.HWC[ self.w ] ) ] )
        return s

    def init_stp_code( self, start_diag ):
        s = ''
        x = [ self.get_vars( 'x', 0 ) ]
        y = [ self.get_vars( 'y', i ) for i in xrange( 2 * self.steps - 1 ) ]
        z = [ self.get_vars( 'z', 0 ) ]
        w = [ self.get_vars( 'w', i ) for i in xrange( self.steps ) ]
        h = [ self.get_vars( 'h', i, xrange( self.wlog2 ) ) for i in xrange( self.steps * 16 ) ]
        v = x + y + z
        do_step = [ self.column_step, self.diag_step ]
        if start_diag:
            do_step = [ self.diag_step, self.column_step ]
        j = 0
        for i in xrange(0,len(v)-2,2):
            s += do_step[ j%2 ]( v[i], v[i+1], v[i+2], w[j] )
            j += 1
        s += self.hamming_weight( w, h )
        return s

    def init_stp_search_type( self, t ):
        #T = { 'init_N': [0,3] + range(4,16), 'init_NK': [0,3] + range(8,16), 'rate': range(10,16), 'full': [] }
        assert t in self.SEARCH_T.keys()
        if t != 'full':
            self.set_vars( 'x', 0, [ '0x' + '0' * ( self.w/4 ) for _ in xrange( len( self.SEARCH_T[t] ) ) ], self.SEARCH_T[t] )
        return t

    def init_stp_exclude( self ):
       # no all-zero input difference
       s = ' AND\n '.join( [ '({} = 0x{})'.format( x, '0' * ( self.w/4 ) ) for x in self.get_vars( "x", 0 ) ] )
       return 'ASSERT( NOT (\n({:s})\n));\n'.format(s)

    def init_vars( self, name, r = 0, m = 0, n = 0 ):
        assert m <= n
        v = [ name + '{:02d}{:02d}'.format( r,i ) for i in xrange( m,n ) ]
        self.variables[ (name,r) ] = v
        return '{:s} : BITVECTOR({:s});\n'.format( ', '.join(v), str(self.w) )

    def get_vars( self, name, r = 0, indices = xrange(16) ):
        v = self.variables[ (name,r) ]
        return [ v[i] for i in indices ]

    def set_vars( self, name, r, val, indices = xrange(16) ):
        v = self.get_vars( name, r, indices )
        s = ' AND\n '.join( [ '({} = {})'.format( x,y ) for x,y in zip( v, val ) ] )
        self.stp_exclude += 'ASSERT( \n({:s})\n);\n'.format(s)

    def set_input_vars( self, val, indices = xrange(16) ):
        self.set_vars( 'x', 0, val, indices )

    def set_output_vars( self, val, indices = xrange(16) ):
        self.set_vars( 'z', 0, val, indices )

    def set_input_vars_to_output_vars( self, val ):
        self.set_vars( 'x', 0, self.get_vars( 'z' ) ) # for iterative differentials

    def H( self, a, b, c, p = None ):
        assert p != None
        s = ''
        # a ^ b ^ c = (a ^ b ^ c) & ( (a | b) <<1 )
        s += 'ASSERT( ( BVXOR( BVXOR( {:s},{:s} ), {:s} ) ) = ( BVXOR( BVXOR( {:s},{:s} ), {:s} ) & ( ( ( {:s} | {:s} ) << 1)[{:s}:0] ) ) );\n'.format( a, b, c, a, b, c, a, b, str(self.w-1) )
        # p = (a | b) <<1 (helper variable for weight calculation)
        s += 'ASSERT( {:s} = ( ( ( {:s} | {:s} ) << 1)[{:s}:0] ) );\n'.format( p, a, b, str(self.w-1) )
        return s

    def XOR_ROTR( self, a, b, c, r ):
        # c = (a^b)>>>r
        return 'ASSERT( {:s} = ( BVXOR( {:s}, {:s} ) >> {:s} ) | ( ( BVXOR( {:s}, {:s} ) << {:s} )[{:s}:0] ) );\n\n'.format( c, a, b, str(r), a, b, str(self.w-r), str(self.w-1) )

    def G( self, a, b, c, p ):
        assert len(a) == len(b) == len(c) == 4
        s = ''
        s += self.H( a[0], a[1], b[0], p[0] ); s+= self.XOR_ROTR( a[3], b[0], b[3], self.ROT[self.w][0] )
        s += self.H( a[2], b[3], b[2], p[1] ); s+= self.XOR_ROTR( a[1], b[2], b[1], self.ROT[self.w][1] )
        s += self.H( b[0], b[1], c[0], p[2] ); s+= self.XOR_ROTR( b[3], c[0], c[3], self.ROT[self.w][2] )
        s += self.H( b[2], c[3], c[2], p[3] ); s+= self.XOR_ROTR( b[1], c[2], c[1], self.ROT[self.w][3] )
        return s

    def column_step( self, a, b, c, p ):
        assert len(a) == len(b) == len(c) == len(p) == 16
        s = '% Column step\n'
        s += self.G( [ a[ 0], a[ 4], a[ 8], a[12] ], [ b[ 0], b[ 4], b[ 8], b[12] ], [ c[ 0], c[ 4], c[ 8], c[12] ], [ p[ 0], p[ 4], p[ 8], p[12] ] )
        s += self.G( [ a[ 1], a[ 5], a[ 9], a[13] ], [ b[ 1], b[ 5], b[ 9], b[13] ], [ c[ 1], c[ 5], c[ 9], c[13] ], [ p[ 1], p[ 5], p[ 9], p[13] ] )
        s += self.G( [ a[ 2], a[ 6], a[10], a[14] ], [ b[ 2], b[ 6], b[10], b[14] ], [ c[ 2], c[ 6], c[10], c[14] ], [ p[ 2], p[ 6], p[10], p[14] ] )
        s += self.G( [ a[ 3], a[ 7], a[11], a[15] ], [ b[ 3], b[ 7], b[11], b[15] ], [ c[ 3], c[ 7], c[11], c[15] ], [ p[ 3], p[ 7], p[11], p[15] ] )
        s += '\n'
        return s

    def diag_step( self, a, b, c, p ):
        assert len(a) == len(b) == len(c) == len(p) == 16
        s = '% Diagonal step\n'
        s += self.G( [ a[ 0], a[ 5], a[10], a[15] ], [ b[ 0], b[ 5], b[10], b[15] ], [ c[ 0], c[ 5], c[10], c[15] ],[ p[ 0], p[ 5], p[10], p[15] ] )
        s += self.G( [ a[ 1], a[ 6], a[11], a[12] ], [ b[ 1], b[ 6], b[11], b[12] ], [ c[ 1], c[ 6], c[11], c[12] ],[ p[ 1], p[ 6], p[11], p[12] ] )
        s += self.G( [ a[ 2], a[ 7], a[ 8], a[13] ], [ b[ 2], b[ 7], b[ 8], b[13] ], [ c[ 2], c[ 7], c[ 8], c[13] ],[ p[ 2], p[ 7], p[ 8], p[13] ] )
        s += self.G( [ a[ 3], a[ 4], a[ 9], a[14] ], [ b[ 3], b[ 4], b[ 9], b[14] ], [ c[ 3], c[ 4], c[ 9], c[14] ],[ p[ 3], p[ 4], p[ 9], p[14] ] )
        s += '\n'
        return s

    def hamming_weight( self, w, h ):
        s = '% hamming weight computation\n'
        s += ''.join( [ self.hw( x,y ) for x,y in zip( sum( w,[] ), h ) ] )
        t = ', '.join( [ '{:s}'.format( u[-1] ) for u in h ] )
        s += 'ASSERT( dp = ( BVPLUS( {:d}, {:s} ) ) );\n\n'.format( self.w, t )
        s += 'ASSERT( dp = 0x{:s} );\n'.format( hex( self.dp )[2:].zfill( self.w / 4 ) )
        return s

    def hw( self, w, h ):
        s = ''
        if self.w == 32:
          s += 'ASSERT( {:s} = BVPLUS(32, ( {:s} & m01 ), ( ( ( {:s} >>  1)[31:0] ) & m01 ) ) );\n'.format( h[0], w, w )
          s += 'ASSERT( {:s} = BVPLUS(32, ( {:s} & m02 ), ( ( ( {:s} >>  2)[31:0] ) & m02 ) ) );\n'.format( h[1], h[0], h[0] )
          s += 'ASSERT( {:s} = BVPLUS(32, ( {:s} & m04 ), ( ( ( {:s} >>  4)[31:0] ) & m04 ) ) );\n'.format( h[2], h[1], h[1] )
          s += 'ASSERT( {:s} = BVPLUS(32, ( {:s} & m08 ), ( ( ( {:s} >>  8)[31:0] ) & m08 ) ) );\n'.format( h[3], h[2], h[2] )
          s += 'ASSERT( {:s} = BVPLUS(32, ( {:s} & m16 ), ( ( ( {:s} >> 16)[31:0] ) & m16 ) ) );\n'.format( h[4], h[3], h[3] )
          s += '\n'
        elif self.w == 64:
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m01 ), ( ( ( {:s} >>  1)[63:0] ) & m01 ) ) );\n'.format( h[0], w, w )
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m02 ), ( ( ( {:s} >>  2)[63:0] ) & m02 ) ) );\n'.format( h[1], h[0], h[0] )
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m04 ), ( ( ( {:s} >>  4)[63:0] ) & m04 ) ) );\n'.format( h[2], h[1], h[1] )
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m08 ), ( ( ( {:s} >>  8)[63:0] ) & m08 ) ) );\n'.format( h[3], h[2], h[2] )
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m16 ), ( ( ( {:s} >> 16)[63:0] ) & m16 ) ) );\n'.format( h[4], h[3], h[3] )
          s += 'ASSERT( {:s} = BVPLUS(64, ( {:s} & m32 ), ( ( ( {:s} >> 32)[63:0] ) & m32 ) ) );\n'.format( h[5], h[4], h[4] )
          s += '\n'
        return s

    """ extract differences of a differential ( see stp.py parse() ) """
    def extract( self, var, r, differential ):
        v = self.get_vars( var, r )
        try:
            return { key : differential[key] for key in v }
        except KeyError:
            print "Differential {}".format( differential )

    def extract_input( self, differential ):
        return self.extract( 'x', 0, differential )

    def extract_output( self, differential ):
        return self.extract( 'z', 0, differential )

    """ x: input difference, z: output difference """
    def exclude( self, x = {}, z = {}, r = False ):
        s = ''
        if x != {}:
            s += ' AND\n '.join( [ '({:s} = {:s})'.format( key, x[key] ) for key in sorted(x) ] )
        if z != {}:
            if x != {}:
                s += ' AND\n '
            s += ' AND\n '.join( [ '({:s} = {:s})'.format( key, z[key] ) for key in sorted(z) ] )
        if not r:
            self.stp_exclude += 'ASSERT( NOT (\n {:s}\n));\n'.format( s )
        else:
            return 'ASSERT( NOT (\n {:s}\n));\n'.format( s )
