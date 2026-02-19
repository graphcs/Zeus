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

Criteria are weighted according to their strategic importance:

| Criterion | Weight | Pass Threshold |
|-----------|--------|----------------|
| Capital Preservation | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Return Competitiveness | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| First Principles Foundation | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Secrets Integration | 5.0x | Score ≥ 3 required; < 3 is disqualifying |
| Innovation | 5.0x | Score ≥ 2 required |
| Simplicity | 3.0x | No minimum threshold |
| Durability | 3.0x | No minimum threshold |
| Human Cognitive Efficiency | 3.0x | Score ≥ 3 required; < 3 is disqualifying |
| Adaptability | 3.0x | Score ≥ 3 required; < 3 is disqualifying |
| Human Input Capacity | 1.0x | No minimum threshold |
| Transparency | 1.0x | No minimum threshold |
| Crypto-Native | 1.0x | Relaxation permitted with justification |
| Regulatory Environment | 1.0x | Relaxation permitted with justification |
| Capital Requirements | 1.0x | Relaxation permitted with justification |
| HARD Constraints | Binary | Pass/Fail; any failure is disqualifying |

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

---

## Section 1: Core Pain Point Criteria

*These criteria assess the solution's expected effectiveness against the three irreducible pains from the Problem Statement: loss of capital, forgone returns, and human cognitive burden.*

### 1.1 Capital Preservation (Objective 1: MUST)

**Criterion**: The solution design protects against permanent capital impairment while enabling wealth compounding.

| Score | Description |
|-------|-------------|
| 5 | Design structurally prevents unbounded loss; multiple independent safeguards; worst-case scenarios bounded and recoverable; no dependence on favorable conditions to avoid disaster |
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

---

### 1.2 Return Competitiveness (Objective 2: MUST)

**Criterion**: The solution design minimizes expected forgone returns through sound logic and structural advantages.

| Score | Description |
|-------|-------------|
| 5 | Design systematically addresses all major sources of forgone returns; clear logical argument for why selection, timing, sizing, and friction gaps narrow over time; structural advantages compound |
| 4 | Design addresses major sources of forgone returns; logical case for convergence on available returns is sound; minor gaps may persist |
| 3 | Design avoids systematic value destruction; reasonable argument that approach captures fair share of available returns; no obvious inefficiencies |
| 2 | Design likely leaves material value on table; logical case for return capture incomplete; significant inefficiencies unaddressed |
| 1 | Design structurally disadvantaged; no credible argument for competitive returns; obvious improvements available |

**Assessment Approach**:
- Enumerate forgone return sources from Problem Statement §3.3 and assess how design addresses each
- Evaluate the logical argument: why should this approach converge on minimizing forgone returns over time?
- Assess selection logic: how does the design identify and capture available opportunities?
- Assess timing logic: how does the design avoid systematic timing errors?
- Assess sizing logic: how does the design allocate appropriately to opportunities?
- Evaluate friction: fees, costs, drag—are these minimized by design?
- Consider: is there a coherent theory for why this approach should not systematically underperform alternatives?

---

### 1.3 Human Cognitive Efficiency (Objective 6: MUST)

**Criterion**: The solution design demands minimal ongoing human time, attention, effort, and emotional energy.

| Score | Description |
|-------|-------------|
| 5 | Design requires < 1 hour/week human involvement; decisions rare and bounded; emotional exposure minimized; sustainable indefinitely |
| 4 | Design requires 1–5 hours/week human involvement; decisions infrequent; monitoring light; emotional load manageable; long-term sustainable |
| 3 | Design requires 5–10 hours/week human involvement; some active management needed; emotional load moderate; sustainable with discipline |
| 2 | Design requires 10–20 hours/week human involvement; frequent decisions or monitoring; material emotional exposure; sustainability questionable |
| 1 | Design requires > 20 hours/week human involvement or constant vigilance; high decision load; significant emotional burden; unsustainable |

