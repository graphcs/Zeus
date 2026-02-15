# Inventors' Toolkit — LLM Reference Document

## Document Purpose
This document is a structured reference for guiding invention and innovation work. Use it to select and apply appropriate methods based on the current situation, problem type, and desired outcome.

## How to Use This Document
1. Identify the current phase of work (problem framing, ideation, evaluation, etc.)
2. Match the situation to relevant method tags
3. Select methods based on triggers and use-when conditions
4. Follow the method structure: ask the specified questions, apply the technique, produce the expected outputs
5. Chain methods as needed — outputs from one method become inputs to another

---

## Method Schema
Each method follows this structure:
- **ID**: Unique identifier
- **Name**: Method name
- **Category**: Primary category
- **Tags**: Searchable attributes for method selection
- **Triggers**: Situations that indicate this method is appropriate
- **Description**: What the method does
- **Process**: Steps to execute
- **Key Questions**: Questions to ask when applying
- **Outputs**: What the method produces
- **Chains With**: Methods that commonly precede or follow

---

## Categories
- PROBLEM_FRAMING: Define the right problem
- IDEATION: Generate solution concepts
- BREAKTHROUGH: Overcome contradictions and fixation
- COGNITIVE: Escape habitual thinking
- EXPLORATION: Test and learn quickly
- EVALUATION: Select and prioritize
- TEAM_PROCESS: Enable sustained innovation
- STRATEGIC: Align with market and business
- HUMAN_CENTERED: Ensure human fit
- EMERGING: Advanced and experimental approaches

---

## Methods

### PROBLEM_FRAMING Methods

#### Method: FIRST_PRINCIPLES
- **ID**: PF-001
- **Category**: PROBLEM_FRAMING
- **Tags**: [fundamentals, assumptions, physics, constraints, rebuild, decomposition]
- **Triggers**: 
  - Existing solutions feel constrained by tradition
  - "That's just how it's done" appears in discussion
  - Industry has converged on similar approaches
- **Description**: Reduce the problem to fundamental truths (physics, economics, human nature), stripping away assumptions, then rebuild solutions from scratch.
- **Process**:
  1. State the current problem and conventional solutions
  2. List all assumptions embedded in current approaches
  3. For each assumption, ask: "Is this a law of nature or a convention?"
  4. Identify the true constraints (physical, legal, economic)
  5. Rebuild possible solutions using only true constraints
- **Key Questions**:
  - What must be true? (Laws of physics, mathematics, human biology)
  - What is assumed but not required?
  - If we were starting from zero today, would we build it this way?
  - What would a solution look like if [assumption] were false?
- **Outputs**: List of true constraints, list of false assumptions, reframed problem statement, unconventional solution directions
- **Chains With**: CONTRADICTION_MAPPING, IDEAL_FINAL_RESULT, CONSTRAINT_SURFACING

---

#### Method: JOBS_TO_BE_DONE
- **ID**: PF-002
- **Category**: PROBLEM_FRAMING
- **Tags**: [user-needs, progress, hiring, switching, outcomes, motivation]
- **Triggers**:
  - Users adopt workarounds
  - Churn is unpredictable
  - Feature additions don't improve satisfaction
  - Competing with non-consumption
- **Description**: Define the job the user is "hiring" a solution to do, focusing on the progress they seek rather than product features.
- **Process**:
  1. Identify the struggling moment — when does the user seek progress?
  2. Define the job in format: "When [situation], I want to [motivation], so I can [outcome]"
  3. Map functional, emotional, and social dimensions of the job
  4. Identify current solutions being "hired" (including non-consumption)
  5. Identify hiring and firing criteria
- **Key Questions**:
  - What progress is the user trying to make?
  - What are they firing when they hire this solution?
  - What functional job must be done?
  - What emotional job must be done? (How do they want to feel?)
  - What social job must be done? (How do they want to be perceived?)
- **Outputs**: Job statement, job dimensions map, competing solutions list, hiring criteria
- **Chains With**: EMPATHY_MAPPING, USER_JOURNEY_MAPPING, DEMAND_SIDE_ANALYSIS

---

#### Method: FIVE_WHYS
- **ID**: PF-003
- **Category**: PROBLEM_FRAMING
- **Tags**: [root-cause, symptoms, recurring, depth, causation]
- **Triggers**:
  - Problem seems vague
  - Problem keeps recurring despite fixes
  - Treating symptoms rather than causes
  - Surface-level understanding
- **Description**: Iteratively ask "why" to move from symptoms to root causes.
- **Process**:
  1. State the problem as observed
  2. Ask "Why does this happen?" — record answer
  3. For the answer, ask "Why?" again
  4. Repeat until reaching a root cause (typically 5 iterations, sometimes more or fewer)
  5. Verify the causal chain by reading it forward
- **Key Questions**:
  - Why does this happen?
  - Is this answer a cause or another symptom?
  - Have we reached something we can act on?
  - Are there multiple branches of causation?
- **Outputs**: Causal chain, root cause identification, actionable intervention points
- **Chains With**: SYSTEMS_MAPPING, CONSTRAINT_SURFACING, STAKEHOLDER_POWER_MAPPING

---

#### Method: SYSTEMS_MAPPING
- **ID**: PF-004
- **Category**: PROBLEM_FRAMING
- **Tags**: [feedback-loops, stakeholders, delays, incentives, second-order, complexity, unintended-consequences]
- **Triggers**:
  - Interventions cause unintended consequences
  - Multiple stakeholders with different incentives
  - Problem involves delays or accumulations
  - Simple solutions have failed
- **Description**: Map the system including stakeholders, feedback loops, delays, and incentives to reveal second-order effects.
- **Process**:
  1. Identify all entities involved (people, organizations, resources)
  2. Map relationships and flows between entities
  3. Identify feedback loops (reinforcing and balancing)
  4. Note delays in the system
  5. Map incentives for each stakeholder
  6. Identify leverage points
- **Key Questions**:
  - Who are all the stakeholders?
  - What does each stakeholder want?
  - Where are the feedback loops?
  - What are the delays between action and effect?
  - Where are the high-leverage intervention points?
- **Outputs**: System diagram, stakeholder-incentive map, feedback loop identification, leverage point ranking
- **Chains With**: STAKEHOLDER_POWER_MAPPING, FIVE_WHYS, ECOSYSTEM_MAPPING

---

#### Method: CONSTRAINT_SURFACING
- **ID**: PF-005
- **Category**: PROBLEM_FRAMING
- **Tags**: [constraints, limitations, hidden, challenge, opportunity, blocking]
- **Triggers**:
  - Team says "we can't because..."
  - Apparent dead ends
  - Constraints assumed but not examined
  - Solution space feels artificially narrow
- **Description**: List explicit and implicit constraints, then challenge each to find hidden opportunities.
- **Process**:
  1. List all stated constraints
  2. List unstated/implicit constraints (regulatory, technical, cultural, resource)
  3. For each constraint, determine: real vs. assumed, permanent vs. temporary
  4. Challenge assumed constraints: What if this weren't true?
  5. Identify constraints that could become opportunities
- **Key Questions**:
  - What constraints are we assuming?
  - Is this constraint real or assumed?
  - Is this constraint permanent or temporary?
  - What would we do if this constraint disappeared?
  - Can this constraint become an advantage?
- **Outputs**: Constraint inventory (categorized as real/assumed, permanent/temporary), challenged assumptions, constraint-as-opportunity list
- **Chains With**: FIRST_PRINCIPLES, ASSUMPTION_REVERSAL, CONTRADICTION_MAPPING

---

#### Method: PROBLEM_REFRAMING
- **ID**: PF-006
- **Category**: PROBLEM_FRAMING
- **Tags**: [perspective, abstraction, reframe, stuck, fixation, category]
- **Triggers**:
  - Team keeps arriving at same unsatisfying solutions
  - Problem feels intractable
  - Single framing dominates discussion
  - Need fresh perspective
- **Description**: Deliberately restate the problem from multiple angles to escape fixation on one framing.
- **Process**:
  1. State the current problem framing
  2. Reframe at higher abstraction: What is the broader goal?
  3. Reframe at lower abstraction: What is the specific pain point?
  4. Reframe by changing subject: Whose problem is this?
  5. Reframe by category: What if this is a [different type] problem?
  6. Select most promising reframing(s) for further work
- **Key Questions**:
  - What if this isn't a [current category] problem at all?
  - Whose problem is this really?
  - What would this problem look like from [other stakeholder]'s view?
  - What's the problem behind the problem?
  - What if we're solving the wrong problem?
- **Outputs**: Multiple problem framings, selected reframing, new solution directions
- **Chains With**: JOBS_TO_BE_DONE, FIVE_WHYS, LATERAL_THINKING

---

#### Method: ETHNOGRAPHIC_OBSERVATION
- **ID**: PF-007
- **Category**: PROBLEM_FRAMING
- **Tags**: [observation, context, behavior, workarounds, unarticulated, field-research]
- **Triggers**:
  - Survey data conflicts with actual behavior
  - Designing for unfamiliar users
  - Need to understand real context of use
  - Users can't articulate their needs
- **Description**: Observe users in their natural context without intervention to discover workarounds, frustrations, and unarticulated needs.
- **Process**:
  1. Define observation objectives
  2. Identify contexts and users to observe
  3. Observe without intervening — take notes on behavior, environment, tools, social dynamics
  4. Note workarounds, frustrations, emotional moments
  5. Debrief and identify patterns
  6. Generate insights about unarticulated needs
- **Key Questions**:
  - What are they actually doing (vs. what they say they do)?
  - What workarounds have they created?
  - What frustrates them that they've accepted as normal?
  - What's in their environment that affects behavior?
  - What surprised us?
- **Outputs**: Observation notes, behavior patterns, workaround inventory, insight statements, unarticulated needs
- **Chains With**: EMPATHY_MAPPING, CONTEXTUAL_INQUIRY, JOBS_TO_BE_DONE

---

#### Method: EXTREME_USER_ANALYSIS
- **ID**: PF-008
- **Category**: PROBLEM_FRAMING
- **Tags**: [margins, power-users, non-users, rejection, latent-needs, edge-cases]
- **Triggers**:
  - Mainstream market seems saturated
  - Looking for latent needs
  - Average users mask important signals
  - Need to find unmet needs
- **Description**: Study users at the margins — power users, non-users, and those who reject the category — to reveal latent needs.
- **Process**:
  1. Identify extreme user segments: heavy users, non-users, rejectors, hackers/modifiers
  2. Recruit and study extreme users
  3. Understand why power users use so intensively
  4. Understand why non-users don't engage
  5. Understand why rejectors actively avoid
  6. Extract insights applicable to mainstream
- **Key Questions**:
  - Why do some people use this 10x more than average?
  - Why do some people refuse to use any solution?
  - What have power users modified or hacked?
  - What would convert a non-user?
  - What needs are extreme users revealing that average users mask?
- **Outputs**: Extreme user profiles, intensity drivers, rejection reasons, latent need hypotheses
- **Chains With**: JOBS_TO_BE_DONE, DEMAND_SIDE_ANALYSIS, DISRUPTIVE_INNOVATION

---

#### Method: DEMAND_SIDE_ANALYSIS
- **ID**: PF-009
- **Category**: PROBLEM_FRAMING
- **Tags**: [adoption, switching-costs, barriers, competing-behaviors, demand, pull]
- **Triggers**:
  - Great solutions exist but adoption is low
  - Need to understand barriers to change
  - Competing with established behaviors
  - Push marketing isn't working
- **Description**: Map the full demand landscape including who wants change, why, and what prevents adoption.
- **Process**:
  1. Identify the push: What's creating dissatisfaction with current state?
  2. Identify the pull: What's attractive about the new solution?
  3. Identify habits: What current behaviors must change?
  4. Identify anxieties: What fears prevent switching?
  5. Map switching costs (financial, learning, social, emotional)
  6. Identify intervention points
- **Key Questions**:
  - What pushes people away from current solutions?
  - What pulls people toward new solutions?
  - What habits anchor current behavior?
  - What anxieties block change?
  - What are the switching costs?
- **Outputs**: Push-pull-habit-anxiety map, switching cost inventory, adoption barrier ranking, intervention opportunities
- **Chains With**: JOBS_TO_BE_DONE, USER_JOURNEY_MAPPING, ADOPTION_CURVE_PLANNING

---

#### Method: STAKEHOLDER_POWER_MAPPING
- **ID**: PF-010
- **Category**: PROBLEM_FRAMING
- **Tags**: [stakeholders, influence, power, interests, buy-in, politics, blockers]
- **Triggers**:
  - Solutions require buy-in from multiple parties
  - Conflicting interests among stakeholders
  - Need to understand who can block or enable
  - Political dynamics affect adoption
