# Evaluation Criteria

---

## Overview

This document defines the criteria, metrics, and rubrics for evaluating candidate solution designs. Its sole purpose is to inform the selection of which solution to build.

Because solutions cannot be tested before selection, all evaluations are necessarily ex-ante: they must be estimated or inferred based on available data, logic, strategic reasoning, insight, judgment, and qualitative assessment. Scores reflect the evaluator's reasoned confidence in how the solution would perform if implemented, not measured outcomes.

---

## Evaluation Framework

### Scoring Structure

Each criterion is scored on a 1–5 scale:

| Score | Meaning |
|-------|---------|
| 5 | High confidence the solution will exceed expectations |
| 4 | High confidence the solution will meet expectations |
| 3 | Reasonable confidence the solution will meet minimum threshold |
| 2 | Significant uncertainty or concerns; may fall short |
| 1 | Low confidence; likely to fail expectations |

### Weighting by Priority

Criteria are weighted according to their priority level:

| Criterion | Objective | Treatment | Weight | Pass Threshold |
|-----------|-----------|-----------|--------|----------------|
| Capital Preservation | 1 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Return Competitiveness | 2 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| First Principles Foundation | 3 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Secrets & Differentiated Innovation | 4 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Focused Mastery | 5 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Adaptability | 6 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Human Cognitive Efficiency | 7 | MUST | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Simplicity | 8 | COULD | 2.0x | No minimum threshold |
| Human Input Capacity | 9 | COULD | 2.0x | No minimum threshold |
| Transparency | 10 | COULD | 2.0x | No minimum threshold |
| Crypto-Native | C3 | SOFT | 1.0x | Relaxation permitted with justification |
| Regulatory Environment | C4 | SOFT | 1.0x | Relaxation permitted with justification |
| Capital Requirements | C5 | SOFT | 1.0x | Relaxation permitted with justification |
| HARD Constraints (C1, C2) | — | HARD | Binary | Pass/Fail; any failure is disqualifying |

**Disqualification Rule**: Any MUST criterion scoring < 3 or any HARD constraint failure disqualifies the solution regardless of total score.

### Assessment Methods

Since solutions cannot be tested, evaluations draw on:

| Method | Description |
|--------|-------------|
| **Design Analysis** | Logical examination of the solution's architecture, mechanisms, and internal consistency |
| **First Principles Reasoning** | Deduction from fundamental truths about how the approach should perform |
| **Analogical Evidence** | Performance of similar approaches, strategies, or mechanisms in comparable contexts |
| **Historical Data** | Backtests, simulations, or historical analysis where applicable (with appropriate skepticism) |
| **Expert Judgment** | Informed qualitative assessment drawing on domain knowledge |
| **Failure Mode Analysis** | Identification of how and why the solution could fail; assessment of likelihood and severity |
| **Comparative Assessment** | How the solution compares to known alternatives on each dimension |

### Method Precedence

When assessment methods produce conflicting signals, apply this precedence:

1. **Failure Mode Analysis and First Principles Reasoning** take precedence for assessing downside risk and structural soundness — they reason forward from how things work, independent of historical conditions
2. **Design Analysis** takes precedence for assessing internal consistency and operational feasibility
3. **Analogical Evidence and Historical Data** are supporting, not primary — they inform confidence but cannot prove future performance; weight them less when they conflict with structural reasoning, and apply appropriate skepticism (survivorship bias, regime dependence, overfitting)
4. **Expert Judgment** serves as tiebreaker when other methods are inconclusive
5. **Comparative Assessment** establishes relative positioning but cannot determine absolute quality

The core principle is: structural reasoning (how the design works and how it fails) outweighs empirical reasoning (what happened historically), because the solution is being evaluated ex-ante and past conditions may not recur.

### Scoring Synthesis

Assessment approach bullets identify the dimensions to evaluate, not a checklist. The score reflects overall judgment across all dimensions, weighted by their relevance to the criterion. A critical failure on any single dimension can cap the score regardless of strength elsewhere — particularly for dimensions that relate to the criterion's pass threshold.

---

## Section 1: Core Pain Point Criteria

*These criteria assess the solution's expected effectiveness against the three irreducible pains from the Problem Statement: loss of capital, forgone returns, and cognitive requirement.*

### 1.1 Capital Preservation (Objective 1: MUST)

**Criterion**: The solution design protects against permanent capital impairment while enabling wealth compounding—preserving capital first, then maximizing returns within that constraint.

