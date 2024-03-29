#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vector median comparison
# Author: Glen Langston
# Description: This GRC demo compares the outputs of average and median with straght vector plotting
# GNU Radio version: 3.10.0.0-rc1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
import sip
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
from gnuradio import radio_astro



from gnuradio import qtgui

class vectordemo_c2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Vector median comparison", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Vector median comparison")
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

        self.settings = Qt.QSettings("GNU Radio", "vectordemo_c2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.fftsize = fftsize = 1024
        self.decimate = decimate = 4

        ##################################################
        # Blocks
        ##################################################
        self._decimate_tool_bar = Qt.QToolBar(self)
        self._decimate_tool_bar.addWidget(Qt.QLabel("Decimate" + ": "))
        self._decimate_line_edit = Qt.QLineEdit(str(self.decimate))
        self._decimate_tool_bar.addWidget(self._decimate_line_edit)
        self._decimate_line_edit.returnPressed.connect(
            lambda: self.set_decimate(int(str(self._decimate_line_edit.text()))))
        self.top_grid_layout.addWidget(self._decimate_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, decimate)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, decimate)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fftsize,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 100)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['One in 4', 'Median', 'Median', '', '',
            '', '', '', '', '']
        widths = [1, 2, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["black", "blue", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.blackmanharris(1024), False, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*fftsize, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, min(decimate,15))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, min(decimate,15))
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(fftsize)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0_1 = blocks.add_const_vff([50.]*fftsize)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vff([0.]*fftsize)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2e5, .05, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 3e5, .1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.blocks_add_const_vxx_0_1, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_add_const_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.radio_astro_vmedian_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vectordemo_c2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
        self.blocks_add_const_vxx_0_0.set_k([0.]*self.fftsize)
        self.blocks_add_const_vxx_0_1.set_k([50.]*self.fftsize)
        self.radio_astro_vmedian_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0.set_vlen(self.fftsize)

    def get_decimate(self):
        return self.decimate

    def set_decimate(self, decimate):
        self.decimate = decimate
        Qt.QMetaObject.invokeMethod(self._decimate_line_edit, "setText", Qt.Q_ARG("QString", str(self.decimate)))
        self.blocks_keep_one_in_n_0.set_n(min(self.decimate,15))
        self.blocks_keep_one_in_n_0_0.set_n(min(self.decimate,15))
        self.radio_astro_vmedian_0.set_mode(self.decimate)
        self.radio_astro_vmedian_0_0.set_mode(self.decimate)




def main(top_block_cls=vectordemo_c2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
