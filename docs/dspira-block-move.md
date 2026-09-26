# DSPIRA block move

The research repository was renamed from `gr-radio_astro` to `radio-research-software`.
Its research applications and installed `gnuradio.radio_astro` module remain here.

The twelve classroom blocks now have one maintained home in
[dspira-software](https://github.com/WVURAIL/dspira-software):

`chart_recorder`, `comparator`, `correlate`, `csv_filesink`, `hdf5_sink`,
`integration`, `png_print_spectrum`, `powerSpectrum`, `running_norm_std`,
`systemp_calibration`, `triggered_save_csv`, and `vector_moving_average`.

Their Python implementations were moved unchanged, together with the GRC definitions,
copyright notices, and existing tests. The destination's `docs/block-migration.json`
records source paths and checksums from revision
`cdbda4f577b538c0750b882241f8a36ecc2e88f8`.

The destination installs `gnuradio.dspira`. GRC identifiers retain their previous
`radio_astro_` names so saved flowgraphs still load; generated Python imports
the new module. Reopen and regenerate a saved flowgraph after installing the new package.
Previously generated Python files do not update themselves.

The historical `examples/transients/bench/noise-collection.grc` and
`Pulsar_file_detection.grc` use the HDF5 recorder. Install DSPIRA software to obtain
that block when porting those older examples. They already require compatibility
work and are not part of the supported application test set.

The remaining research and DSPIRA packages install separate Python modules and
disjoint GRC definitions. Neither repository duplicates the moved block implementations.
Old tags and immutable commit references preserve the earlier combined releases.
