#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-radio_astro author.
#


import numpy as np
from gnuradio import gr
import time
from datetime import datetime
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    canPlot = True
except:
    print("Can not import matplotlib")
    canPlot = False

class png_print_spectrum(gr.sync_block):
    """
    This block enables a spectrum to be plotted as a png image file.
    The input is
    
    Parameters:
    (1) vec_length - vector length in channels
    (2) samp_rate - used to calculate frequency values for spectrum output; set in a Variable box.
    (3) freq - center frequency used to calculate frequency values for spectrum output; set in a Variable box.
    (4) prefix - Variable block with id = prefix; used in the filename to describe the pathlength. 
    (5) graphprint_toggle - string data type that is "True" or "False" to indicate whether the graph is to be printed to a .png file ("True") or not.
    (6) graphinfo = text input in a QT GUI Entry block input by user during a run. This will show up in the title of the .png file.
    (7) The file is written to the pathlength described by the in a Variable block with id = prefix, and written with filename format = prefix + timenow + graphinfo + ".png"
    """

    def __init__(self, vec_length, samp_rate, freq, prefix, graphprint_toggle, graphinfo):
        gr.sync_block.__init__(self,
            name="png_print_spectrum",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=None)

        self.vec_length = int(vec_length)
        self.samp_rate = samp_rate
        self.freq = freq
        self.prefix = prefix
        self.graphprint_toggle = graphprint_toggle
        self.graphinfo = graphinfo

    # Define vectors and constants:
        self.spectrum = np.zeros(vec_length)
        self.frequencies = np.zeros(vec_length)
        self.frequencies = np.arange(freq - samp_rate/2, freq + samp_rate/2, samp_rate/vec_length)[:vec_length]
        self.data_array = np.zeros((vec_length,2))
        self.a = np.zeros(self.vec_length)    

    def work(self, input_items, output_items):
        inp0 = input_items[0]
        for in0 in inp0:
            self.spectrum[:] = in0

            if self.graphprint_toggle == "True":     #If true, write the spectrum to a .png file.
                current_time = time.time()
                self.timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")[:-5]
                # write (freq, output) as a column array to a text file, titled e.g. "2018-07-24_15.15.49_spectrum.txt"
                # The "prefix", i.e. the file path, is defined in the prefix variable box in the .grc program.
                self.textfilename = self.prefix + self.timenow + "_test.csv"
                self.data_array[:,0] = np.round(self.frequencies/1e6, decimals=4)
                self.data_array[:,1] = np.round(self.spectrum, decimals=4)
                
                # Set up graph and write to png file:
                
                font1 = {'family': 'serif', 'color': 'darkred', 'weight': 'bold', 'size': 20,}

                font2 = {'family': 'serif', 'color':  'darkblue','weight': 'bold','size': 28,}

                fig, ax = plt.subplots(1, figsize=(16, 12))
                plt.title("Spectrum collected at " + self.timenow, fontdict=font2)
                plt.suptitle(self.timenow + "_spectrum.png", fontdict=font1)

                plt.xlim([1419.5,1421.5])
                #plt.ylim([0,50000])
                ax.plot(self.frequencies/1e6, self.spectrum, linewidth=3)
                plt.axhline(linewidth=2, color='black')
                plt.axvline(x=1419.50, linewidth=3, color='black')
                plt.axvline(x=1420.41, linewidth=2, color='r')  # indicate unshifted HI peak position.
                plt.xlabel("Frequency (MHz)", fontdict=font1)
                plt.ylabel("Signal", fontdict=font1)

                #Set tick marks
                ax.xaxis.set_major_locator(plt.MultipleLocator(0.1))
                ax.xaxis.set_minor_locator(plt.MultipleLocator(.01))

                # Add grid lines
                plt.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1)

                # Show the minor grid lines with very faint and almost transparent grey lines
                plt.minorticks_on()
                plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

                #plt.plot(self.frequencies/1e6, self.spectrum)
                plt.savefig(self.prefix + "spectrum" + self.timenow + self.graphinfo +".png")
                plt.show
                self.graphprint_toggle = "False"

        return len(input_items[0])
    
    #Check if graphprint_toggle is changed:

    def set_graphprint_toggle(self, graphprint_toggle):
        if self.graphprint_toggle == "False":
            self.graphprint_toggle = "True"

    def set_graphinfo(self, graphinfo):
        self.graphinfo = graphinfo




