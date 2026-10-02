---
title: Overview
---

# Chapter 9: Coverage and Sufficiency

## Purpose

This chapter asks whether the model's own requirements have actually been checked, not just declared: for every requirement usage, has any candidate really been claimed to satisfy it, and of what polarity? It also applies Hawkins' sufficiency idea to two real judgment records this tutorial already built, and extends Chapter 8's staleness check from one record to several tracked at once.

This chapter adds no new model element. `models/ch08-cumulative.sysml`, the real, current model Chapter 8 committed, already has everything these notebooks query: two requirement usages (`timely`, `heatGenerationReq`) and four real satisfy relationships. Rather than growing a `models/ch09-cumulative.sysml` that would carry nothing new, every notebook in this chapter queries `models/ch08-cumulative.sysml` directly, and says so. This is a deliberate design choice, not an oversight: the chapter's own coverage-gap finding needs no new element, and the tutorial's own non-goal discipline (Chapter 6 and Chapter 7's own precedent of stating scope honestly) argues against adding one only to keep a file-per-chapter convention.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 - requirement coverage](01-requirement-coverage.ipynb) | Build a real coverage report by joining every requirement usage against every satisfy relationship, contrast it against a polarity-blind join that gets it wrong, and confirm it against the repository's own (now-fixed) `requirement_coverage()` helper. |
| [02 - evidence sufficiency](02-evidence-completeness.ipynb) | Apply Hawkins' sufficiency idea to two real ReviewRecords, reconstructed verbatim from Chapter 6 and Chapter 8. |
| [03 - stale detection at scale](03-stale-detection.ipynb) | Check several tracked records against the real, current model in one pass, before and after a real edit. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No additional tooling beyond earlier chapters.

## Method

Notebook 01 queries `model.query()` for every named `RequirementUsage` and `get_satisfy_relationships()` for every `SatisfyRequirementUsage`, joins them by requirement, and surfaces which requirements have a real positive claim of satisfaction, which have only a negative one, and which have none. It finds that `heatGenerationReq` is checked on both sides (`rated` passes, `weak` fails) while `timely` has never had a positive claim: `nominal` has no `assert satisfy timely by nominal` anywhere in the model, an absence, not a finding that `nominal` fails `timely` (`cycleTime` is still not derived from anything). (Chapter 10 later adds a third named requirement, `energyConservationReq`, which this same `requirement_coverage()` helper also reports as `covered=False` -- but for a structurally different reason: by design, tied to an already-proved lemma by subsetting rather than by any `assert satisfy`, not by omission like `timely`'s; see that chapter's own `AC-C10` judgment record.) The notebook also shows what a polarity-blind join would have wrongly concluded (`timely` "covered" by `slow`'s own failing claim) -- the exact bug the repository's own `requirement_coverage()` helper carried until this chapter's work found and fixed it -- and confirms its own join against that now-corrected helper. Notebook 02 reconstructs `AS-C06` and `AS-C08` verbatim, field for field, and asks whether each one's own counterevidence, residual_uncertainties and premises are substantive and whether its engineering_conclusion matches what its own evidence supports, honestly scoped to these two records, not a claim about every judgment record this tutorial has ever produced. Notebook 03 checks both records' staleness together against the real model, before and after loosening `deliveredEnergyBoundedBySupply`'s own bound: `AS-C06` is already stale, and substantively so (Chapter 7 added `HeatGenerator`'s `efficiency`/`efficiencyBounded`/`deliveredEnergy`, so an efficiency comparison its own counterevidence called out of reach can now at least be started, though the Joule-heating relation it also names, and any response-time comparison, are still not modeled); `AS-C08` goes stale from an edit to a different part of the file than the one its own residual specifically names as a risk, caught only because its `content_hash` covers the whole file.

## Expected result

After running all three notebooks: notebook 01's coverage report shows `heatGenerationReq` covered (a positive claim by `rated`, a negative one by `weak`) and `timely` not covered (only a negative claim, by `slow`), with a polarity-blind join and the now-fixed `requirement_coverage()` helper both checked directly against that result; notebook 02's two reconstructed records both validate cleanly, both carry non-empty, substantive counterevidence, residual_uncertainties and (where present) premises, and both keep `disposition = "pending"`, never the forbidden alternative; notebook 03 shows `AS-C06` already stale before any edit, for a reason substantively tied to real model growth, and `AS-C08` current until the shared edit is applied, after which both report stale, for two genuinely different reasons.

## Experiment

See `exercises/ch09/exercise.ipynb`.
