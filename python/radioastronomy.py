"""
Class defining a Radio Frequency Spectrum
Includes reading and writing ascii files
HISTORY
18APR18 GIL add NAVE to save complete obsevering setup
18MAR10 GIL add labels for different integration types
18APR01 GIL add labels for different observing types
18MAR28 GIL merge in iplatlon with gnuradio companion upates
18MAR05 GIL add device parameter
18JAN25 GIL add all info included in the notes (.not) file
16JAN01 GIL initial version
"""

##################################################
# Imports
##################################################
import datetime
import numpy
import copy
import angles
try:
    import ephem
except ImportError:
    print 'Ephemerous Python Code needed!'
    print 'In Linux type:'
    print '       sudo apt-get install python-dev'
    print '       sudo apt-get install python-pip'
    print '       sudo pip install pyephem'
    print ''
    exit()

MAXCHAN = 1024
OBSSURVEY = 0
OBSHOT = 1
OBSCOLD = 2
OBSREF = 3
NOBSTYPES = 4
obstypes = [ OBSSURVEY, OBSHOT, OBSCOLD, OBSREF]
obslabels = [ 'SURVEY', 'HOT', 'COLD', 'REFERENCE' ]
# flags for recording state (either wait or record)
INTWAIT = 0
INTRECORD = 1
INTSAVE = 2
NINTTYPES = 3
intlabels = [ 'WAIT', 'RECORD', 'SAVE']
# Units for calibration
UNITCOUNTS = 0
UNITDB = 1
UNITKELVIN = 2
UNITJANSKY = 3
NUNITTYPES = 4
units = [ UNITCOUNTS, UNITDB, UNITKELVIN, UNITJANSKY]
unitlabels = [ 'Counts', 'Power (dB)', 'Kelvin', 'Jansky']

### average two utcs using the strange steps required by datetime
def aveutcs( utc1, utc2):
    """
    Ave Utcs takes as input two utc time and returns the average of these utcs
    Input and output 1st output are in datetime format.  The second output
    is the time interval between start and stop in seconds
    Glen Langston, 2018 April 20
    """

    # expecting utc1 before utc2, check and swap if necessary
    if utc1 > utc2:
        temp = utc1
        utc1 = utc2
        utc2 = temp

    dt = utc2 - utc1
    duration = dt.total_seconds()
    dt2 = dt/2
    # compute the average time of obs
    utcout  = utc1 + dt2
    return (utcout, duration)

###
### iplatlon() is not a part of the class so that it is not required.
### These values may be manually entered into the notes file
###
def iplatlon():
    """
    iplatlon() uses the ip address to get the latitude and longitude
    The latitude and longitude are only rough, but usually 
    better han 100 km accuracy.  This is good enough for small antennas.
    """
    # default values for Green Bank, WV
    City = 'Green Bank'
    Region = 'West Virginia'
    Country = 'USA'
    lon = float( -79.8)
    lat = float( +38.4)
    try:
        import re
        import json
        from urllib2 import urlopen
    except:
        print 'Can not find Python code for:'
        print 'import re'
        print 'import json'
        print 'from urllib2 import urlopen'
        # returning Green bank
        return City, Region, Country, lat, lon

    try:
        data = str(urlopen('http://checkip.dyndns.com/').read())
    except:
        print 'Can not open internet access to get Location'
        # returning Green bank
        return City, Region, Country, lat, lon

    try:
        IP = re.compile(r'(\d+.\d+.\d+.\d+)').search(data).group(1)
    except:
        print 'Can not parse ip string'
        return City, Region, Country, lat, lon
    try:
        url = 'http://ipinfo.io/' + IP + '/json'
        response = urlopen(url)
        data = json.load(response)
    except:
        print 'Can not get ip location from internet'
        return City, Region, Country, lat, lon

    org=data['org']
    City = data['city']
    Country=data['country']
    Region=data['region']

    loc = data['loc']
    locs = loc.split(',')
    lat = float( locs[0])
    lon = float( locs[1])

    print '\nYour IP details: '
    print 'IP       : {0} '.format(IP)
    print 'Region   : {0}; Country : {1}'.format(Region, Country)
    print 'City     : {0}'.format(City)
    print 'Org      : {0}'.format(org)
    print 'Latitude : ',lat,';  Longitude: ',lon
    return City, Region, Country, lat, lon

