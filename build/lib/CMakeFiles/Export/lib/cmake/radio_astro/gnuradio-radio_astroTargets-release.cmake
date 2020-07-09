#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-radio_astro" for configuration "Release"
set_property(TARGET gnuradio::gnuradio-radio_astro APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gnuradio::gnuradio-radio_astro PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-radio_astro.so.f6eb67f0"
  IMPORTED_SONAME_RELEASE "libgnuradio-radio_astro.so.1.0.0git"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-radio_astro )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-radio_astro "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-radio_astro.so.f6eb67f0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
