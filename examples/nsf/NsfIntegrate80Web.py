#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Web display NsfIntegrate: SDRPlay 8MHz Astronomical Obs.
# Author: Glen Langston
# Description: Astronomy with 8.0 MHz SDRPlay RSP 1A
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import eng_notation
import bokehgui
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
import configparser




class NsfIntegrate80Web(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Web display NsfIntegrate: SDRPlay 8MHz Astronomical Obs.", catch_exceptions=True)
        self.plot_lst = []
        self.widget_lst = []

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
        try: Bandwidths = self._Bandwidths_config.getfloat('main', 'bandwidth')
        except: Bandwidths = 8.e6
        self.Bandwidths = Bandwidths
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(ConfigFile)
        try: fftsize_save = self._fftsize_save_config.getint('main', 'fftsize')
        except: fftsize_save = 1024
        self.fftsize_save = fftsize_save
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(ConfigFile)
        try: IF_attn_save = self._IF_attn_save_config.getfloat('main', 'ifattn')
        except: IF_attn_save = 30
        self.IF_attn_save = IF_attn_save
        self.Frequency = Frequency = float(Frequencys)
        self.Bandwidth = Bandwidth = int(Bandwidths)
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
        self.IF_attn = IF_attn = float(IF_attn_save)
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
        self._DebugOn_save_config = configparser.ConfigParser()
        self._DebugOn_save_config.read(ConfigFile)
        try: DebugOn_save = self._DebugOn_save_config.getboolean('main', 'debugon')
        except: DebugOn_save = False
        self.DebugOn_save = DebugOn_save
        self._DcOffset_save_config = configparser.ConfigParser()
        self._DcOffset_save_config.read(ConfigFile)
        try: DcOffset_save = self._DcOffset_save_config.getboolean('main', 'dcoffsetmode')
        except: DcOffset_save = False
        self.DcOffset_save = DcOffset_save
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
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(ConfigFile)
        try: Azimuth_save = self._Azimuth_save_config.getfloat('main', 'azimuth')
        except: Azimuth_save = 90.
        self.Azimuth_save = Azimuth_save
        self.yunits = yunits = ["Counts", "Power (dB)", "Intensity (Kelvins)", "Intensity (K)"]
        self.ymins = ymins = [ 0.01,  -20,  90.,-5.]
        self.ymaxs = ymaxs = [5., 10., 180., 80.]
        self.xunits = xunits = [ "MHz", "km.sec", "Channel"]
        self.xsteps = xsteps = [Bandwidth*1.E-6/fftsize, -Bandwidth*3.E5/(H1*fftsize), 1]
        self.xmins = xmins = [numin*1E-6, (H1 - numin)*(3E5/H1), 0 , 0]
        self._xaxis_save_config = configparser.ConfigParser()
        self._xaxis_save_config.read(ConfigFile)
        try: xaxis_save = self._xaxis_save_config.getint('main', 'Xaxis')
        except: xaxis_save = 0
        self.xaxis_save = xaxis_save
        self.units = units = 0
        self.samp_rate = samp_rate = Bandwidth
        self.obstype = obstype = 0
        self.observer = observer = observers_save
        self.nAve = nAve = int(nAves)
        self.Xaxis = Xaxis = 0
        self.Telescope = Telescope = telescope_save
        self.Record = Record = 1
        self.IQMode = IQMode = bool(IQMode_save)
        self.Gain3 = Gain3 = IF_attn
        self.Gain2 = Gain2 = IF_attn
        self.Gain1 = Gain1 = Gain1s
        self.Elevation = Elevation = float(Elevation_save)
        self.Device = Device = device_save
        self.DebugOn = DebugOn = bool(DebugOn_save)
        self.DcOffsetMode = DcOffsetMode = bool(DcOffset_save)
        self.DabNotch = DabNotch = bool(DabNotch_save)
        self.BroadcastNotch = BroadcastNotch = bool(BroadcastNotch_save)
        self.BiasOn = BiasOn = bool(BiasOn_save)
        self.Azimuth = Azimuth = float( Azimuth_save)

        ##################################################
        # Blocks
        ##################################################
        self._obstype_options = [    0,     1,     2,     3,   ]
        self._obstype_labels = [      'Survey',      'Cold',      'Hot',      'Ref',  ]

        self.obstype_radiobutton = bokehgui.radiobutton(self.widget_lst, None, self._obstype_labels, inline = True)
        self.obstype_radiobutton.add_callback(
                  lambda new: self.set_obstype(int(self._obstype_options[new])))
        self._Record_options = [    0,     1,     2,   ]
        self._Record_labels = [      'Wait',      'Average',      'Save',  ]

        self.Record_radiobutton = bokehgui.radiobutton(self.widget_lst, None, self._Record_labels, inline = True)
        self.Record_radiobutton.add_callback(
                  lambda new: self.set_Record(int(self._Record_options[new])))
        self.Frequency_textbox = bokehgui.textbox(self.widget_lst, str(float(Frequencys)), 'Frequency' +": ")
        self.Frequency_textbox.add_callback(
          lambda attr, old, new: self.set_Frequency(eng_notation.str_to_num(new)))
        self.Elevation_textbox = bokehgui.textbox(self.widget_lst, str(float(Elevation_save)), 'Elevation' +": ")
        self.Elevation_textbox.add_callback(
          lambda attr, old, new: self.set_Elevation(eng_notation.str_to_num(new)))
        self.Azimuth_textbox = bokehgui.textbox(self.widget_lst, str(float( Azimuth_save)), 'Azimuth' +": ")
        self.Azimuth_textbox.add_callback(
          lambda attr, old, new: self.set_Azimuth(eng_notation.str_to_num(new)))
        self.sdrplay3_rsp1a_0 = sdrplay3.rsp1a(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rsp1a_0.set_sample_rate(samp_rate)
        self.sdrplay3_rsp1a_0.set_center_freq(Frequency)
        self.sdrplay3_rsp1a_0.set_bandwidth(8000e3)
        self.sdrplay3_rsp1a_0.set_gain_mode(False)
        self.sdrplay3_rsp1a_0.set_gain(-Gain2, 'IF')
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
        self.radio_astro_vmedian_0_3_2 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_3_1 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_3_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_3 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_2_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_2 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_1 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_ra_integrate_1 = radio_astro.ra_integrate(ObsName+".not", observers_save, fftsize, Frequencys, Bandwidths, Azimuth, Elevation, Record, obstype, 4**5, units, 295., 10.)
        self.radio_astro_ra_ascii_sink_0 = radio_astro.ra_ascii_sink(ObsName+".not", observer, fftsize, Frequencys, Bandwidths, Azimuth, Elevation, Record, obstype, 4**5, nAve, telescope_save, device_save, Gain1, float(Gain2), float(Gain2))
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.hamming(fftsize), True, 1)
        self.bokehgui_vector_sink_x_0 = bokehgui.vec_sink_f_proc(fftsize,
                             "",                     4                    )

        labels = ['Latest', 'Ave', 'Hot', 'Cold', '',
                  '', '', '', '', '']
        legend_list = []

        for i in  range(    4  ):
          if len(labels[i]) == 0:
            legend_list.append("Data {0}".format(i))
          else:
            legend_list.append(labels[i])

        self.bokehgui_vector_sink_x_0_plot = bokehgui.vec_sink_f(self.plot_lst, self.bokehgui_vector_sink_x_0, update_time = 2000, legend_list = legend_list, is_message =False)

        self.bokehgui_vector_sink_x_0_plot.set_y_axis([-0.1, 4.])
        self.bokehgui_vector_sink_x_0_plot.set_y_label('Intensity' + '(' +'Counts'+')')
        self.bokehgui_vector_sink_x_0_plot.set_x_label('Channel' + '(' +'(Int)'+')')

        self.bokehgui_vector_sink_x_0_plot.set_x_values([0,1])
        self.bokehgui_vector_sink_x_0_plot.enable_grid(False)
        self.bokehgui_vector_sink_x_0_plot.enable_axis_labels(True)
        self.bokehgui_vector_sink_x_0_plot.enable_legend(True)
        self.bokehgui_vector_sink_x_0_plot.set_layout(*((1,0,1,2)))
        colors = ["yellow", "green", "red", "blue", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        styles = ["solid", "solid", "solid", "solid", "solid",
                  "solid", "solid", "solid", "solid", "solid"]
        markers = [None, None, None, None, None,
                   None, None, None, None, None]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in  range(     4  ):
          self.bokehgui_vector_sink_x_0_plot.format_line(i, colors[i], widths[i], styles[i], markers[i], alphas[i])
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*fftsize)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fftsize)
        self.Bandwidth_textbox = bokehgui.textbox(self.widget_lst, str(int(Bandwidths)), 'Bandwidth' +": ")
        self.Bandwidth_textbox.add_callback(
          lambda attr, old, new: self.set_Bandwidth(int(new)))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.radio_astro_vmedian_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radio_astro_ra_ascii_sink_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.radio_astro_ra_integrate_1, 4), (self.blocks_null_sink_0_0, 0))
        self.connect((self.radio_astro_ra_integrate_1, 0), (self.radio_astro_vmedian_0_3, 0))
        self.connect((self.radio_astro_ra_integrate_1, 1), (self.radio_astro_vmedian_0_3_0, 0))
        self.connect((self.radio_astro_ra_integrate_1, 2), (self.radio_astro_vmedian_0_3_1, 0))
        self.connect((self.radio_astro_ra_integrate_1, 3), (self.radio_astro_vmedian_0_3_2, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.radio_astro_vmedian_0_1, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.radio_astro_vmedian_0_1, 0), (self.radio_astro_ra_ascii_sink_0, 0))
        self.connect((self.radio_astro_vmedian_0_1, 0), (self.radio_astro_ra_integrate_1, 0))
        self.connect((self.radio_astro_vmedian_0_2, 0), (self.radio_astro_vmedian_0_2_0, 0))
        self.connect((self.radio_astro_vmedian_0_2_0, 0), (self.radio_astro_vmedian_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_3, 0), (self.bokehgui_vector_sink_x_0, 0))
        self.connect((self.radio_astro_vmedian_0_3_0, 0), (self.bokehgui_vector_sink_x_0, 1))
        self.connect((self.radio_astro_vmedian_0_3_1, 0), (self.bokehgui_vector_sink_x_0, 2))
        self.connect((self.radio_astro_vmedian_0_3_2, 0), (self.bokehgui_vector_sink_x_0, 3))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_stream_to_vector_0_0, 0))


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
        self._Bandwidths_config.set('main', 'bandwidth', str(self.Bandwidth))
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
        self._DcOffset_save_config = configparser.ConfigParser()
        self._DcOffset_save_config.read(self.ConfigFile)
        if not self._DcOffset_save_config.has_section('main'):
        	self._DcOffset_save_config.add_section('main')
        self._DcOffset_save_config.set('main', 'dcoffsetmode', str(self.DcOffsetMode))
        self._DcOffset_save_config.write(open(self.ConfigFile, 'w'))
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

    def get_Frequencys(self):
        return self.Frequencys

    def set_Frequencys(self, Frequencys):
        self.Frequencys = Frequencys
        self.set_Frequency(float(self.Frequencys))
        self.Frequency_textbox.set_value(float(self.Frequencys))
        self.radio_astro_ra_ascii_sink_0.set_frequency(self.Frequencys)
        self.radio_astro_ra_integrate_1.set_frequency(self.Frequencys)

    def get_Bandwidths(self):
        return self.Bandwidths

    def set_Bandwidths(self, Bandwidths):
        self.Bandwidths = Bandwidths
        self.set_Bandwidth(int(self.Bandwidths))
        self.Bandwidth_textbox.set_value(int(self.Bandwidths))
        self.radio_astro_ra_ascii_sink_0.set_bandwidth(self.Bandwidths)
        self.radio_astro_ra_integrate_1.set_bandwidth(self.Bandwidths)

    def get_fftsize_save(self):
        return self.fftsize_save

    def set_fftsize_save(self, fftsize_save):
        self.fftsize_save = fftsize_save
        self.set_fftsize(self.fftsize_save)

    def get_IF_attn_save(self):
        return self.IF_attn_save

    def set_IF_attn_save(self, IF_attn_save):
        self.IF_attn_save = IF_attn_save
        self.set_IF_attn(float(self.IF_attn_save))

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(self.ConfigFile)
        if not self._Frequencys_config.has_section('main'):
        	self._Frequencys_config.add_section('main')
        self._Frequencys_config.set('main', 'Frequency', str(self.Frequency))
        self._Frequencys_config.write(open(self.ConfigFile, 'w'))
        self.set_numin((self.Frequency - (self.Bandwidth/2.)))
        self.sdrplay3_rsp1a_0.set_center_freq(self.Frequency)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(self.ConfigFile)
        if not self._Bandwidths_config.has_section('main'):
        	self._Bandwidths_config.add_section('main')
        self._Bandwidths_config.set('main', 'bandwidth', str(self.Bandwidth))
        self._Bandwidths_config.write(open(self.ConfigFile, 'w'))
        self.set_numin((self.Frequency - (self.Bandwidth/2.)))
        self.set_samp_rate(self.Bandwidth)
        self.set_xsteps([self.Bandwidth*1.E-6/self.fftsize, -self.Bandwidth*3.E5/(self.H1*self.fftsize), 1])

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
        self.set_xmins([self.numin*1E-6, (self.H1 - self.numin)*(3E5/self.H1), 0 , 0])

    def get_nAves(self):
        return self.nAves

    def set_nAves(self, nAves):
        self.nAves = nAves
        self.set_nAve(int(self.nAves))

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(self.ConfigFile)
        if not self._fftsize_save_config.has_section('main'):
        	self._fftsize_save_config.add_section('main')
        self._fftsize_save_config.set('main', 'fftsize', str(self.fftsize))
        self._fftsize_save_config.write(open(self.ConfigFile, 'w'))
        self.set_xsteps([self.Bandwidth*1.E-6/self.fftsize, -self.Bandwidth*3.E5/(self.H1*self.fftsize), 1])
        self.radio_astro_vmedian_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_1.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_2.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_2_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_3.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_3_0.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_3_1.set_vlen(self.fftsize)
        self.radio_astro_vmedian_0_3_2.set_vlen(self.fftsize)

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
        self.set_IQMode(bool(self.IQMode_save))

    def get_IF_attn(self):
        return self.IF_attn

    def set_IF_attn(self, IF_attn):
        self.IF_attn = IF_attn
        self.set_Gain2(self.IF_attn)
        self.set_Gain3(self.IF_attn)
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(self.ConfigFile)
        if not self._IF_attn_save_config.has_section('main'):
        	self._IF_attn_save_config.add_section('main')
        self._IF_attn_save_config.set('main', 'ifattn', str(self.IF_attn))
        self._IF_attn_save_config.write(open(self.ConfigFile, 'w'))

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1
        self.set_xmins([self.numin*1E-6, (self.H1 - self.numin)*(3E5/self.H1), 0 , 0])
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
        self.set_Elevation(float(self.Elevation_save))
        self.Elevation_textbox.set_value(float(self.Elevation_save))

    def get_DebugOn_save(self):
        return self.DebugOn_save

    def set_DebugOn_save(self, DebugOn_save):
        self.DebugOn_save = DebugOn_save
        self.set_DebugOn(bool(self.DebugOn_save))

    def get_DcOffset_save(self):
        return self.DcOffset_save

    def set_DcOffset_save(self, DcOffset_save):
        self.DcOffset_save = DcOffset_save
        self.set_DcOffsetMode(bool(self.DcOffset_save))

    def get_DabNotch_save(self):
        return self.DabNotch_save

    def set_DabNotch_save(self, DabNotch_save):
        self.DabNotch_save = DabNotch_save
        self.set_DabNotch(bool(self.DabNotch_save))

    def get_BroadcastNotch_save(self):
        return self.BroadcastNotch_save

    def set_BroadcastNotch_save(self, BroadcastNotch_save):
        self.BroadcastNotch_save = BroadcastNotch_save
        self.set_BroadcastNotch(bool(self.BroadcastNotch_save))

    def get_BiasOn_save(self):
        return self.BiasOn_save

    def set_BiasOn_save(self, BiasOn_save):
        self.BiasOn_save = BiasOn_save
        self.set_BiasOn(bool(self.BiasOn_save))

    def get_Azimuth_save(self):
        return self.Azimuth_save

    def set_Azimuth_save(self, Azimuth_save):
        self.Azimuth_save = Azimuth_save
        self.set_Azimuth(float( self.Azimuth_save))
        self.Azimuth_textbox.set_value(float( self.Azimuth_save))

    def get_yunits(self):
        return self.yunits

    def set_yunits(self, yunits):
        self.yunits = yunits

    def get_ymins(self):
        return self.ymins

    def set_ymins(self, ymins):
        self.ymins = ymins

    def get_ymaxs(self):
        return self.ymaxs

    def set_ymaxs(self, ymaxs):
        self.ymaxs = ymaxs

    def get_xunits(self):
        return self.xunits

    def set_xunits(self, xunits):
        self.xunits = xunits

    def get_xsteps(self):
        return self.xsteps

    def set_xsteps(self, xsteps):
        self.xsteps = xsteps

    def get_xmins(self):
        return self.xmins

    def set_xmins(self, xmins):
        self.xmins = xmins

    def get_xaxis_save(self):
        return self.xaxis_save

    def set_xaxis_save(self, xaxis_save):
        self.xaxis_save = xaxis_save

    def get_units(self):
        return self.units

    def set_units(self, units):
        self.units = units
        self.radio_astro_ra_integrate_1.set_units(self.units)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate)

    def get_obstype(self):
        return self.obstype

    def set_obstype(self, obstype):
        self.obstype = obstype
        self.radio_astro_ra_ascii_sink_0.set_obstype(self.obstype)
        self.radio_astro_ra_integrate_1.set_obstype(self.obstype)

    def get_observer(self):
        return self.observer

    def set_observer(self, observer):
        self.observer = observer
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
        self._nAves_config = configparser.ConfigParser()
        self._nAves_config.read(self.ConfigFile)
        if not self._nAves_config.has_section('main'):
        	self._nAves_config.add_section('main')
        self._nAves_config.set('main', 'nave', str(self.nAve))
        self._nAves_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_nave(self.nAve)

    def get_Xaxis(self):
        return self.Xaxis

    def set_Xaxis(self, Xaxis):
        self.Xaxis = Xaxis
        self._xaxis_save_config = configparser.ConfigParser()
        self._xaxis_save_config.read(self.ConfigFile)
        if not self._xaxis_save_config.has_section('main'):
        	self._xaxis_save_config.add_section('main')
        self._xaxis_save_config.set('main', 'Xaxis', str(self.Xaxis))
        self._xaxis_save_config.write(open(self.ConfigFile, 'w'))

    def get_Telescope(self):
        return self.Telescope

    def set_Telescope(self, Telescope):
        self.Telescope = Telescope
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
        self.radio_astro_ra_ascii_sink_0.set_record(self.Record)
        self.radio_astro_ra_integrate_1.set_inttype(self.Record)

    def get_IQMode(self):
        return self.IQMode

    def set_IQMode(self, IQMode):
        self.IQMode = IQMode
        self._IQMode_save_config = configparser.ConfigParser()
        self._IQMode_save_config.read(self.ConfigFile)
        if not self._IQMode_save_config.has_section('main'):
        	self._IQMode_save_config.add_section('main')
        self._IQMode_save_config.set('main', 'iqmode', str(self.IQMode))
        self._IQMode_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(bool(self.IQMode))

    def get_Gain3(self):
        return self.Gain3

    def set_Gain3(self, Gain3):
        self.Gain3 = Gain3

    def get_Gain2(self):
        return self.Gain2

    def set_Gain2(self, Gain2):
        self.Gain2 = Gain2
        self.radio_astro_ra_ascii_sink_0.set_gain2(float(self.Gain2))
        self.radio_astro_ra_ascii_sink_0.set_gain3(float(self.Gain2))
        self.sdrplay3_rsp1a_0.set_gain(-self.Gain2, 'IF')

    def get_Gain1(self):
        return self.Gain1

    def set_Gain1(self, Gain1):
        self.Gain1 = Gain1
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(self.ConfigFile)
        if not self._Gain1s_config.has_section('main'):
        	self._Gain1s_config.add_section('main')
        self._Gain1s_config.set('main', 'gain1', str(self.Gain1))
        self._Gain1s_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_gain1(self.Gain1)
        self.sdrplay3_rsp1a_0.set_gain(-self.Gain1, 'RF')

    def get_Elevation(self):
        return self.Elevation

    def set_Elevation(self, Elevation):
        self.Elevation = Elevation
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

    def get_DebugOn(self):
        return self.DebugOn

    def set_DebugOn(self, DebugOn):
        self.DebugOn = DebugOn
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
        self._DcOffset_save_config = configparser.ConfigParser()
        self._DcOffset_save_config.read(self.ConfigFile)
        if not self._DcOffset_save_config.has_section('main'):
        	self._DcOffset_save_config.add_section('main')
        self._DcOffset_save_config.set('main', 'dcoffsetmode', str(self.DcOffsetMode))
        self._DcOffset_save_config.write(open(self.ConfigFile, 'w'))
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(bool(self.DcOffsetMode))

    def get_DabNotch(self):
        return self.DabNotch

    def set_DabNotch(self, DabNotch):
        self.DabNotch = DabNotch
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
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(self.ConfigFile)
        if not self._Azimuth_save_config.has_section('main'):
        	self._Azimuth_save_config.add_section('main')
        self._Azimuth_save_config.set('main', 'azimuth', str(self.Azimuth))
        self._Azimuth_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_azimuth(self.Azimuth)
        self.radio_astro_ra_integrate_1.set_azimuth(self.Azimuth)




def main(top_block_cls=NsfIntegrate80Web, options=None):
    # Create Top Block instance
    tb = top_block_cls()

    try:
        tb.start()

        bokehgui.utils.run_server(tb, sizing_mode = "fixed",  widget_placement =  (0, 0), window_size =  (600, 900))
    finally:
        print("Exiting the simulation. Stopping Bokeh Server")
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