**Assessment Approach**:
- Map required human activities and estimate time for each
- Count human decision points and assess complexity of each
- Evaluate monitoring requirements and urgency of human responses needed
- Assess emotional exposure (volatility visibility, loss salience, uncertainty tolerance required)
- Consider: could a human maintain this for 10+ years without burnout?

---

## Section 2: Foundation Criteria

*These criteria assess the intellectual and structural foundations of the solution design.*

### 2.1 First Principles Foundation (Objective 3: MUST)

**Criterion**: The solution design is built from fundamental truths that remain stable over time.

| Score | Description |
|-------|-------------|
| 5 | Every major design decision traces to an identified first principle; no dependence on temporary conditions; logic remains valid under regime change |
| 4 | Core design grounded in first principles; limited tactical elements that are isolated and replaceable |
| 3 | Primary logic grounded in durable truths; some condition-dependent elements but not load-bearing |
| 2 | First principles present but inconsistently applied; material dependence on current conditions |
| 1 | Design primarily tactical; built on assumptions that may not persist; fragile to environmental change |

**Assessment Approach**:
- Require explicit first principles inventory from solution proposal
- Verify each major design decision maps to a principle
- Identify assumptions—which are durable vs. condition-dependent?
- Stress test: what market/technology/regulatory changes would invalidate the approach?
- Assess: will this logic still make sense in 10 years?

---

### 2.2 Secrets Integration (Objective 4: MUST)

**Criterion**: The solution design embeds non-obvious truths that provide structural advantage.

| Score | Description |
|-------|-------------|
| 5 | Multiple identified secrets with clear logic; approach differs substantially from conventional wisdom; differentiation defensible; mechanism for secret refresh included |
| 4 | At least one significant, well-articulated secret; meaningful differentiation; some adaptability as secrets erode |
| 3 | Identifiable edge or non-consensus insight present; differentiation exists but may be narrow |
| 2 | Differentiation claimed but secrets not clearly articulated or defended; approach similar to existing alternatives |
| 1 | No apparent secrets; replicates conventional wisdom; competes on execution alone |

**Assessment Approach**:
- Require explicit secrets inventory from solution proposal
- For each claimed secret: Is it true? Is it non-obvious? Is it not yet widely acted upon?
- Assess defensibility: why won't this be arbitraged away quickly?
- Evaluate secret refresh mechanism: how will new secrets be discovered?
- Consider: what does this approach believe that most participants do not?

---

### 2.3 Adaptability (Objective 5: MUST)

**Criterion**: The solution design can improve over time and remain effective as conditions change.

| Score | Description |
|-------|-------------|
| 5 | Explicit learning mechanisms; incremental updates achievable without full redesign; assumptions explicit and updateable; regime-shift resilience built in |
| 4 | Clear path for incorporating lessons; most changes achievable without full redesign; adaptable to moderate shifts |
| 3 | Can incorporate major lessons; material changes possible but with friction; some regime sensitivity |
| 2 | Limited adaptability; changes require substantial rework; regime shifts pose significant risk |
| 1 | Static design; no adaptation mechanism; high obsolescence risk |

**Assessment Approach**:
- Assess whether changes can be made incrementally or require full redesign
- Identify explicit vs. implicit assumptions; assess updateability
- Consider regime change scenarios: how would design fare in sustained bear market, regulatory shift, technology change?
- Assess learning loops: how would successes and failures be captured and applied?
- Consider: what's the cost to change X if we learn X was wrong?

---

## Section 3: Design Quality Criteria

### 3.1 Innovation and Differentiation (Objective 7: SHOULD)

**Criterion**: The solution design is structurally distinct from existing approaches.

| Score | Description |
|-------|-------------|
| 5 | Novel approach; no direct competitors; innovation enables capabilities unavailable elsewhere |
| 4 | Significant differentiation; occupies distinct position; innovation in key areas |
| 3 | Meaningful differentiation in some dimensions; not head-on competition with established approaches |
| 2 | Limited differentiation; competes primarily on execution within established category |
| 1 | Replicates existing approach; differentiation minimal |

