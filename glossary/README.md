# Glossary

A small local knowledge graph that is this repository's source of truth for definitions.

**Two node types, one kind of edge.** A `gl:Source` is a text or medium (a standard, a paper, a video series, this tutorial). A `gl:Term` is a load-bearing word. A **definition is an edge** (`gl:Definition`) from a source to a term, because the same term can be defined slightly differently by different texts. Terms carry no definition of their own. Keep the number of sources (N) small and the number of terms (M) modest; the count of definitions grows as at most N x M and is expected to be sparse (`python -m glossary stats` reports the density).

**Canon first.** Definitions come from canonical sources. The tutorial appears as a source only to record contextual *refinements* that narrow or clarify a canonical definition, so learners are never taught something misaligned with canon. A tutorial edge says what it refines (`gl:refines`); a departure is `gl:differsFrom`, and `check` fails on one unless a human approved it (`gl:approvedBy`, with `gl:approvalNote`).

**Only a human confirms.** Agents propose (`gl:status gl:proposed`). Only Z sets `gl:confirmed` and `gl:confirmedBy`. The **tutorial definition** of a term is not stored on the term: it is a SPARQL view (`queries/tutorial_definitions.rq`, CLI `tutorial`) that picks, per term, the confirmed edge from the best-ranked source. Each source carries a `gl:rank` (the citation order; lower wins: tutorial refinements 0, SEBoK 1, SysML 2, API 3, KerML 4, Hawkins 5, Åström 6, Sutton 7, Douglas 8). `gl:preferred` breaks a tie between edges of the same source only. `python -m glossary tutorial --proposed` previews the view as if every proposed edge were confirmed. `render` uses the selected edge's `gl:gloss`, or its text when it is at most 240 characters.

**Every claim is checkable.** Each canonical edge carries a short verbatim `gl:quote` and, for file sources, the `gl:pdfPage` where it appears. `verify-sources` checks each registered file's sha256 and that each quote is on its page. Douglas (video) quotes are copied from the transcripts as read and cannot be checked mechanically.

## Use

```bash
uv run python -m glossary lookup mechanism        # all definitions of a term
uv run python -m glossary compare "logical architecture"
uv run python -m glossary terms | sources | stats
uv run python -m glossary where sebok             # terms one source defines
uv run python -m glossary sparql terms            # a named query, a .rq file, or inline SPARQL
uv run python -m glossary check                   # SHACL + integrity + gloss drift
uv run python -m glossary verify-sources          # needs the originals in sources/local/
uv run python -m glossary render                  # write glosses between <!-- gloss:ID --> markers; regenerate docs/glossary.md
```

Every command takes `--json`. `check` passes in a fresh worktree or CI without the source PDFs (hashes and quotes are verified only for files that are present).

## Getting the source files

The seven file sources in `sources/sources.ttl` are copyrighted, so the originals are not in the repository. `sources/local/` is gitignored; you fetch the files once and place them there under the exact filename in the first column. Each row gives the first 12 hex digits of the registered `gl:sha256` (the full hash is in `sources/sources.ttl`).

