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
# 20Feb16 GIL remove normalization.  Do that in post processing
# 20Feb15 GIL fix normalization for different averaging times
# 19OCT14 GIL track down time estimate issues
# 19SEP14 GIL fix gain and telescope location
# 18AUG18 GIL return time until average is complete
# 18AUG17 GIL allow note file to have any extension on input
# 18MAY20 GIL code cleanup
# 18APR29 GIL fix change in nmedian and expected duration
# 18APR20 GIL add gain1, gain2 and gain3
# 18APR19 GIL fix minor typos
# 18APR18 GIL update arguments
# 18APR13 GIL first functioning version

import os
import sys
import datetime
import numpy as np
from gnuradio import gr
from . import radioastronomy

class ra_ascii_sink(gr.sync_block):
    """
    Write Ascii File.  The input
    1) Spectrum
    Parameters are
    1) Vector length in Channels
    2) Frequency (Hz)
    3) Bandwidth (Hz)
    4) Telescop Azimuth (d)
    5) Telescop Elevation (d)
    6) Record Flag
    7) Observation Type
    8) Count of spectra averaged
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, noteName, observers, vlen, frequency, bandwidth,
                 azimuth, elevation, record, obstype, 
                 nmedian, nave, site, device, gain1, gain2, gain3):
        gr.sync_block.__init__(self,
                               name="ra_ascii_sink",              
                               in_sig=[(np.float32, int(vlen))], # input is 1 spectrum
                               out_sig=[np.float32],             # output is time remaining
        )
        vlen = int(vlen)
        self.vlen = vlen
        self.nave = nave
        self.avecount = 0
        self.record = radioastronomy.INTWAIT
        self.sum = np.zeros(vlen)
        self.noteName = str(noteName)
        # split out extension name
        noteParts = self.noteName.split('.')
        #always use .not extension for notes files
        self.noteName = noteParts[0]+'.not'
        if len(noteParts) > 2:
            print('!!! Warning, unexpected Notes File name! ')
            print('!!! Using file: ',self.noteName)
        self.obs = radioastronomy.Spectrum()
        self.obs.read_spec_ast(self.noteName)    # read the parameters 
        self.obs.observer = observers
        self.obs.nChan = vlen
        self.obs.refChan = self.obs.nChan/2.
        self.obs.nSpec = 1
        self.obs.ydataA = np.zeros(vlen)
        self.obs.ydataB = np.zeros(vlen)
        self.obs.xdata = np.zeros(vlen)
        now = datetime.datetime.utcnow()
        self.startutc = now
        self.stoputc = now
        self.obs.utc = now
        self.average_done = 0.0  # no data averaged yet
        self.setupdir = "./"
        self.noteName = noteName
        # split out extension name
        noteParts = self.noteName.split('.')
        #always use .not extension for notes files
        self.noteName = noteParts[0]+'.not'
        if len(noteParts) > 2:
            print('!!! Warning, unexpected Notes File name! ')
            print('!!! Using file: ', self.noteName)
        else:
            if os.path.isfile( self.noteName):
                print('Setup File       : ', self.noteName)
            else:
                if os.path.isfile( "Watch.not"):
                    try:
                        import shutil
                        shutil.copyfile( "Watch.not", self.noteName)
                        print("Created %s from file: Watch.not" % (self.noteName))
                    except:
                        print("! Create the Note file %s, and try again !" % (self.noteName))
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print('DataDir          : ', self.obs.datadir)
        print('Observer Names   : ', self.obs.observer)
        # skip writing notes until the end of init
        dosave = False
        self.set_obstype(obstype)
        self.set_frequency(frequency, dosave)
        self.set_bandwidth(bandwidth, dosave)
        self.set_azimuth(azimuth, dosave)
        self.set_elevation(elevation, dosave)
        self.set_nmedian(nmedian, dosave)
        self.set_nave(nave, dosave)
        self.set_gain1(gain1, dosave)
        self.set_gain2(gain2, dosave)
        self.set_gain3(gain3, dosave)
        self.set_site(site, dosave)
        self.set_device(device, dosave)
        self.set_record(record)
        self.save_setup()

    def forecast(self, noutput_items, ninput_items): #forcast is a no op
        """
        The work block always processes all inputs
        """
        return ninput_items

    def set_frequency(self, frequency, dosave=True):
        self.obs.centerFreqHz = np.float(frequency)
        deltaNu = self.obs.bandwidthHz/np.float(self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print("Setting Frequency: %10.0f Hz" % (self.obs.centerFreqHz))
        for iii in range(self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu
        if dosave:
            self.save_setup()

    def set_bandwidth(self, bandwidth, dosave=True):
        self.obs.bandwidthHz = np.float(bandwidth)
        deltaNu = self.obs.bandwidthHz/np.float(self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print("Setting Bandwidth: %10.0f Hz" % (self.obs.bandwidthHz))
        self.dt = self.obs.nmedian * self.obs.nChan / self.obs.bandwidthHz
        self.average_sec = self.dt * self.nave
        for iii in range(self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu
        self.average_sec = self.dt * self.nave
        print("Integration Time: %8.2f" % (self.average_sec))
        print("N media, N ave: %d, %d" % (self.obs.nmedian, self.nave))
        print("N chan,       : %d" % (self.obs.nChan))
        if dosave:
            self.save_setup()

    def set_azimuth(self, azimuth, dosave=True):
        """
        Record telescope azimuth for astronomical calculations
        """
        self.obs.telaz = np.float(azimuth)
        print("Setting Azimuth  : %6.1f d" % self.obs.telaz)
        if dosave:
            self.save_setup()
                              
    def set_elevation(self, elevation, dosave=True):
        """
        Record telescope elevation for astronmical calculations
        """
        self.obs.telel = np.float(elevation)
        print("Setting Elevation: %6.1f d" % self.obs.telel)
        if dosave:
            self.save_setup()

    def set_nmedian(self, nmedian, dosave=True):
        """
        Set the number of spectra averaged before input to work block
        """
        self.obs.nmedian = int(nmedian)
        self.dt = self.obs.nmedian * self.vlen / self.obs.bandwidthHz
        self.average_sec = self.dt * self.nave
        print('Median N Spectra : %d  (Integration time: %8.3f)' % (self.obs.nmedian, self.average_sec))
        if dosave:
            self.save_setup()

    def set_gain1(self, gain1, dosave=True):
        """
        Record the SDR gain settings 
        """
        self.obs.gains[0] = float(gain1)
        print('Gain 1           : %7.2f' % (self.obs.gains[0]))
        if dosave:
            self.save_setup()

    def set_gain2(self, gain2, dosave=True):
        """
        Record the SDR gain settings 
        """
        self.obs.gains[1] = float(gain2)
        print('Gain 2           : %7.2f' % (self.obs.gains[1]))
        if dosave:
            self.save_setup()

    def set_gain3(self, gain3, dosave=True):
        """
        Record the SDR gain settings 
        """
        self.obs.gains[2] = float(gain3)
        print('Gain 3           : %7.2f' % (self.obs.gains[2]))
        if dosave:
            self.save_setup()

    def set_nave(self, nave, dosave=True):
        self.nave = int(nave)
        self.obs.nave = self.nave
        print('Average N Spectra: %d' % (self.nave))
        self.dt = self.obs.nmedian * self.vlen / self.obs.bandwidthHz
        self.average_sec = self.dt * self.nave
        print('Average time     : %8.3f s' % (self.average_sec))
        if dosave:
            self.save_setup()

    def get_setup(self):
        """
        return the name of the files used for setup
        """
        return self.noteName

    def set_setup(self, noteName):
        """
        Read the setup files and initialize all values
        """
        self.noteName = str(noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters 
    
    def save_setup(self):
        """
        The setup files is a full spectrum
        """
        self.obs.write_ascii_file(self.setupdir, self.noteName)
        print('Updated: %s' % (self.noteName))
        
    def update_len(self, spectrum):
        """
        Update the length of the output vectors
        """
        self.obs.ydataA = np.zeros(self.vlen)
        self.obs.ydataB = np.zeros(self.vlen)
        self.obs.xdata = np.zeros(self.vlen)
        self.obs.nchan = self.vlen
        self.obs.refchan = self.vlen/2.

    def set_obstype(self, obstype):
        """
        The observing type is an integer with enumerated values
        """
        self.obstype = int(obstype)
        if obstype == radioastronomy.OBSHOT or obstype == radioastronomy.OBSCOLD:
            if self.obs.telel > 0.:
                self.obstype = radioastronomy.OBSCOLD
            else:
                self.obstype = radioastronomy.OBSHOT
        print("Observation Type : ", radioastronomy.obslabels[self.obstype])

    def set_observers(self, observers, dosave=True):
        """
        Set the observer names to give credit for discoveries
        """
        self.obs.observer = str(observers)
        print("Observers : ", self.obs.observer)
        if dosave:
            self.save_setup()

    def set_site(self, site, dosave=True):
        """
        Set the telescope name for this site
        """
        self.obs.site = str(site)
        self.obs.noteA = str(site)
        print("Telescope : ", self.obs.site)
        if dosave:
            self.save_setup()

    def set_device(self, device, dosave=True):
        """
        The device string sets up the SDR for the observations
        """
        self.obs.device = str(device)
        print("Device    : ", self.obs.device)
        if dosave:
            self.save_setup()

    def set_record(self, record):
        """ 
        When chaning record status, need to update counters
        """
        # restart the average loop
        self.avenmedian = 0
        self.obs.writenmedian = 0
        now = datetime.datetime.utcnow()
        # report when the state changed
        strnow = now.isoformat()
        parts = strnow.split('.')
        strnow = parts[0]
        if record == radioastronomy.INTWAIT: 
            print("Stop  Recording  : ", strnow)
            self.startutc = now
            self.obs.writecount = 0
        # if changing state from recording to not recording
        elif self.record == radioastronomy.INTWAIT and record != radioastronomy.INTWAIT:
            print("Start Recording  : ", strnow)
            self.startutc = now
            # reset the inner averaging loop to restart
            self.avecount = 0
        self.record = int(record)

    def get_record(self):
        """
        return the recording state (WAIT, RECORD, SAVE)
        """
        return self.record

    def get_obstype(self):
        """
        return the observing type (Survey, hot, cold, ref)
        """
        return self.obstype

    def get_average_sec(self):
        """
        return the total predicted averaging time (seconds)
        """
        return self.average_sec

    def get_average_left(self):
        """
        return the total time remaining is expected minus total (seconds)
        """
        return (self.average_sec - self.average_done)

    def work(self, input_items, output_items):
        """
        Work averages all input vectors and outputs one vector for each N inputs
        """
        inn = input_items[0]
        
        # get the number of input vectors
        nv = len(inn)          # number of vectors in this port
        spec = inn[0]          # first input vector
        li = len(spec)          # length of first input vector
        ncp = min(li, self.vlen)  # don't copy more required (not used)
        t = 0

        if li != self.vlen:
            print('spectrum length changed! %d => %d' % (self.vlen, li))
            self.vlen = li
            self.obs.xdata = np.zeros(li)
            self.obs.ydataA = np.zeros(li)
            self.obs.ydataB = np.zeros(li)
            self.set_frequency(self.obs.centerfrequencyHz)
            self.set_bandwidth(self.obs.bandwidthHz)
            return 1

        noutports = len(output_items)
        if noutports != 1:
            print('!!!!!!! Unexpected number of output ports: ', noutports)
        out = output_items[0]  # all vectors in PORT 0

        iout = 0 # count the number of output vectors
        for i in range(nv):
            # get the length of one input
            spec = inn[i]
            # if just starting a sum
            if self.avecount == 0:
                self.sum = spec
                self.average_done = self.dt
            else:
                # else add to sum
                self.average_done = self.average_done + self.dt
                self.sum = self.sum + spec
#            print 'Done: ', self.average_done
            self.avecount = self.avecount + 1
            # if still averaging, continue
            if self.avecount < self.nave:
                continue
            # else average is complete
            now = datetime.datetime.utcnow()
            self.stoputc = now
            middle, duration = radioastronomy.aveutcs(self.startutc, self.stoputc)
            self.obs.utc = middle
            self.obs.durationSec = duration
            # this removes component due non-gain part of spectrum
            # avecount normaizes the counts of observations
#            self.obs.ydataA[0:ncp] = self.sum[0:ncp]/float(self.avecount)
            self.obs.ydataA[0:ncp] = self.sum[0:ncp]
            self.obs.azel2radec()
            strnow = middle.isoformat()
            datestr = strnow.split('.')
            daypart = datestr[0]
            yymmdd = daypart[2:19]
            if self.record != radioastronomy.INTWAIT: 
                print('Record Duration  : %7.2fs (Expected %7.2fs)' % (duration, self.average_sec))
                if duration < .8 * self.average_sec:
                    print('Duration too short, not saving')
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
                self.obs.count = self.avecount * self.nave
                self.obs.write_ascii_file( self.obs.datadir, outname)
                print('\a')  # ring the terminal bell
                # must restore the count for possible changes in nave
                self.obs.count = tempcount
            else:
                # else not recording, plenty of time to compute data statistics
                n6 = int(ncp/6)
                n56 = 5*n6
                vmin = min ( spec[n6:n56])
                vmax = max ( spec[n6:n56])
                vmed = np.median( spec[n6:n56])
                print("%s:  Max %9.3f Min: %9.3f Median: %9.3f      " % (yymmdd, vmax, vmin, vmed))
                # move backwards to replace previous message
                sys.stdout.write("\033[F")
                self.obs.writecount = 0 
            # if here data written, restart sum
            self.avecount = 0
            self.startutc = now

        out[:] = self.average_sec - self.average_done
        iout = iout+1
        
        # end for all input vectors
        if (nv != iout):
            print('Accumulation error:  ', nv, iout)
        return iout
    # end ascii_sink()


