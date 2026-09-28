# Getting Started

## Run the tutorial

This is everything you need to work through the chapters and exercises. It does not need
Node.js or npm; those are only for previewing the rendered book, covered further down.

**Prerequisites:**

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Graphviz (`dot` on your PATH): several chapters render diagrams with it

```sh
git clone https://github.com/Open-MBEE/toaster.git
cd toaster
uv sync --locked
uv run python scripts/check-tools.py
```

`check-tools.py` verifies Graphviz is installed and downloads the OpenSysML binary this
tutorial's Python package connects to. It prints each tool's version; if anything is missing,
it names what to install.

`uv sync --locked` also installs JupyterLab and the kernel this project uses (both are
declared dependencies, not a separate install step). Open any chapter or exercise notebook with:

```sh
uv run jupyter lab
```

Run the test suite to confirm the environment is working:

```sh
uv run pytest tests/ -v
```

## Preview the rendered book locally

There is no published site yet: deployment stays off until the tutorial has complete,
end-to-end content ready to publish (see `docs/contributor.md`). Building it yourself, here,
is currently the only way to see the tutorial as a rendered book rather than as raw notebook
files. This needs Node.js in addition to the Python setup above.

**Additional prerequisite:** Node.js 22 (see `.nvmrc`) and npm.

```sh
npm install
npx mystmd start --execute
```

`--execute` runs every notebook and renders its real output. Without it, MyST renders the
stored cell content only, and a freshly-cloned notebook has none, so every code cell appears
with no output at all.

Building and deploying the GitHub Pages site itself is a maintainer task, not something you
need for the tutorial; see `docs/contributor.md`.

## The tools this tutorial uses, and why

This tutorial models a system in SysML v2 and runs that model with Python. Two tools do that
work, and neither implements the full SysML v2 specification yet. Both are under active
development, and this tutorial tracks what each one can currently do.

**OpenSysML** (`opensysml`, installed automatically by `check-tools.py`) is the primary tool: it
loads, validates, queries, and evaluates every model in this tutorial. Every chapter needs it.

**sysml-toolkit** does one thing OpenSysML cannot yet: prove that a constraint holds for every
value of an unbound quantity, not just check it against one fixed value, using the Z3 solver.
No chapter currently uses this; it becomes relevant once Chapter 8 is re-derived to need it.
It is not on crates.io. The name `sysmlv2` is reserved on PyPI by sysml-toolkit's own
maintaining organization, but the package published there today is a placeholder, not the real
thing; do not `pip install` it. Get a working binary instead from
[its GitHub releases page](https://github.com/Open-MBEE/sysml-toolkit/releases) (macOS, Linux,
and Windows builds are published there). Revisit this note once the maintainers publish the real
package: installing it should then replace both this download step and, eventually, the
`subprocess` call in `src/toaster/modelcheck.py` (`DEFERRED.md` D-025) with a direct Python call.

When a tool does not yet support something a chapter needs, this tutorial says so, uses the next
tool that does, and wraps the difference behind a plain Python function so a chapter's own code
reads the same either way. `src/toaster/modelcheck.py` is one example: it will call
sysml-toolkit's command-line tool under the hood, so Chapter 8's own cells only ever see a
Python function call. Each of these wrappers is recorded in `DEFERRED.md`, with the specific gap
it patches and the condition under which the patch comes out: once a published Python package
reaches the same capability, the wrapper is replaced with a direct call to it.

## Fork and exercise

Fork the repository, provision the environment (above), then:

1. Read the worked example: open a chapter notebook in `chapters/` and run every cell.
2. Open the parallel exercise: `exercises/ch{N}/exercise.ipynb`.
3. The exercise asks you to apply the same construct or operation to a different part of the
   toaster. The only tools it needs are the ones the chapter already introduced.

The `exercises/` notebooks are blank workspaces. They are not pre-executed and not part of the
CI pipeline. Work in them directly; do not modify the chapter notebooks while doing an exercise.
