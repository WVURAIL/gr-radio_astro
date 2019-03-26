# Install script for directory: /Users/glangsto/Research/gr-radio_astro/swig

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro" TYPE MODULE FILES "/Users/glangsto/Research/gr-radio_astro/build/swig/_radio_astro_swig.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro/_radio_astro_swig.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro/_radio_astro_swig.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro/_radio_astro_swig.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro" TYPE FILE FILES "/Users/glangsto/Research/gr-radio_astro/build/swig/radio_astro_swig.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/radio_astro" TYPE FILE FILES
    "/Users/glangsto/Research/gr-radio_astro/build/swig/radio_astro_swig.pyc"
    "/Users/glangsto/Research/gr-radio_astro/build/swig/radio_astro_swig.pyo"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/radio_astro/radio_astro/swig" TYPE FILE FILES
    "/Users/glangsto/Research/gr-radio_astro/swig/radio_astro_swig.i"
    "/Users/glangsto/Research/gr-radio_astro/build/swig/radio_astro_swig_doc.i"
    )
endif()