def degree2float(instring, hint):
    """
    degree2float() takes an input angle string in "dd:MM:ss.sss" format or dd.dd
    and returns a floating point value in degrees
    """
    outfloat = 0.0
    parts = instring.split(':')
    if len(parts) == 1:  # if only one part, then degrees
        outfloat = float(instring)
    elif len(parts) == 3:  # if three parts, then dd:mm:ss
        anangle = angles.DeltaAngle(instring)
        outfloat = anangle.d
    else:
        print "%s format error: %s, zero returned " % (hint, instring)
    return outfloat

def hour2float(instring, hint):
    """
    hour2float() takes an input hours string in "hh:MM:ss.sss" format or hh.hhh
    and returns a floating point value in degrees
    """
    outfloat = 0.0
    parts = instring.split(':')
    if len(parts) == 1:  # if only one part, then degrees
        outfloat = float(instring)
    elif len(parts) == 3:  # if three parts, then dd:mm:ss
        anangle = angles.AlphaAngle(instring)
        outfloat = anangle.d
    else:
        print "%s format error: %s, zero returned " % (hint, instring)
    return outfloat

def time2float(instring, hint):
    """
    time2float() takes an input time string in "hh:MM:ss.sss" or ss.sss format
    and returns a floating point time value in seconds
    """
    outfloat = 0.0
    parts = instring.split(':')
    if len(parts) == 1:  # if only one part, then degrees
        outfloat = float(instring)
    elif len(parts) == 3:  # if three parts, then dd:mm:ss
        atime = angles.AlphaAngle(instring)
        outfloat = atime.h*3600.
    else:
        print "%s format error: %s, zero returned " % (hint, instring)
    return outfloat

class Spectrum(object):
    """
    Define a Radio Spectrum class for processing, reading and
    writing astronomical data.
    """
    def __init__(self):
        """
        initialize all spectrum class values
        many will be overwritten laters
        """
        noteA = ""
        noteB = ""
        gains = [0., 0., 0., 0., 0.] # gains are in dB
        utc = datetime.datetime.utcnow()
        telType = "Pyramid Horn"
        refChan = MAXCHAN/2
        observer = "Glen Langston"
        xdata = numpy.zeros(MAXCHAN)
        ydataA = numpy.zeros(MAXCHAN)
        ydataB = numpy.zeros(MAXCHAN)
        #now fill out the spectrum structure.
        self.writecount = 0
        self.count = int(0)          # count of spectra summed
        self.noteA = str(noteA).strip()      # observing note A
        self.noteB = str(noteB).strip()      # observing note B
        self.observer = str(observer)# name of the observer
        device = "airspy=0,pack=1,bias=1 " # AIRSPY with packed data and bias t 0n
        device = "rtl=0,bias=0 "     # rtl sdr dongle device string
        self.device = str(device)    # parameter string for SDR type
        datadir = "../data"
        self.datadir = str(datadir)  # directory for storing data
        site = "Moumau House"
        self.site = str(site)        # name of the observing site
        self.city = str("Green Bank") # observing city
        self.region = str("West Virginia") # observing region
        self.country = str("US")     # observing country
        self.gains = gains           # one or more gain parameters
        self.telaz = 0.              # telescope azimuth (degrees)
        self.telel = 0.    # telescope elevation (degrees)
        self.tellon = 0.   # geographic longitude negative = West (degrees)
        self.tellat = 0.   # geopgraphic latitude (degrees)
        self.telelev = 0.  # geographic elevation above sea-level (meteres)
        self.centerFreqHz = 1.0   # centerfrequency of the observation (Hz)
        self.bandwidthHz = 1.0   # sampleRate of the observation (Hz)
        self.deltaFreq = 1.0   # frequency interval between channels
        self.utc = utc   # average observation time (datetime class)
        self.lst = 0.    # local sideral time degrees, ie 12h = 180deg
        self.durationSec = 0.    # integrated observing time (seconds)
        self.telType = str(telType) # "Horn, Parabola  Yagi, Sphere"
        # define size of horn or antenna (for parabola usuall A = B)
        self.telSizeAm = float(1.)  # A size parameter in meters
        self.telSizeBm = float(1.)  # B size parameter in meters
        self.etaA = .8 # antenna efficiency (range 0 to 1)
        self.etaB = .99 # efficiency main beam (range 0 to 1)
        self.bunit = 'Counts'       # brightness units
        self.refChan = refChan
        self.version = str("2.0.1")
        self.polA = str("X")        # polariation of A ydata: X, Y, R, L,
        self.polB = str("Y")        # polariation of B ydata: X, Y, R, L,
        self.polAngle = float(0.0)  # orientation of polariation of A
        self.frame = str("TOPO")    # reference frame (LSR, BARY, TOPO)
