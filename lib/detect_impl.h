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

#ifndef INCLUDED_RADIO_ASTRO_DETECT_IMPL_H
#define INCLUDED_RADIO_ASTRO_DETECT_IMPL_H

#include <radio_astro/detect.h>

#ifndef TIME_UTC                   // must define utc time flag
#define TIME_UTC    1
#endif

#define MAX_VLEN 16384
#define MAX_BUFF (2L*MAX_VLEN)

// constants for calculating Modified Julian Date
#define DaysPer400Years   (365L*400 + 97)
#define DaysPer100Years   (365L*100 + 24)
#define DaysPer4Years     (365*4    +  1)
#define DaysPer1Year      365
#define MonthsPerYear     12
#define MonthsPer400Years (12*400)
#define MonthMarch        3
#define mjdOffset         (678881  /* Epoch Nov 17, 1858 */)

static const short DaysMarch1ToBeginingOfMonth[12] = { 
  0, 
  31, 
  31 + 30, 
  31 + 30 + 31, 
  31 + 30 + 31 + 30, 
  31 + 30 + 31 + 30 + 31, 
  31 + 30 + 31 + 30 + 31 + 31,
  31 + 30 + 31 + 30 + 31 + 31 + 30,
  31 + 30 + 31 + 30 + 31 + 31 + 30 + 31,
  31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30, 
  31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31,
  31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 31 };

namespace gr {
  namespace radio_astro {

    class detect_impl : public detect
    {
     private:
      // values computed in this block
      int d_vec_length = 2048;
      float d_dms = 4.0;
      float d_f_obs = 1.;
      float d_bw = 1.;
      float d_t_int = 0.;
      int d_nt = 1;
      int vlen = d_vec_length;
      int vlen2 = vlen/2;
      double nsigma = 4.0;
      double peak = 0;        // peak, rms and date/time of detected event
      double rms = 0;         // rms of values in circular buffer
      double mjd = 0;         // modified Julian Date of event
      gr_complex circular[MAX_BUFF];
      float circular2[MAX_BUFF];   // circular buffer for input samples**2
      long inext = 0;         // next place for a sample in buffer
      long inext2 = MAX_BUFF/2;  // place to check for new peak
      long imax2 = 0;         // index to last maximum
      double max2 = 0;        // max value squared so far
      double sum2 = 0;        // sum of values squared
      double rms2 = 0;        // rms squared of values in circular buffer
      double oneovern = 1./double(MAX_BUFF);
      bool bufferfull = false;// assume buffer is not full 
      double nsigma_rms = 0;  // comparision value for event detection
      gr_complex samples[MAX_VLEN];  // output event buffer 
      bool initialized = 0;   // flag initializing output
      double bufferdelay = float(MAX_VLEN/2)*1.E-6/d_bw;
      
     public:
      detect_impl(int vec_length,float dms, float f_obs, float bw, float t_int, int nt);
      ~detect_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      //      set nsigma for a detection;
      void set_dms( float dms);

      //      set the bandwidth, in MHz
      void set_bw( float bw);

      void set_freq( float f_obs);

      void set_dt( float t_int);
      
      void set_mode( int nt);

      void set_vlen( int vec_length);
      
      int update_buffer();

      int event(const gr_complex *input, gr_complex *output);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      /* function for Modified Julian Date (MJD) */
      int ymd_to_mjd(int year, int month, int day);      

      /* more accurate function for Modified Julian Date (MJD) */
      int ymd_to_mjd_x(int year, int month, int day);      

      double get_mjd();
    }; 
  } // namespace radio_astro
} // namespace gr

#endif /* INCLUDED_RADIO_ASTRO_DETECT_IMPL_H */