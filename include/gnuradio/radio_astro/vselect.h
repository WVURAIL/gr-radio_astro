/* -*- c++ -*- */
/*
 * Copyright 2020 Quiet Skies LLC -- Glen Langston - glen.i.langston@gmail.com.
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

#ifndef INCLUDED_RADIO_ASTRO_VSELECT_H
#define INCLUDED_RADIO_ASTRO_VSELECT_H

#include <gnuradio/radio_astro/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace radio_astro {

    /*!
    * \brief Vector Selects a range of channeles from a vector.  The selected
     * channel range is copied to the output vector. 
     * input:
     * vector of length vector_length 
     * parameters
     * 1. Input Vector length
     * 2. vector beginning channel to select. 
     * 3. vec_out_len - length of output vector
     * output:
     * 1: Vector of floating point samples, of length vec_out_len
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API vselect : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<vselect> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of radio_astro::vselect.
       *
       * To avoid accidental use of raw pointers, radio_astro::vselect's
       * constructor is in a private implementation
       * class. radio_astro::vselect::make is the public interface for
       * creating new instances.
       */

      virtual void set_vlen(int vec_length) = 0;  // Vector Length Parameter

      virtual void set_vec_begin(int vec_begin) = 0;  // start channel of select

      virtual void set_vec_out_len(int vec_out_len) = 0;  // Number of channels to select

      static sptr make(int vec_length, int vec_begin, int vec_out_len);
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_VSELECT_H */