# compute coordinates from az,el location and date+time all angles in degrees
        self.ra = float(0.0)        # degrees, ie 12h => 180deg
        self.dec = float(0.0)
        self.gallon = float(0.0)
        self.gallat = float(0.0)
        self.az_sun = float(0.0)
        self.altsun = float(0.0)
        self.epoch = str("2000")
        self.fft_rate = 5000
        self.nave = 20              # setup parameters for NsfIntegrate
        self.nmedian = 4096         # setup parameters for NsfIntegrate
# finally the data
        self.xdata = xdata
        self.ydataA = ydataA
        self.ydataB = ydataB
        self.nChan = len(ydataA)
        self.nSpec = 1

    def __str__(self):
        """
        Define a spectrum summary string
        """
        secs = self.durationSec
        return "({0}, {1}, {2})".format(self.site, self.utc, str(secs))

    def radec2gal(self):
        """
        Compute the ra,dec (J2000) from Az,El location and time
        """
        rads = numpy.pi / 180.
        radec2000 = ephem.Equatorial( rads*self.ra, rads*self.dec, epoch=ephem.J2000)
        # to convert to dec degrees need to replace on : with d
        self.epoch = "2000"
        gal = ephem.Galactic(radec2000)
        aparts = angles.phmsdms(str(gal.lon))
        self.gallon = angles.sexa2deci(aparts['sign'], *aparts['vals'])
        aparts = angles.phmsdms(str(gal.lat))
        self.gallat = angles.sexa2deci(aparts['sign'], *aparts['vals'])

    def azel2radec(self):
        """
        Compute the ra,dec (J2000) from Az,El location and time
        """
        location = ephem.Observer()
        location.lon = str(self.tellon)
        location.lat = str(self.tellat)
        location.elevation = self.telelev
        strnow = self.utc.isoformat()
        # convert Time string format into value for Observer
        dates = strnow.split('T')
        datestr = dates[0] + ' ' + dates[1]
        location.date = datestr
        # compute Local Sidereal Time
        lst = location.sidereal_time()
        aparts = angles.phmsdms(str(lst))
        self.lst = angles.sexa2deci(aparts['sign'], *aparts['vals'], todeg=True)
        ## Must set the date before calculating ra, dec!!!
        # compute apparent RA,DEC for date of observations
        ra_a, dec_a = location.radec_of(str(self.telaz), str(self.telel))
        fmt = 'Date   = %s,  LST = %s, %f (%f, %f)'
#        print fmt % (datestr, lst, self.lst, self.telaz, self.telel)
        radec = ephem.Equatorial(ra_a, dec_a, epoch=datestr)
#        print 'Ra,Dec %s,%s for %s' % (radec.ra, radec.dec, radec.epoch)
        radec2000 = ephem.Equatorial( radec, epoch=ephem.J2000)
#        print 'Ra,Dec %s,%s for %s' % (radec2000.ra, radec2000.dec, radec2000.epoch)
        # Hours
        aparts = angles.phmsdms(str(radec2000.ra))
        self.ra = angles.sexa2deci(aparts['sign'], *aparts['vals'], todeg=True)
        # to convert to dec degrees need to replace on : with d
        aparts = angles.phmsdms(str(radec2000.dec))
        self.dec = angles.sexa2deci(aparts['sign'], *aparts['vals'])
        self.epoch = "2000"
        # now update galactic coordinates
        self.radec2gal()
        sun = ephem.Sun(location)
        aparts = angles.phmsdms(str(sun.az))
        self.az_sun = angles.sexa2deci(aparts['sign'], *aparts['vals'])
        aparts = angles.phmsdms(str(sun.alt))
        self.altsun = angles.sexa2deci(aparts['sign'], *aparts['vals'])
