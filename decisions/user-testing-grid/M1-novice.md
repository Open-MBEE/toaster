# Grid cell M1-novice — GitHub repo, Novice persona

## First five minutes (required for M1, per the design doc)

I land on the GitHub page and see README.md rendered first. The title "Toaster" is immediately followed by a clear, one-sentence description: "An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML." I read that I'll start from an abstract system and progressively add detail to a domestic toaster example. This makes sense and feels concrete.

I then see a note that "no site is published yet" and I'm directed to docs/setup.md for local setup. This is honest and clear—I appreciate the transparency, though it signals the project is incomplete. I see academic references (Hawkins, Douglas) and that this is adapted from established materials, which suggests credibility.

The Quick Start section lists commands: `git clone`, `uv sync --locked`, `uv run pytest`, and npm/mystmd for the book. I recognize git and npm but not `uv` or `mystmd`. The command sequence looks manageable but I'd need to research what these unfamiliar tools do before proceeding.

I then skim the top-level structure via `ls`. I see chapters/, exercises/, models/, src/, tests/, docs/, and decisions/—all organized and named clearly. I notice some files that seem project-internal (AGENTS.md, CLAUDE.md, DEFERRED.md) at the root level, which I don't immediately understand the purpose of. The presence of a test suite and a build system (myst.yml, package.json, pyproject.toml) suggests active maintenance.

I check the LICENSE and confirm it's Apache 2.0, which is permissive and recognizable.

**Clone decision:** I would clone this, but with hesitation. The tutorial structure is appealing and the documentation is clear, but I'd want to understand the prerequisites (uv, mystmd) before diving in. The "not published" status tells me I'm getting early access to something in-progress, which could be an advantage if I want to contribute or a risk if I need stability.

## Structured findings

- id: M1-novice-01
  severity: positive
  location: README.md, lines 3-5
  quote: "An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML. Starting from one abstract system definition, readers progressively add purpose, requirements, measures, functions, structure, and executable behavior for a domestic toaster."
  expected: A clear, concise statement of what the tutorial teaches
  actual: The description is concrete, uses a relatable example (toaster), and outlines a progressive learning path

- id: M1-novice-02
  severity: friction
  location: README.md, line 7
  quote: "No site is published yet; deployment stays off until the tutorial has complete, end-to-end content ready to publish."
  expected: Transparent project status that doesn't alarm newcomers
  actual: Clear disclaimer, but signals incompleteness which may deter some visitors from cloning

- id: M1-novice-03
  severity: friction
  location: README.md, lines 19, 26-27
  quote: "uv sync --locked" and "npx mystmd start --execute"
  expected: Setup commands using tools I would recognize (pip, npm)
  actual: Introduces unfamiliar tools (uv, mystmd) without explaining what they are or why they're needed

- id: M1-novice-04
  severity: confusing
  location: Repository root directory
  quote: Files like AGENTS.md, CLAUDE.md, DEFERRED.md at root level
  expected: Root-level files to be primarily user-facing (README, LICENSE, setup instructions)
  actual: Contains project-internal coordination files that a first-time visitor would not immediately understand

- id: M1-novice-05
  severity: positive
  location: README.md, lines 9-11
  quote: "Adapted from Brian Douglas's Systems Engineering Part 3 and Part 4... Engineering judgment records follow Hawkins et al. 2011 §§3.1–3.4."
  expected: Attribution and sourcing
  actual: Clearly cites academic foundations and established materials, signaling credibility and research backing

- id: M1-novice-06
  severity: positive
  location: README.md, lines 32-43 (Repository structure)
  quote: "chapters/ — worked example notebooks (10 chapters, read-only for exercises) exercises/ — parallel exercise notebooks (fork and work here)"
  expected: Organized directory structure with clear roles for different files
  actual: Structure is logical and well-annotated, making it easy to understand where to start reading and where to write your own work

- id: M1-novice-07
  severity: positive
  location: Repository root, LICENSE file
  quote: Apache License Version 2.0
  expected: A recognizable, permissive open-source license
  actual: Apache 2.0 is present and immediately identifiable

- id: M1-novice-08
  severity: positive
  location: Repository root, presence of tests/
  quote: Directory "tests/" with pytest suite referenced in Quick Start
  expected: Evidence of automated testing
  actual: Presence of a comprehensive test suite suggests maintenance and quality assurance

## Overall

PASS, with minor friction. As a first-time visitor, I would clone this repository. The README is clear and welcoming, the structure is professional and organized, and the academic grounding is reassuring. The "not published yet" disclaimer and unfamiliar tools (uv, mystmd) introduce friction but not blockers—I'd research these tools before running the quick start. The project feels maintained, credible, and thoughtfully designed for learning.
