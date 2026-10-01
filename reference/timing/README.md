# Telescope timing configuration references

These configurations and the setup notes below are retained from the 2020 radio-telescope timing experiment. They originally lived in `gr-radio_astro/misc` and now live in `reference/timing/`. The kernel version, host address, and hardware assumptions describe that historical setup.

## Original setup notes

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

