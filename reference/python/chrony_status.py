#Python Script get last chrony demon tracking log
#HISTORY
#20FEB20 GIL Initial version
#
import subprocess
import sys
import os

def getchrony():
    """
    Read the Chrony log file and read latest value
    """
    
    filename = "/var/log/chrony/tracking.log"
    fileNotOK = True
    try:
        if os.path.isfile(filename):
            fileNotOK = False
    except:
        fileNotOK = True
    # if file is not OK, return default
    if fileNotOK:
        return( "2020-02-20T02:02:02.000", 0., 0.)
    
    #get the very last line in the filea
    line = subprocess.check_output(['tail', '-1', filename])
    parts = line.split()
    nparts = len(parts)

    if nparts < 10:
        return( "", 0., 0.)
       
    date = parts[0]
    time = parts[1]
    ip = parts[2]
    #print("Offset: %s" % (parts[9]))
    offset = float(parts[6])
    offsetrms = float(parts[9])
    datestr = "%sT%s" % (date, time)
    return( datestr, offset, offsetrms)

    
if __name__=='__main__':
    """
    Execute getchrony and print values()
    """
    doHelp = False
    doThree = False
    filename = "/var/log/chrony/tracking.log"

    nargs = len(sys.argv)
    if nargs == 2:
        doHelp = ( sys.argv[1].upper() == "-H")
        doThree = ( sys.argv[1].upper() == "3")
    if nargs > 2:
        doHelp = ( sys.argv[1].upper() == "-H" or sys.argv[2].upper() == "-H")
        doThree = ( sys.argv[1].upper() == "3" or sys.argv[2].upper() == "3")
    
    if doHelp:
        print("Get Latest Chrony deamon log values")
        print("Usage: python getchrony.py [-H] [3]")
        print("Where -H  Optionally print help info")
        print("Where 3   Return parsed log value in 3 parts:")
        print("")
        print("   The Offset (seconds) should be added to System time to get the UTC time of events")
        print("")
        with open(filename) as f:
            first_line = f.readline()
            second_line = f.readline()
            third_line = f.readline()
        sys.stdout.write("%s" % (first_line))
        sys.stdout.flush()
        sys.stdout.write("%s" % (second_line))
        sys.stdout.flush()
        sys.stdout.write("%s" % (third_line))
        sys.stdout.flush()
    
    line = subprocess.check_output(['tail', '-1', filename])

    if doHelp:
        sys.stdout.write("%s" % (line))
        sys.stdout.flush()
        
    datestr, offset, offsetrms = getchrony()
    print( "%s %9.6f %8.6f" % (datestr, offset, offsetrms))
    exit()
