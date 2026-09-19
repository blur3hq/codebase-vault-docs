# Changelog

## Unreleased

- Rewrote the README in a plainer voice and positioned the skill as agent-agnostic: Agent Skills layout for Claude Code, Codex, Cursor and similar; paste-in instructions for any other LLM.

- Reworked the README with a visual cover, a quick start, a vault layout, and a worked documentation example.
- Corrected installation instructions to copy the inner skill directory, placing `SKILL.md` directly under `~/.claude/skills/codebase-vault-docs/`.
- Added contribution guidance and focused issue and pull request templates.

## 2026-09-19

- Initial release. Extracted and generalized from a real multi-day documentation pass over a 14-module C++ physics/simulation stack.
- `SKILL.md`: workflow (gather facts, structure as a folder, explain don't index, cross-link instead of duplicating, verify before reporting done).
- `references/tone-and-structure.md`: the full rule set, tone, structure, diagrams, equations, sourcing, and the markdown/Obsidian Canvas formatting gotchas that silently break rendering (hard-wrapped paragraphs, pipe-aliased links inside table cells, canvases with edges that skip tiers).
