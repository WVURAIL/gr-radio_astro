#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 DSPIRA.
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
from datetime import datetime

class csv_filesink(gr.sync_block):
    """
    This block is controlled by the string variable save_toggle: if save_toggle = "True" (a string, not boolean), the data is written to a new .csv file every new integration time. The minimum integration time for the block to work is 0.1 s. 
    """
    def __init__(self, vec_length, samp_rate, freq, prefix, save_toggle, integration_select, short_long_time_scale, az, elev, location):
        gr.sync_block.__init__(self,
            name="csv_filesink",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=None)

        self.vec_length = int(vec_length)
        self.samp_rate = samp_rate
        self.freq = freq
        self.prefix = prefix
        self.save_toggle = save_toggle
        self.integration_select = integration_select
        self.short_long_time_scale = short_long_time_scale
        self.az = az
        self.elev = elev
        self.location = location

        self.frequencies = np.arange(freq - samp_rate/2, freq + samp_rate/2, samp_rate/vec_length)[:vec_length]
        self.data_array = np.zeros((vec_length,2))
        self.N_long_counter = 0
        self.spectrum = np.zeros(vec_length)

    def work(self, input_items, output_items):
        # in0 = input_items[0]
        # self.spectrum[:] = in0

        in0_buffer = input_items[0]

        for in0 in in0_buffer:

        # <+signal processing here+>

            if self.save_toggle == "True":     #If true, capture the spectrum to a new .csv text file each integration.
                if self.integration_select == 0:
                    current_time = time.time()
                    self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")[:-5]
                    #write (freq, output) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_spectrum.txt"
                    # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
                    self.textfilename = self.prefix + self.timenow + "_" + self.location + "_" + self.az + "_" + self.elev + "_spectrum.csv"
                    self.data_array[:,0] = np.round(self.frequencies/1e6, decimals=4)
                    self.data_array[:,1] = np.round(in0, decimals=4)
                    np.savetxt(self.textfilename, self.data_array, delimiter=',')

                    self.N_long_counter = self.N_long_counter + 1  #Increase counter for long integration print to .csv

                else:
                    if self.N_long_counter >= self.short_long_time_scale-1:
                        current_time = time.time()
                        self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")[:-5]
                        #write (freq, output) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_spectrum.txt"
                        # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
                        self.textfilename = self.prefix + self.timenow + "_" + self.location + "_" + self.az + "_" + self.elev + "_spectrum.csv"
                        self.data_array[:,0] = np.round(self.frequencies/1e6, decimals=4)
                        self.data_array[:,1] = np.round(in0, decimals=4)
                        np.savetxt(self.textfilename, self.data_array, delimiter=',')
                        #
                        self.N_long_counter = 0
                    else:
                        self.N_long_counter = self.N_long_counter + 1  #Increase counter for long integration print to .csv
            
            return len(input_items[0])

    def set_save_toggle(self, save_toggle):
        self.save_toggle = save_toggle

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select

    def set_az(self, az):
        self.az = az

    def set_elev(self, elev):
        self.elev = elev

    def set_location(self, location):
        self.location = location


