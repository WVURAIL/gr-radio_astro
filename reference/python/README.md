# Earlier Python utilities

- [system_temperature.py](system_temperature.py): an earlier hot/cold-load calibration helper, formerly `tsys.py`.
- [chrony_status.py](chrony_status.py): a chrony status helper, formerly `getchrony.py`.

These utilities were not installed or imported by the research package before this move.
Their implementations are unchanged and are not covered by the package QA suite.
The calibration helper still expects the older top-level `radioastronomy` import.
The clock helper requires a suitable chrony service and host configuration.
