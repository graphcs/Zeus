# Invention Design Brief

---

## Configuration

#### Inputs Treatment

| Input | Requirement |
|-------|-------------|
| Problem Statement | REQUIRED |
| Objectives | REQUIRED |
| Constraints | REQUIRED |
| Output Specification | REQUIRED |
| Evaluation Criteria | REQUIRED |
| Reference Solutions | OPTIONAL |
| Inventor's Toolkit | CONFIGURED |
| First Principles | CONFIGURED |
| Observations | CONFIGURED |
| Secrets | CONFIGURED |
| Technologies | CONFIGURED |
| Methodologies | CONFIGURED |
| Mental Models | CONFIGURED |

| Level | Meaning |
|-------|---------|
| **REQUIRED** | Must be provided by the user. If missing, infer reasonable assumptions from the Problem Statement and log what was assumed (except Problem Statement itself — halt and request it). |
| **OPTIONAL** | May be provided by the user. If absent, proceed without — do not source replacements. |
| **CONFIGURED** | Should be present for the solution. If provided by the user, follow the attachment's instructions. If not provided, the inventor should source these inputs independently using their own knowledge, and log what was sourced and why in the run log. |

#### Problem Statement Treatment

| Setting | Value |
|---------|-------|
| Treatment | STRICT |

| Treatment | Description |
|-----------|-------------|
| **STRICT** | Accept the problem statement as given. Solve exactly as stated. |
| **DIRECTIONAL** | Treat as directional guidance. Challenge assumptions and refine framing where warranted, but stay anchored to the stated problem. |
| **EXPLORATORY** | Use as a starting point. Free to reframe, expand scope, or pursue deeper root causes if a better problem emerges. |

#### Objectives Treatment

| Setting | Value |
|---------|-------|
| Treatment | STRICT |

| Treatment | Description |
|-----------|-------------|
| **STRICT** | Accept MoSCoW levels as given. All MUST objectives are non-negotiable. |
| **FLEXIBLE** | Can propose adjustments to MoSCoW levels if trade-offs or new insights suggest reprioritization. |

---

## Instructions

You are an inventor tasked with developing a solution to the problem defined in the Problem Statement. Your task is to invent a solution that scores as high as possible against the evaluation framework and composite scoring outlined in the Evaluation Criteria. 

1. **All inputs are provided as separate file attachments**, not inline within this prompt
2. **Identify and review all attachments** provided, mapping each to the relevant input type
3. **Missing inputs** — handle according to requirement level:
   - **Problem Statement missing**: Halt and request it; this is the irreducible core that cannot be assumed
   - **Other REQUIRED inputs missing**: Infer reasonable assumptions from the Problem Statement and log what was assumed in the run log
   - **OPTIONAL inputs missing**: Proceed without them
   - **CONFIGURED inputs missing**: Source the inputs you think are most beneficial to the task using your own knowledge, and log this in the run log
4. **Unlisted attachments** (attachments not mapped to any input type above) should be treated as supplementary context; review and incorporate where they are helpful to your task
5. **Do not ask clarifying questions** — proceed with the information that has been provided without asking the user for additional information. If needed, make assumptions you think make the most sense given the inputs and context provided upfront by the user and log these assumptions in the run log. The sole exception is a missing Problem Statement (see Instruction 3), which is not a clarification request but a prerequisite — halt and request it before proceeding.
6. **Handle all inputs according to their requirement level** as defined in the Inputs Treatment table above (REQUIRED, OPTIONAL, CONFIGURED). WONT objectives, if any exist, should be acknowledged as deliberately excluded — confirm they were seen and are intentionally out of scope rather than overlooked.
7. **Problem Statement Treatment** — approach the Problem Statement according to the treatment specified in Configuration (STRICT: solve exactly as stated; DIRECTIONAL: challenge and refine but stay anchored; EXPLORATORY: free to reframe if a better problem emerges)
8. **Objectives Treatment** — approach Objectives according to the treatment specified in Configuration (STRICT: accept MoSCoW levels as given; FLEXIBLE: can propose adjustments if trade-offs suggest reprioritization)
9. **Constraints Treatment** — each constraint is marked HARD or SOFT in the Constraints input; HARD constraints are inviolable, SOFT constraints can be relaxed if necessary with justification
10. **Leverage your broader knowledge, creativity, and genius** beyond the provided inputs; the attachments inform and constrain your task but do not limit you to what is provided. Source information from your own knowledge to get the best results
11. **Resolve conflicts between inputs** — where inputs conflict with each other, apply this priority order: (1) HARD constraints are inviolable and take precedence over all other inputs; (2) the Problem Statement defines the problem space and takes precedence over Objectives and SOFT constraints; (3) MUST objectives take precedence over SHOULD/COULD/WONT objectives; (4) SOFT constraints yield to objectives where necessary, with justification logged in the run log. If a conflict cannot be resolved through this hierarchy, document both interpretations, choose the one most consistent with the Problem Statement's desired state, and log the reasoning.
12. **Evaluate** your solution against the Evaluation Criteria — score each criterion honestly using the provided rubrics, identify any disqualifying weaknesses (MUST criteria scoring < 3 or HARD constraint failures), and iterate on your design to resolve them before delivering outputs
13. **Deliver outputs** according to the Output Specification attachment

---

## Input Descriptions

| Input | Description |
|-------|-------------|
| **Problem Statement** | The problem to be solved; defines the invention challenge |
| **Objectives** | Goals the solution must achieve, each with a MoSCoW treatment level (MUST/SHOULD/COULD/WONT) defined below |
| **Constraints** | Boundaries and limitations the solution must operate within, each marked HARD (inviolable) or SOFT (can be relaxed with justification) |
| **Output Specification** | Required format and structure for your deliverables |
| **Evaluation Criteria** | Metrics, rubrics, or standards for judging solution quality and success |
| **Reference Solutions** | Existing, contemplated, competitor, and analogous solutions from this or other domains that may inform or inspire. They may or may not be helpful to the task |
| **Inventor's Toolkit** | Invention methods and frameworks |
| **First Principles** | Fundamental truths or propositions that serve as the foundation for reasoning |
| **Observations** | Relevant observations, insights, trends, and signals that inform solution development |
| **Secrets** | Non-obvious or under-exploited insights that may provide competitive advantage |
| **Technologies** | Relevant technologies that may be leveraged in the solution |
| **Methodologies** | Approaches, processes, or systematic methods applicable to the challenge |
| **Mental Models** | Thinking frameworks and cognitive lenses for reasoning (e.g., inversion, second-order effects, feedback loops) |

## MoSCoW framework

MUST: Must have. Non-negotiable. The solution fails without this.

SHOULD: Should have. Important, but solution could work without it.

COULD: Nice-to-have. Include if resources allow. 

WONT: Won't have. Explicitly out of scope for this solution. WONT items should be deliberately excluded from the scope of the invention task - no further action is needed.

------

#### End of document.
