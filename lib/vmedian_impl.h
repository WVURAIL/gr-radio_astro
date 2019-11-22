/* -*- c++ -*- */
/* 
 * Copyright 2019 - Quiet Skies LLC -- Glen Langston - glen.i.langston@gmail.com
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

#ifndef INCLUDED_RADIO_ASTRO_VMEDIAN_IMPL_H
#define INCLUDED_RADIO_ASTRO_VMEDIAN_IMPL_H

#include <radio_astro/vmedian.h>

#define MAX_VLEN 16384

namespace gr {
  namespace radio_astro {

    class vmedian_impl : public vmedian
    {
     private:
      // values computed in this block
      int d_vec_length = 2048;
      int d_n = 4;
      int d_n1 = d_n-1;
      int d_n2 = d_n-2;
      int count = 0;          // count of vectors so far processed
      int vlen = d_vec_length;
      float vsum[MAX_VLEN];   // vector sum of samples in channel
      float vmin[MAX_VLEN];   // vector of minimum values in channel
      float vmax[MAX_VLEN];   // vector of maximum values in channel
      float oneovern2 = 1./float(d_n2);  // Normally median 4 values, so exclude min,max (2)
      
     public:
      vmedian_impl(int vec_length, int n);
      ~vmedian_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      void set_mode( int n);

      void set_vlen( int vec_length);
      
      int vmedian(const float *input, float *output);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    }; 
  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_VMEDIAN_IMPL_H */
