# Chapter 9 - Coverage and Sufficiency

## Purpose

This chapter asks whether the model's own requirements have actually been checked, not just declared: for every requirement usage, has any candidate really been claimed to satisfy it, and of what polarity? It also applies Hawkins' sufficiency idea to two real judgment records this tutorial already built, and extends Chapter 8's staleness check from one record to several tracked at once.

This chapter adds no new model element. `models/ch08-cumulative.sysml`, the real, current model Chapter 8 committed, already has everything these notebooks query: two requirement usages (`timely`, `heatGenerationReq`) and four real satisfy relationships. Rather than growing a `models/ch09-cumulative.sysml` that would carry nothing new, every notebook in this chapter queries `models/ch08-cumulative.sysml` directly, and says so. This is a deliberate design choice, not an oversight: the chapter's own coverage-gap finding needs no new element, and the tutorial's own non-goal discipline (Chapter 6 and Chapter 7's own precedent of stating scope honestly) argues against adding one only to keep a file-per-chapter convention.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 - Querying the model for what has, and has not, been claimed](01-requirement-coverage.ipynb) | Build a real coverage report by joining every requirement usage against every satisfy relationship; find and explain a real, present gap. |
| [02 - Evidence sufficiency, applied to two real records](02-evidence-completeness.ipynb) | Apply Hawkins' sufficiency idea to two real ReviewRecords, reconstructed faithfully from Chapter 6 and Chapter 8. |
| [03 - Stale detection, at scale](03-stale-detection.ipynb) | Check several tracked records against the real, current model in one pass, before and after a real edit. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No additional tooling beyond earlier chapters.

## Method

Notebook 01 queries `model.query()` for every named `RequirementUsage` and `get_satisfy_relationships()` for every `SatisfyRequirementUsage`, joins them by requirement, and surfaces which requirements have a real positive claim of satisfaction, which have only a negative one, and which have none. It finds that `heatGenerationReq` is checked on both sides (`rated` passes, `weak` fails) while `timely` has never had a positive claim: `nominal` has no `assert satisfy timely by nominal` anywhere in the model, an absence, not a finding that `nominal` fails `timely` (`cycleTime` is still not derived from anything). Notebook 02 reconstructs `AS-C06` and `AS-C08` field for field and asks whether each one's own counterevidence and residual_uncertainties are substantive and whether its engineering_conclusion matches what its own evidence supports, honestly scoped to these two records, not a claim about every judgment record this tutorial has ever produced. Notebook 03 checks both records' staleness together against the real model, before and after loosening `deliveredEnergyBoundedBySupply`'s own bound (Chapter 8's own edit, reused): one record is already stale for reasons the edit has nothing to do with, the other goes stale because of exactly what the edit changes.

## Expected result

After running all three notebooks: notebook 01's coverage report shows `heatGenerationReq` covered by both a positive and a negative claim and `timely` covered by neither, with `conformance.report()`'s `satisfaction-claims-evaluated` check independently confirming no finding exists for `nominal`/`timely` because there is no claim to evaluate; notebook 02's two reconstructed records both validate cleanly, both carry non-empty, substantive counterevidence and residual_uncertainties, and both keep `disposition = "pending"` (SA-7 forbids the alternative); notebook 03 shows `AS-C06` already stale before any edit and `AS-C08` current until the shared edit is applied, after which both report stale.

## Experiment

See `exercises/ch09/exercise.ipynb`.
