# Tone, Structure, and Formatting Rules

This is the actual rulebook. Check every file against it before considering the file, or the module, done.

## Two kinds of document (if the vault also has a worklog)

- **Worklog**: a chronological record of what was done, when. One file per day. Entries are additive, never rewritten except to correct a factual error. Dates belong here.
- **Technical notes**: a description of a system as it currently is. No dates in the body, no narrative of how it got there (that's what the worklog and `git log` are for). Edited in place: when the system changes, the note changes with it.

Do not mix the two. A technical note is never "on 2026-09-19 we found that..."; it is "the retry queue drains oldest-first..."

## Tone

1. **State facts, not justifications.** Describe what the code does, not why it is good that it does so. "The solver receives `terrain_profile` as an array of `{distance_m, height_m}` samples" is a fact. "The solver should never see a map, because that keeps it narrow" is a justification, admissible only when the sentence documents an actual architecture decision (rule 3).
2. **Justify only from demonstrable logic or measured experience, never preference.** Admissible: a physical/mathematical constraint, or a measured/observed result (a test, a benchmark, an incident, a changelog entry describing a real bug). Not admissible: taste, style, or an unstated design preference dressed up as a rule.
3. **Architecture decisions are the one place justification belongs.** When a document records a decision, prefix the paragraph with **Decision:** and give the actual reason on record (quote the source), not an invented one. Do not present a decision as a law of nature, and do not present a fact as if it needed defending.
4. **Axioms and principles over prose.** Prefer short, checkable statements to meandering paragraphs, but see "Explain, don't index" below, this is about density, not about degenerating into a bare list.
5. **Define terms before reusing them.** A future reader should never need git history or tribal knowledge to know what a project-specific term means.
6. **American English**, always, regardless of what language the conversation is conducted in.
7. **Never use "What it is / What it is not" headers, or a "does not own/do" table column.** This reads as AI-generated scope-delimiting filler. Describe what a component is and does in natural prose; fold a real boundary fact into that prose instead of giving it its own negative-framed section.

## Explain, don't index

A table of symbols with file:line citations, or a block of quoted "Decision:" paragraphs with no surrounding prose, is a reference appendix, not a technical note. This is the single most common failure mode and the one most worth checking for before calling a file done.

- Every note leads with prose that explains **how the thing works and why it's shaped that way**. Citations back up a claim; they are never the claim itself.
- If a paragraph only makes sense to someone who then opens the cited source line, it has failed the litmus test (see SKILL.md). Rewrite it to carry the meaning.
- A small, simple module still gets full explanatory treatment. "It's just three constants and an interface" is not an exemption, explain why those three constants are grouped together and what problem the interface solves.

## Structure

- **One file per subject is never enough.** Every module gets its own folder: `00-overview.md` as the entry point (short, orienting, links to the rest), plus separate files that each go deep on one real mechanism, split along the module's natural seams (not padded to hit a file count).
- The overview file gets an at-a-glance diagram of the module's own pieces and, if useful, of the module's place in the larger stack.
- Cross-module dependency: link to the authoritative note (`[[full/vault/path|alias]]`), and for anything load-bearing to understanding *this* module, re-explain it briefly and self-contained right there too (lighter detail than the authoritative version is fine). Never make "go read that other note first" a precondition.

## Diagrams

- **Every file gets at least one diagram, no matter how small the subject.** "Too simple to draw" is never a reason to skip one; draw who calls it, what it hands back, how its pieces relate.
- **Show a computation, don't narrate it.** If step 1 produces `x` and step 2 consumes `x` to produce `y`, that handoff is a flowchart with `x` as a labeled edge from producer to consumer, not a sentence saying "the result is then used for y." Prose explains what a diagram cannot show (the *why*); it never substitutes for the diagram.
- Every module gets a full start-to-end walkthrough this way (a request lifecycle, a computation pipeline), not disconnected fragments.
- Use Mermaid (`flowchart`, `sequenceDiagram`) for a single module's internal mechanism, natively rendered inside a note.
- Use an Obsidian Canvas (`.canvas`, plain JSON) for the cross-module picture, see the Canvas section below, it is easy to make unreadable.

## Equations

- **Explain, don't just quote.** Citing a formula with a file:line is necessary but not sufficient. Say what each term means physically, why the equation has that shape, and where its inputs come from.
- Prefer LaTeX (`$...$` inline, `$$...$$` display) over a bare code block for real math; it's more readable and matches how the source's own comments usually present it.
- **Cite external sources when the code does.** When a comment names a book, a paper, or a classical algorithm (Hairer's `dop853.f` reference, Vincenty's method, Fritsch-Carlson monotonic splines, Cox-de Boor recursion), name that source by author/title in the note, not just the internal file:line. Only for well-established, confidently-known attributions, never invent a year, edition, or page number.

## Sourcing and honesty

- Every equation, decision, and non-obvious claim needs a `file:line` citation the reader could go check.
- When a module's own documentation (README, architecture doc) disagrees with what the source actually does (a claimed dependency that isn't linked, a feature flag with no effect), write what the source does and flag the mismatch explicitly. Don't silently pick a version of the truth.
- A real correctness bug found while researching (not just a docs/code mismatch) gets stated plainly and prominently, in the module's own overview, not buried as a footnote three files deep.

