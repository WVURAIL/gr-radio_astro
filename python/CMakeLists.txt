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

########################################################################
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    powerSpectrum.py
    hdf5_sink.py
    dedisperse.py
    correlate.py
    radioastronomy.py
    jdutil.py
    angles.py
    ra_integrate.py
    ra_vave.py
    ra_ascii_sink.py
    ra_vmedian.py
    systemp_calibration.py
    ra_event_log.py
    ra_event_sink.py
    chart_recorder.py
    csv_filesink.py DESTINATION ${GR_PYTHON_DIR}/radio_astro
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-radio_astro)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_powerSpectrum ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_powerSpectrum.py)
GR_ADD_TEST(qa_hdf5_sink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_hdf5_sink.py)
GR_ADD_TEST(qa_dedisperse ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dedisperse.py)
GR_ADD_TEST(qa_dedispersion ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dedispersion.py)
GR_ADD_TEST(qa_correlate ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_correlate.py)
GR_ADD_TEST(qa_ra_integrate ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_integrate.py)
GR_ADD_TEST(qa_ra_vave ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_vave.py)
GR_ADD_TEST(qa_ra_ascii_sink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_ascii_sink.py)
GR_ADD_TEST(qa_ra_vmedian ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_vmedian.py)
GR_ADD_TEST(qa_systemp_calibration ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_systemp_calibration.py)
GR_ADD_TEST(qa_detect ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_detect.py)
GR_ADD_TEST(qa_ra_event_log ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_event_log.py)
GR_ADD_TEST(qa_ra_event_sink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ra_event_sink.py)
GR_ADD_TEST(qa_chart_recorder ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_chart_recorder.py)
GR_ADD_TEST(qa_csv_filesink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_csv_filesink.py)
