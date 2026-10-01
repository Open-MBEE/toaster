# Grid cell M2-practitioner — GitHub Pages, SE Practitioner persona, Chapters 6+8

## Execution results

Ch6 index (`/index-6`): orients correctly — states the branch question, the five artifacts to be added, and links back to Ch5. One sentence per notebook in the Ingredients table.

Ch6-01 `/subsystem-requirements`: concept-statement one sentence, yes. Context links to Ch5's HeatingSystem. Model-increment cell printed all SysML defs and `assert model.ok` passed silently (no AssertionError rendered, printed output continues normally — the standard proof-by-absence this rendered format uses throughout). Negative control: `bad.ok` False, diagnostic `'unresolved reference: HeatingAssembly::undefinedSlot'` printed. Demonstration: `find_allocations`/`perform_relationships` printed real dict output matching the prose claim (`HeatingAssembly::heatGenAllocation` with the two-segment source chain). Seam: concretely addressable — the SysML text block (`HEATING_ASSEMBLY_DEF`), the tool call (`conn.load_from_content`, `find_allocations`), and the printed query result are visibly three different things on the page, connected by prose that explains why the printed shape follows from the text. No "Tall"/"three worlds" language.

Ch6-02 `/second-level`: one-sentence concept statement. Builds AC-C06 (framing) and AS-C06 (mechanism selection) as full Hawkins records — claim/criteria/premises/evidence/rationale/counterevidence/residual_uncertainties all populated, not placeholders. `validate_record()` printed `[]` both times, and a `Model tag:` dict is printed alongside, confirming the new subject_ref anchor mechanism resolves to a real model element each time. Negative control (`UndefinedCarrier`) correctly failed. Demonstration: `rated.power = 800 [SI::W], heatGenerationReq(rated) = True`; `weak.power = 400 [SI::W], heatGenerationReq(weak) = False` — exact numbers match the 600 W threshold stated earlier on the page.

Ch6-03 `/stopping-judgment`: builds AI-C06 with premises `['AC-C06', 'AS-C06', 'AS-C03', 'AI-C04']` — a real chain, not an assertion of completeness. Negative control: empty-premises record correctly rejected with `'asserted_inference requires at least one premise (Hawkins §3.1)'`. The counterevidence section states plainly what is NOT established (energyIn unconnected, HeatingAssembly not composed into a Toaster, threshold underived) — this is the strongest instance of honest scoping in the chapter.

Ch6 conclusion `/conclusion-5`: three paragraphs (what we built / what this establishes / what comes next) plus exercise reference. Correct structure.

Ch8 index `/index-8`: explicitly states the chapter's central honesty point up front — the lemma is "a hand-restated lemma, not a solver-checked reference," citing D-030/D-031. Sets expectations accurately before the reader hits any code.

Ch8-01 `/invariant-def`: concept-statement one sentence. `model.find()` and `model.query()` both confirmed `deliveredEnergyBoundedBySupply` present; negative control `bad.ok=False` for an undeclared-attribute constraint.

Ch8-02 `/violation-witness`: this is the chapter's core technical claim. `verify_satisfaction()` printed four real verdicts including one legitimate `FAILS` (the `verify timely` objective, which has no subject — explained correctly as a different relationship kind, and `conformance.report()` is shown skipping it rather than miscounting it as a finding). `verify_holds()` printed `[satisfied] ... (z3: holds for all values of unbound features)` for the positive case, `[violated] ... (z3: unsatisfiable -- no assignment can make this hold)` for the full-negation negative control, and `[undecided] ... satisfiable, e.g. heatGenCheck.efficiency = 0...` for the weakened variant, with `holds()` raising `ModelCheckInconclusiveError` rather than collapsing to True/False. All three Z3 outcomes are real printed solver output, not asserted. AS-C08's counterevidence explicitly states the proof does NOT track the original `efficiencyBounded`/`deliveredEnergy` and reports that this was confirmed directly by editing both and observing no change in verdict — this is the single best piece of evidence in either chapter that the judgment record is not hand-waving.

Ch8-03 `/revision-flow`: `check_stale()` returns `False` pre-edit, `True` after loosening the bound — printed output matches the narrative exactly.

Ch8 conclusion `/conclusion-7`: three paragraphs, exercise reference present, and explicitly names the three distinguishable verdict kinds (point-evaluated, proved, undecided) as the chapter's takeaway.

No broken rendering, no dead links, all navigation via sidebar worked. One site-level issue: the home page (`/`) shows a dismissable "Site not loading correctly? ... BASE_URL" warning banner referencing MyST deployment docs — present on first load of `/`, not seen on inner chapter pages.

## Structured findings

- id: M2-practitioner-01
  severity: positive
  location: http://localhost:3000/violation-witness
  quote: "Confirmed directly: loosening efficiencyBounded's own literal bound to <= 1.5, or doubling deliveredEnergy's own definition by a factor of 2.0, in the real committed model changes neither the original elements' own verdicts nor this lemma's verdict at all"
  expected: A Z3 proof chapter claiming a conservation property would gloss over the gap between the proved companion lemma and the real model constructs.
  actual: The page states the gap, names the exact DEFERRED.md IDs (D-030, D-031), and reports a real experiment (editing both originals and observing the verdict does not move) as evidence for the gap rather than just asserting it exists. This is exactly the level of rigor a reviewing SE would want before trusting someone else's Z3 result.

- id: M2-practitioner-02
  severity: cosmetic
  location: http://localhost:3000/violation-witness
  quote: "The claim printed above, the proof it points to, and the record's own counterevidence stating plainly what that proof does and does not establish are three distinct things this notebook watched connect: a written lemma, a real solver's verdict on it, and a record that never overstates what the verdict actually covers."
  expected: Per AGENTS.md 1.10, learner-facing prose should address the seam in behavior without echoing the seam-judgment language itself.
  actual: The phrasing "three distinct things this notebook watched connect" is close in form to this very checklist's own seam-detection question ("three distinct things the reader has just seen connect"), though it does not name "Tall" or "the three worlds" and lists model-specific nouns (lemma/solver/record), not the lens's generic triad (text/tool/result). Not a lint violation, but worth a second pair of eyes — it reads like the construct almost surfaced.

- id: M2-practitioner-03
  severity: cosmetic
  location: http://localhost:3000/
  quote: "Site not loading correctly? This may be due to an incorrect configuration. See for reference."
  expected: A clean landing page on the dev-server preview with no infrastructure warnings visible to a reader.
  actual: A BASE_URL warning banner is shown on the home page (not reproduced on inner chapter pages); likely a dev-server/base-path artifact rather than a content defect, but a first-time reader would see it before anything else.

## Overall

PASS — both chapters execute cleanly in the rendered book, printed output matches prose claims exactly on every cell checked, negative controls fail the way the prose says they will, the Hawkins judgment records (including the new subject_ref/Model-tag anchor mechanism) are genuine engineering arguments with real counterevidence rather than filled-in templates, and the Z3 proof in Chapter 8 is presented with its real scope limits stated and experimentally confirmed — this is the standard I'd want from a colleague's design review, not hand-waving.
