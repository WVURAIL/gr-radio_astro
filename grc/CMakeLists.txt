# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    radio_astro_powerSpectrum.xml
    radio_astro_hdf5_sink.xml
    radio_astro_dedisperse.xml
    radio_astro_dedispersion.xml
    radio_astro_correlate.xml
    radio_astro_ra_integrate.xml
    radio_astro_ra_vave.xml
    radio_astro_ra_ascii_sink.xml
    radio_astro_ra_vmedian.xml
    radio_astro_vmedian.xml
    radio_astro_systemp_calibration.xml
    radio_astro_detect.xml
    radio_astro_ra_event_log.xml
    radio_astro_ra_event_sink.xml
    radio_astro_chart_recorder.xml
    radio_astro_csv_filesink.xml DESTINATION share/gnuradio/grc/blocks
)
