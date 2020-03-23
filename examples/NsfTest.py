#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Signal.  Adds a tone in 1 MHz band
# Author: Glen Langston
# Description: Diagnostic test design
# Generated: Thu Mar 19 21:26:41 2020
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import radio_astro
import sip
import sys
from gnuradio import qtgui


class NsfTest(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test Signal.  Adds a tone in 1 MHz band")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test Signal.  Adds a tone in 1 MHz band")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfTest")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.OffsetMHz = OffsetMHz = 0.111
        self.FreqMHz = FreqMHz = 1437
        self.Bandwidth = Bandwidth = 1.e6
        self.samp_rate = samp_rate = int(Bandwidth)
        self.fftsize = fftsize = 1024
        self.Offset = Offset = OffsetMHz*1.E6
        self.H1 = H1 = 1420.406E6
        self.Gain1 = Gain1 = 75
        self.Frequency = Frequency = FreqMHz*1.E6
        self.Attn1 = Attn1 = 80

        ##################################################
        # Blocks
        ##################################################
        self._Gain1_tool_bar = Qt.QToolBar(self)
        self._Gain1_tool_bar.addWidget(Qt.QLabel('Gain1'+": "))
        self._Gain1_line_edit = Qt.QLineEdit(str(self.Gain1))
        self._Gain1_tool_bar.addWidget(self._Gain1_line_edit)
        self._Gain1_line_edit.returnPressed.connect(
        	lambda: self.set_Gain1(eng_notation.str_to_num(str(self._Gain1_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Gain1_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Attn1_tool_bar = Qt.QToolBar(self)
        self._Attn1_tool_bar.addWidget(Qt.QLabel('Attn1'+": "))
        self._Attn1_line_edit = Qt.QLineEdit(str(self.Attn1))
        self._Attn1_tool_bar.addWidget(self._Attn1_line_edit)
        self._Attn1_line_edit.returnPressed.connect(
        	lambda: self.set_Attn1(eng_notation.str_to_num(str(self._Attn1_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Attn1_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.radio_astro_vmedian_0_2_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_2 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, 4)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            fftsize,
            float(Frequency-(Bandwidth/2.))*1.e-6,
            float(Bandwidth*1.e-6/fftsize),
            "Frequency (MHz)",
            'Intensity',
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(.5)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 1.)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
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
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win, 2, 2, 4, 3)
        for r in range(2, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
        	fftsize,
        	100,
                -.4,
                .4,
        	"",
        	2
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1.)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_histogram_sink_x_0.disable_legend()

        labels = ['I', 'Q', '', '', '',
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
        for i in xrange(2):
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
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 2, 0, 3, 2)
        for r in range(2, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pluto_source_0 = iio.pluto_source('192.168.2.1', int(int(Frequency)), int(int(Bandwidth)), int(20000000), 0x8000, False, False, True, "manual", float(Gain1), '', True)
        self.pluto_sink_0 = iio.pluto_sink('', int(float(Frequency+Offset)), int(float(Bandwidth)), int(20000000), 0x8000, False, float(Attn1), '', True)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, Bandwidth, .1E6, .025E6, firdes.WIN_HAMMING, 6.76))
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, (window.hamming(fftsize)), True, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(fftsize)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((1, ))
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 30, 0)
        self._OffsetMHz_tool_bar = Qt.QToolBar(self)
        self._OffsetMHz_tool_bar.addWidget(Qt.QLabel('OffsetMHz)'+": "))
        self._OffsetMHz_line_edit = Qt.QLineEdit(str(self.OffsetMHz))
        self._OffsetMHz_tool_bar.addWidget(self._OffsetMHz_line_edit)
        self._OffsetMHz_line_edit.returnPressed.connect(
        	lambda: self.set_OffsetMHz(eng_notation.str_to_num(str(self._OffsetMHz_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._OffsetMHz_tool_bar, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._FreqMHz_tool_bar = Qt.QToolBar(self)
        self._FreqMHz_tool_bar.addWidget(Qt.QLabel('Freq (MHz)'+": "))
        self._FreqMHz_line_edit = Qt.QLineEdit(str(self.FreqMHz))
        self._FreqMHz_tool_bar.addWidget(self._FreqMHz_line_edit)
        self._FreqMHz_line_edit.returnPressed.connect(
        	lambda: self.set_FreqMHz(eng_notation.str_to_num(str(self._FreqMHz_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._FreqMHz_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.pluto_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_histogram_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.radio_astro_vmedian_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.pluto_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.pluto_source_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.radio_astro_vmedian_0_2, 0), (self.radio_astro_vmedian_0_2_0, 0))
        self.connect((self.radio_astro_vmedian_0_2_0, 0), (self.radio_astro_vmedian_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfTest")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_OffsetMHz(self):
        return self.OffsetMHz

    def set_OffsetMHz(self, OffsetMHz):
        self.OffsetMHz = OffsetMHz
        self.set_Offset(self.OffsetMHz*1.E6)
        Qt.QMetaObject.invokeMethod(self._OffsetMHz_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.OffsetMHz)))

    def get_FreqMHz(self):
        return self.FreqMHz

    def set_FreqMHz(self, FreqMHz):
        self.FreqMHz = FreqMHz
        self.set_Frequency(self.FreqMHz*1.E6)
        Qt.QMetaObject.invokeMethod(self._FreqMHz_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.FreqMHz)))

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self.set_samp_rate(int(self.Bandwidth))
        self.qtgui_vector_sink_f_0_0.set_x_axis(float(self.Frequency-(self.Bandwidth/2.))*1.e-6, float(self.Bandwidth*1.e-6/self.fftsize))
        self.pluto_source_0.set_params(int(int(self.Frequency)), int(int(self.Bandwidth)), int(20000000), False, False, True, "manual", float(self.Gain1), '', True)
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.Bandwidth, .1E6, .025E6, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.radio_astro_vmedian_0_2_0.set_vlen( self.fftsize)
        self.radio_astro_vmedian_0_2.set_vlen( self.fftsize)
        self.radio_astro_vmedian_0_0.set_vlen( self.fftsize)
        self.radio_astro_vmedian_0.set_vlen( self.fftsize)
        self.qtgui_vector_sink_f_0_0.set_x_axis(float(self.Frequency-(self.Bandwidth/2.))*1.e-6, float(self.Bandwidth*1.e-6/self.fftsize))

    def get_Offset(self):
        return self.Offset

    def set_Offset(self, Offset):
        self.Offset = Offset
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1

    def get_Gain1(self):
        return self.Gain1

    def set_Gain1(self, Gain1):
        self.Gain1 = Gain1
        Qt.QMetaObject.invokeMethod(self._Gain1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Gain1)))
        self.pluto_source_0.set_params(int(int(self.Frequency)), int(int(self.Bandwidth)), int(20000000), False, False, True, "manual", float(self.Gain1), '', True)

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self.qtgui_vector_sink_f_0_0.set_x_axis(float(self.Frequency-(self.Bandwidth/2.))*1.e-6, float(self.Bandwidth*1.e-6/self.fftsize))
        self.pluto_source_0.set_params(int(int(self.Frequency)), int(int(self.Bandwidth)), int(20000000), False, False, True, "manual", float(self.Gain1), '', True)
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)

    def get_Attn1(self):
        return self.Attn1

    def set_Attn1(self, Attn1):
        self.Attn1 = Attn1
        Qt.QMetaObject.invokeMethod(self._Attn1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Attn1)))
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)


def main(top_block_cls=NsfTest, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