- **Description**: Identify all parties affected by the problem and map their relative influence, interests, and positions.
- **Process**:
  1. List all stakeholders affected by problem and potential solutions
  2. Map each stakeholder's interest (what they want)
  3. Map each stakeholder's power/influence
  4. Identify who benefits from status quo vs. change
  5. Identify potential allies and blockers
  6. Plan engagement strategy
- **Key Questions**:
  - Who is affected by this problem?
  - Who has power to enable or block solutions?
  - Who benefits from the status quo?
  - Who would benefit from change?
  - What does each stakeholder need to support the solution?
- **Outputs**: Stakeholder inventory, power-interest matrix, ally/blocker identification, engagement strategy
- **Chains With**: SYSTEMS_MAPPING, ECOSYSTEM_MAPPING, BUSINESS_MODEL_CANVAS

---

### IDEATION Methods

#### Method: STRUCTURED_BRAINSTORMING
- **ID**: ID-001
- **Category**: IDEATION
- **Tags**: [quantity, divergent, group, defer-judgment, volume, generative]
- **Triggers**:
  - Need many ideas quickly
  - Starting ideation phase
  - Team has relevant knowledge to tap
  - Want to build on others' ideas
- **Description**: Generate many ideas quickly using rules that defer judgment, enhanced with prompts and structure.
- **Process**:
  1. Define focus question clearly
  2. Set rules: defer judgment, encourage wild ideas, build on others, go for quantity
  3. Timebox (e.g., 10-15 minutes)
  4. Use prompts/lenses to stimulate (e.g., "What would [persona] do?")
  5. Capture all ideas without discussion
  6. Group and build on ideas in second phase
- **Key Questions**:
  - What's the focus question?
  - What prompts might stimulate new directions?
  - What lenses or roles could we apply?
- **Outputs**: Large quantity of ideas, idea clusters, build-upon variations
- **Chains With**: SCAMPER, FORCED_CONNECTIONS, EVALUATION methods

---

#### Method: SCAMPER
- **ID**: ID-002
- **Category**: IDEATION
- **Tags**: [modification, systematic, existing-solutions, incremental, variation, checklist]
- **Triggers**:
  - Have existing solution to improve
  - Incremental change might unlock novelty
  - Systematic exploration needed
  - Looking for variations
- **Description**: Systematically modify existing solutions using seven prompts: Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse.
- **Process**:
  1. Select existing solution or concept to modify
  2. Apply each SCAMPER prompt:
     - Substitute: What can be substituted? (materials, people, processes)
     - Combine: What can be combined? (functions, features, ideas)
     - Adapt: What can be adapted from elsewhere?
     - Modify: What can be modified? (size, shape, color, frequency)
     - Put to other uses: What else could this be used for?
     - Eliminate: What can be removed?
     - Reverse/Rearrange: What can be reversed or rearranged?
  3. Generate multiple ideas per prompt
  4. Evaluate and select promising variations
- **Key Questions**:
  - What if we substituted [component] with [alternative]?
  - What could we combine this with?
  - What could we adapt from [other domain]?
  - What if we made it bigger/smaller/faster/slower?
  - What else could this be used for?
  - What if we removed [component]?
  - What if we reversed [aspect]?
- **Outputs**: Systematic variations of original concept, modification ideas, new use cases
- **Chains With**: ATTRIBUTE_LISTING, MORPHOLOGICAL_ANALYSIS, TRIMMING

---

#### Method: ANALOGICAL_REASONING
- **ID**: ID-003
- **Category**: IDEATION
- **Tags**: [cross-domain, transfer, borrowing, parallels, distant-fields, analogy]
- **Triggers**:
  - Problem feels stuck within one industry
  - Looking for non-obvious solutions
  - Other domains have solved similar challenges
  - Need fresh perspective
- **Description**: Borrow solutions from other domains by identifying structural parallels.
- **Process**:
  1. Abstract the problem to its functional essence
  2. Identify domains that face structurally similar challenges
  3. Research how those domains solve the analogous problem
  4. Map the solution back to the original domain
  5. Adapt for domain-specific constraints
- **Key Questions**:
  - What is the abstract structure of this problem?
  - Who else faces a similar challenge under different constraints?
  - How do they solve it?
  - What can we borrow and adapt?
  - What doesn't transfer and why?
- **Outputs**: Problem abstraction, analogous domains list, borrowed solution concepts, adapted solutions
- **Chains With**: BIOMIMICRY, FUNCTION_ORIENTED_SEARCH, FORCED_CONNECTIONS

---

#### Method: FORCED_CONNECTIONS
- **ID**: ID-004
- **Category**: IDEATION
- **Tags**: [random, combination, novelty, juxtaposition, unexpected, serendipity]
- **Triggers**:
  - Need unexpected ideas
  - Conventional thinking dominates
  - Want to break patterns
  - Seeking novelty
- **Description**: Randomly combine unrelated concepts to spark novel ideas through unexpected juxtaposition.
- **Process**:
  1. Select random stimulus (word, image, object, concept from unrelated domain)
  2. List attributes and associations of the random element
  3. Force connections between random element and problem
  4. Generate ideas from each connection
  5. Develop promising ideas further
- **Key Questions**:
  - What if this worked like a [random concept]?
  - What attributes of [random element] could apply here?
  - What's the unexpected connection?
  - How might [random domain] approach this?
- **Outputs**: Forced connections, novel idea combinations, unexpected solution directions
- **Chains With**: RANDOM_STIMULUS, CONCEPT_BLENDING, LATERAL_THINKING

---

#### Method: MORPHOLOGICAL_ANALYSIS
- **ID**: ID-005
- **Category**: IDEATION
- **Tags**: [parameters, systematic, combinations, multi-variable, exhaustive, matrix]
- **Triggers**:
  - Complex, multi-variable problem
  - Need systematic exploration
  - Want to ensure coverage of solution space
  - Looking for novel combinations
- **Description**: Break the system into parameters, enumerate options for each, then systematically recombine.
- **Process**:
  1. Identify key parameters/dimensions of the solution
  2. For each parameter, list all possible options
  3. Create morphological matrix
  4. Generate combinations (can be systematic or selective)
  5. Evaluate combinations for feasibility and novelty
- **Key Questions**:
  - What are the key parameters of this solution?
  - What are all possible options for each parameter?
  - What combinations haven't been tried?
  - Which novel combinations are feasible?
- **Outputs**: Parameter list, morphological matrix, novel combinations, unexplored regions of solution space
- **Chains With**: DESIGN_SPACE_EXPLORATION, ATTRIBUTE_LISTING, SCAMPER

---

#### Method: BIOMIMICRY
- **ID**: ID-006
- **Category**: IDEATION
- **Tags**: [nature, biology, evolution, optimization, natural-solutions, adaptation]
- **Triggers**:
  - Problems involving efficiency or optimization
  - Material or structural challenges
  - Resilience or adaptation needed
  - Sustainability is important
- **Description**: Study how nature solves analogous problems and translate biological mechanisms to human design.
- **Process**:
  1. Define the function needed (e.g., "attach without adhesive," "move efficiently through fluid")
  2. Research how organisms accomplish this function
  3. Identify the principles and mechanisms used
  4. Abstract the principle from the biological implementation
  5. Translate to human-made solution
- **Key Questions**:
  - What function do we need?
  - How has nature solved this over millions of years?
  - What's the underlying principle?
  - How can we translate this mechanism?
  - What constraints differ between biological and human contexts?
- **Outputs**: Biological analogies, mechanism identification, translated design principles, bio-inspired solution concepts
- **Chains With**: ANALOGICAL_REASONING, FUNCTION_ORIENTED_SEARCH, FIRST_PRINCIPLES

---

#### Method: DESIGN_SPACE_EXPLORATION
- **ID**: ID-007
- **Category**: IDEATION
- **Tags**: [systematic, coverage, mapping, unexplored, comprehensive, landscape]
- **Triggers**:
  - Teams converge too quickly
  - Want to ensure no good options missed
  - Need comprehensive view of possibilities
  - Avoiding premature convergence
- **Description**: Systematically map the entire solution space before converging, identifying unexplored regions.
- **Process**:
  1. Define dimensions of the solution space
  2. Create map or matrix of possibilities
  3. Plot known/existing solutions
  4. Identify unexplored regions
  5. Generate concepts for unexplored regions
  6. Evaluate why regions are unexplored (impossible vs. overlooked)
- **Key Questions**:
  - What are the key dimensions of possible solutions?
  - Where do existing solutions cluster?
  - What regions are unexplored?
  - Why are they unexplored?
  - What would a solution in [unexplored region] look like?
- **Outputs**: Solution space map, existing solution positions, unexplored region identification, new concept directions
- **Chains With**: MORPHOLOGICAL_ANALYSIS, ATTRIBUTE_LISTING, S_CURVE_ANALYSIS

---

#### Method: NEGATIVE_BRAINSTORMING
- **ID**: ID-008
- **Category**: IDEATION
- **Tags**: [reverse, inversion, failure, opposite, assumptions, anti-solution]
- **Triggers**:
  - Direct ideation feels forced
  - Team is blocked
  - Need to reveal hidden assumptions
  - Want to identify failure modes
- **Description**: Generate ideas for how to make the problem worse or guarantee failure, then invert to find solutions.
- **Process**:
  1. Reframe: "How could we make this problem worse?" or "How could we guarantee failure?"
  2. Brainstorm ways to fail or worsen
  3. Analyze each failure mode
  4. Invert: What would prevent this failure?
  5. Convert inversions into positive solution concepts
- **Key Questions**:
  - How could we guarantee this fails?
  - What would make users hate this?
  - How could we make the problem worse?
  - What's the opposite of each failure mode?
- **Outputs**: Failure mode list, inverted solutions, revealed assumptions, solution concepts
- **Chains With**: ASSUMPTION_REVERSAL, FAILURE_MODE_ANALYSIS, LATERAL_THINKING

---

#### Method: ATTRIBUTE_LISTING
- **ID**: ID-009
- **Category**: IDEATION
- **Tags**: [attributes, variation, systematic, modification, features, incremental]
- **Triggers**:
  - Seeking incremental improvements
  - Want product variants
  - Need systematic modification
  - Exploring parameter space
- **Description**: List all attributes of the current solution and systematically vary each to generate new concepts.
- **Process**:
  1. List all attributes (materials, shape, size, color, weight, power source, interface, timing, etc.)
  2. For each attribute, list alternative values
  3. Generate concepts by changing individual attributes
  4. Generate concepts by changing multiple attributes
  5. Evaluate variations
- **Key Questions**:
  - What are all the attributes of this solution?
  - What are alternative values for each attribute?
  - What happens if we change [attribute] to [value]?
  - What novel combinations of attribute changes are promising?
- **Outputs**: Attribute inventory, variation matrix, new concept variations
- **Chains With**: SCAMPER, MORPHOLOGICAL_ANALYSIS, DESIGN_SPACE_EXPLORATION

---

#### Method: SIX_THINKING_HATS
- **ID**: ID-010
- **Category**: IDEATION
- **Tags**: [perspectives, structured, group, parallel-thinking, roles, de-bono]
- **Triggers**:
  - Group dynamics create unproductive conflict
  - Groupthink dominates
  - Need balanced exploration
  - Different thinking styles clash
- **Description**: Assign different thinking modes to explore the problem systematically, separating different types of thinking.
- **Process**:
  1. White Hat: Focus on data and facts — What do we know? What do we need to know?
  2. Red Hat: Focus on emotions and intuition — How do we feel about this?
  3. Black Hat: Focus on caution and risks — What could go wrong?
  4. Yellow Hat: Focus on benefits and optimism — What's good about this?
  5. Green Hat: Focus on creativity — What are new possibilities?
  6. Blue Hat: Focus on process — What thinking is needed? Summary?
- **Key Questions**:
  - White: What are the facts?
  - Red: What's our gut feeling?
  - Black: What are the risks and problems?
  - Yellow: What are the benefits?
  - Green: What are creative alternatives?
  - Blue: What's our process? What's the conclusion?
- **Outputs**: Structured exploration from multiple perspectives, balanced evaluation, reduced conflict
- **Chains With**: STRUCTURED_BRAINSTORMING, EVALUATION methods, STRUCTURED_CRITIQUE

---

#### Method: CONCEPT_BLENDING
- **ID**: ID-011
- **Category**: IDEATION
- **Tags**: [synthesis, fusion, emergent, hybrid, combination, category-creation]
- **Triggers**:
  - Seeking category-defining innovations
  - Want emergent properties
  - Two concepts might combine powerfully
  - Looking beyond incremental
- **Description**: Take two or more distinct concepts and force a synthesis that has emergent properties neither parent has alone.
- **Process**:
  1. Select two or more source concepts
  2. Identify key properties of each
  3. Explore ways to blend/synthesize
  4. Identify emergent properties of the blend
  5. Develop the most promising blends
- **Key Questions**:
  - What if we combined [concept A] with [concept B]?
  - What properties would emerge from the combination?
  - What's the essence of each concept we want to preserve?
  - What new category does this blend create?
