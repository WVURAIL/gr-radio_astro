# Buckhannon RFI field test, 2018

Pranav Sanghavi recorded this historical radio-interference field test in Buckhannon, West Virginia.
The report describes a clover antenna, a 400–800 MHz receiver chain, and comparisons with a laboratory load.
It contains plotted measurements; the original raw measurement files were not included in the source repository.

## Read the record

- [Original report (PDF)](report.pdf)
- [Editable LaTeX source](report.tex) and [research diary style](research-diary.sty)
- [Signal levels](../../images/rfi/buckhannon-field-test-2018/signal-levels.png) and [detail plot](../../images/rfi/buckhannon-field-test-2018/signal-levels-detail.png)
- [Original paths and checksums](provenance.json)

The document labels the experiment **March 29, 2018**.
Its original directory was `2018_05_18`, and the PDF header says May 25, 2018.
These dates are retained as recorded; they are not treated as interchangeable.
The report describes that experiment, not current instrument performance or a DSPIRA classroom procedure.

## Sources and attribution

Imported from [WVURAIL/memos at `8da9c9a`](https://github.com/WVURAIL/memos/tree/8da9c9a522b3934222913d00c295ffaf49cda47d/2018_05_18).
The PDF and both plot files retain their original bytes.
The LaTeX changes only update the renamed style package and plot paths.
The style changes only update its package name.
Source text, author credits, component values, and plotted measurements are otherwise unchanged.

Run any LaTeX build from this directory so the relative image paths resolve.
The historical source uses CircuitikZ, PSTricks, and other packages listed in the style file.
It also uses `\today`, so rebuilding changes the header date.
The original PDF remains the authoritative record of the historical rendering.
No new LaTeX build was performed for this import.

The diary template credits Mikhail Klassen and Pranav Sanghavi.
Its style file retains its [CC BY-SA 3.0 notice](https://creativecommons.org/licenses/by-sa/3.0/).
The source repository supplied no separate license for the report or plots.
This historical import does not assign them the software repository's GPL license.
