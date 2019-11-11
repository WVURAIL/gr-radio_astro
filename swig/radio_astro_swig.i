/* -*- c++ -*- */

#define RADIO_ASTRO_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "radio_astro_swig_doc.i"

%{
#include "radio_astro/dedispersion.h"
#include "radio_astro/detect.h"
#include "radio_astro/vmedian.h"
%}


%include "radio_astro/dedispersion.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, dedispersion);
%include "radio_astro/detect.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, detect);
%include "radio_astro/vmedian.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, vmedian);
