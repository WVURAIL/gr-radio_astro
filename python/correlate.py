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

class correlate(gr.sync_block):
    """
    docstring for block correlate
    """
    def __init__(self, n_inputs, vec_length):
        gr.sync_block.__init__(self,
            name="correlate",
            in_sig=n_inputs*[(np.complex64, vec_length)],
            out_sig=[(np.complex64, vec_length*(n_inputs+1)*n_inputs/2)])
        self.n_inputs = n_inputs
        self.vec_length = vec_length


    def work(self, input_items, output_items):
        out = output_items[0]
        in1_indices, in2_indices =  np.triu_indices(self.n_inputs)
        out_size = in1_indices.size
        out_arr = np.zeros((out_size, self.vec_length), dtype=np.complex64)
        for i in range(in1_indices.size):
            #print(input_items[in1_indices[i]][0].shape)
            #print(input_items[in1_indices[i]][0].dtype)
            #print(input_items[in1_indices[i]][0,1], input_items[in1_indices[i]][1,1])
            out_arr[i] = input_items[in1_indices[i]][0]*input_items[in2_indices[i]][0].conjugate()
            print(out_arr[i][4])
        out[:] = out_arr.flatten()
        return len(output_items[0])

