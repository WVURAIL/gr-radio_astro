#Python Script to plot raw NSF record data.
#import matplotlib.pyplot as plt
#plot the raw data from the observation
#HISTORY
#17NOV21 GIL use time in file to show date and time
#16AUG29 GIL make more efficient
#16AUG16 GIL use new radiospectrum class
#15AUG30 add option to plot range fo values
#15JUL01 GIL Initial version
#
import matplotlib.pyplot as plt
import sys
import statistics
import radioastronomy
import interpolate

dy = -1.

nargs = len( sys.argv)
verbose = False  # or True

linestyles = ['-','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.']
colors = ['-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g']

scalefactor = 1e8
xallmax = -9.e9
xallmin =  9.e9
yallmax = -9.e9
yallmin =  9.e9

linelist = [1420.0, 1418.0]  # RFI lines in MHz
linewidth = [7, 7]

#for symbol, value in locals().items():

# initialize spectrum for reading and plotting
rs = radioastronomy.Spectrum()

nplot = 0

# plot no more than N spectra
for iii in range(1, min(nargs,25)):

    filename = sys.argv[iii]
    if verbose:
        print '%5d: %s' % (iii, filename)

#    print filename
    rs.read_spec_ast( filename)
# for averages can not use az,el to get ra,dec and glat, glon
#    rs.azel2radec()    # compute ra,dec from az,el 

#    print("GAL Lon,Lat: %8.3f, %8.3f"  % (rs.gallon, rs.gallat))


    parts = filename.split('/')
    nparts = len(parts)
    aname = parts[nparts-1]
    parts = aname.split('.')
    aname = parts[0]
# now compute strings for plotting
    strtime = rs.utc.isoformat()
    parts = strtime.split('T')
    date  = parts[0]
    time  = parts[1]
    time  = time.replace('_',':')
    parts  = time.split('.')
    time = parts[0]
    
    gallon = rs.gallon
    gallat = rs.gallat
    label = '%s, AZ,EL: %5s,%5s, Lon,Lat=%5.1f,%5.1f' % ( time,rs.telaz,rs.telel,gallon,gallat)
    xv = rs.xdata  * 1.E-6 # convert to MHz
    nData = len( xv)
    n6 = int(nData/6)
    n56 = 5*n6
    yv = rs.ydataA

    # The latest versions of the software had a different normalization
    ymedian = statistics.median(yv[n6:n56])
    # if the latest software, the scale factor is just 1.
    if ymedian > .001:
        scalefactor = 1.0

    yv = rs.ydataA * scalefactor
    xmin = min(xv)
    xmax = max(xv)
    xallmin = min(xmin,xallmin)
    xallmax = max(xmax,xallmax)

    yv = interpolate.lines( linelist, linewidth, xv, yv) # interpolate rfi

    ymin = min(yv)
    ymax = max(yv)
    ymed = statistics.median(yv)
    count = rs.count

    print(' Max: %9.1f  Median: %9.1f SNR: %6.2f ; %s %s' % (ymax, ymed, ymax/ymed, count, label))
    if nplot <= 0:
        fig,ax1 = plt.subplots(figsize=(10,6))
#        plt.hold(True)
        fig.canvas.set_window_title(date)
        for tick in ax1.xaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
        for tick in ax1.yaxis.get_major_ticks():
            tick.label.set_fontsize(14) 

        nplot = nplot + 1
    note = rs.noteA
#    print('%s' % note)
    yallmin = min(ymin,yallmin)
    yallmax = max(ymax,yallmax)
    plt.xlim(xallmin,xallmax)
#    plt.ylim(0.9*ymin,1.5*yallmax)
    plt.ylim(0.9*ymin,1.25*yallmax)


    plt.plot(xv, yv, colors[iii-1], linestyle=linestyles[iii-1],label=label, lw=2)
plt.title(note, fontsize=16)
plt.xlabel('Frequency (MHz)',fontsize=16)
plt.ylabel('Intensity (Counts)', fontsize=16)
plt.legend(loc='upper right')
plt.show()
