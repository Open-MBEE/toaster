# Case study: tying a proved lemma to a stated requirement

**Date:** 2026-09-30
**Status:** resolved — direction adopted (B, revised), implementation pending integration
**Related:** `decisions/next-passes.md` item 29; `decisions/log.md` DL-070, DL-071, DL-072 (and the entry recording this decision); SysML v2 formal/2026-03-02 §7.20–7.21, §7.24

## Why this document exists

This is not a chapter of the tutorial and not a terse decision-log line. It is a record of a
real episode of engineering judgment: resolving a question the SysML v2 specification does not
settle on its own, using the spec's letter, the spec's expressed intent, two independently built
candidate models, live tool behavior, and a direct argument about what our own model actually
means. The question itself — *does a formal tie between a proved property and a stated
requirement actually say what we mean it to say* — is exactly the kind of judgment this tutorial
teaches (AGENTS.md: "judgment is the engineer's expertise, exercised with justification and never
eliminated"). This document is the full working, kept because the working is the point, not just
the two lines of SysML it ends in.

## The problem

Chapter 8 proves a real-arithmetic lemma, `deliveredEnergyBoundedBySupply`
(`models/ch08-cumulative.sysml`), for every value its unbound features admit, using
`sysml-toolkit`'s Z3-backed `verify --solve`. Chapter 10's own traceability search —
`requirement_ties`/`tied_to_any_requirement` (`src/toaster/query.py`, finalized at DL-070/DL-071
after several rounds of broadening and then deliberately narrowing) — correctly reports that this
lemma is tied to no stated requirement at all. This was originally treated as intentional
pedagogy: the inverse of Douglas's own "unjustified widget" concern (a design element with no
requirement behind it), here a piece of formal evidence with no requirement behind *it*.

Z reconsidered this (chat, 2026-09-30): using something that plausibly *should* be tied as the
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
subject-conformance rule, confirmed independently once Approach B's own commit history was found
and read — B's author had hit the same issue as a live tool diagnostic (the OMG pilot's "Bound
features should have conforming types") and fixed it by dropping the subject declaration
entirely. Neither review process caught this from reasoning alone; it took a second, independently
built candidate actually exercising a stricter tool to surface it.

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

**Tool support.** Neither OpenSysML nor the OMG pilot flags this. The pilot caught Approach A's
subject-*type* mismatch (a real, mechanically detectable defect), but there is no tool check for
"this satisfy usage's binding is causally irrelevant to the requirement's own truth value" — that
is a semantic property no diagnostic in this toolchain computes. This matters for the
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

**And the honest residual: is the tie itself circular?** Dropping Check A does not touch this
question, which is Approach B's own real contribution via `AC-C10`: `EnergyConservationReq`'s
*need* was identified after Chapter 8's proof already existed, specifically to close the gap
Chapter 10's own search found. `AC-C10` names this directly rather than hiding it, and argues
(not asserts) that it is not fully circular because the underlying physical law would be a real
constraint on any heat generator design whether or not Chapter 8 had proved anything about it —
the timing of *noticing* the need is retroactive; the law's own validity is not. This is a real,
separate judgment call from the `satisfy`-by-constraint question, and it is the one genuinely
assurance-deficit-shaped question this whole episode leaves open, named rather than resolved.

## The decision

Adopt Approach B, revised: keep the subject-less `EnergyConservationReq` (§7.21.1's own
explicitly sanctioned degenerate case), keep the `require constraint :> deliveredEnergyBoundedBySupply`
subsetting (§7.21.2's own sanctioned reuse idiom), **drop** the `assert satisfy
energyConservationReq by deliveredEnergyBoundedBySupply;` line as unnecessary and semantically
vacuous for the reasons above, keep Chapter 10 as the placement (fix the gap where it is found),
keep `AC-C10` (revised to no longer lean on Check A as part of the tie), and keep the exercise
mirror in sync. Approach A's branch (already merged) is to be reconciled against this — the
subject-type defect and the unnecessary verification case both need to come out.

## What we learned (methodology, not just outcome)

1. **A spec settles legality, not appropriateness, on purpose.** Nothing in §7.21 forbids
   `satisfy`-by-constraint. The spec cannot rule out every representational mismatch its own
   grammar permits — that judgment is left to the modeler, every time, and a construct loading
   without diagnostics is never sufficient evidence it is being used for what it is for.
2. **Passing a tool check and fulfilling a construct's own purpose are different claims.**
   Approach A's reviewer (a different model, two full independent cycles) reasoned about the
   subject-type oddness as an open question without identifying it as a defect; the OMG pilot
   caught the type mismatch but has no way to catch semantic vacuity. Every available tool check
   passing is necessary, never sufficient.
3. **Two independent attempts at the same problem surfaced something neither one's own review
   process found alone.** This was not planned redundancy — it was discovered by accident, after
   the fact — but it did real work: Approach B's author hit the subject-type defect as a live
   diagnostic that Approach A's own reviewer only reasoned about abstractly.
4. **Writing the rationale out, at each step, in the open, is what made this resolvable at all.**
   Not the chosen two lines of SysML — the explicit record of *why*, at every branch point (the
   trade study, the hybrid probe, the six-angle interrogation above), is what let a plausible,
   tool-accepted, checker-satisfying construct be recognized as representationally wrong before it
   shipped. A model that only recorded the final answer would have looked identical to one that
   got here by accident.
