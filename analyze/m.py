#Python Script to plot raw NSF record data.
#import matplotlib.pyplot as plt
#plot the raw data from the observation
#HISTORY
#18MAY01 GIL plotting of last average spectrum
#18MAR05 GIL implement folding option
#18FEB06 GIL keep track of first az,el
#17AUG18 GIL plot the last spectrum in the series
#17AUG17 GIL Note elevation range
#16Oct07 GIL check for changes in frequency and/or gain
#16AUG29 GIL make more efficient
#16AUG16 GIL use new radiospectrum class
#15AUG30 add option to plot range fo values
#15JUL01 GIL Initial version
#
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime
import statistics
import radioastronomy
import copy
from scipy.signal import savgol_filter
import interpolate

avetimesec = 3600.
dy = -1.
linelist = [1420.0, 1419.0, 1418.0]  # RFI lines in MHz
linewidth = [9, 5, 7]
verbose = False

nargs = len(sys.argv)
#first argument is the averaging time in seconds
timearg = 1
namearg = 2

# if folding data
if sys.argv[1] == '-f':
    print 'Folding specectra'
    dofold = True
    timearg = timearg+1
    namearg = namearg+1
else:
    dofold = False

avetimesec = float(sys.argv[timearg])
print "Average time: ", avetimesec, " (seconds)"

linestyles = ['-','-','-', '-.','-.','-.','--','--','--','-','-','-', '-.','-.','-.','--','--','--','-','-','-', '-.','-.','-.','--','--','--','-','-','-', '-.','-.','-.','--','--','--']
colors =  ['-b','-r','-g', '-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g']
nmax = len(colors)
scalefactor = 1e8
xallmax = -9.e9
xallmin = 9.e9
yallmax = -9.e9
yallmin = 9.e9
# velocities for fitting baselines
minvel = -450.
minvel = -280.
maxvel = 210.
# currently used
maxvel = 160.
minvel = -160.
# currently used
maxvel = 200.
minvel = -180.

c = 299792.  # (v km/sec)
nuh1 = 1420.4056 # neutral hydrogen frequency (MHz)
thot = 285.0  # define hot and cold
#thot = 272.0  # 30 Farenheit = 272 K
tcold = 10.0
tmin = 20.0 
tmax = 999.0 # define reasoanable value limits

# prepare to remove a linear baseline

xa = 200
#xb = 1024-xa
xb = 1024-200

#for symbol, value in locals().items():
#    print symbol, value

nplot = 0
nhot = 0         # number of obs with el < 0
ncold = 0
nhigh = 0        # highest galactic latitude
minGlat = +90.
maxGlat = -90.
lastfreq = 0.
lastbw = 0.
lastgain = 0.
lastel = 0.
lastaz = 0.
firstdate = ""
lastdate = ""
minel = 200.
maxel = -200.
firstaz = -1
otheraz = -1

#first argument is the averaging time in seconds
names = sys.argv[namearg:]
names = sorted(names)
nFiles = len(names)
rs = radioastronomy.Spectrum()

for filename in names:

    parts = filename.split('/')
    nparts = len(parts)
    if nparts == 1:
        aname = parts[0]
    else:
        aname = parts[nparts-1]
    parts = aname.split('.')
    nparts = len(parts)
    if nparts < 2:
        print 'File is not an astronomy file: ',filename
        continue
    else:
        extension = parts[nparts-1]
    extension = extension.upper()
    if (extension != 'HOT') and (extension != 'AST') and (extension != 'CLD'):
        print 'Extension not recognized : ', parts[nparts-1]
        continue

    rs.read_spec_ast(filename)
    rs.azel2radec()    # compute ra,dec from az,el
    if dofold:
        rs.foldfrequency()

    if rs.telel < 0:
        if nhot == 0:
            hot = copy.deepcopy( rs)
            nhot = 1
        else:
            hot.ydataA = hot.ydataA + rs.ydataA
            hot.count = hot.count + rs.count
            nhot = nhot + 1
    else: # else above horizon, find min, max galactic latitudes
        if rs.gallat > maxGlat:
            maxGlat = rs.gallat
        if rs.gallat < minGlat:
            minGlat = rs.gallat
        if minel > rs.telel:
            minel = rs.telel
        if maxel < rs.telel:
            maxel = rs.telel
        if firstaz < 0:
            firstaz = rs.telaz
            otheraz = firstaz
        if firstaz != rs.telaz:
            otheraz = rs.telaz
            
