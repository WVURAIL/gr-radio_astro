/* -*- c++ -*- */
/* 
 * Copyright 2019 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_RADIO_ASTRO_DEDISPERSED_H
  #define INCLUDED_RADIO_ASTRO_DEDISPERSED_H

#include <radio_astro/api.h>
#include <gnuradio/block.h>


namespace gr {
  namespace radio_astro {

    /*!
     * \brief Dedisperses incoming signals along a range of specified DMs. 
     * 
     * This is the number of frequency channels that the signal is contained
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API dedispersed : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<dedispersed> sptr;

      
      static sptr make(int vec_length, int dms, float f_obs, float bw, float t_int, int nt, int s_bw, int e_bw, int dm_step);
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_DEDISPERSED_H */

