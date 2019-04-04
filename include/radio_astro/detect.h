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

#ifndef INCLUDED_RADIO_ASTRO_DETECT_H
#define INCLUDED_RADIO_ASTRO_DETECT_H

#include <radio_astro/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace radio_astro {

    /*!
     * \brief Event Detection by comparison of signal to RMS Noise level.
     * event detection: fill a circular buffer with complex samples and
     * search for peaks nsigma above the RMS of the data stream
     * input:
     * complex vector of I/Q samples
     * parameters
     * 1. Vector length
     * 2. Number of sigma to declare an event
     * 3. Bandwidth used to unwind the time of the event in circular buffer
     * 4. Estimated time it takes for sample to go from input of horn to block
     * 5. Mode: 1: Monitor, just pass input data,
     *          2: Detect events and repeatedly output the last event
     * output:
     * 1: Vector of complex I/Q samples
     * Event is tagged with three floating point values:
     * 1. Modified Julian Date of Event
     * 2. Peak intensity
     * 3. RMS of data stream near event
     * \ingroup radio_astro
     *
     */
    class RADIO_ASTRO_API detect : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<detect> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of radio_astro::detect.
       *
       * To avoid accidental use of raw pointers, radio_astro::detect's
       * constructor is in a private implementation
       * class. radio_astro::detect::make is the public interface for
       * creating new instances.
       */
      static sptr make(int vec_length, float dms, float f_obs, float bw, float t_int, int nt);

      virtual void set_dms(float dms) = 0;  // This is the nsigma parameter

      virtual void set_vlen(int vec_length) = 0;  // This is the nsigma parameter
      virtual void set_mode(int nt) = 0;  // Data stream (mode == 0) or event

      virtual void set_bw(float bw) = 0;

      virtual void set_freq(float f_obs) = 0;
      
    };

  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_DETECT_H */