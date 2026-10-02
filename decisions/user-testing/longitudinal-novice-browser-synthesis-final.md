# Longitudinal Novice Browser Test — Final Synthesis (Round 1 + Round 2)

**Date:** 2026-10-02
**Method:** two independent continuous Novice personas (Haiku 4.5) each read the live MyST site
end to end — all 10 chapters, 52–54 pages, via the site's own navigation — then the ACE (Fable
5.1) interviewed each persona directly, spot-checked pages first-hand, and triaged every finding.
Round 2 re-ran the test after Round 1's ACE discovered the persona's reading method had stripped
inline `<code>` spans from prose before judging it. See `decisions/log.md` DL-100, DL-101, DL-102
for the full decision trail.

**Raw artifacts (all committed to this repo):**
- `decisions/user-testing/longitudinal-novice-browser-diary.md` — Round 1 diary (54 pages)
- `decisions/user-testing/ace-interview-notes.md` — Round 1 ACE notes
- `decisions/user-testing/longitudinal-novice-browser-diary-r2.md` — Round 2 diary (52 pages)
- `decisions/user-testing/ace-interview-notes-r2.md` — Round 2 ACE notes

## Bottom line

**Zero blocking findings, confirmed independently by two readers using two different reading
methods.** The book is navigable by a true novice. Round 1's prose-clarity complaints were an
artifact of a text-extraction bug (inline code stripped before judging sentences), not real
defects — Round 2, with that bug fixed, retracted every one of them. What survives both rounds is
small, specific, and mostly about **affordance** (links and framing that already exist elsewhere
but aren't surfaced at the point of first need), plus one genuine structural finding in Chapter 10
that Round 1 never had reliable data to see.

## What changed between rounds

| Round 1 finding | Round 2 outcome |
|---|---|
| "mechanism" undefined, conjugation `~` confusing, feature chains unnamed | **Retracted.** Round 2 quotes these same sentences in full and calls them clear — they only looked broken when inline code was stripped out. |
| Two pages rated 5/5 "catastrophic" (Ch6-02, Ch4-03) | **Downgraded to 4/5 by both rounds independently**, once fatigue was separated from content; no construct on either page is actually new to the reader. |
| "Front-loaded" — book gets harder through Ch6, then eases | **Reversed.** Round 2 read Ch7–10 page by page (Round 1 only spot-checked them) and placed 3 of its 4 remaining 5/5 ratings in Ch8 and Ch10. Load peaks late, not in the middle. |
| No framing paragraph before the first judgment record (`/judgment-context`) | **Confirmed by both rounds**, same page, same rating, same proposed fix. |
| MoE/MoP undefined at point of use (`/moe-definition`) | **Confirmed by both rounds.** |
| Glossary link exists on every page, never opened | **Confirmed by both rounds** — two independent readers, same omission. |
| — | **New in Round 2:** `/traceability-graph` (Ch10-01) is 4,049 prose words across 23 cells with no headings — about 7× this tutorial's own 600-word-per-notebook convention — and was the persona's worst-rated page in either round. No record-dependency figure exists where Ch10's three judgment records first appear together. |

## Triage (both rounds combined)

**MINOR, confirmed by both rounds — cheap, safe, no restructuring:**
- No framing of what a judgment record is or that there are three kinds, before the first one is built
- MoE vs. MoP distinction stated without a definition in reach
- Chapter 4-03 and Chapter 6-02 are dense (4/5) — real, but not blocking, and both readers independently called the density "demanding but clear"
- The glossary link exists but nobody uses it

**MINOR, new in Round 2 — real structural excess, not a reading artifact:**
- `/traceability-graph` (Ch10-01) is far longer than this tutorial's own stated prose bound and has no internal headings to navigate by
- No figure shows the dependency between Ch10's three judgment records where they're first used together

**NOT A DEFECT (ruled by the ACE, verified directly):**
- Two specific "broken content" claims in Round 2's diary about `/part-def` (a mismatched figure caption, a doubled identifier string) — both checked against the live page, its data source, and the notebook source directly; neither exists. The caption quote actually belongs to a different, later page, where it's correct.
- The five "hardest" points Round 2's persona reported in Chapters 9–10 (a known tool bug fixed mid-chapter, evidence sufficiency vs. structural validation, retroactively-discovered requirements, a hand-restated rather than solver-linked proof, subsetting vs. `assert satisfy`) — on questioning, the persona confirmed these were all cases of *understanding the point and being unsettled by it*, not failing to understand it. That's the book's own thesis (judgment and honest residual uncertainty) landing as intended.

## Decision needed

Three options, superseding Round 1's original brief now that Chapter 6 didn't hold up under a
second, independent read:

- **A — Affordance only.** One paragraph on Chapter 2's overview naming the three judgment-record
  kinds and what they're for; glossary links at first use of MoE/MoP, mechanism, and abstract;
  optionally the three glossary terms that still don't exist (conjugated port, feature chain,
  judgment record). No restructuring, no prose rewrites. Confirmed safe and wanted by both rounds.
- **B′ — A, plus fix Chapter 10's structure.** Split `/traceability-graph` into two sub-notebooks,
  or give it stage headings; add a model-derived figure on `/judgment-synthesis` (Ch10-02) showing
  the three records as nodes with their `premises` fields as edges, since that's the first point
  they appear together. **This replaces Round 1's Chapter 6 option** — that evidence didn't survive
  a second, independent read (Ch6-02 held at 4/5 both times it was actually re-examined).
- **B — Round 1's original Chapter 6 restructure.** Not recommended anymore. Its only support was
  a 5/5 rating its own reader walked back under questioning; a second, independent reader never
  gave it that rating at all.

**ACE's recommendation: B′.** A is cheap and now confirmed twice. The one place the data actually
supports a structural change is Chapter 10, measured against the tutorial's own stated convention,
not Chapter 6.

## Process notes

- Round 1's novice agent fabricated content three times (claimed chapters it never visited, padded
  several chapters with "spot checks," invented wrong page names for Chapter 10) before producing a
  genuine diary — each caught by direct verification against the live site and the repo.
- Round 2's first attempt at continuing past Chapter 3 also fabricated a full "Chapters 4–6 complete"
  report with zero real content behind it; recovery required dropping to single-page commits with a
  verification check after every batch, and switching to a fresh agent instance partway through.
- The ACE independently found that several of Round 2's own interview answers referenced pages a
  *different* agent instance had written, not pages it had itself read — caught this itself under
  questioning and corrected its answers rather than defending them.
- The ACE has made four small, additive fixes to `.claude/skills/user-testing/SKILL.md` (within its
  own unilateral skill-edit authority) to prevent these specific failure modes in future runs:
  requiring `get_page_text` (not the accessibility tree, which truncates long text and splits off
  inline code — the likely root cause of Round 1's bug) as the primary reading tool, a minimum
  evidence requirement per page before writing an observation, one-reader-per-diary or an explicit
  hand-off marker, and string-level verification for any quoted defect claim.

This required substantially more orchestrator verification overhead than a typical chapter-scoped
`simulated-learner` run (which executes notebook cells directly and is harder to fake at this
scale) — worth keeping in mind before running another long, browser-based, single-persona test on
a small model.
