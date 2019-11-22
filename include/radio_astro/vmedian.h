/* -*- c++ -*- */
/* 
 * Copyright 2019 Quiet Skies LLC -- Glen Langston, Proprietor.
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

#ifndef INCLUDED_RADIO_ASTRO_VMEDIAN_H
#define INCLUDED_RADIO_ASTRO_VMEDIAN_H

#include <radio_astro/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace radio_astro {

    /*!
     * \brief Vector Median of several vectors.   For 3 or 4 vectors 
     * the code implements exactly the median of the values
     * for more vectors, the result is the sum of all values minus the 
     * miniumum and maximum values
     * input:
     * vector of length vector_lenght 
     * parameters
     * 1. Vector length
     * 2. N Number of vectors to median.  This is the decimation rate
     * output:
     * 1: Vector of floating point samples
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API vmedian : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<vmedian> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of radio_astro::vmedian.
       *
       * To avoid accidental use of raw pointers, radio_astro::vmedian's
       * constructor is in a private implementation
       * class. radio_astro::vmedian::make is the public interface for
       * creating new instances.
       */
      static sptr make(int vec_length, int n);

      virtual void set_vlen(int vec_length) = 0;  // This is the nsigma parameter
      virtual void set_mode(int n) = 0;  // Number of vectors to median > 2

    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_VMEDIAN_H */
