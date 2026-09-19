---
name: codebase-vault-docs
description: Build a self-contained technical-reference Obsidian vault for a codebase, module by module. Use when the user wants a codebase, library, or module documented as lasting reference material (not a one-off summary): "document this module," "explain how X works," "build a research vault," "map the architecture," or when continuing an existing vault under research-notes/ or similar. Also use when asked to explain a specific mechanism, algorithm, or equation from source code in a way a reader can understand without opening the source.
---
# Codebase Vault Docs

## What this produces

A folder-per-module Obsidian vault where every file is a real explanation, verified against source, diagrammed, and self-contained. Not a symbol index. Not a citation dump. The end goal, in the user's own words from the session this skill was built from: "yo debería poder tener los docs en la otra mitad de mi pantalla y poder trabajar sin tener que buscar algo para sacarme la duda" (the docs should sit on half the screen and answer questions without ever going back to the source).

**The litmus test, applied to every file before considering it done:** could you copy this file's content into an email, and would the recipient understand the mechanism without having the source (.cpp/.py/.rs/whatever) on their machine? If understanding a paragraph requires opening the cited source line, rewrite the paragraph to carry the meaning itself. The citation is there to let a skeptical reader verify the claim, not to stand in for the explanation.

## Before starting

1. Load `references/tone-and-structure.md` now, in full. It is the actual rulebook (structure, tone, diagrams, equations, citations, markdown formatting gotchas). Do not proceed from memory of a previous session, load it fresh every time this skill is invoked.
2. Identify the vault root (e.g. `research-notes/`) and whether a `conventions/style-guide.md` already exists there. If it does, read it, it may have project-specific refinements layered on top of this skill's defaults. If it doesn't, create one from `references/tone-and-structure.md`'s rule list, adapted to American English regardless of what language the conversation is in.
3. If documenting a large stack of interdependent modules, work bottom-up: primitives first, then domain libraries, then whatever composes them. Each module's note can then cite the (already-documented) module below it instead of re-deriving it.

## Workflow per module

1. **Gather facts before writing a word.** Read the module's own README/DESIGN/CHANGELOG, its primary public headers, and enough of the implementation to ground every equation and every "Decision:" paragraph in an actual source line. For a large module, don't read every file, prioritize the public API and the docs; for a small one, read all of it. Delegating this gathering step to a fresh subagent is fine (a tight, well-scoped research prompt); delegating the *writing* is not, if the first pass reads like an index instead of an explanation, that's a synthesis failure, not a formatting one, redo it yourself using the same gathered facts.
2. **Structure as a folder, never a single file**: `module-name/00-overview.md` as the entry point, plus one file per natural seam (an equation-heavy area, a subsystem, a lifecycle). See the structure rules in the reference doc for the exact pattern.
3. **Write the explanation, not the index.** Every mechanism gets prose that says what it does and why it's shaped that way, a diagram if any step-to-step handoff exists, and equations explained term-by-term, not just quoted. See the reference doc's full checklist, applied per file, before moving to the next one.
4. **Run the stop-slop pass** (invoke the `stop-slop` skill, or apply its checklist directly) on every file before considering the module done: no em dashes, no filler adverbs, no throat-clearing, no AI-tell phrasing.
5. **Cross-link, don't duplicate.** When a mechanism belongs to a different, already-documented module, link to it and give a short, self-contained re-explanation inline (lighter than the authoritative version), never make "go read the other module first" a precondition for understanding this one.
6. **Update the mind map.** Every documented subsystem gets an Obsidian Canvas showing how its pieces connect; add the new module's node(s) and edges rather than leaving the map stale. See the reference doc for canvas JSON gotchas (they are not optional, a naive canvas renders as an unreadable tangle).
7. **Update the vault's home/index page** with links into the new module.
8. **Verify before reporting done**: every wikilink resolves to a real file, every markdown table that contains a piped wikilink has been restructured to avoid the escaping trap (see reference doc), no paragraph was hard-wrapped, no banned word survived outside a direct quote.

## When something doesn't match the docs

If a module's own README/architecture doc claims a dependency or behavior that the actual source doesn't show (a `CMakeLists.txt` that doesn't link what the docs say it should, a feature flag with no effect, a rejected/broken code path), write down what the source actually does and flag the discrepancy explicitly, in the note and in a stack-level "known gaps" section if one exists. Never silently pick one version of the truth. If the discrepancy is a real correctness bug (not just a docs/build mismatch), say so plainly and do not bury it as a footnote.

## Reference

- `references/tone-and-structure.md`: the full rule set (tone, structure, diagrams, equations, citations, external sources, markdown/Obsidian formatting gotchas, canvas layout).
