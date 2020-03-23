"""
Vector Average for radio astronomy
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Quiet Skies LLC
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

class ra_vave(gr.decim_block):
    """
    Vector Average with Decimation.   Only one vector is returned for N input.
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, vlen, vdecimate):
        gr.decim_block.__init__(self,
                                name="ra_vave",
                                in_sig=[(numpy.float32, int(vlen))],   # in 1 spectrum
                                out_sig=[(numpy.float32, int(vlen))],  # out 1 spectrum
                                decim=int(vdecimate))
        self.vlen = int(vlen)
        self.vdecimate = int(vdecimate)
        self.set_decimate(vdecimate)
        self.sum = numpy.zeros(self.vlen)
        self.count = 0

    def forecast(self, noutput_items, ninput_items):
        """
        Indicate the number of inputs required to get 1 output spectrum
        """
        if noutput_items is None:
            return self.vdecimate
        for i in range(len(noutput_items)):
            ninput_items[i] = noutput_items[i]*self.vdecimate
        return ninput_items

    def work(self, input_items, output_items):
        """
        Work averages all input vectors and outputs one vector for each N inputs
        """
        inn = input_items[0]

        # get the number of input vectors
        nv = len(inn)          # number of vectors in this port
        ini = inn[0]           # first input vector
        li = len(ini)          # length of first input vector
        ncp = min(li, self.vlen)  # don't copy more required (not used)

        noutports = len(output_items)
        if noutports != 1:
            print('!!!!!!! Unexpected number of output ports: ', noutports)
        out = output_items[0]  # all vectors in PORT 0

        iout = 0 # count the number of output vectors
        for i in range(nv):
            # get the length of one input
            ini = inn[i]
            # now save this vector until all are received
            if self.count == 0:
                self.sum[0:ncp] = ini[0:ncp]
            else:
                self.sum[0:ncp] = self.sum[0:ncp] + ini[0:ncp]
            self.count = self.count + 1

            # indicate consumption of a vector from input

            if self.count >= self.vdecimate:
                # normalize output average
                self.sum = self.oneovern * self.sum
                outi = out[iout]  # get pointer to ith output
                outi = self.sum   # copy vector to output
                out[iout] = outi  # put a vector in list
                iout = iout+1     # move to next item in list
                # now reset the count and restart the sum
                self.count = 0
        # end for all input vectors
        output_items[0] = out  # put all vectors in output port 0
#        print 'N outputs: ', len(output_items[0]), iout
        return len(output_items[0])
    # end vave()

#   callback function for grc, to update the decimate
    def set_decimate(self, decimate):
        """
        set_decimate updates the average and decimate count
        This should update the time the block takes to complete and
        the Signal to Noise ratio of the sum.
        """
        self.vdecimate = max(1, int(decimate))
        self.oneovern = 1./float(self.vdecimate)
        print("V_ave decimate   : %d" % (self.vdecimate))
