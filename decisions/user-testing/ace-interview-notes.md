# ACE interview notes: novice longitudinal browser test

Date: 2026-10-02
ACE model: Fable 5.1. Novice agent: `a2716a9cc61733a11` (Haiku 4.5, Novice persona).
Source diary: `decisions/user-testing/longitudinal-novice-browser-diary.md` (novice worktree, 1731 lines, 54 page entries).

Written incrementally. Sections: 1 diary read, 2 interview, 3 ACE spot-check, 4 triage, 5 verdict.

## 1. Diary read (before interviewing)

What the diary reports, compressed:

- Ch1 (pp. 3-8): rated a strong start; pattern code -> output -> explanation -> negative control -> query -> diagram "works well". Confusion: `mechanism`, `perform`, `abstract`, `ISQ::DurationValue` undefined on first use.
- Ch2 (pp. 9-13): 2-01 and 2-02 manageable; 2-03 (asserted context, `/judgment-context`) is the first jump, load 4/5: ReviewRecord with 15+ fields, "shift from SysML constructs to Python judgment records happens abruptly without conceptual bridge"; Hawkins cited, never explained.
- Ch3 (pp. 14-19): sustained 4/5; MoE/MoP distinction "still unclear"; `assert satisfy` syntax before semantics; ReviewRecord pattern "repeated three times without consolidation, feels formulaic".
- Ch4 (pp. 20-24): 4-01 action def 4/5 (multiplicity `[0..*]`, "reopening", in/out); 4-02 item def 3/5 and praised for the material-flow vs signal distinction; 4-03 completeness check 5/5, "40+ code blocks", probe pattern unexplained, `criteria` vs `scope`, `counterevidence` vs `residual_uncertainties` felt redundant.
- Ch5 (pp. 25-29): 5-01 model navigation 2/5 ("relief"); 5-02 allocate 3/5 and praised as "well-executed pedagogically"; 5-03 port/interface 4/5, conjugation `~` "circular" explanation.
- Ch6 (pp. 30-34): 6-01 4/5 (feature chains, nested-step rule buried in a comment); 6-02 `/second-level` "5/5 catastrophic", two full ReviewRecords (AC-C06, AS-C06), 50+ blocks, "a novice would give up here"; 6-03 4/5, stopping rule stated here for the first time, partial satisfaction accepted without a decision rule.
- Ch7-10 (pp. 35-54): condensed entries, loads 2-4/5, no new 5/5. Ch7-03 param sweep "no major confusion". Ch8-01 doc comment ~20 lines flagged. Ch10-01 and 10-03 called "honest" (gap found, sign-off deferred to a human).

Diary-level observations I will carry into triage (these are about the diary, not the book):

- D1. The diary contains **three** syntheses written at different depths, and they disagree: an early one (Ch1-2 detailed, Ch3-10 "sampled") predicts "give up between Ch2-3", completion ~20-30%; a Ch1-6 one predicts 70% give up, peak at Ch6-02; the final "grounded in full 10-chapter read" says ~35-40% reach Ch10 with attrition at Ch2-3 and Ch6. The early synthesis is residue from the pass the orchestrator corrected. I treat the final synthesis as the agent's position and will ask it to confirm.
- D2. The top-stuck-point ranking also moved between syntheses (early: mechanism, ISQ/SI, Hawkins, abstract/concrete, flow-typed; final: mechanism, interface/conjugation, abstract/concrete, feature chains, ReviewRecord escalation). Hawkins and ISQ/SI dropped out of the top five without comment.
- D3. The cognitive-load numbers correlate almost perfectly with "number of code blocks" and with "a ReviewRecord appears". The persona may be counting blocks rather than measuring comprehension; probe this.
- D4. Many entries say "shown but not formally defined" about terms the glossary does define (`mechanism`, `interface`, `MoE`, `MoP`, `abstract`). Whether the glossary is reachable from the page is a navigation question I can check in the spot-check.
- D5. Percent-attrition figures ("15% drop", "25% drop") are invented precision from a single simulated reader; I will not carry them into the triage.

