# References

This page lists the primary sources this tutorial draws on.

---

## Brian Douglas — Systems Engineering: Managing System Complexity

A 6-part MATLAB Tech Talk series by Brian Douglas, published by MathWorks in 2020. Parts 3 and 4 both use a domestic toaster as the worked example and establish the engineering ground truth this tutorial re-implements in SysML v2 and Python.

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

The Python library (`opensysml==0.9.0`) used to load, validate, evaluate, and query SysML v2 models in this tutorial. All model loading uses `conn.load_from_content(content, strict=False)`. Gaps between the library's current API and the SysML v2 specification are tracked in [DEFERRED.md](../DEFERRED.md) and as issues in this repository and upstream.

---

## ISQ and SI Units

ISO 80000 (International System of Quantities) and SI (International System of Units). The `ISQ::*` and `SI::*` packages imported in every model provide typed physical quantities (e.g., `ISQ::PowerValue`, `ISQ::DurationValue`, `ISQ::EnergyValue`) and unit literals (e.g., `SI::W`, `SI::s`, `SI::J`).
