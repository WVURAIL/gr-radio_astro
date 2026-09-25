# Radio research software

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14583457.svg)](https://doi.org/10.5281/zenodo.14583457)

Research applications and GNU Radio blocks for radio astronomy with software-defined receivers.
This repository was formerly named `gr-radio_astro`.

## What belongs here

- NSF Integrate and Detect applications for spectral acquisition and event recording.
- Research blocks for integration, event detection, median filtering, and dedispersion.
- Transient simulation notebooks, reference data, and historical bench experiments.

Classroom telescope applications and all twelve DSPIRA processing blocks now live in
[dspira-software](https://github.com/WVURAIL/dspira-software).
They are installed together from that repository.
Board designs belong in [dspira-hardware](https://github.com/WVURAIL/dspira-hardware).

The [DSPIRA website](https://wvurail.org/dspira/) provides classroom installation and observing instructions.
The [LightWork memo series](https://wvurail.org/lightwork/) documents research and instrument development.

## Installing from source

The research package targets GNU Radio 3.10. On Ubuntu, install dependencies:

```sh
sudo apt-get update
sudo apt-get install gnuradio-dev gr-osmosdr airspy cmake build-essential libboost-all-dev python3-h5py python3-ephem python3-pybind11 pybind11-dev
```

Clone, build, test, and install:

```sh
git clone https://github.com/WVURAIL/radio-research-software.git
cd radio-research-software
cmake -S . -B build -DPYTHON_EXECUTABLE=/usr/bin/python3
cmake --build build
ctest --test-dir build --output-on-failure
sudo cmake --install build
sudo ldconfig
python3 -c "from gnuradio import radio_astro; print(radio_astro.__file__)"
```

The Python module remains `gnuradio.radio_astro` for compatibility with research applications.
The repository name does not change the research block identifiers or C++ interface.
Keep the old repository name unused so GitHub's repository redirect continues working.

## Applications and examples

See [the example catalog](examples/README.md) for NSF applications.
[Transient simulations](examples/transients/) include notebooks, reference datasets, and research notes.
Their catalog explains limitations and links the historical bench material.
Some older bench examples use the HDF5 recorder now installed by DSPIRA software.
See [the classroom block move](docs/DSPIRA_BLOCK_MOVE.md) before using those examples.

## History

Historical branches were reviewed and consolidated in 2026.
[Branch history](docs/BRANCH_HISTORY.md) records their disposition and the earlier prototype migration.
Old tags preserve earlier environments, including the GNU Radio 3.8 releases.
The published DOI and original notices remain unchanged.