## 2. Interview

(appended as rounds complete)

## 3. ACE spot-check: `/second-level` (Ch6-02, "level-2 physical realization")

Chosen because the diary rates it the single worst page ("5/5 catastrophic", "a novice would give up here"). Read in full in the browser at http://localhost:3000/second-level before any interview answer came back. I had already read the diary, so this is not uncontaminated; what follows is my reading against the diary's claims.

What the page actually contains (my count from the rendered page):

- 23 executable cells, each followed by its printed output. The diary's "50+ code blocks" counts rendered blocks (input plus output) and so roughly doubles the cell count. This matches diary observation D3: the persona's load scores track block count.
- Structure: one requirement def (HeatGenerationReq, subject on the abstract carrier) -> AC-C06 built in seven named steps (anchor tag, claim, frame, premises, evidence, challenge, assemble) -> AS-C06 built in the same seven steps -> ResistanceCoil -> rated and weak candidates -> negative control -> eval. The seven-step scaffold is announced in prose ("following the construction zone Hawkins' taxonomy uses (anchor, claim, frame, premises, evidence, challenge, assemble)") and then run twice.
- SysML novelty on the page: none that is new to the reader. requirement def (Ch2), `:>` with `attribute :>> power default =` (Ch2 override; `default =` is explained in one sentence here), `assert satisfy` / `assert not satisfy` (Ch3). The new content is entirely in the two records.
- Prose between cells: one to three sentences each, all doing work (each says what the next cell adds and why). No filler. No figure on the page.
- Ordering: records before the part. The page says why in its second paragraph: the selection "is argued from a stated engineering premise, not read off the name of a part built before the argument for it exists." That is the confirmed extension DL-037 (F3/P4: reserve mechanism-suggestive names until a selection is recorded) applied as page order.

My reading, with full SysML/MBSE context:

- The page is not confusing; it is long and it is repetitive by design. The cost is running the identical seven-step scaffold twice back to back, with record fields that are themselves paragraphs of MoE/MoP and mechanism reasoning. A reader who skims the field text loses nothing needed to proceed: Ch6-03 depends on AC-C06 and AS-C06 existing and validating, not on the reader having internalized every sentence of their rationale.
- Would a true novice stall here? I think a novice would skim, not stop. Nothing on the page is a prerequisite for executing or reading the next page, and the SysML cells are all patterns the reader has already run. The diary's "give up" is a fatigue claim, not a comprehension claim; its own evidence (the "Understood" bullets at the top of the entry correctly summarize every element on the page) shows the persona understood the page.
- Where the diary is right: (i) MoE/MoP appears in `framing_criteria` as a one-line test quoted from the architecture-layers skill, and a novice has no page in the book that defines the two terms before Ch3 uses them; (ii) two full records in one sub-notebook is the densest single page in the book and the index does not warn the reader; (iii) no figure, though a generated view (HeatGenerator -> ResistanceCoil with rated and weak) would be derivable from the model (P3) and would break the wall of text.
- Where the persona's reaction says more about the persona: the "50+ blocks" figure, the "catastrophic" rating assigned to a page whose constructs are all review, and the complaint that ResistanceCoil "appears late, almost as an afterthought", which is the page's deliberate and stated point.

ACE finding for this page: MINOR (dense, repetitive, no figure), not BLOCKING. The density is a consequence of a confirmed Z decision (DL-037 ordering plus P1 full records). Whether to split the two records across notebooks, or move AC-C06 into 6-01, changes the chapter's sub-notebook structure and so affects a learning outcome; that is Z's call (P6), not mine. The missing figure is a P3 item I can recommend.

### Round 1 (asked: one page to fix; best and worst page; which completion estimate)

