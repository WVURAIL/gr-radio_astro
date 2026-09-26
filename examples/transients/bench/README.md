# Historical transient benches

These GNU Radio 3.7-era graphs are design references and require porting before current use.
Their original parameters and absolute data paths remain unchanged.

| File | Purpose |
| --- | --- |
| [pipeline-comparison.grc](pipeline-comparison.grc) | Larger comparison bench, formerly `Benchtesting.grc` |
| [spectrometer-bench.grc](spectrometer-bench.grc) | Smaller spectral bench, formerly `bench_testing.grc` |
| [full-detection-flowgraph.grc](full-detection-flowgraph.grc) | Shared-block detection variant |
| [dual-stream-detection.grc](dual-stream-detection.grc) | Separate signal and noise processing paths |
| [noise-collection.grc](noise-collection.grc) | Noise recording experiment |
| [pulsar-file-detection.grc](pulsar-file-detection.grc) | File-based pulsar detection experiment |
| [legacy_bench.py](legacy_bench.py) | Original Python 2-era generated program |
| [bench-development.ipynb](bench-development.ipynb) | Original trial-and-error notebook |

The two detection graphs differ; both remain available.
The six XML graphs depend on older block definitions and may contain disconnected or unresolved ports after conversion.
The notebook and generated program preserve the original experiment, including its environment assumptions.
Read the [bench notes](../../../docs/transients/bench.md) and [block migration](../../../docs/dspira-block-move.md) before adapting them.
