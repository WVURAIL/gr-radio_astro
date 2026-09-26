"""
Class for computing the System Temperature from hot and cold loads
Cashes the hot+cold and off spectra as theses will remain relatively constant
Revised to store more data
"""

##################################################
# Imports
##################################################
try:
    import statistics
except ImportError:
    print('Missing statistics python Code!')
    print('If using Linux, type the following:')
    print('  sudo pip3 install statistics')
    raise RuntimeError("Please Install statistics!")
    
import radioastronomy
import numpy as np

MAXCHAN = 4096

def medianfilter(mydata, nwidth):
    """
    Compute median filtered version of a vector
    nwidth is the half width of the filter, in samples.
    """
    ndata = len( mydata)
    if nwidth < 2:
        print(("Median Width too small: %d < 2" % (nwidth)))
        return( mydata)
    if ndata < nwidth:
        print(("Data array too small: %d < width (%d)" % (ndata, nwidth)))
        return( mydata)
    # initialize the output array
    outdata = mydata
    for iii in range(ndata):
        b = iii - nwidth
        e = iii + nwidth + 1
        if b < 0:
            b = 0
        if e >= ndata:
            e = ndata-1
#        if iii > ndata-(2*nwidth):
#            print("%d (%d to %d)" % (iii, b, e))
        a = statistics.median(mydata[b:e]) 
        b = statistics.median(mydata[(b+1):(e-1)]) 
        outdata[iii] = (a + b)/2.
    return outdata

class Tsys(object):
    """

    """
    def __init__(self):
        """
        initialize the components of the system temperature class
        """
        self.hot = radioastronomy.Spectrum()
        self.cold = radioastronomy.Spectrum()
        self.off = radioastronomy.Spectrum()
        self.tsys = radioastronomy.Spectrum()
        self.thot = 285.    # hot load (ground) temp
        self.tcold = 10.    # kelvins (feed+cmb+cables before 1st amp)
        self.dt = self.thot - self.tcold
        self.tmax  = 1000.  # maximum allowed returned hot load
        self.useoff = False
        self.usehot = False
        self.offdata = np.zeros(MAXCHAN+1)
        self.gain = np.zeros(MAXCHAN+1)
        self.epsilon = 1.E-9 # minimum counts for division

    def tmedian(self):
        """
        Compute median tsys value
        """
        tsys = 0.
        ndata =self.hot.nChan        #        print 'ndata = ',ndata
        bdata = int(ndata/4)
        edata = int(3*ndata/4)
        if ndata < 1:
            return tsys
#        yminhot = min(self.hot.ydataA[bdata:edata]-self.offdata[bdata:edata])
#        ymaxhot = max(self.hot.ydataA[bdata:edata]-self.offdata[bdata:edata])
        yminhot = min(self.hot.ydataA[bdata:edata])
        ymaxhot = max(self.hot.ydataA[bdata:edata])
        chot = 0.
        ccold = 0.
#        print 'Y Hot  min,max: ',yminhot,ymaxhot
        if yminhot != ymaxhot:
            chot = statistics.median(self.hot.ydataA[bdata:edata])
#        ymincold = min(self.cold.ydataA[bdata:edata]-self.offdata[bdata:edata])
#        ymaxcold = max(self.cold.ydataA[bdata:edata]-self.offdata[bdata:edata])
        ymincold = min(self.cold.ydataA[bdata:edata])
        ymaxcold = max(self.cold.ydataA[bdata:edata])
#        print 'Y Cold min,max: ',ymincold,ymaxcold
        if ymincold != ymaxcold:
            ccold = statistics.median(self.cold.ydataA[bdata:edata])
#        print 'hot,cold: ', chot, ccold
        # if there is a difference between the hot and cold load values
        if (chot - ccold) != 0:
            tsys = ((self.dt * ccold))/(chot - ccold)
        else:
            print("No differnce between hot and cold load counts")
        return tsys

    def tcalc( self, yhot, ycold, yoff):
        """
        Compute tsys arrays using arrays of yhot, ycold, yoff values
        """
        # compoueif there is a difference between the hot and cold load values
        dy = yhot[:MAXCHAN] - ycold[:MAXCHAN]  # difference between hot and cold load
        indicies = dy < self.epsilon # compute indicies of small differences 
        dy[indicies] = self.epsilon  # set minimum offsets
