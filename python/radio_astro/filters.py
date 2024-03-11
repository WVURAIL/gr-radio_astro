"""
filtering utilities for vectors median filter utility
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
    
import numpy as np

def median(mydata, nwidth):
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
        outdata[iii] = statistics.median(mydata[b:e]) 
    return outdata

def smooth(mydata, nwidth):
    """
    Compute median filtered version of a vector
    nwidth is the half width of the filter, in samples.
    """
    ndata = len( mydata)
    if ndata < nwidth:
        print(("Data array too small: %d < width (%d)" % (ndata, nwidth)))
        return( mydata)
    # initialize the output array
    outdata = mydata
    nwidth1 = nwidth + 1
    for iii in range(ndata):
        b = iii - nwidth
        e = iii + nwidth
        if b < 0:
            b = 0
        if e >= ndata:
            e = ndata-1
#        if iii > ndata-(2*nwidth):
#            print("%d (%d to %d)" % (iii, b, e))
        outdata[iii] = np.average(mydata[b:e]) 
    return outdata

def hanning( indata, ndata):
   """
   Hanning filter a vector
   """
   # hanning weights: 0.25*x[i-1] + 0.5*x[i] + 0.25*x[i+1]
   
   outdata = 2. * indata
   outdata[1:ndata-1] += indata[0:ndata-2] + indata[2:ndata]
   # normalize sum of for copies
   outdata = 0.25 * outdata
   # ends are not filtered
   outdata[0] = indata[0]
   outdata[ndata-1] = indata[ndata-1]
   return outdata
