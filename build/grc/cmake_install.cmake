# Install script for directory: /home/john/gr_repositories/gr-radio_astro/grc

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_systemp_calibration.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_dedispersion.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_detect.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_vmedian.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_chart_recorder.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_correlate.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_csv_filesink.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_hdf5_sink.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_powerSpectrum.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_ascii_sink.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_event_log.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_event_sink.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_integrate.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_vave.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_ra_vmedian.block.yml"
    "/home/john/gr_repositories/gr-radio_astro/grc/radio_astro_integration.block.yml"
    )
endif()

