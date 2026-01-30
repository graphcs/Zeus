# Zeus V0 Architecture and Design

**Version:** 0.3 (Implemented)  
**Date:** 2026-01-30  

This document describes the implemented architecture for Zeus V0 (Bounded Critique-Led Solver).

---

## 1. Component Architecture

Zeus V0 follows a modular controller-based architecture. The `RunController` acts as the central orchestrator, managing the lifecycle of a request by delegating to specialized stateless components.

```mermaid
classDiagram
    class RunController {
        +run(request)
        -_execute_pipeline(request, record)
        -_check_budget()
    }

    class Normalizer {
        +normalize(request) NormalizedProblem
    }

    class Planner {
        +plan(problem) Plan
    }

    class Generator {
        +generate(problem, plan) Candidate
        +revise(candidate, critique) Candidate
    }

    class Critic {
        +critique(candidate, problem) Critique
    }

    class Assembler {
        +assemble(record) ZeusResponse
    }

    class Persistence {
        +save(record)
        +load(run_id)
    }

    class OpenRouterClient {
        +generate_json()
    }

    RunController --> Normalizer : uses
    RunController --> Planner : uses
    RunController --> Generator : uses
    RunController --> Critic : uses
    RunController --> Assembler : uses
    RunController --> Persistence : uses
    
    Normalizer ..> OpenRouterClient
    Planner ..> OpenRouterClient
    Generator ..> OpenRouterClient
    Critic ..> OpenRouterClient
```

### Component Roles

1.  **RunController (`core/run_controller.py`)**:
    *   **Responsibility**: Orchestrates the workflow, enforces budgets (LLM calls, timeouts), manages state (RunRecord), and ensures invariants (e.g., critique always runs).
    *   **Key Invariants**: Max 1 revision loop, traceability of all runs.

2.  **Normalizer (`core/normalizer.py`)**:
    *   **Responsibility**: Converts raw user input (`ZeusRequest`) into a structured `NormalizedProblem`.
    *   **Key Logic**: Ensures constraints are never dropped, merges user and implied constraints.

3.  **Planner (`core/planner.py`)**:
    *   **Responsibility**: Decomposes the problem into a linear sequence of steps (`Plan`).
    *   **Key Logic**: Generates distinct steps for analysis, generation, and verification.

4.  **Generator (`core/generator.py`)**:
    *   **Responsibility**: Produces the actual content (`Candidate`) based on the plan.
    *   **Key Logic**: Supports both initial generation and revision based on critique.

5.  **Critic (`core/critic.py`)**:
    *   **Responsibility**: provides multi-view feedback (`Critique`).
    *   **Key Logic**: Enforces coverage of 6 key perspectives (scope, architecture, risk, security, compliance, evaluation) in a single LLM call.

6.  **Assembler (`core/assembler.py`)**:
    *   **Responsibility**: Formats the final output (`ZeusResponse`).
    *   **Key Logic**: Calculates costs/usage and ensures `assumptions` and `known_issues` are always present.

7.  **Persistence (`core/persistence.py`)**:
    *   **Responsibility**: Handles disk I/O for `RunRecords`.
    *   **Key Logic**: Append-only JSON storage.

---

## 2. Sequence Diagram (Run Lifecycle)

This sequence diagram illustrates the execution flow within `RunController.run()`.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI
    participant RC as RunController
    participant N as Normalizer
    participant P as Planner
    participant G as Generator
    participant C as Critic
    participant A as Assembler
    participant DB as Persistence

    User->>UI: run zeus (brief/solution)
    UI->>RC: run(ZeusRequest)
    
    activate RC
    RC->>RC: Init RunRecord
    
    %% Phase 1: Normalize
    RC->>N: normalize(request)
    activate N
    N-->>RC: NormalizedProblem
    deactivate N
    
    %% Phase 2: Plan
    RC->>P: plan(problem)
    activate P
    P-->>RC: Plan
    deactivate P
    
    %% Phase 3: Generate V1
    RC->>G: generate(problem, plan)
    activate G
    G-->>RC: Candidate v1
    deactivate G
    
    %% Phase 4: Critique V1
    RC->>C: critique(candidate_v1)
    activate C
    C-->>RC: Critique v1
    deactivate C
    
    %% Phase 5: Revision Loop (Conditional)
    opt If Blocker/Major Issues & Budget Allows
        RC->>G: revise(candidate_v1, critique_v1)
        activate G
        G-->>RC: Candidate v2
        deactivate G
        
        RC->>C: critique(candidate_v2)
        activate C
        C-->>RC: Critique v2
        deactivate C
    end
    
    %% Phase 6: Assemble
    RC->>A: assemble(record)
    activate A
    A-->>RC: ZeusResponse
    deactivate A
    
    %% Logging (Finally block)
    RC->>DB: save(record)
    activate DB
    DB-->>RC: saved path
    deactivate DB
    
    RC-->>UI: ZeusResponse
    deactivate RC
    UI-->>User: Output MD + Assumptions + Issues
```
