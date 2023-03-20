#!/usr/bin/env python
"""
Event writing function compatible with spectrum writing functions
Glen Langston - 2019 September 14
"""
# -*- coding: utf-8 -*-
#
# Copyright 2018 Glen Langston, Quiet Skies <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# HISTORY
# 21Dec30 GIL shorten name to millisconds, not microseconds time
# 21Dec27 GIL finish all units in Hz, not MHz
# 21Dec22 GIL all units in Hz, not MHz
# 21Dec21 GIL finish up MJD + UTC processin
# 21Dec10 GIL separate MJD and UTC to increase precision of transfer
# 21DEC07 GIL reduce printout of events to once a minute
# 20DEC29 GIL recompute LST from event time
# 20JUN26 GIL expect VMJD, VCOUNT, NV tags
# 20JUN25 GIL try to eliminate duplicates; corrected get_tags call
# 19OCT11 GIL add test for duplicate events, sensed by same RMS as last event
# 19SEP14 GIL make gain processing compatible with ra_ascii_sink.py
# 19APR02 GIL cleanup typos
# 19MAR26 GIL take observers, telescope, gain1, azimuth, elevation as inputs
# 19MAR26 GIL record event peak and rms
# 19FEB14 GIL make tags more compatible with C++ tags
# 19JAN15 GIL initial version based on ra_ascii_sink

import os
import datetime
import numpy as np
from gnuradio import gr
import pmt
from gnuradio.radio_astro import radioastronomy

try:
    from . import jdutil
except:
    print("jdutil is needed to compute Modified Julian Days")
    print("try:")
    print("git clone https://github.com/jiffyclub/jdutil.py")
    print("")
    print("Good Luck! -- Glen")

