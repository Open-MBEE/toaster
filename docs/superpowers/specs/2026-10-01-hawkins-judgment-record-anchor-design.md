# Design: anchoring Hawkins judgment records to the model

**Status:** design approved in conversation; pending written-spec review
**Author:** session design work with Z, 2026-10-01
**Related:** `decisions/log.md` DL-075 (the recurring judgment-record seam escalation, which this design retires); `src/toaster/evidence.py`; `.claude/skills/toaster-review-protocol/SKILL.md`; `.claude/skills/toaster-recipe/SKILL.md`; `glossary/definitions/hawkins.ttl`

## Why this exists

Z introduced the Hawkins et al. 2011 `ReviewRecord` mechanism to document and classify the
engineering judgment calls this tutorial makes — not as decoration, but so a reader can see *why*
a claim should be believed, not just that a checker printed `True`. Ten ACE syntheses and
twenty-nine persona reports this session independently converged on one open question about it
(DL-075): what does AGENTS.md 1.10's seam requirement mean for a notebook whose only new content
is a judgment record, not a SysML construct? That question turned out to rest on a real, fixable
gap, found by reading the actual Hawkins paper rather than the glossary's own curated extracts of
it, and then by testing what SysML v2 itself already provides for exactly this problem.

## What the primary source actually says

Hawkins, Kelly, Knight and Graydon, *A New Approach to Creating Clear Safety Arguments* (SSS
2011, pp. 3-23), read in full from the authors' own self-archived copy
(`https://www-users.york.ac.uk/~rdh2/papers/HawkinsSSS11.pdf`), not from memory or the glossary's
prior extracts alone.

**The core move.** Split an argument into a *safety argument* (the direct claim and its support)
and a *confidence argument* (why a skeptical reader should believe that support is sufficient),
kept explicitly separate because conflating them is what the paper diagnoses as the cause of
"large, rambling... poorly-focused" real arguments (Sec. 2).

**The three judgment sites.** Every assertion in an argument is one of three kinds — asserted
inference (a claim is supported by sub-claims, Sec. 3.1), asserted context (a background
assumption is introduced, Sec. 3.2), or asserted solution (evidence is cited to close an argument,
Sec. 3.3) — and each is tied to a specific, named **Assurance Claim Point (ACP)**: a located link
in an argument graph (built in GSN, the Goal Structuring Notation), not a free-floating claim.

**The judgment principle.** An assurance deficit is "any knowledge gap that prohibits perfect
(total) confidence" (Sec. 1, p. 4). Completely mitigating every deficit is "not normally
achievable," so a judgment is required about which residual deficits can be tolerated, assessed by
"expert judgment of the likelihood and severity" of counter-evidence (Sec. 3.4, p. 12). This
tutorial's `counterevidence`/`residual_uncertainties` fields are this principle, directly.

**Domain generality, in the authors' own words (Sec. 5, Conclusions):** "We have limited our
discussion in this paper to safety cases, but the concepts apply immediately to *any* property of
interest... the overall structures and approaches would be identical." Using this framework for
engineering judgment about a toaster, not a hazard, is not a stretch — it is the generalization the
authors themselves license.

**What correctly does not transfer.** GSN itself, Assurance Claim Points as graph-tags, the
recursive confidence-argument *patterns* (six to seven claim-nodes deep per ACP, Figs. 13-14), and
the hazard/risk/certification framing are built for formal, third-party-reviewed certification
arguments. `ReviewRecord` is a flat dataclass, not a GSN tree, and stays that way under this
design — importing the graph apparatus would not serve a teaching tutorial.

**What does transfer, and is currently missing.** An ACP is never free-floating — every confidence
argument is anchored to one specific, located assertion. `ReviewRecord` has no equivalent today:
`model_ref` is a bare file-path string, `content_hash` hashes an entire file, and neither says
*which element* a given judgment is actually about. That anchor exists only informally, in the
free-text `claim` string. This is the real, primary-source-grounded reason DL-075 could not be
settled by argument alone — the thing the two competing seam readings were really both reaching
for was a located subject, and neither the record's own fields nor the model had one.

## The decision

Give `ReviewRecord` a real, singular, checkable subject — the tutorial's own narrowed analog of an
ACP — anchored on **both** sides: a new field in Python, and a real SysML metadata tag in the
model itself, so the connection is visible from the model's own side, not just assumed from
outside it. (Caught directly in review: a Python-only anchor, checked one direction only, would
leave the model itself blind to its own judgment records — a real gap given Chapter 10's whole
purpose is model-side traceability querying.)

### Why singular, not a list

