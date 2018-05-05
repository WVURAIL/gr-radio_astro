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
from gnuradio import gr

class ra_vmedian(gr.decim_block):
    """
    Vector Median with Decimation.   Only one vector is returned for N input.
    The highest and lowest values in each channel are discard and the remainder averaged.
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, vlen, vdecimate):
        gr.decim_block.__init__(self,
            name="vmedian",
            in_sig=[(numpy.float32, int(vlen))],
            out_sig=[(numpy.float32, int(vlen))], 
            decim=int(vdecimate))
        self.vlen = int(vlen)
        self.vdecimate = int(vdecimate)
        self.vsum = numpy.zeros(self.vlen)
        self.vmin = numpy.zeros(self.vlen)
        self.vmax = numpy.zeros(self.vlen)
        self.count = 0
        if self.vdecimate < 3:
            print 'Vector Median, not enough inputs: ',self.vdecimate, ' Using 3'
            self.vdecimate = 3
        self.set_decimate( self.vdecimate)

    def forecast( self, noutput_items, ninput_items):
        if noutput_items == None:
            return self.vdecimate
        for i in range(len(nout_items)):
            ninput_items[i] = noutput_items[i]*self.vdecimate
        return ninput_items
    
    def work(self, input_items, output_items):
        """
        Work averages all input vectors and outputs one vector for each N inputs
        """
        inn = input_items[0]
        
        # get the number of input vectors
        n = len( input_items)  # number of input PORTS (only 1)
        nv = len(inn)          # number of vectors in this port
        ini = inn[0]           # first input vector
        li = len(ini)          # length of first input vector
        ncp = min( li, self.vlen) # get length to copy

        noutports = len( output_items)
        if noutports != 1:
            print '!!!!!!! Unexpected number of output ports: ', noutports
        out = output_items[0]  # all vectors in PORT 0 
        nout = len(out)        # number of output vectors
        out0 = out[0]          # get the first output vector
        lo = len(out0)         # length of 1st output vector
#        print 'Number work outputs: ', nout,' Length: ',lo

        iout = 0 # count the number of output vectors
        for i in range(nv):
            # get the length of one input
            ini = inn[i]

            # now save this vector until all are received
            if self.count == 0:
                # if first vector, averge, min and max are all the same.
                self.vsum[0:ncp] = ini[0:ncp]
                self.vmin[0:ncp] = ini[0:ncp]
                self.vmax[0:ncp] = ini[0:ncp]
            else:
                self.vsum[0:ncp] = self.vsum[0:ncp] + ini[0:ncp]
                self.vmin = numpy.minimum( self.vmin, ini)
                self.vmax = numpy.maximum( self.vmax, ini)
            self.count = self.count + 1

            # if time to mornalize sum and output
            if self.count >= self.vdecimate:
                # normalize output average removing min and max
                self.vsum = self.vsum - (self.vmin + self.vmax)
                self.vsum = self.oneovern * self.vsum
                outi = out[iout]  # get pointer to ith output
                outi = self.vsum  # copy vector to output
                out[iout] = outi  # put a vector in list
                iout = iout+1     # move to next item in list
                # now reset the count and restart the sum
                self.count = 0
        # end for all input vectors
        output_items[0] = out  # put all vectors in output port 0
        return len(output_items[0])
    # end vmedian()

    def set_decimate( self, decimate):
        """
        set_decimate updates the average and decimate count
        This should update the time the block takes to complete and
        the Signal to Noise ratio of the sum.
        """
        self.vdecimate = max( 3, int( decimate))
        self.oneovern = 1./(float(self.vdecimate)-2.)
        print "V_median decimate: %d" % (self.vdecimate)
