# NSF observing applications

These applications acquire spectra, record transient events, and combine both observing modes.
Variant numbers identify the original receiver or bandwidth configuration; they are not software release numbers.
For example, `24`, `30`, `60`, `80`, and `100` commonly indicate 2.4, 3, 6, 8, and 10 MHz.
Check each graph's parameters and receiver settings before observing.

## Launch an application

Install the research library using the [root instructions](../../README.md#installing-from-source).
From the repository root:

```sh
cd applications/nsf/configuration
python3 ../python/nsf_integrate_30.py
```

To edit and regenerate the matching graph from that same directory:

```sh
gnuradio-companion ../flowgraphs/nsf_integrate_30.grc
# Or generate without launching the receiver:
grcc -o ../python ../flowgraphs/nsf_integrate_30.grc
```

Run generated programs from `configuration`, even when Companion writes them beside the source graph.
The application reads and may update its `.conf` and `.not` files in the working directory.
Calibration samples and `nsf.qss` also live there.
Existing observation names, calibration filenames, and instrument settings remain unchanged.
The supplied settings describe earlier instruments; review them and use your own calibration before collecting data.

## Application catalog

The YAML graphs and saved Python programs are retained application sources.
Their presence does not certify every receiver, driver, or web interface with current GNU Radio.
The build tests the research library; hardware acquisition requires a separate observing test.

| Application | Source graph | Saved Python |
| --- | --- | --- |
| `nsf_detect_100` | [Graph](flowgraphs/nsf_detect_100.grc) | [Python](python/nsf_detect_100.py) |
| `nsf_detect_24` | [Graph](flowgraphs/nsf_detect_24.grc) | [Python](python/nsf_detect_24.py) |
| `nsf_detect_25` | [Graph](flowgraphs/nsf_detect_25.grc) | [Python](python/nsf_detect_25.py) |
| `nsf_detect_30` | [Graph](flowgraphs/nsf_detect_30.grc) | [Python](python/nsf_detect_30.py) |
| `nsf_detect_45` | [Graph](flowgraphs/nsf_detect_45.grc) | [Python](python/nsf_detect_45.py) |
| `nsf_detect_60` | [Graph](flowgraphs/nsf_detect_60.grc) | [Python](python/nsf_detect_60.py) |
| `nsf_detect_80` | [Graph](flowgraphs/nsf_detect_80.grc) | [Python](python/nsf_detect_80.py) |
| `nsf_detect_80_web` | [Graph](flowgraphs/nsf_detect_80_web.grc) | [Python](python/nsf_detect_80_web.py) |
| `nsf_integrate_100` | [Graph](flowgraphs/nsf_integrate_100.grc) | [Python](python/nsf_integrate_100.py) |
| `nsf_integrate_24` | [Graph](flowgraphs/nsf_integrate_24.grc) | [Python](python/nsf_integrate_24.py) |
| `nsf_integrate_25` | [Graph](flowgraphs/nsf_integrate_25.grc) | [Python](python/nsf_integrate_25.py) |
| `nsf_integrate_30` | [Graph](flowgraphs/nsf_integrate_30.grc) | [Python](python/nsf_integrate_30.py) |
| `nsf_integrate_31` | [Graph](flowgraphs/nsf_integrate_31.grc) | [Python](python/nsf_integrate_31.py) |
| `nsf_integrate_45` | [Graph](flowgraphs/nsf_integrate_45.grc) | [Python](python/nsf_integrate_45.py) |
| `nsf_integrate_60` | [Graph](flowgraphs/nsf_integrate_60.grc) | [Python](python/nsf_integrate_60.py) |
| `nsf_integrate_80` | [Graph](flowgraphs/nsf_integrate_80.grc) | [Python](python/nsf_integrate_80.py) |
| `nsf_integrate_80_web` | [Graph](flowgraphs/nsf_integrate_80_web.grc) | [Python](python/nsf_integrate_80_web.py) |
| `nsf_watch_100` | [Graph](flowgraphs/nsf_watch_100.grc) | [Python](python/nsf_watch_100.py) |
| `nsf_watch_100_no_gui` | [Graph](flowgraphs/nsf_watch_100_no_gui.grc) | [Python](python/nsf_watch_100_no_gui.py) |
| `nsf_watch_24` | [Graph](flowgraphs/nsf_watch_24.grc) | [Python](python/nsf_watch_24.py) |
| `nsf_watch_25` | [Graph](flowgraphs/nsf_watch_25.grc) | [Python](python/nsf_watch_25.py) |
| `nsf_watch_30` | [Graph](flowgraphs/nsf_watch_30.grc) | [Python](python/nsf_watch_30.py) |
| `nsf_watch_45` | [Graph](flowgraphs/nsf_watch_45.grc) | [Python](python/nsf_watch_45.py) |
| `nsf_watch_60` | [Graph](flowgraphs/nsf_watch_60.grc) | [Python](python/nsf_watch_60.py) |
| `nsf_watch_60_no_gui` | [Graph](flowgraphs/nsf_watch_60_no_gui.grc) | [Python](python/nsf_watch_60_no_gui.py) |
| `nsf_watch_80` | [Graph](flowgraphs/nsf_watch_80.grc) | [Python](python/nsf_watch_80.py) |
| `nsf_watch_80_no_gui` | [Graph](flowgraphs/nsf_watch_80_no_gui.grc) | [Python](python/nsf_watch_80_no_gui.py) |
| `nsf_watch_80_web` | [Graph](flowgraphs/nsf_watch_80_web.grc) | [Python](python/nsf_watch_80_web.py) |

## Historical variants

These XML graphs and older generated programs remain as design references.
They require conversion, dependency review, and testing before use with GNU Radio 3.10.
The Python-only Integrate 90 variant has no matching source graph in this repository.
Run any ported version from the same shared `configuration` directory.

| Application | Source graph | Saved Python |
| --- | --- | --- |
| `nsf_detect_45_histogram` | [Graph](flowgraphs/legacy/nsf_detect_45_histogram.grc) | [Python](python/legacy/nsf_detect_45_histogram.py) |
| `nsf_detect_60_histogram` | [Graph](flowgraphs/legacy/nsf_detect_60_histogram.grc) | Not retained |
| `nsf_detect_60_log` | [Graph](flowgraphs/legacy/nsf_detect_60_log.grc) | [Python](python/legacy/nsf_detect_60_log.py) |
| `nsf_detect_90` | [Graph](flowgraphs/legacy/nsf_detect_90.grc) | [Python](python/legacy/nsf_detect_90.py) |
| `nsf_integrate_90` | Not retained | [Python](python/legacy/nsf_integrate_90.py) |
| `nsf_watch_90` | [Graph](flowgraphs/legacy/nsf_watch_90.grc) | [Python](python/legacy/nsf_watch_90.py) |
| `nsf_watch_90_no_gui` | [Graph](flowgraphs/legacy/nsf_watch_90_no_gui.grc) | [Python](python/legacy/nsf_watch_90_no_gui.py) |

## Background

- [Observing notes](https://github.com/WVURAIL/radio-research-software/wiki/Nsf-gr-radio_astro)
- [NSF instrument figures](../../docs/images/nsf/)
- [LightWork memos](https://wvurail.org/lightwork/)
- [Former filenames](../../docs/file-map.json)

## Generation checks

Checked with GNU Radio 3.10.9.2, the research blocks, and available receiver block definitions.
Results match the original files before reorganization. Generation does not test hardware acquisition.

21 of 28 YAML graphs generated successfully in that environment.
The following graphs retain existing disconnected ports, unresolved expressions, or dependencies that require follow-up:

- [nsf_detect_80](flowgraphs/nsf_detect_80.grc)
- [nsf_detect_80_web](flowgraphs/nsf_detect_80_web.grc)
- [nsf_integrate_80](flowgraphs/nsf_integrate_80.grc)
- [nsf_integrate_80_web](flowgraphs/nsf_integrate_80_web.grc)
- [nsf_watch_80](flowgraphs/nsf_watch_80.grc)
- [nsf_watch_80_web](flowgraphs/nsf_watch_80_web.grc)
- [nsf_watch_80_no_gui](flowgraphs/nsf_watch_80_no_gui.grc)