class ra_event_sink(gr.sync_block):
    """
    Write Event File.  The input
    1) Time Sequence (vector) of I/Q complex samples
    2) Complex MJD of event
    The real and imaginary parts of the MJD sum to the actual MJD.
    Precision is lost during optimization in gnuradio value transfers.
    Parameters are
    1) ConfigFileName
    2) Vector length in Channels
    3) Frequency (Hz)
    4) Bandwidth (Hz)
    5) Record Flag
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, noteName, vlen, frequency, bandwidth, record, note, observer, telescope, device,
                 gain1, azimuth, elevation):
        """
        Initialize the event writing setup, recording the observing parameters
        """
        gr.sync_block.__init__(self,
                               name="ra_event_sink",
                               # inputs: time sequence of I,Q values,
                               # peak, rms, Event MJD
                               in_sig=[(np.complex64, int(vlen))],
                               out_sig=None, )
        vlen = int(vlen)
        self.vlen = vlen
        self.ecount = 1
        self.record = int(record)
        noteName = str(noteName)
        # first keep setup info in class header
        self.observer = str(observer)
        self.site = str(telescope)
        self.noteA = str(note)
        self.device = str(device)
        self.telaz = float(azimuth)
        self.telel = float(elevation)
        self.bandwidthHz = float(bandwidth)
        self.frequencyHz = float(frequency)
        self.gain1 = float(gain1)
        self.obs = radioastronomy.Spectrum(nChan=0, nSamples=vlen)
        # now transfer parameters to the observations file
        self.setupdir = "./"
        # read all generic setup info in the note file
        self.set_setup(noteName, doSave=True)
        # report newly discovered tags once
        self.lasttag = ""

    def set_sample_rate(self, bandwidthHz, doSave=True):
        """
        Set the sample rate for these event detections.
        The sample rate determines the time resolution
        """
        self.bandwidthHz = float(bandwidthHz)
        if self.bandwidthHz <= 10000.:
            print("Invalid Bandwidth: ", self.bandwidthHz)
            self.bandwidthHz = 2.5e6
        if self.bandwidthHz > 50.e6:
            print("Invalid Bandwidth: ", self.bandwidthHz)
            self.bandwidthHz = 10.e6
        print("Setting Bandwidth: %10.6f MHz" % (1.E-6*self.obs.bandwidthHz))
        self.obs.dt = 1./np.fabs(self.obs.bandwidthHz)
        t = -self.obs.dt * self.obs.refSample
        print("NChan = %5d; NSamples = %5d" % \
              (self.obs.nChan, self.obs.nSamples))
        print("N x   = %5d; N y      = %5d" % \
              (len(self.obs.xdata), len(self.obs.ydataA)))
        for iii in range(self.vlen):
            self.obs.xdata[iii] = t
            t = t + self.obs.dt
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_frequency(self, frequencyHz, doSave=True):
        """
        Set the frequency (Hz) of the center of the observations
        """
        frequencyHz = float(frequencyHz)
        if frequencyHz < 10000.:
            print("Invalid Frequency: %12.3f (Hz)" % (self.freqeuncyHz))
            frequencyHz + 2.5e6
            
        self.frequencyHz = frequencyHz
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_device(self, device, doSave=True):
        """
        Record the software defined radio device type and setup
        """
        self.obs.device = str(device)
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)    # read the parameters 

    def set_observer(self, observer, doSave=True):
        """
        Save Observer Names
        """
        self.observer = str(observer)
        self.obs.observer = self.observer
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_telescope(self, telescope, doSave=True):
        """
        Save Telescope Names
        """
        self.site = str(telescope)
        self.obs.site = self.site
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_note(self, noteA, doSave=True):
        """
        Save Note decribing the observations
        """
        self.noteA = str(noteA)
        self.obs.noteA = self.noteA
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_gain1(self, gain1, doSave=True):
        """
        Save SDR Gain parameter (dB)
        """
        self.gain1 = float(gain1)
        self.obs.gains[0] = float(gain1)
        print("Gain 1: %7.2f" % (self.gain1))
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_gain(self, gain1, doSave=True):
        """
        Save SDR Gain parameter (dB) alias
        """
        self.set_gain1( self, gain1, doSave)

    def set_telaz(self, telaz, doSave=True):
        """
        Save Telescope Azimuth
        """
        self.telaz = float(telaz)
        self.obs.telaz = self.telaz
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_vlen(self, vlen, doSave=True):
        """
        Save vector length
        """
        self.vlen = int(vlen)
        if self.vlen < 16:
            self.vlen = 16
            print("Vector too short: %3d, using %3d" % (int(vlen), self.vlen))
        self.obs.nSamples = self.vlen
        self.obs.xdata = np.zeros(self.vlen)
        self.obs.ydataA = np.zeros(self.vlen)
        self.obs.ydataB = np.zeros(self.vlen)
        self.obs.refsample = self.vlen/2.
        self.obs.count = 1
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_telel(self, telel, doSave=True):
        """
        Save Telescope Elevation
        """
        self.telel = float(telel)
        self.obs.telel = self.telel
        if doSave:
            self.obs.write_ascii_file(self.setupdir, self.noteName)

    def set_setup(self, noteName, doSave=True):
        """
        Read the setup files and initialize all values
        """
        self.noteName = str(noteName)
        noteParts = noteName.split('.')
        self.noteName = noteParts[0]+'.not'
        if len(noteParts) > 2:
            print('!!! Warning, unexpected Notes File name! ')
            print('!!! Using file: ', self.noteName)
        else:
            if os.path.isfile(self.noteName):
                print('Setup File       : ', self.noteName)
            else:
                if os.path.isfile("Watch.not"):
                    try:
                        import shutil
                        shutil.copyfile("Watch.not", self.noteName)
                        print("Created %s from file: Watch.not" % (self.noteName))
                    except:
                        pformat = "! Create the Note file %s, and try again !" 
                        print(pformat % (self.noteName))
        self.obs.read_spec_ast(self.setupdir + self.noteName)    # read the parameters 
        self.obs.datadir = "../events/"          # writing events not spectra
        self.obs.nSpec = 0             # not working with spectra
        self.obs.nChan = 0
        self.obs.nTime = 1             # working with time series
        self.obs.refSample = self.vlen/2    # event is in middle of time sequence
        self.obs.nSamples = self.vlen
        self.obs.ydataA = np.zeros(self.vlen)
        self.obs.ydataB = np.zeros(self.vlen)
        self.obs.xdata = np.zeros(self.vlen)
        now = datetime.datetime.utcnow()
        self.eventutc = now
        # set default events values
        self.emjd = 0.
        self.eutc = 0.
        self.epeak = 0.
        self.erms = 1.
        self.evector = 0
        self.env = 0
        self.eoffset = 0
        self.lastRms = 1.
        self.lastmjd = 0.
        self.lastvmjd = 0.
        # set of vector timing values
        self.vmjd = 0.
        self.vutc = 0.
        self.vcount = 0
        self.voffset = 0
        self.nv = 0
        self.obs.utc = now
        self.obs.site = self.site
        self.obs.noteA = self.noteA
        self.obs.device = self.device
        self.obs.telaz = self.telaz
        self.obs.telel = self.telel
        self.obs.centerFreqHz = self.frequencyHz
        self.obs.gains[0] = self.gain1

        self.obs.datadir = "../events/"          # writing events not spectra
        self.obs.noteB = "Event Detection"
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print('DataDir          : ', self.obs.datadir)
        self.set_sample_rate(self.bandwidthHz, doSave=doSave)

    def set_record(self, record):
        """
        When changing record status, need to update counters
        """
        if record == radioastronomy.INTWAIT: 
            print("Stop  Recording  : ")
            self.obs.writecount = 0
            self.ecount = 1
        # if changing state from recording to not recording
        elif self.record == radioastronomy.INTWAIT and record != radioastronomy.INTWAIT:
            print("Start Recording  : ")
        self.record = int(record)

    def get_record(self):
        """
        return the recording state (WAIT, RECORD, SAVE)
        """
        return self.record

    def forecast(self, noutput_items, ninputs):
        """
        forecast the number of spectra required to get required outputs
        inputs:
           noutput_items: number of desired output vectors
           ninputs: number of input data streams (ie block input ports).
        outputs:
           ninputs_needed: number of input vectors needed to produce an output
        """
        # create an integer array of zeros noutput_items long
        ninputs_needed = [0] * ninputs
        # for all input streams
        for i in range(ninputs):
            ninputs_needed[i] = self.gateway.history()
                
        return ninputs_needed
    # end of forecast()

    def work(self, input_items, output_items):
        """
        Work averages all input vectors and outputs one vector for each N inputs
        """
        inn = input_items[0]    # vectors of I/Q (complex) samples
        
        # get the number of input vectors
        nv = len(inn)           # number of events in this port

        # Get tags from ra_vevent block
#        print 'preparing to get tags: ', nv
#        tags = self.get_tags_in_window(0, 0, +self.vlen, pmt.to_pmt('event'))
#
        tags = self.get_tags_in_window(0, 0, +nv)
        if len(tags) > 0:
            for tag in tags:
                # print 'Event Tags detected in sink: ', len(tags)
                key = pmt.to_python(tag.key)
                value = pmt.to_python(tag.value)
                if key == 'MJD':
                    self.emjd = value
                    # print 'Tag MJD : %15.9f' % (self.emjd)
                elif key == 'UTC':
                    self.eutc = value;
                elif key == 'VMJD':
                    self.vmjd = value
                    # print 'Tag VMJD: %15.9f' % (self.emjd)
                elif key == 'VUTC':
                    self.vutc = value
                elif key == 'NV':
                    self.nv = value
                elif key == 'VCOUNT':
                    self.vcount = value
                elif key == 'EVECTOR':
                    self.evector = value
                    # print 'Tag EVECTOR: %15.9f' % (self.emjd)
                elif key == 'ENV':
                    self.env = value
                elif key == 'EOFFSET':
                    self.eoffset = value
                elif key == 'VOFFSET':
                    self.voffset = value
                elif key == 'PEAK':
                    self.epeak = value
                    # print 'Tag PEAK: %7.4f' % (self.epeak)
                elif key == 'RMS':
                    self.erms = value
                    # print 'Tag RMs : %7.4f' % (self.erms)
                elif key != self.lasttag:
                    print('Unknown Tag: ', key, value)
                    self.lasttag = key

        if self.vmjd > self.lastvmjd:
            # print('New Vector Count tag: %15.9f %12d %3d' % \
            #    (self.vmjd, self.vcount, self.nv))
            self.lastvmjd = self.vmjd
            
        nout = 0
        # assume events are not too rapid, only process last in block
        if nv > 0:
            i = nv - 1
            # get the length of one input
            samples = inn[i]
            # if new mjd 
            if self.emjd > self.lastmjd:
                self.lastmjd = self.emjd
                self.obs.ydataA = samples.real
                self.obs.ydataB = samples.imag
                utc = jdutil.mjd_to_datetime(self.emjd)
                self.obs.utc = utc
                # recompute LST, RA, Dec from event time
                self.obs.azel2radec()
                self.obs.emjd = self.emjd
                self.obs.epeak = self.epeak
                self.obs.erms = self.erms
                # create file name from event time
                strnow = utc.isoformat()
                datestr = strnow.split('.')
                daypart = datestr[0]
                if len(datestr) > 1:
                    milliseconds = datestr[1]            # need to add milliseconds to file name
                else:
                    milliseconds = "000"                 # rare case of no milliseconds
                milliseconds = milliseconds[0:3]     # millisconds to 100 micro
                microseconds = "%04d00" % int(milliseconds)
                yymmdd = daypart[2:19]
                # try to remove duplicate tags following
                tags = self.get_tags_in_window(0, 0, +2*self.vlen)
                if self.record == radioastronomy.INTRECORD:
#                    if self.erms == self.lastRms:
#                        #print("Duplicate Event, not writing!")
#                        print("RMS == last RMS: %7.3f" % (self.erms))
#                        continue;
                    #remove : from time
                    # if new version of code with sepearate UTC part of time
                    # eutc is in untis of fractions of a day
                    if self.eutc != 0.:
                        hour,minute,sec,micro = jdutil.days_to_hmsm( self.eutc)
                        emjd = int(self.emjd)
                        hhmmss = "%02d%02d%02d" % (hour,minute,sec)
                        jd = jdutil.mjd_to_jd( self.emjd)
                        yy,mm,dd = jdutil.jd_to_date(jd)
                        yy = yy % 100   # only need the last 2 digits
                        dd = int(dd)
                        yymmdd = "%02d-%02d-%02d" % (yy,mm, dd)
                        microseconds = "%06d" % micro
                        if self.ecount < 2:
                            print("MJD: %.0f %0.9f" % ( emjd, self.eutc))
                            print("MJD: %0.9f" % ( self.emjd))
                        self.emjd = float(emjd) + float(self.eutc)
                        self.eutc = float(0.0)
                        milliseconds = microseconds[0:3]
                    else:
                        yymmdd = yymmdd.replace(":", "")
                    yymmdd = yymmdd + "T" + hhmmss + "_" + milliseconds
                    outname = yymmdd + '.eve'   # tag as an event
                    self.obs.writecount = self.obs.writecount + 1
                    # need to keep track of total number of spectra averaged
                    self.obs.write_ascii_file(self.obs.datadir, outname)
                    print('\a')  # ring the terminal bell
                self.ecount = self.ecount + 1
                self.lastRms = self.erms
            nout = nout+1
            # try to prevent duplicate 
            # output latest event count
        # report all vectors processed
        return nv
    # end event_sink()


