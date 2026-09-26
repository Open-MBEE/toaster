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

`uv run python -m glossary lint [--json] [--baseline FILE] [--write-baseline FILE]` scans learner-facing content (markdown cells of `chapters/**/*.ipynb`, `chapters/**/*.md`, `docs/**/*.md` except the generated `docs/glossary.md`) against the rules in `lint_rules.toml`. Each rule has `id`, `regex` (case-insensitive), `message`, `why`, `severity` (`error` or `warn`) and `scope` (`learner`); a malformed rules file exits 2. Each hit reports file, cell (notebooks), line, rule, matched text and severity, followed by per-rule counts. Without `--baseline` the exit code is 1 if any error hit exists. `--write-baseline` saves the current hits; with `--baseline`, hits matching a saved entry by file, rule and matched text (not line) are "baselined", the rest "new", and only a new error exits 1.

The baseline is count-based: a key (file, rule, matched text) is baselined only up to the number of times it appears in the baseline file (duplicates count), so a further identical hit in that file is new. Fewer hits than baselined is fine (exit 0). Rules-file and baseline errors (non-string fields, `rule` not a list of tables, zero rules, unknown top-level key, duplicate ids, empty regex, unwritable baseline path) exit 2 with a message naming the problem.
