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
try:
    import h5py
except:
    print "Python package:"
    print "   h5py"
    print "Not found.  If needed, at the command line type:"
    print "pip install h5py"
    print ""
    
from gnuradio import gr

class systemp_calibration(gr.sync_block):
    """
    systemp_calibration - takes input from a spectrometer.
        In:  Data stream of spectra
        Several vectors are output:
        out0: Latest Spectrum - either raw or denoised, with or without calibration, depending on user's choice.
        out1: Gain - updated whenever "hot" or "cold" calibrations are done.
        out2: System Temperature - updated whenever "hot" or "cold" calibrations are done.

    The input signal is denoised using 2 methods:
       1. Noise spikes are removed using a moving median method;
       2. The spectrum is smoothed using a moving average weighted with a Gaussian function about each point.
    
    Once the system temperature is determined as a function of frequency, its final value is taken as the average of the system temperature over the spectrum.
    
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
        self.filtered_out0 = np.ones(vec_length)
        self.filtered_spike = np.ones(vec_length)
        self.hot = 2*np.ones(vec_length)   
        self.cold = 1*np.ones(vec_length)
        self.gain = np.ones(vec_length)
        self.tsys = 50*np.ones(vec_length)
        self.thot = 300
        self.tcold = 10
        self.frequencies = np.zeros(vec_length)
        self.frequencies = np.arange(freq - samp_rate/2, freq + samp_rate/2, samp_rate/vec_length)[:vec_length]
        self.data_array = np.zeros((vec_length,2))
        self.a = np.zeros(self.vec_length)
        self.x = np.zeros(vec_length)

        # To do a gaussian smoothing to the data, assign values to the gaussian kernal.
        # Note: The parameter k defines the size of the window used in smoothing; "fwhm" defines the width of the gaussian fit.
        # For the hot and cold calibrations, the spectrum has no peaks in the region of interest; so set k_cal larger: k = 50.
        # For the data spectrum, set k smaller: k_spec = 8, to preserve the peak features.
        
        self.k_spike = 10       # defines the range of values to take median average over for removing noise spikes
        
        # CALCULATE GAUSSIAN SMOOTHING COEFFICIENTS
        # Each data point will be smoothed by taking an average of +/- k points surrounding the point; the average is a weighted Gaussian average
        #1. HOT & COLD CALIBRATIONS
        # k_cal = +/- 50 points surrounding each point
        # FWHM = 1/4 window width (sigma)
        self.k_cal = 50
        self.fwhm_cal = int(self.k_cal/4)
        self.normal_factor_cal = 1/np.sqrt(2*np.pi*self.fwhm_cal**2)
        self.gx_cal = np.arange(-self.k_cal,self.k_cal+1,1)
        self.gauss_window_cal = self.normal_factor_cal*np.exp(-(self.gx_cal**2)/(2*self.fwhm_cal**2))
        self.gauss_window_cal = self.gauss_window_cal/self.gauss_window_cal.sum()

        #2. SPECTRUM SMOOTHING
        # k_spec = +/- 8 points surrounding each point - a narrower window will not shift the peak positions
        # FWHM = 1/4 window width (sigma)
        self.k_spec = 8
        self.fwhm_spec = int(self.k_spec/4)
        self.normal_factor_spec = 1/np.sqrt(2*np.pi*self.fwhm_spec**2)
        self.gx_spec = np.arange(-self.k_spec,self.k_spec+1,1)
        self.gauss_window_spec = self.normal_factor_spec*np.exp(-(self.gx_spec**2)/(2*self.fwhm_spec**2))
        self.gauss_window_spec = self.gauss_window_spec/self.gauss_window_spec.sum()

    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        # Copy the input data into a simpler array:
        self.a[:] = in0[0,:].copy()
        out0 = output_items[0]
        out1 = output_items[1]
        out2 = output_items[2]

         # Check if the "collect" Chooser is changed. If "hot" or "cold" are selected, the Gain and Tsys are updated.
         # The collect variable is selected in the .grc program, as follows:
         #  "cal" = calibrated spectrum
         #  "hot" = spectrum stored in the hot[] array, used for calculating the gain and Tsys.
         #  "cold" = spectrum stored in the cold[] array, used for calculating the gain and Tsys.
         #  "nocal" = raw spectrum that is smoothed using the spike_smoothing and gauss_smoothing routines
         #  "nocal_nofilter" = raw spectrum
        
        if self.collect == "cal":
            
            self.spike_smoothing()          # This routine removes noise spikes.
            
            self.gauss_smoothing_spec()     # This routine smoothes the data using a Gaussian averaging.

            # The output is calibrated using the gain and Tsys:
            out0[:] = self.filtered_out0/(self.gain) - self.tsys
            self.spectrum[:] = self.filtered_out0/(self.gain) - self.tsys

            # The self.spectrum array is what gets output to the .csv file when the Capture Latest Spectrum button is pressed.

            
        elif self.collect == "hot":
                        
            self.spike_smoothing()          # This routine removes noise spikes.
            
            self.gauss_smoothing_cal()      # This routine smoothes the data using a Gaussian averaging.

            # self.filtered_out0 is the output array resulting from the smoothing routines. This spectrum gets stored in the hot temperature hot[] array.
            self.hot[:] = self.filtered_out0[:]  

            # The displayed output is the filtered, non-calibrated spectrum
            out0[:] = self.filtered_out0
            self.spectrum[:] = self.filtered_out0
            
            # Calculate/update the system gain and temperature arrays.
            self.y = self.hot/self.cold
            self.y[self.y == 1] = 2
            self.tsys = (self.thot - self.y*self.tcold)/(self.y-1)
            self.gain = self.cold/(self.tcold + self.tsys)
            self.gain[self.gain <= 0] = 1
            tm = np.median(self.tsys)
            for i in range(self.vec_length):
                self.tsys[i] = tm
            
        elif self.collect == "cold":

            self.spike_smoothing()          # This routine removes noise spikes.
            
            self.gauss_smoothing_cal()      # This routine smoothes the data using a Gaussian averaging.

            # self.filtered_out0 is the output array resulting from the smoothing routines. This spectrum gets stored in the cold temperature cold[] array.
            self.cold[:] = self.filtered_out0[:]  

            # The displayed output is the filtered, non-calibrated spectrum
            out0[:] = self.filtered_out0
            self.spectrum[:] = self.filtered_out0

            # Calculate/update the system gain and temperature arrays.
 
            self.y = self.hot/self.cold
            self.y[self.y == 1] = 2
            self.tsys = (self.thot - self.y*self.tcold)/(self.y-1)
            self.gain = self.cold/(self.tcold + self.tsys)
            self.gain[self.gain <= 0] = 1
            tm = np.median(self.tsys)
            for i in range(self.vec_length):
                self.tsys[i] = tm

        elif self.collect == "nocal":
            
            self.spike_smoothing()          # This routine removes noise spikes.
                        
            self.gauss_smoothing_spec()     # This routine smoothes the data using a Gaussian averaging.

            # The output is the smoothed data, but not calibrated. self.filtered_out0 is the output array resulting from the smoothing routines.
            out0[:] = self.filtered_out0
            self.spectrum[:] = self.filtered_out0
    
        else:
            out0[:] = in0
            self.spectrum[:] = in0

        out1[:] = self.gain
        out2[:] = self.tsys

        if self.spectrumcapture_toggle == True:     #If true, capture the spectrum to a .csv text file.
            current_time = time.time()
            self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            #write (freq, output) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_spectrum.txt"
            # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
            self.textfilename = self.prefix + self.timenow + "_spectrum.csv"
            self.data_array[:,0] = self.frequencies
            self.data_array[:,1] = self.spectrum
            np.savetxt(self.textfilename, self.data_array, delimiter=',')
            self.spectrumcapture_toggle = False
        
        return len(output_items[0])
    

    #Check if collect Chooser block or spectrumcapture_toggle are changed:

    def set_collect(self, collect):
        self.collect = collect

    def set_spectrumcapture_toggle(self, spectrumcapture_toggle):
        if self.spectrumcapture_toggle == False:
            self.spectrumcapture_toggle = True


    #define SPIKE REMOVAL smoothing function
    def spike_smoothing(self):
        
        # Copy the input data into a simpler array:
        # self.a[:] = self.in0[0,:].copy()

        # Set threshold to 120% of the spectrum average for data in spectrum between 1420.2 MHz and 1420.8 MHz where the HI peaks might appear.
        # Test for data points exceeding the threshhold:   
        self.threshold = 1.2*np.mean(self.a[2541:2786])

            # abovethresh_index = array of indices of data that spike above the threshold
            # Find data points above threshold
            # np.where is a tuple with 2 elements; 
            #       the np.where[0] element of this tuple is an array of the indices satisfying the condition. sfs
            
        self.abovethresh_index = np.asarray(np.where(self.a >self.threshold)[0])
            # Remove any nan's from this array:
        self.abovethresh_index = self.abovethresh_index[~np.isnan(np.asarray(np.where(self.a >self.threshold)[0]))]

        # Copy the input array to be manipulated during spike removal:
        self.filtered_spike[:] = self.a[:]           # np.copy(self.in0[0,:])

        for i in range(self.abovethresh_index.shape[0]):
            # lowerbound = max of either 1 or the signal index, whichever is greater,
            # in case the spike is near the beginning of the array and the value 
            # abovethresh-k_spike < 0.
            # Similarly, upperbound defines the maximum index above which theself.tsys = np.mean(self.tsys[self.k_cal:-self.k_cal])re is no data.

            self.lowerbound = max(1, self.abovethresh_index[i] - self.k_spike)
            self.upperbound = min(self.abovethresh_index[i] + self.k_spike, self.vec_length)

            # Replace spikes with median of +/- k_spike surrounding points. For data near edges, the range is reduced to fit array parameters.
            self.filtered_spike[self.abovethresh_index[i]] = np.median(self.a[self.lowerbound:self.upperbound])


    #define GAUSSIAN SMOOTHING functions

    # 1. Smoothing of spectral data. This window covers a narrower range to minimize and artificial shifting of peaks.
    def gauss_smoothing_spec(self):
        # Smooth filtered_spike data array with gaussian average, using the coefficients defined for spectrum data.
        for i in range(self.k_spec, self.vec_length-self.k_spec-1):
            self.filtered_out0[i] = 0
            for j in range(i-self.k_spec, i+self.k_spec+1):
                self.filtered_out0[i] = self.filtered_out0[i] + self.filtered_spike[j]*self.gauss_window_spec[j-i+self.k_spec]

    #2. Smoothing of hot and cold calibration spectra. This window covers a broader range, where we are assuming the hot
    #   and cold spectra are smooth without peaks.
    def gauss_smoothing_cal(self):
        # Smooth filtered_spike data array with gaussian average:
        for i in range(self.k_cal, self.vec_length-self.k_cal-1):
            self.filtered_out0[i] = 0
            for j in range(i-self.k_cal, i+self.k_cal+1):
                self.filtered_out0[i] = self.filtered_out0[i] + self.filtered_spike[j]*self.gauss_window_cal[j-i+self.k_cal]




