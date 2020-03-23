#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Glen Langston, Quiet Skies
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
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
# HISTORY
# 19SEP14 GIL hanning smooth reference in case of subtracting fit
# 19JUN21 GIL more code cleanup
# 19JUN20 GIL subtract baseline from ref.   Integrate ref for 5 seconds
# 19JUN19 GIL subtract baseline from ref.   Integrate ref for 30 seconds
# 19APR29 GIL allow baseline subtracted Tsys
# 19APR08 GIL enforce writing spectra
# 18AUG17 GIL allow note file to have any extension on input
# 18JUN13 GIL remove subtraction of signals
# 18MAY20 GIL code cleanup
# 18APR20 GIL first functioning version
# 18APR11 GIL first functioning version
# 18APR01 GIL initial version

import os
import sys
import datetime
import numpy as np
from gnuradio import gr
import copy
from . import radioastronomy

# this block has 5 output spectra:
# 1st is just the input spectrum
# 2nd is average of the input spectra
# 3rd is hot average spectrum
# 4th is cold average spectrum
# 5th is average reference spectrum
NSPEC = 5
AVEFILE = "Ave.ast"
HOTFILE = "Hot.hot"
COLDFILE = "Cold.ast"
REFFILE = "Ref.ast"
# create a small value to prevent NaNs in log10
EPSILON = 0.00001

