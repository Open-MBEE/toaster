# Pass 4, run 001: Chapter 1 re-derivation (2026-09-27)

Contract PASS4-001. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model each
round), three review rounds. All four fixes were already ruled by prior DL entries
(DL-018/019/020/021, plus the orchestrator's own scoping call on `Heater`) — this contract
executed an already-determined target, not a new design question.

## What shipped

`models/ch01-cumulative.sysml`:
```sysml
package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;

    item def Bread;
    item def Toast;

    action def ToastBread {
        doc /* Transform bread into toast acceptable to its user. */
        in bread : Bread;
        out toast : Toast;
    }

    abstract part def ToastingSystem {
        perform action toastBread : ToastBread;
    }

    part def HeatingSystem;
    part def ControlSystem;

    part def Toaster :> ToastingSystem {
        attribute cycleTime : ISQ::DurationValue;
        part heating : HeatingSystem;
        part control : ControlSystem;
    }
}
```

- **F-1 (DL-018)**: `cycleTime` lost its default; it's a bare typed, unit-bearing slot now — no
  derivation attempted here, that's later chapters' job once the mechanism/energy-balance content
  exists.
- **F-3 (DL-019/020/021)**: the backwards `HeatingSystem :> ToastingSystem` /
  `ControlSystem :> ToastingSystem` are gone; `Toaster :> ToastingSystem` replaces them (the actual
  whole specializes the subject that names it). `ToastingSystem`'s bare `doc` became a real
  functional construct: typed `Bread`/`Toast` item defs, an `action def` with typed in/out flows
  carrying the acceptance language verbatim, and a `perform action`. `HeatingSystem`/`ControlSystem`
  stay concrete placeholders with no mechanism — correct for Ch1, not a defect (DL-020).
- **F-4**: `index.md`/`conclusion.md` no longer call this "the physical architecture layer" or
  "implementation-agnostic" in the same breath; the Expected-result section matches the model's
  real ISQ types; the stale "abstract modifier not yet supported" comment now correctly says it's
  an Editor-API authoring gap, not a parsing failure (`isAbstract: true` is confirmed in the export).
- **F-2, orchestrator's scoping call**: `Heater` removed from Ch1 entirely — it specialized
  nothing and connected to nothing there. Verified safe: each of ch02–ch08's cumulative fixtures
  independently re-declares `Heater` itself; none inherits from ch01's file.
- All four notebook seam cells rewritten to address the construct→tool→result connection
  behaviorally, per the just-landed DL-050/toaster-recipe fix — no naming of Tall, "the three
  worlds", or A-F/O-S/E anywhere in the chapter (confirmed by grep, both by the builder and
  independently by the reviewer).

## Review rounds

1. **Build**: re-derived the model, all 4 notebooks, `index.md`/`conclusion.md`, and the exercise;
   fixed the ch01 entry in `scripts/check_construction.py` (nb04 needed a `ToastingSystem` context
   stub). Found and reported, not silently patched: removing `cycleTime`'s default and adding real
   functional content broke the ch01→ch02 predecessor-containment invariant for the first time.
2. **My call**: recorded the ch01→ch02 gap as a positive assertion (mirroring the existing
   ch03→ch04 precedent exactly — a new test asserting the specific elements are missing, not a
   silent exemption), since Ch2's own re-derivation is next in the sequence and will need to carry
   these elements forward anyway. Accepted the builder's own scoping call to drop a
   numeric-default teaching moment from Ch1 rather than invent content on a placeholder to keep it.
3. **Review round 1: FAIL.** The exercise and nb01's own exercise pointer still taught the exact
   pattern DL-019 replaced (state the purpose as a `doc` comment) — nb01's cell 0 claimed the
   opposite. Also: a factually wrong "reopens" claim about SysML (no such mechanism exists), a
   miscited cell reference, a missing `perform` in `index.md`'s ingredient list, and a wrong spec
   citation for `ItemDefinition` (verified against the real spec PDF: §8.3.10.2, not §8.3.6).
4. **Push-back and fix**: exercise rewritten to fully mirror nb01's bundle (item defs, a
   flow-typed action def, `perform`); all wording/citation fixes applied. The builder
   independently re-checked one of the reviewer's own claims ("copied from ch04") before
   forwarding it and found it didn't hold — ch04 has no citation there at all, not a wrong one —
   and reported the correction rather than propagating an unverified claim.
5. **Review round 2: PASS.** Reviewer wrote and loaded a model answer to the corrected exercise to
   confirm it's actually solvable as written, and independently re-verified the spec citation
   against the same PDF pages. Also independently caught and corrected its own earlier mistaken
   claim before finalizing, matching the same discipline the builder had just shown.

## What the run showed

- **Every OQ this chapter's audit raised was already resolved by prior DL rulings** (DL-018
  through DL-022) — this contract needed zero new escalations, confirming the layer-audit →
  ACE-ruling → re-derivation pipeline this session built actually closes the loop it was designed
  for.
- **A contract executing an already-decided design still needs full review discipline.** The
  blocking finding (F1: the exercise contradicting its own chapter) wasn't a design ambiguity —
  it was an execution gap a careful independent reader caught by literally reading the cells word
  for word, which is exactly what the reviewer role is for.
- **Both agents independently re-checked claims — their own and each other's — before forwarding
  them.** The builder disproved its own forwarded citation-duplication claim (M5's "copied from
  ch04") before reporting it; the reviewer caught and corrected its own identically-shaped mistake
  in the very next round. This is the same discipline the Pass 4 Phase 0 trigger-guard saga
  needed across four rounds, working correctly here in three.
- **A newly-surfaced test gap (ch01→ch02 predecessor containment) was recorded as a positive,
  visible assertion of a known, expected, temporary state — not hidden by a skip or an exemption**,
  following the exact precedent already on file for ch03→ch04. This is the pattern to repeat for
  every subsequent chapter contract until the whole sequence is re-derived.

## Verification

287 tests passing (unchanged in count from Phase 0's close — one parametrized case swapped for one
new, equally-real test), `check_construction.py --check --chapter=1` consistent, `glossary lint`
shows zero hits from ch01 (down from 9 at baseline; 63 remain, all in chapters ≥3, untouched),
`glossary check` clean, 0 co-author trailers across 6 commits, worktree and branch cleaned up.

## Not fixed here, carried forward explicitly

- ch02's own prose still says `HeatingSystem`/`ControlSystem` "specialize `ToastingSystem`" (now
  false) and still discusses overriding `cycleTime`'s default (now gone) — Chapter 2's own
  contract's job, not silently left implicit.
- nb01's second spec citation ("§7.3.3 PartDefinition — AbstractClassifier", pre-existing, not
  introduced by this contract) still disagrees with the glossary's confirmed locators (§7.11.1
  part definition, §7.6.2 abstract definition) — a citation-cleanup backlog item, not blocking.
- M3 (the new ch01→ch02 test doesn't bound the exact failure set) — matches the existing
  ch03→ch04 precedent's own looseness exactly; not tightened, for consistency.