- **Outputs**: Blended concepts, emergent properties, new category definitions
- **Chains With**: FORCED_CONNECTIONS, ANALOGICAL_REASONING, BLUE_OCEAN

---

#### Method: MIND_MAPPING
- **ID**: ID-012
- **Category**: IDEATION
- **Tags**: [associations, radiant, visual, non-linear, connections, exploration]
- **Triggers**:
  - Problem space feels undefined
  - Need to explore associations
  - Visual thinking helps
  - Want non-linear exploration
- **Description**: Radiate associations outward from a central concept, allowing non-linear exploration and unexpected connections.
- **Process**:
  1. Place central concept in the middle
  2. Add primary branches for main themes/aspects
  3. Add secondary branches for associations
  4. Continue branching, following associations
  5. Look for unexpected connections across branches
  6. Identify promising areas for deeper exploration
- **Key Questions**:
  - What are the main aspects of this concept?
  - What does this associate with?
  - What connections exist across branches?
  - What unexpected relationships emerged?
- **Outputs**: Visual map of concept space, identified connections, areas for exploration
- **Chains With**: STRUCTURED_BRAINSTORMING, DESIGN_SPACE_EXPLORATION, SYSTEMS_MAPPING

---

#### Method: WORST_POSSIBLE_IDEA
- **ID**: ID-013
- **Category**: IDEATION
- **Tags**: [inhibition, bad-ideas, permission, assumptions, hidden-value, playful]
- **Triggers**:
  - Team is self-censoring
  - Perfectionism blocks ideation
  - Need to lower inhibition
  - Want to reveal assumptions
- **Description**: Deliberately generate the worst ideas first to lower inhibition and often reveal hidden assumptions or seeds of good ideas.
- **Process**:
  1. Ask: "What are the worst possible solutions?"
  2. Generate deliberately bad ideas enthusiastically
  3. Analyze why each idea is "bad"
  4. Look for hidden assumptions or seeds of value
  5. Invert or modify bad ideas into good ones
- **Key Questions**:
  - What's the worst way to solve this?
  - Why is this idea bad? (Reveals criteria)
  - Is there a seed of value hidden here?
  - What assumption does this bad idea challenge?
- **Outputs**: Bad idea list, revealed criteria and assumptions, inverted/modified good ideas
- **Chains With**: NEGATIVE_BRAINSTORMING, ASSUMPTION_REVERSAL, STRUCTURED_BRAINSTORMING

---

### BREAKTHROUGH Methods

#### Method: TRIZ
- **ID**: BR-001
- **Category**: BREAKTHROUGH
- **Tags**: [systematic, patents, contradictions, inventive-principles, patterns, resolution]
- **Triggers**:
  - Facing apparent contradictions
  - Need systematic rather than random approach
  - Seeking inventive rather than compromise solutions
  - Problem has technical parameters
- **Description**: Systematic method derived from patterns in global patents, focusing on resolving contradictions rather than optimizing tradeoffs.
- **Process**:
  1. Define the problem in terms of contradictions (improving X worsens Y)
  2. Identify the contradicting parameters using TRIZ parameter list
  3. Consult contradiction matrix to find suggested principles
  4. Apply relevant inventive principles (from 40 principles)
  5. Generate specific solutions from principles
- **Key Questions**:
  - What contradiction exists? (Improving what worsens what?)
  - What are the contradicting parameters?
  - Which inventive principles address this contradiction?
  - How can we apply these principles specifically?
- **Outputs**: Contradiction statement, relevant inventive principles, principle-based solution concepts
- **Chains With**: CONTRADICTION_MAPPING, IDEAL_FINAL_RESULT, INVENTIVE_STANDARDS

---

#### Method: IDEAL_FINAL_RESULT
- **ID**: BR-002
- **Category**: BREAKTHROUGH
- **Tags**: [ideal, perfection, zero-cost, function-without-system, aspiration, vision]
- **Triggers**:
  - Need to set aspirational direction
  - Current thinking is too incremental
  - Want to challenge fundamental assumptions
  - Seeking breakthrough rather than improvement
- **Description**: Imagine the perfect solution where the function exists with minimal or zero cost, complexity, or harm.
- **Process**:
  1. Define the useful function needed
  2. Imagine the function being delivered perfectly, instantly, for free
  3. Describe what the Ideal Final Result looks like
  4. Work backward: What prevents achieving the IFR?
  5. Address each barrier
- **Key Questions**:
  - What is the useful function we need?
  - What would it look like if the function delivered itself?
  - What if there were no system, only the result?
  - What prevents achieving the IFR?
  - How close can we get to the IFR?
- **Outputs**: IFR description, barrier identification, solution directions toward IFR
- **Chains With**: FIRST_PRINCIPLES, TRIZ, TRIMMING

---

#### Method: CONTRADICTION_MAPPING
- **ID**: BR-003
- **Category**: BREAKTHROUGH
- **Tags**: [tradeoffs, contradictions, parameters, eliminate-tradeoff, both-and]
- **Triggers**:
  - Facing apparent tradeoffs
  - "You can't have both X and Y"
  - Optimization hitting limits
  - Seeking breakthrough past constraints
- **Description**: Explicitly state what must improve and what must not get worse, then seek to eliminate the tradeoff rather than optimize within it.
- **Process**:
  1. Identify what needs to improve
  2. Identify what must not get worse (or must also improve)
  3. State the contradiction clearly
  4. Analyze: Is this a real physical contradiction or an assumed one?
  5. Seek solutions that resolve rather than balance
- **Key Questions**:
  - What must improve?
  - What must not get worse?
  - Is this tradeoff real or assumed?
  - Who has solved this contradiction?
  - How can we have both?
- **Outputs**: Contradiction statement, real vs. assumed analysis, resolution directions
- **Chains With**: TRIZ, FIRST_PRINCIPLES, CONSTRAINT_SURFACING

---

#### Method: FUNCTIONAL_ANALYSIS
- **ID**: BR-004
- **Category**: BREAKTHROUGH
- **Tags**: [functions, verb-noun, components, replacement, abstraction, essence]
- **Triggers**:
  - Stuck thinking about existing components
  - Need to consider radical replacements
  - Want to separate what from how
  - Seeking simplification
- **Description**: Describe the system only in terms of functions (verb + noun), not components, to enable radical replacement.
- **Process**:
  1. List all components of current system
  2. For each component, identify its function(s) using verb + noun format
  3. Remove component names, keeping only functions
  4. For each function, ask: What else could perform this function?
  5. Identify functions that could be eliminated or combined
- **Key Questions**:
  - What function does this component perform? (verb + noun)
  - What else could perform this function?
  - Is this function necessary?
  - Can functions be combined?
  - What's the minimum set of functions needed?
- **Outputs**: Function list (component-free), alternative function carriers, function elimination opportunities
- **Chains With**: TRIMMING, IDEAL_FINAL_RESULT, FUNCTION_ORIENTED_SEARCH

---

#### Method: SIT (SYSTEMATIC_INVENTIVE_THINKING)
- **ID**: BR-005
- **Category**: BREAKTHROUGH
- **Tags**: [patterns, templates, subtraction, multiplication, division, task-unification, attribute-dependency]
- **Triggers**:
  - Seeking structured innovation
  - Within existing system boundaries
  - Want proven patterns
  - Systematic approach needed
- **Description**: Apply five thinking patterns derived from successful innovations to generate new concepts.
- **Process**:
  1. Subtraction: Remove an essential component — what happens? How might function redistribute?
  2. Multiplication: Copy a component but change it — what if we had two different versions?
  3. Division: Divide a component and rearrange — spatial, functional, or temporal division
  4. Task Unification: Assign a new task to existing component — what else could this do?
  5. Attribute Dependency Change: Create or break dependencies between attributes
- **Key Questions**:
  - Subtraction: What if we removed [essential component]?
  - Multiplication: What if we had multiple versions of [component]?
  - Division: What if we divided [component] and rearranged?
  - Task Unification: What additional task could [component] perform?
  - Attribute Dependency: What if [attribute A] changed with [attribute B]?
- **Outputs**: Pattern-generated concepts, component modifications, new attribute relationships
- **Chains With**: TRIZ, SCAMPER, TRIMMING

---

#### Method: TRIMMING
- **ID**: BR-006
- **Category**: BREAKTHROUGH
- **Tags**: [simplification, removal, cost-reduction, reliability, elegance, less-is-more]
- **Triggers**:
  - System has become bloated
  - Cost reduction needed
  - Reliability issues
  - Seeking elegance
- **Description**: Systematically remove components while preserving or redistributing their functions.
- **Process**:
  1. List all components and their functions
  2. For each component, ask: Can it be eliminated?
  3. If function is needed, ask: Can another component perform it?
  4. If not, ask: Can the function be eliminated entirely?
  5. Implement trimming, verify function preserved
- **Key Questions**:
  - Do we need this component?
  - Can another component perform this function?
  - Can the supersystem perform this function?
  - Can we eliminate the need for this function?
  - What's the minimum viable system?
- **Outputs**: Trimmed system design, function redistribution, simplified architecture
- **Chains With**: FUNCTIONAL_ANALYSIS, IDEAL_FINAL_RESULT, ASIT

---

#### Method: RESOURCES_ANALYSIS
- **ID**: BR-007
- **Category**: BREAKTHROUGH
- **Tags**: [unused, available, free, hidden, substances, fields, space, time, information]
- **Triggers**:
  - New components seem necessary but undesirable
  - Cost constraints are tight
  - Looking for elegant solutions
  - Want to use what's already there
- **Description**: Identify all available resources (substances, fields, space, time, information) that aren't being utilized.
- **Process**:
  1. Inventory all available resources:
     - Substances (materials, byproducts, waste)
     - Fields (energy, forces present)
     - Space (unused volumes, surfaces)
     - Time (idle time, sequences)
     - Information (data, signals present)
  2. Identify which resources are unused or underused
  3. Ask: How could this resource solve the problem?
  4. Generate solutions using available resources
- **Key Questions**:
  - What substances are present but unused?
  - What energy or fields are available?
  - What space is unused?
  - What time is wasted?
  - What information exists but isn't used?
  - How could these solve our problem?
- **Outputs**: Resource inventory, unused resource identification, resource-based solution concepts
- **Chains With**: TRIMMING, IDEAL_FINAL_RESULT, ASIT

---

#### Method: FUNCTION_ORIENTED_SEARCH
- **ID**: BR-008
- **Category**: BREAKTHROUGH
- **Tags**: [function, search, cross-domain, decoupling, what-not-how, alternatives]
- **Triggers**:
  - Current implementation technology is a dead end
  - Need radically different approach
  - Want to find non-obvious solutions
  - Separating what from how
- **Description**: Define the required function abstractly, then search broadly for who else performs that function.
- **Process**:
  1. Define the function needed in abstract terms (verb + object + constraints)
  2. Remove domain-specific assumptions
  3. Search: Who else performs this function? (other industries, nature, other sciences)
  4. Study how they accomplish the function
  5. Adapt their approach to your context
- **Key Questions**:
  - What is the function at its most abstract?
  - Who else needs to [function]?
  - How do they accomplish it?
  - What can we learn and adapt?
  - What constraints differ?
- **Outputs**: Abstract function definition, alternative function performers, adapted solution approaches
- **Chains With**: ANALOGICAL_REASONING, BIOMIMICRY, FUNCTIONAL_ANALYSIS

---

#### Method: S_CURVE_ANALYSIS
- **ID**: BR-009
- **Category**: BREAKTHROUGH
- **Tags**: [evolution, maturity, lifecycle, paradigm, transition, technology-forecasting]
- **Triggers**:
  - Determining whether to improve or replace
  - Technology seems to be hitting limits
  - Planning long-term innovation strategy
  - Assessing technology maturity
- **Description**: Map where the technology sits on its evolution curve to determine whether to optimize existing technology or leap to a new paradigm.
- **Process**:
  1. Identify the key performance parameter
  2. Plot historical performance over time/investment
  3. Assess position on S-curve (birth, growth, maturity, decline)
  4. If mature/declining, identify candidate replacement technologies
  5. Determine strategy: optimize or transition
- **Key Questions**:
  - What is the key performance measure?
  - Where are we on the S-curve?
  - Is improvement slowing despite investment?
  - What technologies could create a new curve?
  - When should we transition?
- **Outputs**: S-curve position assessment, improvement potential estimate, replacement technology candidates, transition strategy
- **Chains With**: TECHNOLOGY_ROADMAPPING, DESIGN_SPACE_EXPLORATION, FIRST_PRINCIPLES

---

#### Method: NINE_WINDOWS
- **ID**: BR-010
- **Category**: BREAKTHROUGH
- **Tags**: [system-operator, time, hierarchy, super-system, subsystem, evolution, strategic]
- **Triggers**:
  - Seeking strategic rather than tactical innovation
  - Need broader perspective
  - Want to understand evolution patterns
  - Looking for hidden resources
