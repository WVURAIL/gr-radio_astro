#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Event Detect
# Author: Glen Langston
# Description: Sigma-based event detection
# Generated: Tue Mar 26 09:34:34 2019
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
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import radio_astro
import sip
import sys
from gnuradio import qtgui


class detect_log(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Event Detect")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Event Detect")
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

        self.settings = Qt.QSettings("GNU Radio", "detect_log")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.vec_length = vec_length = 512
        self.samp_rate = samp_rate = 10e6
        self.nsigma = nsigma = 3.9
        self.mode = mode = 1
        self.freq = freq = 705e6

        ##################################################
        # Blocks
        ##################################################
        self._nsigma_range = Range(0.1, 10., .1, 3.9, 100)
        self._nsigma_win = RangeWidget(self._nsigma_range, self.set_nsigma, 'N Sigma', "counter", float)
        self.top_grid_layout.addWidget(self._nsigma_win)
        self._mode_options = (0, 1, )
        self._mode_labels = ('Monitor', 'Detect', )
        self._mode_tool_bar = Qt.QToolBar(self)
        self._mode_tool_bar.addWidget(Qt.QLabel('Mode'+": "))
        self._mode_combo_box = Qt.QComboBox()
        self._mode_tool_bar.addWidget(self._mode_combo_box)
        for label in self._mode_labels: self._mode_combo_box.addItem(label)
        self._mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._mode_options.index(i)))
        self._mode_callback(self.mode)
        self._mode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_mode(self._mode_options[i]))
        self.top_grid_layout.addWidget(self._mode_tool_bar)
        self.radio_astro_ra_event_sink_0 = radio_astro.ra_event_sink('Watch.not', vec_length, samp_rate, 1)
        self.radio_astro_ra_event_log_0 = radio_astro.ra_event_log('', 'Event Detection', vec_length, samp_rate)
        self.radio_astro_detect_0 = radio_astro.detect(vec_length, nsigma, freq/1e6, samp_rate/1e6, 1, mode)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            vec_length,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'Data Stream',
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.2)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis(-3, 3)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)

        labels = ['I', 'Q', 'I', 'Q', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            vec_length,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'Event',
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(.2)
        self.qtgui_vector_sink_f_0_0.set_y_axis(-3, 3)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)

        labels = ['Event I', 'Event Q', 'I', 'Q', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*vec_length, samp_rate,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*vec_length, '', ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(vec_length)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(vec_length)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_vector_sink_f_0_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.qtgui_vector_sink_f_0_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radio_astro_detect_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_log_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "detect_log")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.radio_astro_ra_event_sink_0.set_vlen( self.vec_length)
        self.radio_astro_ra_event_log_0.set_vlen( self.vec_length)
        self.radio_astro_detect_0.set_vlen( self.vec_length)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.radio_astro_ra_event_sink_0.set_sample_rate( self.samp_rate)
        self.radio_astro_ra_event_log_0.set_sample_rate( self.samp_rate)
        self.radio_astro_detect_0.set_bw( self.samp_rate/1e6)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_nsigma(self):
        return self.nsigma

    def set_nsigma(self, nsigma):
        self.nsigma = nsigma
        self.radio_astro_detect_0.set_dms( self.nsigma)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_callback(self.mode)
        self.radio_astro_detect_0.set_mode( self.mode)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.radio_astro_detect_0.set_f_obs( self.freq/1e6)


def main(top_block_cls=detect_log, options=None):

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
