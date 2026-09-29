# Diagram tool gaps

A living register of confirmed capability gaps and bugs in rendering tools
considered for this tutorial's diagrams, distinct from `DEFERRED.md` (which
stays scoped, per `decisions/log.md` `DL-055`, to gaps in constructs or
dependencies this tutorial actually adopts). Both entries below are about
tools this tutorial does **not** adopt -- see `decisions/diagram-study-real-fixtures.md`
and `docs/superpowers/specs/2026-09-29-diagram-generation-strategy-design.md`
for why. They're recorded here so the findings aren't lost, and so a drafted
upstream issue (`decisions/gap-issue-drafts.md`'s existing discipline: draft,
hold for Z's review, file only on instruction) has a durable source to draw
from once a gap's picture is complete enough to be worth filing.

## G-D001: OMG pilot rejects qualified-name `allocate` targets

- **Tool / version:** OMG SysML v2 Pilot Implementation, release `2026-08`, `jupyter-sysml-kernel-0.62.0`.
- **Symptom:** every real-fixture render attempt (all 4 fixtures, all view types tried) fails with `ERROR:Must be an accessible feature (use dot notation for nesting)`, pointing at an `allocation ... allocate X::y to Z::w;` statement -- e.g. `models/ch05-cumulative.sysml:111`, `allocation heatAllocation allocate ToastBread::applyHeat to Toaster::heating;`.
- **Root cause:** the pilot's name-resolution check rejects a qualified-name (`::`-separated) reference on either side of an `allocate` statement; not established whether this is a pilot limitation or a real question about the tutorial's own `allocate` syntax against the spec (open, not resolved here).
- **Evidence:** `decisions/diagram-study-real-fixtures/evidence/ch05-tree-pilot-emit.log` and the equivalent log for every other fixture/view combination (all show the identical error).
- **Adoption-blocking?** Moot -- the pilot is not adopted for this tutorial (see the tool-selection table in `docs/superpowers/specs/2026-09-29-diagram-generation-strategy-design.md`); this entry exists to inform the pilot's own developers, not to justify a workaround for use here.
- **Status:** documented, not drafted. No issue drafted yet.

## G-D002: SysMLD/sysml2d indexer mis-tracks brace scope on ordinary real syntax

- **Tool / version:** `sysml2d` (SysMLD), pinned commit `1af88250d355f4e218f6653ef934e93ac8319cd6`.
- **Symptom:** `sysmld.model_index.build_model_index()` cannot resolve any correctly-qualified real element name from either of Ch5's or Ch7's real fixture models -- only a truncated, package-prefix-dropped form resolves (e.g. `Toaster` resolves, `ToasterDemo::Toaster` does not).
- **Root cause:** the indexer pops a scope frame (`package_stack`/`def_stack`) on any source line starting with `}`, regardless of whether a tracked keyword (`package`, `part def`, `state def`, and a few behavior kinds) opened that specific brace. Both real fixtures contain an untracked brace pair inside `action def ApplyHeat` (a multi-line `doc` annotation, and an `assert constraint balance { ... }` body) whose closing braces pop frames early, eventually popping the outer `package ToasterDemo { ... }` frame itself before later elements are indexed.
- **Evidence:** `decisions/diagram-study-real-fixtures/evidence/sysmld-indexer-probe.json` (the `idx.has(...)` checks, both a true positive on the truncated form and a false negative on the correct form); `decisions/log.md` `DL-055` and its addendum (the full ACE ruling and independent review that confirmed this root cause against the pinned source directly).
- **Adoption-blocking?** Moot -- SysMLD is not adopted for this tutorial and was already only "not adopted" per the original toy-fixture study, kept in Phase 0's rerun for comparison completeness only. This entry exists to inform sysml2d's own developers.
- **Status:** documented, not drafted. No issue drafted yet.
