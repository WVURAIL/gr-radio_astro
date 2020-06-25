/* -*- c++ -*- */
/* 
 * Copyright 2019 - Quiet Skies LLC -- Glen Langston - glen.i.langston@gmail.com
 * 
 * This is free software;  you can redistribute it and/or modify
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

/* HISTORY 
 * 20Jun25 GIL process all provided vectors
 * 20Jun23 GIL try to find reason some events are missed
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <stdio.h>
#include <time.h> 
#include "detect_impl.h"
#include <iostream>
#include <chrono>

namespace gr {
  namespace radio_astro {

    detect::sptr
    detect::make(int vec_length, float dms, float f_obs, float bw, float t_int, int nt)
    {
      return gnuradio::get_initial_sptr
        (new detect_impl(vec_length, dms, f_obs, bw, t_int, nt));
    }

    /*
     * The private constructor
     */
    detect_impl::detect_impl(int vec_length, float dms, float f_obs, float bw, float t_int, int nt)
      : gr::block("detect",
		  gr::io_signature::make(1, 1, sizeof(gr_complex)*vec_length),
		  gr::io_signature::make(1, 1, sizeof(gr_complex)*vec_length)),
        d_vec_length(vec_length),
        d_dms(dms),
        d_f_obs(f_obs),
        d_bw(bw),
        d_t_int(t_int),
        d_nt(nt)
    { set_vlen( vec_length);  /* initialize all imput values */
      set_mode( nt);
      set_dms( dms);
      set_bw( bw);
      set_freq( f_obs);
      set_dt( t_int);
    }

    /*
     * Our virtual destructor.
     */
    detect_impl::~detect_impl()
    {
    }

    long
    detect_impl::ymd_to_mjd(int year, int month, int day) 
    { long double MJD = 0;
      long I = year, J = month, K = day, JD = 0;

      // Julian date, JD, is calculated only with integer math for 1800 to 2099
      JD = (K-32075);
      JD += 1461*(I+4800+(J-14)/12)/4+367*(J-2-(J-14)/12*12)/12;
      JD -= 3*((I+4900+(J-14)/12)/100)/4;
      MJD = JD - 2400000;
      // printf("Date %5d/%2d/%2d -> %9.1f\n",year, month, day, MJD);
      return( int(MJD));
    } //end of ymd_to_mjd()

    long
    detect_impl::ymd_to_mjd_x(int year, int month, int day) 
    {
      year += month / MonthsPerYear;
      month %= MonthsPerYear;
      // Adjust for month/year to Mar... Feb
      while (month < MonthMarch) {
	month += MonthsPerYear; // Months per year
	year--;
      }
      long d = (year / 400) * DaysPer400Years;
      long y400 = (int) (year % 400);
      d += (y400 / 100) * DaysPer100Years;
      int y100 = y400 % 100;
      d += (y100 / 4) * DaysPer4Years;
      long y4 = y100 % 4;
      d += y4 * DaysPer1Year;
      d += DaysMarch1ToBeginingOfMonth[month - MonthMarch];
      d += day;
      // November 17, 1858 == MJD 0
      d--;
      d -= mjdOffset;
      return d;
    } /* end of int ymd_to_mjd_x() */

    double 
    detect_impl::get_mjd()
    {
      long double mjd = 0, seconds = 0;
      struct timespec ts;
      long r = clock_gettime(CLOCK_REALTIME, &ts);
      char buff[100];
      time_t now = time(NULL);
      struct tm *ptm = gmtime(&now);

      long year = ptm->tm_year + 1900;
      long month = ptm->tm_mon + 1;
      long day = ptm->tm_mday;
      // printf("Current date: %5d %3d %3d\n", year, month, day);
      mjd = ymd_to_mjd_x( year, month, day);

      strftime(buff, sizeof buff, "%D %T", gmtime(&ts.tv_sec));
      // printf("Current time: %s.%09ld UTC\n", buff, ts.tv_nsec);
      
      seconds =  ptm->tm_sec + (60.*ptm->tm_min) + (3600.*ptm->tm_hour);
      //      seconds = seconds % 86400.;
      seconds += (1.e-9*ts.tv_nsec);
      mjd += (seconds/86400.);
      //      printf("MJD: %15.9f + %15.9fs\n", mjd, seconds);

      return mjd;
    } // end of get_mjd()

    void
    detect_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      unsigned ninputs = ninput_items_required.size();
      for(unsigned int i = 0; i < ninputs; i++)
       	    ninput_items_required[i] = noutput_items;
    }

    void 
    detect_impl::set_dms ( float dms)
    {
      nsigma = dms;
      printf("Input N Sigma: %7.1f\n", nsigma);
      d_dms = dms;
    }

    void 
    detect_impl::set_dt ( float dt)
    {
      d_t_int = dt;
      printf("Input Sample Delay: %15.9f s\n", d_t_int);
    }
      
    void 
    detect_impl::set_bw ( float bw)
    {
      if (bw < 0.01)
	{printf("Input Bandwidth too small: %10.6f (MHz)\n", bw);
	 bw = 1.0;
	}
      d_bw = bw;
      
      printf("Input Bandwidth: %7.1f (MHz)\n", bw);
      bufferdelay = float(MAX_VLEN/2)*1.E-6/d_bw;
    }
      
    void 
    detect_impl::set_freq ( float freq)
    {
      d_f_obs = freq;
      printf("Input Frequency: %7.1f (MHz)\n", d_f_obs);
    }
      
    void 
    detect_impl::set_mode ( int nt)
    {
      if (nt == 0){
	printf("Input Mode: Monitor\n");
      }
      else {
	printf("Input Mode: Detect\n");
      }
	
      d_nt = nt;
    } // end of set_mode()
      
    void 
    detect_impl::set_vlen ( int invlen)
    { vlen = invlen;
      if (vlen < 32) 
	{ vlen = 32;
	    printf("Vector Length too short, using %5d\n", vlen);
	}
      else if (vlen > MAX_VLEN) 
	{ vlen = MAX_VLEN;
	    printf("Vector Length too large, using %5d\n", vlen);
	}
      d_vec_length = vlen;
      vlen2 = vlen/2;
      
      // vectors do not yet work;  circular = std::vector<gr_complex>(vlen);
      // now must initialize indicies
      inext = 0;
      bufferfull = false;
      inext2 = (MAX_BUFF/2) + 1;
      printf("Buffer is not full: %5d\n", inext2);
    } // end of set_vlen()
      
    int
    detect_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      unsigned ninputs = ninput_items.size();
      int success;

      // since this is a 1 to 1 process, the numbrer of inputs is
      // the same as the number of output items
      success = event(noutput_items, in, out);
      
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    } // end of detect_impl:: general_work
    

    int
    detect_impl::update_buffer()
    { long i = inext2 - vlen2, length = vlen,
	jstart = 0;

      // the event is centered on sample inext2. Must copy vlen2 before
      // and after the event.   Deal with circular buffer
      // Now must reset the buffer to wait for the next event
      bufferfull = false;

      // if event is within the circular buffer 
      if ((i >= 0) && ((i + length) < MAX_BUFF))
	{ for (long j = 0; j < length; j++)
	    { samples[j] = circular[i];
	      i++;
	    }
	}
      else if (i < 0)   // if before beging of buffer, on other end
	{ i += MAX_BUFF;
	  length = MAX_BUFF - i;
       	  // printf("Two part-shift; Move 1: i=%ld, length=%ld\n", i, length);
	  for (long j = 0; j < length; j++)
	    { samples[j] = circular[i];
	      i++;
	    }
	  i = 0; 
	  jstart = length;
	  length = vlen - length;
       	  // printf("Two part-shift; Move 2: i=%ld, length=%ld\n", i, length);
	  for (long j = jstart; j < vlen; j++)
	    { samples[j] = circular[i];
	      i++;
	    }
	}
      else
	{  /* near end of circular buffer */
	  length = MAX_BUFF - i;
	  if (length > vlen)
	    length = vlen;
	  // printf("End Two part+shift; Move 1: i=%ld, length=%ld\n", i, length);  
	  for (long j = 0; j < length; j++) 
	    {
	      samples[j] = circular[i];
	      i++;
	    }
	  i = 0;
	  jstart = length;
	  length = vlen - length;
	  // printf("End Two part+shift; Move 2: i=%ld, shift=%ld\n", i, length);
	  for (long j = jstart; j < vlen; j++)
	    {
	      samples[j] = circular[i];
	      i++;
	    }
	} // else near end of circular buffer
    return 0;
  } // end of update_buffer()
    
    int
    detect_impl::event(const unsigned ninputs, const gr_complex *input, gr_complex *output)
    {
      //outbuf = (float *) //create fresh one if necessary
      float n_sigma = d_dms; // translate variables 
      //      int vlen = d_vec_length;
      long datalen = d_vec_length * ninputs, nout = 0, jjj = 0;
      gr_complex rp = 0;
      double mag2 = 0, dmjd = 0;

      // get time all samples arrive for any events found
      dmjd = get_mjd();
      // fill the circular buffer
      for(unsigned long j=0; j < datalen; j++)
	{ rp = input[j];
	  mag2 = (rp.real()*rp.real()) + (rp.imag()*rp.imag());
	  circular[inext] = rp;
	  circular2[inext] = mag2;
	  sum2 += mag2;
	  inext++;
	  if (inext >= MAX_BUFF) // if buffer is full
	    { rms2 = sum2*oneovern;
	      rms = sqrt(rms2);
	      inext = 0;
	      bufferfull = true; // flag buffer is now full
		  
	      nsigma_rms = nsigma*nsigma*rms2;
	      sum2 = 0;          // restart rms sum
	    }
	  inext2++;              // update position for search 
	  if (inext2 >= MAX_BUFF) // if at end of circular buffer
	    inext2 = 0;           // go back to beginning
	  if (bufferfull)         // when buffer is full, find peaks
	    {
	      if (circular2[inext2] > nsigma_rms)
		{
		  imax2 = inext2;
		  peak = sqrt(circular2[inext2]);
		  // printf( "N-sigma Peak found: %7.1f\n", peak/rms);
		  // add tags to event
		  add_item_tag(0, // Port number
			       nitems_written(0) + 1, // Offset
			       pmt::mp("PEAK"), // Key
			       pmt::from_double(peak) // Value
			       );
		  add_item_tag(0, // Port number
			       nitems_written(0) + 1, // Offset
			       pmt::mp("RMS"), // Key
			       pmt::from_double(rms) // Value
			       );
		  // dmjd = get_mjd();
		  // time now is after all samples have arrived.
		  // the event was found at sample j + vlen2
		  bufferdelay = float((datalen-j)+vlen2)*1.E-6/d_bw;
		  dmjd -= bufferdelay;
		  // printf("Event MJD: %15.6f; Peak=%8.4f+/-%6.4f\n", dmjd, peak, rms);
		  add_item_tag(0, // Port number
			       nitems_written(0) + 1, // Offset
			       pmt::mp("MJD"), // Key
			       pmt::from_double(dmjd) // Value
			       );

		  update_buffer();
		  break;
		} // end if an event found
	    } // end if buffer full
	} // end for all samples
	      
      if (! initialized) {
	for (int iii = 0; iii <  d_vec_length; iii++)
	  { samples[iii] = input[iii];
	  }
	initialized = 1;     // no need to re-initialize the event
      }

      if (d_nt == 0) // if monitoring input, just output input 
	{
	  // always output the last event
	  for (int iii = 0; iii <  datalen; iii++)
	    { output[iii] = input[iii];
	    }
	}
      else {
	// repeated output the last event
	for (nout = 0; nout < ninputs; nout++)
	  { // fill all output vectors with last event
	    for (int iii = 0; iii < d_vec_length; iii++)
	      { output[jjj] = samples[iii];
		jjj++;
	      }
	  } // end for all input vectors
      } // end else output event

      return 0;
    } // end of detect_impl::event()

  } /* namespace radio_astro */
} /* namespace gr */