#        print 'sun az,el: %s,%s -> %f,%f' % (sun.az, sun.alt, self.az_sun, self.altsun)

##################################################
#
    def write_ascii_file(self, dirname, outname):
        """
        Write ascii file containing astronomy data
        """
    # need the current time to update coordiantes
        now = self.utc
        print "File %4d: %s (%d)" % (self.writecount, outname, self.count)
        fullname = dirname + outname
        outfile = open(fullname, 'w')
        outfile.write('# File: ' + outname + '\n')
        gainstr = ''
        ngains = len(self.gains)
        for iii in range(ngains-1):
            gainstr = gainstr + str(self.gains[iii]) + '; '
        gainstr = gainstr + str(self.gains[ngains-1])
        self.noteA = self.noteA.replace('\n', '')
        self.noteA = self.noteA.strip()
        outline = '# NOTEA     = ' + self.noteA + '\n'
        outfile.write(outline)
        self.noteB = self.noteB.replace('\n', '')
        self.noteB = self.noteB.strip()
        outline = '# NOTEB     = ' + self.noteB + '\n'
        outfile.write(outline)
        self.observer = self.observer.replace('\n', '')
        self.observer = self.observer.strip()
        outline = '# OBSERVER  = ' + self.observer + '\n'
        outfile.write(outline)
        self.device = self.device.replace('\n', '')
        self.device = self.device.strip()
        outline = '# DEVICE    = ' + self.device + '\n'
        outfile.write(outline)
        self.datadir = self.datadir.replace('\n', '')
        self.datadir = self.datadir.strip()
        outline = '# DATADIR   = ' + self.datadir + '\n'
        outfile.write(outline)
        self.site = self.site.replace('\n', '')
        self.site = self.site.strip()
        outline = '# SITE      = ' + self.site + '\n'
        outfile.write(outline)
        self.city = self.city.replace('\n', '')
        self.city = self.city.strip()
        outline = '# CITY      = ' + self.city + '\n'
        outfile.write(outline)
        self.region = self.region.replace('\n', '')
        self.region = self.region.strip()
        outline = '# REGION    = ' + self.region + '\n'
        outfile.write(outline)
        self.country = self.country.replace('\n', '')
        self.country = self.country.strip()
        outline = '# COUNTRY   = ' + self.country + '\n'
        outfile.write(outline)
        self.telType = self.telType.replace('\n', '')
        self.telType = self.telType.strip()
        outline = '# TELTYPE   = ' + self.telType + '\n'
        outfile.write(outline)
        self.frame = self.frame.replace('\n', '')
        self.frame = self.frame.strip()
        outline = '# FRAME     = ' + self.frame + '\n'
        outfile.write(outline)
        outline = '# GAINS     = ' + gainstr + '\n'
        outfile.write(outline)
        ngains = len(self.gains)
        if ngains > 0:
            outline = '# GAIN1     = ' + str(self.gains[0]) + '\n'
            outfile.write(outline)
        if ngains > 1:
            outline = '# GAIN2     = ' + str(self.gains[1]) + '\n'
            outfile.write(outline)
        if ngains > 2:
            outline = '# GAIN3     = ' + str(self.gains[2]) + '\n'
            outfile.write(outline)
        if ngains > 3:
            outline = '# GAIN4     = ' + str(self.gains[3]) + '\n'
            outfile.write(outline)
        outline = '# Count     = ' + str(self.count) + '\n'
        outfile.write(outline)
        outline = '# CenterFreq= ' + str(self.centerFreqHz) + '\n'
        outfile.write(outline)
        outline = '# Bandwidth = '  + str(self.bandwidthHz) + '\n'
        outfile.write(outline)
        outline = '# Duration  = '  + str(self.durationSec) + '\n'
        outfile.write(outline)
        outline = '# DeltaX    = '  + str(self.deltaFreq) + '\n'
        outfile.write(outline)
        outline = '# BUNIT     = '  + str(self.bunit).strip() + '\n'
        outfile.write(outline)
        nChan = len(self.ydataA)
        outline = '# NCHAN     = '  + str(nChan) + '\n'
        outfile.write(outline)
        nSpec = self.nSpec
        outline = '# NSPEC     = '  + str(nSpec) + '\n'
        outfile.write(outline)
        nave  = self.nave
        outline = '# NAVE      = '  + str(nave) + '\n'
        outfile.write(outline)
        nmedian = self.nmedian
        outline = '# NMEDIAN   = '  + str(nmedian) + '\n'
        outfile.write(outline)
        outline = '# Fft_rate  = '  + str(self.fft_rate) + '\n'
        outfile.write(outline)
        strnow = now.isoformat()
        dates = strnow.split('T')
        datestr = dates[0] + ' ' + dates[1]
        outline = '# UTC       = '  + datestr + '\n'
        outfile.write(outline)
        lststr = angles.fmt_angle(self.lst/15., s1=":", s2=":", pre=3)  # convert to hours
        outline = '# LST       = '  + lststr[1:] + '\n'
        outfile.write(outline)
        outline = '# AZ        = '  + str(self.telaz) + '\n'
        outfile.write(outline)
        outline = '# EL        = '  + str(self.telel) + '\n'
        outfile.write(outline)
        anglestr = angles.fmt_angle(float(self.tellon), s1=":", s2=":")
        outline = '# TELLON    = '  + anglestr + '\n'
        outfile.write(outline)
        anglestr = angles.fmt_angle(float(self.tellat), s1=":", s2=":")
        outline = '# TELLAT    = '  + anglestr + '\n'
        outfile.write(outline)
        rastr = angles.fmt_angle(self.ra/15., s1=":", s2=":", pre=3) # convert to hours
        outline = '# RA        = '  + rastr[1:] + '\n'
        outfile.write(outline)
        decstr = angles.fmt_angle(self.dec, s1=":", s2=":")
        outline = '# DEC       = '  + decstr + '\n'
        outfile.write(outline)
        lonstr = angles.fmt_angle(self.gallon, s1=":", s2=":", pre=2)
        outline = '# GALLON    = '  + lonstr[1:] + '\n'
        outfile.write(outline)
        latstr = angles.fmt_angle(self.gallat, s1=":", s2=":", pre=2)
        outline = '# GALLAT    = '  + latstr + '\n'
        outfile.write(outline)
        altstr = angles.fmt_angle(self.altsun, s1=":", s2=":", pre=1)
        outline = '# ALT_SUN   = '  + altstr + '\n'
        outfile.write(outline)
        az_str = angles.fmt_angle(self.az_sun, s1=":", s2=":", pre=1)
        outline = '# AZ_SUN    = '  + az_str + '\n'
        outfile.write(outline)
        outline = '# ETAA      = '  + str(self.etaA) + '\n'
        outfile.write(outline)
        outline = '# ETAB      = '  + str(self.etaB) + '\n'
        outfile.write(outline)
        outline = '# POLANGLE  = '  + str(self.polAngle) + '\n'
        outfile.write(outline)
        outline = '# TELSIZEAM = '  + str(self.telSizeAm) + '\n'
        outfile.write(outline)
        outline = '# TELSIZEBM = '  + str(self.telSizeBm) + '\n'
        outfile.write(outline)
        outline = '# AST_VERS  = '  + str("04.02") + '\n'
        outfile.write(outline)

        dx = self.bandwidthHz/float(self.nChan)
        x = self.centerFreqHz - (self.bandwidthHz/2.) + (dx/2.)
        yv = self.ydataA
        leny = len(yv)
        for i in range(min(self.nChan,leny)):
            outline = str(i).zfill(4) + ' ' + str(long(x)) + ' ' + str(yv[i]) + '\n'
            outfile.write(outline)
            x = x + dx
        del outline
        outfile.close()

    def write_ascii_ast(self, dirname):
        """
        Write ascii file containing astronomy data
        File name is based on time of observation
        """
        now = self.utc
        strnow = now.isoformat()
        datestr = strnow.split('.')
        daypart = datestr[0]
        yymmdd = daypart[2:19]
        # distinguish hot load and regular observations
        if self.telel > 0:
            outname = yymmdd + '.ast'
        else:
            outname = yymmdd + '.hot'
        outname = outname.replace(":", "")
        self.write_ascii_file(dirname, outname)

    def read_spec_ast(self, fullname):
        """
        Read an ascii radio Spectrum file and return a radioSpectrum object
        """
        # turn on/off printing
        verbose = True
        verbose = False
        # Read the file.
        f2 = open(fullname, 'r')
