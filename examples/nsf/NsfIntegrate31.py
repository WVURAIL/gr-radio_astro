#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NsfIntegrate: Average+Record Obs.
# Author: Glen Langston
# Description: PlutoSDR Dongle at maximum rate without dropping samples
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
from PyQt5.QtCore import QObject, pyqtSlot
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
from gnuradio import soapy
import configparser



from gnuradio import qtgui

class NsfIntegrate31(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NsfIntegrate: Average+Record Obs.", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NsfIntegrate: Average+Record Obs.")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfIntegrate31")

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
        self.ObsName = ObsName = "Integrate31"
        self.ConfigFile = ConfigFile = ObsName+".conf"
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(ConfigFile)
        try: Frequencys = self._Frequencys_config.getfloat('main', 'Frequency')
        except: Frequencys = 1420.4e6
        self.Frequencys = Frequencys
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(ConfigFile)
        try: Bandwidths = self._Bandwidths_config.getfloat('main', 'Bandwidth')
        except: Bandwidths = 6.e6
        self.Bandwidths = Bandwidths
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(ConfigFile)
        try: fftsize_save = self._fftsize_save_config.getint('main', 'fftsize')
        except: fftsize_save = 1024
        self.fftsize_save = fftsize_save
        self.Frequency = Frequency = Frequencys
        self.Bandwidth = Bandwidth = Bandwidths
        self._xaxis_save_config = configparser.ConfigParser()
        self._xaxis_save_config.read(ConfigFile)
        try: xaxis_save = self._xaxis_save_config.getint('main', 'Xaxis')
        except: xaxis_save = 0
        self.xaxis_save = xaxis_save
        self._telescope_save_config = configparser.ConfigParser()
        self._telescope_save_config.read(ConfigFile)
        try: telescope_save = self._telescope_save_config.get('main', 'telescope')
        except: telescope_save = 'Bubble Wrap Horn'
        self.telescope_save = telescope_save
        self._observers_save_config = configparser.ConfigParser()
        self._observers_save_config.read(ConfigFile)
        try: observers_save = self._observers_save_config.get('main', 'observers')
        except: observers_save = 'Science Aficionado'
        self.observers_save = observers_save
        self.numin = numin = (Frequency - (Bandwidth/2.))
        self._nAves_config = configparser.ConfigParser()
        self._nAves_config.read(ConfigFile)
        try: nAves = self._nAves_config.getint('main', 'nave')
        except: nAves = 20
        self.nAves = nAves
        self.fftsize = fftsize = fftsize_save
        self.H1 = H1 = 1420.406E6
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(ConfigFile)
        try: Gain1s = self._Gain1s_config.getfloat('main', 'gain1')
        except: Gain1s = 49.
        self.Gain1s = Gain1s
        self._Elevation_save_config = configparser.ConfigParser()
        self._Elevation_save_config.read(ConfigFile)
        try: Elevation_save = self._Elevation_save_config.getfloat('main', 'elevation')
        except: Elevation_save = 90.
        self.Elevation_save = Elevation_save
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(ConfigFile)
        try: Azimuth_save = self._Azimuth_save_config.getfloat('main', 'azimuth')
        except: Azimuth_save = 90.
        self.Azimuth_save = Azimuth_save
        self.yunits = yunits = ["Counts", "Power (dB)", "Intensity (Kelvins)", "Intensity(K)"]
        self.ymins = ymins = [ 0.01,  -20,  90.,-.5]
        self.ymaxs = ymaxs = [5, 10., 200., 50.]
        self.xsteps = xsteps = [Bandwidth*1.E-6/fftsize, -Bandwidth*3.E5/(H1*fftsize), 1]
        self.xmins = xmins = [numin*1E-6, (H1 - numin)*(3E5/H1), 0 ]
        self._xaxis_save_0_config = configparser.ConfigParser()
        self._xaxis_save_0_config.read(ConfigFile)
        try: xaxis_save_0 = self._xaxis_save_0_config.getint('main', 'Xaxis')
        except: xaxis_save_0 = 0
        self.xaxis_save_0 = xaxis_save_0
        self.units = units = 0
        self.samp_rate = samp_rate = int(Bandwidth)
        self.obstype = obstype = 0
        self.observer = observer = observers_save
        self.nAve = nAve = nAves
        self._device_save_config = configparser.ConfigParser()
        self._device_save_config.read(ConfigFile)
        try: device_save = self._device_save_config.get('main', 'device')
        except: device_save = 'airspy,bias=1,pack=1'
        self.device_save = device_save
        self.Xaxis = Xaxis = xaxis_save
        self.Telescope = Telescope = telescope_save
        self.Record = Record = 1
        self.Gain2 = Gain2 = 12.
        self.Gain1 = Gain1 = Gain1s
        self.Elevation = Elevation = Elevation_save
        self.Device = Device = "ip:pluto.local"
        self.Azimuth = Azimuth = Azimuth_save

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._units_options = [0, 1, 2, 3]
        # Create the labels list
        self._units_labels = ['Counts', 'dB', 'Kelvins', 'K - Fit']
        # Create the combo box
        # Create the radio buttons
        self._units_group_box = Qt.QGroupBox("Units" + ": ")
        self._units_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._units_button_group = variable_chooser_button_group()
        self._units_group_box.setLayout(self._units_box)
        for i, _label in enumerate(self._units_labels):
            radio_button = Qt.QRadioButton(_label)
            self._units_box.addWidget(radio_button)
            self._units_button_group.addButton(radio_button, i)
        self._units_callback = lambda i: Qt.QMetaObject.invokeMethod(self._units_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._units_options.index(i)))
        self._units_callback(self.units)
        self._units_button_group.buttonClicked[int].connect(
            lambda i: self.set_units(self._units_options[i]))
        self.top_grid_layout.addWidget(self._units_group_box, 6, 0, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._obstype_options = [0, 1, 3]
        # Create the labels list
        self._obstype_labels = ['Survey', 'Hot/Cold', 'Ref']
        # Create the combo box
        # Create the radio buttons
        self._obstype_group_box = Qt.QGroupBox("Obs:" + ": ")
        self._obstype_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._obstype_button_group = variable_chooser_button_group()
        self._obstype_group_box.setLayout(self._obstype_box)
        for i, _label in enumerate(self._obstype_labels):
            radio_button = Qt.QRadioButton(_label)
            self._obstype_box.addWidget(radio_button)
            self._obstype_button_group.addButton(radio_button, i)
        self._obstype_callback = lambda i: Qt.QMetaObject.invokeMethod(self._obstype_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._obstype_options.index(i)))
        self._obstype_callback(self.obstype)
        self._obstype_button_group.buttonClicked[int].connect(
            lambda i: self.set_obstype(self._obstype_options[i]))
        self.top_grid_layout.addWidget(self._obstype_group_box, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._observer_tool_bar = Qt.QToolBar(self)
        self._observer_tool_bar.addWidget(Qt.QLabel("Who" + ": "))
        self._observer_line_edit = Qt.QLineEdit(str(self.observer))
        self._observer_tool_bar.addWidget(self._observer_line_edit)
        self._observer_line_edit.returnPressed.connect(
            lambda: self.set_observer(str(str(self._observer_line_edit.text()))))
        self.top_grid_layout.addWidget(self._observer_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._nAve_tool_bar = Qt.QToolBar(self)
        self._nAve_tool_bar.addWidget(Qt.QLabel("N_Ave." + ": "))
        self._nAve_line_edit = Qt.QLineEdit(str(self.nAve))
        self._nAve_tool_bar.addWidget(self._nAve_line_edit)
        self._nAve_line_edit.returnPressed.connect(
            lambda: self.set_nAve(int(str(self._nAve_line_edit.text()))))
        self.top_grid_layout.addWidget(self._nAve_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fftsize_tool_bar = Qt.QToolBar(self)
        self._fftsize_tool_bar.addWidget(Qt.QLabel("FFT_size" + ": "))
        self._fftsize_line_edit = Qt.QLineEdit(str(self.fftsize))
        self._fftsize_tool_bar.addWidget(self._fftsize_line_edit)
        self._fftsize_line_edit.returnPressed.connect(
            lambda: self.set_fftsize(int(str(self._fftsize_line_edit.text()))))
        self.top_grid_layout.addWidget(self._fftsize_tool_bar, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._Xaxis_options = [0, 1, 2]
        # Create the labels list
        self._Xaxis_labels = ['Frequency (MHz)', 'Velocity (km/sec)', 'Channels']
        # Create the combo box
        self._Xaxis_tool_bar = Qt.QToolBar(self)
        self._Xaxis_tool_bar.addWidget(Qt.QLabel("Xaxis" + ": "))
        self._Xaxis_combo_box = Qt.QComboBox()
        self._Xaxis_tool_bar.addWidget(self._Xaxis_combo_box)
        for _label in self._Xaxis_labels: self._Xaxis_combo_box.addItem(_label)
        self._Xaxis_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Xaxis_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Xaxis_options.index(i)))
        self._Xaxis_callback(self.Xaxis)
        self._Xaxis_combo_box.currentIndexChanged.connect(
            lambda i: self.set_Xaxis(self._Xaxis_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._Xaxis_tool_bar, 6, 3, 1, 3)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._Record_options = [0, 1, 2]
        # Create the labels list
        self._Record_labels = ['! ! Wait ! !', 'AVERAGE', 'Save']
        # Create the combo box
        # Create the radio buttons
        self._Record_group_box = Qt.QGroupBox("Rec:" + ": ")
        self._Record_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._Record_button_group = variable_chooser_button_group()
        self._Record_group_box.setLayout(self._Record_box)
        for i, _label in enumerate(self._Record_labels):
            radio_button = Qt.QRadioButton(_label)
            self._Record_box.addWidget(radio_button)
            self._Record_button_group.addButton(radio_button, i)
        self._Record_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Record_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._Record_options.index(i)))
        self._Record_callback(self.Record)
        self._Record_button_group.buttonClicked[int].connect(
            lambda i: self.set_Record(self._Record_options[i]))
        self.top_grid_layout.addWidget(self._Record_group_box, 4, 0, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Gain1_tool_bar = Qt.QToolBar(self)
        self._Gain1_tool_bar.addWidget(Qt.QLabel("Gain1" + ": "))
        self._Gain1_line_edit = Qt.QLineEdit(str(self.Gain1))
        self._Gain1_tool_bar.addWidget(self._Gain1_line_edit)
        self._Gain1_line_edit.returnPressed.connect(
            lambda: self.set_Gain1(eng_notation.str_to_num(str(self._Gain1_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Gain1_tool_bar, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Frequency_tool_bar = Qt.QToolBar(self)
        self._Frequency_tool_bar.addWidget(Qt.QLabel("Freq. Hz" + ": "))
        self._Frequency_line_edit = Qt.QLineEdit(str(self.Frequency))
        self._Frequency_tool_bar.addWidget(self._Frequency_line_edit)
        self._Frequency_line_edit.returnPressed.connect(
            lambda: self.set_Frequency(eng_notation.str_to_num(str(self._Frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Frequency_tool_bar, 0, 4, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Elevation_tool_bar = Qt.QToolBar(self)
        self._Elevation_tool_bar.addWidget(Qt.QLabel("Elevation" + ": "))
        self._Elevation_line_edit = Qt.QLineEdit(str(self.Elevation))
        self._Elevation_tool_bar.addWidget(self._Elevation_line_edit)
        self._Elevation_line_edit.returnPressed.connect(
            lambda: self.set_Elevation(eng_notation.str_to_num(str(self._Elevation_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Elevation_tool_bar, 1, 6, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Bandwidth_tool_bar = Qt.QToolBar(self)
        self._Bandwidth_tool_bar.addWidget(Qt.QLabel("Bandwidth" + ": "))
        self._Bandwidth_line_edit = Qt.QLineEdit(str(self.Bandwidth))
        self._Bandwidth_tool_bar.addWidget(self._Bandwidth_line_edit)
        self._Bandwidth_line_edit.returnPressed.connect(
            lambda: self.set_Bandwidth(eng_notation.str_to_num(str(self._Bandwidth_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Bandwidth_tool_bar, 1, 4, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Azimuth_tool_bar = Qt.QToolBar(self)
        self._Azimuth_tool_bar.addWidget(Qt.QLabel("Azimuth" + ": "))
        self._Azimuth_line_edit = Qt.QLineEdit(str(self.Azimuth))
        self._Azimuth_tool_bar.addWidget(self._Azimuth_line_edit)
        self._Azimuth_line_edit.returnPressed.connect(
            lambda: self.set_Azimuth(eng_notation.str_to_num(str(self._Azimuth_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Azimuth_tool_bar, 0, 6, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_plutosdr_source_0 = None
        dev = 'driver=plutosdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_plutosdr_source_0 = soapy.source(dev, "fc32", 1, Device,
                                  stream_args, tune_args, settings)
        self.soapy_plutosdr_source_0.set_sample_rate(0, Bandwidth)
        self.soapy_plutosdr_source_0.set_bandwidth(0, 5e6)
        self.soapy_plutosdr_source_0.set_gain_mode(0, False)
        self.soapy_plutosdr_source_0.set_frequency(0, Frequency)
        self.soapy_plutosdr_source_0.set_gain(0, min(max(Gain1, 0.0), 73.0))
        self.radio_astro_ra_vmedian_0_1_0 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_vmedian_0_1 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_vmedian_0_0 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_vmedian_0 = radio_astro.ra_vmedian(fftsize, 4)
        self.radio_astro_ra_integrate_1 = radio_astro.ra_integrate(ObsName+".not", observers_save, fftsize, Frequencys, Bandwidths, Azimuth, Elevation, Record, obstype, 4**4, units, 295., 10.)
        self.radio_astro_ra_ascii_sink_0 = radio_astro.ra_ascii_sink(ObsName+".not", observer, fftsize, Frequencys, Bandwidths, Azimuth, Elevation, Record, obstype, 4**4, nAve, telescope_save, device_save, float(Gain1), float(Gain2), float(Gain2))
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            fftsize,
            xmins[Xaxis],
            xsteps[Xaxis],
            "",
            'Intensity',
            "",
            5, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(1)
        self.qtgui_vector_sink_f_0_0.set_y_axis(ymins[units], ymaxs[units])
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0.5*(ymins[units] + ymaxs[units]))

        labels = ['Latest', 'Median', 'Hot', 'Cold', 'Ref',
            '', '', '', '', '']
        widths = [1, 3, 2, 2, 3,
            1, 1, 1, 1, 1]
        colors = ["yellow", "dark green", "red", "blue", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [2., 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(5):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win, 2, 2, 4, 5)
        for r in range(2, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(1.)
        self.qtgui_number_sink_0.set_title("")

        labels = ['T Remains:', '', '', '', '',
            '', '', '', '', '']
        units = ['(s)', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0.)
            self.qtgui_number_sink_0.set_max(i, nAve * fftsize * 1024. / Bandwidth)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 6, 6, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            fftsize,
            100,
            -.5,
            .5,
            "",
            2,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(2)
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
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.hamming(fftsize), True, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fftsize)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self._Telescope_tool_bar = Qt.QToolBar(self)
        self._Telescope_tool_bar.addWidget(Qt.QLabel("Tel" + ": "))
        self._Telescope_line_edit = Qt.QLineEdit(str(self.Telescope))
        self._Telescope_tool_bar.addWidget(self._Telescope_line_edit)
        self._Telescope_line_edit.returnPressed.connect(
            lambda: self.set_Telescope(str(str(self._Telescope_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Telescope_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_histogram_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.radio_astro_ra_vmedian_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radio_astro_ra_ascii_sink_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.radio_astro_ra_integrate_1, 4), (self.qtgui_vector_sink_f_0_0, 4))
        self.connect((self.radio_astro_ra_integrate_1, 2), (self.qtgui_vector_sink_f_0_0, 2))
        self.connect((self.radio_astro_ra_integrate_1, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.radio_astro_ra_integrate_1, 1), (self.qtgui_vector_sink_f_0_0, 1))
        self.connect((self.radio_astro_ra_integrate_1, 3), (self.qtgui_vector_sink_f_0_0, 3))
        self.connect((self.radio_astro_ra_vmedian_0, 0), (self.radio_astro_ra_vmedian_0_0, 0))
        self.connect((self.radio_astro_ra_vmedian_0_0, 0), (self.radio_astro_ra_vmedian_0_1, 0))
        self.connect((self.radio_astro_ra_vmedian_0_1, 0), (self.radio_astro_ra_vmedian_0_1_0, 0))
        self.connect((self.radio_astro_ra_vmedian_0_1_0, 0), (self.radio_astro_ra_ascii_sink_0, 0))
        self.connect((self.radio_astro_ra_vmedian_0_1_0, 0), (self.radio_astro_ra_integrate_1, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_stream_to_vector_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfIntegrate31")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_ObsName(self):
        return self.ObsName

    def set_ObsName(self, ObsName):
        self.ObsName = ObsName
        self.set_ConfigFile(self.ObsName+".conf")
        self.radio_astro_ra_ascii_sink_0.set_setup(self.ObsName+".not")
        self.radio_astro_ra_integrate_1.set_setup(self.ObsName+".not")

    def get_ConfigFile(self):
        return self.ConfigFile

    def set_ConfigFile(self, ConfigFile):
        self.ConfigFile = ConfigFile
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(self.ConfigFile)
        if not self._Azimuth_save_config.has_section('main'):
        	self._Azimuth_save_config.add_section('main')
        self._Azimuth_save_config.set('main', 'azimuth', str(self.Azimuth))
        self._Azimuth_save_config.write(open(self.ConfigFile, 'w'))
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(self.ConfigFile)
        if not self._Bandwidths_config.has_section('main'):
        	self._Bandwidths_config.add_section('main')
        self._Bandwidths_config.set('main', 'Bandwidth', str(self.Bandwidth))
        self._Bandwidths_config.write(open(self.ConfigFile, 'w'))
        self._Elevation_save_config = configparser.ConfigParser()
        self._Elevation_save_config.read(self.ConfigFile)
        if not self._Elevation_save_config.has_section('main'):
        	self._Elevation_save_config.add_section('main')
        self._Elevation_save_config.set('main', 'elevation', str(self.Elevation))
        self._Elevation_save_config.write(open(self.ConfigFile, 'w'))
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(self.ConfigFile)
        if not self._Frequencys_config.has_section('main'):
        	self._Frequencys_config.add_section('main')
        self._Frequencys_config.set('main', 'Frequency', str(self.Frequency))
        self._Frequencys_config.write(open(self.ConfigFile, 'w'))
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(self.ConfigFile)
        if not self._Gain1s_config.has_section('main'):
        	self._Gain1s_config.add_section('main')
        self._Gain1s_config.set('main', 'gain1', str(self.Gain1))
        self._Gain1s_config.write(open(self.ConfigFile, 'w'))
        self._device_save_config = configparser.ConfigParser()
        self._device_save_config.read(self.ConfigFile)
        if not self._device_save_config.has_section('main'):
        	self._device_save_config.add_section('main')
        self._device_save_config.set('main', 'device', str(self.Device))
        self._device_save_config.write(open(self.ConfigFile, 'w'))
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(self.ConfigFile)
        if not self._fftsize_save_config.has_section('main'):
        	self._fftsize_save_config.add_section('main')
        self._fftsize_save_config.set('main', 'fftsize', str(self.fftsize))
        self._fftsize_save_config.write(open(self.ConfigFile, 'w'))
        self._nAves_config = configparser.ConfigParser()
        self._nAves_config.read(self.ConfigFile)
        if not self._nAves_config.has_section('main'):
        	self._nAves_config.add_section('main')
        self._nAves_config.set('main', 'nave', str(self.nAve))
        self._nAves_config.write(open(self.ConfigFile, 'w'))
        self._observers_save_config = configparser.ConfigParser()
        self._observers_save_config.read(self.ConfigFile)
        if not self._observers_save_config.has_section('main'):
        	self._observers_save_config.add_section('main')
        self._observers_save_config.set('main', 'observers', str(self.observer))
        self._observers_save_config.write(open(self.ConfigFile, 'w'))
        self._telescope_save_config = configparser.ConfigParser()
        self._telescope_save_config.read(self.ConfigFile)
        if not self._telescope_save_config.has_section('main'):
        	self._telescope_save_config.add_section('main')
        self._telescope_save_config.set('main', 'telescope', str(self.Telescope))
        self._telescope_save_config.write(open(self.ConfigFile, 'w'))
        self._xaxis_save_config = configparser.ConfigParser()
        self._xaxis_save_config.read(self.ConfigFile)
        if not self._xaxis_save_config.has_section('main'):
        	self._xaxis_save_config.add_section('main')
        self._xaxis_save_config.set('main', 'Xaxis', str(self.Xaxis))
        self._xaxis_save_config.write(open(self.ConfigFile, 'w'))
        self._xaxis_save_0_config = configparser.ConfigParser()
        self._xaxis_save_0_config.read(self.ConfigFile)
        if not self._xaxis_save_0_config.has_section('main'):
        	self._xaxis_save_0_config.add_section('main')
        self._xaxis_save_0_config.set('main', 'Xaxis', str(self.Xaxis))
        self._xaxis_save_0_config.write(open(self.ConfigFile, 'w'))

    def get_Frequencys(self):
        return self.Frequencys

    def set_Frequencys(self, Frequencys):
        self.Frequencys = Frequencys
        self.set_Frequency(self.Frequencys)
        self.radio_astro_ra_ascii_sink_0.set_frequency(self.Frequencys)
        self.radio_astro_ra_integrate_1.set_frequency(self.Frequencys)

    def get_Bandwidths(self):
        return self.Bandwidths

    def set_Bandwidths(self, Bandwidths):
        self.Bandwidths = Bandwidths
        self.set_Bandwidth(self.Bandwidths)
        self.radio_astro_ra_ascii_sink_0.set_bandwidth(self.Bandwidths)
        self.radio_astro_ra_integrate_1.set_bandwidth(self.Bandwidths)

    def get_fftsize_save(self):
        return self.fftsize_save

    def set_fftsize_save(self, fftsize_save):
        self.fftsize_save = fftsize_save
        self.set_fftsize(self.fftsize_save)

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        Qt.QMetaObject.invokeMethod(self._Frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Frequency)))
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(self.ConfigFile)
        if not self._Frequencys_config.has_section('main'):
        	self._Frequencys_config.add_section('main')
        self._Frequencys_config.set('main', 'Frequency', str(self.Frequency))
        self._Frequencys_config.write(open(self.ConfigFile, 'w'))
        self.set_numin((self.Frequency - (self.Bandwidth/2.)))
        self.soapy_plutosdr_source_0.set_frequency(0, self.Frequency)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        Qt.QMetaObject.invokeMethod(self._Bandwidth_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Bandwidth)))
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(self.ConfigFile)
        if not self._Bandwidths_config.has_section('main'):
        	self._Bandwidths_config.add_section('main')
        self._Bandwidths_config.set('main', 'Bandwidth', str(self.Bandwidth))
        self._Bandwidths_config.write(open(self.ConfigFile, 'w'))
        self.set_numin((self.Frequency - (self.Bandwidth/2.)))
        self.set_samp_rate(int(self.Bandwidth))
        self.set_xsteps([self.Bandwidth*1.E-6/self.fftsize, -self.Bandwidth*3.E5/(self.H1*self.fftsize), 1])
        self.soapy_plutosdr_source_0.set_sample_rate(0, self.Bandwidth)

    def get_xaxis_save(self):
        return self.xaxis_save

    def set_xaxis_save(self, xaxis_save):
        self.xaxis_save = xaxis_save
        self.set_Xaxis(self.xaxis_save)

    def get_telescope_save(self):
        return self.telescope_save

    def set_telescope_save(self, telescope_save):
        self.telescope_save = telescope_save
        self.set_Telescope(self.telescope_save)
        self.radio_astro_ra_ascii_sink_0.set_site(self.telescope_save)

    def get_observers_save(self):
        return self.observers_save

    def set_observers_save(self, observers_save):
        self.observers_save = observers_save
        self.set_observer(self.observers_save)
        self.radio_astro_ra_integrate_1.set_observers(self.observers_save)

    def get_numin(self):
        return self.numin

    def set_numin(self, numin):
        self.numin = numin
        self.set_xmins([self.numin*1E-6, (self.H1 - self.numin)*(3E5/self.H1), 0 ])

    def get_nAves(self):
        return self.nAves

    def set_nAves(self, nAves):
        self.nAves = nAves
        self.set_nAve(self.nAves)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        Qt.QMetaObject.invokeMethod(self._fftsize_line_edit, "setText", Qt.Q_ARG("QString", str(self.fftsize)))
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(self.ConfigFile)
        if not self._fftsize_save_config.has_section('main'):
        	self._fftsize_save_config.add_section('main')
        self._fftsize_save_config.set('main', 'fftsize', str(self.fftsize))
        self._fftsize_save_config.write(open(self.ConfigFile, 'w'))
        self.set_xsteps([self.Bandwidth*1.E-6/self.fftsize, -self.Bandwidth*3.E5/(self.H1*self.fftsize), 1])

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1
        self.set_xmins([self.numin*1E-6, (self.H1 - self.numin)*(3E5/self.H1), 0 ])
        self.set_xsteps([self.Bandwidth*1.E-6/self.fftsize, -self.Bandwidth*3.E5/(self.H1*self.fftsize), 1])

    def get_Gain1s(self):
        return self.Gain1s

    def set_Gain1s(self, Gain1s):
        self.Gain1s = Gain1s
        self.set_Gain1(self.Gain1s)

    def get_Elevation_save(self):
        return self.Elevation_save

    def set_Elevation_save(self, Elevation_save):
        self.Elevation_save = Elevation_save
        self.set_Elevation(self.Elevation_save)

    def get_Azimuth_save(self):
        return self.Azimuth_save

    def set_Azimuth_save(self, Azimuth_save):
        self.Azimuth_save = Azimuth_save
        self.set_Azimuth(self.Azimuth_save)

    def get_yunits(self):
        return self.yunits

    def set_yunits(self, yunits):
        self.yunits = yunits

    def get_ymins(self):
        return self.ymins

    def set_ymins(self, ymins):
        self.ymins = ymins
        self.qtgui_vector_sink_f_0_0.set_y_axis(self.ymins[self.units], self.ymaxs[self.units])
        self.qtgui_vector_sink_f_0_0.set_ref_level(0.5*(self.ymins[self.units] + self.ymaxs[self.units]))

    def get_ymaxs(self):
        return self.ymaxs

    def set_ymaxs(self, ymaxs):
        self.ymaxs = ymaxs
        self.qtgui_vector_sink_f_0_0.set_y_axis(self.ymins[self.units], self.ymaxs[self.units])
        self.qtgui_vector_sink_f_0_0.set_ref_level(0.5*(self.ymins[self.units] + self.ymaxs[self.units]))

    def get_xsteps(self):
        return self.xsteps

    def set_xsteps(self, xsteps):
        self.xsteps = xsteps
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.xmins[self.Xaxis], self.xsteps[self.Xaxis])

    def get_xmins(self):
        return self.xmins

    def set_xmins(self, xmins):
        self.xmins = xmins
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.xmins[self.Xaxis], self.xsteps[self.Xaxis])

    def get_xaxis_save_0(self):
        return self.xaxis_save_0

    def set_xaxis_save_0(self, xaxis_save_0):
        self.xaxis_save_0 = xaxis_save_0

    def get_units(self):
        return self.units

    def set_units(self, units):
        self.units = units
        self._units_callback(self.units)
        self.qtgui_vector_sink_f_0_0.set_y_axis(self.ymins[self.units], self.ymaxs[self.units])
        self.qtgui_vector_sink_f_0_0.set_ref_level(0.5*(self.ymins[self.units] + self.ymaxs[self.units]))
        self.radio_astro_ra_integrate_1.set_units(self.units)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_obstype(self):
        return self.obstype

    def set_obstype(self, obstype):
        self.obstype = obstype
        self._obstype_callback(self.obstype)
        self.radio_astro_ra_ascii_sink_0.set_obstype(self.obstype)
        self.radio_astro_ra_integrate_1.set_obstype(self.obstype)

    def get_observer(self):
        return self.observer

    def set_observer(self, observer):
        self.observer = observer
        Qt.QMetaObject.invokeMethod(self._observer_line_edit, "setText", Qt.Q_ARG("QString", str(self.observer)))
        self._observers_save_config = configparser.ConfigParser()
        self._observers_save_config.read(self.ConfigFile)
        if not self._observers_save_config.has_section('main'):
        	self._observers_save_config.add_section('main')
        self._observers_save_config.set('main', 'observers', str(self.observer))
        self._observers_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_observers(self.observer)

    def get_nAve(self):
        return self.nAve

    def set_nAve(self, nAve):
        self.nAve = nAve
        Qt.QMetaObject.invokeMethod(self._nAve_line_edit, "setText", Qt.Q_ARG("QString", str(self.nAve)))
        self._nAves_config = configparser.ConfigParser()
        self._nAves_config.read(self.ConfigFile)
        if not self._nAves_config.has_section('main'):
        	self._nAves_config.add_section('main')
        self._nAves_config.set('main', 'nave', str(self.nAve))
        self._nAves_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_nave(self.nAve)

    def get_device_save(self):
        return self.device_save

    def set_device_save(self, device_save):
        self.device_save = device_save
        self.radio_astro_ra_ascii_sink_0.set_device(self.device_save)

    def get_Xaxis(self):
        return self.Xaxis

    def set_Xaxis(self, Xaxis):
        self.Xaxis = Xaxis
        self._Xaxis_callback(self.Xaxis)
        self._xaxis_save_config = configparser.ConfigParser()
        self._xaxis_save_config.read(self.ConfigFile)
        if not self._xaxis_save_config.has_section('main'):
        	self._xaxis_save_config.add_section('main')
        self._xaxis_save_config.set('main', 'Xaxis', str(self.Xaxis))
        self._xaxis_save_config.write(open(self.ConfigFile, 'w'))
        self._xaxis_save_0_config = configparser.ConfigParser()
        self._xaxis_save_0_config.read(self.ConfigFile)
        if not self._xaxis_save_0_config.has_section('main'):
        	self._xaxis_save_0_config.add_section('main')
        self._xaxis_save_0_config.set('main', 'Xaxis', str(self.Xaxis))
        self._xaxis_save_0_config.write(open(self.ConfigFile, 'w'))
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.xmins[self.Xaxis], self.xsteps[self.Xaxis])

    def get_Telescope(self):
        return self.Telescope

    def set_Telescope(self, Telescope):
        self.Telescope = Telescope
        Qt.QMetaObject.invokeMethod(self._Telescope_line_edit, "setText", Qt.Q_ARG("QString", str(self.Telescope)))
        self._telescope_save_config = configparser.ConfigParser()
        self._telescope_save_config.read(self.ConfigFile)
        if not self._telescope_save_config.has_section('main'):
        	self._telescope_save_config.add_section('main')
        self._telescope_save_config.set('main', 'telescope', str(self.Telescope))
        self._telescope_save_config.write(open(self.ConfigFile, 'w'))

    def get_Record(self):
        return self.Record

    def set_Record(self, Record):
        self.Record = Record
        self._Record_callback(self.Record)
        self.radio_astro_ra_ascii_sink_0.set_record(self.Record)
        self.radio_astro_ra_integrate_1.set_inttype(self.Record)

    def get_Gain2(self):
        return self.Gain2

    def set_Gain2(self, Gain2):
        self.Gain2 = Gain2
        self.radio_astro_ra_ascii_sink_0.set_gain2(float(self.Gain2))
        self.radio_astro_ra_ascii_sink_0.set_gain3(float(self.Gain2))

    def get_Gain1(self):
        return self.Gain1

    def set_Gain1(self, Gain1):
        self.Gain1 = Gain1
        Qt.QMetaObject.invokeMethod(self._Gain1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Gain1)))
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(self.ConfigFile)
        if not self._Gain1s_config.has_section('main'):
        	self._Gain1s_config.add_section('main')
        self._Gain1s_config.set('main', 'gain1', str(self.Gain1))
        self._Gain1s_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_gain1(float(self.Gain1))
        self.soapy_plutosdr_source_0.set_gain(0, min(max(self.Gain1, 0.0), 73.0))

    def get_Elevation(self):
        return self.Elevation

    def set_Elevation(self, Elevation):
        self.Elevation = Elevation
        Qt.QMetaObject.invokeMethod(self._Elevation_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Elevation)))
        self._Elevation_save_config = configparser.ConfigParser()
        self._Elevation_save_config.read(self.ConfigFile)
        if not self._Elevation_save_config.has_section('main'):
        	self._Elevation_save_config.add_section('main')
        self._Elevation_save_config.set('main', 'elevation', str(self.Elevation))
        self._Elevation_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_elevation(self.Elevation)
        self.radio_astro_ra_integrate_1.set_elevation(self.Elevation)

    def get_Device(self):
        return self.Device

    def set_Device(self, Device):
        self.Device = Device
        self._device_save_config = configparser.ConfigParser()
        self._device_save_config.read(self.ConfigFile)
        if not self._device_save_config.has_section('main'):
        	self._device_save_config.add_section('main')
        self._device_save_config.set('main', 'device', str(self.Device))
        self._device_save_config.write(open(self.ConfigFile, 'w'))

    def get_Azimuth(self):
        return self.Azimuth

    def set_Azimuth(self, Azimuth):
        self.Azimuth = Azimuth
        Qt.QMetaObject.invokeMethod(self._Azimuth_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Azimuth)))
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(self.ConfigFile)
        if not self._Azimuth_save_config.has_section('main'):
        	self._Azimuth_save_config.add_section('main')
        self._Azimuth_save_config.set('main', 'azimuth', str(self.Azimuth))
        self._Azimuth_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_azimuth(self.Azimuth)
        self.radio_astro_ra_integrate_1.set_azimuth(self.Azimuth)




def main(top_block_cls=NsfIntegrate31, options=None):

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