**Assessment Approach**:
- Map competitive landscape: what existing approaches does this resemble?
- Identify specific differentiators and assess their significance
- Evaluate: does innovation create real advantage or is it novelty for its own sake?

---

### 3.2 Simplicity (Objective 8: COULD)

**Criterion**: The solution design minimizes complexity while achieving required outcomes.

| Score | Description |
|-------|-------------|
| 5 | Minimal moving parts; straightforward logic; elegantly simple |
| 4 | Simple overall; complexity present only where clearly necessary |
| 3 | Moderate complexity; most components justified |
| 2 | Materially complex; some unnecessary elements |
| 1 | Overly complex; unnecessary moving parts |

**Assessment Approach**:
- Count components, dependencies, decision points
- For each complex element: is it necessary? Could simpler alternative achieve same outcome?
- Test explainability: can the approach be explained clearly in 5 minutes?

---

### 3.3 Durability (Objective 9: COULD)

**Criterion**: The solution design favors proven approaches over novel/unproven ones.

| Score | Description |
|-------|-------------|
| 5 | Built on proven, stable foundations; all dependencies have track records |
| 4 | Most components proven; novel elements limited and low-risk |
| 3 | Mix of proven and novel; novel elements solve real problems |
| 2 | Material reliance on unproven approaches; stability uncertain |
| 1 | Heavily experimental; high obsolescence risk |

**Assessment Approach**:
- Inventory dependencies (technologies, platforms, protocols, instruments)
- Assess maturity and stability of each
- Identify single points of failure or abandonment risk

---

### 3.4 Human Input Capacity (Objective 10: COULD)

**Criterion**: The solution design can incorporate human insights and corrections.

| Score | Description |
|-------|-------------|
| 5 | Explicit mechanisms for human input; easy incorporation; improvements retained |
| 4 | Human input possible in most areas; defined process |
| 3 | Human input possible in key areas; some friction |
| 2 | Limited input capacity; incorporation difficult |
| 1 | Closed system; human input not supported |

**Assessment Approach**:
- Identify input points: where can humans inject insights?
- Assess incorporation process: how are inputs integrated?
- Evaluate retention: are improvements from input durable?

---

### 3.5 Transparency (Objective 11: COULD)

**Criterion**: The solution design makes state, performance, and logic visible and verifiable.

| Score | Description |
|-------|-------------|
| 5 | Full visibility; logic fully explainable; all elements verifiable |
| 4 | High visibility; most logic explainable; key elements verifiable |
| 3 | Adequate visibility; core logic explainable |
| 2 | Limited visibility; some black-box elements |
| 1 | Opaque; unexplainable; trust required without verification |

**Assessment Approach**:
- Assess what information would be visible to the operator
- Evaluate explainability of decision logic
- Identify any elements requiring trust without verification

---

## Section 4: Constraint Compliance

### 4.1 Team Scale (Constraint 1: HARD)

**Criterion**: The solution must be implementable by a startup of 5–10 people significantly augmented by AI.

| Assessment | Description |
|------------|-------------|
| PASS | Design executable by small, AI-augmented team; no institutional-scale requirements |
| FAIL | Design requires capabilities, headcount, or resources unavailable to small team |

**Assessment Approach**:
- Inventory required capabilities (skills, systems, relationships)
- Identify which can be AI-augmented vs. require human expertise
- Assess: could a well-chosen team of 5–10 actually build and operate this?

---

### 4.2 Public Information and Instruments (Constraint 2: HARD)

**Criterion**: The solution must use only publicly accessible information and instruments.

| Assessment | Description |
|------------|-------------|
| PASS | All information sources publicly accessible (including paid APIs); all instruments publicly tradeable |
| FAIL | Depends on non-public information, privileged access, or unavailable instruments |

**Assessment Approach**:
- Inventory all information sources; verify public accessibility
- Inventory all instruments; verify public tradeability
- Flag any dependencies on relationships, access, or data that others cannot obtain

