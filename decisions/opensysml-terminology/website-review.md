# opensysml.org review (2026-10-03)

Read by the orchestrator in the in-app browser: the home page, Downloads and Documentation. Paraphrased; no page text is
copied beyond short names. Requested by mzargham (Z) as the basis for an "OpenSysML" terminology revision.

## What the site says OpenSysML is

- The home page calls the whole thing a **stack** ("OpenSysML isn't a single product"): four independently maintained
  projects built against the same open interfaces.
  1. **OpenSysML**, labelled "the runtime": a complete SysML v2 and KerML implementation in Go (language server, REPL, an
     execution runtime that instantiates parts, evaluates constraints and runs action and state behavior), with Python, Node,
     Java, Rust, Julia and MATLAB clients for its service, and a Go API. Repo `Open-MBEE/OpenSysML`. Apache-2.0.
  2. **sysml-toolkit**, labelled "the tool kit": a Rust workspace for parsing, formatting, linting, JSON/CBOR interchange,
     constraint solving and span-preserving model transformation, plus a language server and Python and WebAssembly
     bindings, built for programmatic pipelines and CI. Repo `Open-MBEE/sysml-toolkit`. Apache-2.0.
  3. **SysML v2 Pilot Implementation**, labelled "the reference": the OMG Systems Modeling Community's implementation
     (Java, Xtext, PlantUML visualization, Jupyter kernel). The other two track its grammar and standard library as their
     conformance baseline. EPL-2.0.
  4. **Flexo MMS**, labelled "the model store": Kotlin microservices that version model data (RDF, SPARQL 1.1) with a
     SysML v2 API layer. Apache-2.0.
- The hero line counts "three independently built implementations": a Go runtime, a Rust toolchain and OMG's reference build.
- Licensing statement: the stack is dual-licensed (Apache-2.0 for code, CC BY 4.0 for wiki text and diagrams) with one
  stated exception, the OMG reference implementation under EPL-2.0.
- Documentation sections: Guide, Manual (document generation), Reference, Internals, Project.
- Downloads (runtime): release bundles named `opensysml-<platform>` contain the `sysml` CLI and `sysml-lsp`; the
  `sysml-grpc` service is separate; packages exist on PyPI (`opensysml`), npm (`@openmbee/opensysml`), crates.io
  (`opensysml`) and as the Go module `github.com/Open-MBEE/OpenSysML`.

## The naming ambiguity the toaster repo must handle

The site uses "OpenSysML" at two levels: the **umbrella** (the stack) and the **runtime project** (repo, Python package,
CLI bundle, version numbers). This repository has used "OpenSysML" for the runtime only (Python package `opensysml`,
version v0.9.0, issues `Open-MBEE/OpenSysML#NNN`), and "sysml-toolkit" for the Rust toolchain (`sysmlv2` binary,
v0.9.1) as a separate thing. Under the new reading, a bare "OpenSysML" no longer says which tool a sentence is about, so
statements of the form "OpenSysML cannot X" change truth conditions (true of the runtime, possibly false of the toolkit).

## Direction from mzargham (Z), 2026-10-03

"The tools provided as part of the sysml toolkit are also considered part of OpenSysML, not just the Go runtime. OpenSysML
is the broader term for the permissively licensed tools related to SysML v2."

Open point: the site's own licensing statement keeps the Pilot Implementation (EPL-2.0) inside the stack as an exception,
while Z's wording says "permissively licensed". Whether the Pilot counts as part of OpenSysML in this repository's prose is
not settled by the site and is for the ACE or Z.
