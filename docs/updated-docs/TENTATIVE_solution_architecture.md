# Complete Architecture: Maximizing Solution Quality

## The Core Question

How do we get the **best possible solution** to a problem statement, given:
- A set of reference libraries (first principles, secrets, mental models, etc.)
- Multiple possible framings and approaches
- The risk of anchoring, blind spots, and missed insights
- The need for systematic validation

This document describes the complete architecture, showing how parallel generation, synthesis, enrichment, and critique work together.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                    COMPLETE SOLUTION GENERATION ARCHITECTURE                    │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 0: INTAKE & PROBLEM UNDERSTANDING                                   │ │
│  │                                                                           │ │
│  │ • Normalize inputs                                                        │ │
│  │ • Surface implicit assumptions                                            │ │
│  │ • Identify problem type → suggests which libraries matter most            │ │
│  │ • Generate "problem brief" that all inventors receive                     │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 1: DIVERGENT GENERATION (Parallel, Isolated)                        │ │
│  │                                                                           │ │
│  │ Multiple inventors, different contexts, no cross-talk                     │ │
│  │ Goal: Explore solution space broadly                                      │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 2: CROSS-POLLINATION (Optional)                                     │ │
│  │                                                                           │ │
│  │ Inventors review each other's solutions (still pre-synthesis)             │ │
│  │ Goal: Surface disagreements and sharpen contrasts before combining        │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 3: CONVERGENT SYNTHESIS (Blackboard)                                │ │
│  │                                                                           │ │
│  │ Combine best elements from all candidates into unified draft              │ │
│  │ Goal: Produce initial "best of all worlds" solution                       │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 4: LIBRARY-INFORMED CRITIQUE (Enrichment Pattern)                   │ │
│  │                                                                           │ │
│  │ Each library becomes a "lens" for evaluating the unified draft            │ │
│  │ Goal: Systematic validation that nothing was missed                       │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 5: ITERATIVE REFINEMENT (Critique → Revise Loop)                    │ │
│  │                                                                           │ │
│  │ Address issues surfaced by critics; bounded iteration                     │ │
│  │ Goal: Converge on polished solution                                       │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │ PHASE 6: OUTPUT ASSEMBLY                                                  │ │
│  │                                                                           │ │
│  │ Package final solution with provenance, alternatives, and dissent         │ │
│  │ Goal: Complete, auditable deliverable                                     │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Intake & Problem Understanding

**Purpose:** Ensure all inventors start with a clear, normalized problem statement—but don't bias them with solutions yet.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 0: INTAKE                                                                 │
│                                                                                 │
│  User Inputs                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ • Problem Statement                                                      │   │
│  │ • Objectives (with MoSCoW treatments)                                    │   │
│  │ • Constraints (HARD/SOFT)                                                │   │
│  │ • Output Specification                                                   │   │
│  │ • Evaluation Criteria                                                    │   │
│  │ • Reference Libraries (all of them)                                      │   │
│  │ • Prior Solutions (if any)                                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│                            ┌─────────────────────┐                              │
│                            │    NORMALIZER       │                              │
│                            │                     │                              │
│                            │ • Validate inputs   │                              │
│                            │ • Extract implicit  │                              │
│                            │   assumptions       │                              │
│                            │ • Classify problem  │                              │
│                            │   type              │                              │
│                            │ • Flag ambiguities  │                              │
│                            └──────────┬──────────┘                              │
│                                       │                                         │
│                                       ▼                                         │
│                            ┌─────────────────────┐                              │
│                            │   PROBLEM BRIEF     │                              │
│                            │                     │                              │
│                            │ Normalized problem  │                              │
│                            │ statement that ALL  │                              │
│                            │ inventors receive   │                              │
│                            │ (identical baseline)│                              │
│                            └─────────────────────┘                              │
│                                                                                 │
│  Also produces:                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Problem Classification (informs inventor configuration)                  │   │
│  │                                                                          │   │
│  │ • problem_type: "strategy_design" | "system_architecture" | ...          │   │
│  │ • uncertainty_level: high | medium | low                                 │   │
│  │ • key_domains: [investing, technology, operations, ...]                  │   │
│  │ • recommended_library_emphasis: [secrets, first_principles, ...]         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Key insight:** The problem classification can inform *which* inventor configurations to run, but doesn't force it. You might always run the core four (A, B, C, D) plus problem-specific specialists.

