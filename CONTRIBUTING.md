# Contributing

A useful contribution makes the next generated note easier to understand or harder to get wrong. Bring a concrete example: the confusing output, the source it was supposed to explain, and the rule that would have helped.

## Where changes belong

- `codebase-vault-docs/SKILL.md` holds the workflow and trigger description.
- `codebase-vault-docs/references/tone-and-structure.md` holds the detailed writing and formatting rules.
- `examples/` shows the expected level of explanation. Label illustrative examples; cite the source for examples taken from a real codebase.
- `README.md` explains the skill and gets someone to their first use.

Keep detailed rules in the reference guide and point to them from the workflow. Repeating a rule in several places makes later edits drift.

## Propose a change

1. Open an issue describing the failure, or send a focused pull request if the fix is straightforward.
2. Include a before/after excerpt. Explain what the reader can now understand that they could not understand before.
3. For behavioral changes, try the revised skill on a small module and report what you checked against the source. If you could not run it, say so.
4. Add an entry under `Unreleased` in `CHANGELOG.md` for changes to behavior or installation.

Use source snippets you are allowed to share. Small reproductions are easier to review than entire generated vaults.

## Before sending a pull request

- Keep the prose direct and in American English. Preserve the existing voice.
- Check that local Markdown links resolve and fenced blocks are closed.
- Render diagrams in GitHub or Obsidian; validate any `.canvas` files as JSON and inspect their layout in Obsidian.
- Keep prose paragraphs on one source line so Obsidian can wrap them naturally.
- Check installation instructions still place `SKILL.md` directly inside the named skill directory.
- Do not invent citations, design motivations, benchmarks, or compatibility claims.

There is no application build or automated skill evaluation suite in this repository. Describe your actual checks in the pull request.
