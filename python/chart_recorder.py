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
from datetime import datetime
import time
try:
    import h5py
except:
    print "Python package:"
    print "   h5py"
    print "Not found.  If needed, at the command line type:"
    print "sudo apt install h5py"
    print "or"
    print "pip install h5py"
    print "However we dom't recommend installing python packages using pip"
    print "Use your OS local package manager used to install 'gnuradio' to"
    print "maintain consistent python environments"
    print ""

class chart_recorder(gr.sync_block):
    
    """
    input is integrated data to be added to the output chart recorder array:
        out = array[0,0,0, 0, ... 0, -3 = non-zero value, -2 = non-zero value, -1 = new value input]
    chart_run = binary control to start chart recording write_to_file - determines whether the continuum is captured to a file written to the 
    pathlength described by the prefix variable, and written with the filename = prefix + timenow + "_continuum.csv".
    scan_length = array size of output.
    """
    def __init__(self, scan_length, chart_run, save_to_file, prefix, integration_time):
        gr.sync_block.__init__(self,
            name="chart_recorder",
            in_sig=[(np.float32)],
            out_sig=[(np.float32, int(scan_length))])

        # Define vectors and constants:
        self.scan_length = scan_length
        self.integration_time = integration_time
        self.chart_run = chart_run
        self.save_to_file = save_to_file
        self.prefix = prefix
        self.i = 0
        
        self.output_array = np.zeros(self.scan_length)
        self.time_values = np.arange(0, int(self.scan_length*self.integration_time), self.integration_time)
        self.data_array = np.zeros((int(self.scan_length),2))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        
        if self.chart_run == 1:
            self.output_array[self.i] = in0
            self.i = ((self.i +1) % self.scan_length)
            #print(self.i)

        out[:] = self.output_array.copy()

        # Save the data array to 
        #if (((self.i) % self.scan_length) == 0):
        #    current_time = time.time()
        #    self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        #    #write (time, output_array) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_continuum.txt"
        #    # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
        #    self.textfilename = self.prefix + self.timenow + "_continuum.csv"
        #    self.data_array[:,0] = self.time_values
        #    self.data_array[:,1] = self.output_array.copy()
        #    np.savetxt(self.textfilename, self.data_array, delimiter=',')

        if self.save_to_file == 1:     #If true, capture the spectrum to a .csv text file.
            current_time = time.time()
            self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            #write (time, output_array) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_continuum.txt"
            # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
            self.textfilename = self.prefix + self.timenow + "_continuum.csv"
            self.data_array[:,0] = self.time_values
            self.data_array[:,1] = self.output_array.copy()
            np.savetxt(self.textfilename, self.data_array, delimiter=',')

            self.save_to_file = 0           # Reset save_to_file toggle to 0

        return len(output_items[0])

    #Check if chart_run or save_to_file are changed:

    def start_run(self, chart_run):
        self.chart_run = chart_run
        print(self.chart_run)

    def save_file(self, save_to_file):
        if self.save_to_file == 0:          # The value of save_to_file is not used. This parameter is used simply to call this routine to set
            self.save_to_file = 1           # the save_to_file value to 1 so that the data is written to file in the If statement.
                                            # The Push Button sets the save_to_file value to 1 when pressed, then 0 when released.
                        