| Score | Description |
|-------|-------------|
| 5 | Design structurally prevents unbounded loss; multiple independent safeguards; worst-case scenarios bounded and recoverable; no dependence on favorable conditions to avoid disaster; losses trend toward zero as percentage of total capital |
| 4 | Design addresses major loss vectors; tail risk bounded; concentration and leverage controlled; recovery plausible from worst realistic scenarios |
| 3 | Design acknowledges and addresses primary loss sources; no obvious path to catastrophic loss; basic structural protections present |
| 2 | Some loss scenarios inadequately addressed in design; potential for unrecoverable drawdowns; risk controls incomplete |
| 1 | Design permits unbounded loss scenarios; catastrophic loss structurally possible; inadequate safeguards |

**Assessment Approach**:
- Enumerate loss vectors from Problem Statement §3.1 and assess how design addresses each
- Identify failure modes that could cause permanent impairment
- Evaluate whether poor outcomes are bounded by design or dependent on execution/luck
- Consider analogous strategies' historical drawdown characteristics
- Apply inversion: what would have to go wrong for catastrophic loss to occur?
- Verify no single position or event is capable of causing permanent impairment

---

### 1.2 Return Competitiveness (Objective 2: MUST)

**Criterion**: The solution design minimizes expected forgone returns—reducing underperformance relative to the maximum return achievable within the solution's defined opportunity set.

| Score | Description |
|-------|-------------|
| 5 | Design systematically addresses all major sources of forgone returns; clear logical argument for why selection, timing, sizing, and execution gaps narrow over time; benchmark defined relative to constrained opportunity set; structural advantages compound |
| 4 | Design addresses major sources of forgone returns; logical case for convergence on available returns is sound; minor gaps may persist |
| 3 | Design avoids systematic value destruction; reasonable argument that approach captures fair share of available returns; no obvious inefficiencies |
| 2 | Design likely leaves material value on table; logical case for return capture incomplete; significant inefficiencies unaddressed |
| 1 | Design structurally disadvantaged; no credible argument for competitive returns; obvious improvements available |

**Assessment Approach**:
- Enumerate forgone return sources from Problem Statement §3.3 and assess how design addresses each
- Evaluate the logical argument: why should this approach converge on minimizing forgone returns over time?
- Assess selection logic: how does the design identify and capture available opportunities within the defined pool?
- Assess timing logic: how does the design avoid systematic timing errors?
- Assess sizing logic: how does the design allocate appropriately to opportunities?
- Evaluate friction: fees, costs, drag—are these minimized by design?
- Verify benchmark is defined relative to current opportunity set, not hypothetical omniscience
- Consider: as the opportunity set expands with demonstrated mastery, how do benchmark comparisons adjust?

---

### 1.3 Human Cognitive Efficiency (Objective 7: MUST)

**Criterion**: The solution design demands minimal ongoing human time, attention, effort, and emotional energy—sustainable indefinitely.

| Score | Description |
|-------|-------------|
| 5 | Design requires < 1 hour/week human involvement; decisions rare and bounded; no urgent actions demanded by market movements; emotional exposure minimized; sustainable indefinitely |
| 4 | Design requires 1–5 hours/week human involvement; decisions infrequent; monitoring light; emotional load manageable; long-term sustainable |
| 3 | Design requires 5–10 hours/week human involvement; some active management needed; emotional load moderate; sustainable with discipline |
| 2 | Design requires 10–20 hours/week human involvement; frequent decisions or monitoring; material emotional exposure; sustainability questionable |
| 1 | Design requires > 20 hours/week human involvement or constant vigilance; high decision load; significant emotional burden; unsustainable |

**Scoring Note**: Score based on steady-state operation, not initial setup or learning period. The assessment approach should separately note setup burden, but it does not determine the score.

**Assessment Approach**:
- Map required human activities and estimate time for each
- Count human decision points and assess complexity of each
- Evaluate monitoring requirements and urgency of human responses needed
- Assess emotional exposure (volatility visibility, loss salience, uncertainty tolerance required)
- Verify process does not require constant vigilance or sacrifice of life outside investing
- Consider: could a human maintain this for 10+ years without burnout?

---

## Section 2: Foundation Criteria

*These criteria assess the intellectual and structural foundations of the solution design.*

### 2.1 First Principles Foundation (Objective 3: MUST)

**Criterion**: The solution design is built from fundamental truths that remain stable over time—ensuring durability, robustness, and bottoms-up coherence.

| Score | Description |
|-------|-------------|
| 5 | Every major design decision traces to an identified first principle or combination thereof; no dependence on temporary market conditions, specific technologies, or tactics that may change; logic robust in time and remains valid as surface-level conditions evolve |
| 4 | Core design grounded in first principles; limited tactical elements that are isolated and replaceable; most logic durable |
| 3 | Primary logic grounded in durable truths; some condition-dependent elements but not load-bearing |
| 2 | First principles present but inconsistently applied; material dependence on current conditions |
| 1 | Design primarily tactical; built on assumptions that may not persist; fragile to environmental change |

