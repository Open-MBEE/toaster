---
name: tutorial-supporting-pages
description: docs/ page inventory, reproducibility statement structure, fork-and-exercise workflow, and contributor guide scenarios.
---

# Tutorial Supporting Pages

## Page inventory

| File | Purpose |
|---|---|
| `docs/index.md` | Opening navigation + didactic purpose statement |
| `docs/setup.md` | Provisioning steps + fork-and-exercise workflow |
| `docs/glossary.md` | SysML v2 terms introduced in the tutorial |
| `docs/references.md` | Citations: Brian Douglas video, Hawkins 2011, opensysml, mystmd |
| `docs/reproducibility.md` | Closing reproducibility statement (populated from build manifest) |
| `docs/contributor.md` | Maintainer guide (4 update scenarios) |

## docs/setup.md — fork-and-exercise section

```
## Fork and exercise

Fork the repo, provision the environment (see above), then:

1. Read the worked example: open a chapter notebook in `chapters/` and run all cells.
2. Open the parallel exercise: `exercises/ch{N}/exercise.ipynb`.
3. The exercise asks you to apply the same construct or operation to a different part of the toaster.
   The only tools you need are the ones introduced up to that chapter.
4. The `exercises/` notebooks are blank workspaces — they are not pre-executed
   and not part of the CI pipeline.
```

Cells 0–5 of any sub-notebook are the worked example (read-only reference). The exercise lives in `exercises/` as a separate file. Do not modify chapter notebooks while doing exercises.

## Reproducibility statement — 7 required sections

Author these sections with `{{manifest_field}}` template markers. A2 fills them from the build manifest at CI time.

1. **Materials** — source repo + immutable commit, chapter notebooks, model snapshots, input data origins, artifact hashes
2. **Computational environment** — tested OS/architectures, Python + tool versions, lock files, binary + theme digests, provisioning instructions
3. **Procedure** — exact commands to provision, execute one chapter, execute all chapters, run checks, build site
4. **Experimental conditions** — parameter values, units, assumptions, analysis engines, search bounds, seeds
5. **Result criteria** — expected outputs, reference values, tolerances, volatile-metadata treatment
6. **Verification record** — checks run for this edition, outcomes, platform coverage, links to logs
7. **Interpretive limits** — conditions under which results support claims; remaining uncertainties; reproducing a computation does not establish physical validity

## Contributor guide — 4 required scenarios

1. Update a dependency and regenerate outputs
2. Add a new chapter
3. Change a model element and review stale judgment records
4. Run the full CI pipeline locally

## Tone

Practitioner prose, not tutorial. The reader is a maintainer. Assume they can read Python and SysML.

## What A4 must never do

- Write the reproducibility statement without `{{manifest_field}}` template markers (A2 populates them)
- Write contributor instructions that require unavailable tooling
- Write setup instructions inside chapter narration (they go in `docs/setup.md`)
- Include exercise instructions inside chapter notebooks (exercises live in `exercises/`)
