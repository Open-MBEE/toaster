# Final texts and rulings (ACE, DL-117): authoritative over the inventories

Where `inventory-a.md` / `inventory-b.md` proposed wording that differs from this file, THIS FILE governs. Source: ACE batch
ruling of 2026-10-03 (recorded as DL-117 in `decisions/log.md`). Normative convention: DL-116 and
`docs/superpowers/plans/2026-10-03-opensysml-terminology-plan.md`.

## Clarification of DL-116 (3)
In a DEFERRED.md body, "the sentence stating the gap" means any sentence that reports a tool's observed behavior (what
loads, what is rejected, what is printed), wherever it sits in the entry. The field lines **Workaround**, **Resolution**,
**Upstream issue**, **Toaster issue** and **Status** are dated record and are LEFT AS WRITTEN (class KEEP-BODY): B-014,
B-048, B-057, B-060, B-064, B-067, B-068, B-071. Headings are never edited.

## Binding-surface rulings (inventory-b)
- **B-057** (DEFERRED.md:852): leave, KEEP-BODY.
- **B-082** (`.claude/skills/ace-protocol/SKILL.md:63`, SA-6): done by the ACE in OT-6. SA words are not rewritten; append a
  parenthetical. Final line:
  `| SA-6 | Bounded model checking: opensysml \`check\` engine only (the runtime's engine; for "holds" questions Z accepted sysml-toolkit's \`sysmlv2 verify --solve\` wrapped by \`toaster.modelcheck\`: DL-046, D-025) |`
- **B-084** (`.claude/skills/ace-protocol/z-model.md:21`, Z-12): done by the ACE in OT-6. Nobody rewrites Z's words; add a
  bracketed dated reading note. Final line:
  `- Z-12. OpenSysML and other implementations are toolchain, cited only to flag spec gaps. Tall's three worlds and the optimization/control lens are builder-facing and never named in learner content. [Reading note, 2026-10-03, DL-116/DL-117: said when this repository used "OpenSysML" for the runtime; it now names the stack whose components the tutorial uses are the OpenSysML runtime and sysml-toolkit. The position holds under both readings.]`
- **Gap-statement edits stand** (B-038, B-045, B-047, B-055, B-056, B-063 all three replacements, B-066 first
  replacement, B-070 both replacements). **B-066's second replacement is subsumed** by the D-035 correction below.
- **B-079** (`glossary/sources/notes/reading-notes.md:35`) goes to OT-5: `- The OpenSysML runtime and sysml-toolkit (components of the OpenSysML stack) and the Pilot Implementation are toolchain, cited only to flag spec gaps. They define no terms.` (`uv run python -m glossary check` must stay green.)
- **Skills:** 15 directories, not 14; OT-6 covers every skill's prose.

## DEFINE sites (exact text)

