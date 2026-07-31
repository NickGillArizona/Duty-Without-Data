# Citation Guide

How to cite this archive, a single file within it, or a generated artifact, so that the
cited content remains fixed to one repository state. The archive's formal title is
**Duty Without Data: Research and Replication Archive** (see [`CITATION.cff`](CITATION.cff)).

## Which object to cite

| You are citing | Use |
|---|---|
| The article | The journal citation shown in the [manuscript](manuscript/Duty_Without_Data.md) |
| The archive as a whole | The repository URL together with the full commit SHA you consulted |
| One file or passage | A commit-pinned permalink, with a line range where useful |
| A number that the Note prints | The claim's row in [`article/CLAIMS_LEDGER.csv`](article/CLAIMS_LEDGER.csv), plus the artifact that row identifies |

## Whole-archive citation

Cite the author, the archive's formal title, the repository URL, and the full
forty-character commit SHA of the state you consulted: author, then title, then
`https://github.com/NickGillArizona/Duty-Without-Data`, then the SHA in a trailing
parenthetical. Citation metadata is in [`CITATION.cff`](CITATION.cff); the release
commit SHA is inserted at release.

## Single-file and line-range citation

A branch URL (`.../blob/main/...`) points to a mutable file state. To cite content that
cannot change under you, replace `main` in the URL with the full commit SHA, then append
the repository-relative path and, where it helps, a line range in GitHub's
`#L<start>-L<end>` form.

On GitHub, pressing `y` on any file view rewrites the address bar to the commit-pinned
form of the page you are reading — the simplest way to obtain a stable citation URL.

## Generated artifacts

Files under `results/` that a script regenerates are convenience representations. Cite
the canonical artifact a claim rests on — the one named in `CLAIMS_LEDGER.csv` or
[`replication/REPRODUCE.md`](replication/REPRODUCE.md) — rather than a regenerable export, and pin the commit as
above.

## Raw-footnote-label convention

A reference to "fn N" anywhere in this archive uses the manuscript's raw label `[^N]`,
not GitHub's rendered footnote number. [`article/FOOTNOTE_INDEX.md`](article/FOOTNOTE_INDEX.md) routes
each repository-pointing footnote to its exact file and section.

## Citing the article and the archive together

Cite the article for the legal argument and printed findings; cite the archive for
data, code, instruments, and validation records. The archive does not establish the
truth of a legal proposition or the accuracy of a model classification; what a green
release gate does and does not establish is documented in [`replication/GATES.md`](replication/GATES.md).
