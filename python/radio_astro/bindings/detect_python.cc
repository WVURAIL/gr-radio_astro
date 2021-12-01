/*
 * Copyright 2021 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(detect.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(f5a10bd3e08ff521c9fc6a21d3175fb4)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/radio_astro/detect.h>
// pydoc.h is automatically generated in the build directory
#include <detect_pydoc.h>

void bind_detect(py::module& m)
{

    using detect    = gr::radio_astro::detect;


    py::class_<detect, gr::block, gr::basic_block,
        std::shared_ptr<detect>>(m, "detect", D(detect))

        .def(py::init(&detect::make),
           D(detect,make)
        )
        



        ;




}