Novice's answers, condensed (its full text is in its SubagentHandback):

- **One page to fix:** Ch2-03, the first judgment-record notebook. Concrete change: three paragraphs before the first code cell saying what the three record kinds are (asserted_context = framing, asserted_solution = selection, asserted_inference = inference from evidence), what `disposition` means, what `residual_uncertainties` tracks. Claim: "this single page fixed would unlock Ch3-10 because every judgment record after would have grounding."
- **Best page:** Ch1-03 `/specialization`. "Single idea, one syntax, one failure mode, done cleanly." Shortest notebook.
- **Worst page:** Ch6-02 `/second-level`. Reasons given: "50+ code blocks, two full ReviewRecords with deep reasoning, recursion applied first time, three new concepts (ResistanceCoil, allocation chains, MoE/MoP) simultaneously."
- **Completion estimate:** settles on 35-40% reaching Ch10. Reason for the change: Ch7-10 read at ~3/5, so "the material isn't inherently incomprehensible; it's front-loaded"; dropout "is about tolerance for early density, not material complexity."

ACE notes on round 1:

- The agent gave Ch2-03's URL as `/judgment-record-creation`; its own diary entry (p. 12) has `/judgment-context`. An invented slug, in an interview answer, after three fabrication corrections. I will push back and not trust page names from the interview that the diary does not corroborate.
- "Three new concepts simultaneously" on Ch6-02 is wrong on two of three: allocation chains are on 6-01, and MoE/MoP was introduced in Ch3 (AC-C03). My spot-check found no SysML construct on the page new to the reader. Push back.
- The best-page choice (`/specialization`) and the "single idea, one syntax, one failure mode" criterion is exactly SA-8 (one construct per sub-notebook). The persona's positive baseline confirms the SA, which is useful: its complaints about dense pages are complaints about pages where the *analysis* side carries more than one idea even when the SysML side carries none.
- The "front-loaded, not incomprehensible" reframing is the most useful thing the agent has said: it moves its own finding from "the book is unreadable" to "Ch2-6 density is the issue, and Ch7-10 show the book can pace itself."

