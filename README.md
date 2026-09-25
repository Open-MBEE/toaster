# Toaster

An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML.
Starting from one abstract system definition, readers progressively add purpose, requirements,
measures, functions, structure, and executable behavior for a domestic toaster.

**Published site:** https://open-mbee.github.io/toaster/

Adapted from Brian Douglas's [Systems Engineering Part 3](https://www.mathworks.com/videos/systems-engineering-part-3-the-benefits-of-functional-architectures-1602837771665.html).
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

# Build the site
npm install
npx mystmd build --execute
```

See [docs/setup.md](docs/setup.md) for full setup instructions and the fork-and-exercise workflow.

## Repository structure

```
chapters/   — worked example notebooks (10 chapters, read-only for exercises)
exercises/  — parallel exercise notebooks (fork and work here)
models/     — SysML stage model snapshots
src/toaster/— Python package (bootstrap, connect, query, check, evidence, simulate, render, report)
tests/      — pytest suite
docs/       — setup, glossary, references, reproducibility statement
scripts/    — pre-flight and build utilities
decisions/  — ACE decision log
```
