#Python Script to interpolate frequencies that have RFI
#HISTORY
#16Dec19 GIL check for changes in frequency and/or gain

import numpy as np
import copy

def lines( linelist, lineWidth, x, y):
    """
    lines takes a list of lines to interpoate, interpolates over the RFI
    linelistHz  list of line frequencies (same units as x vector)
    lineWidth   width of lines to interpolate (channels)
    x =        frequencies in the same units as linelist
    y =        intensities (arbirary units)
    """

    nline = len( linelist) 
    nwidth = len( lineWidth)  # use last value if more lines than widths

    nx = len(x)
    nx2 = int(nx/2)
    ny = len(y)
    if nx != ny:
        print "x and y data do not match", nx, ny
        return y

    yout = copy.deepcopy(y) # init the output
    
    increasing = x[nx2+1] > x[nx2]

    for jjj in range( nline): # for all iines
        
        # find line position
        nu = linelist[jjj]
        if nwidth == 1:
            nwidth = lineWidth 
        else:
            nwidth = lineWidth[min(jjj,nwidth-1)]
        nwidth2 = max(1, nwidth/2)
        iline = 0

        for iii in range(nwidth2, nx-nwidth2+1):
            if increasing: # if x increasing with channel
                if x[iii] <= nu and nu < x[iii+1]:
                    iline = iii+1
                    break
            else:  # else x decreasing with chanel
                if x[iii] >= nu and nu > x[iii+1]:
                    iline = iii+1
                    break
        
        if iline == 0:       # if line not in data
            continue

#        print 'Line %d: %f, %d; %f,%f' % (jjj, nu, nwidth2, x[iline-nwidth2],y[iline-nwidth2])
#        print 'Line %d: %f, %d; %f,%f' % (jjj, nu, nwidth2, x[iline],y[iline])
#        print 'Line %d: %f, %d; %f,%f' % (jjj, nu, nwidth2, x[iline+nwidth2],y[iline+nwidth2])

# if here found the line
        ya = y[iline-nwidth2]
        yb = y[iline+nwidth2]
        for iii in range( 0, nwidth):
            kkk = iii+iline-nwidth2
            yout[kkk] = ((ya * (nwidth-iii)) + (yb * iii))/float(nwidth)
#            print 'Line %d: %f,%f' % (kkk, y[kkk], yout[kkk])
 
    return yout