if nhot > 0:
    hot.ydataA = scalefactor * hot.ydataA / float(nhot)
    print "Found %3d hot load obs" % nhot
else:
    print "No hot load data, can not calibrate"
    exit()

xv = hot.xdata * 1.E-6
yv = hot.ydataA
nData = len(xv)
#previously just copy
#hv = yv
hv = interpolate.lines( linelist, linewidth, xv, yv) # interpolate rfi

vel = np.zeros(nData)
# create index array
iv = np.zeros(nData)
for jjj in range (0, nData):
    vel[jjj] = c * (nuh1 - xv[jjj])/nuh1
    iv[jjj] = jjj

# velocity decreases with increasing channel #
for jjj in range (1, (nData-1)):
    if (minvel < vel[jjj]) and (minvel >= vel[jjj+1]):
        xa = jjj
    if (maxvel < vel[jjj]) and (maxvel >= vel[jjj+1]):
        xb = jjj

print 'Min Vel at channel: ',xa, minvel
print 'Max Vel at channel: ',xb, maxvel
                                   
# will need smoothed hot load values in remaining calc
#for iii in range(1,(nData-2)):
#    hv[iii] = (yv[iii-2]+yv[iii-1]+yv[iii]+yv[iii+1]+yv[iii+2])/5.
#hv = yv

print 'Min,Max Galactic Latitudes %7.1f,%7.1f (d)' % (minGlat, maxGlat)

# assume only a limited range of galactic latitudes are available
# not range about +/-60.
use60Range = False

# all galactic latitudes above +/-60d can be used
if minGlat < -60. or maxGlat > 60.:
    minGlat = -60.
    maxGlat = 60.
else: # else no high galactic latitude data
    # use highest galactic latitudes - +/-5.degrees
    if -minGlat > maxGlat:  # if negative latitudes higher
        minGlat = minGlat + 5.
        maxGlat = 90.
    else: # else positive latitudes higher
        maxGlat = maxGlat - 5.
        minGlat = -90.

# but if no low latitude data are available use minimum
# now average coldest data for calibration
for filename in names:

    rs = radioastronomy.Spectrum()
    rs.read_spec_ast(filename)
    rs.azel2radec()    # compute ra,dec from az,el
    if dofold:
        rs.foldfrequency()

    if rs.telel < 0:
        continue
    if rs.gallat > maxGlat or rs.gallat < minGlat:
        if nhigh == 0:
            high = copy.deepcopy( rs)
            high.ydataA = rs.ydataA
            nhigh = 1
        else:
            high.ydataA = high.ydataA + rs.ydataA
            high.count = high.count + rs.count
            nhigh = nhigh + 1

if nhigh < 1.:
    print "No high galactic latitude data: can not calibrate"
    exit()
else:
    high.ydataA = scalefactor * high.ydataA/nhigh
    print "Found %d High Galactic Latidue spectra" % (nhigh)
    yv = high.ydataA

    cv = interpolate.lines( linelist, linewidth, xv, yv) # interpolate rfi

# finally compute gain on a channel by chanel basis
gain = np.zeros(nData)
for iii in range(nData):
    gain[iii] = (hv[iii] - cv[iii])/(thot - tcold)
#    gain[iii] = hv[iii]/thot

def compute_tsky_hotcold( xv, yv, hv, cv, thot, tcold):
    """
    compute_tskk_hotcold() does a full computation of tsys, based on
    Observations of a hot load and a cold sky observation
    """
    nData = len(xv)
    vel = np.zeros(nData)
    tsys = np.zeros(nData)    # initialize arrays
    tsky  = np.zeros(nData)    # initialize arrays

    for jjj in range (0, nData):
        vel[jjj] = c * (nuh1 - xv[jjj])/nuh1
        tsys[jjj] = yv[jjj]/gain[jjj]
        tsky[jjj] = tsys[jjj] - Tsys

    iref = int(nData/2)
    vref = vel[iref]
    dv   = (vel[iref+2]-vel[iref-2])/4.
    imin = int(((minvel - vref)/dv) + iref)
    imax = int(((maxvel - vref)/dv) + iref) + 1
    if imax < imin: # swap indices if frequency opposit velocity
        temp = imin
        imin = imax
        imax = temp

    if imin < 0:
        print 'Imin Error computing baseline: ', imin
        imin = 0
    if imin >= nData:
        print 'Imin Error computing baseline: ', imin
        imin = nData-1

    if imax < 0:
        print 'Imax Error computing baseline: ', imax
        imax = 0
    if imax >= nData:
        print 'Imax Error computing baseline: ', imax
        imax = nData-1

    ya = statistics.median(tsky[(xa-10):(xa+10)])
    yb = statistics.median(tsky[(xb-10):(xb+10)])
    slope = (yb-ya)/(xb-xa)
