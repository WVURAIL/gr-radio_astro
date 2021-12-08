#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NsfIntegrate: SDRPlay 8MHz Astronomical Obs.
# Author: Glen Langston
# Description: Astronomy with 8.0 MHz SDRPlay RSP 1A
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
from gnuradio import sdrplay3



from gnuradio import qtgui

class NsfSdrplayTest80(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NsfIntegrate: SDRPlay 8MHz Astronomical Obs.", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NsfIntegrate: SDRPlay 8MHz Astronomical Obs.")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfSdrplayTest80")

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
        self.samp_rate = samp_rate = 8e6
        self.fftsize = fftsize = 2048
        self.IF_attn = IF_attn = 48
        self.Frequency = Frequency = 1420.406E6

        ##################################################
        # Blocks
        ##################################################
        self._IF_attn_tool_bar = Qt.QToolBar(self)
        self._IF_attn_tool_bar.addWidget(Qt.QLabel("IF_attn" + ": "))
        self._IF_attn_line_edit = Qt.QLineEdit(str(self.IF_attn))
        self._IF_attn_tool_bar.addWidget(self._IF_attn_line_edit)
        self._IF_attn_line_edit.returnPressed.connect(
            lambda: self.set_IF_attn(int(str(self._IF_attn_line_edit.text()))))
        self.top_layout.addWidget(self._IF_attn_tool_bar)
        self.sdrplay3_rsp1a_0 = sdrplay3.rsp1a(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rsp1a_0.set_sample_rate(samp_rate)
        self.sdrplay3_rsp1a_0.set_center_freq(Frequency)
        self.sdrplay3_rsp1a_0.set_bandwidth(0)
        self.sdrplay3_rsp1a_0.set_gain_mode(False)
        self.sdrplay3_rsp1a_0.set_gain(-IF_attn, 'IF')
        self.sdrplay3_rsp1a_0.set_gain(-0, 'RF')
        self.sdrplay3_rsp1a_0.set_freq_corr(0)
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(False)
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(False)
        self.sdrplay3_rsp1a_0.set_agc_setpoint(-30)
        self.sdrplay3_rsp1a_0.set_rf_notch_filter(True)
        self.sdrplay3_rsp1a_0.set_dab_notch_filter(True)
        self.sdrplay3_rsp1a_0.set_biasT(False)
        self.sdrplay3_rsp1a_0.set_debug_mode(False)
        self.sdrplay3_rsp1a_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rsp1a_0.set_show_gain_changes(False)
        self.radio_astro_vmedian_0_2_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_2 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_1 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, 4)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            fftsize,
            Frequency-(samp_rate/2.),
            samp_rate/fftsize,
            "",
            'Intensity',
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(1)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 10)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("Counts")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)

        labels = ['Latest', 'Median', 'Hot', 'Cold', 'Ref',
            '', '', '', '', '']
        widths = [1, 3, 2, 2, 3,
            1, 1, 1, 1, 1]
        colors = ["black", "dark green", "red", "blue", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [2., 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            fftsize,
            100,
            -.5,
            .5,
            "",
            2,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1.)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['I', 'Q', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 4, 0, 2, 2)
        for r in range(4, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.hamming(fftsize), True, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fftsize)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_histogram_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.radio_astro_vmedian_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.radio_astro_vmedian_0_1, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.radio_astro_vmedian_0_1, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_2, 0), (self.radio_astro_vmedian_0_2_0, 0))
        self.connect((self.radio_astro_vmedian_0_2_0, 0), (self.radio_astro_vmedian_0_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_stream_to_vector_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfSdrplayTest80")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.Frequency-(self.samp_rate/2.), self.samp_rate/self.fftsize)
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.Frequency-(self.samp_rate/2.), self.samp_rate/self.fftsize)
        self.radio_astro_vmedian_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_1.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_2.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_2_0.set_vlen(self.fftsize)

    def get_IF_attn(self):
        return self.IF_attn

    def set_IF_attn(self, IF_attn):
        self.IF_attn = IF_attn
        Qt.QMetaObject.invokeMethod(self._IF_attn_line_edit, "setText", Qt.Q_ARG("QString", str(self.IF_attn)))
        self.sdrplay3_rsp1a_0.set_gain(-self.IF_attn, 'IF')

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.Frequency-(self.samp_rate/2.), self.samp_rate/self.fftsize)
        self.sdrplay3_rsp1a_0.set_center_freq(self.Frequency)




def main(top_block_cls=NsfSdrplayTest80, options=None):

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