- **Description**: Analyze the system across three levels (super-system, system, subsystem) and three time periods (past, present, future) to reveal patterns and resources.
- **Process**:
  1. Create 3x3 matrix: columns = past, present, future; rows = super-system, system, subsystem
  2. Fill in each cell:
     - Past: How did each level look before?
     - Present: How does each level look now?
     - Future: How might each level evolve?
  3. Identify evolution patterns
  4. Find resources at super-system or subsystem level
  5. Generate insights for innovation
- **Key Questions**:
  - Past: How did this system/super-system/subsystem evolve?
  - Present: What exists at each level now?
  - Future: What trends will shape each level?
  - What patterns do we see across the nine windows?
  - What resources exist at other levels or times?
- **Outputs**: Nine windows analysis, evolution patterns, level-jumping opportunities, strategic insights
- **Chains With**: SYSTEMS_MAPPING, S_CURVE_ANALYSIS, SCENARIO_PLANNING

---

### COGNITIVE Methods

#### Method: LATERAL_THINKING
- **ID**: CG-001
- **Category**: COGNITIVE
- **Tags**: [indirect, counterintuitive, sideways, provocation, escape, de-bono]
- **Triggers**:
  - Logical thinking leads to same conclusions
  - Need to escape obvious paths
  - Counterintuitive solutions may exist
  - Breaking mental patterns
- **Description**: Deliberately pursue indirect or counterintuitive approaches to escape habitual thinking patterns.
- **Process**:
  1. Recognize current thinking pattern
  2. Apply provocations: "What if the opposite were true?"
  3. Consider indirect routes to the goal
  4. Challenge the direction of approach
  5. Develop promising lateral paths
- **Key Questions**:
  - What if the opposite were true?
  - What if we approached from a completely different direction?
  - What would a naive person try?
  - What's the most counterintuitive approach?
  - What if we pursued a different goal that achieves the same result?
- **Outputs**: Alternative approaches, counterintuitive solutions, broken assumptions
- **Chains With**: ASSUMPTION_REVERSAL, PROVOCATIVE_OPERATIONS, FORCED_CONNECTIONS

---

#### Method: ASSUMPTION_REVERSAL
- **ID**: CG-002
- **Category**: COGNITIVE
- **Tags**: [assumptions, flip, opposite, challenge, hidden-beliefs, inversion]
- **Triggers**:
  - Many assumptions underlie current thinking
  - Need fresh perspective
  - Conventional wisdom may be wrong
  - Seeking contrarian approaches
- **Description**: List the assumptions underlying current approaches and systematically flip each one.
- **Process**:
  1. List all assumptions about the problem, users, constraints, and solutions
  2. For each assumption, state its opposite
  3. Explore: What if the opposite were true?
  4. Generate ideas based on reversed assumptions
  5. Evaluate which reversals reveal opportunities
- **Key Questions**:
  - What assumptions are we making?
  - What if [assumption] were false?
  - What if the opposite were true?
  - What if users wanted [opposite of assumed want]?
  - What opportunities does this reversal reveal?
- **Outputs**: Assumption inventory, reversed assumptions, reversal-based ideas
- **Chains With**: CONSTRAINT_SURFACING, LATERAL_THINKING, NEGATIVE_BRAINSTORMING

---

#### Method: RANDOM_STIMULUS
- **ID**: CG-003
- **Category**: COGNITIVE
- **Tags**: [random, external, associations, unexpected, trigger, serendipity]
- **Triggers**:
  - Need to break out of current thinking
  - Want unexpected associations
  - Team is circling same ideas
  - Seeking serendipity
- **Description**: Introduce unrelated words, images, or artifacts to spark new associations and break patterns.
- **Process**:
  1. Select random stimulus (random word, image, object, or experience)
  2. Examine the stimulus — list its attributes, associations, and how it works
  3. Force connections to the problem
  4. Generate ideas from the connections
  5. Develop promising ideas
- **Key Questions**:
  - What are the attributes of this random element?
  - How does it work?
  - What associations does it trigger?
  - How might any of these connect to our problem?
- **Outputs**: Random-stimulus connections, unexpected ideas, broken thought patterns
- **Chains With**: FORCED_CONNECTIONS, LATERAL_THINKING, ANALOGICAL_REASONING

---

#### Method: ROLE_STORMING
- **ID**: CG-004
- **Category**: COGNITIVE
- **Tags**: [personas, perspectives, roles, empathy, alternative-viewpoints, characters]
- **Triggers**:
  - Need different perspectives
  - Self-censoring blocks ideas
  - Want to think like users or stakeholders
  - Breaking out of expert mindset
- **Description**: Ideate as another persona to access different perspectives and reduce self-censorship.
- **Process**:
  1. Select personas (child, competitor, regulator, hacker, naive user, expert from other field, etc.)
  2. Embody the persona — think about their knowledge, motivations, constraints
  3. Ideate from that persona's perspective
  4. Switch personas and repeat
  5. Synthesize insights across personas
- **Key Questions**:
  - How would a child approach this?
  - What would a competitor do?
  - How would someone from [other field] see this?
  - What would a hacker try?
  - What would frustrate a regulator?
- **Outputs**: Persona-based ideas, alternative perspectives, reduced self-censorship
- **Chains With**: EMPATHY_MAPPING, SIX_THINKING_HATS, EXTREME_USER_ANALYSIS

---

#### Method: INCUBATION
- **ID**: CG-005
- **Category**: COGNITIVE
- **Tags**: [unconscious, rest, stepping-away, sleep, diffuse-thinking, breaks]
- **Triggers**:
  - Intense focus isn't producing results
  - Team is mentally exhausted
  - Problem is complex and needs processing
  - Stuck despite effort
- **Description**: Deliberately step away from the problem to allow unconscious processing.
- **Process**:
  1. Ensure thorough conscious engagement with the problem first
  2. Deliberately step away (take a break, work on something else, sleep on it)
  3. Engage in light, unrelated activities
  4. Return to the problem with fresh perspective
  5. Capture any insights that emerged
- **Key Questions**:
  - Have we thoroughly engaged with this problem?
  - How long should we step away?
  - What unrelated activities might help?
  - What insights emerged during the break?
- **Outputs**: Fresh perspective, incubated insights, renewed energy
- **Chains With**: Any method — use incubation between intensive sessions

---

#### Method: CONSTRAINT_INJECTION
- **ID**: CG-006
- **Category**: COGNITIVE
- **Tags**: [artificial-constraints, forcing, creativity, limitations, what-if, scarcity]
- **Triggers**:
  - Too many options create paralysis
  - Need to force novel solutions
  - Want to test robustness
  - Seeking creative pressure
- **Description**: Artificially add constraints to force novel solutions by eliminating obvious paths.
- **Process**:
  1. Identify an extreme constraint to inject (10x less budget, 10x faster, no electricity, etc.)
  2. Apply the constraint to the problem
  3. Generate solutions that work under the constraint
  4. Evaluate which solutions have merit even without the constraint
  5. Relax constraints gradually
- **Key Questions**:
  - What if we had 1/10th the budget?
  - What if it had to work in 10 seconds?
  - What if [key resource] were unavailable?
  - What if it had to work for 1 million users?
  - What would we do if [constraint]?
- **Outputs**: Constraint-forced solutions, robust approaches, simplified designs
- **Chains With**: FIRST_PRINCIPLES, IDEAL_FINAL_RESULT, RESOURCES_ANALYSIS

---

#### Method: TIME_TRAVEL
- **ID**: CG-007
- **Category**: COGNITIVE
- **Tags**: [future, past, temporal, paradigm-shift, evolution, perspective]
- **Triggers**:
  - Thinking feels trapped in present paradigm
  - Want long-term perspective
  - Need to challenge current assumptions
  - Exploring what might change
- **Description**: Imagine the problem 10, 50, or 100 years in the future or past to escape present-paradigm thinking.
- **Process**:
  1. Select time horizon (past or future, how far)
  2. Future: What technologies, values, or structures might exist? How does this change the problem?
  3. Past: What solutions existed before modern assumptions? What was lost?
  4. Generate ideas informed by temporal shift
  5. Bring relevant insights to present
- **Key Questions**:
  - Future: What will change in 10/50/100 years?
  - Future: How would people then solve this?
  - Past: How did people solve this before [technology/assumption]?
  - Past: What approaches have we forgotten?
  - What can we bring from that time to now?
- **Outputs**: Temporal perspective shifts, past/future-inspired solutions, challenged assumptions
- **Chains With**: SCENARIO_PLANNING, BACKCASTING, SPECULATIVE_DESIGN

---

#### Method: SCALE_SHIFTING
- **ID**: CG-008
- **Category**: COGNITIVE
- **Tags**: [scale, size, magnitude, micro, macro, perspective-change]
- **Triggers**:
  - Problem feels stuck at one level
  - Different scale might reveal solutions
  - Want to test scalability
  - Seeking new perspectives
- **Description**: Consider the problem at radically different scales to reveal different solution approaches.
- **Process**:
  1. State the current scale of the problem
  2. Shift dramatically larger: What if it were 1000x bigger?
  3. Shift dramatically smaller: What if it were 1000x smaller?
  4. Shift user scale: What if for one person? A billion people?
  5. Identify insights from each scale
  6. Apply relevant insights to actual scale
- **Key Questions**:
  - What if this were 1000x bigger?
  - What if this were 1000x smaller?
  - What if this affected only one person?
  - What if this affected a billion people?
  - What approaches work at different scales?
- **Outputs**: Scale-shifted perspectives, scale-dependent insights, robust solutions
- **Chains With**: NINE_WINDOWS, CONSTRAINT_INJECTION, SYSTEMS_MAPPING

---

#### Method: PROVOCATIVE_OPERATIONS
- **ID**: CG-009
- **Category**: COGNITIVE
- **Tags**: [po, illogical, provocation, stepping-stone, de-bono, escape]
- **Triggers**:
  - Logical thinking keeps circling back
  - Need to break patterns
  - Seeking radical departure
  - Conventional provocation isn't working
- **Description**: Make deliberately illogical statements (Po) as stepping stones to escape habitual thinking.
- **Process**:
  1. Create a provocative, illogical statement: "Po: [absurd statement]"
  2. The statement doesn't need to be correct or sensible
  3. Use it as a stepping stone — what does it lead to?
  4. Extract principles or directions from the provocation
  5. Develop viable ideas from the extracted insights
- **Key Questions**:
  - Po: What if [absurd reversal]?
  - What does this provocation make us think of?
  - What principle might underlie this provocation?
  - What viable idea does this lead to?
- **Outputs**: Provocative statements, stepping-stone insights, pattern-breaking ideas
- **Chains With**: LATERAL_THINKING, ASSUMPTION_REVERSAL, FORCED_CONNECTIONS

---

#### Method: BOUNDARY_EXAMINATION
- **ID**: CG-010
- **Category**: COGNITIVE
- **Tags**: [boundaries, limits, implicit, crossing, expansion, scope]
- **Triggers**:
  - Team unconsciously limits solution space
  - Implied boundaries constrain thinking
  - Want to check what's in/out of scope
  - Seeking expanded possibilities
- **Description**: Identify implicit boundaries of the problem and deliberately cross them.
- **Process**:
  1. Define the current problem boundaries (what's in scope, what's out)
  2. Identify implicit/unstated boundaries
  3. For each boundary, ask: What if we crossed it?
  4. Generate solutions that cross boundaries
  5. Evaluate which boundary crossings are valuable
- **Key Questions**:
  - What are we assuming is out of scope?
  - Why is [boundary] where it is?
  - What if we crossed [boundary]?
  - What opportunities exist just outside current boundaries?
- **Outputs**: Boundary map, boundary-crossing opportunities, expanded solution space
- **Chains With**: CONSTRAINT_SURFACING, PROBLEM_REFRAMING, SCALE_SHIFTING

---

### EXPLORATION Methods

#### Method: PROTOTYPING
- **ID**: EX-001
- **Category**: EXPLORATION
- **Tags**: [build, test, artifact, assumption, tangible, learning, iteration]
- **Triggers**:
  - Have concept to test
  - Need tangible artifact
  - Assumptions need validation
  - Learning by building
- **Description**: Build the simplest artifact that tests a key assumption — can be physical, digital, or conceptual.
- **Process**:
  1. Identify the key assumption(s) to test
  2. Determine minimum prototype needed to test
  3. Build the prototype quickly (hours to days, not weeks)
  4. Test with real or representative users
  5. Learn and iterate
- **Key Questions**:
  - What assumption are we testing?
  - What's the minimum prototype to test it?
  - What will we learn?
  - What constitutes success or failure?
  - What's the fastest way to build this?
- **Outputs**: Working prototype, test results, validated/invalidated assumptions, insights for iteration
- **Chains With**: WIZARD_OF_OZ, PAPER_PROTOTYPING, MVE

