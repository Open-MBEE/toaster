# Pass 2, run 010: DL-046 corrected, and toaster.modelcheck built (2026-09-27)

## The correction

The first probe for DL-046 (does OpenSysML v0.9.0 support formal model checking) checked only OpenSysML and concluded negatively: no engine reaches beyond evaluating a fixed value, and DL-006 (an earlier decision scoping model checking out) was left standing. Z asked directly whether the capability was genuinely unreachable or only unreachable through that one tool, naming the Pilot Implementation as a fallback Z would rather avoid but accept if nothing else covered it.

Before reaching for the Pilot Implementation, sysml-toolkit v0.9.1's `verify --solve` (already rebuilt earlier in this pass) was checked and does exactly what was needed: it runs Z3 over undecided constraints and proves a property for all values of an unbound feature, not just evaluates one. Verified with a constructed tautology (`satisfied`), a contradiction (`VIOLATED`), and a bounded-range requirement in the TimelyToast idiom (`satisfied`). DL-006 is superseded; no Pilot Implementation needed. Every affected record (decisions/log.md DL-046, DEFERRED.md D-024, gap-issue-drafts.md Draft 8, pass4-backlog.md) was corrected same-day, with the retraction left visible rather than silently rewritten.

**Lesson:** a probe against one tool is not a probe against "the toolchain." When a capability search comes back negative, check every tool actually available before concluding a gap is real — especially when an earlier pass already inventoried a tool's relevant feature (sysml-toolkit's `verify --solve` was named in the original session's toolchain inventory before this pass began, and should have been the first thing tried, not OpenSysML alone).

## The build (contract PASS2-012)

Z's ruling on the remaining design question (subprocess vs. waiting for a Python binding): accept the subprocess call, but hide it behind a plain Python function, following the repo's standard gap-tracking pattern — patch and document with explicit intent to delete once a published package supports the capability natively (DEFERRED D-025).

`src/toaster/modelcheck.py`: `verify_holds()` and `holds()` wrap `sysmlv2 verify --solve`, parsing its text output (no `--format json` exists for `verify`, unlike `check`/`lint`) into a `ConstraintVerdict` dataclass. Builder Sonnet 5, reviewer Opus 5.5, three rounds:

1. **Build.** The builder verified the CLI's actual output format against the real binary rather than trusting the contract's assumed format, and caught several real divergences before the first hand-back (uppercase VIOLATED, an absent parenthetical on trivially-decided constants, a three-shape `--solve` reason format with an em-dash-appended witness segment on the undecided case).
2. **Review 1: FAIL.** Two real semantic bugs: `holds()` returned vacuous `True` on a file with zero constraints, and a definite VIOLATED verdict could be masked by an unrelated undecided one (raising "inconclusive" instead of returning `False`). Both contradicted the module's own stated purpose. Decided the fix directly (mechanical, not a judgment call): zero verdicts raises Inconclusive; violated always wins over undecided in the precedence.
3. **Push-back.** While building a genuine (non-trivial) test for one of the required coverage additions, the builder found and fixed, unprompted, a real bug beyond the six enumerated items: the summary line is not always stdout's last line (a `--ranges` narrowed-ranges report can follow it), which would have broken any real `ranges=True` call. Flagged explicitly rather than folded in silently.
4. **Review 2: PASS.** All fixes independently reproduced against the real binary with the reviewer's own constructed files, including the `--ranges` fix (confirmed broken at the pre-fix commit, working at HEAD). One non-blocking test gap left (one half of the exit-code/summary cross-check has no dedicated test, though the code itself was independently confirmed correct via a fake binary).

Integrated: 257 tests, ruff clean, `glossary check` passes, no co-author trailers across 8 commits total.

## What this run showed

- **Verifying a claim against reality caught a wrong conclusion before it became a permanent decision.** The orchestrator's own first-pass probe was wrong, and only got corrected because Z pushed back with a direct, specific question rather than accepting "not possible" at face value.
- **A builder that grounds its work against the real tool, not the contract's assumed shape, catches bugs the contract author (the orchestrator) couldn't have specified in advance** — this happened twice in one contract (initial format divergences, then the `--ranges` bug).
- **When a builder finds and fixes something beyond its contract's scope, flagging it explicitly (rather than silently including it, or silently omitting it) let the reviewer verify it specifically** rather than trusting it by association with the rest of the diff.