#        tsys = self.dt * (ycold[:MAXCHAN]-yoff[:MAXCHAN])/dy[:MAXCHAN]
        tsys = self.dt * ycold[:MAXCHAN]/dy[:MAXCHAN]
        return tsys

    def tmedian(self):
        """
        Compute median tsys value
        """
        tsys = 0.
        ndata =self.hot.nChan        #        print 'ndata = ',ndata
        bdata = int(ndata/4)
        edata = int(3*ndata/4)
        if ndata < 1:
            return tsys
        tsys = self.tcalc( self.hot.ydataA, self.cold.ydataA, self.offdata)
        tmed = statistics.median(tsys[bdata:edata])
        return tmed

    def __str__(self):
        """
        Define a spectrum summary string
        """
        tsys = self.tmedian()
        return "({0}, {1}, {2})".format(self.thot, self.tcold, tsys)

    def hotcalc(self):
        """
        Compute the parameters needed for repeated computations with the hot load.
        This module assumes hot load temperature has been set and the hot load data read.
        """
        indicies = self.hot.ydataA < self.epsilon  # avoid divide by zero
        samples = self.hot.ydataA
        samples[indicies] = self.epsilon    # set values to min
        self.hot.ydataB = self.thot/samples # conversion from counts to kelvins
        return

    def gaincalc(self):
        """
        Compute the parameters needed for repeated computations with the hot load.
        This module assumes hot+cold load temperatures have been set and
        the hot load and cold load data read.
        """
        deltas = self.hot.ydataA[:MAXCHAN] - self.cold.ydataA[:MAXCHAN]
        indicies = deltas < self.epsilon  # avoid divide by zero
        deltas[indicies] = self.epsilon
        self.gain = self.dt/deltas
        indicies = self.hot.ydataA < self.epsilon
        samples = self.hot.ydataA
        samples[indicies] = self.epsilon
        thot = statistics.median( samples[:MAXCHAN]*self.gain[:MAXCHAN])
        if thot > self.dt:
            print("gaincalc: Hot Load Equivalent Temperature: %8.3f (K)" % (thot))
        self.gain = thot/samples[:MAXCHAN]
        return

    def readhot(self, hotname):
        """
        Read in the hot load intensity values Counts) for calibration.
        """
        self.hot.read_spec_ast(hotname)
        if len(self.hot.ydataA) > 0:
            self.usehot = True

    def readoff(self, offname):
        """
        Read in the hot load intensity values Counts) for calibration.
        """
        self.off.read_spec_ast(offname)
        if len(self.off.ydataA) > 0:
#            self.useoff = True
            self.offdata = self.off.ydataA

    def readcold(self, coldname):
        """
        Read in the cold load intensity values Counts) for calibration.
        """
        self.cold.read_spec_ast(coldname)

    def tsysvalues(self, ycounts):
        """
        Return the system temperature array, based on cashed hot load parameters
        """
        tsys[:MAXCHAN] = ycounts[:MAXCHAN] * self.gain[:MAXCHAN]
        indicies = tsys > self.tmax
        tsys[indicies] = self.tmax
        return tsys

    def tvalues(self):
        """
        Return the calibrated difference between the reference (cold) spectrum and
        the current spectrum
        """
        # subtract the counts from the reference location
        # now multiply by the gain factor
        tsys = 0.
        ndata =self.hot.nChan
        if ndata < 1:
            return tsys
        tsys = self.tcalc( self.hot.ydataA, self.cold.ydataA, self.offdata)
        self.tsys.ydataA = tsys
        return tsys # return temperatures without correction for reference location

    def tsky(self, ysky):
        """
        Return the calibrated difference between the reference (cold) spectrum and
        the current spectrum
        """
        # subtract the counts from the reference location
        # now multiply by the gain factor
#        tsys = self.gain[:MAXCHAN] * (ysky[:MAXCHAN] - self.offdata[:MAXCHAN])
        tsys = self.gain[:MAXCHAN] * ysky[:MAXCHAN]
        indicies = tsys < 0.       # keep plot within range
        tsys[indicies] = 0.
        indicies = tsys > self.tmax
        tsys[indicies] = self.tmax
        return tsys # return temperatures without correction

# HISTORY
# 17JAN10 GIL disable off use in calibration
# 16OCT11 GIL separate array-only function
# 16OCT10 GIL correction for offdata
# 16SEP06 GIL initial version
