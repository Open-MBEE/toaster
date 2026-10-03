---
name: tutorial-glossary
description: How to use and extend the glossary knowledge graph (sources, terms, definition edges, kinds, the tutorial-definition view, confirmation and refinement rules, CLI, limits). Look a term up before defining it.
---

# Tutorial glossary

`glossary/` is the local source of truth for definitions. It is a **bipartite graph**: nodes are **sources** and **terms**, and a **definition is an edge**, because one term can be defined a little differently by different texts. Keep sources few (N about 10) and terms modest (M about 50, load-bearing only); definitions can grow as N times M, so add an edge only when it is needed. `glossary/README.md` has the file layout.

## Look up before you define or use a term

```
uv run python -m glossary lookup mechanism      # every edge: source, locator, quote, status, refines/differsFrom
uv run python -m glossary tutorial mechanism    # what the tutorial uses: idea, formal semantics, story, own refinement
uv run python -m glossary compare logical-architecture
uv run python -m glossary terms | sources | where sysml | stats
uv run python -m glossary sparql lookup_all --json     # named or inline SPARQL, deterministic order
uv run python -m glossary lint [--baseline FILE]        # vocabulary rules over learner content (rules in glossary/lint_rules.toml)
```

Every command takes `--json`. Rule: if a term is in the glossary, use its tutorial definition and cite the term id (`term-mop`). If it is not and the work depends on it, propose an edge (below); do not invent a definition in prose.

## The four kinds of source

Sources are not ranked against each other. Each supplies a **kind** of definition, and the kinds complement each other.

| `gl:kind` | Sources | Role |
|---|---|---|
| `conceptual` (idea) | SEBoK, Hawkins, Åström and Murray, Sutton and Barto | What the concept means |
| `formal` | SysML v2 language spec, API spec, KerML | Checkable semantics |
| `didactic` (story) | Douglas | Analogy and example |
| `bridge` | This tutorial | Our refinements |

`tutorial TERM` returns the best confirmed edge of each kind (`queries/tutorial_definitions.rq`). `gl:rank` orders sources of the *same* kind only; `gl:preferred` breaks a tie between edges of the same source (for example SEBoK's two senses of *behavior*). `check` fails on an ambiguity within a kind. The one-line gloss used in AGENTS.md and skills comes from the bridge edge if there is one, else the idea, else the formal semantics, else the story.

## Rules

1. **Only a human confirms.** Agents propose (`gl:status gl:proposed`). Only Z sets `gl:confirmed` and `gl:confirmedBy`. `check` rejects an agent name as `confirmedBy`. A proposed edge shows in `tutorial --proposed` (a preview) but never in the confirmed view or a rendered gloss.
2. **Canonical first; refine only where needed.** A tutorial edge (`src-tutorial`) may `gl:refines` another edge to narrow or clarify it, and only the tutorial source may. It must not contradict its parents. `gl:differsFrom` (a departure from the same term's edge) needs `gl:approvedBy` and `gl:approvalNote`; the only approved one is *logical architecture* versus SEBoK (DL-015).
3. **Locators and quotes are checkable.** Each canonical edge has a `gl:locator` and, for file sources, a short `gl:quote` (at most 300 characters) with `gl:pdfPage`. `verify-sources` finds the quote on that page. Douglas locators are `Part N, m:ss` and were read from transcripts. Never quote at length; paraphrase in `gl:text`. **Exception (Z, 2026-09-26, DL-026):** a single definitional sentence of at most 200 characters may reproduce canonical wording in `gl:text` or `gl:gloss` when the source is attributed on the page (the Sources list) and the wording is not placed in quotation marks as if verbatim. Longer text is paraphrased. `gl:quote` is never rendered on the public page.
4. **Glosses are at most 240 characters.** A `gl:gloss` is used verbatim by `render`; without one, `gl:text` is used if it fits.
5. **Change definitions only through the graph**, then `check`, then `render`. Text between `<!-- gloss:ID -->` and `<!-- /gloss -->` is generated; never edit it by hand. Learner-facing pages and the skills cite terms, they do not redefine them.
6. **Builder-facing lenses are not sources or terms** (Tall's three worlds, optimization and control, generalized dynamical systems). Implementations (OpenSysML, sysml-toolkit) are toolchain, not sources.

## Adding a term, source or edge

- **Term:** add a node to `glossary/terms/terms.ttl` (`glid:term-<slug>`, `gl:label`, `gl:loadBearing true` only if a Foundations paragraph or skill relies on it). A term with no edge is an orphan and fails `check`.
- **Source:** add to `glossary/sources/sources.ttl` with `gl:kind`, `gl:rank`, and either a file (`gl:sha256`, `gl:localPath` under the gitignored `glossary/sources/local/`) or a non-file source (`gl:url` and `gl:retrievedOn`, or `gl:commit`). Keep N small; prefer an edge in an existing source.
- **Edge:** add to `glossary/definitions/<source>.ttl` as `glid:def-<source>--<term>` with `gl:source`, `gl:term`, `gl:text`, `gl:locator`, `gl:status gl:proposed`, and `gl:quote` plus `gl:pdfPage` for files.
- Write Turtle through the `glossary.graph.save_graph` helper (canonical, byte-deterministic), not by hand, or `check` will report drift. Then run `check`. On Z's machine also run `verify-sources` (where to get each source file and where to put it: "Getting the source files" in `glossary/README.md`).
- Tell the ACE (or Z) what you proposed; they triage and Z confirms. Log it in `decisions/log.md` if it changes a confirmed definition (only Z can change one).

## Worktree and CI safety

`check` passes in a fresh worktree or CI where the gitignored source PDFs are absent: it verifies hashes and quotes only for files that are present and warns for absent ones. `verify-sources` is the strict check and needs the originals in `glossary/sources/local/`.

## Limits

- Not a general knowledge base: load-bearing terms only, and the density D/(N x M) should stay low (`stats`).
- `lookup` is text and provenance; it does not judge whether prose uses a term correctly. That check belongs to reviewers, who use `lookup` instead of memory.
