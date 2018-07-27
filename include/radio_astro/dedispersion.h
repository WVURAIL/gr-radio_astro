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


#ifndef INCLUDED_RADIO_ASTRO_DEDISPERSION_H
#define INCLUDED_RADIO_ASTRO_DEDISPERSION_H

#include <radio_astro/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace radio_astro {

    /*!
     * \brief <+description of block+>
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API dedispersion : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<dedispersion> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of radio_astro::dedispersion.
       *
       * To avoid accidental use of raw pointers, radio_astro::dedispersion's
       * constructor is in a private implementation
       * class. radio_astro::dedispersion::make is the public interface for
       * creating new instances.
       */
      static sptr make(int vec_length, float dms, float f_obs, float bw, float t_int, int nt);
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_DEDISPERSION_H */

