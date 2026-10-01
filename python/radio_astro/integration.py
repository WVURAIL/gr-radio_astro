#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Kevin Bandura.
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


import operator
import numpy as np
from gnuradio import gr

class integration(gr.decim_block):
    """
    docstring for block integration
    """
    def __init__(self, vec_length, n_integrations):
        n_integrations = self._validate_integrations(n_integrations)
        gr.decim_block.__init__(self,
            name="integration",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=[(np.float32, int(vec_length))], 
            decim = n_integrations)
        self.n_integrations = n_integrations
        self.vec_length = vec_length

    @staticmethod
    def _validate_integrations(value):
        value = operator.index(value)
        if value < 1:
            raise ValueError("n_integrations must be positive")
        return value

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        n = self.n_integrations
        count = min(len(out), len(in0) // n)
        if count:
            windows = in0[:count * n].reshape(count, n, self.vec_length)
            out[:count] = windows.mean(axis=1, dtype=np.float64)
        return count

    def set_n_integrations(self, n_integrations):
        n = self._validate_integrations(n_integrations)
        self.n_integrations = n
        # The Python decimator uses this value when consuming input items.
        self._decim = n
        self.set_relative_rate(1, n)
