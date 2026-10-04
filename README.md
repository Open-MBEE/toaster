# Toaster

An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML.
Starting from one abstract system definition, readers progressively add purpose, requirements,
measures, functions, structure, and executable behavior for a domestic toaster.

CI builds the book on every pull request and deploys it from `main` to <https://open-mbee.github.io/toaster/>. See [docs/setup.md](docs/setup.md) to run the tutorial or preview the book locally.

Adapted from Brian Douglas's [Systems Engineering Part 3](https://www.mathworks.com/videos/systems-engineering-part-3-the-benefits-of-functional-architectures-1602837771665.html)
and [Part 4](https://www.mathworks.com/videos/systems-engineering-part-4-an-introduction-to-requirements-1603872564696.html).
Engineering judgment records follow Hawkins et al. 2011 §§3.1–3.4.

## Quick start

```sh
# Clone and provision
git clone https://github.com/Open-MBEE/toaster.git
cd toaster
uv sync --locked
uv run python scripts/provision-tools.py
uv run python scripts/check-tools.py

# Run tests
uv run pytest tests/ -v

# Preview the book locally (starts a dev server at localhost:3000)
npm ci
uv run npx mystmd start --execute
```

`uv run` matters for the preview: it lets MyST find this project's Jupyter. Without it, MyST
looks for a Jupyter on your `PATH`, which is usually a different installation. To build the
static site the way CI does:

```sh
BASE_URL=/toaster uv run --frozen npx myst build --html --execute --strict
```

See [docs/setup.md](docs/setup.md) for full setup instructions and the fork-and-exercise workflow,
including what `uv` and `mystmd` are and why the quick start above uses them.

## Repository structure

```
chapters/   — worked example notebooks (10 chapters, read-only for exercises)
exercises/  — parallel exercise notebooks (work them in your own fork)
models/     — SysML stage model snapshots
src/toaster/— Python package (bootstrap, connect, query, check, conformance, evidence, modelcheck, simulate, render, report)
tests/      — pytest suite
docs/       — setup, glossary, references, reproducibility statement
scripts/    — pre-flight and build utilities
decisions/  — ACE decision log
```

[`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), and [`DEFERRED.md`](DEFERRED.md) at the repo root are not learner material — they're
this project's own working contract, for the AI agents and maintainers who build and review the
tutorial's content. See [docs/contributor.md](docs/contributor.md) to understand how the tutorial
is built, tested and reviewed, and what contributions it wants: keeping it current to its
toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML
v2 specifications, not adding new content.
