#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
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

class chart_recorder(gr.sync_block):
    """
    input is integrated data to be added to the output chart recorder array:
        out = array[0,0,0, 0, ... 0, -3 = non-zero value, -2 = non-zero value, -1 = new value input]
    """
    def __init__(self, vec_length):
        gr.sync_block.__init__(self,
            name="chart_recorder",
            in_sig=[numpy.float32],
            out_sig=[(np.float32, int(vec_length))])

        # Define vectors and constants:
        self.vec_length = vec_length
        self.output_array = np.zeros(self.vec_length)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        self.output_array[:-1] = output_array[1:]

        self.output_array[-1] = in0

        out[:] = self.output_array.copy()

        return len(output_items[0])
