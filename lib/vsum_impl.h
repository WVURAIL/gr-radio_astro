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

#include <gnuradio/radio_astro/vsum.h>

#define MAX_VLEN (16384)

namespace gr {
  namespace radio_astro {

    class vsum_impl : public vsum
    {
     private:
      // values computed in this block
      int d_vec_length = 2048;
      int d_c_begin = 500;
      int d_c_end = 1028;
      int vlen = d_vec_length;
      int c_begin = d_c_begin;
      int c_end = d_c_end;
      int n = c_end - c_begin;
      float oneovern = 1./float(n); // Normally 4 values, so exclude min,max (2)
      
     public:
      vsum_impl(int vec_length, int c_begin, int c_endn);
      ~vsum_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      void set_c_begin( int c_begin);

      void set_c_end( int c_end);

      void set_vlen( int vec_length);

      void checkn( );
      
      int vsum(const float *input, float *output);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    }; 
  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_VSUM_IMPL_H */
