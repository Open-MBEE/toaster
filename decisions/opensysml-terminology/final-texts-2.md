# Final texts and rulings, batch 2 (ACE, DL-118): authoritative over final-texts.md and the inventories

Source: ACE batch 2 ruling of 2026-10-03, recorded as DL-118. Where this file and `final-texts.md` differ, THIS FILE governs.

## A. DEFERRED.md (on branch term/binding, before it merges)
- **A1. B-056 is REVERTED** (KEEP-BODY, like B-057). Restore the D-032 `**Status: GUARDED.**` sentence byte-identical to `main`
  (`pages-publishing:DEFERRED.md`): `The underlying OpenSysML/sysml-toolkit acceptance-without-diagnostic gap itself remains open upstream — this entry documents the gap and its guard, not a fix to either tool.`
- **A2. Top note last sentence** becomes: `Where an entry records a different result for sysml-toolkit (D-017, D-019, D-023, D-024, D-034, D-035, D-036), a bare "OpenSysML" in the heading is the runtime and the body states what sysml-toolkit v0.9.1 does.` (Rest of the note unchanged.)

## B. docs (OT-3C)
- **B1. Case study L69-71:** `No tool diagnostic and neither review process caught Approach A's own defect; it took re-reading §7.21.1 directly, later, to name it.`
- **B2. Case study L189:** `deserves to be checked against the OpenSysML runtime, not just read off the spec text.`  **L201:** `tested directly against \`model.verify_satisfaction()\` — the runtime's own point-evaluation engine,` (existing em-dash left as is).
- **B3. docs/references.md sysml-toolkit paragraph (amends final-texts.md):** `The Rust toolkit (\`sysmlv2\` binary, pinned v0.9.1), used in Chapter 5 to draw the interconnection diagram (\`sysmlv2 viz\`, laid out by PlantUML), in Chapters 8 and 10 for \`sysmlv2 verify --solve\` (through \`toaster.modelcheck\` in Chapter 8; called directly in Chapter 10), and for the cross-checks recorded in DEFERRED.md.`
- **B4. docs/reproducibility.md L20-22:** replace `Every model-loading call in every notebook goes through this one pinned binary; there's no code path that reaches a different version.` with `Every model-loading call in every notebook goes through this one pinned binary; there's no code path that reaches a different version of the runtime. Chapters 5, 8 and 10 also hand model text to sysml-toolkit's \`sysmlv2\`, pinned by the next item.`
- **B5. docs/setup.md (R112):** `**sysml-toolkit** does what the OpenSysML runtime cannot yet: prove that a constraint holds for every value of an unbound quantity, not just check it against one fixed value, using the Z3 solver.` (The following sentence "Chapter 8 uses it directly ..." stays.)

## C. chapters (OT-3C; markdown cells only)
- **C1.** ch07 nb02 `cell-05`: `confirmed by the tool actually attempting it` -> `confirmed by the runtime actually attempting it`.
- **C2.** ch07 nb02 `cell-27`: `(a documented tool gap, [D-028]` -> `(a documented runtime gap, [D-028]`.
- **C3.** ch08 nb02 `cell-10`: `this toolchain's Z3 backend never actually composes` -> `sysml-toolkit's Z3 backend never actually composes`. ("Two separate, real limits of this toolchain" stays; cells 14 and 16 "this toolchain" stay.)
- **C4.** ch10 nb01 `3a3d9d15`: replace `what \`sysmlv2 verify --solve\` -- a different tool from \`model.verify_satisfaction()\`, this tutorial's own Z3-backed solver, used for \`deliveredEnergyBoundedBySupply\`'s own proof in Chapter 8 -- actually reports` with `what sysml-toolkit's \`sysmlv2 verify --solve\` -- the Z3-backed solver used for \`deliveredEnergyBoundedBySupply\`'s own proof in Chapter 8, a different tool from the OpenSysML runtime's \`model.verify_satisfaction()\` -- actually reports` (ASCII `--` as the cell uses).
- **C5.** ch10 nb01 `9d918eda`: `no pilot warning ever fired against it` -> `no warning from the OMG SysML v2 Pilot Implementation (the pilot) ever fired against it`. ch10 nb01 `310279c7`: `the real OMG pilot` -> `the real pilot`.
- **C6.** exercises/ch08 `cell-16`: no change (sentence-initial lowercase `sysml-toolkit's` stands).

## D. Lint (OT-7) specification
- `glossary/lint.py` already reads only markdown cells of `chapters/**/*.ipynb`, `chapters/**/*.md`, `docs/**/*.md` (minus `docs/glossary.md`); code cells and outputs are never read. Add: (1) optional per-rule boolean `ignore_code` (default false; accepted only as bool, else exit 2) that masks fenced blocks and inline code spans with equal-length spaces (newlines preserved) before matching; the six new rules set it. (2) prefix exclusion of `docs/superpowers/` in `_units()`. (3) Six `[[rule]]` tables, `severity = "error"`, `scope = "learner"`, `why` citing AGENTS.md 1.2 and DL-116: `OpenSysML\s+(or|and|nor|vs\.?|versus)\s+sysml-toolkit`; `sysml-toolkit\s+(or|and)\s+OpenSysML`; `neither\s+OpenSysML`; `not\s+OpenSysML`; `OpenSysML\s+(alone|itself|cannot|can't|does\s+not|doesn't|only)`; `OpenSysML\s+v0\.9`. (4) Acceptance: the six rules show 0 on the merged branch after OT-3C; every other rule's count equals base outside `docs/superpowers` (record before/after per-rule counts). The lint is not a CI gate. DEFERRED.md and exercises/ are outside the lint's scope.