**AGENTS.md line 43 (1.2):**
> **Toolchain, not sources.** OpenSysML (opensysml.org) is the open-source SysML v2 tool stack; this tutorial uses two of its components and names them by role, **the OpenSysML runtime** (Go; `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and **sysml-toolkit** (Rust; `sysmlv2` binary; pinned v0.9.1). A bare "OpenSysML" is a statement about the stack; a claim that is true of, or was probed against, one component names that component, and a version number attaches to a component name. The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such; it is not one of the two tools the chapters run. All of these execute the specs. They are cited only to flag a spec gap (§1.9), never to define a term.

**AGENTS.md line 127 (1.7 bullet):**
> - The OpenSysML runtime v0.9.0 does not resolve `import` across separately loaded sources (sysml-toolkit v0.9.1 does, D-017). A notebook therefore assembles the SysML text from the imported modules plus its explicit increment into one source and loads that (gap G7, §1.9).

**AGENTS.md line 139 (1.9 surface 1):** `1. \`model.query()\` in the OpenSysML runtime: the API Query (select, where, scope, inverse; no traversal). It sees named elements only. Name your allocations, connections and flows and it sees those too.` (line 143 unchanged)

**AGENTS.md line 145 (fuel-port parenthesis):** `(the OpenSysML runtime v0.9.0 and sysml-toolkit v0.9.1 both accept a power port connected to a fuel port; the KerML 1.1 spec searched has no validation constraint for it)`

**CLAUDE.md lines 19-20 (tail of the sources paragraph):** `The OpenSysML runtime and sysml-toolkit, two components of the OpenSysML stack (opensysml.org; AGENTS.md 1.2), are toolchain, cited only to flag spec gaps.`

**docs/references.md "OpenSysML" section (heading unchanged):**
> ## OpenSysML
>
> OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial uses two of its components and names them by role: the OpenSysML runtime (Go; repository `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such.
>
> The OpenSysML runtime: Open-MBEE/OpenSysML. <https://github.com/Open-MBEE/OpenSysML>
>
> The OpenSysML runtime's Python package (`opensysml==0.9.0`), used to load, validate, evaluate, and query SysML v2 models in this tutorial. All model loading uses `conn.load_from_content(content, strict=False)`. Gaps between the runtime's current API and the SysML v2 specification are tracked in [DEFERRED.md](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md) and as issues in this repository and upstream.
>
> sysml-toolkit: Open-MBEE/sysml-toolkit. <https://github.com/Open-MBEE/sysml-toolkit>
>
> The Rust toolkit (`sysmlv2` binary, pinned v0.9.1), used in Chapter 8 for `sysmlv2 verify --solve` through `toaster.modelcheck`, and for the cross-checks recorded in DEFERRED.md.

(The builder preserves any existing link/anchor/text in that section that this block does not change, and keeps the
`Open-MBEE/OpenSysML` and `Open-MBEE/sysml-toolkit` URLs byte-identical.)

**D1, docs/setup.md, new paragraph inserted before line 136 (existing text continues unchanged):**
> OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial uses two of its components and names them by role: the OpenSysML runtime (Go; repository `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such; it is not one of the two tools the chapters run.

**D2, docs/reproducibility.md, new paragraph after line 12:**
> OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial pins two of its components: the OpenSysML runtime (Go; `Open-MBEE/OpenSysML`; Python package `opensysml`; v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; v0.9.1, pinned with Z3 and the standard library in `scripts/tool-pins.json`). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline.

## DEFERRED.md
**Top note** (insert after `# Deferred work`, before `## D-001`):
> **Terminology note (2026-10-03, DL-116, DL-117).** OpenSysML (opensysml.org) is the open-source SysML v2 tool stack; this tutorial uses two of its components, the OpenSysML runtime (Go; `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; pinned v0.9.1). Entries written before this note use a bare "OpenSysML" (and "opensysml") for **the OpenSysML runtime**; read them that way. Headings are unchanged because their anchors are linked from published pages, and Workaround, Resolution, Upstream-issue and Status lines are unchanged because they are dated record; `OpenSysML#NNN` references are issues on the runtime's tracker. Where an entry records a different result for sysml-toolkit (D-017, D-019, D-023, D-034, D-035, D-036), the heading describes the runtime's behavior only and the body states what sysml-toolkit v0.9.1 does.

**D-035 line 878 factual correction** (SEPARATE COMMIT in OT-5; explicitly authorized; replaces the sentence from "This is the same three-way disagreement shape" to "not less."):
> This is the same disagreement shape as D-034 (one pinned tool disagrees with the other two on a real construct's validity), but in the OPPOSITE direction: there, the OpenSysML runtime was the outlier tolerating something the other two correctly rejected; here, sysml-toolkit alone is the outlier, MORE permissive than the other two, not less. **Corrected 2026-10-03 (DL-117):** this sentence originally also cited D-032 and D-033 as one-of-three cases; D-032 records sysml-toolkit accepting the construct too, and D-033 is a runtime display defect with no three-way comparison.

(B-066's first replacement, "confirmed correct against the OpenSysML runtime v0.9.0", stands.)

## Learner-surface rulings (inventory-a)
- **UNPROBED rows (R032, R037, R042, R044, R060, R065, R075, R091, R096, R097, A03; D-028/R? as RUNTIME):** rewrite to name the
  runtime; add NOTHING about sysml-toolkit and no "not probed" sentence in learner text. **R097 final:**
  `**Tool support.** Neither the OpenSysML runtime nor the pilot flags` (no parenthesis).
- **R125** (exercises/ch07 `cell-0` L48-49): accept `which the OpenSysML runtime loads silently but` and A04 `and the OMG SysML v2 Pilot Implementation both flag`. Residual (note in the OT-3B report, do not block): decisions/log.md:876 does not record the pilot flagging `done` specifically.
- **A09** (case study L129-130): `That is a semantic property no diagnostic of the OpenSysML runtime or the pilot computes.` (A06 at L60 must give the Pilot its full name first; apply in file order.)
- **A10-A14:** name sysml-toolkit where D-030/D-031 behavior is attributed:
  - A10 (ch08 nb01 `cell-07`): `because sysml-toolkit's solver never reaches through to either one`
  - A11 (ch08 conclusion L13): `sysml-toolkit's \`verify --solve\` does not compose two separately declared \`assert constraint\`s (whether sibling or inherited) and cannot reason through a chained calc invocation`
  - A12 (ch08 index L11): `sysml-toolkit's \`verify --solve\` does not compose separately declared constraints, and cannot reason through a chained calc invocation`
  - A13 (exercises/ch08 `cell-14`): `D-030 says sysml-toolkit's Z3 backend does not compose two separately`
  - A14 (exercises/ch08 `cell-16`): `sysml-toolkit's Z3 backend never composes two separately declared \`assert`
  "This toolchain" stays only in sentences that are genuinely generic (the inventory's "reviewed, no change" list stands).
- **FALSE-UNDER-STACK finals** (a sysml-toolkit contrast appears at most once per page, at the sentence whose point is the hole):
  - **R066** (ch07 nb02 `cell-09`): `The OpenSysML runtime v0.9.0 keeps a transition's trigger only as a string and never resolves it against \`Start\`, \`Finish\` or \`Cancel\`: a typo, or a reference to a name the model never declares, loads without error and simply never fires`. Same cell, new sub-row: `catches what the tool does not` → `catches what the runtime does not`.
  - **R069** (`cell-23`): `The OpenSysML runtime loads the typo cleanly (the \`OpenSysML itself\` line printed above is the runtime's verdict): \`Strat\` never fires, and nothing in the runtime says so; sysml-toolkit v0.9.1 resolves trigger names and warns on a broken reference (D-023).` A02: `The runtime has a real hole here`. (The stored output line is `OpenSysML itself: typo_model.ok=True`; the wording must match it.)
  - **R070** (`cell-25`, caption): `invisible to the OpenSysML runtime's own loader.` (drop the parenthesis)
  - **R074** (ch07 conclusion L13): `The OpenSysML runtime v0.9.0 does not resolve a transition's trigger against the item def it names;` (drop "where sysml-toolkit v0.9.1 does"). A05: `the runtime lets through silently`.
  - **R112** (docs/setup.md L147): `**sysml-toolkit** does one thing the OpenSysML runtime cannot yet:`
  - **B-002** (AGENTS.md 1.7): as the 1.7 text above.
- The inventory's other proposed wording stands where this file is silent. Where a row's wording is silent AND the convention
  does not settle it, STOP and report.

## Notes for later contracts
- **OT-7 (lint):** `glossary/lint.py` must be checked for what it scans; the new rules must apply to markdown cells and `.md` files
  only (protected code-cell strings in ch07 nb02 `cell-22` and ch03 nb04 `a1b2c3d4` would match `OpenSysML itself` and `OpenSysML v0.9`).
- **OT-6 (ACE edits skills):** all 15 skills' prose; B-082 and B-084 finals above; record the pre-edit revert SHA.
