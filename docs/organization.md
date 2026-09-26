# Repository organization

## Names and locations

- Use lowercase names separated by hyphens for documents, images, and folders.
- Use lowercase names separated by underscores for Python files and matching application flowgraphs.
- Keep installed module names, public headers, and block identifiers compatible with existing users.
- Keep standard build filenames such as `CMakeLists.txt`, `README.md`, and `LICENSE`.
- Keep observation timestamps and instrument configuration filenames when software or measurement records rely on them.
- Store figures under `docs/images`, grouped by topic.
- Store application source graphs and generated Python in separate folders.
- Keep older experiments clearly labeled, together with their compatibility notes.

The NSF settings retain their existing observation names.
Applications read those settings, calibration samples, and the stylesheet from their working directory.
Follow the [launch instructions](../applications/nsf/README.md) to select that directory.
Application filenames and YAML graph IDs now agree, so regeneration produces consistently named Python files.
Legacy XML graph IDs remain unchanged; those experiments still need porting.

## File moves

[file-map.json](file-map.json) maps each former path to its current location.
It also records the source revision and removed, unused build scaffolding.
Use that revision when following an old raw-file link or reproducing an earlier checkout.
Repository file moves do not create GitHub redirects for individual files.

Identical figures now share one file. Their former paths map to the same destination.
Distinct bench graphs and earlier application variants remain available.
The unused flat Python build scaffold and empty application install target were removed.
The active package and bindings remain under `python/radio_astro`.

## Scientific records

The sample spectra, calibration files, binary datasets, and retained figures keep their original bytes.
The transient source manifest retains its original paths and checksums as an import record.
Consult the file map for current locations.
The shorter binary filenames do not assert newly verified metadata or sample formats.
The [transient catalog](../examples/transients/README.md) explains the known data-format limitations.

Credits, licenses, publication identifiers, and the public `gnuradio.radio_astro` API remain unchanged.

Run `python3 scripts/check_repository.py` from the repository root to check catalogs, destinations, and application IDs.
The build workflow runs this check alongside the existing software checks.
