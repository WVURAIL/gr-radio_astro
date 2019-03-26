#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/Users/glangsto/Research/gr-radio_astro/lib
export PATH=/Users/glangsto/Research/gr-radio_astro/build/lib:$PATH
export DYLD_LIBRARY_PATH=/Users/glangsto/Research/gr-radio_astro/build/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-radio_astro 
