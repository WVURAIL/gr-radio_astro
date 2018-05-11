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
from ra_ascii_sink import ra_ascii_sink
import radioastronomy

class qa_ascii_sink (gr_unittest.TestCase):
    """
    qa_ascii_sink is a test function to confirm proper operation of
    the radio astronomy data recording block ascii_sink GRC block vmedian
    Glen Langston, 2018 April 19
    """

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        vsize = 2048
        vin = numpy.zeros(vsize)
        for i in range(vsize):
            vin[i] = float(i)
        # create a set of vectors
        src = blocks.vector_source_f( vin.tolist(), False)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vsize)
        # parameters we're setting
        frequency = 1419.5E6
        bandwidth = 6.E6
        azimuth = 179.9
        elevation = 44.9
        observers = "Science Aficionados"
        setupFile = "Watch.not"
        site = "Moumau House"
        device = "rtlsdr,bias=0"
        device = "airspy,pack=1,bias=1"
        obstype = radioastronomy.OBSSURVEY
        record = radioastronomy.INTRECORD
        nmedian = 4**6
        nave = 10
        gain1 = 40.5
        gain2 = 11.0
        gain3 = 11.0
        # block we're testing
        vblock = ascii_sink( setupFile, observers, vsize, frequency, bandwidth, azimuth, elevation, record, 
                             obstype, nmedian, nave, site, device, gain1, gain2, gain3)
        print 'Test init DataDir: ',vblock.obs.datadir

        # skip writing the notes file over and over
        dosave = False
        # now set all parameters
        vblock.set_frequency( frequency, dosave)
        vblock.set_bandwidth( bandwidth, dosave)
        vblock.set_azimuth( azimuth, dosave)
        vblock.set_elevation( elevation, dosave)
        vblock.set_nmedian( nmedian, dosave)
        vblock.set_gain3( gain3, dosave)
        vblock.set_record( record)

        self.tb.connect (src, s2v)
        self.tb.connect (s2v, vblock)
        self.tb.run ()

        vblock.set_record( radioastronomy.INTWAIT)
        self.tb.run()

if __name__ == '__main__':
    gr_unittest.run(qa_ascii_sink, "qa_ascii_sink.xml")
