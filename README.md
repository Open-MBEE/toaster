# Toaster

An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML.
Starting from one abstract system definition, readers progressively add purpose, requirements,
measures, functions, structure, and executable behavior for a domestic toaster.

No site is published yet; deployment stays off until the tutorial has complete, end-to-end content ready to publish. See [docs/setup.md](docs/setup.md) to run the tutorial or build the book locally.

Adapted from Brian Douglas's [Systems Engineering Part 3](https://www.mathworks.com/videos/systems-engineering-part-3-the-benefits-of-functional-architectures-1602837771665.html)
and [Part 4](https://www.mathworks.com/videos/systems-engineering-part-4-an-introduction-to-requirements-1603872564696.html).
Engineering judgment records follow Hawkins et al. 2011 §§3.1–3.4.

## Quick start

```sh
# Clone and provision
git clone https://github.com/Open-MBEE/toaster.git
cd toaster
uv sync --locked
uv run python scripts/check-tools.py

# Run tests
uv run pytest tests/ -v

# Preview the book locally (starts a dev server at localhost:3000)
npm install
npx mystmd start --execute
```

See [docs/setup.md](docs/setup.md) for full setup instructions and the fork-and-exercise workflow,
including what `uv` and `mystmd` are and why the quick start above uses them.

## Repository structure

```
chapters/   — worked example notebooks (10 chapters, read-only for exercises)
exercises/  — parallel exercise notebooks (fork and work here)
models/     — SysML stage model snapshots
src/toaster/— Python package (bootstrap, connect, query, check, conformance, evidence, modelcheck, simulate, render, report)
tests/      — pytest suite
docs/       — setup, glossary, references, reproducibility statement
scripts/    — pre-flight and build utilities
decisions/  — ACE decision log
```

`AGENTS.md`, `CLAUDE.md`, and `DEFERRED.md` at the repo root are not learner material — they're
this project's own working contract, for the AI agents and maintainers who build and review the
tutorial's content. See [docs/contributor.md](docs/contributor.md) if you want to understand how
the tutorial is actually built, tested, and reviewed, or to contribute to it yourself.
