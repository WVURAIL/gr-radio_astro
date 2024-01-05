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
** 24Jan03 GIL Initial version to select a range of channels to shorten a vector
** 
*/

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <stdio.h>
#include <time.h> 
#include "vselect_impl.h"
#include <iostream>
#include <chrono>

namespace gr {
  namespace radio_astro {

    vselect::sptr
    vselect::make(int vec_length, int vec_begin, int vec_out_len)
    {
      return gnuradio::make_block_sptr<vselect_impl>(
	   vec_length, vec_begin, vec_out_len);
    }

    /*
     * The private constructor
     */
    vselect_impl::vselect_impl(int vec_length, int vec_begin, int vec_out_len)
      : gr::block("vselect",
		  gr::io_signature::make(1, 1, sizeof(float)*vec_length),
		  gr::io_signature::make(1, 1, sizeof(float)*vec_out_len)),
        d_vec_length(vec_length),
	d_vec_begin(vec_begin), 
        d_vec_out_len(vec_out_len)
    { set_vlen( vec_length);  /* initialize all imput values */
      set_vec_begin( vec_begin);
      set_vec_out_len( vec_out_len);
    }

    /*
     * Our virtual destructor.
     */
    vselect_impl::~vselect_impl()
    {
    }

    void
    vselect_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      /* for each output vector, d_n input vectors are needed */
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = noutput_items;
    }

    void 
    vselect_impl::set_vec_begin ( int invec_begin)
    /* set begin index to selected output array */
    { char * errmsg = NULL;
      vec_begin = invec_begin;
      
      if (vec_begin < 0) {
	fprintf( stderr, "Vector index starts at 0; == %d \n", vec_begin);
       vec_begin = 0;
      }

      fprintf(stderr, "Selecting %d channels starting at %d\n", vec_out_len,
	      vec_begin);
      d_vec_begin = vec_begin;
    } // end of set_vec_begin()
      
    void 
    vselect_impl::set_vec_out_len ( int invec_out_len)
    /* set begin index to selected output array */
    { char * errmsg = NULL;
      vec_out_len = invec_out_len;
      
      if (vec_out_len < 1) {
	fprintf( stderr, "Vector output must be > 0; == %d \n", invec_out_len);
       invec_out_len = 1;
      }

      if (vec_out_len + d_vec_begin > vlen) {
         fprintf(stderr, "Selected %d channel end beyond %d\n",
	      vec_out_len + d_vec_begin,
	      vlen);
	 vec_out_len = vlen - d_vec_begin;
      }
      d_vec_out_len = vec_out_len;
      vec_out_len = vec_out_len;
    } // end of set_vec_out_len()
      
    void
    vselect_impl::set_vlen ( int invlen)
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
    vselect_impl::general_work (int noutput_items,
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
	  success = vselect( onein, oneout);
	  // every n vectors, one more output is written 
	  nout += success;
	}
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (ninputs);

      // Tell runtime system how many output items we produced.
      return nout;
    } // end of vselect_impl:: general_work
    

    int
    vselect_impl::vselect(const float *input, float *output)
    { /* Inputs are an input vector and an output vector of values
	 nout is either 0 or 1, depending on whether the count is complete
       */
      int ii = 0, jj = 0;

      for (jj = vec_begin; jj < vec_out_len; jj++) {
	 output[ii] = input[jj];
	 ii ++;
      }
      return 1;
    } // end of vselect_impl::vselect()

  } /* namespace radio_astro */
} /* namespace gr */

