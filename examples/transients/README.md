# Transient simulation examples

Research notebooks, simulation data, and bench references from Andrew Dyck's 2019 transient project.
These belong to the radio research collection. Classroom applications are maintained separately.

## Notebooks

- [Pulsar simulation](pulsar-simulation.ipynb): pulse generation, dispersion, channelization, and a dispersion-measure search.
- [Background comparison](pulsar-background-comparison.ipynb): an alternative noise-subtraction method with correlation outputs.
- [Search development](pulsar-search-development.ipynb): earlier peak-search and averaging heuristics for comparison.

Use Python 3, Jupyter, NumPy, SciPy, and Matplotlib.
Start Jupyter in this directory. Outputs go to generated/; the original samples in data/ stay untouched.
The notebooks simulate high-rate signals and can allocate large arrays. Inspect sample counts before executing them.

The migration changed local paths and integer sample counts, and cleared old outputs.
It did not validate the research algorithms or execute the full simulations.
Dependencies remain unpinned; random seeds and the original environment were not recorded.
Circular shifts, peak-selection heuristics, and noise estimates need review before scientific use.
The maintained C++ dedispersion and detect blocks are separate implementations, not drop-in reproductions of these notebooks.

## Reference data

The six files in data/ preserve their original bytes and filenames.
The filename parameters are historical labels, not independently verified metadata.
Notebook parameters changed during development, so rerunning them need not reproduce these samples.
The .bin and _noise.bin writers use interleaved signed 16-bit real and imaginary samples.
Later notebooks write _integrated_FFT.bin, _dispersed.bin, and _corr.bin as float32 arrays.
The earlier search notebook instead writes integrated spectra as int16.
The stored files have no headers; confirm layout, endianness, and producing version before analysis.
The _SNR.bin producer was not identified during consolidation.
See source-manifest.json for byte counts and checksums.

## Notes and bench material

- [Original simulation explanation](simulation-notes.md)
- [Original bench procedure](bench-notes.md)
- [Plot descriptions](plot-notes.md)
- [Existing diagnostic plots](../../docs/transient_documentation/)
- [Existing bench examples](../../docs/transient_benchtesting/)
- [Full detection flowgraph](dual-stream-detection.grc)

The original notes describe the older experiment and may reference its former paths.
The full detection flowgraph uses retired GNU Radio 3.7 blocks and absolute file paths.
It is retained as a design reference; it has not been ported or runtime-tested.
Use the current library for supported blocks. Do not install the retired OOT scaffolding alongside it.

Original credits and notices are retained in CONTRIBUTORS.md and SOURCE-NOTICE.txt.
See LICENSE.txt and notices within individual files for licensing.

The imported dual-stream graph retains separate signal and noise processing paths.
The existing Full_detection_Flowgraph.grc uses a different shared-block variant and remains unchanged.
