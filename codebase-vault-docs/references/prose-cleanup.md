# Prose Cleanup Checklist

Run this over every note before calling it done. The rules paraphrase the [stop-slop](https://github.com/hardikpandya/stop-slop) skill; if that skill is installed, invoking it is equivalent.

## Cut

- Em dashes. Replace with a period, a comma, a colon, or parentheses, whichever the sentence actually needs. Do not replace mechanically with a comma; that produces comma splices (two independent clauses joined by a bare comma), which are banned too.
- Throat-clearing openers: "It's worth noting that", "Importantly", "In essence", "At its core", "Here's the thing".
- Filler adverbs and intensifiers: "simply", "essentially", "actually", "very", "really", "highly", "seamlessly", "robust", "elegant".
- Scope-delimiting filler: "What it is / What it is not" sections, "does not own" columns, "This is not about X" sentences.
- Quotable one-liners that close a paragraph on a punchline. Rewrite as a plain statement or delete.
- Meta-narration: "The rest of this note covers...", "As we saw above". Link or state the fact instead.

## Restructure

- "Not X, but Y" contrasts: state Y.
- Lists of three by reflex. Two items or four are fine when the subject has two or four.
- Passive voice where the actor matters: name the function, the caller, the thread.
- Inanimate things performing human actions ("the design chooses", "the module wants"). Name the mechanism or the person who decided.
- Three consecutive sentences of the same length. Break one.
- Vague declaratives ("the implications are significant", "this has important consequences"). Name the specific consequence.

## Check

- Every sentence states a fact, a mechanism, or a decision with its source. Nothing evaluates the code's quality.
- Every project-specific term was defined before its first reuse.
- No hard-wrapped paragraphs (run `scripts/unwrap.py --check`).
