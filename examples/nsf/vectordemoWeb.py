#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vector averaging and median comparison
# Author: Glen Langston
# Description: This GRC demo compares the outputs of average and median with straght vector plotting
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import radio_astro
import bokehgui




class vectordemoWeb(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Vector averaging and median comparison", catch_exceptions=True)
        self.plot_lst = []
        self.widget_lst = []

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.fftsize = fftsize = 1024

        ##################################################
        # Blocks
        ##################################################
        self.radio_astro_ra_vmedian_0_0 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_vmedian_0 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_vave_0_0 = radio_astro.ra_vave(fftsize, 4)
        self.radio_astro_ra_vave_0 = radio_astro.ra_vave(fftsize, 4)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.blackmanharris(1024), False, 1)
        self.bokehgui_vector_sink_x_0 = bokehgui.vec_sink_f_proc(fftsize,
                             "",                     3                    )

        labels = ['Original', 'Average', 'Median', '', '',
                  '', '', '', '', '']
        legend_list = []

        for i in  range(    3  ):
          if len(labels[i]) == 0:
            legend_list.append("Data {0}".format(i))
          else:
            legend_list.append(labels[i])

        self.bokehgui_vector_sink_x_0_plot = bokehgui.vec_sink_f(self.plot_lst, self.bokehgui_vector_sink_x_0, update_time = 2000, legend_list = legend_list, is_message =False)

        self.bokehgui_vector_sink_x_0_plot.set_y_axis([-10, 150])
        self.bokehgui_vector_sink_x_0_plot.set_y_label('Intensity' + '(' +'Counts'+')')
        self.bokehgui_vector_sink_x_0_plot.set_x_label('Samples' + '(' +""+')')

        self.bokehgui_vector_sink_x_0_plot.set_x_values([1,fftsize])
        self.bokehgui_vector_sink_x_0_plot.enable_grid(False)
        self.bokehgui_vector_sink_x_0_plot.enable_axis_labels(True)
        self.bokehgui_vector_sink_x_0_plot.enable_legend(True)
        self.bokehgui_vector_sink_x_0_plot.set_layout(*([1,0,1,1]))
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        styles = ["solid", "solid", "solid", "solid", "solid",
                  "solid", "solid", "solid", "solid", "solid"]
        markers = [None, None, None, None, None,
                   None, None, None, None, None]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in  range(     3  ):
          self.bokehgui_vector_sink_x_0_plot.format_line(i, colors[i], widths[i], styles[i], markers[i], alphas[i])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*fftsize, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, 4)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, 4)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(fftsize)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0_1 = blocks.add_const_vff([100.]*fftsize)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vff([0.]*fftsize)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff([50.]*fftsize)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2e5, .05, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 3e5, .1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.bokehgui_vector_sink_x_0, 1))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.bokehgui_vector_sink_x_0, 2))
        self.connect((self.blocks_add_const_vxx_0_1, 0), (self.bokehgui_vector_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_add_const_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radio_astro_ra_vave_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radio_astro_ra_vmedian_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.radio_astro_ra_vave_0, 0), (self.radio_astro_ra_vave_0_0, 0))
        self.connect((self.radio_astro_ra_vave_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.radio_astro_ra_vmedian_0, 0), (self.radio_astro_ra_vmedian_0_0, 0))
        self.connect((self.radio_astro_ra_vmedian_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.blocks_add_const_vxx_0.set_k([50.]*self.fftsize)
        self.blocks_add_const_vxx_0_0.set_k([0.]*self.fftsize)
        self.blocks_add_const_vxx_0_1.set_k([100.]*self.fftsize)




def main(top_block_cls=vectordemoWeb, options=None):
    # Create Top Block instance
    tb = top_block_cls()

    try:
        tb.start()

        bokehgui.utils.run_server(tb, sizing_mode = "fixed",  widget_placement =  (0, 0), window_size =  (400, 500))
    finally:
        print("Exiting the simulation. Stopping Bokeh Server")
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
