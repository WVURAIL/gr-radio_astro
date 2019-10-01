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
from scipy import signal

def p_shift(img1, period, iter, s_pos, nt, ndm, t_int):
    #period = 1/.005
    f_step_size = 1/t_int/nt
    iterations = iter
    start_position = s_pos                                  #Determines which multiple of the period to start on

    bin_shift =int(round((period*abs(start_position))/f_step_size)) #Determines the total number of bins shifted from zero

    max_bin = int(round(period*(iterations+start_position)/f_step_size))


    start_bin = int((round((period*abs(start_position+1))/f_step_size))-(round((period*abs(start_position))/f_step_size)))

    # Determines the starting bin size in order to create the arrays
    print("The max bin is", max_bin)
    print("The bin shift is",bin_shift)
    print("The start bin size is",start_bin)

    iterations_new = iterations+1
    #print(start_bin)               # The modified iteration count for the "for loop"
    new_pulse = np.zeros((np.shape(img1)[0],int(start_bin)))
    #print(range((ndm)))


    # The position from the start of the data to begin folding from


    for j in range((ndm)):
        if max_bin > np.shape(img1)[1]:
            print(
                "Error: max bin larger than max size of data array"
            )
            break

        if bin_shift> np.shape(img1)[1]:
            print(
                "Error: bin_shift larger than maximum size of data array"
            )
            break

        all_pulse = np.zeros(int(start_bin))
        pulse_dats= img1[j, 1+int(bin_shift):max_bin+1]               # Sets the data to be looked at 
        
        con=np.zeros(0)                             # The counter for if the bin size changes
        old_bins=0                                  # The previous iteration bin size
        last_start = 0  # The last starting place in the frequency
        skip=0
        for i in range(1,iterations_new):
            bins = int((round(period*(i+start_position)/f_step_size))\
                -(round(period*(i-1+start_position)/f_step_size))) # Determines the number of bins in one "period"
            
            #print(i)
            if bins == old_bins or old_bins == 0:
                #print(i) 
                all_pulse += np.concatenate(
                        
                    (con,pulse_dats[last_start+skip:last_start+bins]) # If current and previous bin sizes are the same,
                                                                # con does not change
                )
                
                last_start += bins                               # Last start is updated
                #print(i)
                #print(last_start)
                
            elif int(old_bins)-int(bins) > 0:
                if skip-(int(old_bins)-int(bins))>=0:
                    skip = skip-(int(old_bins)-int(bins))
                    
                    all_pulse +=np.concatenate(
                        
                        (con, pulse_dats[last_start+skip:last_start+bins]) # Current and previous bin sizes are not the same, so
                    )                                                 # con is changed. Data is also determined
                
                    
                    
                else:
                    print( old_bins)
                    print(bins)
                    con = np.zeros(
                        
                        len(con) + (abs(skip - (int(old_bins)-int(bins))))       # con is updated
                    
                    )
                    skip=0
                    
                
                    all_pulse +=np.concatenate(
                        
                        (con, pulse_dats[last_start:last_start+bins]) # Current and previous bin sizes are not the same, so
                    )                                                 # con is changed. Data is also determined
                
                    last_start += bins                                # Last start is updated
                    #print(i)
                    #print(last_start)
            else:
                #print("two")
                if (len(con) - (int(bins)-int(old_bins)))>= 0:
                    con = np.zeros(
                        len(con) - abs(int(bins)-int(old_bins))      # Con is updated
                    )
                    
                    all_pulse +=np.concatenate(
                        
                        (con,pulse_dats[last_start:last_start+bins]) # Current and previous bin sizes are not the same.
                                                                    # Bin size has increased but is lower or equal to
                    )                                                # the original bin size
                    
                    last_start += bins
                else:
                    skip = int(abs(len(con) - (int(bins)-int(old_bins))))
                    #print("three")
                    all_pulse += pulse_dats[
                        last_start+skip    # Current and previous bin sizes are not the same.
                        :last_start+bins]                            # Bin size has increased but is greater than the 
                                                                    # original bin size.
                    
                    last_start +=int(bins)                               # Last start is updated
                    
                    con = np.zeros(0)                                # Con is reset to 0
                #print(i)
                #print(last_start)
            
            #print(last_start)
            old_bins = bins                                          # old bins is updated
        new_pulse[j,:] = np.fft.fftshift(all_pulse/iterations) # The folded pulse is determined for each freq

    return new_pulse

