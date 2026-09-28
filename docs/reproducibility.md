# Reproducibility

This page states what "reproducible" means for this tutorial, what actually makes it true today,
and where that guarantee currently stops. It doesn't repeat the setup steps themselves; see
[Getting Started](setup.md) for how to provision the environment, and
[Contributor Guide](contributor.md) for the maintainer-side mechanics this page points at.

## What's pinned, and why that's most of the guarantee

Reproducing this tutorial's outputs depends on reproducing three things exactly: the Python
environment, the OpenSysML binary, and (only if you're building the rendered book) the Node
toolchain.

- **Python dependencies** are pinned by `uv.lock`, installed with `uv sync --locked` (not
  `uv sync`, which would let versions drift). Every chapter and every test runs against the exact
  versions recorded there.
- **The OpenSysML binary** is pinned by version string (`v0.9.0` as of this tutorial), downloaded
  by `scripts/check-tools.py` rather than resolved from a floating "latest." Every model-loading
  call in every notebook goes through this one pinned binary; there's no code path that reaches a
  different version.
- **Node dependencies**, if you're building the rendered book rather than just running notebooks,
  are pinned by `package-lock.json` (`npm ci`, not `npm install`) and the Node version itself by
  `.nvmrc`. This only affects how the book *looks*; it has no bearing on what any notebook computes.

Given the same three pins, the same model source text should produce the same loaded model, the
same diagnostics, and the same evaluated results, because nothing in the load-and-evaluate path
reaches the network, reads wall-clock time, or depends on iteration order over an unordered
collection. That's a design property of how the notebooks are written, not something this tutorial
has independently verified by running the same notebook on multiple machines or operating systems
side by side — stated as a claim about the code, not a measured guarantee across environments.

## What CI actually checks today

`.github/workflows/ci.yml`'s `build` job runs the pinned-dependency install, `check-tools.py`, and
the full test suite (`pytest tests/ glossary/tests/`) on every push and pull request. It does **not**
yet execute the chapter notebooks or build the rendered book — those steps are scaffolded in the
workflow file but not active. Until they are, "the tests pass" and "every chapter notebook executes
cleanly end to end" are checked by different means: the former continuously in CI, the latter by
whoever re-derives or reviews a chapter, locally, as part of that chapter's own acceptance checks
(see `decisions/pass4-run-*.md` for what that's looked like in practice). `docs/contributor.md`'s
"Run the full CI pipeline locally" section gives the exact commands to run both together.

Deployment to a published site is disabled outright (`docs/contributor.md`'s "Deployment status"),
so nothing about reproducibility here depends on a hosted build ever having existed; every notebook
output referenced anywhere in this tutorial was produced by running it locally, the same way a
reader would.

## Judgment records are reproducible in a different sense: by evidence, not by re-running code

A `ReviewRecord`'s `content_hash` is computed from the exact model source it was written against
(`docs/contributor.md`'s "Change a model element and review stale judgment records" describes the
mechanism). That hash doesn't make the *judgment* reproducible the way a computation is; it makes
the judgment's own evidentiary basis checkable: given the same model source and the same record, a
reader can re-run the cited evaluation, re-read the cited assumptions, and reach their own view on
whether the record's claim still holds. Every record in this tutorial is `record_kind:
"worked_example"` with `disposition: "pending"` for exactly this reason — nothing is asserted as a
settled, accepted conclusion, so nothing here claims a reproducibility that would require trusting a
verdict rather than checking the evidence yourself.

## Where the reproducibility guarantee currently stops

- **Cited source texts are pinned by hash, not distributed.** `glossary/sources/sources.ttl`
  records a sha256 hash for each source this tutorial cites (SEBoK, the SysML v2 and KerML specs,
  Hawkins et al. 2011, and so on), but the PDFs themselves are gitignored, not committed, because
  most of them are under copyright the tutorial doesn't hold. `uv run python -m glossary check`
  verifies a source's hash only when that file happens to be present locally; in a fresh clone or in
  CI, it reports a warning ("source PDF not present locally") rather than a failure. This means a
  reader can independently confirm the tutorial cites the edition it says it does, provided they
  obtain their own copy of that same source and check its hash against the recorded one; it is not
  something cloning this repository alone reproduces.
- **A gap fixed upstream doesn't silently change what's here.** Where OpenSysML or sysml-toolkit
  doesn't yet support something the spec allows, `DEFERRED.md` records the gap together with the
  exact version it was found against (down to a commit hash, for the one case built from source
  rather than a tagged release). If a later version of either tool closes that gap, this tutorial's
  own behavior doesn't change until someone deliberately bumps the pinned version and updates the
  affected notebooks; the recorded gap is what tells a maintainer, later, exactly which patch to
  remove and why.
- **The rendered book isn't rebuilt automatically.** Because the notebook-execution and book-build
  steps aren't yet part of CI (see above), a change to a notebook's own code doesn't automatically
  re-verify that the book still renders correctly; that's a manual step today, tracked as its own
  open item, not a silent gap in what's claimed.