# read the whole file into a single variable, which is a list of every row of the file.
        lines = f2.readlines()
        f2.close()

# initialize some variable to be lists:
        x1 = []
        y1 = []
        y2 = []
        datacount = 0
        linecount = 0

# scan the rows of the file stored in lines, and put the values into some variables:
        for line in lines:
            parts = line.split()
            if linecount == 0:
                parts[1] = parts[1].upper()
                if parts[1] != 'FILE:':
                    print ""
                    print "read_spec_ascii input error!"
                    print ""
                    print "Input not an NSF Spectrum file:", fullname
                    exit()
            linecount = linecount + 1
# if a very short or blank line
            if len(line) < 3:
                continue
            if linecount == 2:
                self.noteA = line[2:].replace('\n', '')
# if a comment or parameter line, decode value
            if line[0] == '#':
# parse keywords as upper case: ie Ra == RA
                parts[1] = parts[1].upper()
                if parts[1] == 'UTC':
                    timefmt = "%Y-%m-%d %H:%M:%S.%f"
                    utc = datetime.datetime.strptime(parts[3] + " " + parts[4], timefmt)
                    self.utc = utc
                if parts[1] == 'CENTERFREQ':
                    self.centerFreqHz = float(parts[3])
                if parts[1] == 'CENTERFREQ=':
                    self.centerFreqHz = float(parts[2])
                if parts[1] == 'BANDWIDTH':
                    self.bandwidthHz = float(parts[3])
                if parts[1] == 'DURATION':
                    self.durationSec = float(parts[3])
                if parts[1] == 'DELTAX':
                    self.deltaFreq = float(parts[3])
                if parts[1] == 'LST':
                    lstparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(lstparts['sign'], *lstparts['vals'])
                    self.lst = x*15. # convert back to degrees
                    if verbose: 
                        print parts[3], x
                if parts[1] == 'AZ':
                    self.telaz = degree2float(parts[3], parts[1])
                if parts[1] == 'EL':
                    self.telel = degree2float(parts[3], parts[1])
                if parts[1] == 'COUNT':
                    self.count = int(parts[3])
                if parts[1] == 'NCHAN':
                    self.nChan = int(parts[3])
                if parts[1] == 'BUNIT':
                    otherparts = line.split('=')
                    self.bunit = str( otherparts[1]).strip()
                    if verbose:
                        print 'Bunit    ', self.bunit
                if parts[1] == 'NSPEC':
                    self.nSpec = int(parts[3])
                if parts[1] == 'NAVE':
                    self.nave  = int(parts[3])
                if parts[1] == 'NMEDIAN':
                    self.nmedian = int(parts[3])
                if parts[1] == 'REFCHAN':
                    self.refChan = float(parts[3])
                if parts[1] == 'FFT_RATE':
                    self.fft_rate = int(parts[3])
                    if self.fft_rate < 1:
                        self.fft_rate = 1
                if parts[1] == 'ETAA':
                    self.etaA = float(parts[3])
                if parts[1] == 'ETAB':
                    self.etaB = float(parts[3])
                if parts[1] == 'POLANGLE':
                    self.polAngle = float(parts[3])
                if parts[1] == 'LNA' or parts[1] == 'GAINS':  # get one or more gains separated by ';'
                    gains = []
                    for jjj in range(3, len(parts)):
                        gainstr = parts[jjj].replace(';', ' ')
                        gainstr = gainstr.replace(',', ' ')
                        moreparts = gainstr.split()
                        for kkk in range(len(moreparts)):
                            gains.append(float(moreparts[kkk]))
                    if verbose:
                        print 'read: parts: ', parts
                        print 'read: gains: ', gains
                    self.gains = numpy.array(gains)
                if parts[1] == 'LNA=' or parts[1] == 'GAINS=':  # get one or more gains separated by ';'
                    gains = []
                    for jjj in range(2, len(parts)):
                        gainstr = parts[jjj].replace(';', ' ')
                        gainstr = gainstr.replace(',', ' ')
                        moreparts = gainstr.split()
                        for kkk in range(len(moreparts)):
                            gains.append(float(moreparts[kkk]))
                    self.gains = numpy.array(gains)
                apart = parts[1]
                if apart[0:3] == 'GAIN':
                    i = int( apart[4])
                    if i > 0 and i < 6:
                        n = len( parts)
                        self.gains[i-1] = float( parts[n-1])
                    else:
                        if apart[4] != 'S':
                           print "Error parsing GAINn: ", line 
                if parts[1] == 'OBSERVER':
                    otherparts = line.split('=')
                    self.observer = str( otherparts[1]).strip()
                    if verbose:
                        print 'Observer: ', self.observer
                if parts[1] == 'DEVICE':
                    otherparts = line.split('=', 1)
                    if len(otherparts) > 1:
                        self.device = str( otherparts[1]).strip()
                    else:
                        print 'Error parsing device : ', line
                    if verbose:
                        print 'Device  : ', self.device
                if parts[1] == 'DATADIR':
                    otherparts = line.split('=', 1)
                    if len(otherparts) > 1:
                        self.datadir = str( otherparts[1]).strip()
                    else:
                        print 'Error parsing datadir : ', line
                    if verbose:
                        print 'DataDir : ', self.datadir
                if parts[1] == 'SITE':
                    otherparts = line.split('=')
                    self.site = str( otherparts[1]).strip()
                    if verbose:
                        print 'Site    : ', self.site
                if parts[1] == 'CITY':
                    otherparts = line.split('=')
                    self.city = str( otherparts[1]).strip()
                    if verbose:
                        print 'City    : ', self.city
                if parts[1] == 'REGION':
                    otherparts = line.split('=')
                    self.region = str( otherparts[1]).strip()
                    if verbose:
                        print 'Region  : ', self.region
                if parts[1] == 'COUNTRY':
                    otherparts = line.split('=')
                    self.country = str( otherparts[1]).strip()
                    if verbose:
                        print 'Country : ', self.country
                if parts[1] == 'NOTEA':
                    otherparts = line.split('=')
                    self.noteA = str( otherparts[1]).strip()
                    if verbose:
                        print 'Note A  : ', self.noteA
                if parts[1] == 'NOTEB':
                    otherparts = line.split('=')
                    self.noteB = str( otherparts[1]).strip()
                    if verbose:
                        print 'Note B  : ', self.noteB
                if parts[1] == 'AST_VERS':
                    otherparts = line.split('=')
                    if verbose:
                        self.version = str( otherparts[1]).strip()
                if parts[1] == 'FRAME':
                    otherparts = line.split('=')
                    self.frame = str( otherparts[1]).strip()
                    if verbose:
                        print 'FRAME  : ', self.frame
                if parts[1] == 'TELTYPE':
                    otherparts = line.split('=')
                    self.telType = str( otherparts[1]).strip()
                    if verbose:
                        print 'Tel Type: ', self.telType
                if parts[1] == 'LON' or parts[1] == 'GALLON':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.gallon = x
                if parts[1] == 'LAT' or parts[1] == 'GALLAT':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.gallat = x
