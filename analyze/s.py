#Python Script to plot summarize NSF record data.
#import matplotlib.pyplot as plt
#plot the raw data from the observation
#HISTORY
#18MAR05 GIL only summarize .hot and .ast files
#16SEP30 GIL show frequency and bandwidth
#16AUG29 GIL make more efficient
#
import sys
import statistics
import radioastronomy

dy = -1.

nargs = len( sys.argv)
if nargs < 2:
    print 'S: Summarize a list of observations'
    print 'S usage:'
    print 'S [-v] <filenames>'
    print 'where'
    print '-v          optionally print verbose summary information'
    print '<filenames> list of file names to summarize'
    print '  Only *.ast, *.hot and *.cld files will be read. Others will be skipped'
    exit()

linestyles = ['-','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.','-','--','-.']
colors = ['-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g','-b','-r','-g']

scalefactor = 1e8
xallmax = -9.e9
xallmin =  9.e9
yallmax = -9.e9
yallmin =  9.e9

#for symbol, value in locals().items():
#    print symbol, value
lastaz = 0.
lastel = 0.
lastfreq = 0.
lastbw = 0
lastgain = 0.
nsame = 0
nread = 0

labelfmt = '%s %5s,%5s %5.1f,%5.1f: %8.2f,%5.2f %5.1f - %s' 
names = sys.argv[1:nargs]
names = sorted(names)

##label = labelfmt % (time,rs.telaz,rs.telel,gallon,gallat,freq,bw,gain, filename)
rs = radioastronomy.Spectrum()

if names[0] == '-v':
    verbose = True
    names = names[1:]
else:
    verbose = False

for filename in names:

#    print filename
    parts = filename.split('/')
    nparts = len(parts)
    aname = parts[nparts-1]
    parts = aname.split('.')
    nparts = len(parts)
    if nparts < 2:
        continue
# only summarize astronomy files
    if (parts[1] != 'ast') and (parts[1] != 'hot') and (parts[1] != 'cld'):
        continue
    if verbose:
        print 'File: ',filename
    rs.read_spec_ast( filename)
    rs.azel2radec()    # compute ra,dec from az,el

    gallon = rs.gallon
    gallat = rs.gallat
    freq = rs.centerFreqHz / 1.E6
    bw = rs.bandwidthHz / 1.E6
    gain = rs.gains[0]
    parts = filename.split('/')
    nparts = len(parts)
    aname = parts[nparts-1]
    parts = aname.split('.')
    adatetime = str(rs.utc)
    parts = adatetime.split(' ')
    date  = parts[0]
    time  = parts[1]
    parts  = time.split('.')
    time = parts[0]

    if rs.telaz != lastaz or rs.telel != lastel or lastbw != bw or lastfreq != freq or lastgain != gain:
        lastbw = bw
        lastfreq = freq
        lastaz = rs.telaz
        lastel = rs.telel
        lastgain = gain

        if nread == 0:
            label = (labelfmt % (time,rs.telaz,rs.telel,gallon,gallat,freq,bw,gain,filename))
        elif nsame > 1:
            print "%4d %s " % (nsame, label)
        label = labelfmt % (time,rs.telaz,rs.telel,gallon,gallat,freq,bw,gain, filename)
        if nread == 0:
            print 'Count  Time    Az    El   G-Lon G-Lat  Frequency  BW   Gain    Filename'
        print "%4d %s " % (1, label)
        nsame = 1
    else:
        nsame = nsame + 1

    nread = nread + 1
    label = labelfmt % (time,rs.telaz,rs.telel,gallon,gallat,freq,bw,gain, filename)

if nsame > 0:
    print "%4d %s " % (nsame, label)
