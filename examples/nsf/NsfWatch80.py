#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NSF Watch 8MHz SDRPlay
# Author: Glen Langston
# Description: SDRPlay RSP1A, 8 MHz samples
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

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
from gnuradio import sdrplay3
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import configparser



from gnuradio import qtgui

class NsfWatch80(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NSF Watch 8MHz SDRPlay", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NSF Watch 8MHz SDRPlay")
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

        self.settings = Qt.QSettings("GNU Radio", "NsfWatch80")

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
        self.ObsName = ObsName = "Integrate80"
        self.ConfigFile = ConfigFile = ObsName+".conf"
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(ConfigFile)
        try: Frequencys = self._Frequencys_config.getfloat('main', 'Frequency')
        except: Frequencys = 1420.4e6
        self.Frequencys = Frequencys
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(ConfigFile)
        try: Bandwidths = self._Bandwidths_config.getfloat('main', 'Bandwidth')
        except: Bandwidths = 8.e6
        self.Bandwidths = Bandwidths
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
        self._nsigmas_config = configparser.ConfigParser()
        self._nsigmas_config.read(ConfigFile)
        try: nsigmas = self._nsigmas_config.getfloat('main', 'nsigma')
        except: nsigmas = 5.5
        self.nsigmas = nsigmas
        self._nAves_config = configparser.ConfigParser()
        self._nAves_config.read(ConfigFile)
        try: nAves = self._nAves_config.getint('main', 'nave')
        except: nAves = 20
        self.nAves = nAves
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(ConfigFile)
        try: fftsize_save = self._fftsize_save_config.getint('main', 'fftsize')
        except: fftsize_save = 1024
        self.fftsize_save = fftsize_save
        self._device_save_config = configparser.ConfigParser()
        self._device_save_config.read(ConfigFile)
        try: device_save = self._device_save_config.get('main', 'device')
        except: device_save = 'airspy,bias=1,pack=1'
        self.device_save = device_save
        self._IQMode_save_config = configparser.ConfigParser()
        self._IQMode_save_config.read(ConfigFile)
        try: IQMode_save = self._IQMode_save_config.getboolean('main', 'iqmode')
        except: IQMode_save = False
        self.IQMode_save = IQMode_save
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(ConfigFile)
        try: IF_attn_save = self._IF_attn_save_config.getfloat('main', 'ifattn')
        except: IF_attn_save = 30
        self.IF_attn_save = IF_attn_save
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(ConfigFile)
        try: Gain1s = self._Gain1s_config.getfloat('main', 'gain1')
        except: Gain1s = 49.
        self.Gain1s = Gain1s
        self.Frequency = Frequency = Frequencys
        self._Elevation_save_config = configparser.ConfigParser()
        self._Elevation_save_config.read(ConfigFile)
        try: Elevation_save = self._Elevation_save_config.getfloat('main', 'elevation')
        except: Elevation_save = 90.
        self.Elevation_save = Elevation_save
        self._DebugOn_save_config = configparser.ConfigParser()
        self._DebugOn_save_config.read(ConfigFile)
        try: DebugOn_save = self._DebugOn_save_config.getboolean('main', 'debugon')
        except: DebugOn_save = False
        self.DebugOn_save = DebugOn_save
        self._DcOffsetMode_save_config = configparser.ConfigParser()
        self._DcOffsetMode_save_config.read(ConfigFile)
        try: DcOffsetMode_save = self._DcOffsetMode_save_config.getboolean('main', 'dcoffsetmode')
        except: DcOffsetMode_save = False
        self.DcOffsetMode_save = DcOffsetMode_save
        self._DabNotch_save_config = configparser.ConfigParser()
        self._DabNotch_save_config.read(ConfigFile)
        try: DabNotch_save = self._DabNotch_save_config.getboolean('main', 'dabnotch')
        except: DabNotch_save = False
        self.DabNotch_save = DabNotch_save
        self._BroadcastNotch_save_config = configparser.ConfigParser()
        self._BroadcastNotch_save_config.read(ConfigFile)
        try: BroadcastNotch_save = self._BroadcastNotch_save_config.getboolean('main', 'broadcastnotch')
        except: BroadcastNotch_save = False
        self.BroadcastNotch_save = BroadcastNotch_save
        self._BiasOn_save_config = configparser.ConfigParser()
        self._BiasOn_save_config.read(ConfigFile)
        try: BiasOn_save = self._BiasOn_save_config.getboolean('main', 'biason')
        except: BiasOn_save = False
        self.BiasOn_save = BiasOn_save
        self.Bandwidth = Bandwidth = Bandwidths
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(ConfigFile)
        try: Azimuth_save = self._Azimuth_save_config.getfloat('main', 'azimuth')
        except: Azimuth_save = 90.
        self.Azimuth_save = Azimuth_save
        self.samp_rate = samp_rate = Bandwidth
        self.observer = observer = observers_save
        self.numin = numin = (Frequency - (Bandwidth/2.))
        self.nsigma = nsigma = nsigmas
        self.nAve = nAve = nAves
        self.fftsize = fftsize = fftsize_save
        self.Telescope = Telescope = telescope_save
        self.Record = Record = 1
        self.IQMode = IQMode = IQMode_save
        self.IF_attn = IF_attn = IF_attn_save
        self.H1 = H1 = 1420.406E6
        self.Gain2 = Gain2 = 12.
        self.Gain1 = Gain1 = Gain1s
        self.EventMode = EventMode = 1
        self.Elevation = Elevation = Elevation_save
        self.Device = Device = device_save
        self.DebugOn = DebugOn = bool(DebugOn_save)
        self.DcOffsetMode = DcOffsetMode = DcOffsetMode_save
        self.DabNotch = DabNotch = DabNotch_save
        self.BroadcastNotch = BroadcastNotch = BroadcastNotch_save
        self.BiasOn = BiasOn = BiasOn_save
        self.Azimuth = Azimuth = Azimuth_save

        ##################################################
        # Blocks
        ##################################################
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
        self._nsigma_range = Range(0., 10., .1, nsigmas, 100)
        self._nsigma_win = RangeWidget(self._nsigma_range, self.set_nsigma, "N Sigma", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._nsigma_win, 2, 6, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 8):
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
        # Create the options list
        self._Record_options = [0, 1]
        # Create the labels list
        self._Record_labels = ['! ! Wait ! !', 'AVERAGE']
        # Create the combo box
        # Create the radio buttons
        self._Record_group_box = Qt.QGroupBox("Spec. Mode" + ": ")
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
        self.top_grid_layout.addWidget(self._Record_group_box, 3, 0, 1, 3)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        _IQMode_check_box = Qt.QCheckBox("IQMode")
        self._IQMode_choices = {True: True, False: False}
        self._IQMode_choices_inv = dict((v,k) for k,v in self._IQMode_choices.items())
        self._IQMode_callback = lambda i: Qt.QMetaObject.invokeMethod(_IQMode_check_box, "setChecked", Qt.Q_ARG("bool", self._IQMode_choices_inv[i]))
        self._IQMode_callback(self.IQMode)
        _IQMode_check_box.stateChanged.connect(lambda i: self.set_IQMode(self._IQMode_choices[bool(i)]))
        self.top_grid_layout.addWidget(_IQMode_check_box, 9, 4, 1, 2)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._IF_attn_tool_bar = Qt.QToolBar(self)
        self._IF_attn_tool_bar.addWidget(Qt.QLabel("IF_attn" + ": "))
        self._IF_attn_line_edit = Qt.QLineEdit(str(self.IF_attn))
        self._IF_attn_tool_bar.addWidget(self._IF_attn_line_edit)
        self._IF_attn_line_edit.returnPressed.connect(
            lambda: self.set_IF_attn(eng_notation.str_to_num(str(self._IF_attn_line_edit.text()))))
        self.top_grid_layout.addWidget(self._IF_attn_tool_bar, 4, 6, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Gain1_tool_bar = Qt.QToolBar(self)
        self._Gain1_tool_bar.addWidget(Qt.QLabel("Gain1" + ": "))
        self._Gain1_line_edit = Qt.QLineEdit(str(self.Gain1))
        self._Gain1_tool_bar.addWidget(self._Gain1_line_edit)
        self._Gain1_line_edit.returnPressed.connect(
            lambda: self.set_Gain1(eng_notation.str_to_num(str(self._Gain1_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Gain1_tool_bar, 2, 2, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Frequency_tool_bar = Qt.QToolBar(self)
        self._Frequency_tool_bar.addWidget(Qt.QLabel("Freq. Hz" + ": "))
        self._Frequency_line_edit = Qt.QLineEdit(str(self.Frequency))
        self._Frequency_tool_bar.addWidget(self._Frequency_line_edit)
        self._Frequency_line_edit.returnPressed.connect(
            lambda: self.set_Frequency(eng_notation.str_to_num(str(self._Frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Frequency_tool_bar, 0, 5, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._EventMode_options = [0, 1]
        # Create the labels list
        self._EventMode_labels = ['! ! Wait ! !', 'Write']
        # Create the combo box
        # Create the radio buttons
        self._EventMode_group_box = Qt.QGroupBox("Event Mode" + ": ")
        self._EventMode_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._EventMode_button_group = variable_chooser_button_group()
        self._EventMode_group_box.setLayout(self._EventMode_box)
        for i, _label in enumerate(self._EventMode_labels):
            radio_button = Qt.QRadioButton(_label)
            self._EventMode_box.addWidget(radio_button)
            self._EventMode_button_group.addButton(radio_button, i)
        self._EventMode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._EventMode_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._EventMode_options.index(i)))
        self._EventMode_callback(self.EventMode)
        self._EventMode_button_group.buttonClicked[int].connect(
            lambda i: self.set_EventMode(self._EventMode_options[i]))
        self.top_grid_layout.addWidget(self._EventMode_group_box, 3, 3, 1, 3)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Elevation_tool_bar = Qt.QToolBar(self)
        self._Elevation_tool_bar.addWidget(Qt.QLabel("Elevation" + ": "))
        self._Elevation_line_edit = Qt.QLineEdit(str(self.Elevation))
        self._Elevation_tool_bar.addWidget(self._Elevation_line_edit)
        self._Elevation_line_edit.returnPressed.connect(
            lambda: self.set_Elevation(eng_notation.str_to_num(str(self._Elevation_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Elevation_tool_bar, 1, 7, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(7, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Device_tool_bar = Qt.QToolBar(self)
        self._Device_tool_bar.addWidget(Qt.QLabel("Dev" + ": "))
        self._Device_line_edit = Qt.QLineEdit(str(self.Device))
        self._Device_tool_bar.addWidget(self._Device_line_edit)
        self._Device_line_edit.returnPressed.connect(
            lambda: self.set_Device(str(str(self._Device_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Device_tool_bar, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _DebugOn_check_box = Qt.QCheckBox("Debug")
        self._DebugOn_choices = {True: True, False: False}
        self._DebugOn_choices_inv = dict((v,k) for k,v in self._DebugOn_choices.items())
        self._DebugOn_callback = lambda i: Qt.QMetaObject.invokeMethod(_DebugOn_check_box, "setChecked", Qt.Q_ARG("bool", self._DebugOn_choices_inv[i]))
        self._DebugOn_callback(self.DebugOn)
        _DebugOn_check_box.stateChanged.connect(lambda i: self.set_DebugOn(self._DebugOn_choices[bool(i)]))
        self.top_grid_layout.addWidget(_DebugOn_check_box, 9, 8, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(8, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        _DcOffsetMode_check_box = Qt.QCheckBox("DcOffset")
        self._DcOffsetMode_choices = {True: True, False: False}
        self._DcOffsetMode_choices_inv = dict((v,k) for k,v in self._DcOffsetMode_choices.items())
        self._DcOffsetMode_callback = lambda i: Qt.QMetaObject.invokeMethod(_DcOffsetMode_check_box, "setChecked", Qt.Q_ARG("bool", self._DcOffsetMode_choices_inv[i]))
        self._DcOffsetMode_callback(self.DcOffsetMode)
        _DcOffsetMode_check_box.stateChanged.connect(lambda i: self.set_DcOffsetMode(self._DcOffsetMode_choices[bool(i)]))
        self.top_grid_layout.addWidget(_DcOffsetMode_check_box, 9, 0, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        _DabNotch_check_box = Qt.QCheckBox("DabNotch")
        self._DabNotch_choices = {True: True, False: False}
        self._DabNotch_choices_inv = dict((v,k) for k,v in self._DabNotch_choices.items())
        self._DabNotch_callback = lambda i: Qt.QMetaObject.invokeMethod(_DabNotch_check_box, "setChecked", Qt.Q_ARG("bool", self._DabNotch_choices_inv[i]))
        self._DabNotch_callback(self.DabNotch)
        _DabNotch_check_box.stateChanged.connect(lambda i: self.set_DabNotch(self._DabNotch_choices[bool(i)]))
        self.top_grid_layout.addWidget(_DabNotch_check_box, 9, 2, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        _BroadcastNotch_check_box = Qt.QCheckBox("Broadcast")
        self._BroadcastNotch_choices = {True: True, False: False}
        self._BroadcastNotch_choices_inv = dict((v,k) for k,v in self._BroadcastNotch_choices.items())
        self._BroadcastNotch_callback = lambda i: Qt.QMetaObject.invokeMethod(_BroadcastNotch_check_box, "setChecked", Qt.Q_ARG("bool", self._BroadcastNotch_choices_inv[i]))
        self._BroadcastNotch_callback(self.BroadcastNotch)
        _BroadcastNotch_check_box.stateChanged.connect(lambda i: self.set_BroadcastNotch(self._BroadcastNotch_choices[bool(i)]))
        self.top_grid_layout.addWidget(_BroadcastNotch_check_box, 9, 3, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        _BiasOn_check_box = Qt.QCheckBox("BiasTee")
        self._BiasOn_choices = {True: True, False: False}
        self._BiasOn_choices_inv = dict((v,k) for k,v in self._BiasOn_choices.items())
        self._BiasOn_callback = lambda i: Qt.QMetaObject.invokeMethod(_BiasOn_check_box, "setChecked", Qt.Q_ARG("bool", self._BiasOn_choices_inv[i]))
        self._BiasOn_callback(self.BiasOn)
        _BiasOn_check_box.stateChanged.connect(lambda i: self.set_BiasOn(self._BiasOn_choices[bool(i)]))
        self.top_grid_layout.addWidget(_BiasOn_check_box, 9, 6, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Bandwidth_tool_bar = Qt.QToolBar(self)
        self._Bandwidth_tool_bar.addWidget(Qt.QLabel("Bandwidth" + ": "))
        self._Bandwidth_line_edit = Qt.QLineEdit(str(self.Bandwidth))
        self._Bandwidth_tool_bar.addWidget(self._Bandwidth_line_edit)
        self._Bandwidth_line_edit.returnPressed.connect(
            lambda: self.set_Bandwidth(eng_notation.str_to_num(str(self._Bandwidth_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Bandwidth_tool_bar, 1, 5, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Azimuth_tool_bar = Qt.QToolBar(self)
        self._Azimuth_tool_bar.addWidget(Qt.QLabel("Azimuth" + ": "))
        self._Azimuth_line_edit = Qt.QLineEdit(str(self.Azimuth))
        self._Azimuth_tool_bar.addWidget(self._Azimuth_line_edit)
        self._Azimuth_line_edit.returnPressed.connect(
            lambda: self.set_Azimuth(eng_notation.str_to_num(str(self._Azimuth_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Azimuth_tool_bar, 0, 7, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(7, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.sdrplay3_rsp1a_0.set_gain(-Gain1, 'RF')
        self.sdrplay3_rsp1a_0.set_freq_corr(0)
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(bool(DcOffsetMode))
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(bool(IQMode))
        self.sdrplay3_rsp1a_0.set_agc_setpoint(-30)
        self.sdrplay3_rsp1a_0.set_rf_notch_filter(bool(BroadcastNotch))
        self.sdrplay3_rsp1a_0.set_dab_notch_filter(bool(DabNotch))
        self.sdrplay3_rsp1a_0.set_biasT(bool(BiasOn))
        self.sdrplay3_rsp1a_0.set_debug_mode(bool(DebugOn))
        self.sdrplay3_rsp1a_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rsp1a_0.set_show_gain_changes(True)
        self.radio_astro_vmedian_0_0_1_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0_1 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_ra_event_sink_0 = radio_astro.ra_event_sink(ObsName+"Event.not", fftsize, Frequency, Bandwidth, EventMode, 'Event Detection', 'Observer', Telescope, Device, float(IF_attn), Azimuth, Elevation)
        self.radio_astro_ra_event_log_0 = radio_astro.ra_event_log('', 'Event Detection', fftsize, 1.0)
        self.radio_astro_ra_ascii_sink_0 = radio_astro.ra_ascii_sink(ObsName+".not", observer, fftsize, Frequency, Bandwidth, Azimuth, Elevation, Record, 0, 4**5, nAve, telescope_save, device_save, float(IF_attn), float(Gain2), float(Gain1))
        self.radio_astro_detect_0 = radio_astro.detect(fftsize, nsigma, Frequency, Bandwidth, fftsize/Bandwidth, EventMode)
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
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 3, 6, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            fftsize,
            100,
            -.4,
            .4,
            "",
            2,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(2.)
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
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 4, 0, 1, 5)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 5):
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
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.radio_astro_vmedian_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.radio_astro_detect_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_log_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_sink_0, 0))
        self.connect((self.radio_astro_ra_ascii_sink_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.radio_astro_ra_ascii_sink_0, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_0, 0), (self.radio_astro_vmedian_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_1, 0), (self.radio_astro_vmedian_0_0_1_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_1_0, 0), (self.radio_astro_vmedian_0_0_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_stream_to_vector_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NsfWatch80")
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
        self.radio_astro_ra_event_sink_0.set_setup(self.ObsName+"Event.not")

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
        self._BiasOn_save_config = configparser.ConfigParser()
        self._BiasOn_save_config.read(self.ConfigFile)
        if not self._BiasOn_save_config.has_section('main'):
        	self._BiasOn_save_config.add_section('main')
        self._BiasOn_save_config.set('main', 'biason', str(self.BiasOn))
        self._BiasOn_save_config.write(open(self.ConfigFile, 'w'))
        self._BroadcastNotch_save_config = configparser.ConfigParser()
        self._BroadcastNotch_save_config.read(self.ConfigFile)
        if not self._BroadcastNotch_save_config.has_section('main'):
        	self._BroadcastNotch_save_config.add_section('main')
        self._BroadcastNotch_save_config.set('main', 'broadcastnotch', str(self.BroadcastNotch))
        self._BroadcastNotch_save_config.write(open(self.ConfigFile, 'w'))
        self._DabNotch_save_config = configparser.ConfigParser()
        self._DabNotch_save_config.read(self.ConfigFile)
        if not self._DabNotch_save_config.has_section('main'):
        	self._DabNotch_save_config.add_section('main')
        self._DabNotch_save_config.set('main', 'dabnotch', str(self.DabNotch))
        self._DabNotch_save_config.write(open(self.ConfigFile, 'w'))
        self._DcOffsetMode_save_config = configparser.ConfigParser()
        self._DcOffsetMode_save_config.read(self.ConfigFile)
        if not self._DcOffsetMode_save_config.has_section('main'):
        	self._DcOffsetMode_save_config.add_section('main')
        self._DcOffsetMode_save_config.set('main', 'dcoffsetmode', str(self.DcOffsetMode))
        self._DcOffsetMode_save_config.write(open(self.ConfigFile, 'w'))
        self._DebugOn_save_config = configparser.ConfigParser()
        self._DebugOn_save_config.read(self.ConfigFile)
        if not self._DebugOn_save_config.has_section('main'):
        	self._DebugOn_save_config.add_section('main')
        self._DebugOn_save_config.set('main', 'debugon', str(self.DebugOn))
        self._DebugOn_save_config.write(open(self.ConfigFile, 'w'))
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
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(self.ConfigFile)
        if not self._IF_attn_save_config.has_section('main'):
        	self._IF_attn_save_config.add_section('main')
        self._IF_attn_save_config.set('main', 'ifattn', str(self.IF_attn))
        self._IF_attn_save_config.write(open(self.ConfigFile, 'w'))
        self._IQMode_save_config = configparser.ConfigParser()
        self._IQMode_save_config.read(self.ConfigFile)
        if not self._IQMode_save_config.has_section('main'):
        	self._IQMode_save_config.add_section('main')
        self._IQMode_save_config.set('main', 'iqmode', str(self.IQMode))
        self._IQMode_save_config.write(open(self.ConfigFile, 'w'))
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
        self._nsigmas_config = configparser.ConfigParser()
        self._nsigmas_config.read(self.ConfigFile)
        if not self._nsigmas_config.has_section('main'):
        	self._nsigmas_config.add_section('main')
        self._nsigmas_config.set('main', 'nsigma', str(self.nsigma))
        self._nsigmas_config.write(open(self.ConfigFile, 'w'))
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

    def get_Frequencys(self):
        return self.Frequencys

    def set_Frequencys(self, Frequencys):
        self.Frequencys = Frequencys
        self.set_Frequency(self.Frequencys)

    def get_Bandwidths(self):
        return self.Bandwidths

    def set_Bandwidths(self, Bandwidths):
        self.Bandwidths = Bandwidths
        self.set_Bandwidth(self.Bandwidths)

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

    def get_nsigmas(self):
        return self.nsigmas

    def set_nsigmas(self, nsigmas):
        self.nsigmas = nsigmas
        self.set_nsigma(self.nsigmas)

    def get_nAves(self):
        return self.nAves

    def set_nAves(self, nAves):
        self.nAves = nAves
        self.set_nAve(self.nAves)

    def get_fftsize_save(self):
        return self.fftsize_save

    def set_fftsize_save(self, fftsize_save):
        self.fftsize_save = fftsize_save
        self.set_fftsize(self.fftsize_save)

    def get_device_save(self):
        return self.device_save

    def set_device_save(self, device_save):
        self.device_save = device_save
        self.set_Device(self.device_save)
        self.radio_astro_ra_ascii_sink_0.set_device(self.device_save)

    def get_IQMode_save(self):
        return self.IQMode_save

    def set_IQMode_save(self, IQMode_save):
        self.IQMode_save = IQMode_save
        self.set_IQMode(self.IQMode_save)

    def get_IF_attn_save(self):
        return self.IF_attn_save

    def set_IF_attn_save(self, IF_attn_save):
        self.IF_attn_save = IF_attn_save
        self.set_IF_attn(self.IF_attn_save)

    def get_Gain1s(self):
        return self.Gain1s

    def set_Gain1s(self, Gain1s):
        self.Gain1s = Gain1s
        self.set_Gain1(self.Gain1s)

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
        self.radio_astro_detect_0.set_freq(self.Frequency)
        self.radio_astro_ra_ascii_sink_0.set_frequency(self.Frequency)
        self.radio_astro_ra_event_sink_0.set_frequency(self.Frequency)
        self.radio_astro_ra_event_sink_0.set_frequency(self.Frequency)
        self.sdrplay3_rsp1a_0.set_center_freq(self.Frequency)

    def get_Elevation_save(self):
        return self.Elevation_save

    def set_Elevation_save(self, Elevation_save):
        self.Elevation_save = Elevation_save
        self.set_Elevation(self.Elevation_save)

    def get_DebugOn_save(self):
        return self.DebugOn_save

    def set_DebugOn_save(self, DebugOn_save):
        self.DebugOn_save = DebugOn_save
        self.set_DebugOn(bool(self.DebugOn_save))

    def get_DcOffsetMode_save(self):
        return self.DcOffsetMode_save

    def set_DcOffsetMode_save(self, DcOffsetMode_save):
        self.DcOffsetMode_save = DcOffsetMode_save
        self.set_DcOffsetMode(self.DcOffsetMode_save)

    def get_DabNotch_save(self):
        return self.DabNotch_save

    def set_DabNotch_save(self, DabNotch_save):
        self.DabNotch_save = DabNotch_save
        self.set_DabNotch(self.DabNotch_save)

    def get_BroadcastNotch_save(self):
        return self.BroadcastNotch_save

    def set_BroadcastNotch_save(self, BroadcastNotch_save):
        self.BroadcastNotch_save = BroadcastNotch_save
        self.set_BroadcastNotch(self.BroadcastNotch_save)

    def get_BiasOn_save(self):
        return self.BiasOn_save

    def set_BiasOn_save(self, BiasOn_save):
        self.BiasOn_save = BiasOn_save
        self.set_BiasOn(self.BiasOn_save)

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
        self.set_samp_rate(self.Bandwidth)
        self.radio_astro_detect_0.set_bw(self.Bandwidth)
        self.radio_astro_ra_ascii_sink_0.set_bandwidth(self.Bandwidth)
        self.radio_astro_ra_event_sink_0.set_sample_rate(self.Bandwidth)

    def get_Azimuth_save(self):
        return self.Azimuth_save

    def set_Azimuth_save(self, Azimuth_save):
        self.Azimuth_save = Azimuth_save
        self.set_Azimuth(self.Azimuth_save)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate)

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

    def get_numin(self):
        return self.numin

    def set_numin(self, numin):
        self.numin = numin

    def get_nsigma(self):
        return self.nsigma

    def set_nsigma(self, nsigma):
        self.nsigma = nsigma
        self._nsigmas_config = configparser.ConfigParser()
        self._nsigmas_config.read(self.ConfigFile)
        if not self._nsigmas_config.has_section('main'):
        	self._nsigmas_config.add_section('main')
        self._nsigmas_config.set('main', 'nsigma', str(self.nsigma))
        self._nsigmas_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_detect_0.set_dms(self.nsigma)

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
        self.radio_astro_detect_0.set_vlen(self.fftsize)
        self.radio_astro_ra_event_log_0.set_vlen(self.fftsize)
        self.radio_astro_ra_event_sink_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0_1.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0_1_0.set_vlen(self.fftsize)

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
        self.radio_astro_ra_event_sink_0.set_telescope(self.Telescope)

    def get_Record(self):
        return self.Record

    def set_Record(self, Record):
        self.Record = Record
        self._Record_callback(self.Record)
        self.radio_astro_ra_ascii_sink_0.set_record(self.Record)

    def get_IQMode(self):
        return self.IQMode

    def set_IQMode(self, IQMode):
        self.IQMode = IQMode
        self._IQMode_callback(self.IQMode)
        self._IQMode_save_config = configparser.ConfigParser()
        self._IQMode_save_config.read(self.ConfigFile)
        if not self._IQMode_save_config.has_section('main'):
        	self._IQMode_save_config.add_section('main')
        self._IQMode_save_config.set('main', 'iqmode', str(self.IQMode))
        self._IQMode_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(bool(self.IQMode))

    def get_IF_attn(self):
        return self.IF_attn

    def set_IF_attn(self, IF_attn):
        self.IF_attn = IF_attn
        Qt.QMetaObject.invokeMethod(self._IF_attn_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.IF_attn)))
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(self.ConfigFile)
        if not self._IF_attn_save_config.has_section('main'):
        	self._IF_attn_save_config.add_section('main')
        self._IF_attn_save_config.set('main', 'ifattn', str(self.IF_attn))
        self._IF_attn_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_gain1(float(self.IF_attn))
        self.radio_astro_ra_event_sink_0.set_gain1(float(self.IF_attn))
        self.sdrplay3_rsp1a_0.set_gain(-self.IF_attn, 'IF')

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1

    def get_Gain2(self):
        return self.Gain2

    def set_Gain2(self, Gain2):
        self.Gain2 = Gain2
        self.radio_astro_ra_ascii_sink_0.set_gain2(float(self.Gain2))

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
        self.radio_astro_ra_ascii_sink_0.set_gain3(float(self.Gain1))
        self.sdrplay3_rsp1a_0.set_gain(-self.Gain1, 'RF')

    def get_EventMode(self):
        return self.EventMode

    def set_EventMode(self, EventMode):
        self.EventMode = EventMode
        self._EventMode_callback(self.EventMode)
        self.radio_astro_detect_0.set_mode(self.EventMode)
        self.radio_astro_ra_event_sink_0.set_record(self.EventMode)

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
        self.radio_astro_ra_event_sink_0.set_telel(self.Elevation)

    def get_Device(self):
        return self.Device

    def set_Device(self, Device):
        self.Device = Device
        Qt.QMetaObject.invokeMethod(self._Device_line_edit, "setText", Qt.Q_ARG("QString", str(self.Device)))
        self._device_save_config = configparser.ConfigParser()
        self._device_save_config.read(self.ConfigFile)
        if not self._device_save_config.has_section('main'):
        	self._device_save_config.add_section('main')
        self._device_save_config.set('main', 'device', str(self.Device))
        self._device_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_event_sink_0.set_device(self.Device)

    def get_DebugOn(self):
        return self.DebugOn

    def set_DebugOn(self, DebugOn):
        self.DebugOn = DebugOn
        self._DebugOn_callback(self.DebugOn)
        self._DebugOn_save_config = configparser.ConfigParser()
        self._DebugOn_save_config.read(self.ConfigFile)
        if not self._DebugOn_save_config.has_section('main'):
        	self._DebugOn_save_config.add_section('main')
        self._DebugOn_save_config.set('main', 'debugon', str(self.DebugOn))
        self._DebugOn_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_debug_mode(bool(self.DebugOn))

    def get_DcOffsetMode(self):
        return self.DcOffsetMode

    def set_DcOffsetMode(self, DcOffsetMode):
        self.DcOffsetMode = DcOffsetMode
        self._DcOffsetMode_callback(self.DcOffsetMode)
        self._DcOffsetMode_save_config = configparser.ConfigParser()
        self._DcOffsetMode_save_config.read(self.ConfigFile)
        if not self._DcOffsetMode_save_config.has_section('main'):
        	self._DcOffsetMode_save_config.add_section('main')
        self._DcOffsetMode_save_config.set('main', 'dcoffsetmode', str(self.DcOffsetMode))
        self._DcOffsetMode_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(bool(self.DcOffsetMode))

    def get_DabNotch(self):
        return self.DabNotch

    def set_DabNotch(self, DabNotch):
        self.DabNotch = DabNotch
        self._DabNotch_callback(self.DabNotch)
        self._DabNotch_save_config = configparser.ConfigParser()
        self._DabNotch_save_config.read(self.ConfigFile)
        if not self._DabNotch_save_config.has_section('main'):
        	self._DabNotch_save_config.add_section('main')
        self._DabNotch_save_config.set('main', 'dabnotch', str(self.DabNotch))
        self._DabNotch_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_dab_notch_filter(bool(self.DabNotch))

    def get_BroadcastNotch(self):
        return self.BroadcastNotch

    def set_BroadcastNotch(self, BroadcastNotch):
        self.BroadcastNotch = BroadcastNotch
        self._BroadcastNotch_callback(self.BroadcastNotch)
        self._BroadcastNotch_save_config = configparser.ConfigParser()
        self._BroadcastNotch_save_config.read(self.ConfigFile)
        if not self._BroadcastNotch_save_config.has_section('main'):
        	self._BroadcastNotch_save_config.add_section('main')
        self._BroadcastNotch_save_config.set('main', 'broadcastnotch', str(self.BroadcastNotch))
        self._BroadcastNotch_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_rf_notch_filter(bool(self.BroadcastNotch))

    def get_BiasOn(self):
        return self.BiasOn

    def set_BiasOn(self, BiasOn):
        self.BiasOn = BiasOn
        self._BiasOn_callback(self.BiasOn)
        self._BiasOn_save_config = configparser.ConfigParser()
        self._BiasOn_save_config.read(self.ConfigFile)
        if not self._BiasOn_save_config.has_section('main'):
        	self._BiasOn_save_config.add_section('main')
        self._BiasOn_save_config.set('main', 'biason', str(self.BiasOn))
        self._BiasOn_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_biasT(bool(self.BiasOn))

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
        self.radio_astro_ra_event_sink_0.set_telaz(self.Azimuth)




def main(top_block_cls=NsfWatch80, options=None):

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
