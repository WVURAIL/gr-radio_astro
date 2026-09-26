# Vector demonstrations

Vector displays, complex signals, and alternative web interfaces.

Review the graph dependencies before generating or running an example. Receiver examples require suitable hardware.

| Example | Files | Format |
| --- | --- | --- |
| `nsf_ping` | [Graph](legacy/nsf_ping.grc) · [Python](legacy/nsf_ping.py) | Legacy XML; needs porting |
| `vector_demo_complex` | [Graph](legacy/vector_demo_complex.grc) | Legacy XML; needs porting |
| `vector_demo` | [Graph](vector_demo.grc) · [Python](vector_demo.py) | YAML |
| `vector_demo_bokeh` | [Graph](vector_demo_bokeh.grc) | YAML |
| `vector_demo_complex_2` | [Graph](vector_demo_complex_2.grc) · [Python](vector_demo_complex_2.py) | YAML |
| `vector_demo_web` | [Graph](vector_demo_web.grc) · [Python](vector_demo_web.py) | YAML |

The historical ping experiment is also retained under `legacy`.

[Return to the example catalog](../README.md).

## Generation checks

Checked with GNU Radio 3.10.9.2, the research blocks, and available receiver block definitions.
Results match the original files before reorganization. Generation does not test hardware acquisition.

2 of 4 YAML graphs generated successfully in that environment.
The following graphs retain existing disconnected ports, unresolved expressions, or dependencies that require follow-up:

- [vector_demo_web](vector_demo_web.grc)
- [vector_demo_bokeh](vector_demo_bokeh.grc)