---

#### Method: WIZARD_OF_OZ
- **ID**: EX-002
- **Category**: EXPLORATION
- **Tags**: [simulation, manual, behind-curtain, fake-automation, demand-test, feasibility]
- **Triggers**:
  - Automation would be expensive to build
  - Want to test experience before building
  - Testing demand for capability
  - Validating interaction design
- **Description**: Simulate functionality manually before building automation — users experience the result while humans provide it behind the scenes.
- **Process**:
  1. Identify the functionality to simulate
  2. Design the user-facing experience
  3. Create manual process to deliver results
  4. Run the simulation with real users
  5. Measure demand, satisfaction, and feasibility
- **Key Questions**:
  - What functionality should we simulate?
  - How can humans deliver this manually?
  - What will users experience?
  - What are we learning about demand and experience?
  - What did we learn about the actual work involved?
- **Outputs**: Simulated experience, demand validation, experience insights, feasibility learning
- **Chains With**: PRETOTYPING, PROTOTYPING, CONCIERGE_TEST

---

#### Method: PRETOTYPING
- **ID**: EX-003
- **Category**: EXPLORATION
- **Tags**: [demand, before-building, fake-door, landing-page, market-test, validation]
- **Triggers**:
  - Unsure if demand exists
  - Want to test before building
  - Need market validation
  - Resources are limited
- **Description**: Test demand before building the solution using techniques like landing pages, fake doors, and concierge tests.
- **Process**:
  1. Define what demand signal you need to see
  2. Choose pretotyping technique:
     - Fake door: Button/link that measures clicks before feature exists
     - Landing page: Describe offering, measure sign-ups
     - Concierge: Deliver service manually to first customers
     - Mechanical Turk: Fake automation with human labor
  3. Set success criteria
  4. Run the pretotype
  5. Measure and decide
- **Key Questions**:
  - What demand signal would convince us?
  - How can we test demand without building?
  - What's the minimum commitment we can ask for?
  - What did the signal tell us?
- **Outputs**: Demand signal, market validation data, go/no-go decision
- **Chains With**: WIZARD_OF_OZ, MVE, ASSUMPTION_RISK_RANKING

---

#### Method: THOUGHT_EXPERIMENTS
- **ID**: EX-004
- **Category**: EXPLORATION
- **Tags**: [mental, what-if, scenarios, reasoning, no-build, logical]
- **Triggers**:
  - Building would be premature
  - Can reason through scenarios
  - Testing logical coherence
  - Resource-constrained exploration
- **Description**: Run rigorous "what-if" scenarios mentally or in discussion without building anything.
- **Process**:
  1. Define the scenario or question
  2. Establish assumptions and parameters
  3. Reason through consequences step by step
  4. Identify what would happen, what could go wrong
  5. Extract insights and implications
- **Key Questions**:
  - What would happen if we did X?
  - What are the consequences at each step?
  - What could go wrong?
  - What does this reveal about our assumptions?
  - What would we need to believe for this to work?
- **Outputs**: Scenario analysis, logical implications, identified risks, refined assumptions
- **Chains With**: FAILURE_MODE_ANALYSIS, SCENARIO_PLANNING, COUNTERFACTUAL_THINKING

---

#### Method: STORYBOARDING
- **ID**: EX-005
- **Category**: EXPLORATION
- **Tags**: [visual, narrative, sequence, journey, experience, communication]
- **Triggers**:
  - Solution involves experience over time
  - Need to communicate concept
  - Testing user journey
  - Identifying gaps in experience
- **Description**: Create visual narratives showing the solution in context, frame by frame.
- **Process**:
  1. Define the scenario and user
  2. Identify key moments in the experience
  3. Sketch each moment (frame)
  4. Add context, dialogue, emotion
  5. Review for gaps, friction, opportunities
- **Key Questions**:
  - What are the key moments in this experience?
  - What is the user thinking/feeling at each moment?
  - Where are the gaps or friction points?
  - What happens before and after?
- **Outputs**: Visual storyboard, identified journey gaps, experience narrative
- **Chains With**: USER_JOURNEY_MAPPING, PAPER_PROTOTYPING, BODYSTORMING

---

#### Method: PAPER_PROTOTYPING
- **ID**: EX-006
- **Category**: EXPLORATION
- **Tags**: [low-fidelity, sketches, cheap, fast, disposable, iteration]
- **Triggers**:
  - Testing interaction concepts
  - Need fast iteration
  - Before any development
  - Want user comfort in critique
- **Description**: Create low-fidelity mockups using paper, cardboard, or sketches for rapid iteration.
- **Process**:
  1. Sketch the interface or concept on paper
  2. Create movable elements as needed
  3. Test with users (facilitator acts as computer)
  4. Observe confusion and friction
  5. Iterate immediately
- **Key Questions**:
  - What's the core interaction to test?
  - How can we simulate this with paper?
  - What confused the user?
  - What do they expect to happen?
- **Outputs**: Paper prototype, user feedback, interaction insights, rapid iterations
- **Chains With**: PROTOTYPING, STORYBOARDING, USABILITY_TESTING

---

#### Method: BODYSTORMING
- **ID**: EX-007
- **Category**: EXPLORATION
- **Tags**: [physical, acting, space, embodied, simulation, ergonomics]
- **Triggers**:
  - Solution involves physical interaction
  - Need to understand space and movement
  - Testing ergonomics
  - Experiencing rather than imagining
- **Description**: Physically act out scenarios to generate and test ideas using body and space.
- **Process**:
  1. Define the scenario to explore
  2. Set up the physical space (can be rough simulation)
  3. Act out the experience physically
  4. Note discoveries about movement, space, timing
  5. Generate ideas from the embodied experience
- **Key Questions**:
  - What does it feel like to do this physically?
  - What did we discover about space and movement?
  - What's awkward or uncomfortable?
  - What opportunities did physical experience reveal?
- **Outputs**: Embodied insights, spatial discoveries, physically-informed ideas
- **Chains With**: STORYBOARDING, EXPERIENCE_PROTOTYPING, ROLE_STORMING

---

#### Method: SCENARIO_PLANNING
- **ID**: EX-008
- **Category**: EXPLORATION
- **Tags**: [futures, uncertainty, robustness, multiple-paths, strategic, flexibility]
- **Triggers**:
  - Future is uncertain
  - Need robust solutions
  - Testing across conditions
  - Strategic planning
- **Description**: Develop multiple plausible futures and test solutions against each.
- **Process**:
  1. Identify key uncertainties that shape the future
  2. Select two most impactful, uncertain dimensions
  3. Create 2x2 matrix of four scenarios
  4. Develop rich narrative for each scenario
  5. Test solutions against all scenarios
  6. Identify robust strategies
- **Key Questions**:
  - What are the key uncertainties?
  - What scenarios could unfold?
  - How would our solution perform in each?
  - What strategy works across scenarios?
  - What are early indicators of each scenario?
- **Outputs**: Scenario matrix, scenario narratives, robustness assessment, adaptive strategy
- **Chains With**: TECHNOLOGY_ROADMAPPING, TIME_TRAVEL, BACKCASTING

---

#### Method: MVE (MINIMUM_VIABLE_EXPERIMENT)
- **ID**: EX-009
- **Category**: EXPLORATION
- **Tags**: [minimum, decisive, learning, efficient, focused, experiment]
- **Triggers**:
  - Resources are limited
  - Need to maximize learning
  - Uncertainty is high
  - Focused validation needed
- **Description**: Identify the smallest possible test that provides decisive information.
- **Process**:
  1. Identify the key assumption to test
  2. Define what would prove or disprove it
  3. Design the minimum experiment to get that signal
  4. Set clear success/failure criteria in advance
  5. Run the experiment
  6. Make decision based on results
- **Key Questions**:
  - What's the most critical assumption?
  - What's the minimum test to validate/invalidate it?
  - What signal would change our decision?
  - How can we get that signal fastest and cheapest?
- **Outputs**: Focused experiment design, decisive result, clear learning
- **Chains With**: ASSUMPTION_RISK_RANKING, PRETOTYPING, PROTOTYPING

---

#### Method: FAILURE_MODE_ANALYSIS
- **ID**: EX-010
- **Category**: EXPLORATION
- **Tags**: [failure, risk, pre-mortem, prevention, robustness, what-could-go-wrong]
- **Triggers**:
  - Before major investment
  - Need to build confidence
  - Identifying risks
  - Testing robustness
- **Description**: Systematically imagine how the solution could fail to identify and prevent failure modes.
- **Process**:
  1. Pre-mortem: Imagine the project has failed completely
  2. Generate explanations for why it failed
  3. Identify most likely and most severe failure modes
  4. Develop mitigations for top failure modes
  5. Test whether mitigations work
- **Key Questions**:
  - It's one year later and this has failed completely. Why?
  - What are all the ways this could fail?
  - Which failures are most likely? Most severe?
  - How can we prevent or mitigate each?
  - What early warning signs should we watch for?
- **Outputs**: Failure mode inventory, risk ranking, mitigation plans, early warning indicators
- **Chains With**: ASSUMPTION_RISK_RANKING, THOUGHT_EXPERIMENTS, KILL_CRITERIA

---

### EVALUATION Methods

#### Method: IMPACT_VS_EFFORT
- **ID**: EV-001
- **Category**: EVALUATION
- **Tags**: [prioritization, matrix, quick-wins, big-bets, effort, impact]
- **Triggers**:
  - Multiple ideas to prioritize
  - Need quick decisions
  - Looking for asymmetric opportunities
  - Resource allocation
- **Description**: Map ideas on impact vs. effort matrix to find asymmetric opportunities.
- **Process**:
  1. List ideas to evaluate
  2. Estimate impact (high/medium/low or score)
  3. Estimate effort (high/medium/low or score)
  4. Plot on 2x2 matrix
  5. Prioritize: High impact/Low effort first
- **Key Questions**:
  - What impact could this have?
  - What effort would this require?
  - What are the quick wins? (High impact, low effort)
  - What are the big bets? (High impact, high effort)
  - What should we avoid? (Low impact, high effort)
- **Outputs**: Prioritized idea list, quick wins identification, effort-impact map
- **Chains With**: ASSUMPTION_RISK_RANKING, PUGH_MATRIX, PORTFOLIO_THINKING

---

#### Method: ASSUMPTION_RISK_RANKING
- **ID**: EV-002
- **Category**: EVALUATION
- **Tags**: [assumptions, risk, critical, validation, priority, testing]
- **Triggers**:
  - Ideas rest on assumptions
  - Need to prioritize testing
  - Identifying fatal flaws
  - Limited validation resources
- **Description**: Identify which assumptions would kill the idea if false and prioritize testing them.
- **Process**:
  1. List all assumptions underlying the idea
  2. For each assumption, rate:
     - Criticality: How bad if false? (1-5)
     - Uncertainty: How confident are we? (1-5)
  3. Calculate risk score = Criticality × Uncertainty
  4. Rank assumptions by risk score
  5. Test highest-risk assumptions first
- **Key Questions**:
  - What assumptions underlie this idea?
  - Which assumptions would be fatal if wrong?
  - How uncertain are we about each?
  - What should we test first?
- **Outputs**: Assumption inventory, risk ranking, test priority list
- **Chains With**: MVE, KILL_CRITERIA, FEASIBILITY_DESIRABILITY_VIABILITY

---

#### Method: REGRET_MINIMIZATION
- **ID**: EV-003
- **Category**: EVALUATION
- **Tags**: [regret, long-term, missed-opportunity, decision, courage, optionality]
- **Triggers**:
  - Deciding whether to pursue bold idea
  - Risk aversion may cause missed opportunities
  - Long-term thinking needed
  - Need decision framework
- **Description**: Evaluate options by asking which you would regret not trying.
- **Process**:
  1. Project to end of life or career
  2. Ask: Which option would I regret not trying?
  3. Consider regret of action vs. regret of inaction
  4. Factor in what you'd learn even from failure
  5. Make decision based on regret minimization
- **Key Questions**:
  - Looking back, which would I regret not trying?
  - What would I regret more: trying and failing, or never trying?
  - What would I learn even if it fails?
  - Is this a once-in-a-lifetime opportunity?
- **Outputs**: Decision based on long-term regret minimization
- **Chains With**: REVERSIBILITY_ANALYSIS, PORTFOLIO_THINKING, OPPORTUNITY_COST

---

#### Method: PORTFOLIO_THINKING
- **ID**: EV-004
- **Category**: EVALUATION
- **Tags**: [portfolio, diversification, horizons, balance, risk, bets]
- **Triggers**:
  - Multiple initiatives to balance
  - Need risk diversification
  - Different time horizons
  - Strategic allocation