#                baseline = tsky
#                print 'ya,b: %6.1f,%6.1f; slope: %8.4f' % (ya, yb, slope)
    for iii in range( nData):
        tsky[iii] = tsky[iii] - (ya + (slope*(iii-xa)))

    return tsky, vel

fig, ax1 = plt.subplots(figsize=(10, 6))
#plt.hold(True)
az = hot.telaz
el = hot.telel
ymin = 1000.  # initi to large values
ymax = 0.
yallmin = ymin
yallmax = ymax
ymed = statistics.median(yv)
count = hot.count
ncold = 0

# set indicies for normalizing intensities
bData = 790
eData = 900
bData = int(3*int(nData/10))
eData = int(6.5*int(nData/10))

# compute median raw values
hotmedian = statistics.median(hv[bData:eData])
coldmedian = statistics.median(cv[bData:eData])
hvnorm = (1./hotmedian) * hv
cvnorm = (1./coldmedian) * cv

#
deltanorm = cvnorm - hvnorm
deltanorm = deltanorm + 1.0
zeronorm = 0.0*deltanorm + 1.0

# copute the reciever temperature
trx = np.zeros(nData)
zeros = np.zeros(nData)
for iii in range(nData):
    trx[iii] = (cv[iii]/gain[iii]) - tcold

Tsys = statistics.median(trx[bData:eData])
print "Median Receiver + Antenna Temp: ", Tsys

#plt.plot(xv, trx, colors[1], linestyle=linestyles[0],label="Tsys")
#plt.legend(loc='upper left')
#plt.show()

avetime = datetime.timedelta(seconds=avetimesec)

#plt.plot(vel, hv, colors[0], linestyle=linestyles[3],label="hot")

nRead = 0        

# now read through all data and average cold sky obs
for filename in names:

    parts = filename.split('/')
    nparts = len(parts)
    aname = parts[nparts-1]
    parts = aname.split('.')
    aname = parts[0]
    extension = parts[1]
    nRead = nRead + 1
# exclude hot load data for averaging
    if extension == 'hot':
        continue

    rs = radioastronomy.Spectrum()
#  print filename
    rs.read_spec_ast(filename)
    rs.azel2radec()    # compute ra,dec from az,el
    if dofold:
        rs.foldfrequency()

    dt = str(rs.utc)
    parts = dt.split(' ')
    date = parts[0]
    nd = len(date)
    date = date[2:nd]
    time = parts[1]
    time = time.replace('_', ':')  # put time back in normal hh:mm:ss format
    parts = time.split('.')  # trim off seconds part of time
    time = parts[0]

    if firstdate == "":
        firstdate = date

# if a sky observation
    if rs.telel > 0.:

