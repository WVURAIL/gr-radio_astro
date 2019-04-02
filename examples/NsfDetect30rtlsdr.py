#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Nsf RTLSDR Event Detect: 3MHz
# Author: Glen Langston
# Description: Rtlsdr
# Generated: Tue Apr  2 15:34:33 2019
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import radio_astro
import sip
import sys
import time
from gnuradio import qtgui


class NsfDetect30rtlsdr(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Nsf RTLSDR Event Detect: 3MHz")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Nsf RTLSDR Event Detect: 3MHz")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfDetect30rtlsdr")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.observer = observer = 'observers_save'
        self.nsigma = nsigma = 5.0
        self.fftsize = fftsize = 8192
        self.Telescope = Telescope = 'telescope_save'
        self.Mode = Mode = 2
        self.Gain1 = Gain1 = 45.0
        self.Frequency = Frequency = 1420.4
        self.EventMode = EventMode = 0
        self.Elevation = Elevation = -90
        self.Device = Device = 'rtlsdr=0'
        self.Bandwidth = Bandwidth = 3.
        self.Azimuth = Azimuth = 0

        ##################################################
        # Blocks
        ##################################################
        self._nsigma_range = Range(0., 10., .1, 5.0, 100)
        self._nsigma_win = RangeWidget(self._nsigma_range, self.set_nsigma, 'N Sigma', "counter", float)
        self.top_grid_layout.addWidget(self._nsigma_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fftsize_tool_bar = Qt.QToolBar(self)
        self._fftsize_tool_bar.addWidget(Qt.QLabel('Window_size'+": "))
        self._fftsize_line_edit = Qt.QLineEdit(str(self.fftsize))
        self._fftsize_tool_bar.addWidget(self._fftsize_line_edit)
        self._fftsize_line_edit.returnPressed.connect(
        	lambda: self.set_fftsize(int(str(self._fftsize_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._fftsize_tool_bar, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Telescope_tool_bar = Qt.QToolBar(self)
        self._Telescope_tool_bar.addWidget(Qt.QLabel('Tel'+": "))
        self._Telescope_line_edit = Qt.QLineEdit(str(self.Telescope))
        self._Telescope_tool_bar.addWidget(self._Telescope_line_edit)
        self._Telescope_line_edit.returnPressed.connect(
        	lambda: self.set_Telescope(str(str(self._Telescope_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Telescope_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Mode_options = (0, 2, )
        self._Mode_labels = ('Monitor', 'Detect', )
        self._Mode_tool_bar = Qt.QToolBar(self)
        self._Mode_tool_bar.addWidget(Qt.QLabel('Mode'+": "))
        self._Mode_combo_box = Qt.QComboBox()
        self._Mode_tool_bar.addWidget(self._Mode_combo_box)
        for label in self._Mode_labels: self._Mode_combo_box.addItem(label)
        self._Mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Mode_options.index(i)))
        self._Mode_callback(self.Mode)
        self._Mode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_Mode(self._Mode_options[i]))
        self.top_grid_layout.addWidget(self._Mode_tool_bar, 7, 0, 2, 2)
        for r in range(7, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Gain1_tool_bar = Qt.QToolBar(self)
        self._Gain1_tool_bar.addWidget(Qt.QLabel('Gain1'+": "))
        self._Gain1_line_edit = Qt.QLineEdit(str(self.Gain1))
        self._Gain1_tool_bar.addWidget(self._Gain1_line_edit)
        self._Gain1_line_edit.returnPressed.connect(
        	lambda: self.set_Gain1(eng_notation.str_to_num(str(self._Gain1_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Gain1_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Frequency_tool_bar = Qt.QToolBar(self)
        self._Frequency_tool_bar.addWidget(Qt.QLabel('Freq. (MHz)'+": "))
        self._Frequency_line_edit = Qt.QLineEdit(str(self.Frequency))
        self._Frequency_tool_bar.addWidget(self._Frequency_line_edit)
        self._Frequency_line_edit.returnPressed.connect(
        	lambda: self.set_Frequency(eng_notation.str_to_num(str(self._Frequency_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Frequency_tool_bar, 1, 5, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._EventMode_options = (0, 1, )
        self._EventMode_labels = ('Wait', 'Write', )
        self._EventMode_tool_bar = Qt.QToolBar(self)
        self._EventMode_tool_bar.addWidget(Qt.QLabel('Event Mode'+": "))
        self._EventMode_combo_box = Qt.QComboBox()
        self._EventMode_tool_bar.addWidget(self._EventMode_combo_box)
        for label in self._EventMode_labels: self._EventMode_combo_box.addItem(label)
        self._EventMode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._EventMode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._EventMode_options.index(i)))
        self._EventMode_callback(self.EventMode)
        self._EventMode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_EventMode(self._EventMode_options[i]))
        self.top_grid_layout.addWidget(self._EventMode_tool_bar, 5, 0, 2, 2)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Elevation_tool_bar = Qt.QToolBar(self)
        self._Elevation_tool_bar.addWidget(Qt.QLabel('Elevation'+": "))
        self._Elevation_line_edit = Qt.QLineEdit(str(self.Elevation))
        self._Elevation_tool_bar.addWidget(self._Elevation_line_edit)
        self._Elevation_line_edit.returnPressed.connect(
        	lambda: self.set_Elevation(eng_notation.str_to_num(str(self._Elevation_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Elevation_tool_bar, 0, 6, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Device_tool_bar = Qt.QToolBar(self)
        self._Device_tool_bar.addWidget(Qt.QLabel('Dev'+": "))
        self._Device_line_edit = Qt.QLineEdit(str(self.Device))
        self._Device_tool_bar.addWidget(self._Device_line_edit)
        self._Device_line_edit.returnPressed.connect(
        	lambda: self.set_Device(str(str(self._Device_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Device_tool_bar, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Bandwidth_tool_bar = Qt.QToolBar(self)
        self._Bandwidth_tool_bar.addWidget(Qt.QLabel('Band. (MHz)'+": "))
        self._Bandwidth_line_edit = Qt.QLineEdit(str(self.Bandwidth))
        self._Bandwidth_tool_bar.addWidget(self._Bandwidth_line_edit)
        self._Bandwidth_line_edit.returnPressed.connect(
        	lambda: self.set_Bandwidth(eng_notation.str_to_num(str(self._Bandwidth_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Bandwidth_tool_bar, 1, 6, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Azimuth_tool_bar = Qt.QToolBar(self)
        self._Azimuth_tool_bar.addWidget(Qt.QLabel('Azimuth'+": "))
        self._Azimuth_line_edit = Qt.QLineEdit(str(self.Azimuth))
        self._Azimuth_tool_bar.addWidget(self._Azimuth_line_edit)
        self._Azimuth_line_edit.returnPressed.connect(
        	lambda: self.set_Azimuth(eng_notation.str_to_num(str(self._Azimuth_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._Azimuth_tool_bar, 0, 5, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + Device )
        self.rtlsdr_source_0.set_sample_rate(Bandwidth*1e6)
        self.rtlsdr_source_0.set_center_freq(Frequency*1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(float(Gain1), 0)
        self.rtlsdr_source_0.set_if_gain(12, 0)
        self.rtlsdr_source_0.set_bb_gain(12, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(Bandwidth*1e6, 0)

        (self.rtlsdr_source_0).set_processor_affinity([3])
        self.radio_astro_ra_event_sink_0 = radio_astro.ra_event_sink('WatchDetect.not', fftsize, Frequency, Bandwidth, EventMode, 'Event Detection', 'Glen', Telescope, Device, float(Gain1), Azimuth, Elevation)
        self.radio_astro_detect_0 = radio_astro.detect(fftsize, nsigma, Frequency, Bandwidth, fftsize*1.e-6/Bandwidth, Mode)
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 3, 10, 5)
        for r in range(2, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
        	fftsize,
        	100,
                -.5,
                .5,
        	"",
        	2
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1)
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
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win)
        self._observer_tool_bar = Qt.QToolBar(self)
        self._observer_tool_bar.addWidget(Qt.QLabel('Who'+": "))
        self._observer_line_edit = Qt.QLineEdit(str(self.observer))
        self._observer_tool_bar.addWidget(self._observer_line_edit)
        self._observer_line_edit.returnPressed.connect(
        	lambda: self.set_observer(str(str(self._observer_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._observer_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_histogram_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.radio_astro_detect_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_sink_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfDetect30rtlsdr")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_observer(self):
        return self.observer

    def set_observer(self, observer):
        self.observer = observer
        Qt.QMetaObject.invokeMethod(self._observer_line_edit, "setText", Qt.Q_ARG("QString", str(self.observer)))

    def get_nsigma(self):
        return self.nsigma

    def set_nsigma(self, nsigma):
        self.nsigma = nsigma
        self.radio_astro_detect_0.set_dms( self.nsigma)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        Qt.QMetaObject.invokeMethod(self._fftsize_line_edit, "setText", Qt.Q_ARG("QString", str(self.fftsize)))
        self.radio_astro_ra_event_sink_0.set_vlen( self.fftsize)
        self.radio_astro_detect_0.set_vlen( self.fftsize)

    def get_Telescope(self):
        return self.Telescope

    def set_Telescope(self, Telescope):
        self.Telescope = Telescope
        Qt.QMetaObject.invokeMethod(self._Telescope_line_edit, "setText", Qt.Q_ARG("QString", str(self.Telescope)))
        self.radio_astro_ra_event_sink_0.set_telescope( self.Telescope)

    def get_Mode(self):
        return self.Mode

    def set_Mode(self, Mode):
        self.Mode = Mode
        self._Mode_callback(self.Mode)
        self.radio_astro_detect_0.set_mode( self.Mode)

    def get_Gain1(self):
        return self.Gain1

    def set_Gain1(self, Gain1):
        self.Gain1 = Gain1
        Qt.QMetaObject.invokeMethod(self._Gain1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Gain1)))
        self.rtlsdr_source_0.set_gain(float(self.Gain1), 0)

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        Qt.QMetaObject.invokeMethod(self._Frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Frequency)))
        self.rtlsdr_source_0.set_center_freq(self.Frequency*1e6, 0)
        self.radio_astro_ra_event_sink_0.set_frequency( self.Frequency)
        self.radio_astro_detect_0.set_f_obs( self.Frequency)

    def get_EventMode(self):
        return self.EventMode

    def set_EventMode(self, EventMode):
        self.EventMode = EventMode
        self._EventMode_callback(self.EventMode)
        self.radio_astro_ra_event_sink_0.set_record( self.EventMode)

    def get_Elevation(self):
        return self.Elevation

    def set_Elevation(self, Elevation):
        self.Elevation = Elevation
        Qt.QMetaObject.invokeMethod(self._Elevation_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Elevation)))
        self.radio_astro_ra_event_sink_0.set_telel( self.Elevation)

    def get_Device(self):
        return self.Device

    def set_Device(self, Device):
        self.Device = Device
        Qt.QMetaObject.invokeMethod(self._Device_line_edit, "setText", Qt.Q_ARG("QString", str(self.Device)))
        self.radio_astro_ra_event_sink_0.set_device( self.Device)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        Qt.QMetaObject.invokeMethod(self._Bandwidth_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Bandwidth)))
        self.rtlsdr_source_0.set_sample_rate(self.Bandwidth*1e6)
        self.rtlsdr_source_0.set_bandwidth(self.Bandwidth*1e6, 0)
        self.radio_astro_ra_event_sink_0.set_sample_rate( self.Bandwidth)
        self.radio_astro_detect_0.set_bw( self.Bandwidth)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.Bandwidth)

    def get_Azimuth(self):
        return self.Azimuth

    def set_Azimuth(self, Azimuth):
        self.Azimuth = Azimuth
        Qt.QMetaObject.invokeMethod(self._Azimuth_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Azimuth)))
        self.radio_astro_ra_event_sink_0.set_telaz( self.Azimuth)


def main(top_block_cls=NsfDetect30rtlsdr, options=None):

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