# if parse telescope geographic latitude and longitude into float
                if parts[1] == 'TELLON':
                    self.tellon = degree2float(parts[3], parts[1])
                if parts[1] == 'TELLAT':
                    self.tellat = degree2float(parts[3], parts[1])
# parse ra, dec into float
                if parts[1] == 'RA':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.ra = x * 15. # convert back to degrees
                    if verbose:
                        print 'RA', parts[3], aparts, x
                if parts[1] == 'DEC':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.dec = x
# if sun coordinates into a float
                if parts[1] == 'ALT_SUN':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.altsun = x
                if parts[1] == 'AZ_SUN':
                    aparts = angles.phmsdms(parts[3])
                    x = angles.sexa2deci(aparts['sign'], *aparts['vals'])
                    self.az_sun = x
# this is the end of the if first character is a # IF statement
                continue
# sometimes there are user comments in the top few lines; ignore
            if linecount < 5:
                continue
# start data processing
            datacount = datacount+1
            p = line.split()
            np = len(p)
            if (np < 3):
                continue
            try:
                x1.append(float(p[1]))
            except:
                x1.append( 0.0)
            try:
                y1.append(float(p[2]))
            except:
                y1.append( 0.0)
            if self.nSpec > 1:
                try:
                    y2.append(float(p[3]))
                except:
                    y2.append( 0.0)

