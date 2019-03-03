#!/usr/bin/env python
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
# 19FEB14 GIL make tags more compatible with C++ tags
# 19JAN15 GIL initial version based on ra_ascii_sink

import os
import sys
import datetime
import numpy as np
from gnuradio import gr
import radioastronomy
import pmt

try:
    import jdutil
except:
    print "jdutil is needed to compute Modified Julian Days"
    print "try:"
    print "git clone https://github.com/jiffyclub/jdutil.py"
    print ""
    print "Good Luck! -- Glen"

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
    3) Bandwidth (MHz)
    4) Record Flag
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, noteName, vlen, bandwidth, record):
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
        self.obs = radioastronomy.Spectrum()
        self.setupdir = "./"
        noteParts = noteName.split('.')
        self.noteName = noteParts[0]+'.not'
        if len(noteParts) > 2:
            print '!!! Warning, unexpected Notes File name! '
            print '!!! Using file: ', self.noteName
        else:
            if os.path.isfile( self.noteName):
                print 'Setup File       : ', self.noteName
            else:
                if os.path.isfile( "Watch.not"):
                    try:
                        import shutil
                        shutil.copyfile( "Watch.not", self.noteName)
                        print "Created %s from file: Watch.not" % (self.noteName)
                    except:
                        pformat = "! Create the Note file %s, and try again !" 
                        print pformat % (self.noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters

        # prepare to Event get messages
#        print 'Registered event on input port of sink'

#        self.set_tag_propagation_policy(gr.TPP_ALL_TO_ALL)
#        self.set_msg_handler(pmt.intern('in_port'), self.event_handler)

        self.obs.datadir = "../events/"          # writing events not spectra
        self.obs.noteB = "Event Detection"
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print 'DataDir          : ', self.obs.datadir
        self.obs.nSpec = 0             # not working with spectra
        self.obs.nChan = vlen
        self.obs.nTime = 1             # working with time series
        self.obs.nSamples = vlen
        vlen2 = int(vlen/2)
        self.obs.refSample = vlen2     # event is in middle of time sequence
        self.obs.ydataA = np.zeros(vlen, dtype=np.complex64)
        self.obs.xdata = np.zeros(vlen)
        now = datetime.datetime.utcnow()
        self.eventutc = now
        self.obs.utc = now
        self.eventmjd = jdutil.datetime_to_mjd( now)
        self.lastmjd = self.eventmjd
        self.emagnitude = 0.
        self.erms = 0.
        self.set_sample_rate( bandwidth)

    def event_handler(self, msg):
        """
        Receive the Peak, RMS and MJD on the input stream
        """
        print 'Event Message received: '
        # Grab packet PDU data                                                                                                     
        self.eventmjd = pmt.from_float(msg)
        print 'MJD: %15.6f ' % (self.eventmjd)
        return

    def forecast(self, noutput_items, ninput_items): #forcast is a no op
        """
        The work block always processes all inputs
        """
        ninput_items = noutput_items
        return ninput_items

    def set_sample_rate(self, bandwidthMHz):
        bandwidthMHz = np.float(bandwidthMHz)
        if bandwidthMHz <= 0.0001:
            print "Invalid Bandwidth: ", bandwidthMHz
            bandwidthMHz = 1.
        if bandwidthMHz >= 1000.:
            print "Invalid Bandwidth: ", bandwidthMHz
            bandwidthMHz = 1.
        self.bandwidth = bandwidthMHz         # header units MHz
        self.obs.bandwidthHz = bandwidthMHz*1.E6  # observation units Hz
        print "Setting Bandwidth: %10.6f MHz" % (1.E-6*self.obs.bandwidthHz)
        self.obs.dt = 1./np.fabs(self.obs.bandwidthHz)
        t = -self.obs.dt * self.obs.refSample
        for iii in range(self.vlen):
            self.obs.xdata[iii] = t
            t = t + self.obs.dt

    def set_setup(self, noteName):
        """
        Read the setup files and initialize all values
        """
        self.noteName = str(noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters 
        self.obs.datadir = "../events/"          # writing events not spectra
        self.obs.nSpec = 0             # not working with spectra
        self.obs.nChan = vlen
        self.obs.nTime = 1             # working with time series
        self.obs.refSample = vlen/2    # event is in middle of time sequence
        self.obs.nSamples = vlen
        self.obs.ydataA = np.zeros(vlen, dtype=np.complex64)
        self.obs.xdata = np.zeros(vlen)
        now = datetime.datetime.utcnow()
        self.eventutc = now
        self.obs.utc = now
        self.setupdir = "./"
        self.set_sample_rate( self.bandwidthMHz)
    
    def set_record(self, record):
        """ 
        When changing record status, need to update counters
        """
        if record == radioastronomy.INTWAIT: 
            print "Stop  Recording  : "
            self.obs.writecount = 0
            self.ecount = 1
        # if changing state from recording to not recording
        elif self.record == radioastronomy.INTWAIT and record != radioastronomy.INTWAIT:
            print "Start Recording  : "
        self.record = int(record)

    def get_record(self):
        """
        return the recording state (WAIT, RECORD, SAVE)
        """
        return self.record

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
        tags = self.get_tags_in_window(0, 0, +self.vlen)
#
        if len(tags) > 0:
            for tag in tags:
#            print 'Event Tags detected in sink: ', len(tags)
                key = pmt.to_python(tag.key)
                value = pmt.to_python(tag.value)
                if key == 'MJD':
                    self.eventmjd = value
#                    print 'Tag MJD : %15.9f' % (self.eventmjd)
                elif key == 'PEAK':
                    self.emagnitude = value
#                    print 'Tag PEAK: %7.4f' % (self.emagnitude)
                elif key == 'RMS':
                    self.erms = value
#                    print 'Tag RMs : %7.4f' % (self.erms)
                else:
                    print 'Unknown Tag: ', value
        nout = 0
        for i in range(nv):
            # get the length of one input
            samples = inn[i]
            # if new mjd 
            if self.eventmjd > self.lastmjd:
                self.lastmjd = self.eventmjd
                self.obs.ydataA = samples.real
                self.obs.ydataB = samples.imag
                utc = jdutil.mjd_to_datetime( self.eventmjd)
                self.obs.utc = utc
                # create file name from event time
                strnow = utc.isoformat()
                datestr = strnow.split('.')
                daypart = datestr[0]
                yymmdd = daypart[2:19]
#                print 'Sink Event: ', self.ecount
#                print 'Sink Utc : ', self.obs.utc
#                print 'Sink MJD : %15.9f' % (self.eventmjd)
#                print 'Sink days: %12.6f + %12.6f ' % (fdays, hours)
#                print 'Sink Magnitude: ', peaks, ' +/- ', rmss
                if self.record == radioastronomy.INTRECORD:
                    #remove : from time
                    yymmdd = yymmdd.replace(":", "")
                    outname = yymmdd + '.eve'   # tag as an event
                    self.obs.writecount = self.obs.writecount + 1
                    # need to keep track of total number of spectra averaged
                    tempcount = self.obs.count
                    self.obs.write_ascii_file( self.obs.datadir, outname)
                    print('\a')  # ring the terminal bell
                self.ecount = self.ecount + 1
            nout = nout+1
            # output latest event count
        return nout
    # end event_sink()


