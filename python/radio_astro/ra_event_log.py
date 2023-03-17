#!/usr/bin/env python
# This python program logs detected events, within the
# Gnuradio Companion environment
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
# 23Mar13 GIL no more np.float() or np.int()
# 21DEC27 GIL finish all frequencies in Hz
# 21DEC22 GIL all frequencies in Hz
# 21DEC21 GIL take integer part of MJD if UTC is present
# 21DEC07 GIL reduce prints to once a minute
# 20NOV24 GIL another try at fixing log mjds
# 20SEP17 GIL fix creating new logs every day
# 20AUG28 GIL move event logs to a separate directory
# 20JUN26 GIL log vector tags to deterine accurate time
# 19FEB14 GIL make tag labels compatible with C++ tags
# 19JAN19 GIL initial version based on ra_event_sink

import os
import sys
import datetime
import numpy as np
from gnuradio import gr
import pmt

class ra_event_log(gr.sync_block):
    """
    Event Log writes a summary of detected events to a log file.  The input
    1) vector of I,Q (complex) samples centered in time on the event
    The Event MJD, Peak and RMS are passed as tags
    Parameters are
    1) LogFileName
    2) Note on Purpose of event detection
    2) Vector length in Channels
    3) Bandwidth (Hz)
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, logname, note, vlen, bandwidth):
        gr.sync_block.__init__(self,
                               name="ra_event_log",              
                               # inputs: 
                               # peak, rms, Event MJD
                               in_sig=[(np.complex64, int(vlen))],
                               # no outputs
                               out_sig=None, )
        vlen = int(vlen)
        self.vlen = vlen
        self.ecount = 0
        self.lastmjd = 0.
        self.lastvmjd = 0.
        self.printmjd = 0.
        self.bandwidth = bandwidth
        now = datetime.datetime.utcnow()
        self.startutc = now
        self.setupdir = "./"
        self.logdir = "../eventlog"
        self.logname = str(logname)
        self.lastlogname = str(logname)
        self.fullname = self.logdir
        self.logmjd = 0.
        self.lastlogmjd = 0.
        self.emjd = 0.
        self.eutc = 0.
        self.epeak = 0.
        self.erms = 0.
        self.evector = 0
        self.env = 0
        self.eoffset = 0
        self.voffset = 0
        self.vmjd = 0.
        self.vutc = 0.
        self.vcount = 0
        self.nv = 0
        self.lasttag = ""
        self.lastprintmjd = 0         # keep track of prints
        self.printdelta = (1./1440.)  # print every minute, 1440 minutes/day
        self.note = str(note)
        self.pformat = "%18.12f %15d %05d %10.3f %3d %5d %10.6f %10.6f %5d %5d\n" 
        self.vformat = "%18.12f %15d %05d %10.3f %3d %5d \n" 
        self.set_note( note)          # should set all values before opening log file
        self.set_sample_rate( bandwidth)
        self.set_logname(logname)
        
    def set_vlen(self, vlen):
        """
        Save vector length
        """
        self.vlen = int(vlen)

    def set_sample_rate(self, bandwidth):
        """
        Set the sample rate to know the time resolution
        """
        bandwidth = float(bandwidth)
        if bandwidth < 10000.:
            print("Invalid Bandwidth: ", bandwidth)
            return
        self.bandwidth = bandwidth
        print("Setting Bandwidth: %10.6f MHz" % (1.E-6*self.bandwidth))

    def get_sample_rate(self):
        """
        Return the sample rate to know the time resolution
        """
        return self.bandwidth

    def get_event_count(self):
        """
        Return the count of events so far logged
        """
        return self.ecount

    def create_logname(self):
        """ 
        Create the Event log name from the current date and time
        """
        now = datetime.datetime.utcnow()
        now = str(now)
        datestr = now.split('.')    # get rid of fractions of a second
        daypart = datestr[0]         
        yymmdd = daypart[2:10]      # 2019-01-19T01:23:45 -> 19-01-19

        logname = "Event-%s.log" % (yymmdd)  # create from date
        return logname
        
    def set_logname(self, logname):
        """
        Read the setup files and initialize all values
        """

        logname = str(logname)
        if logname == "":   # if no log file name provided
            logname = self.create_logname()
            
        self.logname = logname
        # if file is same as last, the file is already initialized
        if self.lastlogname == self.logname:
            return

        # create the log directory if it does not exist
        if not os.path.exists(self.logdir):
            try:
                os.makedirs(self.logdir)
            except:
                print("Can not Create Log Directory: $s" % (self.logdir))
                exit()
        self.fullname = self.logdir + "/" + self.logname            

        self.lastlogname = logname

        # if file already exists, no need to add header
        if os.path.exists(self.fullname):
            print("Using Event Log: %s" % (self.lastlogname))
            return
            
        with open( self.fullname, "w") as f:
            outline = "# Event Log Opened on %s\n" % (self.startutc.isoformat())
            f.write(outline)
            outline = "# %s\n" % (self.note)
            f.write(outline)
            outline = "# bandwidth = %15.6f Hz\n" % (self.bandwidth)
            f.write(outline)
            outline = "# vlen      = %6d\n" % (self.vlen)
            f.write(outline)
            outline = "#E       MJD           vector #   second  micro.sec  NV  Zero#   Peak       RMS    Event# Offset\n"
            f.write(outline)
            outline = "#V       MJD           vector #   second  micro.sec  NV  Zero#\n"
            f.write(outline)
            f.close()
        # save new log for checking name change
        print("Created New Event Log: %s" % (self.lastlogname))
        return
    
    def set_note(self, note):
        """
        Update the note for the event log
        """
        self.note = str(note)
        return

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
        
        # get any tags of a new detected event
#        tags = self.get_tags_in_window(0, 0, +self.vlen, pmt.to_pmt('event'))
        tags = self.get_tags_in_window(0, 0, +nv)
        # if there are tags, then a new event was detected
        if len(tags) > 0:
            for tag in tags:
#                print 'Tag: ', tag
                key = pmt.to_python(tag.key)
                value = pmt.to_python(tag.value)
                if key == 'MJD':
                    self.emjd = value
#                    print 'Tag MJD : %15.9f' % (self.emjd)
                if key == 'UTC':
                    self.eutc = value
#                    print 'Tag UTC : %15.9f' % (self.eutc)
                elif key == 'VMJD':
                    self.vmjd = value
                    # print 'Tag VMJD: %15.9f' % (self.vmjd)
                elif key == 'VUTC':
                    self.vutc = value
                    # print 'Tag VMJD: %15.9f' % (self.vmjd)
                elif key == 'PEAK':
                    self.epeak = value
#                    print 'Tag PEAK: %7.4f' % (self.epeak)
                elif key == 'RMS':
                    self.erms = value
#                    print 'Tag RMs : %7.4f' % (self.erms)
                elif key == 'VCOUNT':
                    self.vcount = value
                    # print 'Tag VCOUNT: %15.9f' % (self.vcount)
                elif key == 'EVECTOR':
                    self.evector = value
                    # print 'Tag VMJD: %15.9f' % (self.emjd)
                elif key == 'ENV':
                    self.env = value
                elif key == 'EOFFSET':
                    self.eoffset = value
                elif key == 'VOFFSET':
                    self.voffset = value
                elif key == 'NV':
                    self.nv = value
                    # print 'Tag NV  : %15d' % (self.nv)
                elif key != self.lasttag:
                    print('Unknown Tag: ', key, value)
                    self.lasttag = key
        # if receive an event utc
        if self.eutc != 0.:
            if self.ecount < 2:
                print("Event %.9f" % (self.emjd))
            self.emjd = float(int(self.emjd))
            if self.ecount < 2:
                print("Event %.0f %0.9f" % (self.emjd, self.eutc))
            # transfer to 
            self.emjd += self.eutc
            self.eutc = 0.
        if self.vutc != 0.:
            if self.ecount < 2:
                print("Event %.9f" % (self.vmjd))
            self.vmjd = float(int(self.vmjd))
            if self.ecount < 2:
                print("Event %.0f %0.9f" % (self.vmjd, self.vutc))
            # transfer to 
            self.vmjd += self.vutc
            self.vutc = 0.
        i = nv - 1
        # expect only one event in tag group
        if i > -1:
            # if a new Modified Julian Day, then an event was detected
            if self.emjd > self.lastmjd:
                # log the event
                self.ecount = self.ecount + 1
                if self.emjd - self.lastprintmjd > self.printdelta:
                    print("Event : %15.9f %16d %9.4f %8.4f %4d" % \
                          (self.emjd, self.evector, self.epeak, \
                           self.erms, self.ecount))
                    self.lastprintmjd = self.emjd
                # round down to integer mjd
                self.logmjd = int(self.emjd)
                seconds = (self.emjd - self.logmjd)*86400.
                isecond = int(seconds)
                microseconds = (seconds - isecond) * 1.e6
                outline = self.pformat % (self.emjd, self.evector, isecond, microseconds, self.env, self.voffset, self.epeak, self.erms, self.ecount, self.eoffset)
                # create log file names here, if new mjd
                if self.lastlogmjd != self.logmjd:
                    self.set_logname( "")
                    self.lastlogmjd = self.logmjd
                self.lastmjd = self.emjd
                # now write the log entry
                try:
                    # confirm log name is current, sets the full name
                    # based on date
                    with open( self.fullname, "a+") as f:
                        f.write(outline)
                        f.close()
                except:
                    print("Can Not Log")
                
            # also log vector time tags to interpolate accurate time
            if self.vmjd > self.lastvmjd:
                # log the time of this vector
                if self.vmjd > self.printmjd:
                    print("Vector: %15.9f %16d %4d %5d" % (self.vmjd, self.vcount, self.nv, self.voffset))
                    # print every few minutes (24*60 = 1440 minutes in a day)
                    self.printmjd = self.vmjd + (2./1440.)   
                imjd = int(self.vmjd)
                seconds = (self.vmjd - imjd)*86400.
                isecond = int(seconds)
                microseconds = (seconds - isecond) * 1.e6
                self.lastvmjd = self.vmjd
                outline = self.vformat % (self.vmjd, self.vcount, isecond, microseconds, self.nv, self.voffset)
                try:
                    # confirm log name is current, sets the full name
                    # based on date
                    with open( self.fullname, "a+") as f:
                        f.write(outline)
                        f.close()
                except:
                    print("Can Not Log")
                
            # end for all input events
        return nv
    # end event_log()


