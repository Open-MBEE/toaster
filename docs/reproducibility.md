# Reproducibility

This page states what "reproducible" means for this tutorial, what actually makes it true today,
and where that guarantee currently stops. It doesn't repeat the setup steps themselves; see
[Getting Started](setup.md) for how to provision the environment, and
[Contributor Guide](contributor.md) for the maintainer-side mechanics this page points at.

## What's pinned, and why that's most of the guarantee

Reproducing this tutorial's outputs depends on reproducing four things exactly: the Python
environment, the OpenSysML binary, the external tools some chapters call, and (only if you're
building the rendered book) the Node toolchain.

- **Python dependencies** are pinned by [`uv.lock`](https://github.com/Open-MBEE/toaster/blob/main/uv.lock), installed with `uv sync --locked` (not
  `uv sync`, which would let versions drift). Every chapter and every test runs against the exact
  versions recorded there.
- **The OpenSysML binary** is pinned by version string (`v0.9.0` as of this tutorial), downloaded
  by [`scripts/check-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py) rather than resolved from a floating "latest." Every model-loading
  call in every notebook goes through this one pinned binary; there's no code path that reaches a
  different version.
- **The external tools** that chapters 5, 8 and 10 call (the `sysmlv2` command-line tool, Z3, the
  PlantUML jar and the SysML v2 standard library) are pinned in
  [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json) and installed by
  `scripts/provision-tools.py`. The `sysmlv2` tool, Z3 and the PlantUML jar are pinned by version
  and sha256 hash, and the script refuses to install a download whose hash does not match; the
  standard library is pinned by git commit and checked out at exactly that commit, with no hash
  (see [Getting Started](#tools-for-chapters)). Java and Graphviz come from your
  system and are not pinned.
- **Node dependencies**, if you're building the rendered book rather than just running notebooks,
  are pinned by [`package-lock.json`](https://github.com/Open-MBEE/toaster/blob/main/package-lock.json) (`npm ci`, not `npm install`) and the Node version itself by
  [`.nvmrc`](https://github.com/Open-MBEE/toaster/blob/main/.nvmrc). This only affects how the book *looks*; it has no bearing on what any notebook computes.

Given the same pins, the same model source text should produce the same loaded model, the
same diagnostics, and the same evaluated results, because nothing in the load-and-evaluate path
reaches the network, reads wall-clock time, or depends on iteration order over an unordered
collection. That's a design property of how the notebooks are written, not something this tutorial
has independently verified by running the same notebook on multiple machines or operating systems
side by side — stated as a claim about the code, not a measured guarantee across environments.

## What CI actually checks

[`.github/workflows/ci.yml`](https://github.com/Open-MBEE/toaster/blob/main/.github/workflows/ci.yml) builds the book on every pull request.
The `build` job installs the pinned dependencies, provisions the external tools with
[`scripts/provision-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/provision-tools.py), runs the full test suite
(`pytest tests/ glossary/tests/`), builds the rendered book with every chapter notebook executed,
and then runs the release gate, [`scripts/check-site.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-site.py).
The gate fails the build on any cell that raised an error, on a figure count that differs from the
recorded baseline, on a host path in any built file, on `exercises/` files or `DEFERRED.md`
published as raw downloads, and on a root-relative link or asset reference that does not carry the base path or does not
resolve (it reads `href`, `src`, `srcset`, `meta` content and CSS `url()` values; relative links
and `#fragment` links are not checked). It does not compare
each executed output with the output stored in the notebook, and it does not run the notebooks on
more than one operating system. The [Contributor Guide](#deployment-status) says how
to run the same build and gate locally.

Pull-request builds do not deploy. A push to `main` that passes the same build is deployed to
<https://open-mbee.github.io/toaster/>. The stored notebook outputs in the repository were
produced locally; the published book is produced by CI executing the notebooks again, so a
reader of the site is looking at the CI run's output. Chapter-level acceptance runs from before CI
executed notebooks are recorded among [the run records in `decisions/`](https://github.com/Open-MBEE/toaster/tree/main/decisions).

## Judgment records are reproducible in a different sense: by evidence, not by re-running code

A `ReviewRecord`'s `content_hash` is computed from the exact model source it was written against
(the [Contributor Guide](#change-a-model-element)'s section on
changing a model element describes the mechanism). That hash doesn't make the *judgment* reproducible the way a computation is; it makes
the judgment's own evidentiary basis checkable: given the same model source and the same record, a
reader can re-run the cited evaluation, re-read the cited assumptions, and reach their own view on
whether the record's claim still holds. Every record in this tutorial is `record_kind:
"worked_example"` with `disposition: "pending"` for exactly this reason — nothing is asserted as a
settled, accepted conclusion, so nothing here claims a reproducibility that would require trusting a
verdict rather than checking the evidence yourself.

Some record text quotes identifiers such as `D-029`. These refer to entries in
[`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md), the register of known
toolchain gaps; they are not links on the page because the record text is stored exactly as the
notebook wrote it.

## Where the reproducibility guarantee currently stops

- **Cited source texts are pinned by hash, not distributed.** [`glossary/sources/sources.ttl`](https://github.com/Open-MBEE/toaster/blob/main/glossary/sources/sources.ttl)
  records a sha256 hash for each source this tutorial cites (SEBoK, the SysML v2 and KerML specs,
  Hawkins et al. 2011, and so on), but the PDFs themselves are gitignored, not committed, because
  most of them are under copyright the tutorial doesn't hold. `uv run python -m glossary check`
  verifies a source's hash only when that file happens to be present locally; in a fresh clone or in
  CI, it reports a warning ("source PDF not present locally") rather than a failure. This means a
  reader can independently confirm the tutorial cites the edition it says it does, provided they
  obtain their own copy of that same source and check its hash against the recorded one; it is not
  something cloning this repository alone reproduces.
- **A gap fixed upstream doesn't silently change what's here.** Where OpenSysML or sysml-toolkit
  doesn't yet support something the spec allows, [`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md) records the gap together with the
  exact version it was found against (down to a commit hash, for the one case built from source
  rather than a tagged release). If a later version of either tool closes that gap, this tutorial's
  own behavior doesn't change until someone deliberately bumps the pinned version and updates the
  affected notebooks; the recorded gap is what tells a maintainer, later, exactly which patch to
  remove and why.
- **The published book is one environment's run.** CI builds it on one Linux runner with the
  pinned tools. That the same notebooks reproduce their stored outputs on other machines is a
  property of how they are written (above), not something CI measures.
