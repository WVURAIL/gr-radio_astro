# Install script for directory: /Users/glangsto/Research/gr-radio_astro/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/opt/local/")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro" TYPE FILE FILES
    "/Users/glangsto/Research/gr-radio_astro/python/__init__.py"
    "/Users/glangsto/Research/gr-radio_astro/python/powerSpectrum.py"
    "/Users/glangsto/Research/gr-radio_astro/python/hdf5_sink.py"
    "/Users/glangsto/Research/gr-radio_astro/python/dedisperse.py"
    "/Users/glangsto/Research/gr-radio_astro/python/correlate.py"
    "/Users/glangsto/Research/gr-radio_astro/python/radioastronomy.py"
    "/Users/glangsto/Research/gr-radio_astro/python/jdutil.py"
    "/Users/glangsto/Research/gr-radio_astro/python/angles.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_integrate.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_vave.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_ascii_sink.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_vmedian.py"
    "/Users/glangsto/Research/gr-radio_astro/python/systemp_calibration.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_event_log.py"
    "/Users/glangsto/Research/gr-radio_astro/python/ra_event_sink.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro" TYPE FILE FILES
    "/Users/glangsto/Research/gr-radio_astro/build/python/__init__.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/powerSpectrum.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/hdf5_sink.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/dedisperse.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/correlate.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/radioastronomy.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/jdutil.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/angles.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_integrate.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_vave.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_ascii_sink.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_vmedian.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/systemp_calibration.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_event_log.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_event_sink.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/python/__init__.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/powerSpectrum.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/hdf5_sink.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/dedisperse.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/correlate.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/radioastronomy.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/jdutil.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/angles.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_integrate.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_vave.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_ascii_sink.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_vmedian.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/systemp_calibration.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_event_log.pyo"
    "/Users/glangsto/Research/gr-radio_astro/build/python/ra_event_sink.pyo"
    )
endif()

