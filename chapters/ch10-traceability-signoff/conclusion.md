# Chapter 10 Conclusion

## What we built

No new model element: `models/ch10-cumulative.sysml` carries `models/ch08-cumulative.sysml`'s content forward unchanged, and every notebook in this chapter queries it directly. What changed is what can be asked of it and of the tutorial's own record set: notebook 01 adds a real traceability graph, tracing both named requirements from functional intent through allocation and realization to verification evidence, and finds that `deliveredEnergyBoundedBySupply` is tied to no requirement usage at all; notebook 02 reconstructs three real `ReviewRecord`s (`AS-C06`, `AS-C08`, `AI-C06`) into a ledger and reads what each one's own kind, disposition and residual uncertainty actually says; notebook 03 synthesizes both into one new record, `AI-C10`, and states plainly that the record itself is not sign-off.

## What this establishes

The traceability graph traces the model's two requirements very differently, and says so honestly. `heatGenerationReq` has real, bidirectional verification evidence: `rated` really satisfies it, `weak` really fails it, both real claims about real candidates. `timely` traces just as far through a real functional intent, a real allocation and real physical candidates, but stops one link short of any positive verification at all: the only claim against it is negative (`slow` fails it), and `Toaster::cycleTime` is still not derived from anything, so no one has ever actually checked whether `nominal` satisfies it. And this tutorial's own strongest piece of formal evidence, `deliveredEnergyBoundedBySupply`, proved by Z3 for every value its unbound features admit, is tied to no requirement usage anywhere in the model: the inverse of a failure mode Douglas's own traceability concern names (an unjustified widget, a design element with no requirement behind it), here evidence with no requirement in front of it.

The judgment ledger, built from three real records rather than asserted about all of them, shows what that graph's own evidence is actually worth. `AS-C06` stays `undetermined`: its own residual admits the mechanism selection could be revisited against a real trade study, not settled by the domain premise it currently rests on. `AS-C08` is `supported`, but narrowly: its own residual is explicit that the proof is of a hand-restated companion lemma, not automatically re-checked against the real elements it mirrors if either is edited. `AI-C06` stays `undetermined` too: its own residual leaves the branch's further decomposition, composition into a real `Toaster` candidate, and `ApplyHeat`'s other flows all genuinely open. Two records out of three stay `undetermined`, and the one `supported` record is supported only for a claim already narrowed to a restated copy, not the real elements it mirrors.

The synthesis record, `AI-C10`, brings both together honestly, within its own stated scope: it names what has real, bidirectional evidence, what has only one-sided evidence, and what formal proof exists tied to no stated requirement at all, with `engineering_conclusion="undetermined"`, the only honest word for a model with one covered requirement, one uncovered one, and its own strongest proof tied to neither. And it states, in its own prose, the distinction the whole chapter rests on: a completed traceability graph and judgment ledger are not sign-off itself. Sign-off is a human, accountable act; this tutorial can show the inputs to that act, honestly and within its own stated scope, but it does not, and should not, perform it on the learner's behalf.

## What comes next

This is the tutorial's last chapter. What continues from here is not another chapter but the reader's own accountable engineering: taking the traceable, honestly-scoped case this tutorial teaches how to build, and exercising, on a real design, the judgment this tutorial has shown but never made for them.

## Exercise

See `exercises/ch10/exercise.ipynb`: it asks you to build this same traceability graph, judgment ledger and sign-off synthesis over your own coffee-maker model.
