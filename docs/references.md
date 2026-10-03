# References

This page lists the primary sources this tutorial draws on.

---

## SEBoK — Guide to the Systems Engineering Body of Knowledge

*Guide to the Systems Engineering Body of Knowledge (SEBoK)*, version 2.14. BKCASE / INCOSE / IEEE Computer Society / SERC.

The tutorial's conceptual source, cited first in this tutorial's citation order ([AGENTS.md Part 1](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md)): the ideas behind functional, logical and physical architecture, MoE/MoP/TPM, allocation, and the "what/how/where" progression this tutorial refines. SEBoK itself nests the functional view inside the logical architecture (PDF 587, 593, 1554), which is why the tutorial's own logical/functional split is a recorded departure (a departure from SEBoK's use of the term, stated in the [logical architecture](glossary.md#logical-architecture) entry and approved by mzargham (Z)), not a restatement.

## Åström and Murray — Feedback Systems

K. J. Åström and R. M. Murray. *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd ed., electronic edition v3.1.5 (2020-07-24). (SEBoK itself cites the 2008 first edition; this tutorial uses the current 2nd edition instead.)

The canonical control-theory anchor for **mechanism**: a system as an input-to-output dynamic relation (state-space form `dx/dt = f(x, u)`, §3.2), distinct from a control law that chooses inputs. Cited only for this term, outside the SEBoK/OMG-spec canon; the tutorial's specific word "mechanism" and its determinism emphasis are a recorded refinement, not this source's own vocabulary.

## Sutton and Barto — Reinforcement Learning: An Introduction

R. S. Sutton and A. G. Barto. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018 (authors' PDF).

The canonical anchor for **policy**: a rule for choosing actions given states (§1.3, §3.5), against the environment's own dynamics. Cited only for this term, alongside Åström and Murray's "control law" as a near-synonym; neither source uses "mechanism" or "policy" in exactly the tutorial's sense, so both terms are recorded refinements.

## Brian Douglas — Systems Engineering: Managing System Complexity

A MATLAB Tech Talk series by Brian Douglas, published by MathWorks in 2020; the playlist lists five parts (verified 2026-09-26, [`glossary/sources/notes/reading-notes.md`](https://github.com/Open-MBEE/toaster/blob/main/glossary/sources/notes/reading-notes.md)). Parts 3 and 4 both use a domestic toaster as the worked example and establish the engineering ground truth this tutorial re-implements in SysML v2 and Python.

**Part 3 — The Benefits of Functional Architectures**
Brian Douglas. MathWorks, October 15, 2020. 14:24.
YouTube: <https://www.youtube.com/watch?v=UTm1ORuZ1dg&list=PLn8PRpmsu08owzDpgnQr7vo2O-FUQm_fL&index=3>
MathWorks: <https://www.mathworks.com/videos/systems-engineering-part-3-the-benefits-of-functional-architectures-1602837771665.html>

Introduces functional, logical, and physical architectures. Demonstrates progressive decomposition of `toast bread` into approximately 15 verb-noun functions, with material, energy, and signal flows at each level. Establishes the principle that functions describe WHAT, not HOW, and that functional completeness is auditable by accounting for every input and output.

**Part 4 — An Introduction to Requirements**
Brian Douglas. MathWorks, October 28, 2020. 15:05.
YouTube: <https://www.youtube.com/watch?v=Iblo2Il-pOA&list=PLn8PRpmsu08owzDpgnQr7vo2O-FUQm_fL&index=4>
MathWorks: <https://www.mathworks.com/videos/systems-engineering-part-4-an-introduction-to-requirements-1603872564696.html>

Introduces requirements as the quantification layer of systems engineering. Demonstrates requirement anatomy (description, rationale, verification method), requirement types (functional, performance, constraint, and others), and requirement hierarchy using the toaster as the worked example — from high-level stakeholder needs down to component-level specifications. Connects requirement structure to the functional architecture introduced in Part 3.

Full series index: <https://www.mathworks.com/videos/series/systems-engineering.html>

---

## Hawkins et al. 2011 — A New Approach to Creating Clear Safety Arguments

R. Hawkins, T. Kelly, J. Knight, P. Graydon. In *Advances in Systems Safety* (Proceedings of the 19th Safety-Critical Systems Symposium), Springer, 2011, pp. 3–23.

Defines the three judgment sites used in this tutorial's ReviewRecord structure: asserted context (§3.2), asserted inference (§3.1), and asserted solution (§3.3). Also introduces the appropriateness, sufficiency, and trustworthiness criteria for evidence — the basis for the tutorial's worked-example judgment records.

---

## SysML v2 Language Specification

OMG Systems Modeling Language v2.0 (SysML v2). Object Management Group, formal/2026-03-02.

The normative specification for all SysML v2 constructs used in this tutorial. Chapter references appear in gap comments (e.g., `§7.16`) where a construct is loaded via string rather than through a future Editor API call.

---

## OpenSysML

Open-MBEE/OpenSysML. <https://github.com/Open-MBEE/OpenSysML>

The Python library (`opensysml==0.9.0`) used to load, validate, evaluate, and query SysML v2 models in this tutorial. All model loading uses `conn.load_from_content(content, strict=False)`. Gaps between the library's current API and the SysML v2 specification are tracked in [DEFERRED.md](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md) and as issues in this repository and upstream.

---

## ISQ and SI Units

ISO 80000 (International System of Quantities) and SI (International System of Units). The `ISQ::*` and `SI::*` packages imported in every model provide typed physical quantities (e.g., `ISQ::PowerValue`, `ISQ::DurationValue`, `ISQ::EnergyValue`) and unit literals (e.g., `SI::W`, `SI::s`, `SI::J`).
