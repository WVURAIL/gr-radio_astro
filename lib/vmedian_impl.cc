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
#include "vmedian_impl.h"
#include <iostream>
#include <chrono>

namespace gr {
  namespace radio_astro {

    vmedian::sptr
    vmedian::make(int vec_length, int n)
    {
      return gnuradio::get_initial_sptr
        (new vmedian_impl(vec_length, n));
    }

    /*
     * The private constructor
     */
    vmedian_impl::vmedian_impl(int vec_length, int n)
      : gr::block("vmedian",
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length),
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length)),
        d_vec_length(vec_length),
        d_n(n)
    { set_vlen( vec_length);  /* initialize all imput values */
      set_mode( n);
    }

    /*
     * Our virtual destructor.
     */
    vmedian_impl::~vmedian_impl()
    {
    }

    void
    vmedian_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      /* for each output vector, d_n input vectors are needed */
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = d_n*noutput_items;
    }

    void 
    vmedian_impl::set_mode ( int n)
    {
      printf("Medianing %d vectors", n);
      d_n = n;
      d_n1 = d_n - 1;
      d_n2 = d_n - 2;
      oneovern2 = 1./float(d_n2);  // Normally median 4 values, so exclude min,max (2)
    } // end of set_mode()
      
    void 
    vmedian_impl::set_vlen ( int invlen)
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
    vmedian_impl::general_work (int noutput_items,
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
	  success = vmedian( onein, oneout);
	  // every n vectors, one more output is written 
	  nout += success;
	}
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (ninputs);

      // Tell runtime system how many output items we produced.
      return nout;
    } // end of vmedian_impl:: general_work
    

    int
    vmedian_impl::vmedian(const float *input, float *output)
    {
      int nout = 0;

      if ( count == 0) 
	{ for(unsigned int j=0; j < vlen; j++)
	    { vsum[j] = vmin[j] = vmax[j] = input[j];
	    }	  
	  count = 1;
	}
      else if (count < d_n1) 
	{ 
	  for(unsigned int j=0; j < vlen; j++)
	    { vsum[j] += input[j];
	      if (input[j] > vmax[j])
		vmax[j] = input[j];
	      else if (input[j] < vmin[j])
		vmin[j] = input[j];
	    }
	  count += 1;
	}
      else {  /* if here, count is full, time to complete the median */
	  for(unsigned int j=0; j < vlen; j++)
	    { if (input[j] > vmax[j])
		output[j] = vsum[j] - vmin[j];
	      else if (input[j] < vmin[j])
		output[j] = vsum[j] - vmax[j];
	      else { /* else neither min nor max, must add to sum */
		vsum[j] += input[j];
		output[j] = vsum[j] - (vmax[j] + vmin[j]);
	      } /* end else neither min nor max */
	    } /* end for all channels */
	  // finally scale by number of vectors averaged
	  for(unsigned int j=0; j < vlen; j++)
	     output[j] *= oneovern2;
	  nout = 1;
	  count = 0;
      } /* end else final count */

      return nout;
    } // end of vmedian_impl::vmedian()

  } /* namespace radio_astro */
} /* namespace gr */

