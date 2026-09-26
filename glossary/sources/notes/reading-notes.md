# Reading notes on the sources

Notes made while seeding the glossary (2026-09-26). They record what was read, what surprised us, and what was left out.

## SEBoK v2.14 (`sebok-v2.14.pdf`)
- Definitions come from the glossary section and from articles (allocation, emergence, alternative solutions). Locators are PDF pages.
- SEBoK's *logical architecture* **contains** the functional view (glossary, PDF 1554). This tutorial separates a functional layer from a logical one, so the tutorial's "logical architecture" is a recorded `gl:differsFrom`, approved by Z in planning (DL-015).
- SEBoK has no glossary entry for *mechanism*, *decomposition*, *concept selection* or *realization*. "Concept" is a problem-space term (the Concept Definition stage), so the tutorial says *selection among alternatives* (article title, PDF 340).
- SEBoK describes three kinds of emergence (simple, weak, strong; PDF 232). The tutorial maps them onto layers by how a value is obtained (computed versus explored); that mapping is ours, not SEBoK's.

## SysML v2.0 language specification, API and Services, KerML
- The language spec is method-neutral: it defines no functional, logical or physical *architecture*. It says a part "can represent any level of abstraction" (Sec. 7.11.1) and gives MoE and MoP only as metadata tags (Sec. 9.3.4).
- Printed page = PDF page minus 32 for the language spec. Section numbers were checked against the headings near each quote.
- KerML 1.1 Beta 2 is older than the SysML v2.0 specification that builds on it.
- Only one edge each is seeded from the API spec (*query*) and KerML (*specialization*), so both sources carry a definition; more join when a term needs them.

## Hawkins et al. 2011 (`hawkins-2011.pdf`)
- Read in full. The repo's earlier section numbers (3.1 asserted inference, 3.2 asserted context, 3.3 asserted solution, 3.4 confidence argument structure) match the paper. Printed page = PDF page plus 2.
- The paper's own name for what the repo calls `residual_uncertainties` is **assurance deficit**, and it names *counter-evidence* as what recognising deficits helps us look for.
- Its argument is that completely mitigating all assurance deficits is not normally achievable, so a judgment about when they can be tolerated is necessary (Sec. 3.4).

## Astrom and Murray, *Feedback Systems* (2nd ed. v3.1.5)
- This is the 2nd edition electronic version, **not** the 2008 first edition that SEBoK cites.
- They use "mechanism" only generically and never "policy" in the tutorial's sense: they write *control law* and *controller*. The tutorial's *mechanism* is therefore a refinement of the input/output dynamics definition (Sec. 3.2), with the word and the determinism emphasis marked as ours.

## Sutton and Barto, *Reinforcement Learning* (2nd ed.)
- *Policy* is defined directly (Sec. 1.3 and 3.5). The environment's *dynamics* p(s', r | s, a) are stochastic in general; "comparatively deterministic" is the tutorial's emphasis, not theirs.

## Douglas, Systems Engineering Parts 3 and 4 (video)
- Read from the YouTube transcripts on 2026-09-26. Transcripts are not committed (copyright). Quotes are short and copied as read; they cannot be checked mechanically, so a reviewer should spot-check the timestamps.
- Douglas's three questions are what / **who** / where. The tutorial's what / **how** / where is a recorded refinement.
- The playlist lists five videos; `docs/references.md` says a six-part series.

## Left out on purpose
- OpenSysML, sysml-toolkit and the Pilot Implementation are toolchain, cited only to flag spec gaps. They define no terms.
- Tall's three worlds and the optimization and control lens are builder-facing and never appear in learner content, so they are neither sources nor terms.
- *Declarative*, *executable specification* and *model checking* have no canonical definition in the sources read, so they are not seeded. They can join if a source is chosen for them.
