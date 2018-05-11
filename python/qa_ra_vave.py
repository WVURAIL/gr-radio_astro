#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from ra_vave import ra_vave

class qa_vave (gr_unittest.TestCase):
    """
    qa_vave is a Gnuradio Companion diagnostic block to confirm proper operation of
    the vector average block vave
    Glen Langston, 2018 April 19
    """
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        vsize = 1024
        vdecimate = 4
        vin = numpy.zeros(2*vsize*vdecimate)
        for i in range(vsize):
            vin[i] = float(i)
            vin[(vsize*vdecimate)+i] = vin[i]
        # create a set of vectors
        src = blocks.vector_source_f( vin.tolist())
        s2v = blocks.stream_to_vector(gr.sizeof_float, vsize)
        # block we're testing
        vblock = ra_vave( vsize, vdecimate)

#        print 'Vblock: ',dir(vblock)
        vblock.set_decimate( vdecimate)

        v2s = blocks.vector_to_stream( gr.sizeof_float, vsize)
        snk = blocks.vector_sink_f(vsize)

        self.tb.connect (src, s2v)
        self.tb.connect (s2v, vblock)
        self.tb.connect (vblock, snk)
#        self.tb.connect (v2s, snk)
        expected = vin[0:(2*vsize)]/4.
        expected[vsize:] = expected[0:vsize]
        print 'Expected: ', expected[0:7]
        outdata = None
        waittime = 0.01

        self.tb.run ()
        outdata = snk.data()
        print 'Output: ', outdata[0:7]
        # check data
        self.assertFloatTuplesAlmostEqual (expected, outdata, 6)

if __name__ == '__main__':
    gr_unittest.run(qa_vave, "qa_vave.xml")
