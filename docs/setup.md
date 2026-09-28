# Getting Started

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Node.js 22 (see `.nvmrc`) and npm, for building the site locally
- Graphviz (`dot` on your PATH), for the diagrams

## Provision the environment

```sh
git clone https://github.com/Open-MBEE/toaster.git
cd toaster
uv sync --locked
uv run python scripts/check-tools.py
```

`check-tools.py` verifies Graphviz is installed and downloads the OpenSysML binary this
tutorial's Python package connects to. It prints each tool's version; if anything is missing,
it names what to install.

Run the test suite to confirm the environment is working:

```sh
uv run pytest tests/ -v
```

## Build and preview the site locally

```sh
npm install
npx mystmd start --execute
```

`--execute` runs every notebook and renders its real output. Without it, MyST renders the stored
cell content only, and a freshly-cloned notebook has none, so every code cell appears with no
output at all.

## The tools this tutorial uses, and why

This tutorial models a system in SysML v2 and runs that model with Python. Two tools do that
work, and neither implements the full SysML v2 specification yet. Both are under active
development, and this tutorial tracks what each one can currently do.

**OpenSysML** (`opensysml`, installed automatically by `check-tools.py`) is the primary tool: it
loads, validates, queries, and evaluates every model in this tutorial. Most chapters need nothing
else.

**sysml-toolkit** does the one thing OpenSysML cannot yet: Chapter 8 needs a bounded proof that a
constraint holds for every value of an unbound quantity, not just a check against one fixed value.
sysml-toolkit's command-line tool has that capability, built on the Z3 solver. It is not a
published package; building it means cloning
[Open-MBEE/sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit) and following its own
build instructions. Chapters 1 through 7 do not need it.

When a tool does not yet support something a chapter needs, this tutorial says so, uses the next
tool that does, and wraps the difference behind a plain Python function so a chapter's own code
reads the same either way. `src/toaster/modelcheck.py` is one example: it calls sysml-toolkit's
command-line tool under the hood, so Chapter 8's own cells only ever see a Python function call.
Each of these wrappers is recorded in `DEFERRED.md`, with the specific gap it patches and the
condition under which the patch comes out: once a published Python package reaches the same
capability, the wrapper is replaced with a direct call to it.

## Fork and exercise

Fork the repository, provision the environment (above), then:

1. Read the worked example: open a chapter notebook in `chapters/` and run every cell.
2. Open the parallel exercise: `exercises/ch{N}/exercise.ipynb`.
3. The exercise asks you to apply the same construct or operation to a different part of the
   toaster. The only tools it needs are the ones the chapter already introduced.

The `exercises/` notebooks are blank workspaces. They are not pre-executed and not part of the
CI pipeline. Work in them directly; do not modify the chapter notebooks while doing an exercise.