# at this point all data and header keywords are read
        self.xdata = numpy.array(x1)  # transfer
        self.ydataA = numpy.array(y1) # always transfer 1 spectrum
        if self.nSpec > 1:            # if more than one spectrum
            self.ydataB = numpy.array(y2)   # transfer it too
            
        ndata = len(self.xdata)
        if self.nChan != ndata:
            print "File header Miss-match and number of channels in data"
            print ": %f != %f" % (self.nChan, ndata)
            self.nChan = int(ndata)
        return

    def foldfrequency( self):
        """
        foldfrequency flips and averages the folded xaxis
        """
        yfold = self.ydataA[::-1]
#        print len(yfold)
        yfold = self.ydataA + yfold
#        yfold = yfold * 0.5
        yfold = yfold
        return yfold

def lines( linelist, lineWidth, x, y):
    """
    lines takes a list of lines to interpoate, interpolates over the RFI
    linelistHz list of line frequencies
    lineWidth = width of lines to interpolate (channels)
    x = frequencies in the same units as linelist
    y = intensities
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

# HISTORY
# 18Apr12 GIL move the line interpolation function into radioastronomy
# 18Feb12 GIL restore fold function for ubuntu WX generated data
# 16AUG17 GIL separate out modules and ephemeris
# 15JUN04 GIL recording working, but having trouble with display
# 15JUN02 GIL return coordinates so that the data can be understood
# 15MAY29 GIL get averaging functioning and also periodic updates
# 15MAY16 GIL start creating averages
# 15MAY15 GIL try to reduce the cpu load
# 15MAY05 GIL have recording working now.  still too much CPU usage.
# 15MAY04 GIL found that the program was taking too much CPU
#             performance was fine once sleep of 10ms was added
# 15MAY01 GIL Initial version


# File: 18-02-10T201333.ast
# NOTEA     = ubuntu linux new bubble horn with lid
# NOTEB     = 
# OBSERVER  = Glen Langston
# SITE      = Moumau House
# CITY      = Green Bank
# REGION    = West Virginia
# COUNTRY   = US
# TELTYPE   = Pyramid Horn
# FRAME     = TOPO
# GAINS     = 14.0; 11.0; 11.0
# GAIN1     = 14.0
# GAIN2     = 11.0
# GAIN3     = 11.0
# Count     = 32027
# CenterFreq= 1419000000.0
# Bandwidth = 6000000.0
# Duration  = 37.422869
# DeltaX    = 5859.375
# NCHAN     = 1024
# NSPEC     = 1
# Fft_rate  = 5000
# UTC       = 2018-02-10 20:13:33.334787
# LST       = 00:17:36.520
# AZ        = 180.0
# EL        = 70.0
# TELLON    = -79:50:22.920
# TELLAT    = +38:25:59.160
# RA        = 00:15:45.450
# DEC       = +18:13:40.700
# GALLON    = 111:09:09.80
# GALLAT    = -43:49:34.30
# ALT_SUN   = +25:29:02.8
# AZ_SUN    = +223:38:57.2
# ETAA      = 0.8
# ETAB      = 0.99
# POLANGLE  = 0.0
# TELSIZEAM = 1.0
# TELSIZEBM = 1.0
# AST_VERS  = 03.01
###0000 1416002929 3.47444e-09
###0001 1416008789 1.66126e-09
###0002 1416014648 3.1796e-10
