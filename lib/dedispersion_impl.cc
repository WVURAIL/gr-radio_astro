/* -*- c++ -*- */
/* 
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
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
#include "dedispersion_impl.h"
#include <iostream>

namespace gr {
  namespace radio_astro {

    dedispersion::sptr
    dedispersion::make(int vec_length, float dms, float f_obs, float bw, float t_int, int nt)
    {
      return gnuradio::get_initial_sptr
        (new dedispersion_impl(vec_length, dms, f_obs, bw, t_int, nt));
    }

    /*
     * The private constructor
     */
    dedispersion_impl::dedispersion_impl(int vec_length, float dms, float f_obs, float bw, float t_int, int nt)
      : gr::block("dedispersion",
              gr::io_signature::make(1, 1, sizeof(float)*vec_length*nt),
              gr::io_signature::make(1, 1, sizeof(float)*nt)),
        d_vec_length(vec_length),
        d_dms(dms),
        d_f_obs(f_obs),
        d_bw(bw),
        d_t_int(t_int),
        d_nt(nt)
    {}

    /*
     * Our virtual destructor.
     */
    dedispersion_impl::~dedispersion_impl()
    {
    }

    void
    dedispersion_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = noutput_items;
    }

    int
    dedispersion_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];
      int success;
      success = dedisperse(in, out);
      std::cout << success;
      //std::cout << out[0*d_dms+ 0] << " " << out[31*d_dms+49] <<"\n";

      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }
    
    int
    dedispersion_impl::dedisperse(const float *input, float *output)
    {
      //outbuf = (float *) //create fresh one if necessary
      float dmk = 4148808/d_t_int;
      int shift;
      unsigned int y;
      float f_low = d_f_obs - d_bw/2;
      float inv_f_low_sq = 1/(f_low*f_low);
      //std::cout << input[10*d_vec_length + 20] << " " << input[31*d_vec_length + 0] <<"\n";
      //for(unsigned int i=0; i < d_dms; i++){
          //need to zero outbuf
          for (unsigned int k=0; k < d_nt; k++){
            output[k] = 0;
          }
          for(unsigned int j=0; j < d_vec_length; j++){
            shift = round( dmk * d_dms * (inv_f_low_sq - 1/((d_bw*j/d_vec_length + f_low)*(d_bw*j/d_vec_length + f_low) )));
            for(unsigned int k=0; k < d_nt; k++){
              y = (k-shift) % d_nt;
              output[k] += input[y*d_vec_length+j];
            }
          }
      //}
      return 0;
    }

  } /* namespace radio_astro */
} /* namespace gr */

