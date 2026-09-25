---
name: myst-publication
description: CI pipeline structure, MyST config, GitHub Pages deployment, and exercises/ exclusion rule.
---

# MyST Publication

## myst.yml structure

```yaml
version: 1
project:
  title: Toaster
  github: https://github.com/Open-MBEE/toaster
site:
  template: book-theme
  options:
    baseurl: /toaster
  toc:
    - file: docs/index
    - title: Chapter 1 — System and Purpose
      children:
        - file: chapters/ch01-system-purpose/index
        - file: chapters/ch01-system-purpose/01-abstract-def
        # ... sub-notebooks ...
        - file: chapters/ch01-system-purpose/conclusion
    # ... chapters 2-10 ...
    - file: docs/reproducibility
```

`exercises/` must NOT appear in the MyST TOC. Exercise notebooks are blank workspaces — executing them would fail.

## Node environment

`.nvmrc`: `22` (LTS). `package.json`: `{ "dependencies": { "mystmd": "1.11.0" } }`. Commit `package-lock.json`.

Build command: `npx mystmd build --execute`

## 7-step CI pipeline

1. Provision environment + verify tools (`uv sync --locked`, `npm ci`, `scripts/check-tools.py`)
2. Execute every chapter notebook fresh kernel with timeout (nbclient; **exclude `exercises/`**)
3. Assert expected outputs, diagnostics, negative controls, review-record integrity
4. Stage executed notebooks, generated models, figures, provenance manifest
5. Build MyST HTML (`npx mystmd build`)
6. Check navigation, code, outputs, figures, downloads under `/toaster` base path
7. Deploy to Pages (deployment job only; `pages: write` permission restricted to that job)

## exercises/ exclusion rule

The CI notebook execution step must explicitly exclude `exercises/`. These notebooks are blank workspaces; executing them causes failures. Example nbclient usage:

```sh
uv run jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=300 \
  chapters/**/*.ipynb     # NOT exercises/
```

Or configure nbclient exclude patterns directly. Never execute `exercises/` in CI.

## GitHub Pages deployment

- `pages: write` and `id-token: write` on deployment job only
- Deployment runs only after steps 1–6 pass
- `BASE_URL=/toaster` must be set before the build step
- `|| true` is banned in every CI step

## What A2 must never do

- Set BASE_URL to anything other than `/toaster`
- Skip the notebook execution step
- Deploy from a failed CI run
- Use `|| true` anywhere in CI
- Include `exercises/` in the MyST TOC or notebook execution pass
