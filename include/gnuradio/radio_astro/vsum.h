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

#ifndef INCLUDED_RADIO_ASTRO_VSUM_H
#define INCLUDED_RADIO_ASTRO_VSUM_H

#include <gnuradio/radio_astro/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace radio_astro {

    /*!
    * \brief Vector Sum channels;  returns the average of channels in range
     * input:
     * vector of length vector_lenght 
     * parameters
     * 1. Vector length
     * 2. Begin Channel Number
     * 3. End Channel Number
     * output:
     * 1: Floating point average of channels
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API vsum : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<vsum> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of radio_astro::vsum.
       *
       * To avoid accidental use of raw pointers, radio_astro::vsum's
       * constructor is in a private implementation
       * class. radio_astro::vsum::make is the public interface for
       * creating new instances.
       */

      virtual void set_vlen(int vec_length) = 0;  // Size of input vector

      virtual void set_c_begin(int c_begin) = 0;  // Begin channel to sum

      virtual void set_c_end(int c_end) = 0;  // End channel to sum

      static sptr make(int vec_length, int c_begin, int c_end);   
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_VSUM_H */

