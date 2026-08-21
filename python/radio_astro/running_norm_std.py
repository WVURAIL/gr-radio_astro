#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Kevin Bandura.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class running_norm_std(gr.sync_block):
    """
    docstring for block running_norm_std
    """
    def __init__(self, intype, vec_length, running_length ):
        if intype == complex:
            datatype = np.complex64
        elif intype == float:
            datatype = np.float32
        elif intype == int:
            datatype = np.int32
        else:
            raise
        gr.sync_block.__init__(self,
            name="running_norm_std",
            in_sig=[(datatype, int(vec_length))],
            out_sig=[(datatype, int(vec_length))])
        self.datatype = datatype
        self.running_length = running_length
        self.vec_length = vec_length
        self._std1 = np.zeros(self.vec_length, dtype=self.datatype)
        self.data_history = np.zeros((self.running_length, self.vec_length), dtype=self.datatype)
        self.history_count = 0
        self.start_count = 0


    def work(self, input_items, output_items):
        out = output_items[0]
        in0_all = input_items[0]
        for in_input, in0 in enumerate(in0_all):
            self.data_history[self.history_count] = in0
            self.history_count += 1
            if self.history_count == self.running_length:
                self.history_count = 0

            self._std1 = self.data_history.std(axis=0)
            output_items[0][in_input,:] = self._std1
        return len(output_items[0])
