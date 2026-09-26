#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Jul 17 16:01:37 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import dedispersion_oot
import numpy as np
import radio_astro
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.vec_length = vec_length = 400
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/vec_length)
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.prefix = prefix = "/home/dspradio/grc_data/"
        self.samp_rate = samp_rate = 10e6
        self.recfile = recfile = prefix + timenow + "rtl_drift.h5"
        self.freq = freq = 1420.5e6
        self.dm_number = dm_number = 1
        self.display_integration = display_integration = 0.0002
        self.delay1 = delay1 = 0
        self.custom_window = custom_window = sinc*np.hamming(4*vec_length)

        ##################################################
        # Blocks
        ##################################################
        self.radio_astro_dedispersed_0_0 = radio_astro.dedispersed(400, 0, 1400, 10, 150.0/750, 750, 20, 21, 1)
        self.radio_astro_dedispersed_0 = radio_astro.dedispersed(400, 0, 1400, 10, 150.0/750, 750, 20, 21, 1)
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            vec_length,
            0,
            1,
            "x-Axis",
            "y-Axis",
            "one",
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(.1)
        self.qtgui_vector_sink_f_0_1.set_y_axis(-140, 10)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
        	2, #size
        	1e6, #samp_rate
        	"Detection", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.010)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["green", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	750, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	750, #size
        	samp_rate/10, #samp_rate
        	"dedispersed", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.fft_vxx_0_0 = fft.fft_vcc(400, True, (window.rectangular(vec_length)), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(400, True, (window.rectangular(vec_length)), True, 1)
        self._delay1_range = Range(0, 20000, 10, 0, 200)
        self._delay1_win = RangeWidget(self._delay1_range, self.set_delay1, "delay1", "counter_slider", int)
        self.top_layout.addWidget(self._delay1_win)
        self.dedispersion_oot_Pulse_Detection_0 = dedispersion_oot.Pulse_Detection(25, 2.0, 750, ([2]*dm_number))
        self.blocks_vector_to_stream_1_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, dm_number)
        self.blocks_vector_to_stream_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, 750*dm_number)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_float*1, 400)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, 400)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, 5e9,True)
        self.blocks_stream_to_vector_2_0 = blocks.stream_to_vector(gr.sizeof_float*400, 750)
        self.blocks_stream_to_vector_2 = blocks.stream_to_vector(gr.sizeof_float*400, 750)
        self.blocks_stream_to_vector_1_1 = blocks.stream_to_vector(gr.sizeof_float*1, 400)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, 400)
        self.blocks_stream_to_vector_0_3 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_2_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_multiply_const_vxx_0_3 = blocks.multiply_const_vcc((custom_window[0:vec_length]))
        self.blocks_multiply_const_vxx_0_2_0 = blocks.multiply_const_vcc((custom_window[-vec_length:]))
        self.blocks_multiply_const_vxx_0_2 = blocks.multiply_const_vcc((custom_window[-vec_length:]))
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_vcc((custom_window[2*vec_length:3*vec_length]))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((custom_window[2*vec_length:3*vec_length]))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc((custom_window[vec_length:2*vec_length]))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((custom_window[vec_length:2*vec_length]))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((custom_window[0:vec_length]))
        self.blocks_multiply_conjugate_cc_0_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_interleaved_short_to_complex_0_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_cc(int(display_integration*samp_rate/vec_length), vec_length)
        self.blocks_integrate_xx_0_0 = blocks.integrate_cc(int(display_integration*samp_rate/vec_length), vec_length)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(400, 1)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_short*1, '/home/andy/FRB_Pipeline_and_Contributions/gr-transient/jupyter/pulse_sim_10mhz_int16_5ms_period_60dm_1400MHz_center_150ms_long_noise.bin', True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, '/home/andy/FRB_Pipeline_and_Contributions/gr-transient/jupyter/pulse_sim_10mhz_int16_5ms_period_60dm_1400MHz_center_150ms_long.bin', True)
        self.blocks_delay_0_0_1 = blocks.delay(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_delay_0_0_0_1 = blocks.delay(gr.sizeof_gr_complex*1, 2*vec_length)
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 3*vec_length)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 3*vec_length)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2*vec_length)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(vec_length)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(vec_length)
        self.blocks_add_xx_0_0 = blocks.add_vcc(vec_length)
        self.blocks_add_xx_0 = blocks.add_vcc(vec_length)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1_0, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_stream_to_vector_0_2_0, 0))
        self.connect((self.blocks_delay_0_0_1, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_interleaved_short_to_complex_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0_0, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0_0, 0), (self.blocks_delay_0_0_0_1, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0_0, 0), (self.blocks_delay_0_0_1, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0_0, 0), (self.blocks_stream_to_vector_0_3, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_2_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_3, 0), (self.blocks_add_xx_0_0, 3))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0, 0), (self.blocks_multiply_const_vxx_0_3, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_3, 0), (self.blocks_multiply_const_vxx_0_2_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.blocks_stream_to_vector_2, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_stream_to_vector_1_1, 0), (self.blocks_stream_to_vector_2_0, 0))
        self.connect((self.blocks_stream_to_vector_1_1, 0), (self.qtgui_vector_sink_f_0_1, 1))
        self.connect((self.blocks_stream_to_vector_2, 0), (self.radio_astro_dedispersed_0, 0))
        self.connect((self.blocks_stream_to_vector_2_0, 0), (self.radio_astro_dedispersed_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.blocks_stream_to_vector_1_1, 0))
        self.connect((self.blocks_vector_to_stream_1_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_vector_to_stream_1_0_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.dedispersion_oot_Pulse_Detection_0, 0), (self.blocks_vector_to_stream_1_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 1))
        self.connect((self.radio_astro_dedispersed_0, 0), (self.blocks_vector_to_stream_1_0, 0))
        self.connect((self.radio_astro_dedispersed_0, 0), (self.dedispersion_oot_Pulse_Detection_0, 0))
        self.connect((self.radio_astro_dedispersed_0_0, 0), (self.dedispersion_oot_Pulse_Detection_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.vec_length))
        self.blocks_multiply_const_vxx_0_3.set_k((self.custom_window[0:self.vec_length]))
        self.blocks_multiply_const_vxx_0_2_0.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_2.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_1_0.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_1.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[0:self.vec_length]))
        self.blocks_delay_0_0_1.set_dly(self.vec_length)
        self.blocks_delay_0_0_0_1.set_dly(2*self.vec_length)
        self.blocks_delay_0_0_0_0_0.set_dly(3*self.vec_length)
        self.blocks_delay_0_0_0_0.set_dly(3*self.vec_length)
        self.blocks_delay_0_0_0.set_dly(2*self.vec_length)
        self.blocks_delay_0_0.set_dly(self.vec_length)

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow
        self.set_recfile(self.prefix + self.timenow + "rtl_drift.h5")

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile(self.prefix + self.timenow + "rtl_drift.h5")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/10)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_dm_number(self):
        return self.dm_number

    def set_dm_number(self, dm_number):
        self.dm_number = dm_number

    def get_display_integration(self):
        return self.display_integration

    def set_display_integration(self, display_integration):
        self.display_integration = display_integration

    def get_delay1(self):
        return self.delay1

    def set_delay1(self, delay1):
        self.delay1 = delay1

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0_3.set_k((self.custom_window[0:self.vec_length]))
        self.blocks_multiply_const_vxx_0_2_0.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_2.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_1_0.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_1.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[0:self.vec_length]))


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