- **Description**: Pursue multiple bets across time horizons and risk levels.
- **Process**:
  1. Categorize ideas by type:
     - Core: Improve existing (low risk, near-term)
     - Adjacent: Expand to related areas (medium risk, medium-term)
     - Transformational: Breakthrough bets (high risk, long-term)
  2. Assess current portfolio balance
  3. Determine target allocation
  4. Adjust investments to achieve balance
- **Key Questions**:
  - What's our current portfolio mix?
  - Do we have enough transformational bets?
  - Are we over-invested in any one category?
  - What's the right balance for our situation?
- **Outputs**: Portfolio categorization, balance assessment, allocation recommendations
- **Chains With**: INNOVATION_AMBITION_MATRIX, REAL_OPTIONS, IMPACT_VS_EFFORT

---

#### Method: PUGH_MATRIX
- **ID**: EV-005
- **Category**: EVALUATION
- **Tags**: [comparison, baseline, systematic, criteria, controlled-convergence, objective]
- **Triggers**:
  - Multiple promising concepts
  - Need objective comparison
  - Want systematic evaluation
  - Avoiding favoritism
- **Description**: Compare concepts systematically against criteria using a reference baseline.
- **Process**:
  1. Define evaluation criteria
  2. Select a baseline concept (often current solution)
  3. Score each concept vs. baseline: + (better), S (same), - (worse)
  4. Sum positives and negatives
  5. Iterate: Combine strengths of top concepts
  6. Re-evaluate hybrid concepts
- **Key Questions**:
  - What criteria matter?
  - How does each concept compare to baseline on each criterion?
  - Can we combine strengths of top concepts?
  - What makes the winners better?
- **Outputs**: Comparison matrix, ranked concepts, hybrid concepts
- **Chains With**: WEIGHTED_CRITERIA, FEASIBILITY_DESIRABILITY_VIABILITY, IMPACT_VS_EFFORT

---

#### Method: WEIGHTED_CRITERIA
- **ID**: EV-006
- **Category**: EVALUATION
- **Tags**: [criteria, weights, priorities, scoring, stakeholders, alignment]
- **Triggers**:
  - Need explicit prioritization
  - Stakeholders disagree on importance
  - Want transparent evaluation
  - Multiple criteria matter
- **Description**: Assign importance weights to criteria and score each option to force explicit priority discussion.
- **Process**:
  1. List evaluation criteria
  2. Assign weights to each criterion (sum to 100)
  3. Score each option on each criterion (1-5 or 1-10)
  4. Calculate weighted scores
  5. Compare and discuss
- **Key Questions**:
  - What criteria matter?
  - How important is each criterion relative to others?
  - How does each option score on each criterion?
  - Does the weighted score match our intuition? If not, why?
- **Outputs**: Weighted scores, ranking, explicit priority discussions
- **Chains With**: PUGH_MATRIX, FEASIBILITY_DESIRABILITY_VIABILITY, STAKEHOLDER_POWER_MAPPING

---

#### Method: REAL_OPTIONS
- **ID**: EV-007
- **Category**: EVALUATION
- **Tags**: [options, flexibility, uncertainty, staged, learning, optionality]
- **Triggers**:
  - High uncertainty
  - Want to preserve flexibility
  - Staged investment possible
  - Learning value matters
- **Description**: Value the ability to learn and change course, not just expected outcomes.
- **Process**:
  1. Identify the decision and options
  2. Identify what you could learn before committing further
  3. Value the option to change course based on learning
  4. Prefer options that preserve future flexibility
  5. Stage investments to buy options
- **Key Questions**:
  - What options does this create or foreclose?
  - What could we learn before committing further?
  - What's the value of waiting and learning?
  - How can we stage this to preserve flexibility?
- **Outputs**: Option valuation, staged investment plan, flexibility-preserving decisions
- **Chains With**: MVE, ASSUMPTION_RISK_RANKING, REVERSIBILITY_ANALYSIS

---

#### Method: FEASIBILITY_DESIRABILITY_VIABILITY
- **ID**: EV-008
- **Category**: EVALUATION
- **Tags**: [three-lenses, holistic, technical, human, business, innovation]
- **Triggers**:
  - Need holistic evaluation
  - Ensuring multiple dimensions covered
  - Innovation validation
  - Cross-functional alignment
- **Description**: Evaluate ideas on three dimensions: Feasibility (can we build it?), Desirability (do people want it?), Viability (should we build it?).
- **Process**:
  1. Evaluate Feasibility (Technical):
     - Can we build this? Do we have or can we get the capabilities?
  2. Evaluate Desirability (Human):
     - Do people want this? Does it meet real needs?
  3. Evaluate Viability (Business):
     - Should we build this? Can it sustain a business model?
  4. Ideas must score well on all three
  5. Identify which dimension is weakest and address
- **Key Questions**:
  - Feasibility: Can we build it? What capabilities do we need?
  - Desirability: Do users want it? What need does it meet?
  - Viability: Can this sustain a business? What's the model?
  - Which dimension is weakest?
- **Outputs**: Three-dimension assessment, weakness identification, improvement priorities
- **Chains With**: BUSINESS_MODEL_CANVAS, PUGH_MATRIX, ASSUMPTION_RISK_RANKING

---

#### Method: KILL_CRITERIA
- **ID**: EV-009
- **Category**: EVALUATION
- **Tags**: [stopping, criteria, pre-commitment, discipline, sunk-cost, objectivity]
- **Triggers**:
  - Starting new initiative
  - Need to prevent escalation of commitment
  - Want objective go/no-go decisions
  - Avoiding sunk cost fallacy
- **Description**: Pre-commit to conditions that would stop the project, removing emotional attachment from later decisions.
- **Process**:
  1. Before starting, define kill criteria
  2. Specify measurable conditions that would stop the project
  3. Set checkpoints for evaluation
  4. At each checkpoint, evaluate honestly
  5. Kill or continue based on pre-committed criteria
- **Key Questions**:
  - Under what conditions should we stop?
  - What would prove this won't work?
  - What metric would trigger reconsideration?
  - When will we evaluate?
- **Outputs**: Kill criteria list, checkpoint schedule, objective stop conditions
- **Chains With**: ASSUMPTION_RISK_RANKING, MVE, FAILURE_MODE_ANALYSIS

---

#### Method: OPPORTUNITY_COST
- **ID**: EV-010
- **Category**: EVALUATION
- **Tags**: [tradeoffs, alternatives, resources, allocation, comparison, cost]
- **Triggers**:
  - Resources are constrained
  - Choices are mutually exclusive
  - Need to justify allocation
  - Comparing alternatives
- **Description**: Explicitly consider what else the resources could accomplish.
- **Process**:
  1. Identify the resources required (time, money, people, attention)
  2. List alternative uses for those resources
  3. Estimate value of best alternative use
  4. Compare value of proposed use to opportunity cost
  5. Decide if proposed use is truly best
- **Key Questions**:
  - What resources does this require?
  - What else could we do with those resources?
  - What's the best alternative use?
  - Is this better than the best alternative?
- **Outputs**: Alternative use analysis, opportunity cost estimate, comparative decision
- **Chains With**: PORTFOLIO_THINKING, IMPACT_VS_EFFORT, WEIGHTED_CRITERIA

---

#### Method: REVERSIBILITY_ANALYSIS
- **ID**: EV-011
- **Category**: EVALUATION
- **Tags**: [reversibility, risk, two-way-door, commitment, flexibility, recovery]
- **Triggers**:
  - High stakes decision
  - Uncertainty is high
  - Want to minimize downside
  - Assessing commitment level
- **Description**: Assess how easily a decision can be changed if it proves wrong.
- **Process**:
  1. Classify decision: One-way door (irreversible) or two-way door (reversible)?
  2. Estimate cost of reversal if wrong
  3. For irreversible decisions: Require more confidence
  4. For reversible decisions: Move faster, learn from doing
  5. Look for ways to make irreversible decisions more reversible
- **Key Questions**:
  - Can we undo this if wrong?
  - What would it cost to reverse?
  - How can we make this more reversible?
  - Is our confidence level appropriate for the reversibility?
- **Outputs**: Reversibility classification, reversal cost estimate, decision speed guidance
- **Chains With**: REAL_OPTIONS, REGRET_MINIMIZATION, KILL_CRITERIA

---

### TEAM_PROCESS Methods

#### Method: PSYCHOLOGICAL_SAFETY
- **ID**: TP-001
- **Category**: TEAM_PROCESS
- **Tags**: [safety, culture, trust, wild-ideas, no-penalty, openness]
- **Triggers**:
  - Team seems hesitant to share
  - Ideas are too safe
  - Need innovation culture
  - Fear of judgment blocks contribution
- **Description**: Create conditions where team members can share wild ideas without social penalty.
- **Process**:
  1. Model vulnerability — leader shares half-formed ideas
  2. Respond constructively to all ideas
  3. Separate idea from person when evaluating
  4. Celebrate productive failures
  5. Call out and discourage dismissive behavior
- **Key Questions**:
  - Do people feel safe sharing crazy ideas?
  - How do we respond when ideas fail?
  - Is judgment deferred during ideation?
  - Are all voices heard?
- **Outputs**: Increased idea flow, wilder ideas, more contribution
- **Chains With**: FAILURE_CELEBRATION, DIVERGENCE_CONVERGENCE, STRUCTURED_CRITIQUE

---

#### Method: DIVERGENCE_CONVERGENCE
- **ID**: TP-002
- **Category**: TEAM_PROCESS
- **Tags**: [process, separation, ideation, evaluation, phases, discipline]
- **Triggers**:
  - Ideas getting killed too early
  - Criticism mixing with generation
  - Need structured process
  - Want more and better ideas
- **Description**: Explicitly separate idea generation from evaluation into distinct phases.
- **Process**:
  1. Divergent phase: Generate many ideas, defer judgment, build on others
  2. Clear transition point
  3. Convergent phase: Evaluate, critique, select
  4. Never do both simultaneously
  5. Can cycle through multiple rounds
- **Key Questions**:
  - Are we diverging or converging now?
  - Has judgment been deferred during ideation?
  - Have we generated enough before evaluating?
  - Is the transition clear to everyone?
- **Outputs**: More ideas, better evaluation, clearer process
- **Chains With**: STRUCTURED_BRAINSTORMING, PSYCHOLOGICAL_SAFETY, TIME_BOXED_SPRINTS

---

#### Method: TIME_BOXED_SPRINTS
- **ID**: TP-003
- **Category**: TEAM_PROCESS
- **Tags**: [timeboxing, momentum, intensity, focus, deadlines, sprints]
- **Triggers**:
  - Work expanding to fill time
  - Need to maintain momentum
  - Want focused intensity
  - Avoiding perfectionism
- **Description**: Use short, intense, time-limited cycles to maintain momentum and focus.
- **Process**:
  1. Define sprint objective
  2. Set fixed time boundary (hours, days, not weeks)
  3. Work intensively within the timebox
  4. Stop at deadline regardless of completion
  5. Review, learn, set next sprint
- **Key Questions**:
  - What's the sprint objective?
  - What's the time boundary?
  - What's the minimum viable deliverable?
  - What did we learn?
- **Outputs**: Rapid progress, maintained momentum, frequent learning points
- **Chains With**: DESIGN_SPRINT, DIVERGENCE_CONVERGENCE, RETROSPECTIVES

---

#### Method: CROSS_FUNCTIONAL_TEAMS
- **ID**: TP-004
- **Category**: TEAM_PROCESS
- **Tags**: [diversity, disciplines, perspectives, groupthink, inclusion, outsiders]
- **Triggers**:
  - Building innovation team
  - Need diverse perspectives
  - Avoiding groupthink
  - Cross-disciplinary problem
- **Description**: Include diverse disciplines, backgrounds, and thinking styles on the team.
- **Process**:
  1. Identify disciplines relevant to the problem
  2. Include non-obvious disciplines (art, psychology, anthropology, etc.)
  3. Include "outsiders" who aren't domain experts
  4. Ensure cognitive diversity (thinking styles, not just demographics)
  5. Create conditions for all voices to contribute
- **Key Questions**:
  - What disciplines are relevant?
  - What perspectives are we missing?
  - Do we have cognitive diversity?
  - Are all voices being heard?
- **Outputs**: Diverse team composition, broader solution space, avoided groupthink
- **Chains With**: PSYCHOLOGICAL_SAFETY, ROLE_STORMING, SIX_THINKING_HATS

---

#### Method: FAILURE_CELEBRATION
- **ID**: TP-005
- **Category**: TEAM_PROCESS
- **Tags**: [failure, learning, culture, experimentation, risk-taking, celebration]
- **Triggers**:
  - Building innovation culture
  - Team risk-averse
  - Need to encourage experimentation
  - Learning from setbacks
- **Description**: Actively celebrate productive failures that generated learning.
- **Process**:
  1. Define "productive failure" — thoughtful experiment, clear learning
  2. Share failure stories openly
  3. Extract and document learnings
  4. Recognize individuals who took smart risks
  5. Distinguish from careless mistakes