def detection(img1, img2, nt, ndm, period, iter, s_pos, t_int ):
    """
    Determines if a pulsar has been detected. If so, the data is let through and the dedispersed pulsar is given as an output array. If not, then nothing is given
    and the statement that a pulsar has not been detected is printed.

    NOTES:


    INPUT:

    img1    : (float array) The dedispersed pulsar that we are anylizing.
    img2    : (float array) The noise that is assumed to be the background noise for the pulsar.
    nt      : (int) The number of timestamps
    ndm     : (int) Number of DMs looked at
    period  : (float) 1/(period of the pulsar)

    OUTPUT

    SNR: The signal to noise ratio of the pulsar to noise




    """

    img1 = img1.reshape((ndm, nt))
    img2 = img2.reshape((ndm,nt))

    ffty = np.fft.fft(img1, axis=1)
    ffty_noise = np.fft.fft(img2, axis=1)
    
    window=(signal.tukey(ffty.shape[1], .006))  # The alpha parameter was found based on trial and error.
    B=abs(window*ffty[:])                     
    window_noise = (signal.tukey(ffty_noise.shape[1], .006))
    B_noise = abs(window_noise*ffty_noise[:])

    d_pulse = p_shift(B,period, iter, s_pos, nt, ndm, t_int)
    d_pulse_noise = p_shift(B_noise, period, iter, s_pos, nt, ndm, t_int)
    #print(d_pulse)
    #print(B[2,:])

    maximums_p = np.zeros(len(d_pulse))
    for i in range(len(d_pulse)):
        maximums_p[i] = np.max(d_pulse[i])
        
    #Find the mean and standard deviation
    corr_mean_p = np.mean(d_pulse_noise, axis=1)
    corr_std_p = np.std(d_pulse_noise, axis=1)

    SNR_p = (maximums_p-corr_mean_p)/(corr_std_p)

    return SNR_p.flatten(), B

class Period_Pulse_detection(gr.sync_block):
    """
    Determines if a pulsar has been detected. Does so by folding the data by the period, and then checking the SNR of the data.  
    If so, the data is let through and the dedispersed pulsar is given as an output array and a statement saying that a pulsar has been detected is printed. If not, then nothing is given.

    
    NOTES:

----------------------------------------------------------------------------
    INPUT:

    img1    : (float array) The dedispersed pulsar that we are anylizing.
    img2    : (float array) The noise that is assumed to be the background noise for the pulsar.
    nt      : (int) The number of timestamps in seconds
    ndm     : (int) Number of DMs looked at
    period  : (float) 1/(period of the pulsar), where period of pulsar is in seconds
    iter    : (int) Number of iterations of the period to run through when summing the power spectrum
    s_pos   : (int) What iteration of the period to begin folding on
    t_int   : (float) size of the timestep in the data in seconds

 ----------------------------------------------------------------------------   
    OUTPUT:

    SNR: The signal to noise ratio of the pulsar to noise    
    
    
    """
    def __init__(self, nt, dms, period, iter, s_pos, t_int):
        self.ndm = len(dms)
        gr.sync_block.__init__(self,
            name="Period_Pulse_detection",
            in_sig=[(np.float32, nt*self.ndm),(np.float32,nt*self.ndm)],
            out_sig=[(np.float32, nt)])
        self.nt = nt
        self.dms=dms
        self.period = period
        self.iter = iter
        self.s_pos = s_pos
        self.t_int=t_int


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]
        outcome, sig= detection(in0,in1, self.nt, self.ndm, self.period, self.iter, self.s_pos, self.t_int)
        #print(len(np.where(outcome>10)[0]))
        for i in range(self.ndm):
            #print(outcome)
            if len(np.where(outcome>10)[0]) <1:
                #print("NO PULSAR DETECTED")
                #signals=sig[0]*0
                continue
            elif  outcome[i]==outcome.max():
                out[:] = np.asarray(sig[i])
                print("PULSAR DETECTED")
        #signals = np.asarray(signals)
       

        # <+signal processing here+>
        #out[:] = outcome
        return len(output_items[0])