Checks I ran between rounds (own evidence, not the novice's):

- Glossary CLI: `mechanism`, `MoE`, `MoP`, `allocation`, `abstract definition`, `interface`, `judgment`, `asserted context/solution/inference` all have entries; `conjugation`, `feature chain`, `judgment record` have none. The site nav on every page has a "Glossary" link (/glossary). So four of the novice's "never defined" terms are defined one click away, and three are genuinely undefined anywhere in the book's own vocabulary.
- `/judgment-context` (Ch2-03) read in full: 11 executable cells (the diary says "20+ code blocks": same double-count). Each record field has a one-sentence gloss immediately before its cell. The intro says what an asserted_context record does and does not claim. What the page does *not* do: name the three record kinds, or say in plain words what problem a judgment record solves. `/index-2` adds one sentence: "first example of Hawkins et al. (2011) §3.2 ... asserts that the assumption is appropriate for the context."

### Round 2 (asked: three pushbacks; figures; in-the-moment consistency; Ch6-02 self-assessment)

Novice's answers, condensed:

- **P1 (slug):** concedes `/judgment-record-creation` was invented from memory; `/judgment-context` is right. Says it also answered `/specialization` from memory (that one happens to match diary p. 6). `/second-level` was checked.
- **P2 (block count):** concedes it was counting rendered output blocks as code blocks, across the diary. Revised fresh rating for `/second-level`: "3.5-4/5, not 5/5."
- **P3 (what was new on 6-02):** concedes no new construct. Names what was new: first concrete realization of an abstract part with a bound default (`ResistanceCoil :> HeatGenerator`, `power default = 800`), first two records in one notebook, first satisfaction assertions on physical candidates. "Convergence and depth of previously-seen elements."
- **Q4 (figures):** helped: Ch1-02 box diagram (made abstract vs concrete visible). Hurt: "large dense model diagrams in Ch7+ became visual noise." Missing: "a glossary diagram in the Ch1 overview defining mechanism, interface, abstract, feature chain." (Vague; pushed back in round 3.)
- **Q5 (in-the-moment confusion):** port conjugation `~`, on Ch6-01 `/subsystem-requirements` ("had to re-read to understand directional flow"). The other three (def/type wording, what allocation accomplishes, sign-off philosophy) were noticed only when writing the summary, or inferred by example without stalling.
- **Q6 (self-assessment):** "The 5/5 rating was FATIGUE, not comprehension failure." Fresh: 3.5-4/5. Real top blocker restated as "Chapter 6 convergence": 6-01 at 4/5 followed immediately by 6-02, "not any single page."

ACE notes on round 2:

- The two headline findings of the diary (two 5/5 "catastrophic" pages; "50+ code blocks") are both withdrawn by the persona under questioning. What survives is a sequencing claim: two dense notebooks back to back in Ch6, after a dense Ch4-03.
- Conjugation is the one cross-cutting item with an in-the-moment stall, and it is one of the three terms with no glossary entry. That is a specific, checkable gap.
- The "figure hurt" answer (Ch7+ structure diagrams as noise) is a P3 diagram-audit item: a model-derived figure whose inclusion is not judged for the page's purpose. I will carry it as MINOR pending my own look.

### Round 3 (asked: missing model figure, pushed; glossary use; what exactly is missing at Ch2-03; Ch4-03 recount)

Novice's answers, condensed:

- **R1 (missing figure):** withdrew the "glossary diagram" answer; "I did not identify a model-visualization page with a genuinely missing figure during my read-through. The book appears to render model diagrams where structurally appropriate."
- **R2 (glossary):** never opened `/glossary`. In persona: "assumed it was a reference page at the END of the book, not something to consult while reading forward ... the chapter itself had no 'see Glossary' prompts."
- **R3 (Ch2-03 gap, precisely):** the field glosses are adequate. Missing: (a) that there are three record kinds and what each is for; (b) what problem a judgment record solves. Placement: one paragraph on `/index-2`, before the first record is built, would suffice.
- **R4 (Ch4-03 recount):** "40+ code blocks" withdrawn (my count: 24 rendered blocks, about 12 cells). Fresh rating 4/5. Genuinely new on the page: the probe pattern and the asserted_inference kind; `model.verify_constraint()` new but straightforward. "The 5/5 was combination fatigue."

### A finding about the diary's reading method (own evidence)

Three diary entries quote prose as cut off mid-sentence: Ch2-02 "redeclares the inherited under . The operator is a redefinition", Ch4-02 "None of the three is wired as an accept...", Ch5-03 "receives what sends". I checked `/assumptions` in the browser. The rendered paragraph is complete: "`attribute :>> cycleTime` redeclares the inherited `cycleTime` under `slow`. The `:>>` operator is a redefinition; it can only name an attribute that already exists in the type chain." Every gap in the diary's quotation is an inline `<code>` span. The persona's text extraction dropped inline code, so it read the book's prose with every identifier, operator and keyword deleted. "Receives what `durationOut` sends" became "receives what sends".

Consequences for triage: (i) the three "text cuts off" items are not book defects; (ii) every diary complaint that a sentence "assumes" a term or is "terse" or "circular" was made against prose missing its nouns, and is weaker evidence than it looks; (iii) the conjugation stall (the one in-the-moment confusion the persona reports) was on a sentence it could not have read correctly. The orchestrator should treat prose-clarity findings in this diary as unconfirmed until re-read with inline code intact, and the user-testing skill should tell browser-based learners to read via the accessibility tree or innerText, not a code-stripping extractor.

Two more checks after round 3:

- `/moe-definition` (Ch3-01, 11 cells) and `/second-level` both carry the string "(architecture-layers skill)" inside the learner-facing `criteria` text of a record. `.claude/skills/architecture-layers` is a builder-facing file a learner cannot see.
- `/interfaces` (Ch5-03), conjugation sentence as rendered: "~DurationPort is the conjugate of DurationPort: durationIn receives what a DurationPort sends, the SysML v2 idiom for matching a port to its interface partner." Complete and correct; the diary quoted it as "receives what sends".

## 4. Triage

Severity scale per the user-testing skill: BLOCKING (a true novice cannot proceed without help), MINOR (friction; a determined learner continues), COSMETIC (wording or style; does not impede understanding). Two extra labels where the item is not a book defect: NOT A DEFECT, METHOD.

| # | Point (where) | Severity | Justification (one sentence) |
|---|---|---|---|
| S1 | "mechanism" used from Ch1-01 without definition | MINOR | The glossary defines it (tutorial refinement of F3) one click from every page, and the learner proceeds reading it as "how it is built", which is what the pages mean; the fix is a link at first use, not a rewrite. |
| S2 | No framing of judgment records before Ch2-03: what the three kinds are, what problem a record solves | MINOR | Every field on `/judgment-context` is glossed before its cell and the record runs and validates, so nothing stops the learner; the persona's refined ask (confirmed by my read) is one paragraph on `/index-2`. |
| S3 | ReviewRecord scaffold repeated (Ch2-03, 3-01, 3-03, 4-03, 6-02, 6-03) without a consolidation page | MINOR | Full records as worked examples are required by P1 and SA-7, so the repetition is the design; the cost is page length, the persona proceeded every time, and adding a consolidation page is a structure change for Z. |
| S4 | `/second-level` (Ch6-02) density: two full records, 23 cells, no figure | MINOR | The persona withdrew its 5/5 to 3.5-4 as fatigue, no SysML construct on the page is new to the reader, and the records-before-part ordering is the confirmed DL-037 extension; splitting the records across notebooks is Z's call. |
| S5 | `/completeness-check` (Ch4-03) density | MINOR | Persona withdrew 5/5 to 4/5; the new content (probe pattern, asserted_inference, `verify_constraint`) is explained on the page and the persona names it correctly. |
| S6 | Port conjugation `~` (Ch5-03, Ch6-01) | MINOR | The page's one sentence is complete and correct when read with inline code intact (the persona read it code-stripped), but `~` is a new operator with no glossary term; propose a spec-sourced "conjugated port" entry. |
| S7 | Feature chains (`toastBread.applyHeat`) from Ch5-02 without a name | MINOR | The persona inferred the meaning correctly each time; the notation has no name or glossary entry in the book, so propose a KerML-sourced term. |
| S8 | Abstract vs concrete rule stated once (Ch1-01) | COSMETIC | The rule is stated where introduced, the glossary carries the formal definition, and the persona names no page where it stalled on it. |
| S9 | `ISQ::`/`SI::` unit notation and `[0..*]` multiplicity unexplained at first use | COSMETIC | The persona reports inferring both correctly at first sight; a sentence at first use is a style item. |
| S10 | Hawkins cited, not explained | COSMETIC | `/index-2` gives one sentence and the glossary has the idea definition; the S2 paragraph covers this. |
| S11 | Stopping rule first stated in Ch6-03; partial satisfaction accepted | COSMETIC | Partial satisfaction with recorded residual uncertainty is P1, the thing the book teaches; `/index-6` names the stopping rule; a forward pointer would help but nothing impedes. |
| S12 | Prose "cuts off mid-sentence" (Ch2-02, Ch4-02, Ch5-03) | NOT A DEFECT | The rendered pages are complete; every gap in the diary's quotations is an inline `<code>` span the persona's extractor dropped. |
| S13 | "(architecture-layers skill)" cited inside learner-facing record criteria (`/moe-definition`, `/second-level`) | COSMETIC, RULED | A reference to a builder-facing file in learner content fails P4 (never load-bearing, never visible); replace with the glossary or SEBoK locator for MoE/MoP (F5). |
| S14 | MoE/MoP distinction unclear from Ch3-01 onward | MINOR | Both terms have idea, formal and tutorial definitions in the glossary; the page states the split only as a one-line criteria string, so link it (and fix S13). |
| C1 | "def" / "definition" / "type" / "construct" wording varies | COSMETIC | By the persona's own account noticed only when writing the summary; a `tutorial-style-guide` item. |
| C2 | What allocation accomplishes never stated in prose | COSMETIC | The glossary's tutorial definition says it in one line, and the persona praised `/allocate` as "well-executed pedagogically"; link at first use. |
| C3 | Sign-off deferred to a human; no mechanical gate | NOT A DEFECT | This is SA-7 and P1, the book's thesis; the persona reported it as a discovery in Ch10, not as confusion. |
| C4 | Diagram style varies; Ch7+ full-structure diagrams read as "visual noise" | MINOR (unverified) | A P3 diagram-audit question: whether a whole-model containment figure on a page about one record or requirement includes more than the page means to show, and whether the recipe records that; I did not re-read the Ch7+ pages myself. |
| C5 | Cumulative model loaded from disk; the reader never sees the whole model | MINOR (unverified) | SA-2 by design; a visible link from each chapter index to its `chNN-cumulative.sysml` would close the "trust me" gap, if one is not already there. |
| C6 | No consolidation or checkpoint pages; "relentless" pacing Ch2-6 | MINOR | Structural; the persona's own Ch7-10 ratings (2-4/5) show the book paces down after Ch6, so this is a Ch2-6 question for Z, not a book-wide one. |
| C7 | Glossary never opened; no in-page "see glossary" prompts | MINOR | The single cheapest fix across S1, S6, S7, S8, S14 and C2: the definitions exist and the learner did not know to look. |
| C8 | Diary method: output blocks counted as code blocks (2-3x), slugs invented in interview, three conflicting syntheses appended rather than replaced, inline code stripped from all prose read | METHOD | For the `user-testing` skill: require cell counts, diary-verified slugs, one replaced synthesis, and reading via accessibility tree or innerText. |

BLOCKING: none. MINOR: S1-S7, S14, C4-C7. COSMETIC: S8-S11, S13 (ruled), C1, C2. Not defects: S12, C3. Method: C8.

## 5. Interview probe answers (the five the orchestrator asked for)

1. **One page to fix:** Ch2-03 `/judgment-context`, refined under questioning to one paragraph on `/index-2` naming the three record kinds and the problem a judgment record solves; the field glosses on the notebook page are adequate.
2. **Best / worst:** best `/specialization` ("single idea, one syntax, one failure mode, done cleanly", which is SA-8 described from the learner's side); worst `/second-level`, downgraded by the persona from 5/5 to 3.5-4/5 once block-counting and fatigue were separated out.
3. **Visual load:** figure beat prose on `/part-def` (Ch1-02 box diagram made abstract vs concrete visible); figure as noise in Ch7+ whole-model diagrams; no page identified where a model-derived figure was missing ("the book appears to render model diagrams where structurally appropriate").
4. **Consistency, in the moment:** conjugation `~` only (Ch5-03/6-01); the other three were retrospective. The sentence it stalled on was read with its inline code deleted.
5. **Self-assessment:** the Ch6-02 5/5 "was fatigue, not comprehension failure"; fresh 3.5-4/5; the real top blocker restated as "Chapter 6 convergence" (6-01 at 4/5 immediately followed by 6-02), not any single page.

## 6. ACE verdict

Navigable by a true novice: yes, with friction and no blocking page. The persona completed all 54 pages, its own "Understood" bullets correctly summarize every page including the two it called catastrophic, it withdrew both 5/5 ratings under questioning, and it never opened the glossary that defines most of the terms it reported as undefined. The genuine gaps are small and specific: one framing paragraph on `/index-2` before the first judgment record (S2); glossary links at first use plus three missing terms, conjugated port, feature chain, judgment record (S6, S7, C7); a builder-facing skill citation inside two learner pages (S13, ruled below); and one structural question only Z can answer, whether Ch6's two records should sit in one sub-notebook after Ch4-03 and Ch6-01 (S3, S4, C6). The main caveat is on the evidence, not the book: the persona read every sentence of prose with its inline code stripped, counted output blocks as code, and invented page names when answering from memory, so its prose-clarity findings should be re-run with intact reading before any prose is rewritten.

## 7. Decision-log entry text (for the orchestrator to number and commit)

```
## DL-NNN | 2026-10-02 | user-testing | Novice longitudinal browser test: ACE interview and triage

Path: Handled by ACE (one ruling) / Escalated to Z (structure and minor items)
Decision: No BLOCKING finding. Ruled: remove "(architecture-layers skill)" from learner-facing record criteria text on /moe-definition and /second-level and cite the glossary (SEBoK / tutorial) locator for MoE/MoP instead. Escalated: whether to add a judgment-record framing paragraph to /index-2, glossary links at first use plus three new terms, and whether Ch6-02's two records stay in one sub-notebook. All MINOR and COSMETIC items listed for Z per user-testing skill ("do not decide minor or cosmetic items without Z's direction").
Principles applied: P4 (earn your place, builder-facing lenses never in learner content), F5 (cite the canonical kind of definition), P1 and SA-7 (full worked-example records), P3 (figures as judged views), P6 (Z keeps substantive decisions), user-testing skill severity scale.
Reasoning: (1) The two 5/5 pages were re-read by the ACE: 23 and ~12 cells, no construct new to the reader on 6-02, probe pattern and asserted_inference new on 4-03 and explained there; the persona withdrew both ratings as fatigue, so neither meets "cannot proceed". (2) Three "cut off" prose findings are artifacts of code-stripped extraction; rendered pages are complete. (3) Most "undefined" terms have glossary entries one click away and the persona never opened the glossary; the gap is affordance, not definition. (4) A skill-file citation in learner text is visible to the learner and refers to something the learner cannot reach; P4's test (what gets harder without it: nothing) and F5 (cite the kind of definition asked for) determine the replacement. (5) Adding or moving learner content changes a learning outcome, so those items go to Z.
Determined: yes for the S13 ruling; the structural items (S2, S3, S4, C6) underdetermined at P6 (learning-outcome change).
Extension: yes. P4 has been applied to Tall-lens vocabulary; here it is applied to a citation of a builder-facing skill file inside learner content.
Provenance: ace-interview-notes.md sections 2-4 (interview rounds 1-3, spot-check of /second-level, page checks of /judgment-context, /assumptions, /moe-definition, /interfaces, /completeness-check); glossary CLI results for mechanism, MoE, MoP, allocation, abstract definition, interface, judgment, asserted context (entries exist) and conjugation, feature chain, judgment record (none); DL-037 (records before mechanism-suggestive names); SA-7, SA-8; user-testing skill severity definitions.
  Brief (for Z):
    DECISION NEEDED: which of the novice-test MINOR items to act on before the next user-test run.
    Options:
      A. Affordance only: glossary links at first use of mechanism, MoE/MoP, abstract, allocation; add glossary terms conjugated port, feature chain, judgment record; one framing paragraph on /index-2. No notebook restructuring.
      B. A plus Ch6 restructure: move AC-C06 into 6-01 or split 6-02 so no sub-notebook carries two full records.
      C. A plus a re-run of the novice test with intact inline-code reading before any prose change.
    ACE recommendation: C. The diary's prose findings are weakened by the extraction artifact; A is cheap and safe; B changes chapter structure on evidence the persona itself downgraded.
```
