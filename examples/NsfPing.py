#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Signal.  Adds a Short pulse in a narrow Band
# Author: Glen Langston
# Description: Diagnostic test design
# Generated: Mon Mar 23 10:44:39 2020
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
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import radio_astro
import sip
import sys
from gnuradio import qtgui


class NsfPing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test Signal.  Adds a Short pulse in a narrow Band")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test Signal.  Adds a Short pulse in a narrow Band")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfPing")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.OffsetMHz = OffsetMHz = 0.111
        self.FreqMHz = FreqMHz = 1398
        self.samp_rate = samp_rate = 100000
        self.fftsize = fftsize = 2048
        self.Offset = Offset = OffsetMHz*1.E6
        self.Mode = Mode = 2
        self.H1 = H1 = 1420.406E6
        self.Gain1 = Gain1 = 40
        self.Frequency = Frequency = FreqMHz*1.E6
        self.EventMode = EventMode = 0
        self.Bandwidth = Bandwidth = 4e6
        self.Attn1 = Attn1 = 80

        ##################################################
        # Blocks
        ##################################################
        self._Mode_options = (0, 2, )
        self._Mode_labels = ('Monitor', 'Detect', )
        self._Mode_tool_bar = Qt.QToolBar(self)
        self._Mode_tool_bar.addWidget(Qt.QLabel('Data Mode'+": "))
        self._Mode_combo_box = Qt.QComboBox()
        self._Mode_tool_bar.addWidget(self._Mode_combo_box)
        for label in self._Mode_labels: self._Mode_combo_box.addItem(label)
        self._Mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Mode_options.index(i)))
        self._Mode_callback(self.Mode)
        self._Mode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_Mode(self._Mode_options[i]))
        self.top_grid_layout.addWidget(self._Mode_tool_bar, 6, 0, 1, 2)
        for r in range(6, 7):
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
        self.radio_astro_detect_0 = radio_astro.detect(fftsize, 5, Frequency, Bandwidth, fftsize*1.e-6/Bandwidth, Mode)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
        	fftsize, #size
        	Bandwidth, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0.set_y_axis(-.3, .3)

        self.qtgui_time_sink_x_0_0.set_y_label('Event', "")

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['I', 'Q', '', '', '',
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

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 2, 5, 7)
        for r in range(2, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 9):
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
        self.pluto_sink_0 = iio.pluto_sink('', int(float(Frequency+Offset)), int(float(Bandwidth)), int(20000000), 0x8000, False, float(Attn1), '', True)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(.999999, 1., 1.)
        (self.blocks_threshold_ff_0).set_max_output_buffer(1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vff((10, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.2, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SAW_WAVE, .02, 1.00001, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, .15, 0)
        self.Ping = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.Ping.set_update_time(0.10)
        self.Ping.set_title("Ramp")

        labels = ['Ping', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.Ping.set_min(i, 0.)
            self.Ping.set_max(i, 1)
            self.Ping.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.Ping.set_label(i, "Data {0}".format(i))
            else:
                self.Ping.set_label(i, labels[i])
            self.Ping.set_unit(i, units[i])
            self.Ping.set_factor(i, factor[i])

        self.Ping.enable_autoscale(False)
        self._Ping_win = sip.wrapinstance(self.Ping.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._Ping_win, 0, 4, 2, 5)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self._EventMode_options = (0, 1, )
        self._EventMode_labels = ('Wait', 'Write', )
        self._EventMode_tool_bar = Qt.QToolBar(self)
        self._EventMode_tool_bar.addWidget(Qt.QLabel('Write Mode'+": "))
        self._EventMode_combo_box = Qt.QComboBox()
        self._EventMode_tool_bar.addWidget(self._EventMode_combo_box)
        for label in self._EventMode_labels: self._EventMode_combo_box.addItem(label)
        self._EventMode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._EventMode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._EventMode_options.index(i)))
        self._EventMode_callback(self.EventMode)
        self._EventMode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_EventMode(self._EventMode_options[i]))
        self.top_grid_layout.addWidget(self._EventMode_tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.Ping, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_histogram_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.pluto_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.radio_astro_detect_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.blocks_vector_to_stream_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfPing")
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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.radio_astro_detect_0.set_vlen( self.fftsize)

    def get_Offset(self):
        return self.Offset

    def set_Offset(self, Offset):
        self.Offset = Offset
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)

    def get_Mode(self):
        return self.Mode

    def set_Mode(self, Mode):
        self.Mode = Mode
        self._Mode_callback(self.Mode)
        self.radio_astro_detect_0.set_mode( self.Mode)

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1

    def get_Gain1(self):
        return self.Gain1

    def set_Gain1(self, Gain1):
        self.Gain1 = Gain1
        Qt.QMetaObject.invokeMethod(self._Gain1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Gain1)))

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self.radio_astro_detect_0.set_freq( self.Frequency)
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)

    def get_EventMode(self):
        return self.EventMode

    def set_EventMode(self, EventMode):
        self.EventMode = EventMode
        self._EventMode_callback(self.EventMode)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self.radio_astro_detect_0.set_bw( self.Bandwidth)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.Bandwidth)
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)

    def get_Attn1(self):
        return self.Attn1

    def set_Attn1(self, Attn1):
        self.Attn1 = Attn1
        Qt.QMetaObject.invokeMethod(self._Attn1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Attn1)))
        self.pluto_sink_0.set_params(int(float(self.Frequency+self.Offset)), int(float(self.Bandwidth)), int(20000000), float(self.Attn1), '', True)


def main(top_block_cls=NsfPing, options=None):

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
