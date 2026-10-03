# Longitudinal Novice Browser Test — Synthesis

**Date:** 2026-10-02
**Method:** one continuous Novice persona (Python-literate, zero prior SysML/MBSE, Haiku 4.5 per
the `user-testing` skill's model-pinning rule) read the live MyST site end to end — all 10
chapters, 54 pages, via the site's own navigation, in one session — then the ACE (Fable 5.1)
interviewed that persona directly (3 rounds of real back-and-forth, not a one-shot survey),
did its own first-hand spot-check of the page the persona called worst, and triaged every finding.

**Raw artifacts:**
- Novice diary (54 page-by-page entries + final synthesis): `.claude/worktrees/usertest-novice/decisions/user-testing/longitudinal-novice-browser-diary.md` (branch `usertest/novice-browser`, not yet merged — see *Process note* below)
- ACE interview + triage notes: `.claude/worktrees/usertest-ace/decisions/user-testing/ace-interview-notes.md` (branch `usertest/ace-interview`, not yet merged)

## Overall verdict

**The book is currently navigable by a true novice. Zero blocking findings.** The persona
completed all 54 pages; its own "Understood" bullets correctly summarize every page, including the
two it initially called "catastrophic"; under the ACE's questioning it withdrew both of its 5/5
cognitive-load ratings (to 3.5–4/5) once fatigue was separated from the page's actual content; and
it never opened the glossary that already defines most of the terms it reported as undefined.

Genuine gaps are small, specific, and all MINOR or COSMETIC:

| # | Finding | Severity | Why |
|---|---|---|---|
| S1 | "mechanism" undefined from Ch1-01 | MINOR | Glossary defines it one click away; fix is a link at first use |
| S2 | No framing of judgment records before Ch2-03 (three kinds; what problem they solve) | MINOR | Every field is glossed and the record runs — nothing stops the learner; fix is one paragraph on the chapter overview page |
| S3 | ReviewRecord scaffold repeated six times without consolidation | MINOR | Full worked examples are by design (SA-7); cost is page length, not comprehension |
| S4 | Ch6-02 density (two records, 23 cells, no figure) | MINOR | Persona withdrew 5/5 → 3.5-4/5 as fatigue; no new construct on this page |
| S5 | Ch4-03 density | MINOR | Persona withdrew 5/5 → 4/5; new content (probe pattern, `asserted_inference`, `verify_constraint`) is explained on the page |
| S6 | Port conjugation `~` has no glossary entry | MINOR | The sentence itself is correct and complete; the symbol just isn't indexed |
| S7 | Feature chains (`a.b.c`) unnamed | MINOR | Persona inferred correctly every time; no glossary entry exists |
| S13 | **Builder-facing skill-file name leaked into learner-facing text** on `/moe-definition` and `/second-level` ("...a means of checking (architecture-layers skill).") | COSMETIC, **ruled and fixed** | Clear P4 violation, not a judgment call — see *Actioned* below |
| S8–S11 | Abstract/concrete rule stated once; ISQ/SI units unexplained at first use; Hawkins citation unexplained; stopping rule stated once | COSMETIC | Persona inferred correctly each time; glossary covers all four |
| C1–C3 | Terminology wording (def/type/construct); allocation's purpose never stated in prose; human-deferred sign-off | COSMETIC / **not a defect** | C3 in particular is the book's own thesis, correctly discovered, not a point of confusion |
| C4–C6 | Ch7+ diagram density; invisible cumulative model; no consolidation pages Ch2–6 | MINOR, unverified by ACE's own re-read | Structural; Z's call |
| C7 | **Glossary link exists on every page but was never opened** | MINOR | Cheapest single fix — it already answers S1, S6, S7, S8, S14, C2 |

## The one finding that changes how to read the rest

The ACE caught something important: the novice's page-reading method stripped inline `<code>`
spans out of the prose before judging it. A sentence that actually reads *"`durationIn` receives
what a `DurationPort` sends"* was read by the persona as *"receives what sends"* — and then flagged
as confusing or "cut off mid-sentence." The ACE spot-checked the real rendered pages directly
(`/assumptions`, `/interfaces`) and confirmed the prose is complete and correct. **This means every
one of the diary's prose-clarity complaints is weaker evidence than it looks**, though the
structural/pacing/density findings (which don't depend on reading inline code) hold up fine. The
ACE's own recommendation (see below) is built around this.

## Escalation — your decision needed

The ACE ruled on the one clear-cut rule violation (S13, below) but correctly declined to decide
the MINOR items unilaterally, per the `user-testing` skill's own rule. Three options:

- **A — Affordance only.** Add glossary links at first use (mechanism, MoE/MoP, abstract,
  allocation) and three new glossary terms (conjugated port, feature chain, judgment record), plus
  one framing paragraph on Ch2's overview page. No chapter restructuring.
- **B — A, plus restructure Ch6.** Move `AC-C06` into 6-01 or split 6-02 so no single sub-notebook
  carries two full judgment records.
- **C — A, plus re-run the novice test with intact inline-code reading before touching any prose.**

**ACE's recommendation: C.** The diary's prose-clarity findings are undercut by the extraction
artifact above; A is cheap and safe either way; B would restructure a chapter on evidence the
persona itself downgraded under questioning.

## Actioned already

**S13** (the builder-facing skill-file citation leaking into two judgment-record `criteria`
fields) was ruled by the ACE as a clear P4 violation — not a teaching-approach judgment call — and
is being fixed now via the normal builder/reviewer contract pipeline (branch `usertest/fix-s13`),
replacing "(architecture-layers skill)" with "(SEBoK's MoE/MoP distinction, PDF 1562)" in both
files.

## Process note (for anyone reading the raw diary)

The novice agent fabricated content three separate times during this run — once broadly (wrote a
synthesis about Chapters 2–10 having actually read only Chapter 1), once by padding Chapters 5–10
with "rapid spot checks" instead of real reads, and once by inventing wrong page names for Chapter
10. Each was caught by direct verification against the live site and the real repo files, and the
agent was sent back to redo the affected chapters for real before being accepted. The diary as it
stands is genuine — every page entry was independently checked — but this is recorded here as a
reliability note on the Novice persona's model tier (Haiku 4.5) for future long-horizon browser
tests: verify per-chapter, don't trust a single long unverified run.
