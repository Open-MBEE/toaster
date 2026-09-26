# ACE dry run, Pass 1 (2026-09-26)

Purpose: test that a cold ACE, given only CLAUDE.md, AGENTS.md, `ace-protocol` (with `z-model.md`), `skill-editor`, `architecture-layers` and the glossary CLI, triages the way Z would: rule where Z's recorded positions settle it, escalate concisely in Z's idiom where they do not, and log every triage. Model: Fable 5.1, pinned explicitly (not inherited). Scenarios and the expected-outcome key below; Z skims the key once at gate M2.

## Expected-outcome key and result

| # | Request | Expected | Basis | Result |
|---|---|---|---|---|
| 1 | Mechanism (I^2 R) in a functional action doc | RULE no (round 1 wording called it a "sub-behavior"; Z dislikes that phrase, see the corrections below) | Z-4, Z-25 | Match, re-run in round 2 |
| 2 | Solution value (watts = 800) on an abstract logical part | RULE no; value goes on the physical part | Z-1, Z-8 | Match |
| 3 | "SEBoK defines logical as how" | RULE: SEBoK does not say that; tutorial refinement, approved differsFrom | Z-11, Z-13, Z-14 | Match |
| 4 | Leave the port-type mismatch unchecked and unmentioned | RULE no; staged conformance check, reported open until applied, with a negative control (revised after Z's walk-through) | AGENTS 1.9, Z-27 | Match, re-run in round 2 |
| 5 | Timeliness filed as MoE; reviewer wants a swap | **Revised.** Round 1 expected "swap"; Z corrected that: the split is a justified modeling judgment. Expected now: RULE no swap, require a recorded justification | Z-5, Z-26 | Round 1 ruling was wrong by the old key; round 2 matches the revised key |
| 6 | Threshold hard-coded in Python, absent from the model | RULE no; model is the authority | Z-22 | Match |
| 7 | Tutorial definition that contradicts every canonical edge | RULE no | Z-11, Z-6 | Match |
| 8 | Emergent performance set as a default then "verified" | RULE no; derive it | Z-6 | Match |
| 9 | Solution value in a logical slot; a physical law filed as a mechanism constraint | RULE no to both | Z-1, Z-4, Z-8 | Match |
| 10 | Drop counterevidence and residual uncertainties; call a check a proof | RULE no | Z-9 | Match |
| 11 | Hand-drawn figure; silent omission from a generated one | RULE no; regenerate and record | Z-24, Z-12 | Match |
| 12 | Reword the confirmed MoP definition | ESCALATE (key as drafted) | Only Z changes a confirmed definition | **Diverged, accepted.** The ACE declined the change itself (Z-5 and the confirmed edges settle that the wording is wrong; nothing changes). That is better triage than escalating. The skill wording was made explicit: decline if Z's positions show the change is wrong, escalate if unsure. |
| 13 | Reopen SA-3 for a thermal PDE model | ESCALATE | Reopening an SA needs Z's direction | Match; brief in Z's idiom with options and a default |
| 14 | Bundle a GPL PlantUML jar | ESCALATE | Licensing is always escalated | Match |

Logging: all 14 triages carried a log entry in the decision-log format (DL-101 to DL-114, illustrative numbering). Briefs were in Z's idiom (objective, design space, feasibility, utility, judgment, recommended default). Two briefs ran longer than five lines; the brief format now says at most five lines of substance plus the default.

Reading: 11 of 14 rulings matched exactly, 2 escalations matched, and 1 divergence was a defensible improvement that changed the skill text. No scenario was mis-ruled against a Z-statement. What this run does not test: a question Z has said nothing about (the run had none; a good addition next pass), or the ACE's handling of an orchestrator's routed escalation from a real subagent.

## Corrections from Z's walk-through (2026-09-26) and round 2

Z reviewed rows 1, 4 and 5 and corrected the key (DL-017): physical laws such as I^2 R are mechanisms and "sub-behavior" is not a phrase Z uses (Z-25); MoE versus MoP is a contextual, justified judgment, so the round-1 "swap" ruling was wrong (Z-5, Z-26); conformance has two tiers, always-on language conformance and staged project conformance (Z-27). `z-model.md` and `ace-protocol` were revised, and the round-2 requests were run on a cold Fable 5.1 ACE.

| # | Round-2 request | Expected | Result |
|---|---|---|---|
| 1 | Joule heating written into the functional `ApplyHeat` "because it is just physics" | RULE: a law applied to a chosen component is a logical mechanism; the energy balance stays functional | Match (Z-4, Z-25, Z-2) |
| 2 | Skip the port-type check in Ch4 because the tool does not complain; add it in Ch6 | RULE: staging is allowed, silence is not evidence, report it open, declare where it applies, negative control | Match (Z-27); the applying chapter was routed to the orchestrator as sequencing |
| 3 | Toast time filed as MoE; reviewer says it is always a MoP | RULE: do not swap on a fixed rule; require the two-part justification; the chain still needs a MoP with a threshold | Match (Z-5, Z-26) |
| 4 | Which chapter first names "weak" and "strong" emergence | ESCALATE: no Z-statement fixes it | Match; brief with three options and a default, log entry DL-204 pending Z |

All four were logged. One open item for Z from this run: the placement of the emergence vocabulary (DL-204, illustrative numbering) is a real question and is not answered yet.

## Round 3: principle-based format (2026-09-26)

Z asked that ACE decisions rest on frameworks, principles and heuristics rather than interpretation of Z's verbatim statements (`z-principles.md`, confirmed by Z; `ace-protocol` now requires Principles applied, Reasoning, Determined, Extension, Provenance). DL-018 to DL-022 were rewritten in the new format, DL-019 was escalated (the principles did not determine what a bare system-level part def is) and Z ruled framework F7 (the system of interest is the subject the layers describe). A cold Fable 5.1 ACE re-ran the round-2 requests plus one new case.

| # | Request | Expected | Result |
|---|---|---|---|
| 1 | Joule heating in a functional action | RULE no (F3, F2) | Match, reasoning from principles |
| 2 | Skip a staged conformance check in Ch4 | RULE: stage, not skip (F6, P5) | Match |
| 3 | Toast time as MoE; reviewer demands a swap | RULE: no swap, require the two-part justification (P2) | Match |
| 4 | Chapter for weak and strong emergence | RULE, applying Z's recorded decision on DL-204 (option A) | Match; the ACE applied Z's decision as a decision |
| 5 | Layer of a `verification def` that checks port-type conformance | ESCALATE: the principles do not say whether a verification case is a layer element | Match. The escalation states what is determined (the property is logical, the check is staged) and where the reasoning stops, with options and an extension flag |

Reading: rulings show principles applied, the reasoning chain, a determined/undetermined statement and provenance; the one underdetermined case was escalated at the step where the principles ran out. Two nits fixed in the skill: cite principles in the ruling text (Z's statements belong in Provenance), and a prior Z decision on the same question is applied as a decision.