- **Key Questions**:
  - What did we learn from this failure?
  - Was this a thoughtful experiment or carelessness?
  - How can we share this learning?
  - How do we recognize smart risk-taking?
- **Outputs**: Learning from failures, reduced fear, increased experimentation
- **Chains With**: PSYCHOLOGICAL_SAFETY, RETROSPECTIVES, MVE

---

#### Method: STRUCTURED_CRITIQUE
- **ID**: TP-006
- **Category**: TEAM_PROCESS
- **Tags**: [feedback, constructive, specific, protocol, improvement, safety]
- **Triggers**:
  - Feedback becomes personal
  - Critique is unproductive
  - Need constructive input
  - Protecting relationships
- **Description**: Use formal protocols to ensure feedback is constructive, specific, and separated from presenter.
- **Process**:
  1. Presenter shares concept
  2. Clarifying questions only (no judgment)
  3. Use format: "I like..." "I wish..." "What if...?"
  4. Focus on concept, not presenter
  5. Presenter collects feedback, doesn't defend
- **Key Questions**:
  - What do I like about this?
  - What do I wish were different?
  - What if we tried...?
  - How can this be improved?
- **Outputs**: Constructive feedback, improved concepts, maintained relationships
- **Chains With**: PSYCHOLOGICAL_SAFETY, DIVERGENCE_CONVERGENCE, PUGH_MATRIX

---

#### Method: RETROSPECTIVES
- **ID**: TP-007
- **Category**: TEAM_PROCESS
- **Tags**: [learning, reflection, improvement, documentation, process, meta]
- **Triggers**:
  - After project or sprint
  - Building organizational learning
  - Improving process
  - Capturing knowledge
- **Description**: Systematically extract and share lessons from each project or sprint.
- **Process**:
  1. What went well? (Keep doing)
  2. What didn't go well? (Stop or change)
  3. What surprised us?
  4. What did we learn?
  5. What will we do differently next time?
  6. Document and share
- **Key Questions**:
  - What went well?
  - What didn't go well?
  - What surprised us?
  - What will we do differently?
  - How do we share this learning?
- **Outputs**: Lessons learned, process improvements, organizational learning
- **Chains With**: FAILURE_CELEBRATION, TIME_BOXED_SPRINTS, INNOVATION_METRICS

---

### STRATEGIC Methods

#### Method: BLUE_OCEAN
- **ID**: ST-001
- **Category**: STRATEGIC
- **Tags**: [uncontested, new-market, value-innovation, differentiation, competition, strategy]
- **Triggers**:
  - Industry competition is intense
  - Margins compressed
  - Competing on same dimensions
  - Seeking new market space
- **Description**: Seek uncontested market space by reconstructing value rather than competing in existing markets.
- **Process**:
  1. Map current industry competitive factors
  2. Apply Eliminate-Reduce-Raise-Create grid:
     - Eliminate: What factors should be eliminated?
     - Reduce: What should be reduced below industry standard?
     - Raise: What should be raised above industry standard?
     - Create: What should be created that industry never offered?
  3. Design new value curve
  4. Target non-customers
- **Key Questions**:
  - What does the industry compete on?
  - What can be eliminated that customers don't value?
  - What can be reduced?
  - What can be raised?
  - What new factors can we create?
  - Who are the non-customers?
- **Outputs**: Value curve, ERRC grid, blue ocean strategy
- **Chains With**: DISRUPTIVE_INNOVATION, VALUE_CHAIN, JOBS_TO_BE_DONE

---

#### Method: DISRUPTIVE_INNOVATION
- **ID**: ST-002
- **Category**: STRATEGIC
- **Tags**: [disruption, low-end, new-market, simpler, cheaper, overlooked]
- **Triggers**:
  - Incumbents adding features customers don't value
  - Overlooked segments exist
  - Non-consumption is high
  - Seeking strategic entry point