A first draft of this design used `subject_refs: list[str]`. Z's own objection killed it: the
*relationship* a judgment has to different elements it touches is not uniform, so one undifferentiated
list loses the distinction. Hawkins' own answer to multiplicity is not "a bigger ACP" — each kind of
assertion already has its own role-typed container (assumptions for context, evidence for solution,
premises for inference), and `ReviewRecord` already has all three: `assumption_refs`, `evidence_refs`,
`premises`. The actual gap was narrower: a single, clean subject — the one thing the claim is
*directly* about — which those three existing lists were never meant to carry. `subject_ref` fills
exactly that slot, matching Hawkins' own "one ACP, one link" shape.

### Why a model-side tag, not just a validated Python string

Probed directly against OpenSysML v0.9.0 before committing (see Verification below), because this
toolchain has a known, adjacent gap (`VerificationMethod` metadata, cited in Ch8's own notebook, is
"not yet supported"), so nothing about custom metadata could be assumed to work. It does, for the
shape this design needs. SysML v2 §7.27.2 already defines exactly the relationship wanted: a
`metadata def` with an `about` clause binds the usage's inherited `annotatedElement` feature to the
named target(s) — a real, queryable model relationship, not a string a human has to trust.

## Design

### 1. Schema (`src/toaster/evidence.py`)

```python
@dataclass
class ReviewRecord:
    identifier: str
    kind: Literal["asserted_context", "asserted_inference", "asserted_solution"]
    claim: str
    subject_ref: str = ""          # NEW — the tutorial's own ACP: one qualified name
    model_ref: str = ""
    content_hash: str = ""
    ...  # unchanged otherwise
```

`validate_record(r: ReviewRecord, model: Any | None = None) -> list[str]` gains:

- **Required-ness rule** (no model needed to check this): `subject_ref` must be non-empty for
  `kind in ("asserted_context", "asserted_solution")`. For `kind == "asserted_inference"`,
  `subject_ref` may be empty **only if** `premises` is non-empty — the pure cross-record synthesis
  case (`AI-C10` is the only current record that needs this exemption).
- **Resolution check** (needs `model`, the new optional parameter): if `subject_ref` is set,
  `model.find(subject_ref) is not None`, else an error naming the unresolved reference.
- **Cross-representation check** (needs `model` and the new query helper, see below): if a
  `ReviewRecordRef` tag exists in the model for this record's `identifier`, its own
  `annotatedElement` must match `subject_ref` and its own `identifier` attribute must match
  `r.identifier` — catching drift between the Python side and the model side if they're ever
  edited independently.

### 2. Model-side construct (new SysML, introduced once)

```sysml
metadata def ReviewRecordRef {
    attribute identifier : String;
}
```

