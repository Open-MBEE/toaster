# Chapter 10: Traceability and Sign-off

## Purpose

This chapter builds a real traceability graph over the model's two named requirements, synthesizes three of the tutorial's own real judgment records into a ledger, and shows what an accountable engineer's sign-off actually looks like in form: a bounded, honest statement of what is established, what is not, and what residual judgment remains, not a declaration that the case is closed. This is the tutorial's final chapter.

This chapter adds no new named model element: `models/ch10-cumulative.sysml` carries `models/ch08-cumulative.sysml`'s content forward unchanged, the same deliberate design choice Chapter 9 made (`decisions/pass4-run-009.md`); this chapter's own traceability and judgment work needs no new element either. Unlike Chapter 9, this chapter commits its own `models/ch10-cumulative.sysml` file: Chapter 9 left no cumulative fixture of its own, which would have made `scripts/check_construction.py`'s own predecessor-containment check silently no-op between Chapter 8 and Chapter 10 (`decisions/next-passes.md` item 21). This chapter resolves that for real: `check_predecessor_containment()` now falls back to the nearest earlier chapter with a real fixture when the immediate predecessor has none, so Chapter 8's own named elements are actually checked against this chapter's own committed file, not skipped.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 - A real traceability graph, and one real, unjustified widget](01-traceability-graph.ipynb) | Trace both requirements from functional intent through allocation and realization to verification evidence, built entirely from real queries, and find that the model's own strongest formal proof is tied to no requirement at all. |
| [02 - A judgment ledger, over three real records this tutorial has already built](02-judgment-synthesis.ipynb) | Reconstruct `AS-C06` and `AS-C08` (re-verified against their real originals) plus `AI-C06`, and read what each record's own kind, disposition and residual uncertainty actually says. |
| [03 - A synthesis record, and what it is not](03-engineering-signoff.ipynb) | Synthesize the graph and the ledger into one honest, bounded record, and state plainly why that record is not itself sign-off. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No additional tooling beyond earlier chapters.

## Method

Notebook 01 finds each requirement's own declared subject by reading the requirement definition's own `subject` feature in the API-JSON export, then follows the real allocation and realization chain to each one's physical candidates, and joins that chain against `requirement_coverage()`'s own polarity-correct result (Chapter 9). `heatGenerationReq` traces all the way to genuine, opposite-polarity evidence (`rated` satisfies it, `weak` fails it); `timely` traces just as far through intent, allocation and realization, but stops one link short, since no candidate has ever been positively checked against it. The notebook also asks the same question in the other direction: is `deliveredEnergyBoundedBySupply`, the one property in this tutorial proved by Z3 for every value its unbound features admit, tied to any requirement usage at all? It is not, a real instance of the failure mode Douglas's own traceability concern names: evidence disconnected from any stated need. Notebook 02 reconstructs three real judgment records verbatim, `AS-C06` and `AS-C08` (already reconstructed once by Chapter 9, re-verified here rather than assumed correct) plus `AI-C06` (Chapter 6's own stopping judgment, an `asserted_inference`, alongside the two `asserted_solution` records), and reads each one's own kind, disposition and residual uncertainty rather than only its count. Notebook 03 synthesizes both into one new record, `AI-C10`, an `asserted_inference` whose own premises are literally the other two notebooks' findings, and states explicitly why that record, however honest and complete, is not sign-off itself.

## Expected result

After running all three notebooks: notebook 01's graph shows `heatGenerationReq` covered on both sides (`satisfied_by=['rated']`, `failed_by=['weak']`), `timely` covered on neither (`satisfied_by=[]`, `failed_by=['slow']`), and `deliveredEnergyBoundedBySupply` tied to no requirement usage; notebook 02's ledger shows three records, all `disposition="pending"` and `record_kind="worked_example"`, two `engineering_conclusion="undetermined"` (`AS-C06`, `AI-C06`) and one `"supported"` but narrowly scoped (`AS-C08`); notebook 03's synthesis record (`AI-C10`) validates cleanly, keeps `disposition="pending"` and `engineering_conclusion="undetermined"`, and the notebook states plainly, in prose, that this record is not sign-off.

## Experiment

See `exercises/ch10/exercise.ipynb`.
