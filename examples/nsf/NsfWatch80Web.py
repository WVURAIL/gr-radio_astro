#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Web display Nsf Detect: SDRPlay 8MHz Astronomical Obs.
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




class NsfWatch80Web(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Web display Nsf Detect: SDRPlay 8MHz Astronomical Obs.", catch_exceptions=True)
        self.plot_lst = []
        self.widget_lst = []

        ##################################################
        # Variables
        ##################################################
        self.ObsName = ObsName = "Integrate80"
        self.ConfigFile = ConfigFile = ObsName+".conf"
        self._IF_attn_save_config = configparser.ConfigParser()
        self._IF_attn_save_config.read(ConfigFile)
        try: IF_attn_save = self._IF_attn_save_config.getfloat('main', 'ifattn')
        except: IF_attn_save = 30
        self.IF_attn_save = IF_attn_save
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(ConfigFile)
        try: Bandwidths = self._Bandwidths_config.getfloat('main', 'bandwidth')
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
        self.IF_attn = IF_attn = float(IF_attn_save)
        self._Gain1s_config = configparser.ConfigParser()
        self._Gain1s_config.read(ConfigFile)
        try: Gain1s = self._Gain1s_config.getfloat('main', 'gain1')
        except: Gain1s = 49.
        self.Gain1s = Gain1s
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(ConfigFile)
        try: Frequencys = self._Frequencys_config.getfloat('main', 'Frequency')
        except: Frequencys = 1420.4e6
        self.Frequencys = Frequencys
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
        self.Bandwidth_val = Bandwidth = float(Bandwidths)
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(ConfigFile)
        try: Azimuth_save = self._Azimuth_save_config.getfloat('main', 'azimuth')
        except: Azimuth_save = 90.
        self.Azimuth_save = Azimuth_save
        self.samp_rate = samp_rate = Bandwidth
        self.observer = observer = observers_save
        self.nsigma_val = nsigma = float(nsigmas)
        self.nAve = nAve = int(nAves)
        self.fftsize = fftsize = fftsize_save
        self.Telescope_val = Telescope = telescope_save
        self.Samples_val = Samples = int(fftsize_save)
        self.Record_val = Record = True
        self.Observer_val = Observer = observers_save
        self.IQMode = IQMode = bool(IQMode_save)
        self.H1 = H1 = 1420.406E6
        self.Gain3 = Gain3 = IF_attn
        self.Gain2 = Gain2 = IF_attn
        self.Gain1 = Gain1 = Gain1s
        self.Frequency_val = Frequency = float(Frequencys)
        self.Explanation_val = Explanation = 'NSF Watch Horn Radio Telescope with SDRPlay'
        self.Elevation_val = Elevation = float(Elevation_save)
        self.Device = Device = device_save
        self.DebugOn = DebugOn = bool(DebugOn_save)
        self.DcOffsetMode = DcOffsetMode = bool(DcOffset_save)
        self.DabNotch = DabNotch = bool(DabNotch_save)
        self.BroadcastNotch = BroadcastNotch = bool(BroadcastNotch_save)
        self.BiasOn = BiasOn = bool(BiasOn_save)
        self.Azimuth_val = Azimuth = float(Azimuth_save)

        ##################################################
        # Blocks
        ##################################################
        self.nsigma = bokehgui.label(self.widget_lst, str(nsigma), 'N Sigma' +": ")
        self.Telescope = bokehgui.label(self.widget_lst, str(Telescope), 'Telescope' +": ")
        self.Record = bokehgui.label(self.widget_lst, str(Record), 'Record' +": ")
        self.Observer = bokehgui.label(self.widget_lst, str(Observer), 'Observer' +": ")
        self.Frequency = bokehgui.label(self.widget_lst, str(Frequency), 'Frequency' +": ")
        self.Elevation = bokehgui.label(self.widget_lst, str(Elevation), 'Elevation' +": ")
        self.Bandwidth = bokehgui.label(self.widget_lst, str(Bandwidth), 'Bandwidth' +": ")
        self.Azimuth = bokehgui.label(self.widget_lst, str(Azimuth), 'Azimuth' +": ")
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
        self.radio_astro_vmedian_0_0_1_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0_1 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_vmedian_0 = radio_astro.vmedian(fftsize, 4)
        self.radio_astro_ra_event_sink_0 = radio_astro.ra_event_sink(ObsName+"Event.not", fftsize, Frequency, Bandwidth, True, 'Event Detection', Observer, Telescope, Device, float(IF_attn), Azimuth, Elevation)
        self.radio_astro_ra_ascii_sink_0 = radio_astro.ra_ascii_sink(ObsName+".not", observer, fftsize, Frequency, Bandwidth, Azimuth, Elevation, Record, 0, 4**5, nAve, telescope_save, device_save, float(IF_attn), float(Gain2), float(Gain1))
        self.radio_astro_detect_0 = radio_astro.detect(fftsize, nsigma, Frequency, Bandwidth, fftsize/Bandwidth, True)
        self.fft_vxx_0_0 = fft.fft_vcc(fftsize, True, window.hamming(fftsize), True, 1)
        self.bokehgui_vector_sink_x_0 = bokehgui.vec_sink_c_proc(fftsize,
                             "",                     1                    )

        labels = ['I', 'Q', '', '', '',
                  '', '', '', '', '']
        legend_list = []

        for i in  range(       2*1    ):
          if len(labels[i]) == 0:
            if(i % 2 == 0):
              legend_list.append("Re{{Data {0}}}".format(i/2))
            else:
              legend_list.append("Im{{Data {0}}}".format(i/2))
          else:
            legend_list.append(labels[i])

        self.bokehgui_vector_sink_x_0_plot = bokehgui.vec_sink_c(self.plot_lst, self.bokehgui_vector_sink_x_0, update_time = 1000, legend_list = legend_list, is_message =False)

        self.bokehgui_vector_sink_x_0_plot.set_y_axis([-.9, .9])
        self.bokehgui_vector_sink_x_0_plot.set_y_label('Inensity' + '(' +'Counts'+')')
        self.bokehgui_vector_sink_x_0_plot.set_x_label('Time' + '(' +"Microseconds"+')')

        self.bokehgui_vector_sink_x_0_plot.set_x_values((0,1))
        self.bokehgui_vector_sink_x_0_plot.enable_grid(False)
        self.bokehgui_vector_sink_x_0_plot.enable_axis_labels(True)
        self.bokehgui_vector_sink_x_0_plot.enable_legend(True)
        self.bokehgui_vector_sink_x_0_plot.set_layout(*((0,1,1,1)))
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        styles = ["solid", "solid", "solid", "solid", "solid",
                  "solid", "solid", "solid", "solid", "solid"]
        markers = [None, 'sx', None, None, None,
                   None, None, None, None, None]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in  range(  2*1  ):
            self.bokehgui_vector_sink_x_0_plot.format_line(i, colors[i], widths[i], styles[i], markers[i], alphas[i])
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fftsize)
        self.Samples = bokehgui.label(self.widget_lst, str(Samples), 'N samples' +": ")
        self.Explanation = bokehgui.label(self.widget_lst, str(Explanation), 'Explanation' +": ")


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.radio_astro_vmedian_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.radio_astro_detect_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.bokehgui_vector_sink_x_0, 0))
        self.connect((self.radio_astro_detect_0, 0), (self.radio_astro_ra_event_sink_0, 0))
        self.connect((self.radio_astro_ra_ascii_sink_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.radio_astro_vmedian_0, 0), (self.radio_astro_ra_ascii_sink_0, 0))
        self.connect((self.radio_astro_vmedian_0_0, 0), (self.radio_astro_vmedian_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_0, 0), (self.radio_astro_vmedian_0_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_1, 0), (self.radio_astro_vmedian_0_0_1_0, 0))
        self.connect((self.radio_astro_vmedian_0_0_1_0, 0), (self.radio_astro_vmedian_0_0_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_stream_to_vector_0_0, 0))


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

    def get_IF_attn_save(self):
        return self.IF_attn_save

    def set_IF_attn_save(self, IF_attn_save):
        self.IF_attn_save = IF_attn_save
        self.set_IF_attn(float(self.IF_attn_save))

    def get_Bandwidths(self):
        return self.Bandwidths

    def set_Bandwidths(self, Bandwidths):
        self.Bandwidths = Bandwidths
        self.Bandwidth.set_value(float(self.Bandwidths))

    def get_telescope_save(self):
        return self.telescope_save

    def set_telescope_save(self, telescope_save):
        self.telescope_save = telescope_save
        self.Telescope.set_value(self.telescope_save)
        self.radio_astro_ra_ascii_sink_0.set_site(self.telescope_save)

    def get_observers_save(self):
        return self.observers_save

    def set_observers_save(self, observers_save):
        self.observers_save = observers_save
        self.Observer.set_value(self.observers_save)
        self.set_observer(self.observers_save)

    def get_nsigmas(self):
        return self.nsigmas

    def set_nsigmas(self, nsigmas):
        self.nsigmas = nsigmas
        self.nsigma.set_value(float(self.nsigmas))

    def get_nAves(self):
        return self.nAves

    def set_nAves(self, nAves):
        self.nAves = nAves
        self.set_nAve(int(self.nAves))

    def get_fftsize_save(self):
        return self.fftsize_save

    def set_fftsize_save(self, fftsize_save):
        self.fftsize_save = fftsize_save
        self.Samples.set_value(int(self.fftsize_save))
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
        self.radio_astro_ra_ascii_sink_0.set_gain1(float(self.IF_attn))
        self.radio_astro_ra_event_sink_0.set_gain1(float(self.IF_attn))

    def get_Gain1s(self):
        return self.Gain1s

    def set_Gain1s(self, Gain1s):
        self.Gain1s = Gain1s
        self.set_Gain1(self.Gain1s)

    def get_Frequencys(self):
        return self.Frequencys

    def set_Frequencys(self, Frequencys):
        self.Frequencys = Frequencys
        self.Frequency.set_value(float(self.Frequencys))

    def get_Elevation_save(self):
        return self.Elevation_save

    def set_Elevation_save(self, Elevation_save):
        self.Elevation_save = Elevation_save
        self.Elevation.set_value(float(self.Elevation_save))

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

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self.Bandwidth.set_value(float(self.Bandwidths))
        self._Bandwidths_config = configparser.ConfigParser()
        self._Bandwidths_config.read(self.ConfigFile)
        if not self._Bandwidths_config.has_section('main'):
        	self._Bandwidths_config.add_section('main')
        self._Bandwidths_config.set('main', 'bandwidth', str(self.Bandwidth))
        self._Bandwidths_config.write(open(self.ConfigFile, 'w'))
        self.set_samp_rate(self.Bandwidth)
        self.radio_astro_detect_0.set_bw(self.Bandwidth)
        self.radio_astro_ra_ascii_sink_0.set_bandwidth(self.Bandwidth)
        self.radio_astro_ra_event_sink_0.set_sample_rate(self.Bandwidth)

    def get_Azimuth_save(self):
        return self.Azimuth_save

    def set_Azimuth_save(self, Azimuth_save):
        self.Azimuth_save = Azimuth_save
        self.Azimuth.set_value(float(self.Azimuth_save))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate)

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

    def get_nsigma(self):
        return self.nsigma

    def set_nsigma(self, nsigma):
        self.nsigma = nsigma
        self.nsigma.set_value(float(self.nsigmas))
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
        self._fftsize_save_config = configparser.ConfigParser()
        self._fftsize_save_config.read(self.ConfigFile)
        if not self._fftsize_save_config.has_section('main'):
        	self._fftsize_save_config.add_section('main')
        self._fftsize_save_config.set('main', 'fftsize', str(self.fftsize))
        self._fftsize_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_detect_0.set_vlen(self.fftsize)
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
        self.Telescope.set_value(self.telescope_save)
        self._telescope_save_config = configparser.ConfigParser()
        self._telescope_save_config.read(self.ConfigFile)
        if not self._telescope_save_config.has_section('main'):
        	self._telescope_save_config.add_section('main')
        self._telescope_save_config.set('main', 'telescope', str(self.Telescope))
        self._telescope_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_event_sink_0.set_telescope(self.Telescope)

    def get_Samples(self):
        return self.Samples

    def set_Samples(self, Samples):
        self.Samples = Samples
        self.Samples.set_value(int(self.fftsize_save))

    def get_Record(self):
        return self.Record

    def set_Record(self, Record):
        self.Record = Record
        self.Record.set_value(True)
        self.radio_astro_ra_ascii_sink_0.set_record(self.Record)

    def get_Observer(self):
        return self.Observer

    def set_Observer(self, Observer):
        self.Observer = Observer
        self.Observer.set_value(self.observers_save)
        self.radio_astro_ra_event_sink_0.set_observer(self.Observer)

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

    def get_H1(self):
        return self.H1

    def set_H1(self, H1):
        self.H1 = H1

    def get_Gain3(self):
        return self.Gain3

    def set_Gain3(self, Gain3):
        self.Gain3 = Gain3

    def get_Gain2(self):
        return self.Gain2

    def set_Gain2(self, Gain2):
        self.Gain2 = Gain2
        self.radio_astro_ra_ascii_sink_0.set_gain2(float(self.Gain2))
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
        self.radio_astro_ra_ascii_sink_0.set_gain3(float(self.Gain1))
        self.sdrplay3_rsp1a_0.set_gain(-self.Gain1, 'RF')

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self.Frequency.set_value(float(self.Frequencys))
        self._Frequencys_config = configparser.ConfigParser()
        self._Frequencys_config.read(self.ConfigFile)
        if not self._Frequencys_config.has_section('main'):
        	self._Frequencys_config.add_section('main')
        self._Frequencys_config.set('main', 'Frequency', str(self.Frequency))
        self._Frequencys_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_detect_0.set_freq(self.Frequency)
        self.radio_astro_ra_ascii_sink_0.set_frequency(self.Frequency)
        self.radio_astro_ra_event_sink_0.set_frequency(self.Frequency)
        self.radio_astro_ra_event_sink_0.set_frequency(self.Frequency)
        self.sdrplay3_rsp1a_0.set_center_freq(self.Frequency)

    def get_Explanation(self):
        return self.Explanation

    def set_Explanation(self, Explanation):
        self.Explanation = Explanation
        self.Explanation.set_value('NSF Watch Horn Radio Telescope with SDRPlay')

    def get_Elevation(self):
        return self.Elevation

    def set_Elevation(self, Elevation):
        self.Elevation = Elevation
        self.Elevation.set_value(float(self.Elevation_save))
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
        self.Azimuth.set_value(float(self.Azimuth_save))
        self._Azimuth_save_config = configparser.ConfigParser()
        self._Azimuth_save_config.read(self.ConfigFile)
        if not self._Azimuth_save_config.has_section('main'):
        	self._Azimuth_save_config.add_section('main')
        self._Azimuth_save_config.set('main', 'azimuth', str(self.Azimuth))
        self._Azimuth_save_config.write(open(self.ConfigFile, 'w'))
        self.radio_astro_ra_ascii_sink_0.set_azimuth(self.Azimuth)
        self.radio_astro_ra_event_sink_0.set_telaz(self.Azimuth)




def main(top_block_cls=NsfWatch80Web, options=None):
    # Create Top Block instance
    tb = top_block_cls()

    try:
        tb.start()

        bokehgui.utils.run_server(tb, sizing_mode = "fixed",  widget_placement =  (0, 0), window_size =  (600, 800))
    finally:
        print("Exiting the simulation. Stopping Bokeh Server")
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