**Assessment Approach**:
- Require explicit first principles inventory from solution proposal
- Verify each major design decision maps to one or more principles
- Identify assumptions—which are durable vs. condition-dependent?
- Stress test: what market/technology/regulatory changes would invalidate the approach?
- Assess: will this logic still make sense in 10 years?
- Verify solution does not depend on temporary market conditions

---

### 2.2 Secrets & Differentiated Innovation (Objective 4: MUST)

**Criterion**: The solution design embeds non-obvious truths (secrets)—beliefs that most market participants would dismiss or dispute—as the foundation for creating a "Zero to One" innovation that is structurally distinct and hard to replicate.

| Score | Description |
|-------|-------------|
| 5 | Multiple identified secrets with clear logic; each secret would be dismissed or disputed by most participants; approach differs substantially from conventional wisdom; creates genuinely new value (Zero to One) rather than incremental improvement; delivers performance meaningfully and demonstrably superior to existing approaches across the dimensions that matter most; explicit mechanism for recognizing eroded secrets and discovering new ones |
| 4 | At least one significant, well-articulated secret that requires conviction to act upon; meaningful differentiation; defensible structural advantages; some adaptability as secrets erode |
| 3 | Identifiable edge or non-consensus insight present; differentiation exists but may be narrow; occupies distinct position rather than competing head-on |
| 2 | Differentiation claimed but secrets not clearly articulated or defended; approach similar to existing alternatives; competes primarily on execution |
| 1 | No apparent secrets; replicates conventional wisdom; competes on execution alone; easily replicated |

**Assessment Approach**:
- Require explicit secrets inventory from solution proposal, including source (provided, discovered, or developed)
- For each claimed secret: Is it true? Is it non-obvious? Would most participants dismiss or dispute it? Is it not yet widely acted upon?
- Assess defensibility: why won't this be arbitraged away quickly?
- Evaluate secret refresh mechanism: how will the solution recognize when existing secrets have lost their value? How will new secrets be discovered?
- Assess innovation quality: does this create genuinely new value or incremental improvement?
- Consider: what does this approach believe that most participants do not?

---

### 2.3 Focused Mastery (Objective 5: MUST)

**Criterion**: The solution design starts with a narrow, well-defined domain and achieves mastery before expanding scope—depth before breadth.

| Score | Description |
|-------|-------------|
| 5 | Initial scope deliberately bounded and small enough to master fully; clear criteria for what constitutes mastery; expansion only after demonstrating consistent performance; dominates chosen domain rather than competing marginally across many; complexity and breadth grow only as competence justifies |
| 4 | Well-defined initial domain; reasonable path to mastery; expansion criteria specified; depth prioritized over breadth |
| 3 | Initial scope bounded; some path to mastery evident; expansion considerations present but less rigorous |
| 2 | Scope too broad for initial mastery; expansion driven by ambition rather than demonstrated competence; breadth prioritized prematurely |
| 1 | No focus; attempts to cover wide domain from start; no mastery criteria; diffuse effort across many areas |

**Assessment Approach**:
- Assess whether initial scope is deliberately constrained and achievable
- Evaluate mastery criteria: how will the solution know when it has "won" the initial domain?
- Verify expansion is evidence-driven (by demonstrated performance) rather than ambition-driven
- Consider: is the solution extracting available value from current domain before expanding?
- Assess: at each stage, does the solution dominate its chosen domain?

---

### 2.4 Adaptability (Objective 6: MUST)

**Criterion**: The solution design improves and adapts over time—getting better as experience accumulates, remaining effective as conditions change, and allowing revision without starting over.

| Score | Description |
|-------|-------------|
| 5 | Explicit learning mechanisms; solution itself and returns improve over successive periods through observation, learning, self-critique, and validation/invalidation; incremental updates achievable without full redesign; assumptions explicit and updateable; regime-shift resilience built in |
| 4 | Clear path for incorporating lessons; most changes achievable without full redesign; adaptable to moderate shifts; learning loops present |
| 3 | Can incorporate major lessons; material changes possible but with friction; some regime sensitivity |
| 2 | Limited adaptability; changes require substantial rework; regime shifts pose significant risk |
| 1 | Static design; no adaptation mechanism; high obsolescence risk |

