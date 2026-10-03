# Case study: tying a proved lemma to a stated requirement

**Date:** 2026-09-30
**Status:** resolved — direction adopted (B, revised); `assert satisfy` drop confirmed by direct
test, not argument alone; implementation pending integration
**Related:** [`decisions/next-passes.md`](https://github.com/Open-MBEE/toaster/blob/main/decisions/next-passes.md) item 29; [`decisions/log.md`](https://github.com/Open-MBEE/toaster/blob/main/decisions/log.md) DL-070, DL-071, DL-072 (and the entry recording this decision); SysML v2 formal/2026-03-02 §7.20–7.21, §7.24

## Why this document exists

This is not a chapter of the tutorial and not a terse decision-log line. It is a record of a
real episode of engineering judgment: resolving a question the SysML v2 specification does not
settle on its own, using the spec's letter, the spec's expressed intent, two independently built
candidate models, live tool behavior, and a direct argument about what our own model actually
means. The question itself — *does a formal tie between a proved property and a stated
requirement actually say what we mean it to say* — is exactly the kind of judgment this tutorial
teaches ([AGENTS.md](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md): "judgment is the engineer's expertise, exercised with justification and never
eliminated"). This document is the full working, kept because the working is the point, not just
the two lines of SysML it ends in.

## The problem

Chapter 8 proves a real-arithmetic lemma, `deliveredEnergyBoundedBySupply`
([`models/ch08-cumulative.sysml`](https://github.com/Open-MBEE/toaster/blob/main/models/ch08-cumulative.sysml)), for every value its unbound features admit, using
`sysml-toolkit`'s Z3-backed `verify --solve`. Chapter 10's own traceability search —
`requirement_ties`/`tied_to_any_requirement` ([`src/toaster/query.py`](https://github.com/Open-MBEE/toaster/blob/main/src/toaster/query.py), finalized after several rounds of broadening and then deliberately narrowing) — correctly reports that this
lemma is tied to no stated requirement at all. This was originally treated as intentional
pedagogy: the inverse of Douglas's own "unjustified widget" concern (a design element with no
requirement behind it), here a piece of formal evidence with no requirement behind *it*.

mzargham (Z) reconsidered this (chat, 2026-09-30): using something that plausibly *should* be tied as the
worked example of something that is *not* tied is confusing. The decision was to add a real tie,
and to preserve the "unjustified widget" pedagogy separately, with a freshly constructed fixture
built specifically to be untied.

## Two independent attempts, same day

Two different designs for the tie were built independently, in parallel, without either one aware
of the other:

**Approach A** (built this session, reviewed twice, merged, then revisited): a `requirement def
EnergyConservationReq` with an explicit `subject heatGen : HeatGenerator`, a `require constraint
:> deliveredEnergyBoundedBySupply`, and a `verification def EnergyConservationTest` (§7.24
Verification Case) mirroring this model's own existing `TimelyToastTest` precedent. Placed in
Chapter 8, alongside the proof.

**Approach B** (found afterward, in an existing unmerged worktree, commits from the same day): a
`requirement def EnergyConservationReq` with *no* declared subject (inheriting the library
default, `Anything`), the same `require constraint :> deliveredEnergyBoundedBySupply`, *plus* an
explicit `assert satisfy energyConservationReq by deliveredEnergyBoundedBySupply;`. Placed in
Chapter 10, at the point the gap is found, with a new Hawkins `asserted_context` judgment record
(`AC-C10`) directly naming the risk that a requirement identified *from* existing evidence, after
the fact, is circular.

Independent review of Approach A (a different model than the author, two full cycles) found a
real test-suite weakening but did not catch a deeper defect: `EnergyConservationReq`'s declared
subject (`heatGen : HeatGenerator`) was never actually used by its own required constraint, which
is stated purely over unrelated free-standing elements. This is a real violation of §7.21.1's
subject-conformance *spirit*, found by re-reading the spec directly, not by any tool diagnostic —
**correction (found during review of the reconciliation contract, see below): Approach A never had
an `assert satisfy` line at all, so the OMG pilot had no live binding to flag on it, and running
the pilot against Approach A's own committed model directly confirms 0 issues.** The pilot
diagnostic ("Bound features should have conforming types") belongs to a different draft:
Approach B's *own first commit* paired a typed subject with an `assert satisfy
energyConservationReq by deliveredEnergyBoundedBySupply;` line, and *that* combination is what the
pilot actually flagged — confirmed directly against that commit's own model. B's author fixed it
two commits later by dropping the subject declaration. So two different defects, in two
different places, were each found a different way: Approach A's (a declared-but-unused subject,
no live binding) by direct spec reading; Approach B's own first draft's (a typed subject *plus* a
real, type-inconsistent binding) by the pilot's own mechanical check. Neither tool nor either
review process caught Approach A's own defect; it took re-reading §7.21.1 directly, later, to
name it.

## The trade study

Compared on three axes, in the priority Z set: spec faithfulness, didactic clarity, tool usage.

- **Spec faithfulness.** B is correct where A (as merged) violated a binding rule. A's one
  advantage — demonstrating §7.24's Verification Case mechanism — is real but not required, and a
  hybrid (C: B's fix plus A's verification case layered on top) was probed and found spec-clean
  (the verification case's own local subject narrowing from `Anything` to `HeatGenerator` is a
  legal specialization, not a repeat of A's bug) but added real cost: more surface area for a
  second worked example of a construct already shown once (`TimelyToastTest`), and a genuine,
  unresolved chapter-placement tension (the tie belongs where the gap is found, Chapter 10; a
  verification case arguably belongs where verification mechanics live, Chapter 8).
- **Didactic clarity.** B wins clearly: `AC-C10` continues this tutorial's own established voice
  (every major judgment — `AS-C06`, `AS-C08`, `AI-C06`, `AI-C10` — names its own limits rather than
  asserting a clean result), closes the gap in the same chapter that finds it, and keeps the
  exercise mirror in sync. A added a new tie with no judgment record at all.
- **Tool usage.** Close to even; B runs the live solver and captured its output as cited evidence;
  A had two independent review cycles but on a less demanding check.

Z's direction at this point: lean B, but verify two specific things about B's own design before
committing to it.

## The deep interrogation: is `assert satisfy ... by <a constraint>` legitimate?

This is the substantive part. Two questions were asked: does it contradict the spec, and does it
manufacture an unnecessary substitute for something the spec already provides. Both were answered
by reading the spec directly (§7.20.1–7.20.3, §7.21.1, §7.21.2, §7.21.4), not by inference from a
single worked example, and the answer required looking at the same fact from several different
angles before it became clear enough to act on.

**The letter of the rule.** `assert satisfy energyConservationReq by deliveredEnergyBoundedBySupply;`
is grammatically legal and loads cleanly under OpenSysML. The one binding constraint the spec
states — §7.21.1's "a requirement usage can only be satisfied by an entity that conforms to the
definition of its subject" — is satisfied once the subject is left undeclared (inheriting
`Anything`, which everything conforms to). Nothing in the grammar or the type system forbids this
construction. On the letter alone, it is fine.

**The expressed intent.** The letter is not the whole of the rule. §7.21.1's own account of
"Requirement Satisfaction" states the *purpose* of a satisfy requirement usage directly: it
"asserts that a requirement is satisfied when a given feature is bound to the subject
parameter... which means that the required constraint... must be true **when** [an attribute] **is
bound to** [the candidate's value]." The spec's own worked example (`maximumVehicleMass`
satisfied by `c1`) only works because the requirement's formula is *written in terms of the
subject* (`massActual <= massRequired`, with `massActual` later redefined to `vehicle.totalMass`).
Binding is supposed to *do something*: substitute a real candidate's values into a formula that
depends on them, and the formula's truth or falsehood then genuinely depends on which candidate
you picked. `EnergyConservationReq`'s own required constraint, `c :> deliveredEnergyBoundedBySupply`,
never mentions its subject anywhere — the lemma it subsets is a closed proposition over its own
free-standing elements. Binding anything to the subject changes nothing about whether the
constraint evaluates true. The construct's grammar is satisfied; its purpose is not exercised.

**Tool support.** Neither OpenSysML nor the OMG pilot flags *this specific line* (Check A as finally
written, subject-less). The pilot does catch a live binding type-mismatch — confirmed directly
against Approach B's own first draft, which paired a typed subject with this same `assert satisfy`
line and drew "Bound features should have conforming types" — but there is no tool check for "this
satisfy usage's binding is causally irrelevant to the requirement's own truth value" even when the
types happen to line up, which is the finally-written version's own problem. That is a semantic
property no diagnostic in this toolchain computes. This matters for the
methodology, not just the conclusion: a construct passing every available tool check is evidence
it is *legal*, not evidence it is *doing what it looks like it is doing*. The absence of a tool
complaint was never going to settle this question.

**Our model's own context.** The spec's own reusable-constraint worked example, `massLimit`, is
authored as an *open template*: it declares its own `in mass`/`in massLimit` parameters
specifically so a reusing requirement can rebind them to the subject's own values
(`require massLimit { :>> mass = massActual; :>> massLimit = massRequired; }`). `deliveredEnergyBoundedBySupply`
was never authored that way — Chapter 8 built it as a fully closed, already-evaluated proposition
over its own `heatGenCheck`/`heatGenCheckDuration`, precisely because its whole point was to be
proved once, universally, not instantiated per candidate. Subsetting it into a requirement's
required constraint (Check B) is a legitimate reuse of a closed fact. Trying to additionally
*satisfy* it with a candidate (Check A) presupposes an open template that was never there to begin
with.

**Our model's own intent.** What we actually want to claim is narrow and already fully available
without `satisfy`: "this universally-quantified, Z3-proved property establishes that this stated
requirement's own formal condition holds." We do not want to claim "here is one candidate, and
under its particular values this requirement comes out true" — that is a strictly *weaker* claim
(a point check, not a universal proof), and it is exactly the kind of check this tutorial already
criticizes elsewhere (`timely`'s own point-evaluation limits, Chapter 3 and Chapter 8's own
contrast between `verify_satisfaction()` and `verify_holds()`). Reaching for `satisfy` here would
not just be unnecessary, it would misrepresent the kind of evidence actually in hand.

**Judgment about "good enough."** §7.21.1 states the satisfaction criterion directly: "since a
requirement is a kind of constraint, a requirement can be evaluated to be true or false. A
requirement is satisfied when it evaluates to true." `EnergyConservationReq`'s own required
constraint already evaluates true, by construction (it *is* the proved lemma). That is the
requirement satisfied, in the spec's own words, with no `satisfy` usage needed at all. Checking
this directly against the project's own finalized checker closes the loop: `tied_to_any_requirement`
already returns `True` from the subsetting relationship alone (Check B), independent of whether any
`assert satisfy` is ever written. Good enough was already reached one step earlier than either
branch's own design assumed.

**Judgment about appropriate representation.** There are two different registers available —
a requirement definition's own formal content (what the requirement *is*), and an instance-level
satisfy claim (what candidate *meets* it) — and the spec keeps them genuinely distinct for a
reason: one is a template, the other is a claim about a specific filling of that template. The
right register for "a general physical law, independent of any one proof of it, now established
as this requirement's own content" is the first. Reaching for the second register, because it
happens to also be legal and because it adds a second hit in our own traceability search, is a
representational mismatch — using the syntax built for "candidate satisfies requirement" to mean
something closer to "this evidence is cited by this requirement," which is a different relationship
the model already states more directly through subsetting.

**And one more: writing to the checker versus writing to be true.** The sharpest form of Z's
second question, stated plainly: Check A was not needed by `tied_to_any_requirement` (Check B
already succeeds alone), was not asked for by the requirement's own semantics (the binding does no
work), and existed in Approach B's design for reasons closest to "give the tie-detector a second
way to find it." That is a trap specific to tool-assisted, checker-driven development: a model
element that makes an automated check pass *feels* like confirmation, but passing a check you wrote
is not the same evidence as a construct doing the job its own specification says it does. The
"unjustified widget" this chapter is specifically about traceability gaps; manufacturing a
construct to close one gap, in a way the construct's own spec semantics do not support, would be
a second, quieter instance of the same failure mode in reverse.

**Empirical confirmation, not just argument.** Z was not convinced by the argument above on its
own — correctly: an abstract claim that a construct "does no evaluative work" deserves to be
checked against the tool, not just read off the spec text. Two things were verified directly
rather than asserted.

First, the base library itself settles where subject-dependence actually comes from.
`Systems Library/Requirements.sysml`'s own `RequirementCheck` defines `result =
allTrue(assumptions()) implies allTrue(constraints())` — a pure function of the requirement's own
nested constraint features. `subj` is not referenced anywhere in that computation; a requirement's
truth depends on its subject *only if* one of its own required or assumed constraints happens to
reference the subject's own features (exactly what the spec's worked example, `massLimit`, does
via `:>> mass = massActual`, and exactly what `EnergyConservationReq`'s own `require constraint c
:> deliveredEnergyBoundedBySupply` does not do).

Second, this was tested directly against `model.verify_satisfaction()` — the tool's own
point-evaluation engine, the same one a reader would reach for expecting confirmation, the same
way `heatGenerationReq`'s own real `assert satisfy ... by rated` / `by weak` claims are confirmed
elsewhere in this model. Three variants of `assert satisfy energyConservationReq by X;` were built
and run with `X` bound to the lemma itself, to a totally unrelated part, and to `heatGenCheck`
itself. **All three produced the identical verdict — not a pass, an error:**
`require condition evaluation failed: no value for feature heatGenCheck.efficiency`. The binding
is not merely logically inert; the construct cannot be evaluated at all, for the structural reason
already named above (`heatGenCheck`/`heatGenCheckDuration` are deliberately left free, since the
whole point of the Z3 proof is that it holds for every value, not one). A reader who tries to
confirm this claim the way the tutorial has already taught them to — by running
`verify_satisfaction()` — gets an error, not the pass a skim of the model would suggest.

This also sharpens what `AC-C10`'s own cited evidence (`requirement_coverage(...)` reporting
`covered=True`) actually is. `requirement_coverage()` ([`src/toaster/query.py`](https://github.com/Open-MBEE/toaster/blob/main/src/toaster/query.py)) never runs the
constraint at all — it checks only whether a non-negated `SatisfyRequirementUsage` node *exists* in
the API-JSON export. `AC-C10` already describes this carefully as "a point-evaluation claim about
the assert satisfy declaration's own success, not the same claim as the solver output," which is
honest, but the test above shows it is thinner still: it is not evaluating the declaration's
success, only the declaration's existence and polarity. The one thing in this whole model that
actually *runs* the check errors out identically no matter what is bound.

**And the honest residual: is the tie itself circular?** Dropping Check A does not touch this
question, which is Approach B's own real contribution via `AC-C10`: `EnergyConservationReq`'s
*need* was identified after Chapter 8's proof already existed, specifically to close the gap
Chapter 10's own search found. `AC-C10` names this directly rather than hiding it, and argues
(not asserts) that it is not fully circular because the underlying physical law would be a real
constraint on any heat generator design whether or not Chapter 8 had proved anything about it —
the timing of *noticing* the need is retroactive; the law's own validity is not. This is a real,
separate judgment call from the `satisfy`-by-constraint question, and it is the one genuinely
assurance-deficit-shaped question this whole episode leaves open, named rather than resolved.

## The strongest case for keeping it, considered and set aside

Before settling this, the steelman for keeping `assert satisfy ... by deliveredEnergyBoundedBySupply`
was given its own hearing, not dismissed by default: it is a legible, standard-idiom pointer
("here is what satisfies this requirement") that a skim of the model would find immediately, and
it keeps `EnergyConservationReq` stylistically consistent with its siblings (`heatGenerationReq`,
`timely`), which both do get an explicit `assert satisfy ... by ...`. Both points are real.

They are outweighed by what the empirical test shows: a reader who treats this `satisfy` line the
way the tutorial has already taught them to treat its siblings — by running
`verify_satisfaction()` to confirm it — gets an error, not a pass, and gets the identical error no
matter what is bound as the satisfying feature. A construct that looks, on a skim, like the same
kind of claim as `heatGenerationReq`'s real, checkable ones, but silently behaves differently the
moment it is actually exercised, is a worse outcome than the construct's absence. The legitimate
part of the stylistic-consistency instinct — that an omission should be legible, not silent — is
kept, just by a doc comment instead of a claim that does not hold up when run.

## The decision

Adopt Approach B, revised: keep the subject-less `EnergyConservationReq` (§7.21.1's own
explicitly sanctioned degenerate case), keep the `require constraint :> deliveredEnergyBoundedBySupply`
subsetting (§7.21.2's own sanctioned reuse idiom), **drop** the `assert satisfy
energyConservationReq by deliveredEnergyBoundedBySupply;` line — confirmed by direct test against
`verify_satisfaction()`, not argument alone, to error identically regardless of its own binding —
and in its place add one doc-comment sentence on `EnergyConservationReq` stating plainly why no
`assert satisfy` is given: the requirement's subject carries no distinguishing value, and
attempting to satisfy it produces an evaluation error, not a pass. Keep Chapter 10 as the
placement (fix the gap where it is found), keep `AC-C10` (revised to no longer lean on Check A as
part of the tie — its own evidence should cite the test above rather than `requirement_coverage()`'s
thinner existence check), and keep the exercise mirror in sync. Approach A's branch (already
merged) is to be reconciled against this — the subject-type defect and the unnecessary
verification case both need to come out.

## What we learned (methodology, not just outcome)

1. **A spec settles legality, not appropriateness, on purpose.** Nothing in §7.21 forbids
   `satisfy`-by-constraint. The spec cannot rule out every representational mismatch its own
   grammar permits — that judgment is left to the modeler, every time, and a construct loading
   without diagnostics is never sufficient evidence it is being used for what it is for.
2. **Passing a tool check and fulfilling a construct's own purpose are different claims.**
   Approach A's reviewer (a different model, two full independent cycles) reasoned about the
   subject-type oddness as an open question without identifying it as a defect, and no tool flagged
   it either, because Approach A never attempted a live binding for any tool to check — its problem
   was a declared-but-unused subject, invisible to a diagnostic that only fires on an actual
   type-mismatched binding. The OMG pilot *does* catch a live type mismatch, as it did on Approach
   B's own first draft, but a clean pilot run is not evidence a construct is doing its job, only
   that nothing it actually tried to bind was mistyped. Every available tool check passing is
   necessary, never sufficient.
3. **Two independent attempts at the same problem each surfaced a different real defect, neither
   caught by its own review.** Not planned redundancy — discovered by accident, after the fact —
   but real work: Approach B's own first draft hit a live, pilot-diagnosable type mismatch (fixed
   two commits later, before this reconciliation ever began); Approach A's own, different defect (a
   subject that was never wired to anything, so no tool had anything to check) was found only by
   directly re-reading §7.21.1, after merge, not by any diagnostic. Getting the attribution between
   these two right took a third pass — this document itself first conflated them, and an
   independent review of the reconciliation work that implements this decision caught the
   conflation and this correction is its result.
4. **Writing the rationale out, at each step, in the open, is what made this resolvable at all.**
   Not the chosen two lines of SysML — the explicit record of *why*, at every branch point (the
   trade study, the hybrid probe, the six-angle interrogation above), is what let a plausible,
   tool-accepted, checker-satisfying construct be recognized as representationally wrong before it
   shipped. A model that only recorded the final answer would have looked identical to one that
   got here by accident.
5. **An abstract argument that a construct "does no work" is not the same as having checked it.**
   Z's own pushback on the first version of this document's conclusion was correct: the
   semantic-vacuity argument was right, but it was still only an argument until it was run against
   `verify_satisfaction()` directly. The test did not just confirm the argument, it found something
   the argument alone understated — the construct does not merely add no information, it errors
   when exercised the same way its own siblings are legitimately exercised elsewhere in this
   model. When a judgment call is reachable by direct test, run the test; do not stop at a
   convincing-sounding argument that a thirty-second script could have checked.
