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
from gnuradio import gr
from numba import jit

class dedisperse(gr.basic_block):
    """
    dedisperse block.  Limited to sqare sizes right now
    """
    def __init__(self, vec_length, dms, f_obs, bw, t_int, nt):
        self.ndms = len(dms)
        gr.basic_block.__init__(self,
            name="dedisperse",
            in_sig=[(np.float32, vec_length*nt)],
            out_sig=[(np.float32, vec_length*self.ndms)])
        self.vec_length = vec_length
        self.dms = dms
        self.f_obs = f_obs
        self.bw = bw
        self.nt = nt
        self.t_int = t_int


    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = 1

    @jit
    def dedisperse(img):
        '''Takes in 2d freq vs time and de-disperses it for all the dm in dms
        f_low is the lower frequency.  bw is the total passed bandwidth in mhz. t_bin is the size of a time bin in milliseconds'''
        nf = self.vec_length
        nt = self.nt
        ndm = self.ndm
        dmk = 4148808.0/(self.t_int)
        de_dis_ar = np.zeros((ndm,nt))
        #indecies = np.arange(nt)
        f_low = self.f_obs - self.bw/2
        inv_flow_sq = 1/(f_low)**2
        for i in range(ndm):
            for j in range(nf):
                #ys = indecies.copy()
                shift = int(round(dmk*dms[i] * (inv_flow_sq -1/((bw*(nf-j))/nf + f_low)**2 )) )
                for k in range(nt):
                    y = (k - shift ) % nt
                    de_dis_ar[i,k] += img[j,y]
        return de_dis_ar


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out[:] = self.dedisperse(in0)
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