Introduced in Chapter 2 (the tutorial's first judgment record, `AC-001`), carried forward in every
cumulative model from Ch2 onward — the same convention every other reusable construct in this
tutorial already follows (one definition, authored once, present in every later chapter's own
committed fixture). Each judgment notebook's construction zone builds one usage, using the
**explicit `about` form** (confirmed by probe to be the form that actually populates
`annotatedElement`; the implicit nested shorthand does not):

```sysml
metadata ac001Tag : ReviewRecordRef about timely {
    identifier = "AC-001";
}
```

Only the definition is a new construct, once, in Ch2. Every later chapter's usage is the same
already-taught idiom (matching how `allocate` usages recur across chapters without each counting
as a new construct under SA-8).

### 3. Query helper (`src/toaster/query.py`)

```python
def get_review_record_refs(model, index=None) -> list[dict]:
    """Every ReviewRecordRef tag in the model: {identifier, annotated_element}."""
```

Built on `to_api_json()`, the same pattern `get_satisfy_relationships()` already uses (`MetadataUsage`
elements are visible to `model.query()` natively — no D-001-style gap for basic discovery — but
`annotatedElement` itself is only in the JSON export, confirmed by probe). This is the model→Python
direction: given a loaded model, find every judgment tag and what it's about, independent of any
particular notebook's own Python objects.

### 4. Skill updates

**`toaster-review-protocol`:**
- Add `subject_ref` to the required-fields example and table.
- New section, citing SysML v2 formal/2026-03-02 §7.27.2 directly: explain `about`/`annotatedElement`
  as the real spec mechanism, and `subject_ref` + `ReviewRecordRef` together as this tutorial's
  deliberately narrowed analog of Hawkins' Assurance Claim Point — one link, no GSN graph.
- Update the "three judgment sites" table with the required-ness rule above.

**`toaster-recipe`:**
- The judgment-record construction zone gains a new first named group: "what is being claimed, and
  what, specifically, it is about" — covering `claim`, `subject_ref`, and the `ReviewRecordRef`
  usage together, narrated as one idea (mirrors how a model-increment cell is already one idea with
  several named fragments).
- **Resolves DL-075.** The seam cell for a judgment-record notebook now narrates one bridged
  connection, not a choice between two competing triads: the tagged SysML text (subject + its
  `ReviewRecordRef` usage) is printed; the tool loads it and checks both the Python record and the
  model tag; the result shows they agree (`validate_record` plus `get_review_record_refs`). This is
  a concrete, checkable instance of AGENTS.md 1.10's requirement, not a judgment call between
  readings A/B/C — the question those readings were circling is answered by giving the record an
  actual anchor, not by picking which existing triad counts.

### 5. Glossary

Add `assurance-claim-point` as a confirmed Hawkins-sourced term:

```turtle
glid:def-hawkins--assurance-claim-point
    gl:locator "Sec. 3, p. 8 (PDF 6)" ;
    gl:quote "the confidence argument is tied to a number of Assurance Claim Points (ACP)" ;
    gl:text "The place in the safety argument where an assertion is made; a confidence argument is developed for each." ;
```

(This term already exists in `glossary/definitions/hawkins.ttl` — it was seeded during Pass 1 but
not yet cited anywhere in the skills or schema it now grounds. No new definition edge needed, only
the `gl:refines` tying `subject_ref`/`ReviewRecordRef` to it as the tutorial's own narrowed
instance, and the citation added to `toaster-review-protocol`.)

### 6. Retrofit (every existing record, in one coordinated effort)

| Record | Chapter (original authoring) | `subject_ref` | Needs model tag? |
|---|---|---|---|
| `AC-001` | Ch2 | `timely` (or the specific requirement usage it concerns) | Yes — first usage, defines `ReviewRecordRef` |
| `AC-C03` | Ch3 | the MoE/MoP element it concerns | Yes |
| `AS-C03` | Ch3 | `timely` or the threshold constraint | Yes |
| `AI-C04` | Ch4 | the balance inequality / `ApplyHeat` | Yes |
| `AS-C06` | Ch6 | `ResistanceCoil` or the mechanism-selection element | Yes |
| `AI-C06` | Ch6 | `HeatingAssembly` (the thing judged as a stopping point; `heatGen`/the allocation move to `premises`/`evidence_refs`, not a second subject) | Yes |
| `AS-C08` | Ch8 | `deliveredEnergyBoundedBySupply` | Yes |
| `AI-C10` | Ch10 (synthesis) | — (exempt: `asserted_inference` with non-empty `premises`) | No |

Ch9 and Ch10's own *reconstructions* of `AC-C06`/`AS-C06`/`AS-C08`/`AI-C06` (the judgment ledger
notebooks) carry the same `subject_ref` value forward in their own Python objects; they do not
rebuild the model tag, since the cumulative model they load already has it from the originating
chapter.

Exact `subject_ref` values for each record need confirming against the real model's own qualified
names at implementation time — the table above states intent, not final strings.

## Verification already done (this session, before writing this spec)

Probed directly against a throwaway fixture with OpenSysML v0.9.0, not assumed:

1. `metadata def ReviewRecordRef { attribute identifier : String; }` plus an explicit-`about` usage
   loads cleanly (`model.ok == True`, no diagnostics).
2. `model.find()` resolves the metadata usage directly.
3. `model.query()` finds `MetadataUsage` elements natively (no JSON-export workaround needed for
   basic discovery, unlike `SatisfyRequirementUsage`'s D-001 gap).
4. `to_api_json()` shows a correct `annotatedElement` relationship pointing at the real subject, for
   the explicit `about` form.
5. The attribute's bound value round-trips through the JSON (`LiteralString`/`FeatureValue` chain),
   confirmed readable.
6. The **implicit nested form** (`@ReviewRecordRef {...}` with no `about`, inside the subject's own
   body) does *not* populate an explicit `annotatedElement` entry the same way — confirmed by
   contrast in the same probe. Design conclusion: standardize on the explicit `about` form.

## What this does not change

- `ReviewRecord` stays a flat Python dataclass. No GSN graph, no recursive confidence-argument
  patterns, no certification framing — those were correctly identified as not transferring, and
  nothing here reopens that.
- `model_ref`/`content_hash` are unchanged in meaning (whole-file staleness detection via
  `check_stale()` stays exactly as it is); `subject_ref` is additive, a different and narrower kind
  of anchor (one element, not one file).
- `assumption_refs`, `evidence_refs`, `premises` are unchanged — they stay free text, with new
  guidance (not a requirement) to use a qualified name when an entry happens to name a real model
  element.

## Open items for the implementation plan, not resolved by this spec

- Exact `subject_ref` values per existing record (table above states intent; needs confirming
  against each chapter's real qualified names).
- Contract sequencing: `ReviewRecordRef`'s own definition text must be settled once (this spec fixes
  its shape) and land in Ch2 before later chapters build usages of it — whether that means strictly
  serial contracts or parallel contracts sharing a pinned definition text is a planning decision, not
  a design one.
- Whether a new DEFERRED.md gap entry is warranted if implementation surfaces any OpenSysML
  rough edge beyond what this spec's probe already found (none found so far).
