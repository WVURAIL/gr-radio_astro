# Branch history and legacy migration

This record summarizes the repository review completed on 2026-08-20. GitHub
activity and the recovered commit graph accounted for all 25 branches that
existed before the review. No branch tip or original commit was discarded.

The 2026 maintenance on `main` is one commit whose parent is the unchanged
pre-maintenance tip
[`1112b05`](https://github.com/WVURAIL/gr-radio_astro/commit/1112b05de113738daa50fa7897b7f95733279150).

## Retained branches

Four branches remain because they are the maintained line or contain work that
still merits separate review:

| Branch | Tip at review | Status |
|---|---|---|
| `main` | `1112b05` before the single maintenance commit | Maintained line |
| `gr310` | [`320aed9`](https://github.com/WVURAIL/gr-radio_astro/commit/320aed944146ecb7bcaf82fccdd781ec869794b8) | GNU Radio 3.10 development history |
| `lightning_dev` | [`4349a67`](https://github.com/WVURAIL/gr-radio_astro/commit/4349a6794a039e8b1f0a4b63f4a21fb653d2110a) | Unmerged lightning-development work |
| `systemp_calibration` | [`937617c`](https://github.com/WVURAIL/gr-radio_astro/commit/937617c50adf1e4715e8afd4f4a65afb796e22d6) | Unmerged calibration work |

## Deleted branches

The other 21 branch tips are recoverable from `main`, an existing pull-request
ref, or an annotated tag:

| Former branch | Exact tip | Durable destination |
|---|---|---|
| `correlate` | [`82ee5ba`](https://github.com/WVURAIL/gr-radio_astro/commit/82ee5bad0ee0755e7d2e8832ea61beb11d9adda2) | Merged into `main`; pull request #3 |
| `dedisperse` | [`887e94d`](https://github.com/WVURAIL/gr-radio_astro/commit/887e94dfb34783a065bb6b9febfe14650ca4b065) | Tag `v2019.10-dedisperse` |
| `detect` | [`c52fc30`](https://github.com/WVURAIL/gr-radio_astro/commit/c52fc3075dcc6f4dab2b7bfeb806e60d925961be) | Tag `legacy-detect-2019` |
| `gr310-old` | [`6c21972`](https://github.com/WVURAIL/gr-radio_astro/commit/6c21972a86cf727a139d3d9d1469159247b73d8a) | Tag `legacy-gr310-prototype-2021` |
| `gr37-maint` | [`d668682`](https://github.com/WVURAIL/gr-radio_astro/commit/d6686827e4c1b8d315c3b2ffe83b9eb429a4c9ba) | Tag `v2021.07-gr37` |
| `gr38` | [`e163d99`](https://github.com/WVURAIL/gr-radio_astro/commit/e163d9978d68be3921524f8c49fad2871984dc6a) | Compatibility tag `gr38` |
| `gr38-maint` | [`1390807`](https://github.com/WVURAIL/gr-radio_astro/commit/1390807ca1748973ec7b570fe8be2575aa52392e) | Ancestor of `main` |
| `gr38_dev` | [`3761bb6`](https://github.com/WVURAIL/gr-radio_astro/commit/3761bb698b3ecefe513585f22d796599957ed745) | Merged into `main`; pull request #35 |
| `gr38_dev_ejk` | [`5d4d77b`](https://github.com/WVURAIL/gr-radio_astro/commit/5d4d77b9af7815f57ebe9807ef7314935099f3e7) | Merged into `main`; pull request #36 |
| `hdf5_saveoption` | [`f29282f`](https://github.com/WVURAIL/gr-radio_astro/commit/f29282fbc504001ce34c7362910cd4cbd44ba748) | Merged into `main`; pull request #7 |
| `integrate` | [`176e0b8`](https://github.com/WVURAIL/gr-radio_astro/commit/176e0b8818dae9bde681c5bd34497f795ad66e60) | Merged into `main`; pull request #21 |
| `jmakous-patch-1` | [`bc1b54f`](https://github.com/WVURAIL/gr-radio_astro/commit/bc1b54f0e96ae951b87ac2536c01b872313e54f5) | Merged into `main`; pull request #11 |
| `jmakous-patch-2` | [`d957446`](https://github.com/WVURAIL/gr-radio_astro/commit/d957446bd1b5719a7b32440a6118d6d071df90c9) | Merged into `main`; pull request #12 |
| `jmakous-patch-3` | [`3ebd1eb`](https://github.com/WVURAIL/gr-radio_astro/commit/3ebd1ebb513c8e797555a57dba2503a91b94ae2c) | Merged into `main`; pull request #15 |
| `mac_fixes` | [`b247b78`](https://github.com/WVURAIL/gr-radio_astro/commit/b247b780884d81c0e951b740127bf08b7d495b77) | Merged into `main`; pull request #6 |
| `master` | [`5304ee1`](https://github.com/WVURAIL/gr-radio_astro/commit/5304ee189cfb31255bb78e1eb3d3a7af343aa524) | Pull request #34; incorporated in the GNU Radio 3.7 release line |
| `moving_average` | [`d002571`](https://github.com/WVURAIL/gr-radio_astro/commit/d0025715c0ce16c4f569cc1127eca13cd28511bb) | Merged into `main`; pull request #24 |
| `new_examples` | [`8c6379b`](https://github.com/WVURAIL/gr-radio_astro/commit/8c6379bf822f6c80cd8882c2419eda626cdeb211) | Tag `examples-2018` |
| `spectrometers_2019` | [`a57d78a`](https://github.com/WVURAIL/gr-radio_astro/commit/a57d78a0dbade89e320fe547f24ea20baf93bb4a) | Merged into `main`; pull request #18 |
| `spectrometers_2020` | [`7f021d3`](https://github.com/WVURAIL/gr-radio_astro/commit/7f021d371120fe6398b7c405972d4ec745dc13aa) | Merged through pull request #23; the same tip appeared in closed pull request #22 |
| `watch` | [`cb18878`](https://github.com/WVURAIL/gr-radio_astro/commit/cb18878429b45582c750a172e7d0798c79343593) | Merged into `main`; pull request #5 |

The three new archival tags retain tips that were not otherwise exact public
refs. `detect` has the same patch as a later `main` commit. The functional
changes from `gr310-old` were carried forward or superseded. The two unique
`gr38` CMake snapshots hard-code obsolete MacPorts and Python paths, while its
plotting fix reached `main`. The `gr38` tag deliberately retains the former
branch name because older DSPIRA installation instructions use
`git checkout gr38`.

## Migration from gr-dspira

The archived [`gr-dspira`](https://github.com/WVURAIL/gr-dspira) repository was
also compared file by file:

- Its `systemp_calibration` implementation was transferred by the original
  author in
  [`ee22815`](https://github.com/WVURAIL/gr-radio_astro/commit/ee2281583fbbb1edd70f7ef9aee71f4299e6dd7d)
  and subsequently evolved in this repository.
- Its HDF5 and spectrometer concepts are present in maintained or later work
  here.
- Its unique spectrometer-display, spectrometer-output, and harmonic-generator
  files are incomplete historical experiments, not missing production blocks.
- Its Fourier demo is preserved both in that archive and in the published
  DSPIRA lesson materials.

No additional code or data needed to be migrated from `gr-dspira`.