class ra_integrate(gr.sync_block):
    """
    Radio Astronomy Integrate.  A single vector stream comes into the block.
        In:  Data stream of spectra
    Several vectors are output:
        Out: Latest Spectrum
             Integrated (average) spectrum
             Integrated Hot load
             Integrated Cold load
             Integrated Reference
        The output streams have different possible calibration unitss.
            Counts (linear)
            Counts (db)
            Kelvins
    Parameters are
    1) Vector length in Channels
    2) Frequency (Hz)
    3) Bandwidth (Hz)
    4) Telescop Azimuth (d)
    5) Telescop Elevation (d)
    6) Integration Type  Integrate or Replace
    7) Observation Type
    8) Count of spectra medianed before input to integrate
    9) Brightness units; one of [Counts (linear), Counts(dB), Kelvins]
    10) Hot load temperature
    11) Cold load temperature
    This block is intended to reduce the downstream CPU load.
    """
    def __init__(self, noteName, observers, vlen, frequency, bandwidth, azimuth,
                 elevation, inttype, obstype, nmedian, units, thot, tcold):
        gr.sync_block.__init__(self,
                               name="integrate",
                               in_sig=[(np.float32, int(vlen))],  # 1 input spectrum
                               out_sig=[(np.float32, int(vlen)), (np.float32, int(vlen)),
                                        (np.float32, int(vlen)),  # 5 output spectra
                                        (np.float32, int(vlen)), (np.float32, int(vlen))])
        vlen = int(vlen)
        self.vlen = vlen
        self.nintegrate = 1
        self.noteName = str(noteName)
        noteParts = self.noteName.split('.')
        #always use .not extension for notes files
        self.noteName = noteParts[0]+'.not'
        if len(noteParts) > 2:
            print('!!! Warning, unexpected Notes File name! ')
            print('!!! Using file: ',self.noteName)
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
        self.obstype = obstype
        self.inttype = inttype
        self.obs = radioastronomy.Spectrum()
        self.obs.read_spec_ast(self.noteName)    # read the parameters
        self.obs.nspec = 1                       # make sure we're working with spectra
        self.obs.ntime = 0                       # not events
        self.obs.xdata = np.zeros(self.vlen)
        self.obs.ydataA = np.zeros(self.vlen)
        self.obs.ydataB = np.zeros(self.vlen)
        self.shortave = np.zeros(self.vlen)
        self.shortlast = np.zeros(self.vlen)
        self.nshort=0
        self.maxshort=20                         # count before restart sum
        self.oneovermax = float(1./self.maxshort)# normalization factor
        self.obs.nchan = self.vlen
        self.obs.refchan = self.vlen/2.
        self.obs.observer = observers
        self.ave = radioastronomy.Spectrum()
        self.ave.read_spec_ast(self.noteName)    # read the parameters
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.record = radioastronomy.INTWAIT
        self.hot = radioastronomy.Spectrum()
        self.cold = radioastronomy.Spectrum()
        self.ref = radioastronomy.Spectrum()
        if os.path.isfile(HOTFILE):
            self.hot.read_spec_ast(HOTFILE)
        else:
            self.hot.read_spec_ast(self.noteName)    # read the parameters
        if os.path.isfile(COLDFILE):
            self.cold.read_spec_ast(COLDFILE)
        else:
            self.cold.read_spec_ast(self.noteName)    # read the parameters
        if os.path.isfile(REFFILE):
            self.ref.read_spec_ast(REFFILE)
        else:
            self.ref.read_spec_ast(self.noteName)    # read the parameters
        if self.obs.nChan != vlen:
            self.update_len(self.obs)
        if self.ave.nChan != vlen:
            self.update_len(self.ave)
        if self.hot.nChan != vlen:
            self.update_len(self.hot)
        if self.cold.nChan != vlen:
            self.update_len(self.cold)
        if self.ref.nChan != vlen:
            self.update_len(self.ref)
        now = datetime.datetime.utcnow()
        self.startutc = now
        self.stoputc = now
        self.obs.utc = now
        self.printutc = now
        self.printinterval = 5.  # print averages every few seconds
        n32 = int(self.vlen/32)  # make an array of indices for baseline fitting
        xa = np.arange(n32)+(3*n32)
        xb = np.arange(n32)+(n32*28)        
        self.xfit = np.concatenate((xa,xb))      # indicies for fit 
        self.xindex = np.arange(self.vlen)       # array of integers
        self.yfit = self.obs.ydataA[self.xfit]   # sub-array of fittable data
        self.allchan  = np.array(list(range(self.vlen)))
        print('Setup File       : ', self.noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters
        self.obs.observer = observers
        self.ave.read_spec_ast(self.noteName)    # read the parameters
        # prepare to start writing observations
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print('DataDir          : ', self.obs.datadir)
        print('Observer Names   : ', self.obs.observer)
        self.obstypes = list(range(radioastronomy.NOBSTYPES))
        self.intstatus = list(range(radioastronomy.NINTTYPES))
        self.set_frequency(frequency)
        self.set_bandwidth(bandwidth)
        self.set_azimuth(azimuth)
        self.set_elevation(elevation)
        self.set_inttype(inttype)
        self.set_obstype(obstype)
        self.set_units(units)
        self.set_nmedian(nmedian)
        self.set_thot(thot)
        self.set_tcold(tcold)
        self.epsilons = np.full(self.vlen, EPSILON)

    def update_len(self, spectrum):
        """
        Update the length of the output vectors
        """
        spectrum.ydataA = np.zeros(self.vlen)
        spectrum.ydataB = np.zeros(self.vlen)
        spectrum.xdata = np.zeros(self.vlen)
        spectrum.nChan = self.vlen
        n32 = int(self.vlen/32)  # make an array of indices for baseline fitting
        xa = np.arange(n32)+(3*n32)
        xb = np.arange(n32)+(n32*28)        
        self.xfit = np.concatenate((xa,xb))      # indicies for fit 
        self.xindex = np.arange(self.vlen)       # array of integers
        self.yfit = self.obs.ydataA[self.xfit]   # sub-array of fittable data
        self.allchan  = np.array(list(range(self.vlen)))
        self.shortave = np.zeros(self.vlen)
        self.shortlast = np.zeros(self.vlen)
        self.nshort=0
        self.obs.nchan = self.vlen
        self.obs.refchan = self.vlen/2.

    def forecast(self, noutput_items, ninput_items): #forcast is a no-op
        """
        Predict how many vectors will be output for each input == same number
        """
        ninput_items = noutput_items
        return ninput_items

    def set_frequency(self, frequency):
        """
        Update the observing center frequency
        """
        self.obs.centerFreqHz = np.float(frequency)
        self.ref.centerFreqHz = np.float(frequency)
        self.ave.centerFreqHz = np.float(frequency)
        self.hot.centerFreqHz = np.float(frequency)
        self.cold.centerFreqHz = np.float(frequency)
        deltaNu = self.obs.bandwidthHz/np.float(self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print("Setting Frequency: %10.0f Hz" % (self.obs.centerFreqHz))
        nx = len( self.obs.xdata)
        if nx != self.vlen:
            self.update_len(self.obs)
        for iii in range(self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu

    def set_bandwidth(self, bandwidth):
        """
        Set the observing bandwidth
        """
        self.obs.bandwidthHz = np.float(bandwidth)
        self.ave.bandwidthHz = np.float(bandwidth)
        self.hot.bandwidthHz = np.float(bandwidth)
        self.cold.bandwidthHz = np.float(bandwidth)
        self.ref.bandwidthHz = np.float(bandwidth)
        deltaNu = self.obs.bandwidthHz/np.float(self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        if len(self.ave.xdata) != self.vlen:
            self.update_len(self.ave)
        if len(self.hot.xdata) != self.vlen:
            self.update_len(self.hot)
        if len(self.cold.xdata) != self.vlen:
            self.update_len(self.cold)
        if len(self.ref.xdata) != self.vlen:
            self.update_len(self.ref)
        print("Setting Bandwidth: %10.0f Hz" % (self.obs.bandwidthHz))
        for iii in range(self.vlen):
            self.obs.xdata[iii] = nu
            self.ave.xdata[iii] = nu
            self.hot.xdata[iii] = nu
            self.cold.xdata[iii] = nu
            self.ref.xdata[iii] = nu
            nu = nu + deltaNu

    def set_azimuth(self, azimuth):
        """
        Record the Telescope Azimuth for coordinate calculations
        """
        self.obs.telaz = np.float(azimuth)
        self.ave.telaz = self.obs.telaz
        self.hot.telaz = self.obs.telaz
        self.cold.telaz = self.obs.telaz
        self.ref.telaz = self.obs.telaz
        print("Setting Azimuth  : %6.1f d" % self.obs.telaz)

    def set_elevation(self, elevation):
        """
        Record the Telescope Elevation for coordinate calculations
        """
        self.obs.telel = np.float(elevation)
        self.ave.telaz = self.obs.telel
        self.hot.telaz = self.obs.telel
        self.cold.telaz = self.obs.telel
        self.ref.telaz = self.obs.telel
        print("Setting Elevation: %6.1f d" % self.obs.telel)

    def set_nmedian(self, nmedian):
        """
        save the number of spectra averaged before input
        Used to estimate the total observing time
        """
        nmedian = int(nmedian)
        self.obs.nmedian = nmedian
        self.ave.nmedian = nmedian
        self.hot.nmedian = nmedian
        self.cold.nmedian = nmedian
        self.ref.nmedian = nmedian
        print('Median Count     : %d' % (self.obs.nmedian))
        t = self.obs.nmedian * self.vlen / self.obs.bandwidthHz
        print('Average time     : %8.3f s' % (t))

    def get_setup(self):
        """
        Return the name of the file used to setup the observations
        """
        return self.noteName

    def set_setup(self, noteName):
        """
        Record the name of the spectrum file used for setup, then read values
        """
        self.noteName = str(noteName)
        self.obs.read_spec_ast(self.noteName)    # read the parameters

    def set_obstype(self, obstype):
        """
        Update the observing type, one of Survey, Wait, Cold, Hot or Ref
        """
        self.obstype = int(obstype)
        if obstype == radioastronomy.OBSHOT or obstype == radioastronomy.OBSCOLD:
            if self.obs.telel > 0.:
                self.obstype = radioastronomy.OBSCOLD
            else:
                self.obstype = radioastronomy.OBSHOT
        print("Observation Type : ", radioastronomy.obslabels[self.obstype])

    def set_inttype(self, inttype):
        """
        Update the recording integration type, one of WAIT, RECORD or Save
        """
        self.inttype = int(inttype)
        print("Integration Type : ", radioastronomy.intlabels[self.inttype])
        
    def set_observers(self, observers):
        """
        Save the name of the observers to give credit
        """
        observers = str(observers)
        self.obs.observer = observers
        self.ave.observers = observers
        self.ref.observer = observers
        self.cold.observers = observers
        self.hot.observers = observers
        print("Observers : ", self.obs.observer)

    def set_units(self, units):
        """
        Set the type of calibration desired for plotting
        """
        if type(units) is int:
            self.units = int(units)
        else:
            self.units = 0
        print("Units     : ", radioastronomy.unitlabels[self.units])

    def set_tcold(self, tcold):
        """
        Set the estimated cold load temperature in Kelvins
        """
        tcold = float(tcold)
        if tcold < 3.:
            tcold = 3.
        self.tcold = tcold
        print("T_cold    : ", self.tcold)

    def set_thot(self, thot):
        """
        Set the estimated hot load temperature in Kelvins (usually 295 K)
        """
        thot = float(thot)
        if thot < 50.:
            thot = 295.
        self.thot = thot
        print("T_hot     : ", self.thot)

    def set_record(self, record):
        """
        Set the recording state; update counters
        """
        record = int(record)
        now = datetime.datetime.utcnow()
        self.obs.writecount = 0
        strnow = now.isoformat()
        parts = strnow.split('.')
        strnow = parts[0]
        if record == radioastronomy.INTWAIT:
            print("Stop  Averaging  : ", strnow)
            self.stoputc = now
        # only restart averaging if not in averaging state
        elif self.record == radioastronomy.INTWAIT:
            print("Start Averaging  : ", strnow)
            self.startutc = now
        self.record = int(record)

    def get_record(self):
        """
        Return the record status
        """
        return self.record

    def get_obstype(self):
        """
        Return the observation type
        """
        return self.obstype

    def write_spec(self):
        """
        If writing a spectrum to a save file
        """
        strnow = self.obs.utc.isoformat()
        datestr = strnow.split('.')
        daypart = datestr[0]
        yymmdd = daypart[2:19]
        
        # distinguish hot load and regular observations
        if self.obstype == radioastronomy.OBSREF:
            outname = yymmdd + '.tst'
        else:
            if self.obs.telel > 0:
                outname = yymmdd + '.ast'
            else:
                outname = yymmdd + '.hot'
            #remove : from time
        outname = outname.replace(":", "")
                
        self.obs.writecount = self.obs.writecount + 1
        self.obs.write_ascii_file(self.obs.datadir, outname)

    def compute_thotcold(self, yv, hv, cv, thot, tcold):
        """ 
        compute_tsky() compute an array of calibrated spectra assuming hot, cold obs.
        The inputs are:
        yv      spectrum to calibrate (raw counts).  This is also the cold lod spectrum
        hv      spectrum of hot load (raw counts).
        cv      cold sky spectrum (raw counts).
        thot    Hot load temperature in Kelvins (usually between 275. an 300 K
        tcold   Cold load temperature in Kelvins (usually between 10 and 100 K
        """
        nData = self.vlen

        tsys = np.zeros(nData)      # initialize arrays with zeros
        Y = np.zeros(nData)        
        # For full Temp calibration, a spectrum taken at high elevation away from 
        # The galactic plan is used.   For this program the cold spectrum must be
        # the spectrum being calibrated.   See the M command for comparision
        # comput the cold/hot ratio
        Y = hv/cv                       # Y is ratio of hot data to cold data
        YM1 = Y - 1.                    # Y minus 1
        YM1 = np.maximum(YM1, self.epsilons)  # avoid divide by zero

        # the cold, receiver, temperature is this function
        tsys = (thot - (Y * tcold))/YM1
    
        n6 = int(nData/6)
        n56 = 5*n6

        tsysmedian = np.median(tsys[n6:n56])

        tsky = np.zeros(nData)    # initialize arrays

        # The system gain Sgain is computed assuming a tsys is the cold load
        Sgain = np.full(nData, (tsysmedian+thot))/hv
        # scale the observed instensity in counts to Kelvins.
        tsky = Sgain * yv

        return tsky, tsysmedian

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
        n6 = int(ncp/6)
        n56 = 5*n6

        if li != self.vlen:
            print('spectrum length changed! %d => %d' % (self.vlen, li))
            self.vlen = li
            self.obs.xdata = np.zeros(li)
            self.obs.ydataA = np.zeros(li)
            self.obs.ydataB = np.zeros(li)
            self.set_frequency(self.obs.centerfrequencyHz)
            self.set_bandwidth(self.obs.bandwidthHz)
            return 1

        # define output vectors
        out = output_items[0]
        ave = output_items[1]
        hot = output_items[2]
        cold = output_items[3]
        ref = output_items[4]

        nout = 0
        for i in range(nv):
            now = datetime.datetime.utcnow()
            # get the length of one input
            spec = inn[i]
            # deal with average state
            if self.inttype == radioastronomy.INTWAIT:
                self.ave.ydataB = spec
                self.nintegrate = 1
                self.ave.ydataA = spec
                self.startutc = now
                self.obs.utc = now
                self.obs.count = self.obs.nmedian
            else: # else averaging and maybe writing
                self.ave.ydataB = self.ave.ydataB + spec
                self.nintegrate = self.nintegrate + 1
                oneovern = 1./np.float(self.nintegrate)
                self.ave.ydataA = oneovern*self.ave.ydataB
                # total number of spectra averaged 
                # is the number medianed times the number averaged
                self.ave.count = self.obs.nmedian*self.nintegrate
                self.ave.utc, duration = radioastronomy.aveutcs(self.startutc, now)
                self.ave.durationsec = duration
                # only record aveaged spectra
                # now, if updating hot, cold or references spectra
                # if saving files, must reload any configuration changes updated by the sinks
                if (self.inttype == radioastronomy.INTSAVE) and (self.nintegrate % 20 == 1):
                    if self.obstype == radioastronomy.OBSHOT:
                        self.hot.read_spec_ast(self.noteName)    # read the parameters 
                    elif self.obstype == radioastronomy.OBSCOLD:
                        self.cold.read_spec_ast(self.noteName)    # read the parameters 
                    elif self.obstype == radioastronomy.OBSREF:
                        self.ref.read_spec_ast(self.noteName)    # read the parameters 
                if self.obstype == radioastronomy.OBSHOT:
                    self.hot.ydataA = np.maximum(self.ave.ydataA[0:self.vlen], self.epsilons[0:self.vlen])
                    self.hot.nave = self.nintegrate
                    self.hot.count = self.ave.count
                    self.hot.utc = self.ave.utc
                    self.hot.durationsec = self.ave.durationsec
                    self.hot.ydataA[0:1] = self.hot.ydataA[2]
                elif self.obstype == radioastronomy.OBSCOLD:
                    self.cold.ydataA = np.maximum(self.ave.ydataA[0:self.vlen], self.epsilons[0:self.vlen])
                    self.cold.nave = self.nintegrate
                    self.cold.count = self.ave.count
                    self.cold.utc = self.ave.utc
                    self.cold.durationsec = self.ave.durationsec
                    self.cold.ydataA[0:1] = self.cold.ydataA[2]
                elif self.obstype == radioastronomy.OBSREF:
                    self.ref.ydataA = np.maximum(self.ave.ydataA[0:self.vlen], self.epsilons[0:self.vlen])
                    self.ref.nave = self.nintegrate
                    self.ref.count = self.ave.count
                    self.ref.utc = self.ave.utc
                    self.ref.durationsec = self.ave.durationsec
                    self.ref.ydataA[0:1] = self.ref.ydataA[2]
                # if writing files, reduce write rate
                if (self.inttype == radioastronomy.INTSAVE) and (self.nintegrate % 20 == 1):
                    if self.obstype == radioastronomy.OBSHOT:
                        self.hot.write_ascii_file("./", HOTFILE)
                    elif self.obstype == radioastronomy.OBSCOLD:
                        self.cold.write_ascii_file("./", COLDFILE)
                    elif self.obstype == radioastronomy.OBSREF:
                        self.ref.write_ascii_file("./", REFFILE)
            # after flip, the first couple channels are anomoulusly large
            spec[0:1] = spec[2]
            self.ave.ydataA[0:1] = self.ave.ydataA[2]
            self.ave.nave = self.nintegrate
            # since the data rate should be low, nout will usually be 0
            # have all spectra, decide plot format
            if self.units == radioastronomy.UNITCOUNTS:
                out[nout] = spec
                ave[nout] = self.ave.ydataA
                hot[nout] = self.hot.ydataA
                cold[nout] = self.cold.ydataA
                ref[nout] = self.ref.ydataA
            elif self.units == radioastronomy.UNITDB:
                spec = np.maximum(spec, self.epsilons)
                self.ave.ydataA = np.maximum(self.ave.ydataA, self.epsilons)
                out[nout] = 10. * np.log10(spec)
                ave[nout] = 10. * np.log10(self.ave.ydataA)
                hot[nout] = 10. * np.log10(self.hot.ydataA)
                cold[nout] = 10. * np.log10(self.cold.ydataA)
                ref[nout] = 10. * np.log10(self.ref.ydataA)
            else:           # else need Kelvins
                hv = self.hot.ydataA[0:self.vlen] 
                hv = np.maximum(hv, self.epsilons[0:self.vlen])
                cv = self.cold.ydataA[0:self.vlen]
                cv = np.maximum(cv, self.epsilons[0:self.vlen])
                yv = self.ave.ydataA[0:self.vlen]
                yv = np.maximum(yv, self.epsilons[0:self.vlen])
                # compute Kelvings per count factor
                tsys, trx = self.compute_thotcold(yv, hv, cv, self.thot, self.tcold)
                TSYS = trx + self.thot
                # now compute center scalar value
                oneoverhot = np.full(self.vlen, 1.)
                oneoverhot = oneoverhot / hv
                # compute short term Tsys value
                outs = TSYS * spec * oneoverhot
                aves = tsys
                hot[nout] = np.full(self.vlen, TSYS+self.thot)
                colds = TSYS * self.cold.ydataA * oneoverhot
                cold[nout] = TSYS * self.cold.ydataA * oneoverhot
                refs = TSYS * self.ref.ydataA * oneoverhot
                if self.units == radioastronomy.UNITBASELINE: # if subtracting a baseline
                    # select the channels at the edges
                    self.yfit = outs[self.xfit]
                    thefit = np.polyfit( self.xfit, self.yfit, 1)
                    outs = outs - ((self.xindex*thefit[0]) + thefit[1])
                    # now subtract fit from average
                    self.yfit = aves[self.xfit]
                    thefit = np.polyfit( self.xfit, self.yfit, 1)
                    aves = aves - ((self.xindex*thefit[0]) + thefit[1])
                    # now subtract fit from cold
                    self.yfit = colds[self.xfit]
                    thefit = np.polyfit( self.xfit, self.yfit, 1)
                    colds = colds - ((self.xindex*thefit[0]) + thefit[1])
                    # if subtracting fit, change reference role to
                    # short duration average; must recalculate
                    if self.nshort <= 0:
                        self.shortave = spec
                        self.nshort = 1
                    else:
                        self.shortave = self.shortave + spec
                        self.nshort = self.nshort + 1
                    if self.nshort >= self.maxshort:
                        self.shortlast = self.oneovermax * self.shortave
                        self.shortlast = TSYS * self.shortlast * oneoverhot
                        self.yfit = self.shortlast[self.xfit]
                        thefit = np.polyfit( self.xfit, self.yfit, 1)
                        temps = self.shortlast - ((self.xindex*thefit[0]) + thefit[1])
                        # hanning smooth
                        refs = 2.*temps
                        refs[1:self.vlen-1] += (temps[0:self.vlen-2] + temps[2:self.vlen])
                        refs = 0.25*refs
                        # will keep showing last short reference until next is ready
                        self.shortlast = refs
                        self.nshort = 0   # restart sum on next cycle
                        print("")
                        print("New Ref")
                        print("")
                    else:
                        refs = self.shortlast
                    # end if subtracting baseline
                out[nout] = outs
                ave[nout] = aves
                ref[nout] = refs
                cold[nout] = colds
            # completed calibration, update count of output vectors
            nout = nout + 1

            self.stoputc = now
            dt = now - self.printutc
            # if time to print
            if dt.total_seconds() > self.printinterval:

                strnow = now.isoformat()
                datestr = strnow.split('.')
                daypart = datestr[0]
                yymmdd = daypart[2:19]
                avespec = ave[0]
                avespec = avespec[n6:n56]
                vmin = min(avespec)
                vmax = max(avespec)
                vmed = np.median(avespec)

                label = radioastronomy.unitlabels[self.units]
                if self.units == 0:
                    print("%s Max %9.3f Min: %9.3f Median: %9.3f %s " % (yymmdd, vmax, vmin, vmed, label))
                elif self.units == 1:
                    print("%s Max %9.3f Min: %9.3f Median: %9.3f %s " % (yymmdd, vmax, vmin, vmed, label))
                else: 
                    print("%s Max %9.1f Min: %9.1f Median: %9.1f %s " % (yymmdd, vmax, vmin, vmed, label))
                sys.stdout.write("\033[F")
                self.printutc = now
        # end for all input vectors
        return nout
    # end ra_integrate()


