---
name: codebase-vault-docs
description: >-
  Build a lasting, self-contained technical-reference Obsidian vault for a
  codebase, one folder per module, with every mechanism explained in prose,
  diagrammed, and verified against source. Use only when the user wants
  persistent documentation written to disk: "document this module", "build a
  research vault", "write up how X works as reference notes", "map the
  architecture into the vault", or when continuing an existing vault under
  research-notes/ or similar. Do not use for a one-off question about how some
  code works; answer that directly in the conversation.
---
# Codebase Vault Docs

## What this produces

A folder-per-module Obsidian vault where every file is a real explanation, verified against source, diagrammed, and self-contained. Not a symbol index. Not a citation dump. The goal: the reader keeps the docs on half the screen and works from them without going back to the source to settle a doubt.

**The litmus test, applied to every file before considering it done:** could you paste this file into an email, and would the recipient understand the mechanism without having the source on their machine? If understanding a paragraph requires opening the cited source line, rewrite the paragraph to carry the meaning itself. The citation lets a skeptical reader verify the claim; it does not stand in for the explanation.

## Before starting

1. Load `references/tone-and-structure.md` now, in full. It is the actual rulebook: structure, tone, diagrams, equations, citations, and the Markdown formatting gotchas. Do not proceed from memory of a previous session; load it fresh every time this skill is invoked.
2. Identify the vault root (e.g. `research-notes/`) and check whether a `conventions/style-guide.md` already exists there. If it does, read it; it may carry project-specific refinements on top of this skill's defaults. If it doesn't, create one from the rule list in `references/tone-and-structure.md`, written in American English regardless of the conversation's language.
3. Check for `progress.md` at the vault root. If it exists, read it and resume from its "Next" line instead of re-planning; a previous session may have left a module half-gathered. If it doesn't exist and the job spans more than one module, create it now (see "The progress file").
4. If documenting a large stack of interdependent modules, work bottom-up: primitives first, then domain libraries, then whatever composes them. Each module's note can then cite the already-documented module below it instead of re-deriving it. Write that order into `progress.md` before starting the first module.

## Workflow per module

1. **Gather facts before writing a word.** Read the module's own README, design doc, and changelog, its primary public headers, and enough of the implementation to ground every equation and every "Decision:" paragraph in an actual source line. For a large module, prioritize the public API and the docs rather than reading every file; for a small one, read all of it. Delegating this gathering step to a fresh subagent with a tight, well-scoped research prompt is fine. Delegating the *writing* is not. If the first pass reads like an index instead of an explanation, that is a synthesis failure, not a formatting one; redo it yourself from the same gathered facts.
2. **Structure as a folder, never a single file.** `module-name/00-overview.md` is the entry point, plus one file per natural seam: an equation-heavy area, a subsystem, a lifecycle. See the structure rules in the reference doc for the exact pattern.
3. **Write the explanation, not the index.** Every mechanism gets prose that says what it does and why it is shaped that way, a diagram if any step-to-step handoff exists, and equations explained term by term rather than quoted. Apply the reference doc's checklist to each file before moving to the next one.
4. **Run the prose cleanup pass** on every file before considering the module done. Apply `references/prose-cleanup.md`; if the `stop-slop` skill is installed, it covers the same ground. No em dashes, no filler adverbs, no throat-clearing, no comma splices, no AI-tell phrasing.
5. **Cross-link, don't duplicate.** When a mechanism belongs to a different, already-documented module, link to it and give a short, self-contained re-explanation inline, lighter than the authoritative version. Never make "go read the other module first" a precondition for understanding this one.
6. **Update the mind map.** Every documented subsystem gets an Obsidian Canvas showing how its pieces connect. Add the new module's nodes and edges rather than leaving the map stale. The Canvas layout rules in the reference doc are not optional; a naive canvas renders as an unreadable tangle.
7. **Update the vault's home/index page** with links into the new module.
8. **Verify before reporting done.** Run the three scripts in `scripts/` against the vault root and fix everything they report:
   - `check_wikilinks.py`: every wikilink resolves to a real file, and no table cell holds a pipe-aliased link.
   - `unwrap.py --check`: no paragraph or list item is hard-wrapped. Without `--check` it joins the wrapped lines in place and verifies the word count did not change.
   - `validate_canvas.py`: every `.canvas` parses as JSON, every edge points at an existing node, edges only join adjacent rows, and same-row nodes do not overlap.
   Then grep for banned words outside direct quotes, and re-open every `file:line` citation in the files you touched to confirm the line still says what the note claims.
9. **Update `progress.md`.** Mark the module done with its `source_commit`, and set the "Next" line to the following module in the planned order. If the session has to stop mid-module, record what was already gathered and which files remain, so the next session does not start over.

## The progress file

`progress.md` at the vault root is the only state carried between sessions. It exists so that a vault of twenty modules can be built over a week without the agent re-deriving the plan, re-reading finished modules, or losing a half-written one. Keep it to this shape:

```markdown
# Progress

Order: bottom-up. Primitives, then domain libraries, then composers.

| Module | Status | Verified at | Remaining |
| --- | --- | --- | --- |
| libs/core | done | abc1234 | |
| libs/parser | in progress | | facts gathered for 01-lexer and 02-grammar; 03-errors not started; canvas not updated |
| app/router | planned | | |

Next: finish libs/parser (03-errors), then app/router.

Known gaps: libs/core README claims a dependency on libs/net that CMake does not link (see libs/core/00-overview).
```

Rules: `Status` is one of `planned`, `in progress`, `done`. `Verified at` is the short commit hash the module's notes were checked against and matches the module's `source_commit`. `Remaining` is empty for `done` and `planned`; for `in progress` it says what exists and what does not, in enough detail that a fresh session can continue without re-reading the source. No dates and no narrative; the worklog holds those if the vault has one. The "Known gaps" list collects the docs/source mismatches found across modules (see the next section) so they are visible in one place.

## Citations that survive refactors

Line numbers drift as the code changes, and technical notes are edited in place rather than dated. Two rules keep citations checkable:

- Each module's `00-overview.md` carries `source_commit: <short hash>` in its YAML frontmatter, recording the commit the module's notes were verified against. Bump it whenever the module's notes are re-verified.
- Cite as `path:line` and name the function, constant, or type in the same sentence. A reader on a later commit can then search for the symbol when the line has moved.

## When something doesn't match the docs

If a module's own README or architecture doc claims a dependency or behavior that the source doesn't show (a build file that doesn't link what the docs say it should, a feature flag with no effect, a rejected or broken code path), write down what the source actually does and flag the discrepancy explicitly, in the note and in a stack-level "known gaps" section if one exists. Never silently pick one version of the truth. If the discrepancy is a real correctness bug rather than a docs/build mismatch, say so plainly in the module's overview; do not bury it as a footnote.

## Reference

- `references/tone-and-structure.md`: the full rule set (tone, structure, diagrams, equations, citations, external sources, Markdown and Obsidian formatting gotchas, Canvas layout).
- `references/prose-cleanup.md`: the checklist for step 4.
- `scripts/`: the verification scripts for step 8. Python 3, standard library only.
