#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Kevin Bandura.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class comparator(gr.sync_block):
    """
    docstring for block comparator
    """
    def __init__(self, level=1000):
        gr.sync_block.__init__(self,
            name="comparator",
            in_sig=[np.float32, ],
            out_sig=[np.int32, ])
        self.level = level


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        #print(in0[0])
        if in0[0] > self.level:
            out[:] = 1
        else:
            out[:] = 0
        # Return the number of output items produced
        return len(output_items[0])
