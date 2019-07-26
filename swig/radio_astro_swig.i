/* -*- c++ -*- */

#define RADIO_ASTRO_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "radio_astro_swig_doc.i"

%{
#include "radio_astro/dedispersion_old.h"
#include "radio_astro/detect.h"
#include "radio_astro/dedispersed.h"
%}


%include "radio_astro/dedispersion_old.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, dedispersion_old);
%include "radio_astro/detect.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, detect);

%include "radio_astro/dedispersed.h"
GR_SWIG_BLOCK_MAGIC2(radio_astro, dedispersed);
