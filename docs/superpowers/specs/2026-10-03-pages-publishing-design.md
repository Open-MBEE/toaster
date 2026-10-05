# Publishing the book to GitHub Pages: design

**Date:** 2026-10-03
**Status:** draft for Z's review (architectural path: spec, then plan, then contracts)
**Plan:** `docs/superpowers/plans/2026-10-03-pages-publishing-phase-a-plan.md`

## Context

Z asked whether the repo is ready to publish as a GitHub Pages site. The readiness review (this session) found
the content is publishable but the build and deploy path is not:

1. No Pages pipeline. Pages is not enabled on `Open-MBEE/toaster`; `.github/workflows/ci.yml` runs tests only, and
   its deploy job is `if: false` ("WP-8 placeholder"). The site has only ever been built on Z's machine
   (`npx myst start --execute`).
2. Figures exist only when notebooks execute. 17 of 18 figure cells have empty stored outputs, by repo
   convention (diagram cells stay `execution_count: null`, `outputs: []`; the minimal-diff rule, DL-099, forbids
   whole-notebook re-execution). A build that publishes stored outputs without executing would drop nearly every
   diagram.
3. Executing needs a toolchain CI does not have: the OpenSysML binary (`scripts/check-tools.py` provisions it),
   Graphviz (CI installs it), and, for Ch5-03, Ch8, Ch10 and `exercises/ch08`, a `sysmlv2` binary from
   sysml-toolkit, its `sysml.library`, a PlantUML jar and a `java` executable.
4. Those notebooks hard-code locations: `Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"`,
   `.../spec-refs/SysML-v2-Release/sysml.library`, `/opt/homebrew/opt/plantuml/libexec/plantuml.jar`,
   `/opt/homebrew/opt/openjdk/.../bin/java`. They fail on any other machine and publish the author's directory
   layout. `toaster.modelcheck` already accepts `SYSMLV2_BINARY` / `SYSMLV2_LIB_DIR`; `toaster.render.
   render_toolkit_interconnection` deliberately accepts only explicit paths.
5. Learner pages cite internal artifacts that will not exist on the site: `SA-7`, `DL-070..072`, `D-001..D-033`,
   `DEFERRED.md`, `AGENTS.md`, `decisions/...` paths.
6. The site will live at `https://open-mbee.github.io/toaster/` (a subpath); nothing sets `BASE_URL`.

Facts established: sysml-toolkit (public, Apache-2.0) publishes prebuilt `sysmlv2` binaries per release with a
`SHA256SUMS` (v0.9.1: x86_64-unknown-linux-gnu, aarch64/x86_64-apple-darwin, ...). Z's local binary is `sysmlv2 0.9.1`
built from `v0.9.1-1-gaf839f0`. The `sysml.library` is the `spec-refs/SysML-v2-Release` submodule
(`Systems-Modeling/SysML-v2-Release`, commit `de1070ae8e79c21532b8004fc663d47b35d0e9fa`). Docker and
`gh` with the `workflow` scope are available on Z's machine.

## Decisions

1. **Execute the book in CI.** The published site is built with `myst build --html --execute`. Not "publish stored
   outputs": that drops the figures, and committing executed outputs would break the minimal-diff convention.
2. **One tool resolver.** A single module (`toaster.tools`) resolves the `sysmlv2` binary, its library, the
   PlantUML jar and `java` from environment variables, then PATH and platform-known locations, and fails with
   an actionable message. Notebooks call it; no notebook names a home or Homebrew path. Env names:
   `SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR` (both already used by `modelcheck`), `PLANTUML_JAR`, `JAVA`.
3. **Provision by pinned download.** Locally and in CI the toolkit comes from its GitHub release, verified against
   the release `SHA256SUMS` pinned in this repo; the library from the pinned SysML-v2-Release commit. Nothing is
   compiled from Rust in CI. Phase A decides the exact version (v0.9.1 expected, since the DEFERRED findings were
   made on 0.9.1) after checking the release binary reproduces the stored outputs.
4. **Deploy only from `main`.** Pull requests run the full build (so a broken book fails review) but do not
   deploy. Deploy uses the official `actions/upload-pages-artifact` / `actions/deploy-pages` flow with
   `BASE_URL=/toaster`.
5. **Dangling references:** each learner-visible reference to an internal artifact is either linked to its GitHub
   file (stable `blob/main` URL) or reworded so the page stands alone. Phase A inventories and classifies them;
   Z picks the policy for the ambiguous classes.
6. **Z-only step:** enabling Pages (Settings, Pages, Source: GitHub Actions) is a repository admin action; it is
   the last step, after a green PR build.

## Non-goals

No chapter content changes beyond the reference cleanup; no custom domain; no versioned docs; no change to which
notebooks are in the book; no Rust build in CI; no change to the minimal-diff or glossary rules.

## Open questions for Z (answered at plan review, defaults given)

- Q1. CI time: executing all notebooks plus provisioning may take several minutes per run. Acceptable? Default yes.
- Q2. Dangling references to `DEFERRED.md` and `decisions/`: link to GitHub files, or reword to stand alone?
  Default: link when the reader benefits from the full text (deferred-gap entries), reword when it is process
  jargon (`SA-7`, `DL-nnn`).
- Q3. Should the book repo expose the agent roles page (`docs/contributor.md` describes `.claude/agents/`)?
  Default: yes, it is accurate and the project is public.

## Verification

A pull-request build on a clean `ubuntu-latest` runner executes every notebook with zero error cells and
produces the site; the built site's figure count equals the figure count of the local build; no built page
contains `/Users/`, `/opt/homebrew`, or `Documents/GitHub`; all internal links resolve with `BASE_URL=/toaster`.