| Registered filename | What it is | Where to get it | sha256 (first 12) |
|---|---|---|---|
| `sysml-v2.0-language-formal-26-03-02.pdf` | OMG SysML v2.0, Part 1: Language Specification, formal/2026-03-02 | OMG specification page <https://www.omg.org/spec/SysML/2.0/>, row "Specification - Language", formal/26-03-02; its PDF link is <https://www.omg.org/spec/SysML/2.0/Language/PDF>. Match by sha256 | `46e6c0476a6f` |
| `kerml-1.1-beta2.pdf` | OMG Kernel Modeling Language (KerML) 1.1 Beta 2 (older than the SysML v2.0 spec that builds on it) | OMG KerML page <https://www.omg.org/spec/KerML/> lists only formal/26-03-01, not this Beta 2 draft; no public link to Beta 2 was confirmed, so obtain the OMG KerML 1.1 Beta 2 PDF and match by sha256 | `e8b7f33d9dac` |
| `sysml-api-services-v1.0-formal-26-03-04.pdf` | OMG Systems Modeling API and Services v1.0, formal/2026-03-04 | OMG specification page <https://www.omg.org/spec/SystemsModelingAPI/>, formal/26-03-04; its PDF link is <https://www.omg.org/spec/SystemsModelingAPI/1.0/PDF> | `1a93ffb92145` |
| `sebok-v2.14.pdf` | Guide to the Systems Engineering Body of Knowledge (SEBoK), version 2.14 | SEBoK <https://sebokwiki.org/wiki/Download_SEBoK_PDF> ("Download SEBoK PDF") | `251668f0ed4e` |
| `astrom-murray-fbs-2e-v3.1.5.pdf` | Astrom and Murray, Feedback Systems, 2nd ed., electronic edition v3.1.5 (24 Jul 2020) | The authors' book page <https://fbswiki.org/wiki/index.php/Main_Page> ("Complete PDF (24 Jul 2020)") | `e2fa6992fe5a` |
| `hawkins-2011.pdf` | Hawkins, Kelly, Knight, Graydon, "A New Approach to Creating Clear Safety Arguments", Springer 2011, the book-chapter PDF, DOI 10.1007/978-0-85729-133-2_1 | <https://doi.org/10.1007/978-0-85729-133-2_1> (Springer; download the chapter PDF in a browser) | `53af633615db` |
| `sutton-barto-rl-2e.pdf` | Sutton and Barto, Reinforcement Learning: An Introduction, 2nd ed. (authors' PDF) | <http://incompleteideas.net/book/RLbook2020trimmed.pdf> (the "trimmed" file) | `fd1751be1a2f` |

Procedure:

1. Put each file, or a symlink to it, in `glossary/sources/local/` under the exact registered filename. Symlinks work: `verify-sources` hashes through them.
2. Run `uv run python -m glossary verify-sources`. Success prints `verify-sources: ok` and exits 0.
3. If it reports `source-absent`, the filename is wrong or missing. If it reports `source-hash`, you have a different edition or print of the document: run `shasum -a 256 <file>` and compare it with the table, and fetch the right one. The hash is what counts, not where the file came from.
4. Never commit these files. `check` (not `verify-sources`) is the command CI and fresh worktrees run, and it only warns for absent files; `verify-sources` is the strict check for a machine that holds the originals.
5. Hawkins: the registered file is the Springer book-chapter PDF. A browser download is named like `chp:10.1007%2F978-0-85729-133-2_1.pdf`; rename it to `hawkins-2011.pdf`. An author's manuscript copy exists elsewhere, but its hash does not match.
6. Sutton and Barto: use the authors' `RLbook2020trimmed.pdf`. The same site's `RLbook2020.pdf` and `RLbook2018.pdf` have different hashes and fail. The site's `https` endpoint has a self-signed certificate (so `curl` and some browsers refuse it); the plain `http` link above works, and the sha256 is what guarantees you have the right file.

## Layout

```
vocabulary/glossary-core.ttl   classes and properties
shapes/glossary.shapes.ttl     SHACL cardinality, datatype, pattern
sources/sources.ttl            the source register (sha256 and local path, or URL and date, or commit)
sources/notes/                 our own notes on the sources
sources/local/                 the originals (gitignored; copyrighted)
terms/terms.ttl                term nodes only
definitions/<source>.ttl       one file of edges per source
queries/*.rq                   named SPARQL queries (each with an explicit ORDER BY)
check.py, render.py, cli.py    integrity checks, generated glosses, the command line
tests/                         pytest, run from the repo root
```

## Adding to the graph

1. **A source:** copy the original into `sources/local/`, add a `gl:Source` to `sources/sources.ttl` with its `gl:sha256` and `gl:localPath` (or `gl:url` and `gl:retrievedOn` for a video, `gl:commit` for a repository).
2. **A term:** add a `gl:Term` to `terms/terms.ttl` (label only).
3. **A definition edge:** add a `gl:Definition` to `definitions/<source>.ttl` with `gl:source`, `gl:term`, a paraphrase in `gl:text`, a short `gl:quote`, `gl:pdfPage`, `gl:locator`, and `gl:status gl:proposed`. Run `verify-sources`.
4. Run `check`. Files must stay in canonical Turtle: load and save through `glossary.graph.save_graph`.
5. Ask Z to confirm. Do not set `gl:confirmed` yourself.

Do not add a term without a canonical source. If a word has no canonical definition, it is not ready to be a glossary term.

## Lint

`uv run python -m glossary lint [--json] [--baseline FILE] [--write-baseline FILE]` scans learner-facing content (markdown cells of `chapters/**/*.ipynb`, `chapters/**/*.md`, `docs/**/*.md` except the generated `docs/glossary.md` and everything under `docs/superpowers/`) against the rules in `lint_rules.toml`. Each rule has `id`, `regex` (case-insensitive), `message`, `why`, `severity` (`error` or `warn`) and `scope` (`learner`), plus an optional boolean `ignore_code` (default `false`; any other type exits 2). A rule with `ignore_code = true` is matched against a copy of each unit in which fenced blocks (` ``` ` and `~~~`) and inline code spans (including double-backtick spans) are replaced by spaces of equal length, newlines kept, so line numbers are unchanged; rules without it see the text as written. A backtick-fenced MyST directive (for example ```{note}) is masked as a fenced block, so prose inside it is invisible to `ignore_code` rules. A malformed rules file exits 2. Each hit reports file, cell (notebooks), line, rule, matched text and severity, followed by per-rule counts. Without `--baseline` the exit code is 1 if any error hit exists. `--write-baseline` saves the current hits; with `--baseline`, hits matching a saved entry by file, rule and matched text (not line) are "baselined", the rest "new", and only a new error exits 1.

The baseline is count-based: a key (file, rule, matched text) is baselined only up to the number of times it appears in the baseline file (duplicates count), so a further identical hit in that file is new. Fewer hits than baselined is fine (exit 0). Rules-file and baseline errors (non-string fields, `rule` not a list of tables, zero rules, unknown top-level key, duplicate ids, empty regex, unwritable baseline path) exit 2 with a message naming the problem.