---

### 4.3 Crypto-Native (Constraint 3: SOFT)

**Criterion**: The solution should be built on or around crypto/blockchain infrastructure and markets.

| Score | Description |
|-------|-------------|
| 5 | Fully crypto-native; leverages unique crypto properties |
| 4 | Primarily crypto-native; non-crypto elements limited and justified |
| 3 | Substantially crypto-focused; material non-crypto components |
| 2 | Hybrid approach; significant traditional elements |
| 1 | Primarily non-crypto |

**Relaxation Justification**: If score < 3, document why and what crypto advantages are sacrificed.

---

### 4.4 Regulatory Environment (Constraint 4: SOFT)

**Criterion**: The solution should prefer less regulated markets.

| Score | Description |
|-------|-------------|
| 5 | Operates in unregulated/lightly regulated venues; no licensing required |
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
4. **Check disqualification thresholds**: Verify minimum scores are met per weighting table
5. **Sum weighted scores** for total; divide by 210 for percentage

### Score Summary Template

| Section | Criterion | Score | Weight | Weighted |
|---------|-----------|-------|--------|----------|
| 1.1 | Capital Preservation | /5 | 5.0x | /25 |
| 1.2 | Return Competitiveness | /5 | 5.0x | /25 |
| 1.3 | Human Cognitive Efficiency | /5 | 3.0x | /15 |
| 2.1 | First Principles Foundation | /5 | 5.0x | /25 |
| 2.2 | Secrets Integration | /5 | 5.0x | /25 |
| 2.3 | Adaptability | /5 | 3.0x | /15 |
| 3.1 | Innovation | /5 | 5.0x | /25 |
| 3.2 | Simplicity | /5 | 3.0x | /15 |
| 3.3 | Durability | /5 | 3.0x | /15 |
| 3.4 | Human Input | /5 | 1.0x | /5 |
| 3.5 | Transparency | /5 | 1.0x | /5 |
| 4.3 | Crypto-Native | /5 | 1.0x | /5 |
| 4.4 | Regulatory | /5 | 1.0x | /5 |
| 4.5 | Capital Requirements | /5 | 1.0x | /5 |
| | **TOTAL** | | | **/210** |

### Constraint Compliance

| Constraint | Treatment | Status | Notes |
|------------|-----------|--------|-------|
| 4.1 Team Scale | HARD | ☐ PASS / ☐ FAIL | |
| 4.2 Public Information | HARD | ☐ PASS / ☐ FAIL | |

### Interpretation Guide

| Total Score | Interpretation |
|-------------|----------------|
| 180–210 (85–100%) | Exceptional candidate; high confidence |
| 150–179 (70–85%) | Strong candidate; good confidence |
| 115–149 (55–70%) | Adequate candidate; moderate confidence |
| 85–114 (40–55%) | Weak candidate; significant concerns |
| < 85 (< 40%) | Poor candidate; unlikely to succeed |

---

## Appendix: Solution Proposal Requirements

To enable evaluation, solution proposals should include:

**Foundation Documentation**
- [ ] First principles inventory with design decision mapping
- [ ] Secrets inventory with defensibility and refresh assessment
- [ ] Key assumptions inventory (explicit, with durability assessment)

**Design Documentation**
- [ ] Architecture overview
- [ ] Component inventory with complexity justification
- [ ] Dependency inventory with maturity assessment
- [ ] Failure mode analysis

**Pain Point Assessment**
- [ ] Loss vector analysis (how each source of loss from Problem Statement §3.1 is addressed)
- [ ] Forgone return analysis (how each source from Problem Statement §3.3 is addressed)
- [ ] Human cognitive load estimate (time, decisions, monitoring, emotional exposure)

**Constraint Compliance**
- [ ] Resource requirements (team, skills, systems)
- [ ] Information and instrument sources with access verification
- [ ] Capital requirements and scaling characteristics
- [ ] Regulatory exposure assessment