## Markdown formatting (the parts that silently break rendering)

- **Never hard-wrap a paragraph or list item.** Write each paragraph, and each list item's text (including wrapped continuations), as one single line in the source file, however long. A manual line break mid-paragraph renders as a real, visible line break for a reader without "Readable Line Length" enabled in Obsidian, producing a ragged column instead of flowing prose. Headings, table rows, list-marker lines, and fenced code/Mermaid blocks are unaffected, they must stay exactly as authored, line by line.
  - If converting an existing hard-wrapped vault: write a small script that joins consecutive non-blank lines into one, resetting on blank lines, table rows (`^\s*\|`), headings (`^#`), and fence toggles (`` ^``` ``); a line starting with a list marker (`-`, `*`, `+`, `N.`) flushes the previous buffer and starts a new one (preserving *its own* leading indentation for nested lists, do not `.strip()` the first line of a buffer). Verify with a word-count diff (before == after) across every file, not just a visual spot check.
- **Never put a pipe-aliased wikilink (`[[path|alias]]`) inside a markdown table cell.** The literal `|` has to be escaped as `\|` for table syntax, and whether Obsidian correctly unescapes it before resolving the link is not something to gamble on. Either restructure the table into a bullet list, or drop the alias/link inside the cell and rely on prose elsewhere on the page for the real link.
- **Cross-module wikilinks use the full vault-root-relative path** (`[[libs/parser-core/00-overview|parser-core]]`), never a `../` relative path (not valid Obsidian syntax) and never a bare filename shared by many modules (e.g. every module's entry file is named `00-overview.md`; a bare `[[00-overview]]` is ambiguous vault-wide). Same-folder links to a sibling file in the same module can stay bare (`[[01-solve]]`) since that basename is normally unique.
- Before reporting a module done, grep every `[[path/...]]` link and confirm the target file exists (a quick script beats trusting memory across dozens of files).

## Canvas (mind map) layout

A naively laid-out canvas renders as an unreadable tangle of crossing lines. Rules that keep it legible:

- Lay out nodes in a **strict grid by tier/row**; give every row in the same conceptual layer the same y-coordinate.
- **Only draw edges between adjacent rows.** An edge that skips two or three tiers to reach a distant node sweeps across every row in between and is the single biggest cause of visual mess. If a real dependency genuinely skips tiers, mention it in the note's prose instead of drawing it on the map.
- Order nodes left-to-right within a row so that a node's primary edge(s) to the row below/above are short, near-vertical lines, not long diagonals sweeping across the whole width. When two nodes in a row both connect to the same node one row over, straddle that shared node between them.
- Keep floating annotation/fact nodes to a minimum (one or two, not five), and place each directly adjacent to the one row it's relevant to, never scattered through the middle of the dependency lines.
- Give every node comfortable width/height and real spacing (60px+ gaps); check for x-range overlaps between adjacent same-row nodes before publishing.
- Validate the `.canvas` file as JSON before considering it done (a syntax slip fails silently in the UI otherwise).
