INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RADIO_ASTRO radio_astro)

FIND_PATH(
    RADIO_ASTRO_INCLUDE_DIRS
    NAMES radio_astro/api.h
    HINTS $ENV{RADIO_ASTRO_DIR}/include
        ${PC_RADIO_ASTRO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RADIO_ASTRO_LIBRARIES
    NAMES gnuradio-radio_astro
    HINTS $ENV{RADIO_ASTRO_DIR}/lib
        ${PC_RADIO_ASTRO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RADIO_ASTRO DEFAULT_MSG RADIO_ASTRO_LIBRARIES RADIO_ASTRO_INCLUDE_DIRS)
MARK_AS_ADVANCED(RADIO_ASTRO_LIBRARIES RADIO_ASTRO_INCLUDE_DIRS)

