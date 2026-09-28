# Chapter 9 Conclusion

## What we built

No new model element: every notebook in this chapter queries `models/ch08-cumulative.sysml`, the real, current model Chapter 8 committed, directly. What changed is what can be asked of it: notebook 01 adds a real coverage report joining every requirement usage against every satisfy relationship; notebook 02 applies Hawkins' sufficiency idea to two real, faithfully-reconstructed ReviewRecords (`AS-C06`, `AS-C08`); notebook 03 extends Chapter 8's own `check_stale()` demonstration from one record to two tracked together.

## What this establishes

The coverage report is not a hypothetical exercise: it finds a real gap already present in this tutorial's own accumulated model. `heatGenerationReq` has been checked against two different candidates, one that meets it and one that does not; `timely` has only ever been checked against a candidate that fails it, plus a verification-case objective that names it without claiming anything about a subject. No one has ever claimed `nominal`, the usage meant to represent the toaster actually meeting its timing requirement, satisfies `timely` -- an absence of a claim, not evidence that it would fail one, since `cycleTime` is still not derived from anything. `conformance.report()`'s existing `satisfaction-claims-evaluated` check independently agrees: it reports no finding for `nominal`/`timely` at all, because there is nothing for it to evaluate. Sufficiency, applied to two real records rather than asserted about all of them, shows what the check actually demands: not merely a non-empty `counterevidence` field (the mechanized floor `validate_record()` already enforces) but a substantive one, and an `engineering_conclusion` that matches what the record's own evidence supports -- `AS-C06` honestly stays `undetermined` because its selection rests on a domain premise, not a trade study; `AS-C08` is `supported` because its own claim was already narrowed to exactly what got proved. Staleness, checked across both records at once against the same real edit, shows two different real histories: one record already stale from ordinary chapter-to-chapter model growth, the other freshly stale from the one change its own record already named as a risk.

## What comes next

Chapter 10 builds the full traceability graph this chapter's coverage report only samples one join of, and asks what a real sign-off over that graph would actually require.

## Exercise

See `exercises/ch09/exercise.ipynb`: it asks you to produce a coverage table for the bread-handling requirements, using the query-and-join pattern notebook 01 builds.
