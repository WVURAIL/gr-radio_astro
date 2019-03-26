#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/Users/glangsto/Research/gr-radio_astro/python
export PATH=/Users/glangsto/Research/gr-radio_astro/build/python:$PATH
export DYLD_LIBRARY_PATH=/Users/glangsto/Research/gr-radio_astro/build/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=/Users/glangsto/Research/gr-radio_astro/build/swig:$PYTHONPATH
/Users/glangsto/anaconda2/bin/python2 /Users/glangsto/Research/gr-radio_astro/python/qa_dedispersion.py 
