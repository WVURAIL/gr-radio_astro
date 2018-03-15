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
import time

class dedisperse(gr.basic_block):
    """
    dedisperse block.  Limited to sqare sizes right now
    """
    def __init__(self, vec_length, dms, f_obs, bw, t_int, nt):
        self.ndm = len(dms)
        gr.basic_block.__init__(self,
            name="dedisperse",
            in_sig=[(np.float32, vec_length*nt)],
            out_sig=[(np.float32, nt*self.ndm)])
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

    #@jit
    def dedisperse(self, img):
        '''Takes in 2d freq vs time and de-disperses it for all the dm in dms
        f_low is the lower frequency.  bw is the total passed bandwidth in mhz. t_bin is the size of a time bin in milliseconds'''
        current_time = time.time()
        nf = self.vec_length
        nt = self.nt
        ndm = self.ndm
        dmk = 4148808.0/(self.t_int)
        de_dis_ar = np.zeros((nt,ndm))
        #indecies = np.arange(nt)
        print(img.shape)
        img = img.reshape((nt,self.vec_length))
        f_low = self.f_obs - self.bw/2
        inv_flow_sq = 1/(f_low)**2
        for i in range(ndm):
            for j in range(nf):
                #ys = indecies.copy()
                #shift = int(round(dmk*self.dms[i] * (inv_flow_sq -1/((self.bw*(nf-j))/nf + f_low)**2 )) )  #nf-j if freq inverted.
                shift = int(round(dmk*self.dms[i] * (inv_flow_sq -1/((self.bw*(j))/nf + f_low)**2 )) )
                for k in range(nt):
                    y = (k - shift ) % nt
                    de_dis_ar[k,i] += img[y,j]
        new_time = time.time()
        time_difference = new_time-current_time
        print(time_difference)
        return de_dis_ar.flatten()


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out[:] = self.dedisperse(in0)
        self.consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
