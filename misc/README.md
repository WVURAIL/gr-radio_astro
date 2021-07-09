# gr-radio_astro/misc

##  This sub-directory contains files associated with synchronizing multiple radio telescopes

These files contain configurations to be copied to a Raspberry pi /etc directory

In order to provide precise time to Raspberry PIs the dault configuration
is for all the Pis to share a common timing host.   In this case the host IP is
`192.168.1.200`
which has a GPS based clock.  The time is shared through auto startup of gpsd.

The host also should be running "chrony"

## The PIs need to be running Precision Time Protocol, implemented in daemon ptp4l.

The Pi kernel must be modified to emulate hardware time transfers.   This
process has been tested with Pi Kernel 5.3.y
<p>

Glen Langston --- National Science Foundation, June 22, 2020

