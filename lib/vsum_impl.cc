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

/* HISTORY
** 21Dec04 GIL Limit decimate to Gnuradio max vector queue
*/

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <stdio.h>
#include <time.h> 
#include "vsum_impl.h"
#include <iostream>
#include <chrono>

namespace gr {
  namespace radio_astro {

    vsum::sptr
    vsum::make(int vec_length, int c_begin, int c_end)
    {
      return gnuradio::make_block_sptr<vsum_impl>(
						  vec_length, c_begin, c_end);
    }

    /*
     * The private constructor
     */
    vsum_impl::vsum_impl(int vec_length, int c_begin, int c_end)
      : gr::block("vsum",
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length),
		  gr::io_signature::make(1, 1, sizeof(float))),
        d_vec_length(vec_length),
        d_c_begin( c_begin),
	d_c_end( c_end)
    { set_vlen( vec_length);  /* initialize all imput values */
      set_c_begin( c_begin);
      set_c_end( c_end);
    }

    /*
     * Our virtual destructor.
     */
    vsum_impl::~vsum_impl()
    {
    }

    void
    vsum_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      /* for each output vector, d_n input vectors are needed */
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = noutput_items;
    }

    void vsum_impl::checkn()
    { int n = c_end - c_begin, temp = 0;

      if (c_end < c_begin) {
	temp = c_begin;
	c_begin = c_end;
	c_end = c_begin;
      }

      if (c_begin == c_end) {
	if (c_end < vlen) {
	  c_end = c_end + 1;
	}
      }
      n = c_end - c_begin;
      oneovern = 1.;
      if (n > 1.) {
	oneovern = 1./float(n);  // use to multiply for average
      }
    } // end of set_checkn()

  void 
    vsum_impl::set_c_begin ( int c_begin)
    { char * errmsg = NULL;
      
      if (c_begin < 0) {
	fprintf( stderr, "Begin channel must be >= 0\n");
        c_begin = 0;
      }
      else if (c_begin > vlen) {
	fprintf( stderr, "Begin channel must be < end channel\n");
	c_begin = vlen;
      }
      checkn();
      
    } // end of set_c_begin()

   void 
    vsum_impl::set_c_end ( int c_end)
    { char * errmsg = NULL;
      
      if (c_end < 0) {
	fprintf( stderr, "Begin channel must be >= 0\n");
        c_end = 0;
      }
      else if (c_end > vlen) {
	fprintf( stderr, "Begin channel must be < end channel\n");
	c_end = vlen;
      }
      checkn();
      
    } // end of set_c_end()
      
    void 
    vsum_impl::set_vlen ( int invlen)
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
    vsum_impl::general_work (int noutput_items,
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
	  success = vsum( onein, oneout);
	  // every n vectors, one more output is written 
	  nout += success;
	}
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (ninputs);

      // Tell runtime system how many output items we produced.
      return nout;
    } // end of vsum_impl:: general_work
    

    int
    vsum_impl::vsum(const float *input, float *output)
    { /* Inputs are an input vector and an output vector of values
	 nout is either 0 or 1, depending on whether the count is complete
       */
      int nout = 1, ii = 0;
      float sum = 0.;

      for (ii = c_begin; ii < c_end; ii++) {
	sum += input[ii];
      }
      sum = sum * oneovern;
      output[0] = sum;

      return nout;
    } // end of vsum_impl::vsum()

  } /* namespace radio_astro */
} /* namespace gr */

