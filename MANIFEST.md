title: gr-radio_astro
brief: GNU Radio out-of-tree blocks and flowgraphs for radio astronomy with software-defined radios.
tags:
  - sdr
  - radio astronomy
  - gnuradio
  - dsp
  - instrumentation
  - hydrogen line
author:
  - WVU Radio Astronomy Instrumentation Lab <wvurail@gmail.com>
  - Glen Langston
  - Kevin Bandura
  - John Makous
  - Pranav Sanghavi
copyright_owner:
  - WVU Radio Astronomy Instrumentation Lab
license: GPL-3.0
gr_supported_version: v3.10
repo: https://github.com/WVURAIL/gr-radio_astro
website: https://wvurail.org/
---
Blocks and GNU Radio Companion flowgraphs for doing radio astronomy with a
software-defined radio: integration and averaging, calibration against hot and
cold loads, event detection and dedispersion, correlation for two-element
interferometry, and sinks that write spectra to CSV, HDF5 and PNG.

The module carries two related bodies of work. The **NSF Integrate and Detect**
software supports neutral-hydrogen measurements and transient event detection,
and is documented in the
[LightWork memo series](https://wvurail.org/lightwork/). The **DSPIRA**
software was written for and by the high school teachers of the NSF Research
Experiences for Teachers site at West Virginia University; the curriculum built
on it is at [dspira-lessons](https://wvurail.org/dspira-lessons/).

Requires GNU Radio 3.10 or newer.

Licensing is not uniform across the repository: some files are GPL-3.0-only,
some GPL-3.0-or-later, and a few retained utility files carry BSD terms. See
NOTICE, and the notice in each file, which remain the authoritative terms.
