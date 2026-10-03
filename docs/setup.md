# Getting Started

## Run the tutorial

This is everything you need to work through the chapters and exercises. It does not need
Node.js or npm; those are only for previewing the rendered book, covered further down.

**Prerequisites:**

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Graphviz (`dot` on your PATH): several chapters render diagrams with it
- Java 17 or later (`java` on your PATH): chapter 5 runs the PlantUML jar with it

```sh
git clone https://github.com/Open-MBEE/toaster.git
cd toaster
uv sync --locked
uv run python scripts/provision-tools.py
uv run python scripts/check-tools.py
```

`provision-tools.py` downloads the pinned external tools into `.tools/` (see
[Tools for chapters 5, 8 and 10](#tools-for-chapters) below).
[`check-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py)
prints where each tool resolves and its version, verifies Graphviz is installed, and downloads
the OpenSysML binary this tutorial's Python package connects to. If anything is missing, it
names what to install.

`uv sync --locked` also installs JupyterLab and the kernel this project uses (both are
declared dependencies, not a separate install step). Open any chapter or exercise notebook with:

```sh
uv run jupyter lab
```

Run the test suite to confirm the environment is working:

```sh
uv run pytest tests/ -v
```

The glossary's source checks (`uv run python -m glossary verify-sources`) also need the copyrighted source PDFs, which are not in the repository. The section "Getting the source files" in [`glossary/README.md`](https://github.com/Open-MBEE/toaster/blob/main/glossary/README.md) says where to get each one and where to put it.

## Preview the rendered book locally

CI builds this book on every pull request and deploys it from `main` to
<https://open-mbee.github.io/toaster/>; see [the contributor guide](#deployment-status).
To see it rendered from your own checkout, with your own changes, preview it locally. This needs
Node.js in addition to the Python setup above.

**Additional prerequisite:** Node.js 22 (see [`.nvmrc`](https://github.com/Open-MBEE/toaster/blob/main/.nvmrc)) and npm.

```sh
npm ci
uv run npx mystmd start --execute
```

`--execute` runs every notebook and renders its real output. Without it, MyST renders the
stored cell content only, and a freshly-cloned notebook has none, so every code cell appears
with no output at all.

`uv run` is needed so that MyST finds this project's Jupyter, the one `uv sync --locked`
installed with the project's kernel. Without it, MyST looks for a Jupyter on your `PATH`, which
is usually a different installation and does not have the tutorial's dependencies.

To build the static site the way CI does, rather than serve it, use the build form. The base
URL is the path the site is served under on GitHub Pages:

```sh
BASE_URL=/toaster uv run --frozen npx myst build --html --execute
```

Building and deploying the GitHub Pages site itself is a maintainer task, not something you
need for the tutorial; see [the contributor guide](#deployment-status).

(tools-for-chapters)=
## Tools for chapters 5, 8 and 10

Some chapters call external programs that are not Python packages. Chapters 5, 8 and 10 run the
`sysmlv2` command-line tool against the SysML v2 standard library; chapter 5 also draws its
interconnection diagram with PlantUML, and chapters 8 and 10 prove constraints with Z3 through
`sysmlv2 verify --solve`. One command downloads pinned versions of these into `.tools/`, a
directory git ignores:

```sh
uv run python scripts/provision-tools.py
```

It installs the pinned `sysmlv2` command-line tool (sysml-toolkit), the Z3 solver, the PlantUML
jar and the SysML v2 standard library (`sysml.library`), as pinned in
[`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json).
It checks the `sysmlv2` tool, Z3 and the PlantUML jar against a sha256 hash before installing
them; the library is pinned by git commit and checked out at exactly that commit, with no hash.
Re-running it keeps what is already installed and matches its pin.
`uv run python scripts/provision-tools.py --check` verifies the installed files without
downloading anything, and `--dest DIR` installs somewhere other than `.tools/`. Tools installed
with `--dest` elsewhere are found only if you apply the `export` lines the script prints at the
end (the environment variables in the table below); otherwise they are not seen.

Two tools come from your system instead. **Java 17 or later** (`java`) runs the PlantUML jar,
and **Graphviz** (`dot`) lays out the other diagrams; install them with your package manager.

Then verify:

```sh
uv run python scripts/check-tools.py
```

It prints where each tool resolved from and its version, and exits non-zero, naming the
provisioning command, if one is missing.

Each tool is found the same way: an explicit argument, then an environment variable, then
`.tools/`, then your `PATH` (the library and the jar are never searched for on `PATH`; Java is
never provisioned). Set a variable to use a tool installed somewhere else. A variable that names
a missing or invalid file is an error; it does not fall back to the next place.

| Variable | Overrides |
|---|---|
| `SYSMLV2_BINARY` | the `sysmlv2` executable (default `.tools/bin/sysmlv2`, then `PATH`) |
| `SYSMLV2_LIB_DIR` | the `sysml.library` directory, which must contain a `Systems Library` folder (default `.tools/sysml.library`) |
| `PLANTUML_JAR` | the PlantUML jar (default `.tools/plantuml.jar`) |
| `JAVA` | the `java` executable (default: `PATH`) |
| `Z3` | the `z3` executable (default `.tools/bin/z3`, then `PATH`) |

When a test needs one of these tools and cannot find it, it skips by default. Set
`TOASTER_REQUIRE_TOOLS=1` to make a missing tool a failure instead, for example before you
trust a green test run:

```sh
TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/ -v
```

## The tools this tutorial uses, and why

This tutorial models a system in SysML v2 and runs that model with Python. Two tools do that
work, and neither implements the full SysML v2 specification yet. Both are under active
development, and this tutorial tracks what each one can currently do.

**OpenSysML** (`opensysml`, installed automatically by [`check-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py)) is the primary tool: it
loads, validates, queries, and evaluates every model in this tutorial. Every chapter needs it.
[`scripts/check-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py) also provisions a second OpenSysML binary, the
render-capable CLI (distinct from the service binary the Python package
itself talks to) — chapters that render an action-flow or state-transition
diagram need it; nothing else does.

**sysml-toolkit** does one thing OpenSysML cannot yet: prove that a constraint holds for every
value of an unbound quantity, not just check it against one fixed value, using the Z3 solver.
Chapter 8 uses it directly (`toaster.modelcheck.verify_holds`, wrapping its `sysmlv2 verify
--solve` CLI) to prove `deliveredEnergyBoundedBySupply` for every value its unbound features
admit. It is not on crates.io. The name `sysmlv2` is reserved on PyPI by sysml-toolkit's own
maintaining organization, but the package published there today is a placeholder, not the real
thing; do not `pip install` it. Get a working binary instead from `scripts/provision-tools.py`
(above), which installs the pinned build from
[its GitHub releases page](https://github.com/Open-MBEE/sysml-toolkit/releases). Revisit this note
once the maintainers publish the real package: installing it should then replace both this
download step and, eventually, the `subprocess` call in
[`src/toaster/modelcheck.py`](https://github.com/Open-MBEE/toaster/blob/main/src/toaster/modelcheck.py)
([`DEFERRED.md` D-025](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md#d-025-toastermodelcheck-wraps-sysmlv2-verify---solve-via-subprocess-intended-for-deprecation))
with a direct Python call.

When a tool does not yet support something a chapter needs, this tutorial says so, uses the next
tool that does, and wraps the difference behind a plain Python function so a chapter's own code
reads the same either way. [`src/toaster/modelcheck.py`](https://github.com/Open-MBEE/toaster/blob/main/src/toaster/modelcheck.py) is one example: it will call
sysml-toolkit's command-line tool under the hood, so Chapter 8's own cells only ever see a
Python function call. Each of these wrappers is recorded in [`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md), with the specific gap
it patches and the condition under which the patch comes out: once a published Python package
reaches the same capability, the wrapper is replaced with a direct call to it.

## Fork and exercise

Fork the repository, provision the environment (above), then:

1. Read the worked example: open a chapter notebook in `chapters/` and run every cell.
2. Open the parallel exercise: `ch{N}/exercise.ipynb` in the [`exercises/` directory](https://github.com/Open-MBEE/toaster/tree/main/exercises).
3. The exercise asks you to apply the same construct or operation to a different domain: a
   coffee maker, built in parallel to the toaster throughout the tutorial. The only tools it
   needs are the ones the chapter already introduced.

The [`exercises/`](https://github.com/Open-MBEE/toaster/tree/main/exercises) notebooks are blank workspaces. They are not pre-executed and not part of the
CI pipeline. Work in them directly; do not modify the chapter notebooks while doing an exercise.

**Keep your model between chapters.** Each exercise's first cell asks you to paste in your own
completed model from the previous chapter's exercise — there is no committed solution file to
load instead. Save the full `source` string your notebook ends with (for example, to a scratch
`.sysml` file in your own fork, or just keep the notebook itself open) before moving to the next
chapter's exercise, or you will have nothing to paste in. Chapter 6's own exercise is the one
case where you need to keep **two** separate snapshots, not one: the model state right before you
add `Impeller` (used by the mechanism-selection judgment, written before the mechanism it selects
exists) and the model state right after (used by the stopping judgment, and the one that carries
forward into Chapter 7). Chapter 6's own exercise notebook flags exactly where to save each one.
