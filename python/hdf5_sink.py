#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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
import h5py
import time

class hdf5_sink(gr.sync_block):
    """
    docstring for block hdf5_sink
    """
    def __init__(self, vec_length, fname='default.h5', pointing = "AZ,EL", freq_start=1419.0, freq_step=0.002 , notes = 'default' ):
        current_time = time.time()
        gr.sync_block.__init__(self,
            name="hdf5_sink",
            in_sig=[(np.complex64, vec_length)],
            out_sig=None)
        self.h5 = h5py.File(fname, 'w')
        self.h5.attrs["file_name"] = fname
        self.h5.attrs["notes"] = notes
        self.h5.attrs["start_time"] = current_time
        self.h5.attrs["pointing"] = pointing
        self.h5.attrs['freq_start'] = freq_start
        self.h5.attrs["freq_step"] = freq_step
        self.timeDataset = self.h5.create_dataset('timestamp', (1,1), dtype=np.float64, maxshape=(None,1))
        self.spectrumDataset = self.h5.create_dataset('spectrum', (1,vec_length), dtype=np.complex64, maxshape=(None,vec_length))
        self.n_times = 1
        self.n = 0
        self.vec_size = vec_length



    def work(self, input_items, output_items):
        in0 = input_items[0]
        current_time = time.time()
        #oversized = in0.size/self.vec_size
        #print(in0.shape)
        ### Seems can actually get a bunch of vectors as the input piled up.
        #this doesn't seem to break if only have one.
        for inp0 in in0:
            if self.n == self.n_times:
                self.n_times = self.n+1
                self.timeDataset.resize((self.n_times,1))
                self.spectrumDataset.resize((self.n_times,self.vec_size))
            else:
                pass
            print( self.n_times) #debugging.  remove
            self.timeDataset[self.n] = current_time
            self.spectrumDataset[self.n] = inp0
            self.n += 1
        return len(input_items[0])

