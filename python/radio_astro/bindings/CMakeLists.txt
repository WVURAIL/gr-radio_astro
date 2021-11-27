# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT radio_astro_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT radio_astro_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND radio_astro_python_files
    dedispersion_python.cc
    detect_python.cc
    vmedian_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(radio_astro
   ../../..
   gr::radio_astro
   "${radio_astro_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/radio_astro/
  DEPENDS radio_astro_python)

install(TARGETS radio_astro_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/radio_astro COMPONENT pythonapi)
