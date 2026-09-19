# Changelog

## Unreleased

- Added `progress.md` at the vault root: module status, verified commit, and what a half-finished module still needs, so a large vault can be built across sessions without re-planning.
- Script fixes: `unwrap.py` copies YAML frontmatter verbatim instead of joining its keys into one line; `check_wikilinks.py` ignores links inside inline code, resolves embeds by file name anywhere in the vault, and reports bare links whose basename matches several files; `validate_canvas.py` clusters rows by proximity instead of exact `y`, skips `group` nodes, and warns on gaps under 60px.
- Added `tests/` with a good and a bad fixture vault and a unittest suite over the scripts' exit codes and messages. CI runs it.
- Fixed the `SKILL.md` frontmatter: the description contained `: "`, which strict YAML parsers reject. It is now a folded block, and a GitHub workflow parses it on every push.
- Narrowed the trigger to persistent documentation requests; one-off "how does X work" questions no longer match.
- Added `scripts/` with `check_wikilinks.py`, `unwrap.py`, and `validate_canvas.py`; the verification step now runs them instead of describing them.
- Added `references/prose-cleanup.md` so the cleanup pass does not depend on another skill being installed.
- Citations now name the symbol next to `path:line`, and each `00-overview.md` records `source_commit` in its frontmatter.
- Decision-only notes may skip the diagram instead of inventing one.
- Renamed tone rule 4 to "Dense prose over padding" and removed comma splices from the skill text.
- Replaced project-specific examples and the original-session quote with generic ones.
- Rewrote the README in a plainer voice and positioned the skill as agent-agnostic: Agent Skills layout for Claude Code, Codex, Cursor and similar; paste-in instructions for any other LLM.

- Reworked the README with a visual cover, a quick start, a vault layout, and a worked documentation example.
- Corrected installation instructions to copy the inner skill directory, placing `SKILL.md` directly under `~/.claude/skills/codebase-vault-docs/`.
- Added contribution guidance and focused issue and pull request templates.

## 2026-09-19

- Initial release. Extracted and generalized from a real multi-day documentation pass over a multi-module C++ numerical codebase.
- `SKILL.md`: workflow (gather facts, structure as a folder, explain don't index, cross-link instead of duplicating, verify before reporting done).
- `references/tone-and-structure.md`: the full rule set, tone, structure, diagrams, equations, sourcing, and the markdown/Obsidian Canvas formatting gotchas that silently break rendering (hard-wrapped paragraphs, pipe-aliased links inside table cells, canvases with edges that skip tiers).