**Assessment Approach**:
- Assess whether changes can be made incrementally or require full redesign
- Identify explicit vs. implicit assumptions; assess updateability
- Consider regime change scenarios: how would design fare in sustained bear market, regulatory shift, technology change?
- Assess learning loops: how would successes and failures be captured and applied?
- Evaluate evolution capability: how does the solution get better over time?
- Consider: what's the cost to change X if we learn X was wrong?

---

## Section 3: Design Quality Criteria

*These criteria assess preferred design qualities that enhance the solution but are not strictly required.*

### 3.1 Simplicity (Objective 8: COULD)

**Criterion**: When multiple approaches achieve equivalent outcomes, the solution design chooses the simpler one—fewer moving parts, with complexity justified only when it enables outcomes simpler approaches cannot achieve.

| Score | Description |
|-------|-------------|
| 5 | Minimal moving parts; straightforward logic; elegantly simple; complexity absent or clearly justified by enabling superior outcomes |
| 4 | Simple overall; complexity present only where clearly necessary and justified |
| 3 | Moderate complexity; most components justified |
| 2 | Materially complex; some unnecessary elements |
| 1 | Overly complex; unnecessary moving parts; complexity not justified by outcomes |

**Assessment Approach**:
- Count components, dependencies, decision points
- For each complex element: is it necessary? Could simpler alternative achieve same outcome?
- Test explainability: can the approach be explained clearly in 5 minutes?
- Verify complexity justifies itself by enabling outcomes simpler approaches cannot achieve

---

### 3.2 Human Input Capacity (Objective 9: COULD)

**Criterion**: The solution design can incorporate human suggestions and feedback to improve performance—combining the best of what machines and humans contribute.

| Score | Description |
|-------|-------------|
| 5 | Explicit mechanisms for human input; easy incorporation; improvements retained; solution not impervious to external guidance; gets best performance by combining machine and human strengths |
| 4 | Human input possible in most areas; defined process for incorporation |
| 3 | Human input possible in key areas; some friction |
| 2 | Limited input capacity; incorporation difficult |
| 1 | Closed system; human input not supported; impervious to external guidance |

**Assessment Approach**:
- Identify input points: where can humans inject insights, observations, and corrections?
- Assess incorporation process: how are inputs integrated?
- Evaluate retention: are improvements from input durable?
- Consider: does the solution leverage human strengths appropriately?

---

### 3.3 Transparency (Objective 10: COULD)

**Criterion**: The solution design makes current state, performance, and evolutions visible, verifiable, and tracked—confidence earned through evidence rather than required as blind faith.

| Score | Description |
|-------|-------------|
| 5 | Full visibility; logic fully explainable; all elements verifiable; no trust required without possibility of verification |
| 4 | High visibility; most logic explainable; key elements verifiable |
| 3 | Adequate visibility; core logic explainable |
| 2 | Limited visibility; some black-box elements |
| 1 | Opaque; unexplainable; trust required without verification |

**Assessment Approach**:
- Assess what information would be visible to the operator
- Evaluate explainability of decision logic
- Identify any elements requiring trust without verification
- Verify current state, performance, and evolutions are tracked

---

## Section 4: Constraint Compliance

### 4.1 Team Scale (Constraint 1: HARD)

**Criterion**: The solution must be implementable by a startup of 5–10 people significantly augmented by AI.

| Assessment | Description |
|------------|-------------|
| PASS | Design executable by small, AI-augmented team; no institutional-scale requirements; does not require large headcount or capabilities only available to established financial institutions |
| FAIL | Design requires capabilities, headcount, or resources unavailable to small team |

**Assessment Approach**:
- Inventory required capabilities (skills, systems, relationships)
- Identify which can be AI-augmented vs. require human expertise
- Assess: could a well-chosen team of 5–10 actually build and operate this?

---

### 4.2 Digital and Remote (Constraint 2: HARD)

**Criterion**: The solution must be a digital solution that can be built remotely.

| Assessment | Description |
|------------|-------------|
| PASS | Solution is fully digital; can be built and operated by a remote team; no physical infrastructure, in-person presence, or location-dependent components required |
| FAIL | Solution requires physical infrastructure, in-person operations, or location-dependent components that prevent remote implementation |

**Assessment Approach**:
- Verify all components are digital / software-based
- Confirm the solution can be built and operated by a distributed remote team
- Flag any dependencies on physical presence or location-specific infrastructure

---

### 4.3 Crypto-Native (Constraint 3: SOFT)

**Criterion**: The solution should be built on or around crypto/blockchain infrastructure and markets.

| Score | Description |
|-------|-------------|
| 5 | Fully crypto-native; leverages unique crypto properties (24/7 operation, programmability, transparency, global access, reduced intermediary dependence) |
| 4 | Primarily crypto-native; non-crypto elements limited and justified |
| 3 | Substantially crypto-focused; material non-crypto components |
| 2 | Hybrid approach; significant traditional elements |
| 1 | Primarily non-crypto |

