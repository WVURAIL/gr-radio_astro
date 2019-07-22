#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Jul 22 15:19:49 2019
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
from PyQt5.QtCore import QObject, pyqtSlot
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
import numpy as np
import osmosdr
import radio_astro
import sip
import sys
import time
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
        self.vec_length = vec_length = 4096
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/vec_length)
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.samp_rate = samp_rate = 10e6
        self.prefix = prefix = "/home/john/DSPIRA_2019/Horn_Spectra_2019"
        self.freq = freq = 1419e6
        self.ymin = ymin = 0
        self.ymax = ymax = 20000
        self.spectrumcapture_toggle = spectrumcapture_toggle = False
        self.save_toggle = save_toggle = "False"
        self.recfile = recfile = prefix + timenow + "_ymethod_cal.h5"
        self.integration_time = integration_time = 40
        self.freq_step = freq_step = samp_rate/vec_length
        self.freq_start = freq_start = freq - samp_rate/2
        self.display_integration = display_integration = 1
        self.custom_window = custom_window = sinc*np.hamming(4*vec_length)
        self.collect = collect = "nocal"

        ##################################################
        # Blocks
        ##################################################
        self._ymin_range = Range(-100, 5000, 50, 0, 200)
        self._ymin_win = RangeWidget(self._ymin_range, self.set_ymin, 'ymin', "counter", float)
        self.top_grid_layout.addWidget(self._ymin_win, 0, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self._ymax_range = Range(50, 300000, 50, 20000, 200)
        self._ymax_win = RangeWidget(self._ymax_range, self.set_ymax, 'ymax', "counter", float)
        self.top_grid_layout.addWidget(self._ymax_win, 1, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        _spectrumcapture_toggle_push_button = Qt.QPushButton('Capture Latest Spectrum')
        self._spectrumcapture_toggle_choices = {'Pressed': True, 'Released': False}
        _spectrumcapture_toggle_push_button.pressed.connect(lambda: self.set_spectrumcapture_toggle(self._spectrumcapture_toggle_choices['Pressed']))
        _spectrumcapture_toggle_push_button.released.connect(lambda: self.set_spectrumcapture_toggle(self._spectrumcapture_toggle_choices['Released']))
        self.top_grid_layout.addWidget(_spectrumcapture_toggle_push_button, 1, 2, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(2,3)]
        self._save_toggle_options = ("True", "False", )
        self._save_toggle_labels = ('Write to File', 'Not writing to file', )
        self._save_toggle_tool_bar = Qt.QToolBar(self)
        self._save_toggle_tool_bar.addWidget(Qt.QLabel('Save File'+": "))
        self._save_toggle_combo_box = Qt.QComboBox()
        self._save_toggle_tool_bar.addWidget(self._save_toggle_combo_box)
        for label in self._save_toggle_labels: self._save_toggle_combo_box.addItem(label)
        self._save_toggle_callback = lambda i: Qt.QMetaObject.invokeMethod(self._save_toggle_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._save_toggle_options.index(i)))
        self._save_toggle_callback(self.save_toggle)
        self._save_toggle_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_save_toggle(self._save_toggle_options[i]))
        self.top_grid_layout.addWidget(self._save_toggle_tool_bar, 1, 4, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(4,5)]
        self._collect_options = ("nocal", "cal", "hot", "cold", )
        self._collect_labels = ("Spectrum with no calibration", "Spectrum with calibration", "Hot calibration", "Cold calibration", )
        self._collect_tool_bar = Qt.QToolBar(self)
        self._collect_tool_bar.addWidget(Qt.QLabel("Collect Data"+": "))
        self._collect_combo_box = Qt.QComboBox()
        self._collect_tool_bar.addWidget(self._collect_combo_box)
        for label in self._collect_labels: self._collect_combo_box.addItem(label)
        self._collect_callback = lambda i: Qt.QMetaObject.invokeMethod(self._collect_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._collect_options.index(i)))
        self._collect_callback(self.collect)
        self._collect_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_collect(self._collect_options[i]))
        self.top_grid_layout.addWidget(self._collect_tool_bar, 0, 2, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(2,3)]
        self.radio_astro_systemp_calibration_0 = radio_astro.systemp_calibration(vec_length, collect, samp_rate, freq, prefix, spectrumcapture_toggle)
        self.radio_astro_hdf5_sink_0_0_0 = radio_astro.hdf5_sink(float, 1, vec_length, save_toggle, recfile+"_3LNA17", 'A180E55', freq - samp_rate/2, samp_rate/vec_length, '')
        self.qtgui_vector_sink_f_0_0_1 = qtgui.vector_sink_f(
            vec_length,
            freq - samp_rate/2,
            samp_rate/vec_length,
            "Frequency",
            "Signal",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(ymin, ymax)
        self.qtgui_vector_sink_f_0_0_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_1_win, 4, 0, 5, 5)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(4,9)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,5)]
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            vec_length,
            freq - samp_rate/2,
            samp_rate/vec_length,
            "frequency",
            "Gain",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis(0, 200)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win, 9, 2, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(9,10)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(2,3)]
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            vec_length,
            freq - samp_rate/2,
            samp_rate/vec_length,
            "frequency",
            "System Temperature",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 400)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win, 9, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(9,10)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
        	1024,
        	100,
                -1,
                1,
        	"",
        	1
        )

        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_histogram_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 9, 3, 1, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(9,10)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(3,5)]
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'airspy=0,bias=1,pack=0' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(14, 0)
        self.osmosdr_source_0.set_if_gain(12, 0)
        self.osmosdr_source_0.set_bb_gain(10, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.fft_vxx_0 = fft.fft_vcc(vec_length, True, (window.rectangular(vec_length)), True, 1)
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_multiply_const_vxx_0_2 = blocks.multiply_const_vcc((custom_window[-vec_length:]))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((custom_window[2*vec_length:3*vec_length]))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((custom_window[vec_length:2*vec_length]))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((custom_window[0:vec_length]))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(int(display_integration*samp_rate/vec_length), vec_length)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 3*vec_length)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2*vec_length)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(vec_length)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(vec_length)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.radio_astro_systemp_calibration_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 2), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 1), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 0), (self.qtgui_vector_sink_f_0_0_1, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 0), (self.radio_astro_hdf5_sink_0_0_0, 0))

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
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.set_freq_step(self.samp_rate/self.vec_length)
        self.blocks_multiply_const_vxx_0_2.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_1.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[0:self.vec_length]))
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
        self.set_recfile(self.prefix + self.timenow + "_ymethod_cal.h5")

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.set_freq_step(self.samp_rate/self.vec_length)
        self.set_freq_start(self.freq - self.samp_rate/2)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile(self.prefix + self.timenow + "_ymethod_cal.h5")

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.freq - self.samp_rate/2, self.samp_rate/self.vec_length)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.set_freq_start(self.freq - self.samp_rate/2)

    def get_ymin(self):
        return self.ymin

    def set_ymin(self, ymin):
        self.ymin = ymin
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(self.ymin, self.ymax)

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(self.ymin, self.ymax)

    def get_spectrumcapture_toggle(self):
        return self.spectrumcapture_toggle

    def set_spectrumcapture_toggle(self, spectrumcapture_toggle):
        self.spectrumcapture_toggle = spectrumcapture_toggle
        self.radio_astro_systemp_calibration_0.set_parameters(self.collect, self.spectrumcapture_toggle)

    def get_save_toggle(self):
        return self.save_toggle

    def set_save_toggle(self, save_toggle):
        self.save_toggle = save_toggle
        self._save_toggle_callback(self.save_toggle)
        self.radio_astro_hdf5_sink_0_0_0.set_save_toggle(self.save_toggle)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time

    def get_freq_step(self):
        return self.freq_step

    def set_freq_step(self, freq_step):
        self.freq_step = freq_step

    def get_freq_start(self):
        return self.freq_start

    def set_freq_start(self, freq_start):
        self.freq_start = freq_start

    def get_display_integration(self):
        return self.display_integration

    def set_display_integration(self, display_integration):
        self.display_integration = display_integration

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0_2.set_k((self.custom_window[-self.vec_length:]))
        self.blocks_multiply_const_vxx_0_1.set_k((self.custom_window[2*self.vec_length:3*self.vec_length]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[self.vec_length:2*self.vec_length]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[0:self.vec_length]))

    def get_collect(self):
        return self.collect

    def set_collect(self, collect):
        self.collect = collect
        self._collect_callback(self.collect)
        self.radio_astro_systemp_calibration_0.set_parameters(self.collect, self.spectrumcapture_toggle)


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
