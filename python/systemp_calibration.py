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

import numpy as np
from datetime import datetime
import time
import h5py
from gnuradio import gr

class systemp_calibration(gr.sync_block):
    """
    systemp_calibration - takes input from a spectrometer.
        In:  Data stream of spectra
        Several vectors are output:
        out0: Latest Spectrum - either raw or with calibration, depending on user's choice.
        out1: Gain - updated whenever "hot" or "cold" calibrations are done.
        out2: System Temperature - updated whenever "hot" or "cold" calibrations are done.
    
    Parameters:
    (1) vec_length - vector length in channels
    (2) collect - controlled by a Chooser block, which needs 4 options with the variables: nocal (= raw spectrum), cal (= spectrum with calibrations), hot (= hot calibration), cold (= cold calibration)
    (3) samp_rate - used to calculate frequency values for spectrum output; set in a Variable box.
    (4) freq - center frequency used to calculate frequency values for spectrum output; set in a Variable box.
    (5) prefix - used in the filename to describe the pathlength; set in a Variable box. 
    (6) spectrumcapture_toggle - determines whether the spectrum is captured to a file written to the pathlength described by the prefix variable, and written with the filename = prefix + timenow + "_spectrum.csv".
    """
    def __init__(self, vec_length, collect, samp_rate, freq, prefix, spectrumcapture_toggle):
        gr.sync_block.__init__(self,
            name="systemp_calibration",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=3*[(np.float32, int(vec_length))])
        
        self.vec_length = int(vec_length)
        self.collect = collect
        self.spectrumcapture_toggle = False
        self.samp_rate = samp_rate
        self.freq = freq
        self.prefix = prefix

         # Define vectors and constants:
        self.spectrum = np.zeros(vec_length)
        self.hot = 2*np.ones(vec_length)   
        self.cold = 1*np.ones(vec_length)
        self.gain = np.ones(vec_length)
        self.tsys = 50*np.ones(vec_length)
        self.thot = 300
        self.tcold = 10
        self.frequencies = np.arange(freq - samp_rate/2, freq + samp_rate/2, samp_rate/vec_length)
        self.data_array = np.zeros((vec_length,2))
    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        out2 = output_items[2]

         # Check if the "collect" Chooser is changed. If "hot" or "cold" are selected, the gain and tsys are updated.
        
        if self.collect == "cal":
            out0[:] = in0/(self.gain) - self.tsys
        elif self.collect == "hot":
            out0[:] = in0
            self.hot[:] = in0
            self.y = self.hot/self.cold
            self.y[self.y == 1] = 2
            self.tsys = (self.thot - self.y*self.tcold)/(self.y-1)
            self.gain = self.cold/(self.tcold + self.tsys)
            self.gain[self.gain <= 0] = 1
            
        elif self.collect == "cold":
            out0[:] = in0
            self.cold[:] = in0
            self.y = self.hot/self.cold
            self.y[self.y == 1] = 2
            self.tsys = (self.thot - self.y*self.tcold)/(self.y-1)
            self.gain = self.cold/(self.tcold + self.tsys)
            self.gain[self.gain <= 0] = 1
        else:
            out0[:] = in0 
        float
        out1[:] = self.gain
        out2[:] = self.tsys

        if self.spectrumcapture_toggle == True:
            current_time = time.time()
            self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            #write (freq, output) in a column to a text file, titled e. "2018-07-24_15.15.49_spectrum.txt"
            self.textfilename = self.prefix + self.timenow + "_spectrum.csv"
            self.data_array[:,0] = self.frequencies
            self.data_array[:,1] = self.spectrum
            np.savetxt(self.textfilename, self.data_array, delimiter=',')
            self.spectrumcapture_toggle = False
        
        self.spectrum[:] = out0

        return len(output_items[0])
    
    #Check if collect Chooser block is changed.
    def set_parameters(self, collect, spectrumcapture_toggle):
        self.collect = collect
        if self.spectrumcapture_toggle == False:
            self.spectrumcapture_toggle = True
