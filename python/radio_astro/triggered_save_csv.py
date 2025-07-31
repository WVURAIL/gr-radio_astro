#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Kevin Bandura.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from datetime import datetime

class triggered_save_csv(gr.sync_block):
    """
    docstring for block triggered_save_csv
    """
    def __init__(self, save_length=20, vec_length=4096):
        gr.sync_block.__init__(self,
            name="triggered_save_csv",
            in_sig=[np.int32, (np.complex64,vec_length)],
            out_sig=None)
        # Define vectors and constants:
        self.triggered = False
        self.saved_samples = 0
        self.vec_length = int(vec_length)
        self.save_length = save_length
        self.output_array = np.zeros((self.save_length, self.vec_length), dtype=np.complex64)


    def work(self, input_items, output_items):
        #print(input_items)
        in0 = input_items[0]
        in1 = input_items[1]
        print(np.sum(np.abs(in1[0])))  # Debugging line
        print(in0[0])
        print(self.triggered)
        if in0[0] == 1:  # Trigger condition    
            self.triggered = True
        if self.triggered:
            if self.saved_samples < self.save_length:
                self.output_array[self.saved_samples] = in1[0]
                self.saved_samples += 1
            else:
                # Reset the trigger and saved samples if save_length is reached
                self.triggered = False
                self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")[:-5]
                self.textfilename = self.timenow + "_timestream.csv"
                print("Saving to file:", self.textfilename)
                np.savetxt(self.textfilename, self.output_array.flatten(), delimiter=',')
                self.saved_samples = 0
        return len(input_items[0])
