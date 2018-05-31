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
# 18APR20 GIL add gain1, gain2 and gain3
# 18APR19 GIL fix minor typos
# 18APR18 GIL update arguments
# 18APR13 GIL first functioning version

import os
import numpy as np
import datetime
import copy
from gnuradio import gr
import radioastronomy
#import statistics

class ra_ascii_sink(gr.sync_block):
    """
    Write Ascii File.  The input
    1) Spectrum 
    Parameters are
    1) Vector length in Channels
    2) Frequency (Hz)
    3) Bandwidth (Hz)
    4) Telescope Azimuth (d)
    5) Telescope Elevation (d)
    6) Record Flag 
    7) Observation Type
    8) Count of spectra averaged
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, noteName, observers, vlen, frequency, bandwidth, azimuth, elevation, record, obstype, 
                 nmedian, nave, site, device, gain1, gain2, gain3):
        gr.sync_block.__init__(self,
            name="ascii_sink",
                     # spectrum
            in_sig=[(np.float32, int(vlen))],
            out_sig=None)
        vlen = int(vlen)
        self.vlen = vlen
        self.nave = nave
        self.avecount = 0
        self.record = radioastronomy.INTWAIT
        self.sum = np.zeros(vlen)
        self.noteName = str(noteName)
        self.obs = radioastronomy.Spectrum()
        self.obs.read_spec_ast(self.noteName)    # read the parameters 
        self.obs.observer = observers
        self.obs.nChan = vlen
        self.obs.nSpec = 1
        self.obs.ydataA = np.zeros(vlen)
        self.obs.ydataB = np.zeros(vlen)
        self.obs.xdata = np.zeros(vlen)
        now = datetime.datetime.utcnow()
        self.startutc = now
        self.stoputc = now
        self.obs.utc = now
        self.setupdir = ""#"./"
        self.notesName = noteName
        self.obstype = int( obstype)
        print 'Setup File       : ',self.noteName
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print 'DataDir          : ',self.obs.datadir
        print 'Observer Names   : ',self.obs.observer
        # skip writing notes until the end of init
        dosave = False
        self.set_frequency( frequency, dosave)
        self.set_bandwidth( bandwidth, dosave)
        self.set_azimuth( azimuth, dosave)
        self.set_elevation( elevation, dosave)
        self.set_nave( nave, dosave)
        self.set_nmedian( nmedian, dosave)
        self.set_gain1( gain1, dosave)
        self.set_gain2( gain2, dosave)
        self.set_gain3( gain3, dosave)
        self.set_record( record)
        self.save_setup()

    def forecast( self, noutput_items, ninput_items): #forcast is a no
        return ninput_items

    def set_frequency( self, frequency, dosave = True):
        self.obs.centerFreqHz = np.float( frequency)
        deltaNu = self.obs.bandwidthHz/np.float( self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print "Setting Frequency: %10.0f Hz" % (self.obs.centerFreqHz)
        for iii in range( self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu
        if dosave:
            self.save_setup()

    def set_bandwidth( self, bandwidth, dosave = True):
        self.obs.bandwidthHz = np.float( bandwidth)
        deltaNu = self.obs.bandwidthHz/np.float( self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print "Setting Bandwidth: %10.0f Hz" % (self.obs.bandwidthHz)
        for iii in range( self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu
        if dosave:
            self.save_setup()

    def set_azimuth( self, azimuth, dosave = True):
        self.obs.telaz = np.float( azimuth)
        print "Setting Azimuth  : %6.1f d" % self.obs.telaz
        if dosave:
            self.save_setup()
                              
    def set_elevation( self, elevation, dosave = True):
        self.obs.telel = np.float( elevation)
        print "Setting Elevation: %6.1f d" % self.obs.telel
        if dosave:
            self.save_setup()

    def set_nmedian( self, nmedian, dosave = True):
        self.obs.nmedian = int( nmedian)
        self.obs.count = int( nmedian )
        print 'Median N Spectra : %d' % (self.obs.nmedian)
        t = self.obs.nmedian * self.nave * self.vlen / self.obs.bandwidthHz
#        print 'Average time     : %8.3f s' % (t)
        if dosave:
            self.save_setup()

    def set_gain1( self, gain1, dosave = True):
        self.obs.gain1 = float(gain1)
        print 'Gain 1           : %7.2f' % (self.obs.gain1)
        if dosave:
            self.save_setup()

    def set_gain2( self, gain2, dosave = True):
        self.obs.gain2 = float(gain2)
        print 'Gain 2           : %7.2f' % (self.obs.gain2)
        if dosave:
            self.save_setup()

    def set_gain3( self, gain3, dosave = True):
        self.obs.gain3 = float(gain3)
        print 'Gain 3           : %7.2f' % (self.obs.gain3)
        if dosave:
            self.save_setup()

    def set_nave( self, nave, dosave = True):
        self.nave = int( nave)
        self.obs.nave = self.nave
        print 'Average N Spectra: %d' % (self.nave)
        t = self.obs.nmedian * self.nave * self.vlen / self.obs.bandwidthHz
        print 'Average time     : %8.3f s' % (t)
        if dosave:
            self.save_setup()

    def get_setup( self):
        return self.noteName

    def set_setup( self, noteName):
        self.noteName = str( noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters 
    
    def save_setup( self):
        self.obs.write_ascii_file( self.setupdir, self.noteName)
        
    def set_obstype( self, obstype):
        self.obstype = int( obstype)
        print "Observation Type : ", radioastronomy.obslabels[self.obstype]

    def set_observers( self, observers, dosave = True):
        self.obs.observer = str( observers)
        print "Observers : ", self.obs.observer
        if dosave:
            self.save_setup()

    def set_site( self, site, dosave = True):
        self.obs.site = str( site)
        print "Telescope : ", self.obs.site
        if dosave:
            self.save_setup()

    def set_device( self, device, dosave = True):
        self.obs.device = str( device)
        print "Device    : ", self.obs.device
        if dosave:
            self.save_setup()

    def set_record( self, record):
        # restart the average loop
        self.avenmedian = 0
        self.obs.writenmedian = 0
        now = datetime.datetime.utcnow()
        self.startutc = now
        # report when the state changed
        strnow = now.isoformat()
        parts = strnow.split('.')
        strnow = parts[0]
        if record == radioastronomy.INTWAIT: 
            print "Stop  Recording  : ", strnow
        # if changing state from recording to not recording
        elif self.record == radioastronomy.INTWAIT and record != radioastronomy.INTWAIT:
            print "Start Recording  : ", strnow
            # reset the inner averaging loop to restart
            self.avecount = 0
        self.record = int( record)

    def get_record( self):
        return self.record

    def get_obstype( self):
        return self.obstype

    def work(self, input_items, output_items):
        """
        Work averages all input vectors and outputs one vector for each N inputs
        """
        inn = input_items[0]
        
        # get the number of input vectors
        n = len( input_items)  # number of input PORTS (only 1)
        nv = len(inn)          # number of vectors in this port
        spec = inn[0]          # first input vector
        li = len(spec)          # length of first input vector
        ncp = min( li, self.vlen)  # don't copy more required (not used)

        if (li != self.vlen):
            print 'spectrum length changed! %d => %d' % ( self.vlen, li)
            self.vlen = li
            self.xdata = np.zeros(li)
            self.ydataA = np.zeros(li)
            self.ydataB = np.zeros(li)
            self.set_frequency( self.obs.centerfrequencyHz)
            self.set_bandwidth( self.obs.bandwidthHz)
            return 1

        noutports = len( output_items)
        if noutports != 0:
            print '!!!!!!! Unexpected number of output ports: ', noutports

        iout = 0 # nmedian the number of output vectors
        for i in range(nv):
            # get the length of one input
            spec = inn[i]
            endvalue = np.median( spec[(ncp-7):(ncp-1)])
            # remove dc bias, measured at end of spectrum
            spec = spec - np.full( self.vlen, endvalue)
            # if just starting a sum
            if self.avecount == 0:
                self.sum = spec
            else:
                # else add to sum
                self.sum = self.sum + spec
            self.avecount = self.avecount + 1
            # if still averaging, continue
            if self.avecount < self.nave:
                continue
            # else average is complete
            now = datetime.datetime.utcnow()
            self.stoputc = now
            middle, duration = radioastronomy.aveutcs( self.startutc, self.stoputc)
            self.obs.utc = middle
            self.obs.durationSec = duration
            tsamples = self.obs.count * self.nave * float(self.obs.nChan) / self.obs.bandwidthHz
            # this removes component due non-gain part of spectrum
            self.obs.ydataA[0:ncp] = self.sum[0:ncp]
            self.obs.azel2radec()
            strnow = middle.isoformat()
            datestr = strnow.split('.')
            daypart = datestr[0]
            yymmdd = daypart[2:19]
            if self.record != radioastronomy.INTWAIT: 
                print 'Record Duration  : %7.2fs (Expected %7.2fs)' % (duration, tsamples)
                if duration < .8 * tsamples:
                    print 'Duration too short, not saving'
                    self.startutc = now
                    self.avecount = 0
                    continue
                # distinguish hot load and regular observations
                if self.obstype == radioastronomy.OBSREF:
                    outname = yymmdd + '.ref'
                else:
                    if self.obs.telel > 0:
                        outname = yymmdd + '.ast'
                    else:
                        outname = yymmdd + '.hot'
                #remove : from time
                outname = outname.replace(":", "")
                
                self.obs.writecount = self.obs.writecount + 1
                # need to keep track of total number of spectra averaged
                tempcount = self.obs.count
                self.obs.count = self.obs.count * self.nave
                self.obs.write_ascii_file( self.obs.datadir, outname)
                # must restore the count for possible changes in nave
                self.obs.count = tempcount
            else:
                # else not recording, plenty of time to compute data statistics
                n6 = int(ncp/6)
                n56 = 5*n6
                vmin = min ( spec[n6:n56])
                vmax = max ( spec[n6:n56])
                vmed = np.median( spec[n6:n56])
                print "%s:  Max %9.3f Min: %9.3f Median: %9.3f " % (yymmdd, vmax, vmin, vmed)
                self.obs.writecount = 0 
            # if here data written, restart sum
            self.avecount = 0
            self.startutc = now
              
        # end for all input vectors
        return 1
    # end ascii_sink()


