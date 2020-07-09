# Install script for directory: /home/john/gr_repositories/gr-radio_astro/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
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

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/radio_astro" TYPE FILE FILES
    "/home/john/gr_repositories/gr-radio_astro/python/__init__.py"
    "/home/john/gr_repositories/gr-radio_astro/python/systemp_calibration.py"
    "/home/john/gr_repositories/gr-radio_astro/python/chart_recorder.py"
    "/home/john/gr_repositories/gr-radio_astro/python/correlate.py"
    "/home/john/gr_repositories/gr-radio_astro/python/csv_filesink.py"
    "/home/john/gr_repositories/gr-radio_astro/python/hdf5_sink.py"
    "/home/john/gr_repositories/gr-radio_astro/python/radioastronomy.py"
    "/home/john/gr_repositories/gr-radio_astro/python/jdutil.py"
    "/home/john/gr_repositories/gr-radio_astro/python/angles.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_ascii_sink.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_event_log.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_event_sink.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_integrate.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_vave.py"
    "/home/john/gr_repositories/gr-radio_astro/python/ra_vmedian.py"
    "/home/john/gr_repositories/gr-radio_astro/python/powerSpectrum.py"
    "/home/john/gr_repositories/gr-radio_astro/python/integration.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/radio_astro" TYPE FILE FILES
    "/home/john/gr_repositories/gr-radio_astro/build/python/__init__.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/systemp_calibration.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/chart_recorder.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/correlate.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/csv_filesink.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/hdf5_sink.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/radioastronomy.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/jdutil.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/angles.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_ascii_sink.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_event_log.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_event_sink.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_integrate.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_vave.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_vmedian.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/powerSpectrum.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/integration.pyc"
    "/home/john/gr_repositories/gr-radio_astro/build/python/__init__.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/systemp_calibration.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/chart_recorder.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/correlate.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/csv_filesink.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/hdf5_sink.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/radioastronomy.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/jdutil.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/angles.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_ascii_sink.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_event_log.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_event_sink.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_integrate.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_vave.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/ra_vmedian.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/powerSpectrum.pyo"
    "/home/john/gr_repositories/gr-radio_astro/build/python/integration.pyo"
    )
endif()

