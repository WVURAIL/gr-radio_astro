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

#ifndef INCLUDED_RADIO_ASTRO_DEDISPERSION_IMPL_H
#define INCLUDED_RADIO_ASTRO_DEDISPERSION_IMPL_H

#include <radio_astro/dedispersion.h>

namespace gr {
  namespace radio_astro {

    class dedispersion_impl : public dedispersion
    {
     private:
      // Nothing to declare in this block.
      int d_vec_length;
      float d_dms;
      float d_f_obs;
      float d_bw;
      float d_t_int;
      int d_nt;

     public:
      dedispersion_impl(int vec_length,float dms, float f_obs, float bw, float t_int, int nt);
      ~dedispersion_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int dedisperse(const float *input, float *output);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_DEDISPERSION_IMPL_H */