# if first time reading data, set obs parameters
        if lastfreq == 0.:
            lastfreq = rs.centerFreqHz 
            lastbw = rs.bandwidthHz
            lastgain = rs.gains[0]
            lastaz = rs.telaz
            lastel = rs.telel
            cold = copy.deepcopy( rs)
            crosszero = False
            firstlon = rs.gallon
            ncold = 0

        if ncold > 0:
            # time difference is between mid-points of integrations
            dt = rs.utc - cold.utc 
            # add the time since midpoint of latests
            dt = dt + datetime.timedelta(seconds=rs.durationSec/2.)
            # plus time before start of the first
            dt = dt + datetime.timedelta(seconds=cold.durationSec/2.)

            lastdate = date

            newAzEl = (lastaz != rs.telaz) or (lastel != rs.telel)
            newObs = (lastfreq != rs.centerFreqHz) or (lastbw != rs.bandwidthHz) or (lastgain != rs.gains[0]) or newAzEl
            if newObs:
                print "Change in observing parameters: "
                if lastfreq != rs.centerFreqHz:
                    print "LastFreq: ", lastfreq/1e6, "New: ", rs.centerFreqHz/1e6, " MHz"
                    lastfreq = rs.centerFreqHz
                if lastbw != rs.bandwidthHz:
                    print "LastBandwidth: ", lastbw/1e6, "New: ", rs.bandwidthHz/1e6, " MHz"
                    lastbw = rs.bandwidthHz
                if lastgain != rs.gains[0]:
                    print "LastGain: ", lastgain, "New: ", rs.gains[0], " dB"
                    lastgain = rs.gains[0]
                if newAzEl:
                    print "LastAzEl: ", lastaz,lastel, "New: ", rs.telaz,rs.telel, " degrees"
                    lastaz = rs.telaz
                    lastel = rs.telel

           # if time to average (or end of all files)
            if (dt > avetime) or (filename == sys.argv[nargs-1]) or newObs:
                cold.ydataA = cold.ydataA/float(timesum)

                gallon = cold.gallon/float(timesum)
                if gallon > 360.:
                    gallon = gallon - 360.
                elif gallon < 0.:
                    gallon = gallon + 360.
                    
                gallat = cold.gallat/float(timesum)
                az = cold.telaz
                el = cold.telel

                xv = cold.xdata * 1.E-6
                yv = cold.ydataA * scalefactor
                yv = interpolate.lines( linelist, linewidth, xv, yv) # interpolate rfi

                xmin = min(xv)
                xmax = max(xv)
                xallmin = min(xmin, xallmin)
                xallmax = max(xmax, xallmax)
                count = cold.count
                note = cold.noteA
                    #print('%s' % note)
                ncolor = min(nmax-1, nplot) 

                label = 'L,L=%5.1f,%5.1f' % (gallon, gallat)

                tsky, vel = compute_tsky_hotcold( xv, yv, hv, cv, thot, tcold)
                ymed = statistics.median(tsky)

                ymin = min(tsky[(1*nData/4):(3*nData/4)])
                ymax = max(tsky[(1*nData/4):(3*nData/4)])
                yallmin = min(ymin,yallmin)
                yallmax = max(ymax,yallmax)
                avedatetime = cold.utc.isoformat()
                dates = avedatetime.split('T')
                atime = dates[1]
                timeparts = atime.split('.')
                labeltime = timeparts[0]
                label = '%s, A,E: %5s,%5s, L,L: %5.1f,%5.1f' % (labeltime, az, el, gallon, gallat)
                if minel == maxel:
                    label = '%s L,L=%5.1f,%5.1f' % (labeltime, gallon, gallat)
                else:
                    label = '%s L,L=%5.1f,%4.1f A,E=%4.0f,%4.0f' % (labeltime, gallon, gallat, az, el)
                if ncold > 0:
                    print ' Max: %9.1f  Median: %9.1f SNR: %6.2f ; %s %s' % (ymax, ymed, ymax/ymed, ncold, label)
                    if gallat < 7.5 and gallat > -7.5:
                        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label, lw=4)
                    elif gallat < 15. and gallat > -15.:
                        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label, lw=2)
                    else:
                        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label)
                    nplot = nplot + 1
                ncold = 0
                if nRead >= nFiles:
                    break
            # end if a new observation
            # end if a cold file
            if nRead >= nFiles:
                break

# if this was a new obs; restart the sums
        if ncold == 0:
            cold = copy.deepcopy(rs)  # initial spectrum is one just read
            ncold = 1
#            print 'Xmin: ', min(cold.xdata)/1e6, 'Xmax: ', max(cold.xdata),' MHz'
            # sums are weighted by durations
            crossZero = False
            firstlon = rs.gallon
            cold.ydataA = rs.ydataA * cold.durationSec
            cold.gallat = rs.gallat * cold.durationSec
            cold.gallon = rs.gallon * cold.durationSec
            # keep track of observing time for weighted sum
            timesum = rs.durationSec
        else: # else ont enough time yet, average cold data
            cold.count = cold.count + rs.count
            ncold = ncold + 1
            cold.ydataA = cold.ydataA + (rs.ydataA * cold.durationSec)
            # fix wrap of longitudes
            if abs(rs.gallon - firstlon) > 180:
                crossZero = True
                if rs.gallon > firstlon:
                    rs.gallon = rs.gallon - 360.
                else:
                    rs.gallon = rs.gallon + 360.
            cold.gallon = cold.gallon + (rs.gallon * cold.durationSec)
            cold.gallat = cold.gallat + (rs.gallat * cold.durationSec)
            # keep track of observing time for weighted sum
            timesum = timesum + rs.durationSec
            # end if not a enough time

        # end if a cold file
        if nRead >= nFiles:
            break

    #end for all files to sum
