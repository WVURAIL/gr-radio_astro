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
# 18APR20 GIL first functioning version
# 18APR11 GIL first functioning version
# 18APR01 GIL initial version

import os
import numpy as np
import datetime
import copy
from gnuradio import gr
import radioastronomy
# try:
# import statistics
# except ImportError:
#     print 'Statistics Python Code needed!'
#     print 'In Linux type:'
#     print '       sudo pip install statistics'
#     print ''
#     exit()

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
    def __init__(self, setupFile, observers, vlen, frequency, bandwidth, azimuth, elevation, inttype, obstype, nmedian, units, thot, tcold):
        gr.sync_block.__init__(self,
            name="integrate",
                     # spectrum
            in_sig=[(np.float32, int(vlen))],
            out_sig=[(np.float32, int(vlen)), (np.float32, int(vlen)),
                     (np.float32, int(vlen)),
                     (np.float32, int(vlen)), (np.float32, int(vlen))])
        self.vlen = int(vlen)
        self.nave = 1L
        self.setupFile = str(setupFile)
        self.obstype = obstype
        self.inttype = inttype
        self.obs = radioastronomy.Spectrum()
        self.ave = radioastronomy.Spectrum()
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.record = radioastronomy.INTWAIT
        self.hot = radioastronomy.Spectrum()
        self.cold = radioastronomy.Spectrum()
        self.ref = radioastronomy.Spectrum()
        self.obs.read_spec_ast(self.setupFile)    # read the parameters 
        self.obs.observer = observers
        self.ave.read_spec_ast(self.setupFile)    # read the parameters 
        if os.path.isfile( HOTFILE):
            self.hot.read_spec_ast( HOTFILE)
        else:
            self.hot.read_spec_ast(self.setupFile)    # read the parameters 
        if os.path.isfile( COLDFILE):
            self.cold.read_spec_ast( COLDFILE)
        else:
            self.cold.read_spec_ast(self.setupFile)    # read the parameters 
        if os.path.isfile( REFFILE):
            self.ref.read_spec_ast( REFFILE)
        else:
            self.ref.read_spec_ast(self.setupFile)    # read the parameters 
        if self.obs.nChan != vlen:
            self.update_len( self.obs)
        if self.ave.nChan != vlen:
            self.update_len( self.ave)
        if self.hot.nChan != vlen:
            self.update_len( self.hot)
        if self.cold.nChan != vlen:
            self.update_len( self.cold)
        if self.ref.nChan != vlen:
            self.update_len( self.ref)
        now = datetime.datetime.utcnow()
        self.startutc = now
        self.stoputc = now
        self.obs.utc = now
        print 'Setup File       : ',self.setupFile
        # prepare to start writing observations
        if not os.path.exists(self.obs.datadir):
            os.makedirs(self.obs.datadir)
        nd = len(self.obs.datadir)
        if self.obs.datadir[nd-1] != '/':
            self.obs.datadir = self.obs.datadir + "/"
            print 'DataDir          : ',self.obs.datadir
        print 'Observer Names   : ',self.obs.observer
        self.obstypes = range(radioastronomy.NOBSTYPES)
        self.intstatus = range(radioastronomy.NINTTYPES)
        self.set_frequency( frequency)
        self.set_bandwidth( bandwidth)
        self.set_azimuth( azimuth)
        self.set_elevation( elevation)
        self.set_inttype( inttype)
        self.set_obstype( obstype)
        self.set_units( units)
        self.set_nmedian( nmedian)
        self.set_thot( thot)
        self.set_tcold( tcold)
        self.epsilons = np.full(self.vlen, EPSILON)

    def update_len( self, spectrum):
        spectrum.ydataA = np.zeros(self.vlen)
        spectrum.ydataB = np.zeros(self.vlen)
        spectrum.xdata = np.zeros(self.vlen)
        spectrum.nChan = self.vlen

    def forecast( self, noutput_items, ninput_items): #forcast is a no
        return ninput_items

    def set_frequency( self, frequency):
        self.obs.centerFreqHz = np.float( frequency)
        self.ref.centerFreqHz = np.float( frequency)
        self.ave.centerFreqHz = np.float( frequency)
        self.hot.centerFreqHz = np.float( frequency)
        self.cold.centerFreqHz = np.float( frequency)
        deltaNu = self.obs.bandwidthHz/np.float( self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print "Setting Frequency: %10.0f Hz" % (self.obs.centerFreqHz)
        for iii in range( self.vlen):
            self.obs.xdata[iii] = nu
            nu = nu + deltaNu

    def set_bandwidth( self, bandwidth):
        self.obs.bandwidthHz = np.float( bandwidth)
        self.ave.bandwidthHz = np.float( bandwidth)
        self.hot.bandwidthHz = np.float( bandwidth)
        self.cold.bandwidthHz = np.float( bandwidth)
        self.ref.bandwidthHz = np.float( bandwidth)
        deltaNu = self.obs.bandwidthHz/np.float( self.vlen)
        n0 = self.obs.centerFreqHz - (self.obs.bandwidthHz/2.)
        nu = n0
        print "Setting Bandwidth: %10.0f Hz" % (self.obs.bandwidthHz)
        for iii in range( self.vlen):
            self.obs.xdata[iii] = nu
            self.ave.xdata[iii] = nu
            self.hot.xdata[iii] = nu
            self.cold.xdata[iii] = nu
            self.ref.xdata[iii] = nu
            nu = nu + deltaNu

    def set_azimuth( self, azimuth):
        self.obs.telaz = np.float( azimuth)
        self.ave.telaz = self.obs.telaz
        self.hot.telaz = self.obs.telaz
        self.cold.telaz = self.obs.telaz
        self.ref.telaz = self.obs.telaz
        print "Setting Azimuth  : %6.1f d" % self.obs.telaz
                              
    def set_elevation( self, elevation):
        self.obs.telel = np.float( elevation)
        self.ave.telaz = self.obs.telel
        self.hot.telaz = self.obs.telel
        self.cold.telaz = self.obs.telel
        self.ref.telaz = self.obs.telel
        print "Setting Elevation: %6.1f d" % self.obs.telel

    def set_nmedian( self, nmedian):
        nmedian = int( nmedian)
        self.obs.nmedian = nmedian
        self.ave.nmedian = nmedian
        self.hot.nmedian = nmedian
        self.cold.nmedian = nmedian
        self.ref.nmedian = nmedian
        print 'Median Count     : %d' % (self.obs.nmedian)
        t = self.obs.nmedian * self.vlen / self.obs.bandwidthHz
        print 'Average time     : %8.3f s' % (t)

    def get_setup( self):
        return self.setupFile

    def set_setup( self, setupFile):
        self.setupFile = str( setupFile)
        self.obs.read_spec_ast(self.setupFile)    # read the parameters 

    def set_obstype( self, obstype):
        self.obstype = int( obstype)
        print "Observation Type : ", radioastronomy.obslabels[self.obstype]
    
    def set_inttype( self, inttype):
        self.inttype = int( inttype)
        print "Integration Type : ", radioastronomy.intlabels[self.inttype]
    
    def set_observers( self, observers):
        observers = str( observers)
        self.obs.observer = observers
        self.ave.observers = observers
        self.ref.observer = observers
        self.cold.observers = observers
        self.hot.observers = observers
        print "Observers : ", self.obs.observer

    def set_units( self, units):
        self.units = int( units)
        print "Units     : ", radioastronomy.unitlabels[self.units]

    def set_tcold( self, tcold):
        tcold = float( tcold)
        if tcold < 3.:
            tcold = 3.
        self.tcold = tcold
        print "T_cold    : ", self.tcold

    def set_thot( self, thot):
        thot = float( thot)
        if thot < 50.:
            thot = 295.
        self.thot = thot
        print "T_hot     : ", self.thot

    def set_record( self, record):
        now = datetime.datetime.utcnow()
        self.obs.writecount = 0
        strnow = now.isoformat()
        parts = strnow.split('.')
        strnow = parts[0]
        if record == radioastronomy.INTWAIT:
            print "Stop  Averaging  : ", strnow
            self.stoputc = now
        # only restart averaging if not in averaging state
        elif self.record == radioastronomy.INTWAIT:
            print "Start Averaging  : ", strnow
            self.startutc = now
        self.record = int( record)

    def get_record( self):
        return self.record

    def get_obstype( self):
        return self.obstype

    def write_spec( self):

        strnow = self.obs.utc.isoformat()
        datestr = strnow.split('.')
        daypart = datestr[0]

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
        self.obs.write_ascii_file( self.obs.datadir, outname)


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
        n6 = int(ncp/6)
        n56 = 5*n6

        if (li != self.vlen):
            print 'spectrum length changed! %d => %d' % ( self.vlen, li)
            self.vlen = li
            self.obs.xdata = np.zeros(li)
            self.obs.ydataA = np.zeros(li)
            self.obs.ydataB = np.zeros(li)
            self.set_frequency( self.obs.centerfrequencyHz)
            self.set_bandwidth( self.obs.bandwidthHz)
            return 1

        noutports = len( output_items)
        if noutports != NSPEC:
            print '!!!!!!! Unexpected number of output ports: ', noutports

        # define output vectors
        out = output_items[0]
        ave = output_items[1]
        hot = output_items[2]
        cold = output_items[3]
        ref = output_items[4]

        nout = 0
        iout = 0 # count the number of output vectors
        li2  = 2
        li20 = int(li/20)
        li1920 = 19*li20
        linm2 = li - 2
        for i in range(nv):
            now = datetime.datetime.utcnow()
            # get the length of one input
            spec = inn[i]
#           attempt to remove DC bias, but seems to be more due to insufficient gain
            beginvalue = np.min( spec[li2:li20])
            endvalue = np.min( spec[li1920:linm2])
            minvalue = (beginvalue+endvalue)*.5
            # now subtract the DC bias
            spec = spec - np.full( self.vlen, minvalue)
            # deal with average state
            if self.inttype == radioastronomy.INTWAIT:
                self.ave.ydataB = spec
                self.nave = 1
                self.ave.ydataA = spec
                self.startutc = now
                self.obs.utc = now
                self.obs.count = self.obs.nmedian
            else: # else averaging and maybe writing
                self.ave.ydataB = self.ave.ydataB + spec
                self.nave = self.nave + 1
                oneovern = 1./np.float(self.nave)
                self.ave.ydataA = oneovern*self.ave.ydataB
                # total number of spectra averaged 
                # is the number medianed times the number averaged
                self.ave.count = self.obs.nmedian*self.nave
                self.ave.utc, duration = radioastronomy.aveutcs( self.startutc, now)
                self.ave.durationsec = duration
                # only record aveaged spectra
                # now, if updating hot, cold or references spectra
                # if saving files, must reload any configuration changes updated by the sinks
                if (self.inttype == radioastronomy.INTSAVE) and (self.nave % 10 == 1):
                    if self.obstype == radioastronomy.OBSHOT:
                        self.hot.read_spec_ast(self.setupFile)    # read the parameters 
                    elif self.obstype == radioastronomy.OBSCOLD:
                        self.cold.read_spec_ast(self.setupFile)    # read the parameters 
                    elif self.obstype == radioastronomy.OBSREF:
                        self.ref.read_spec_ast(self.setupFile)    # read the parameters 
                if self.obstype == radioastronomy.OBSHOT:
                    self.hot.ydataA = np.maximum( self.ave.ydataA, self.epsilons)
                    self.hot.nave = self.nave
                    self.hot.count = self.ave.count
                    self.hot.utc = self.ave.utc
                    self.hot.durationsec = self.ave.durationsec
                elif self.obstype == radioastronomy.OBSCOLD:
                    self.cold.ydataA = np.maximum( self.ave.ydataA, self.epsilons)
                    self.cold.nave = self.nave
                    self.cold.count = self.ave.count
                    self.cold.utc = self.ave.utc
                    self.cold.durationsec = self.ave.durationsec
                elif self.obstype == radioastronomy.OBSREF:
                    self.ref.ydataA = np.maximum( self.ave.ydataA, self.epsilons)
                    self.ref.nave = self.nave
                    self.ref.count = self.ave.count
                    self.ref.utc = self.ave.utc
                    self.ref.durationsec = self.ave.durationsec
                # if writing files, reduce write rate
                if (self.inttype == radioastronomy.INTSAVE) and (self.nave % 10 == 1):
                    if self.obstype == radioastronomy.OBSHOT:
                        self.hot.write_ascii_file( "./", HOTFILE)
                    elif self.obstype == radioastronomy.OBSCOLD:
                        self.cold.write_ascii_file( "./", COLDFILE)
                    elif self.obstype == radioastronomy.OBSREF:
                        self.ref.write_ascii_file( "./", REFFILE)
#                    else:
#                        self.ave.write_ascii_file( "./", AVEFILE)
            # after flip, the first couple channels are anomoulusly large
            spec[0:1] = spec[2]
            self.ave.ydataA[0:1] = self.ave.ydataA[2]
            self.hot.ydataA[0:1] = self.hot.ydataA[2]
            self.cold.ydataA[0:1] = self.cold.ydataA[2]
            self.ref.ydataA[0:1] = self.ref.ydataA[2]
            self.ave.nave = self.nave
            # since the data rate should be low, nout will usually be 0
            # now have all spectra, decide plot format
            if self.units == radioastronomy.UNITCOUNTS:
                out[nout] = spec
                ave[nout] = self.ave.ydataA
                hot[nout] = self.hot.ydataA
                cold[nout] = self.cold.ydataA
                ref[nout] = self.ref.ydataA
            elif self.units == radioastronomy.UNITDB:
                spec = np.maximum( spec, self.epsilons)
                self.ave.ydataA = np.maximum( self.ave.ydataA, self.epsilons)
                out[nout] = 10. * np.log10( spec)
                ave[nout] = 10. * np.log10( self.ave.ydataA)
                hot[nout] = 10. * np.log10( self.hot.ydataA)
                cold[nout] = 10. * np.log10( self.cold.ydataA)
                ref[nout] = 10. * np.log10( self.ref.ydataA)
            elif self.units == radioastronomy.UNITKELVIN:
                dc = self.hot.ydataA - self.cold.ydataA
                dc = np.maximum( dc, self.epsilons)
                Z = self.cold.ydataA/self.hot.ydataA
                oneMZ = np.full( self.vlen, 1.) - Z
                oneMZ = np.maximum( oneMZ, self.epsilons)
                tsys =  ((Z*self.thot) - self.tcold)/oneMZ
                # now compute center scalar value
                TSYS = np.median(tsys[n6:n56])
                oneoverhot = np.full(self.vlen, 1.) / self.hot.ydataA
                out[nout] = TSYS * spec * oneoverhot
                ave[nout] = TSYS * self.ave.ydataA * oneoverhot
                hot[nout] = np.full( self.vlen, TSYS)
                cold[nout] = TSYS * self.cold.ydataA * oneoverhot
                ref[nout] = TSYS * self.ref.ydataA * oneoverhot

            # completed calibration, update count of output vectors
            nout = nout + 1

            # update length to copy
            self.stoputc = now
            strnow = now.isoformat()
            datestr = strnow.split('.')
            daypart = datestr[0]
            yymmdd = daypart[2:19]
            avespec = ave[0]
            avespec = avespec[n6:n56]
            vmin = min ( avespec)
            vmax = max ( avespec)
            vmed = np.median( avespec)

            label = radioastronomy.unitlabels[self.units]
            if self.nave % 5 == 0:
                if self.units == 0:
                    print "%s %5d Max %9.2f Min: %9.2f Median: %9.2f %s " % (yymmdd, self.nave, vmax, vmin, vmed, label)
                elif self.units == 1:
                    print "%s %5d Max %9.3f Min: %9.3f Median: %9.3f %s " % (yymmdd, self.nave, vmax, vmin, vmed, label)
                else: 
                    print "%s %5d Max %9.1f Min: %9.1f Median: %9.1f %s " % (yymmdd, self.nave, vmax, vmin, vmed, label)
              
        # end for all input vectors
        return nout
    # end ra_integrate()


