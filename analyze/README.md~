# hello-world
This project contains plotting tools reviewing spectra data from Science Aficionado Telescopes.
The plotting programs expect Ascii input spectra with extensive headers describing the observations.

The plotting programs are compatible with the NsfIntegrate??.grc output spectra.
These python programs were created using the Gnu Radio Companion (GRC).   These programs
contained here are for analysis after the observations, not for data taking.

These programs are also compatible with the older NsfWatch output (watch.py)

Files:
======

S     Function to call s.py, which summarizes a set of observations in a directory

s.py  Python function to read all selected spectra in a directory and summarize the observations

R     Function to call r.py, which plots raw spectra

r.py  Python function to read the spectra and plot them

T     Function to call t.py, which plots T-sys Calibrated ppectra

t.py  Python function to read the spectra, calibate and plot them

M     Function to call m.py, which plots T-sys Calibrated spectra, with a median baseline subtracted

m.py  Python function to read the spectra, calibate, baseline subtract and plot them

*.ast Astronomical data

*.hot Hot load data for calibration.

data-17nov03    Selection of data for testing plotting functions.  Older format spectra

data-18apr13    Selection of data for testing plotting functions.  Newer format spectra

Support functions
=================

The programs depend on two helper functions:
    
radioastronomy.py   Python to read and write spectra.  This function is shared with the data collecting software.

interpolate.py      Pyhton to interpolate over expected Interfering radio lines.  Needed to for more acurate calibration.

Examples
========

These functions must be executed in the current directry or the python programs copied to the appropriate place in your path.   

To plot all the raw data in a directory type:

R data-17nov03/*

only a maximum of 25 spectra will be plotted. To plot all the hot load data

R data-18apr13/*.hot

To compare selected hot load data and one spectrum 5 minutes after each hour type:

R data-17nov03/*.hot data-17nov03/*T???05*

To plot calibrated data, the set of spectra must include some hot-load observations.  These observations
are taken while pointing the telescope at the ground, to set the gain, assuming a ground temperature of 285 Kelvin.

The calibration scripts take an averaging time argument (in seconds).  To plot all the spectra calibrated with 15 minute averaging time type:

T 900. data-17nov03/*

The scripts monitor the telescope azimuth and elevation and stop averaging each time the angles or
frequencies of observations change.   

To subtract a median baseline type:

M 900.  data-18apr13/*


HISTORY
18MAY04 GIL Minor corrections and place in Github
18APR30 GIL T and M plotting functions
18APR20 GIL Initial version including only the raw spectra plotting

Glen Langston, National Science Foundation (GIL)
Kevin Bandura, University of West Virginia 

