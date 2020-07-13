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

class vector_moving_average(gr.sync_block):
    """
    docstring for block vector_moving_average
    """
    def __init__(self, vec_length, averaging_length, reset_integration):
        gr.sync_block.__init__(self,
            name="vector moving average",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=[(np.float32, int(vec_length))])
        #self.set_history(averaging_length)
        self.averaging_length = averaging_length
        self.vec_length = vec_length
        self._sum1 = np.zeros(self.vec_length)
        self.data_history = np.zeros((self.averaging_length, self.vec_length))
        self.history_count = 0
        self.start_count = 0
        self.reset_integration = reset_integration


    def work(self, input_items, output_items):
        out = output_items[0]
        # Maybe should check here if really averaging length long?
        #print(input_items[0].shape)
        #seems gnuradio gives averaging_length vectors right away, 
        #with zeros till all data there.
        self.data_history[self.history_count] = input_items[0]
        self.history_count += 1
        if self.history_count == self.averaging_length:
             self.history_count = 0

        self._sum1 = self.data_history.sum(axis=0)
        if self.start_count < self.averaging_length:
            self.start_count += 1
            output_items[0][:] = self._sum1/self.start_count
        else:
            output_items[0][:] = self._sum1/self.averaging_length
        return len(output_items[0])

    def set_reset_integration(self, reset_integration):
        self.data_history = np.zeros((self.averaging_length, self.vec_length))
        self.history_count = 0
        self.start_count = 0
        # I don't actually use reset integration variable, just the callback.
        print("Reset Integrations")