---

## Phase 1: Divergent Generation

**Purpose:** Explore solution space broadly through parallel, isolated generation.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DIVERGENT GENERATION                                                   │
│                                                                                 │
│                           Problem Brief (shared)                                │
│                                    │                                            │
│          ┌──────────────┬──────────┼──────────┬──────────────┐                 │
│          │              │          │          │              │                 │
│          ▼              ▼          ▼          ▼              ▼                 │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│   │INVENTOR A  │ │INVENTOR B  │ │INVENTOR C  │ │INVENTOR D  │ │INVENTOR E  │  │
│   │            │ │            │ │            │ │            │ │ (optional) │  │
│   │ Foundationnl│ │ Competitive│ │ Comprehen- │ │ Tabula     │ │ Domain-    │  │
│   │            │ │            │ │ sive       │ │ Rasa       │ │ specific   │  │
│   ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤  │
│   │ CONTEXT:   │ │ CONTEXT:   │ │ CONTEXT:   │ │ CONTEXT:   │ │ CONTEXT:   │  │
│   │            │ │            │ │            │ │            │ │            │  │
│   │ • First    │ │ • Secrets  │ │ • ALL      │ │ • NONE     │ │ • Based on │  │
│   │   Principles│ │ • Tech-    │ │   libraries│ │            │ │   problem  │  │
│   │ • Mental   │ │   nologies │ │            │ │ Only the   │ │   classifi-│  │
│   │   Models   │ │ • Method-  │ │            │ │ problem    │ │   cation   │  │
│   │            │ │   ologies  │ │            │ │ brief      │ │            │  │
│   ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤  │
│   │ MODEL:     │ │ MODEL:     │ │ MODEL:     │ │ MODEL:     │ │ MODEL:     │  │
│   │ Claude     │ │ Claude     │ │ Claude     │ │ GPT-4      │ │ Claude     │  │
│   │ Opus       │ │ Sonnet     │ │ Opus       │ │ (different │ │            │  │
│   │            │ │            │ │            │ │ perspective│ │            │  │
│   ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤  │
│   │ EMPHASIS:  │ │ EMPHASIS:  │ │ EMPHASIS:  │ │ EMPHASIS:  │ │ EMPHASIS:  │  │
│   │            │ │            │ │            │ │            │ │            │  │
│   │ "Ground in │ │ "Maximize  │ │ "Thorough  │ │ "Reason    │ │ Problem-   │  │
│   │ durable    │ │ competitive│ │ coverage,  │ │ from first │ │ specific   │  │
│   │ truths"    │ │ advantage" │ │ miss       │ │ principles │ │ directive  │  │
│   │            │ │            │ │ nothing"   │ │ only"      │ │            │  │
│   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘  │
│         │              │              │              │              │          │
│         ▼              ▼              ▼              ▼              ▼          │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│   │SOLUTION A  │ │SOLUTION B  │ │SOLUTION C  │ │SOLUTION D  │ │SOLUTION E  │  │
│   │            │ │            │ │            │ │            │ │            │  │
│   │ Complete   │ │ Complete   │ │ Complete   │ │ Complete   │ │ Complete   │  │
│   │ solution   │ │ solution   │ │ solution   │ │ solution   │ │ solution   │  │
│   │ per Output │ │ per Output │ │ per Output │ │ per Output │ │ per Output │  │
│   │ Spec       │ │ Spec       │ │ Spec       │ │ Spec       │ │ Spec       │  │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘  │
│                                                                                 │
│   ISOLATION IS CRITICAL: No inventor sees another's work                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Why each inventor matters:**

| Inventor | What it brings | Risk if omitted |
|----------|----------------|-----------------|
| A (Foundational) | Durable, principled architecture | Solution may be tactically clever but fragile |
| B (Competitive) | Differentiation, practical edge | Solution may be sound but undifferentiated |
| C (Comprehensive) | Thorough coverage | May miss non-obvious insights; conventional |
| D (Tabula Rasa) | Unanchored creativity, sanity check | Naive mistakes; but also catches groupthink |
| E (Domain-specific) | Deep domain fit | Generic solution that misses domain nuances |

---

## Phase 2: Cross-Pollination (Optional)

**Purpose:** Before synthesis, let inventors react to each other's work. Surfaces disagreements sharply.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: CROSS-POLLINATION (Optional)                                           │
│                                                                                 │
│ Each inventor receives the OTHER solutions and provides commentary.             │
│ They do NOT revise their own solution—just critique others.                     │
│                                                                                 │
│   ┌────────────────────────────────────────────────────────────────────────┐   │
│   │                                                                        │   │
│   │   Inventor A receives B, C, D solutions                                │   │
│   │   → "What do you disagree with? What did they miss?"                   │   │
│   │   → Produces: Critique of B, C, D from Foundational lens               │   │
│   │                                                                        │   │
│   │   Inventor B receives A, C, D solutions                                │   │
│   │   → "What do you disagree with? What did they miss?"                   │   │
│   │   → Produces: Critique of A, C, D from Competitive lens                │   │
│   │                                                                        │   │
│   │   ... and so on                                                        │   │
│   │                                                                        │   │
│   └────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│   Output: Cross-Critique Matrix                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │              │ Critiqued by A │ Critiqued by B │ Critiqued by C │ ...  │  │
│   │──────────────┼────────────────┼────────────────┼────────────────┼──────│  │
│   │ Solution A   │       —        │ "Misses X"     │ "Too abstract" │ ...  │  │
│   │ Solution B   │ "Unprincipled" │       —        │ "Risky"        │ ...  │  │
│   │ Solution C   │ "Conventional" │ "No edge"      │       —        │ ...  │  │
│   │ Solution D   │ "Naive on Y"   │ "Fresh idea Z" │ "Misses libs"  │ ...  │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   Value: Synthesizer receives not just solutions, but explicit disagreements   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**When to use:** High-stakes problems where understanding *why* inventors disagree is as valuable as the solutions themselves.

**When to skip:** Simpler problems, cost constraints, or when you trust the synthesizer to identify conflicts.

---

## Phase 3: Convergent Synthesis

**Purpose:** Combine the best elements from all candidates into a unified draft.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: CONVERGENT SYNTHESIS                                                   │
│                                                                                 │
│   All solutions + cross-critiques (if Phase 2 ran) loaded to blackboard        │
│                                                                                 │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║                      SOLUTION BLACKBOARD                                ║  │
│   ║                                                                         ║  │
│   ║  candidates[]:                                                          ║  │
│   ║    A: { solution, config, reasoning_trace }                             ║  │
│   ║    B: { solution, config, reasoning_trace }                             ║  │
│   ║    C: { solution, config, reasoning_trace }                             ║  │
│   ║    D: { solution, config, reasoning_trace }                             ║  │
│   ║                                                                         ║  │
│   ║  cross_critiques[]: (if Phase 2 ran)                                    ║  │
│   ║    { critic: "A", target: "B", critique: "..." }                        ║  │
│   ║    ...                                                                  ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: null (to be written)                                    ║  │
│   ║  provenance: {}                                                         ║  │
│   ║  open_issues: []                                                        ║  │
│   ║  resolved_issues: []                                                    ║  │
│   ╚═════════════════════════════════════════════════════════════════════════╝  │
│                          │                                                      │
│                          ▼                                                      │
│              ┌───────────────────────┐                                          │
│              │      SYNTHESIZER      │                                          │
│              │                       │                                          │
│              │  Receives:            │                                          │
│              │  • All candidates     │                                          │
│              │  • Cross-critiques    │                                          │
│              │  • ALL libraries      │◄──── Full context for synthesis          │
│              │  • Evaluation criteria│                                          │
│              │  • Problem brief      │                                          │
│              │                       │                                          │
│              │  Tasks:               │                                          │
│              │  1. Compare approaches│                                          │
│              │  2. Score elements    │                                          │
│              │     against criteria  │                                          │
│              │  3. Identify conflicts│                                          │
│              │  4. Resolve conflicts │                                          │
│              │     with rationale    │                                          │
│              │  5. Combine best      │                                          │
│              │     elements          │                                          │
│              │  6. Track provenance  │                                          │
│              │  7. Flag remaining    │                                          │
│              │     open issues       │                                          │
│              └───────────┬───────────┘                                          │
│                          │                                                      │
│                          ▼                                                      │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║                      SOLUTION BLACKBOARD (updated)                      ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: {                                                       ║  │
│   ║    version: 1                                                           ║  │
│   ║    content: "... synthesized solution ..."                              ║  │
│   ║  }                                                                      ║  │
│   ║                                                                         ║  │
│   ║  provenance: {                                                          ║  │
│   ║    architecture: { from: "C", modified: true, reason: "..." }           ║  │
│   ║    risk_controls: { from: "A", modified: false }                        ║  │
│   ║    competitive_edge: { from: "B", modified: true, reason: "..." }       ║  │
│   ║    simplification: { from: "D", insight: "removed unnecessary X" }      ║  │
│   ║  }                                                                      ║  │
│   ║                                                                         ║  │
│   ║  resolved_issues: [                                                     ║  │
│   ║    { conflict: "A passive vs B active", resolution: "hybrid",           ║  │
│   ║      rationale: "..." }                                                 ║  │
│   ║  ]                                                                      ║  │
│   ║                                                                         ║  │
│   ║  open_issues: [                                                         ║  │
│   ║    { issue: "Technology choice unresolved", severity: "major" }         ║  │
│   ║  ]                                                                      ║  │
│   ╚═════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Synthesizer is the hardest part.** It needs to:
- Not just pick a winner, but genuinely combine elements
- Maintain coherence (no Frankenstein)
- Be explicit about tradeoffs made
- Preserve dissenting views for later reference

---

## Phase 4: Library-Informed Critique (Enrichment Pattern)

**Purpose:** Systematically validate the unified draft against every library. This is your colleague's enrichment pattern, applied post-synthesis.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: LIBRARY-INFORMED CRITIQUE                                              │
│                                                                                 │
│   The unified draft now exists. We systematically check it against each         │
│   library to ensure nothing was missed and no principles were violated.         │
│                                                                                 │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║  SOLUTION BLACKBOARD                                                    ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: { version: 1, content: "..." }                          ║  │
│   ╚═══════════════════════════════╤═════════════════════════════════════════╝  │
│                                   │                                             │
│                                   │ draft is read by all critics                │
│                                   │                                             │
│          ┌────────────────────────┼────────────────────────┐                   │
│          │                        │                        │                   │
│          ▼                        ▼                        ▼                   │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐         │
│   │ FIRST PRINCIPLES│     │    SECRETS      │     │  MENTAL MODELS  │         │
│   │     CRITIC      │     │     CRITIC      │     │     CRITIC      │         │
│   │                 │     │                 │     │                 │         │
│   │ Reads:          │     │ Reads:          │     │ Reads:          │         │
│   │ • Unified draft │     │ • Unified draft │     │ • Unified draft │         │
│   │ • First Princ.  │     │ • Secrets lib   │     │ • Mental Models │         │
│   │   library       │     │                 │     │   library       │         │
│   │                 │     │                 │     │                 │         │
│   │ Questions:      │     │ Questions:      │     │ Questions:      │         │
│   │ • Does draft    │     │ • Which secrets │     │ • What biases   │         │
│   │   violate any   │     │   are embedded? │     │   might be      │         │
│   │   principles?   │     │ • Which are     │     │   present?      │         │
│   │ • Which         │     │   missing?      │     │ • What mental   │         │
│   │   principles    │     │ • Is the edge   │     │   models would  │         │
│   │   are embodied? │     │   defensible?   │     │   improve this? │         │
│   │ • Are any       │     │ • How will      │     │ • Are there     │         │
│   │   missing?      │     │   secrets erode?│     │   blind spots?  │         │
│   └────────┬────────┘     └────────┬────────┘     └────────┬────────┘         │
│            │                       │                       │                   │
│            ▼                       ▼                       ▼                   │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐         │
│   │ OBSERVATIONS    │     │  TECHNOLOGIES   │     │  METHODOLOGIES  │         │
│   │     CRITIC      │     │     CRITIC      │     │     CRITIC      │         │
│   │                 │     │                 │     │                 │         │
│   │ Questions:      │     │ Questions:      │     │ Questions:      │         │
│   │ • Does draft    │     │ • Is chosen     │     │ • Does process  │         │
│   │   align with    │     │   tech mature?  │     │   follow best   │         │
│   │   current       │     │ • Are there     │     │   practices?    │         │
│   │   trends?       │     │   better        │     │ • Are there     │         │
│   │ • What signals  │     │   alternatives? │     │   methodology   │         │
│   │   were missed?  │     │ • Dependencies? │     │   gaps?         │         │
│   └────────┬────────┘     └────────┬────────┘     └────────┬────────┘         │
│            │                       │                       │                   │
│            └───────────────────────┼───────────────────────┘                   │
│                                    │                                           │
│                                    ▼                                           │
│                         ┌─────────────────────┐                                │
│                         │   CRITIQUE MERGER   │                                │
│                         │                     │                                │
│                         │ Combines all critic │                                │
│                         │ findings into:      │                                │
│                         │ • Prioritized       │                                │
│                         │   issues list       │                                │
│                         │ • Coverage report   │                                │
│                         │ • Validation        │                                │
│                         │   confirmations     │                                │
│                         └──────────┬──────────┘                                │
│                                    │                                           │
│                                    ▼                                           │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║  SOLUTION BLACKBOARD (updated)                                          ║  │
│   ║                                                                         ║  │
│   ║  critique_findings: {                                                   ║  │
│   ║    first_principles: {                                                  ║  │
│   ║      violations: [],                                                    ║  │
│   ║      embodied: ["principle_3", "principle_7"],                          ║  │
│   ║      missing: ["principle_12 not addressed"]                            ║  │
│   ║    },                                                                   ║  │
│   ║    secrets: {                                                           ║  │
│   ║      embedded: ["secret_1", "secret_2"],                                ║  │
│   ║      missing: ["secret_4 could strengthen section X"]                   ║  │
│   ║    },                                                                   ║  │
│   ║    ...                                                                  ║  │
│   ║  }                                                                      ║  │
│   ║                                                                         ║  │
│   ║  open_issues: [                                                         ║  │
│   ║    { from: "first_principles_critic", issue: "...", severity: "major" } ║  │
│   ║    { from: "secrets_critic", issue: "...", severity: "minor" }          ║  │
│   ║    ...                                                                  ║  │
│   ║  ]                                                                      ║  │
│   ║                                                                         ║  │
│   ║  library_coverage: {                                                    ║  │
│   ║    first_principles: "85% addressed",                                   ║  │
│   ║    secrets: "60% embedded",                                             ║  │
│   ║    ...                                                                  ║  │
│   ║  }                                                                      ║  │
│   ╚═════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**This is where your colleague's enrichment pattern fits perfectly.**

The difference from the original proposal:
- Libraries aren't used to enrich a single inventor's draft
- They're used to validate/enrich a *synthesized* draft that already combines the best elements

**Key outputs:**
- Which library elements are embodied in the solution
- Which are missing and should be added
- Coverage metrics per library
- Prioritized issues for refinement

---

## Phase 5: Iterative Refinement

**Purpose:** Address issues surfaced by critics until acceptance criteria are met.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: ITERATIVE REFINEMENT                                                   │
│                                                                                 │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║  SOLUTION BLACKBOARD                                                    ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: { version: 1 }                                          ║  │
│   ║  open_issues: [ blockers, majors, minors ]                              ║  │
│   ╚═══════════════════════════════╤═════════════════════════════════════════╝  │
│                                   │                                             │
│                                   ▼                                             │
│                         ┌─────────────────────┐                                │
│                         │  ISSUE PRIORITIZER  │                                │
│                         │                     │                                │
│                         │  Orders issues by:  │                                │
│                         │  • Severity         │                                │
│                         │  • Objective impact │                                │
│                         │  • Constraint risk  │                                │
│                         └──────────┬──────────┘                                │
│                                    │                                           │
│                                    ▼                                           │
│                    ┌───────────────────────────────┐                           │
│                    │  Any blockers or majors?      │                           │
│                    └───────────────┬───────────────┘                           │
│                                    │                                           │
│                     ┌──────────────┴──────────────┐                            │
│                     │                             │                            │
│                    yes                            no                           │
│                     │                             │                            │
│                     ▼                             │                            │
│           ┌─────────────────────┐                 │                            │
│           │      REVISER        │                 │                            │
│           │                     │                 │                            │
│           │ Receives:           │                 │                            │
│           │ • Current draft     │                 │                            │
│           │ • Prioritized issues│                 │                            │
│           │ • Library context   │                 │                            │
│           │   (for fixes)       │                 │                            │
│           │                     │                 │                            │
│           │ Produces:           │                 │                            │
│           │ • Revised draft     │                 │                            │
│           │ • Issues addressed  │                 │                            │
│           │ • Rationale         │                 │                            │
│           └──────────┬──────────┘                 │                            │
│                      │                            │                            │
│                      ▼                            │                            │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║  SOLUTION BLACKBOARD (updated)                                          ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: { version: 2 }                                          ║  │
│   ║  resolved_issues: [ ... + newly resolved ]                              ║  │
│   ║  open_issues: [ remaining ]                                             ║  │
│   ╚═════════════════════════════════════════════════════════════════════════╝  │
│                      │                            │                            │
│                      │     ┌──────────────────────┘                            │
│                      │     │                                                   │
│                      ▼     ▼                                                   │
│           ┌─────────────────────┐                                              │
│           │  TERMINATION CHECK  │                                              │
│           │                     │                                              │
│           │ Stop if:            │                                              │
│           │ • Acceptance met    │                                              │
│           │ • Iteration limit   │                                              │
│           │ • Budget exhausted  │                                              │
│           │ • Plateau detected  │                                              │
│           └──────────┬──────────┘                                              │
│                      │                                                         │
│           ┌──────────┴──────────┐                                              │
│           │                     │                                              │
│         stop               continue                                            │
│           │                     │                                              │
│           ▼                     └─────────► (back to Phase 4 critics           │
│    ┌─────────────┐                           for re-validation)                │
│    │  PHASE 6    │                                                             │
│    └─────────────┘                                                             │
│                                                                                 │
│   ITERATION BOUNDS (from V0 spec):                                             │
│   • Max 2-3 revision loops                                                     │
│   • Budget cap on total LLM calls                                              │
│   • Plateau = improvement < threshold for 2 consecutive iterations             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Output Assembly

**Purpose:** Package the final solution with full provenance, alternatives, and dissent.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: OUTPUT ASSEMBLY                                                        │
│                                                                                 │
│   ╔═════════════════════════════════════════════════════════════════════════╗  │
│   ║  SOLUTION BLACKBOARD (final state)                                      ║  │
│   ║                                                                         ║  │
│   ║  unified_draft: { version: N (final) }                                  ║  │
│   ║  candidates: [ A, B, C, D original solutions ]                          ║  │
│   ║  provenance: { ... }                                                    ║  │
│   ║  resolved_issues: [ ... ]                                               ║  │
│   ║  open_issues: [ remaining minors / accepted risks ]                     ║  │
│   ║  library_coverage: { ... }                                              ║  │
│   ╚═══════════════════════════════╤═════════════════════════════════════════╝  │
│                                   │                                             │
│                                   ▼                                             │
│                        ┌─────────────────────┐                                 │
│                        │     ASSEMBLER       │                                 │
│                        │                     │                                 │
│                        │ Produces all        │                                 │
│                        │ required outputs    │                                 │
│                        │ per Output Spec     │                                 │
│                        └──────────┬──────────┘                                 │
│                                   │                                             │
│                                   ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                        FINAL OUTPUT PACKAGE                             │  │
│   │                                                                         │  │
│   │  REQUIRED DELIVERABLES (per Output Specification):                      │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │ 1. Executive Summary                                              │  │  │
│   │  │ 2. Solution Design Document (with architecture diagram)           │  │  │
│   │  │ 3. Foundation Documentation                                       │  │  │
│   │  │ 4. Constraint Compliance Statement                                │  │  │
│   │  │ 5. Run Log                                                        │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   │                                                                         │  │
│   │  ENHANCED METADATA (from this architecture):                            │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │ 6. Provenance Report                                              │  │  │
│   │  │    • Which elements came from which inventor                      │  │  │
│   │  │    • How conflicts were resolved                                  │  │  │
│   │  │    • Which libraries informed which sections                      │  │  │
│   │  │                                                                   │  │  │
│   │  │ 7. Alternative Approaches (preserved)                             │  │  │
│   │  │    • Candidate A summary + key differentiators                    │  │  │
│   │  │    • Candidate B summary + key differentiators                    │  │  │
│   │  │    • Candidate C summary + key differentiators                    │  │  │
│   │  │    • Candidate D summary + key differentiators                    │  │  │
│   │  │                                                                   │  │  │
│   │  │ 8. Dissenting Views                                               │  │  │
│   │  │    • Ideas from candidates that were NOT adopted                  │  │  │
│   │  │    • Why they were rejected                                       │  │  │
│   │  │    • Conditions under which they might be revisited               │  │  │
│   │  │                                                                   │  │  │
│   │  │ 9. Convergence Report                                             │  │  │
│   │  │    • Where all inventors agreed (high confidence)                 │  │  │
│   │  │    • Where inventors disagreed (uncertainty signal)               │  │  │
│   │  │    • Implications for confidence in final solution                │  │  │
│   │  │                                                                   │  │  │
│   │  │ 10. Library Coverage Report                                       │  │  │
│   │  │    • % of each library embodied in solution                       │  │  │
│   │  │    • Gaps acknowledged                                            │  │  │
│   │  │    • Justification for omissions                                  │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   │                                                                         │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## How Libraries Are Used Across Phases (Summary)

| Phase | How Libraries Are Used |
|-------|------------------------|
| **Phase 0: Intake** | Not used yet; problem classification may reference library metadata |
| **Phase 1: Divergent** | Selectively provided to inventors (none, some, or all per config) |
| **Phase 2: Cross-Poll** | Not directly; inventors critique based on their own lens |
| **Phase 3: Synthesis** | **ALL** libraries provided to synthesizer for full context |
| **Phase 4: Critique** | Each library becomes a dedicated critic lens |
| **Phase 5: Refinement** | Available to reviser for fixing issues |
| **Phase 6: Assembly** | Referenced in coverage report |

**Key insight:** Libraries serve different purposes at different stages:
- **Selective context** during divergent generation (to create diversity)
- **Full context** during synthesis (to make best decisions)
- **Systematic validation** during critique (to ensure coverage)

---

## Decision Points for Configuration

When running this system, you choose:

| Decision | Options | Tradeoff |
|----------|---------|----------|
| **Number of inventors** | 4 (core) to 10+ | Cost vs. coverage |
| **Library distribution** | As described vs. custom | Depends on problem type |
| **Model diversity** | Single model vs. multiple | Cost vs. perspective diversity |
| **Phase 2 inclusion** | Yes / No | Depth of conflict understanding vs. latency |
| **Iteration budget** | 1-3 revision loops | Polish vs. cost |
| **Termination criteria** | Strict vs. relaxed | Quality floor vs. completion guarantee |

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│    INPUTS                                                                       │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ Problem Statement, Objectives, Constraints, Output Spec,               │  │
│    │ Evaluation Criteria, ALL Reference Libraries                           │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 0: Intake & Normalize                                            │  │
│    │ → Problem Brief (shared)                                               │  │
│    │ → Problem Classification                                               │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 1: Divergent Generation (Parallel)                               │  │
│    │                                                                        │  │
│    │   [Inventor A]  [Inventor B]  [Inventor C]  [Inventor D]  [...]        │  │
│    │   (principles)  (secrets)     (all libs)    (no libs)                  │  │
│    │        │             │             │             │                     │  │
│    │        ▼             ▼             ▼             ▼                     │  │
│    │   [Solution A] [Solution B] [Solution C] [Solution D]                  │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 2: Cross-Pollination (Optional)                                  │  │
│    │                                                                        │  │
│    │   Inventors critique each other's solutions                            │  │
│    │   → Cross-Critique Matrix                                              │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 3: Convergent Synthesis                                          │  │
│    │                                                                        │  │
│    │   All candidates + ALL libraries → Synthesizer → Unified Draft v1     │  │
│    │   ══════════════════════════════════════════════════════════════════   │  │
│    │   ║                   SOLUTION BLACKBOARD                          ║   │  │
│    │   ══════════════════════════════════════════════════════════════════   │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 4: Library-Informed Critique                                     │  │
│    │                                                                        │  │
│    │   [FP Critic] [Secrets Critic] [MM Critic] [Tech Critic] [...]         │  │
│    │        │            │              │            │                      │  │
│    │        └────────────┴──────────────┴────────────┘                      │  │
│    │                          │                                             │  │
│    │                          ▼                                             │  │
│    │                   Critique Findings + Open Issues                      │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 5: Iterative Refinement                                          │  │
│    │                                                                        │  │
│    │   ┌─────────────────────────────────────────────────────────────────┐  │  │
│    │   │                                                                 │  │  │
│    │   │   Blockers/Majors? ──yes──► Reviser ──► Updated Draft ──┐      │  │  │
│    │   │         │                                               │      │  │  │
│    │   │         no                                              │      │  │  │
│    │   │         │                           (back to Phase 4) ◄─┘      │  │  │
│    │   │         ▼                                                      │  │  │
│    │   │   Termination Check                                            │  │  │
│    │   │                                                                 │  │  │
│    │   └─────────────────────────────────────────────────────────────────┘  │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │ PHASE 6: Output Assembly                                               │  │
│    │                                                                        │  │
│    │   → Required Deliverables (per Output Spec)                            │  │
│    │   → Provenance Report                                                  │  │
│    │   → Alternative Approaches                                             │  │
│    │   → Dissenting Views                                                   │  │
│    │   → Convergence Report                                                 │  │
│    │   → Library Coverage Report                                            │  │
│    └───────────────────────────────┬────────────────────────────────────────┘  │
│                                    │                                            │
│                                    ▼                                            │
│    ┌────────────────────────────────────────────────────────────────────────┐  │
│    │                        FINAL OUTPUT PACKAGE                            │  │
│    └────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary: How This Maximizes Solution Quality

| Mechanism | What It Prevents | What It Enables |
|-----------|------------------|-----------------|
| **Parallel inventors** | Single-framing anchor bias | Broad solution space exploration |
| **Context variation** | Uniform blind spots | Diverse perspectives |
| **Tabula rasa inventor** | Universal anchoring to libraries | Pure reasoning sanity check |
| **Cross-pollination** | Hidden disagreements | Explicit conflict surfacing |
| **Blackboard synthesis** | Picking winner vs. combining best | True integration of strengths |
| **Library-informed critics** | Missed coverage | Systematic validation |
| **Iterative refinement** | Shipping with known issues | Converging on quality |
| **Provenance tracking** | Black-box output | Full auditability |
| **Preserved alternatives** | Lost optionality | Future revisiting |

This architecture systematically addresses the question: "How do we get the most out of different contexts to get the best solutions?"