**Relaxation Justification**: If score < 3, document why and what crypto advantages are sacrificed.

---

### 4.4 Regulatory Environment (Constraint 4: SOFT)

**Criterion**: The solution should prefer less regulated markets where a broader range of activities are permitted.

| Score | Description |
|-------|-------------|
| 5 | Operates in unregulated/lightly regulated venues; no licensing required; strategies permissible that would be prohibited in traditional finance |
| 4 | Primarily less regulated; limited regulated exposure |
| 3 | Mixed regulatory exposure; core approach unaffected |
| 2 | Material regulatory exposure; some constraints on solution space |
| 1 | Heavily regulated; significant licensing requirements |

**Relaxation Justification**: If score < 3, document why and what solution space is sacrificed.

---

### 4.5 Capital Requirements (Constraint 5: SOFT)

**Criterion**: The solution should be achievable with moderate starting capital ($10,000–$1,000,000).

| Score | Description |
|-------|-------------|
| 5 | Fully functional at $10,000; scales smoothly |
| 4 | Functional at $25,000; full functionality by $100,000 |
| 3 | Functional at $100,000; some features require higher capital |
| 2 | Requires $250,000+ for basic functionality |
| 1 | Requires $1,000,000+ minimum |

**Relaxation Justification**: If score < 3, document why and how lower-capital participants might phase in.

---

## Section 5: Composite Scoring

### Score Calculation

1. **Score each criterion** 1–5 based on reasoned assessment
2. **Apply weights** per the weighting table above
3. **Check HARD constraints**: Pass/Fail (failure is disqualifying)
4. **Check disqualification thresholds**: Verify minimum scores are met per weighting table (all MUST criteria require ≥ 3)
5. **Sum weighted scores** for total; divide by the maximum possible weighted score for percentage. The maximum is the sum of (max score × weight) across all scored criteria: (7 MUST × 5 × 5.0) + (3 COULD × 5 × 2.0) + (3 SOFT × 5 × 1.0) = 175 + 30 + 15 = 220

### Score Summary Template

| Section | Criterion | Objective | Score | Weight | Weighted |
|---------|-----------|-----------|-------|--------|----------|
| 1.1 | Capital Preservation | 1 (MUST) | /5 | 5.0x | /25 |
| 1.2 | Return Competitiveness | 2 (MUST) | /5 | 5.0x | /25 |
| 1.3 | Human Cognitive Efficiency | 7 (MUST) | /5 | 5.0x | /25 |
| 2.1 | First Principles Foundation | 3 (MUST) | /5 | 5.0x | /25 |
| 2.2 | Secrets & Differentiated Innovation | 4 (MUST) | /5 | 5.0x | /25 |
| 2.3 | Focused Mastery | 5 (MUST) | /5 | 5.0x | /25 |
| 2.4 | Adaptability | 6 (MUST) | /5 | 5.0x | /25 |
| 3.1 | Simplicity | 8 (COULD) | /5 | 2.0x | /10 |
| 3.2 | Human Input Capacity | 9 (COULD) | /5 | 2.0x | /10 |
| 3.3 | Transparency | 10 (COULD) | /5 | 2.0x | /10 |
| 4.3 | Crypto-Native | C3 (SOFT) | /5 | 1.0x | /5 |
| 4.4 | Regulatory Environment | C4 (SOFT) | /5 | 1.0x | /5 |
| 4.5 | Capital Requirements | C5 (SOFT) | /5 | 1.0x | /5 |
| | **TOTAL** | | | | **/220** |

### Constraint Compliance

| Constraint | Treatment | Status | Notes |
|------------|-----------|--------|-------|
| 4.1 Team Scale | HARD | ☐ PASS / ☐ FAIL | |
| 4.2 Digital and Remote | HARD | ☐ PASS / ☐ FAIL | |

### Interpretation Guide

| Total Score | Interpretation |
|-------------|----------------|
| 187–220 (85–100%) | Exceptional candidate; high confidence |
| 154–186 (70–85%) | Strong candidate; good confidence |
| 121–153 (55–70%) | Adequate candidate; moderate confidence |
| 88–120 (40–55%) | Weak candidate; significant concerns |
| < 88 (< 40%) | Poor candidate; unlikely to succeed |

**Note**: Solutions that pass disqualification (all MUST criteria ≥ 3, all HARD constraints pass) will score ≥ 52% due to MUST minimum thresholds. Scores below this indicate a disqualified solution.

---

# End of document.
