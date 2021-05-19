/* -*- c++ -*- */
/* 
 * Copyright 2019 - Quiet Skies LLC -- Glen Langston - glen.i.langston@gmail.com
 * 
 * This is free software;  you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <stdio.h>
#include <time.h> 
#include "vmedian3_impl.h"
#include <iostream>
#include <chrono>

namespace gr {
  namespace radio_astro {

    vmedian3::sptr
    vmedian3::make(int vec_length)
    {
      return gnuradio::get_initial_sptr
        (new vmedian3_impl(vec_length));
    }

    /*
     * The private constructor
     */
    vmedian3_impl::vmedian3_impl(int vec_length)
      : gr::block("vmedian3",
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length),
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length)),
        d_vec_length(vec_length)
    { set_vlen( vec_length);  /* initialize all imput values */
    }

    /*
     * Our virtual destructor.
     */
    vmedian3_impl::~vmedian3_impl()
    {
    }

    void
    vmedian3_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      /* for each output vector, d_n input vectors are needed */
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = d_n*noutput_items;
    }


    void 
    vmedian3_impl::set_vlen ( int invlen)
    { vlen = invlen;
      if (vlen < 32) 
	{ vlen = 32;
	  printf("Vector Length too short, using %5d\n", vlen);
	}
      else if (vlen > MAX_VLEN) 
	{ vlen = MAX_VLEN;
	  printf("Vector Length too large, using %5d\n", vlen);
	}
      d_vec_length = vlen;
    } // end of set_vlen()
      
    int
    vmedian3_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0], * onein;
      float *out = (float *) output_items[0], * oneout;
      unsigned ninputs = ninput_items.size();
      int success, nout = 0;

      // for all input vectors
      for (unsigned j = 0; j < ninputs; j++) 
	{ // process one vector at a time
	  onein = &in[j];
	  // write 0 or 1 output vectors
	  oneout = &out[nout];
	  success = vmedian3( onein, oneout);
	  // every n vectors, one more output is written 
	  nout += success;
	}
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (ninputs);

      // Tell runtime system how many output items we produced.
      return nout;
    } // end of vmedian3_impl:: general_work
    

    int
    vmedian3_impl::vmedian3(const float *input, float *output)
    {
      int nout = 0;

      if ( count == 0) 
	{ for(unsigned int j=0; j < vlen; j++)
	    { vsum[j] = vmin[j] = vmax[j] = input[j];
	    }	  
	  count = 1;
	}
      else if (count == 1) 
	{ 
	  for(unsigned int j=0; j < vlen; j++)
	    { if (input[j] > vmax[j])
		{
		vsum[j] = vmax[j];
		vmax[j] = input[j];
		}
	      else if (input[j] < vmin[j])
		{
		vsum[j] = vmin[j];
		vmin[j] = input[j];
		}
	      else
		vsum[j] = input[j];  /* else must be in the middle */
	    }
	  count += 1;
	}
      else {  /* if here, count is full, time to complete the median */
	  for(unsigned int j=0; j < vlen; j++)
	    { if (input[j] > vmax[j])   /* if last greater than max */
		output[j] = vmax[j];    /* middle is now former max */
	      else if (input[j] < vmin[j]) /* if smaller than min */
		output[j] = vmin[j];    /* middle is now former min */
	      else { /* else neither min nor max, must be the middle */
		output[j] = input[j];
	      } /* end else neither min nor max */
	    } /* end for all channels */
	  // finally scale by number of vectors averaged
	  nout = nout + 1;
	  count = 0;
      } /* end else final count */

      return nout;
    } // end of vmedian3_impl::vmedian3()

  } /* namespace radio_astro */
} /* namespace gr */

