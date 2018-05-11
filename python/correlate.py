#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Kevin Bandura.
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

import numpy as np
from gnuradio import gr
#from numba import jit
#import time

#@jit
def _corr(in_dat, out_size, vec_length, in1_indices, in2_indices ):
    out_arr = np.zeros((out_size, vec_length), dtype=np.complex64)
    for i in range(in1_indices.size):
        out_arr[i] = in_dat[in1_indices[i]][0]*in_dat[in2_indices[i]][0].conjugate()
    return out_arr

class correlate(gr.sync_block):
    """
    takes n vector inputs and correlates all pairs of products producing a 'matrix'
    of size (n(n+1)/2, vector_length) on the output.  Output pairs are ordered top to bottom, (0,0), (0,1), 
    (0,2),...(1,1), (1,2)...(n-1,n-1).  
    """
    def __init__(self, n_inputs, vec_length):
        gr.sync_block.__init__(self,
            name="correlate",
            in_sig=n_inputs*[(np.complex64, vec_length)],
            out_sig=[(np.complex64, vec_length*(n_inputs+1)*n_inputs/2)])
        self.n_inputs = n_inputs
        self.vec_length = vec_length
        self.in1_indices, self.in2_indices =  np.triu_indices(n_inputs)
        self.out_size = self.in1_indices.size



    def work(self, input_items, output_items):
        out = output_items[0]
        #current_time = time.time()
        out_arr = _corr(input_items, self.out_size, self.vec_length, self.in1_indices, self.in2_indices)
        out[:] = out_arr.flatten()
        #new_time = time.time()
        #time_difference = new_time-current_time
        #print(time_difference)
        return len(output_items[0])

