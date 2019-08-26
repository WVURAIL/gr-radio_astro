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
import time
try:
    import h5py
except:
    print "Python package:"
    print "   h5py"
    print "Not found.  If needed, at the command line type:"
    print "sudo apt install python-h5py"
    print "or"
    print "pip install h5py"
    print "However we dom't recommend installing python packages using pip"
    print "Use your OS local package manager used to install gnuradio to"
    print "maintain consistent python environments"
    print ""
    
class hdf5_sink(gr.sync_block):
    """
    docstring for block hdf5_sink
    Writing to the file is controlled by the string variable save_toggle: if save_toggle = "True" (a string, not boolean), the data is written to the file; otherwise writing to the file stops.
    """
    def __init__(self, intype, n_inputs, vec_length, save_toggle, fname='default.h5', pointing = "AZ,EL", freq_start=1419.0, freq_step=0.002, notes = 'default' ):
        current_time = time.time()
        if intype == complex:
            datatype = np.complex64
        elif intype == float:
            datatype = np.float32
        elif intype == int:
            datatype = np.int32
        else:
            raise
        gr.sync_block.__init__(self,
            name="hdf5_sink",
            in_sig=n_inputs*[(datatype, vec_length)],
            out_sig=None)
        print(intype)
        self.h5 = h5py.File(fname, 'w')
        self.h5.attrs["file_name"] = fname
        self.h5.attrs["notes"] = notes
        self.h5.attrs["start_time"] = current_time
        self.h5.attrs["pointing"] = pointing
        self.h5.attrs['freq_start'] = freq_start
        self.h5.attrs["freq_step"] = freq_step
        self.save_toggle = save_toggle
        self.timeDataset = self.h5.create_dataset('timestamp', (1,1), dtype=np.float64, maxshape=(None,1))
        self.inputDataset = self.h5.create_dataset('input', (1,1), dtype=np.float64, maxshape=(None,1))
        self.spectrumDataset = self.h5.create_dataset('spectrum', (1,vec_length), dtype=datatype, maxshape=(None,vec_length))
        self.n_times = 1
        self.n = 0
        self.vec_size = vec_length
        self.n_inputs = n_inputs



    def work(self, input_items, output_items):
        #makes a kind of 'flat' file instead of a matrix for inputs.  
        #all inputs must be same datatype.
        current_time = time.time()
        if self.save_toggle == "True":
            for in_num, in0 in enumerate(input_items):
                #in0 = input_items[0]
                #oversized = in0.size/self.vec_size
                #print(in0.shape)
                ### Seems can actually get a bunch of vectors as the input piled up.
                #this doesn't seem to break if only have one.
                for inp0 in in0:
                    if self.n == self.n_times:
                        self.n_times = self.n+1
                        self.timeDataset.resize((self.n_times,1))
                        self.inputDataset.resize((self.n_times, 1))
                        self.spectrumDataset.resize((self.n_times,self.vec_size))
                    else:
                        pass
                    print( self.n_times) #debugging.  remove
                    self.timeDataset[self.n] = current_time
                    self.inputDataset[self.n] = in_num
                    self.spectrumDataset[self.n] = inp0
                    self.n += 1
        
        return len(input_items[0])

    def set_save_toggle(self, save_toggle):
        self.save_toggle = save_toggle

