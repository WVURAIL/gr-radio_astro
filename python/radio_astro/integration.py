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


import numpy as np
from gnuradio import gr

class integration(gr.decim_block):
    """
    docstring for block integration
    """
    def __init__(self, vec_length, n_integrations):
        gr.decim_block.__init__(self,
            name="integration",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=[(np.float32, int(vec_length))], 
            decim = n_integrations)
        self.n_integrations = n_integrations
        self.vec_length = vec_length
        self.set_relative_rate(1.0/n_integrations)
        self.sum = np.zeros(self.vec_length)
        self.integration_count = 0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for inp0 in in0:
            if self.integration_count < self.n_integrations:
                self.sum = self.sum + inp0
                self.integration_count += 1
            else:
                out[:] = self.sum[:]/self.n_integrations
                self.sum = np.zeros(self.vec_length)
                self.integration_count = 0
        return len(output_items[0])

    def set_n_integrations(self, n_integrations):
        self.n_integrations = n_integrations
        self.set_relative_rate(1.0/n_integrations)
        print("Rate Updated")