# end of all files to read

if verbose:
    print 'Number of remaining observations not yet plotted: ', ncold

# if data remaing from summation
if ncold > 1:
    cold.ydataA = cold.ydataA/float(timesum)

    gallon = cold.gallon/float(timesum)
    if gallon > 360.:
        gallon = gallon - 360.
    elif gallon < 0.:
        gallon = gallon + 360.
                    
    gallat = cold.gallat/float(timesum)
    az = cold.telaz
    el = cold.telel

    xv = cold.xdata * 1.E-6
    yv = cold.ydataA * scalefactor
    yv = interpolate.lines( linelist, linewidth, xv, yv) # interpolate rfi
    
    xmin = min(xv)
    xmax = max(xv)
    xallmin = min(xmin, xallmin)
    xallmax = max(xmax, xallmax)
    count = cold.count
    note = cold.noteA
    ncolor = min(nmax-1, nplot) 

    tsky, vel = compute_tsky_hotcold( xv, yv, hv, cv, thot, tcold)
    ymed = statistics.median(tsky)

    ymin = min(tsky[(2*nData/4):(3*nData/4)])
    ymax = max(tsky[(2*nData/4):(3*nData/4)])
    yallmin = min(ymin,yallmin)
    yallmax = max(ymax,yallmax)
    avedatetime = cold.utc.isoformat()
    dates = avedatetime.split('T')
    atime = dates[1]
    timeparts = atime.split('.')
    labeltime = timeparts[0]
    if minel == maxel:
        label = '%s L,L=%5.1f,%5.1f' % (labeltime, gallon, gallat)
    else:
        label = '%s L,L=%5.1f,%5.1f A,E=%4.0f,%4.0f' % (labeltime, gallon, gallat, az, el)
    print ' Max: %9.1f  Median: %9.1f Tsys: %6.2f ; %s %s' % (ymax, ymed, ymax/ymed, ncold, label)
    if gallat < 7.5 and gallat > -7.5:
        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label, lw=4)
    elif gallat < 15. and gallat > -15.:
        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label, lw=2)
    else:
        plt.plot(vel, tsky, colors[ncolor], linestyle=linestyles[ncolor],label=label)
    nplot = nplot + 1
        
# if observations cover multiple days
if firstdate != lastdate:
    date = firstdate + " - " + lastdate
else:
    date = firstdate

mytitle = "%s    " % (date)
if (firstaz == otheraz):
    mytitle = mytitle + "Az = %6.1f, " % (firstaz)
else:
    mytitle = mytitle + "Az = %6.1f to %6.1f, " % (firstaz, otheraz)

if minel == maxel:
    mytitle = mytitle + " El=%6.1f" % (minel)
else:
    mytitle = mytitle + " El=%6.1f to %6.1f" % (minel, maxel)

fig.canvas.set_window_title(mytitle)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
    # specify integer or one of preset strings, e.g.
    #tick.label.set_fontsize('x-small') 
    #tick.label.set_rotation('vertical')
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
    # specify integer or one of preset strings, e.g.
    #tick.label.set_fontsize('x-small') 
    #tick.label.set_rotation('vertical')
#plt.xlim(-400., 250.)
#plt.xlim(-250., 300.)
#plt.xlim(-500., 300.)
#plt.xlim(xallmin,xallmax)
#plt.xlim(-120., 130.)
#plt.xlim(-200., 200.)
plt.xlim(-150., 300.)
if yallmax < 8:
    yallmax = 8
# set the y scale to go above and below all data
plt.ylim((yallmin*.97)-1., 1.15*yallmax)
#plt.ylim(-2., 8.)
#plt.ylim(yallmin*.97, 50.)
#plt.ylim( 0, max(hv))
plt.title(mytitle, fontsize=16)
plt.xlabel('Velocity (km/sec)', fontsize=16)
plt.ylabel('Intensity (Kelvins)', fontsize=16)
#plt.legend(loc='upper left')
plt.legend(loc='upper right')
plt.show()