- **Description**: Identify opportunities to serve overlooked segments with simpler, cheaper solutions that can improve over time.
- **Process**:
  1. Identify over-served customers (paying for features they don't use)
  2. Identify non-consumers (can't access current solutions)
  3. Design simpler, cheaper, more accessible solution
  4. Target overlooked segment initially
  5. Improve over time, moving up market
- **Key Questions**:
  - Who is over-served by current solutions?
  - Who can't access current solutions?
  - What would a "good enough" solution look like?
  - How could we improve over time?
  - Why won't incumbents respond?
- **Outputs**: Target segment, simplified value proposition, improvement trajectory
- **Chains With**: EXTREME_USER_ANALYSIS, BLUE_OCEAN, S_CURVE_ANALYSIS

---

#### Method: BUSINESS_MODEL_CANVAS
- **ID**: ST-003
- **Category**: STRATEGIC
- **Tags**: [business-model, canvas, value, revenue, nine-blocks, holistic]
- **Triggers**:
  - Innovation requires new business model
  - Need holistic view
  - Testing model assumptions
  - Communicating strategy
- **Description**: Map the full business model to ensure innovation addresses all elements.
- **Process**:
  1. Complete nine building blocks:
     - Customer Segments: Who are we creating value for?
     - Value Propositions: What value do we deliver?
     - Channels: How do we reach customers?
     - Customer Relationships: What relationships do we establish?
     - Revenue Streams: How do we capture value?
     - Key Resources: What assets are essential?
     - Key Activities: What must we do well?
     - Key Partnerships: Who helps us?
     - Cost Structure: What are the major costs?
  2. Identify assumptions in each block
  3. Test riskiest assumptions
- **Key Questions**:
  - (See each of nine blocks above)
  - What assumptions are we making?
  - Which assumptions are riskiest?
- **Outputs**: Business model canvas, assumption inventory, test priorities
- **Chains With**: FEASIBILITY_DESIRABILITY_VIABILITY, VALUE_CHAIN, JOBS_TO_BE_DONE

---

#### Method: VALUE_CHAIN_ANALYSIS
- **ID**: ST-004
- **Category**: STRATEGIC
- **Tags**: [value-chain, activities, primary, support, competitive-advantage, systemic]
- **Triggers**:
  - Seeking systemic improvement
  - Understanding value creation
  - Identifying strategic position
  - Analyzing industry structure
- **Description**: Map all activities from raw inputs to end customer to identify where value is created and captured.
- **Process**:
  1. Map primary activities (inbound logistics, operations, outbound logistics, marketing/sales, service)
  2. Map support activities (infrastructure, HR, technology, procurement)
  3. Identify where value is created
  4. Identify where value is destroyed
  5. Find opportunities for improvement or repositioning
- **Key Questions**:
  - What are all the activities in the chain?
  - Where is value created?
  - Where is value destroyed or leaked?
  - Where should we play?
  - How can we reconfigure the chain?
- **Outputs**: Value chain map, value creation/destruction points, strategic options
- **Chains With**: ECOSYSTEM_MAPPING, BUSINESS_MODEL_CANVAS, SYSTEMS_MAPPING

---

#### Method: ECOSYSTEM_MAPPING
- **ID**: ST-005
- **Category**: STRATEGIC
- **Tags**: [ecosystem, players, complementors, competitors, influencers, network]
- **Triggers**:
  - Success depends on others
  - Need to understand industry dynamics
  - Planning partnership strategy
  - Identifying opportunities
- **Description**: Identify all players who influence or are influenced by the solution.
- **Process**:
  1. Map all ecosystem players:
     - Competitors (direct and indirect)
     - Complementors (whose products increase value of ours)
     - Suppliers
     - Customers (segments)
     - Regulators
     - Influencers
  2. Map relationships and dependencies
  3. Identify power dynamics
  4. Find opportunities and threats
- **Key Questions**:
  - Who are all the players in this ecosystem?
  - Who are our complementors?
  - What are the dependencies?
  - Where is power concentrated?
  - What ecosystem changes would benefit us?
- **Outputs**: Ecosystem map, relationship analysis, strategic opportunities
- **Chains With**: STAKEHOLDER_POWER_MAPPING, SYSTEMS_MAPPING, VALUE_CHAIN

---

#### Method: TECHNOLOGY_ROADMAPPING
- **ID**: ST-006
- **Category**: STRATEGIC
- **Tags**: [roadmap, technology, planning, long-term, alignment, trajectory]
- **Triggers**:
  - Planning multi-year investments
  - Aligning technology with market
  - Communicating strategy
  - Coordinating development
- **Description**: Align technology development with market opportunities over time.
- **Process**:
  1. Map market/customer needs over time (top layer)
  2. Map products/services that address needs (middle layer)
  3. Map technologies/capabilities required (bottom layer)
  4. Draw connections showing dependencies
  5. Identify gaps and priorities
- **Key Questions**:
  - What market needs are emerging over time?
  - What products will address those needs?
  - What technologies do those products require?
  - What capabilities must we build?
  - What's the timeline?
- **Outputs**: Technology roadmap, capability gaps, investment priorities
- **Chains With**: S_CURVE_ANALYSIS, SCENARIO_PLANNING, PORTFOLIO_THINKING

---

#### Method: ADOPTION_CURVE_PLANNING
- **ID**: ST-007
- **Category**: STRATEGIC
- **Tags**: [adoption, diffusion, segments, innovators, mainstream, crossing-chasm]
- **Triggers**:
  - Planning go-to-market
  - Understanding adoption dynamics
  - Targeting customer segments
  - Timing market entry
- **Description**: Plan for different segments adopting at different times with different needs.
- **Process**:
  1. Identify adopter segments:
     - Innovators (2.5%): Want newest, tolerate imperfection
     - Early Adopters (13.5%): Want advantage, willing to take risk
     - Early Majority (34%): Want proven solutions, pragmatic
     - Late Majority (34%): Want standards, skeptical
     - Laggards (16%): Want traditional, resistant
  2. Design value proposition for each segment
  3. Plan crossing from early market to mainstream
  4. Identify segment-specific barriers and enablers
- **Key Questions**:
  - Which segment are we targeting now?
  - What does each segment need to adopt?
  - How will we cross from early adopters to mainstream?
  - What references/proof do later segments need?
- **Outputs**: Segment-specific strategies, crossing-the-chasm plan, adoption timeline
- **Chains With**: DEMAND_SIDE_ANALYSIS, JOBS_TO_BE_DONE, DISRUPTIVE_INNOVATION

---

### HUMAN_CENTERED Methods

#### Method: EMPATHY_MAPPING
- **ID**: HC-001
- **Category**: HUMAN_CENTERED
- **Tags**: [empathy, user, says, thinks, feels, does, needs]
- **Triggers**:
  - Starting to understand users
  - Need shared user understanding
  - Want to capture emotional dimension
  - Synthesizing user research
- **Description**: Capture what users say, think, feel, and do to reveal gaps between stated and actual needs.
- **Process**:
  1. Create four quadrants: Says, Thinks, Feels, Does
  2. Based on research, fill in each quadrant
  3. Look for contradictions (says vs. does)
  4. Identify pains and gains
  5. Generate needs/insights
- **Key Questions**:
  - What does the user say?
  - What might they think? (Even if not said)
  - How do they feel?
  - What do they actually do?
  - Where are the contradictions?
- **Outputs**: Empathy map, identified contradictions, user insights, need statements
- **Chains With**: JOBS_TO_BE_DONE, PERSONA_DEVELOPMENT, USER_JOURNEY_MAPPING

---

#### Method: USER_JOURNEY_MAPPING
- **ID**: HC-002
- **Category**: HUMAN_CENTERED
- **Tags**: [journey, touchpoints, experience, pain-points, moments-of-truth, end-to-end]
- **Triggers**:
  - Improving existing experience
  - Designing new experience
  - Finding pain points
  - Understanding full context
- **Description**: Document the complete experience across all touchpoints and time.
- **Process**:
  1. Define the journey scope (start and end points)
  2. Identify all stages of the journey
  3. Map touchpoints at each stage
  4. Document user actions, thoughts, emotions at each touchpoint
  5. Identify pain points and moments of truth
  6. Find opportunities
- **Key Questions**:
  - What are all the stages of the journey?
  - What happens at each touchpoint?
  - How does the user feel at each stage?
  - Where are the pain points?
  - What are the moments of truth?
- **Outputs**: Journey map, pain point inventory, opportunity areas
- **Chains With**: EMPATHY_MAPPING, STORYBOARDING, DEMAND_SIDE_ANALYSIS

---

#### Method: PERSONA_DEVELOPMENT
- **ID**: HC-003
- **Category**: HUMAN_CENTERED
- **Tags**: [persona, archetype, user-segment, concrete, memorable, shared-understanding]
- **Triggers**:
  - Need shared understanding of users
  - Making abstract segments concrete
  - Guiding design decisions
  - Communicating user insights
- **Description**: Create archetypical users based on research to make segments concrete and memorable.
- **Process**:
  1. Synthesize user research into patterns
  2. Identify distinct user archetypes
  3. Create persona for each archetype:
     - Name, photo, demographic details
     - Goals, motivations, frustrations
     - Behaviors, attitudes, context
     - Quote that captures essence
  4. Validate personas with stakeholders
  5. Use personas to guide decisions
- **Key Questions**:
  - What distinct user types exist?
  - What characterizes each type?
  - What are their goals and frustrations?
  - How do we make them memorable?
- **Outputs**: Persona profiles, shared user understanding, decision-making guide
- **Chains With**: EMPATHY_MAPPING, JOBS_TO_BE_DONE, USER_JOURNEY_MAPPING

---

#### Method: CO_CREATION
- **ID**: HC-004
- **Category**: HUMAN_CENTERED
- **Tags**: [co-creation, participatory, workshop, users, collaboration, involvement]
- **Triggers**:
  - Solutions require user acceptance
  - Users have valuable insights
  - Behavior change needed
  - Building ownership
- **Description**: Involve users directly in generating and refining solutions.
- **Process**:
  1. Recruit representative users
  2. Design co-creation activity (workshop, session)
  3. Provide stimulus and constraints
  4. Facilitate user generation of ideas and solutions
  5. Build on and synthesize user contributions
- **Key Questions**:
  - How can we involve users in creating solutions?
  - What stimulus will help users contribute?
  - What did users generate that we wouldn't have?
  - How do we build on their contributions?
- **Outputs**: User-generated ideas, deeper user insights, increased user buy-in
- **Chains With**: PERSONA_DEVELOPMENT, PROTOTYPING, USABILITY_TESTING

---

#### Method: USABILITY_TESTING
- **ID**: HC-005
- **Category**: HUMAN_CENTERED
- **Tags**: [usability, testing, observation, friction, confusion, validation]
- **Triggers**:
  - Have prototype or product
  - Need to validate usability
  - Finding friction points
  - Before or after launch
- **Description**: Observe users attempting tasks to reveal friction and confusion.
- **Process**:
  1. Define tasks to test
  2. Recruit representative users
  3. Observe users attempting tasks (think-aloud protocol)
  4. Note where users struggle, make errors, express confusion
  5. Quantify if needed (success rate, time, errors)
  6. Prioritize fixes
- **Key Questions**:
  - Can users complete the task?
  - Where do they struggle?
  - What confuses them?
  - What did they expect to happen?
  - How severe are the problems?
- **Outputs**: Usability issues, severity ranking, improvement priorities
- **Chains With**: PROTOTYPING, PAPER_PROTOTYPING, A_B_TESTING

---

### EMERGING Methods

#### Method: GENERATIVE_AI_IDEATION
- **ID**: EM-001
- **Category**: EMERGING
- **Tags**: [AI, LLM, volume, combination, critique, automation, scale]
- **Triggers**:
  - Need high volume of ideas
  - Want to explore vast space
  - Rapid iteration needed
  - Augmenting human ideation
- **Description**: Use large language models to generate, combine, and critique ideas at scale.
- **Process**:
  1. Frame the problem for AI
  2. Generate many ideas using AI
  3. Have AI combine and mutate ideas
  4. Use AI to critique and find weaknesses
  5. Human curation and development of best ideas
- **Key Questions**:
  - How should we frame this for AI?
  - What variations should we ask for?
  - What critique should AI provide?
  - Which AI-generated ideas merit human development?
- **Outputs**: Large idea set, combinations, critique analysis, curated shortlist
- **Chains With**: STRUCTURED_BRAINSTORMING, MORPHOLOGICAL_ANALYSIS, EVALUATION methods

---

#### Method: SPECULATIVE_DESIGN
- **ID**: EM-002
- **Category**: EMERGING
- **Tags**: [speculation, futures, provocation, fiction, critical, long-term]
- **Triggers**:
  - Exploring long-term implications
  - Challenging assumptions
  - Provoking discussion
  - Imagining alternative futures
- **Description**: Create artifacts from imagined futures to provoke discussion and challenge assumptions.
- **Process**:
  1. Define a future scenario (10, 50, 100 years)
  2. Create artifacts as if they exist in that future (products, ads, news articles)
  3. Present artifacts to provoke discussion
  4. Explore implications and assumptions
  5. Bring insights back to present decisions
- **Key Questions**:
  - What might the future look like?
  - What artifacts would exist there?
  - What assumptions does this reveal?
  - What should we do differently now?
  - What future do we want to create/avoid?
- **Outputs**: Speculative artifacts, provoked discussion, challenged assumptions, strategic insights
- **Chains With**: TIME_TRAVEL, SCENARIO_PLANNING, THOUGHT_EXPERIMENTS

---

#### Method: LEAN_STARTUP
- **ID**: EM-003
- **Category**: EMERGING
- **Tags**: [lean, MVP, pivot, validated-learning, build-measure-learn, iteration]
- **Triggers**:
  - Operating under extreme uncertainty
  - Need rapid learning
  - Resource-constrained
  - Startup or new venture
- **Description**: Use Build-Measure-Learn cycles with Minimum Viable Products to achieve validated learning.
- **Process**:
  1. Identify riskiest assumption
  2. Build MVP to test that assumption
  3. Measure results
  4. Learn: Validate or invalidate assumption
  5. Decide: Pivot (change strategy) or persevere
  6. Repeat cycle
- **Key Questions**:
  - What's our riskiest assumption?
  - What's the minimum we can build to test it?
  - What will we measure?
  - What did we learn?
  - Pivot or persevere?
- **Outputs**: Validated/invalidated assumptions, learning, pivot/persevere decision
- **Chains With**: MVE, ASSUMPTION_RISK_RANKING, PRETOTYPING

---

#### Method: DESIGN_SPRINT
- **ID**: EM-004
- **Category**: EMERGING
- **Tags**: [sprint, five-days, rapid, structured, prototype, test]
- **Triggers**:
  - Need rapid progress
  - Defined challenge
  - Cross-functional team available
  - Time-boxed innovation needed
- **Description**: Five-day structured process from problem to tested prototype.
- **Process**:
  1. Monday: Map problem, pick target
  2. Tuesday: Sketch competing solutions
  3. Wednesday: Decide on best solution, storyboard
  4. Thursday: Build realistic prototype
  5. Friday: Test with real users
- **Key Questions**:
  - What's the sprint challenge?
  - What solutions emerged?
  - What did the prototype reveal?
  - What did users tell us?
  - What's the next step?
- **Outputs**: Tested prototype, user feedback, validated/invalidated concepts, clear next steps
- **Chains With**: TIME_BOXED_SPRINTS, PROTOTYPING, USABILITY_TESTING

---

#### Method: BACKCASTING
- **ID**: EM-005
- **Category**: EMERGING
- **Tags**: [future, backward, goals, pathway, steps, vision]
- **Triggers**:
  - Setting ambitious long-term goals
  - Creating roadmaps
  - Vision-driven planning
  - Identifying necessary steps
- **Description**: Start from a desired future state and work backward to identify necessary steps.
- **Process**:
  1. Define desired future state vividly
  2. Assume the future state has been achieved
  3. Work backward: What step immediately preceded this state?
  4. Continue backward to present
  5. Sequence steps forward into roadmap
- **Key Questions**:
  - What does success look like?
  - What had to happen just before that?
  - What had to happen before that?
  - What's the first step from today?
  - What's the pathway?
- **Outputs**: Future vision, backward sequence, forward roadmap, milestone identification
- **Chains With**: SCENARIO_PLANNING, TECHNOLOGY_ROADMAPPING, TIME_TRAVEL

---

#### Method: EFFECTUATION
- **ID**: EM-006
- **Category**: EMERGING
- **Tags**: [entrepreneurial, means, uncertainty, contingency, co-creation, affordable-loss]
- **Triggers**:
  - High uncertainty
  - Limited resources
  - Entrepreneurial context
  - Cannot predict future
- **Description**: Use expert entrepreneur logic: start with means, embrace uncertainty, leverage contingencies.
- **Process**:
  1. Start with means: Who am I? What do I know? Whom do I know?
  2. Focus on affordable loss, not expected return
  3. Embrace contingencies as opportunities
  4. Co-create with stakeholders
  5. Shape the future rather than predict it
- **Key Questions**:
  - What means do I have? (identity, knowledge, network)
  - What can I afford to lose?
  - How can I turn this surprise into opportunity?
  - Who can co-create with me?
  - How can I shape the future?
- **Outputs**: Means inventory, affordable loss boundary, contingency leverage, co-creation opportunities
- **Chains With**: LEAN_STARTUP, RESOURCES_ANALYSIS, STAKEHOLDER_POWER_MAPPING

---

## Method Selection Logic

Use these rules to select appropriate methods:

### By Phase

**When framing the problem:**
- Start with: FIVE_WHYS, JOBS_TO_BE_DONE, PROBLEM_REFRAMING
- If system is complex: SYSTEMS_MAPPING, STAKEHOLDER_POWER_MAPPING
- If user behavior is unclear: ETHNOGRAPHIC_OBSERVATION, EXTREME_USER_ANALYSIS
- If constraints dominate: CONSTRAINT_SURFACING, FIRST_PRINCIPLES

**When generating ideas:**
- Start with: STRUCTURED_BRAINSTORMING, SCAMPER, ANALOGICAL_REASONING
- If seeking volume: MORPHOLOGICAL_ANALYSIS, GENERATIVE_AI_IDEATION
- If stuck: FORCED_CONNECTIONS, NEGATIVE_BRAINSTORMING, WORST_POSSIBLE_IDEA
- If seeking breakthrough: TRIZ, CONTRADICTION_MAPPING, CONCEPT_BLENDING

**When testing ideas:**
- Start with: MVE, PROTOTYPING, PRETOTYPING
- If experience-focused: STORYBOARDING, BODYSTORMING
- If uncertain future: SCENARIO_PLANNING, FAILURE_MODE_ANALYSIS
- If rapid progress needed: DESIGN_SPRINT

**When selecting ideas:**
- Start with: IMPACT_VS_EFFORT, ASSUMPTION_RISK_RANKING
- If multiple promising options: PUGH_MATRIX, WEIGHTED_CRITERIA
- If high uncertainty: REAL_OPTIONS, REVERSIBILITY_ANALYSIS
- If strategic alignment needed: FEASIBILITY_DESIRABILITY_VIABILITY, PORTFOLIO_THINKING

### By Situation

**"We keep getting the same solutions":**
→ ASSUMPTION_REVERSAL, FORCED_CONNECTIONS, CONSTRAINT_INJECTION, LATERAL_THINKING

**"We're facing a tradeoff we can't resolve":**
→ TRIZ, CONTRADICTION_MAPPING, FIRST_PRINCIPLES, IDEAL_FINAL_RESULT

**"We don't know what users want":**
→ ETHNOGRAPHIC_OBSERVATION, JOBS_TO_BE_DONE, PRETOTYPING, CO_CREATION

**"We have too many ideas and can't choose":**
→ PUGH_MATRIX, ASSUMPTION_RISK_RANKING, IMPACT_VS_EFFORT, KILL_CRITERIA

**"The team is stuck or blocked":**
→ INCUBATION, RANDOM_STIMULUS, ROLE_STORMING, SIX_THINKING_HATS

**"We need strategic direction":**
→ BLUE_OCEAN, DISRUPTIVE_INNOVATION, S_CURVE_ANALYSIS, TECHNOLOGY_ROADMAPPING

**"Resources are very limited":**
→ ASIT, TRIMMING, RESOURCES_ANALYSIS, MVE, EFFECTUATION

**"We're entering a new market":**
→ ADOPTION_CURVE_PLANNING, ECOSYSTEM_MAPPING, DEMAND_SIDE_ANALYSIS

---

## Output Formats

When applying methods, structure outputs consistently:

### Problem Statement
```
PROBLEM: [Clear statement of the problem]
CONTEXT: [Relevant background]
CONSTRAINTS: [Real constraints]
ASSUMPTIONS: [Assumptions being made]
SUCCESS CRITERIA: [What would success look like]
```

### Idea Description
```
IDEA: [Concise name]
DESCRIPTION: [What it is and how it works]
VALUE: [What benefit it provides]
FEASIBILITY: [High/Medium/Low with rationale]
KEY ASSUMPTIONS: [What must be true]
NEXT STEP: [How to validate or develop]
```

### Method Application Result
```
METHOD: [Method name]
INPUT: [What was used as input]
PROCESS: [Key steps taken]
OUTPUT: [What was generated]
INSIGHTS: [Key learnings]
NEXT METHODS: [Recommended follow-on methods]
```

### Decision Record
```
DECISION: [What was decided]
OPTIONS CONSIDERED: [Alternatives evaluated]
CRITERIA: [How options were evaluated]
RATIONALE: [Why this option was chosen]
RISKS: [Known risks with mitigation]
NEXT STEPS: [Actions to take]
```

---

## End of Document
