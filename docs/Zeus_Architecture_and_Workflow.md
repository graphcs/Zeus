# Zeus Agent - Architecture and Workflow

This document provides a comprehensive analysis of the Zeus Agent project, including system design, workflow, model selection, and data flow.

## 1. System Overview

Zeus Agent (Capital Squared Dashboard) is a multi-agent, 7-phase pipeline designed to solve complex business and technology problems. It takes a problem brief, constraints, and objectives, and uses parallel LLM-powered "inventors" to generate divergent solutions. These solutions are then cross-pollinated, synthesized, critiqued against predefined libraries (First Principles, Mental Models, Technologies, etc.), refined iteratively, and finally assembled into a comprehensive set of deliverables.

The system is built with a Streamlit frontend (`ui.py`) and a robust asynchronous backend (`src/core/run_controller.py`) that orchestrates the pipeline using the OpenRouter API for LLM calls.

---

## 2. System Architecture

The architecture follows a modular, decoupled design where the `RunController` orchestrates various core components.

```mermaid
graph TD

    subgraph Frontend
        UI["Streamlit UI"]
    end

    subgraph Orchestration
        RC["RunController"]
    end

    subgraph CoreModules ["Core Modules"]
        N["Normalizer<br/>Phase 0"]
        I["Inventor<br/>Phase 1 & 2"]
        S["Synthesizer<br/>Phase 3"]
        LC["Library Critic<br/>Phase 4"]
        R["Refiner<br/>Phase 5"]
        A["Assembler<br/>Phase 6"]
    end

    subgraph Infrastructure
        LLM["OpenRouterClient"]
        LL["LibraryLoader"]
        P["Persistence"]
    end

    subgraph Storage
        FS["File System<br/>run_records/"]
        Docs["Library Docs<br/>docs/updated-docs/"]
    end

    UI -->|ZeusRequest| RC
    RC --> N
    RC --> I
    RC --> S
    RC --> LC
    RC --> R
    RC --> A

    N -.-> LLM
    I -.-> LLM
    S -.-> LLM
    LC -.-> LLM
    R -.-> LLM
    A -.-> LLM

    I -.-> LL
    S -.-> LL
    LC -.-> LL
    R -.-> LL

    LL -.-> Docs
    RC -->|RunRecord| P
    P -.-> FS
```

---

## 3. Pipeline Workflow

The Zeus pipeline consists of 7 distinct phases. The pipeline is designed to be resilient; if a phase fails, the system attempts a best-effort assembly of the outputs generated so far.

```mermaid
graph TD
    Start("User Input: Prompt, Constraints, Objectives") --> P0

    subgraph Phase0 ["Phase 0: Intake"]
        P0["Normalizer"] -->|Normalizes input into| PB("ProblemBrief")
    end

    subgraph Phase1 ["Phase 1: Divergent Generation"]
        PB --> I1["Inventor A<br>Foundational"]
        PB --> I2["Inventor B<br>Competitive"]
        PB --> I3["Inventor C<br>Comprehensive"]
        PB --> I4["Inventor D<br>Tabula Rasa"]
        I1 --> IS
        I2 --> IS
        I3 --> IS
        I4 --> IS
        IS("InventorSolutions")
    end

    subgraph Phase2 ["Phase 2: Cross-Pollination"]
        IS -->|Optional| CP["Cross-Critique"]
        CP --> CC("CrossCritiques")
    end

    subgraph Phase3 ["Phase 3: Convergent Synthesis"]
        IS --> S1["Synthesizer"]
        CC --> S1
        S1 -->|Merges ideas| SR("SynthesisResult<br>Unified Draft")
    end

    subgraph Phase4 ["Phase 4: Library-Informed Critique"]
        SR --> LC1["Critic: First Principles"]
        SR --> LC2["Critic: Mental Models"]
        SR --> LC3["Critic: Technologies"]
        LC1 --> LCR
        LC2 --> LCR
        LC3 --> LCR
        LCR("LibraryCritiqueResult")
    end

    subgraph Phase5 ["Phase 5: Iterative Refinement"]
        SR --> R1{"Issues Found?"}
        LCR --> R1
        R1 -- Yes --> R2["Refiner"]
        R2 -->|Fixes Blockers/Majors| R3{"Budget/Revisions Left?"}
        R3 -- Yes --> LC_Re["Re-Critique"]
        LC_Re --> R1
        R3 -- No --> FD("Final Draft")
        R1 -- No --> FD
    end

    subgraph Phase6 ["Phase 6: Output Assembly"]
        FD --> A1["Assembler"]
        A1 -->|Generates 5 Deliverables| ZR("ZeusResponse")
    end

    ZR --> End("Final Output & Scorecard")
```

---

## 4. Phase Model Selection

Zeus allows granular control over which LLM model is used for each phase. This is configured in the UI and passed to the `RunController` via `model_overrides`.

| Phase | Component | Default Model | Purpose |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Normalizer | `anthropic/claude-sonnet-4` | Structuring and classifying the raw user input. |
| **Phase 1** | Inventor | `anthropic/claude-sonnet-4` | Creative, divergent generation of solutions based on assigned libraries. |
| **Phase 2** | Cross-Pollination | `anthropic/claude-sonnet-4` | Analyzing and critiquing peer solutions. |
| **Phase 3** | Synthesizer | `anthropic/claude-sonnet-4` | Merging multiple solutions, resolving conflicts, and tracking provenance. |
| **Phase 4** | Library Critic | `anthropic/claude-sonnet-4` | Strict evaluation of the draft against specific library principles. |
| **Phase 5** | Refiner | `anthropic/claude-sonnet-4` | Iteratively fixing identified blockers and major issues. |
| **Phase 6** | Assembler | `anthropic/claude-sonnet-4` | Formatting the final deliverables and generating the self-evaluation scorecard. |

*Note: The system uses `OpenRouterClient` which supports fallback and retry mechanisms for rate limits and timeouts.*

---

## 5. Data Flow & Schemas

Data is strictly typed using Pydantic models (`src/models/schemas.py`). The `RunRecord` acts as a central state object that accumulates data as it passes through the pipeline.

```mermaid
classDiagram
    class ZeusRequest {
        +String prompt
        +List constraints
        +List objectives
        +Int num_inventors
    }
    
    class ProblemBrief {
        +String problem_statement
        +ProblemClassification classification
        +List implicit_assumptions
    }
    
    class InventorSolution {
        +String inventor_id
        +String content
        +List assumptions
    }
    
    class SynthesisResult {
        +String unified_draft
        +List provenance
        +List resolved_conflicts
    }
    
    class LibraryCritiqueResult {
        +List findings
        +Int blocker_count
        +Int major_count
    }
    
    class ZeusResponse {
        +String executive_summary
        +String solution_design_document
        +String foundation_documentation
        +String self_evaluation_scorecard
        +String run_log
        +Float total_score
    }

    ZeusRequest --> ProblemBrief : Phase 0
    ProblemBrief --> InventorSolution : Phase 1
    InventorSolution --> SynthesisResult : Phase 3
    SynthesisResult --> LibraryCritiqueResult : Phase 4
    SynthesisResult --> ZeusResponse : Phase 6 (if no critique)
    LibraryCritiqueResult --> ZeusResponse : Phase 5 & 6
```

---

## 6. Execution Sequence

The following sequence diagram illustrates the asynchronous execution flow from the Streamlit UI to the final output.

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Thread as Background Thread
    participant RC as RunController
    participant LLM as OpenRouterClient
    participant Persist as Persistence

    User->>UI: Click "Run Zeus"
    UI->>Thread: Start _run_pipeline_thread()
    Thread->>RC: run(ZeusRequest)
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 0: Intake
        RC->>LLM: Normalize Input
        LLM-->>RC: ProblemBrief
    end
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 1: Divergent Generation
        RC->>LLM: Run Inventors (Parallel)
        LLM-->>RC: InventorSolutions
    end
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 3: Synthesis
        RC->>LLM: Synthesize Solutions
        LLM-->>RC: SynthesisResult (Unified Draft)
    end
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 4: Critique
        RC->>LLM: Run Library Critics (Parallel)
        LLM-->>RC: LibraryCritiqueResult
    end
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 5: Refinement (Loop)
        loop Max Revisions
            RC->>LLM: Refine Draft
            LLM-->>RC: Refined Draft
        end
    end
    
    rect rgb(40, 45, 65)
        Note over RC, LLM: Phase 6: Assembly
        RC->>LLM: Assemble Deliverables & Scorecard
        LLM-->>RC: ZeusResponse
    end
    
    RC->>Persist: save(RunRecord)
    Persist-->>RC: Success
    RC-->>Thread: Return ZeusResponse
    Thread-->>UI: Update Session State
    UI-->>User: Display Results & Scorecard
```

## 7. Budget and Error Handling

- **Budgeting**: The system tracks `llm_calls`, `tokens_in`, and `tokens_out` via the `BudgetUsed` schema. If `max_llm_calls` is exceeded, a `BudgetExceededError` is raised, halting further generation but triggering a best-effort assembly of existing data.
- **Error Isolation**: Each phase is wrapped in a `_safe_phase` executor. If a phase fails (e.g., due to LLM timeouts), the error is logged to `RunRecord.errors`, and the pipeline attempts to continue or gracefully assemble whatever was completed.
- **Retries**: The `OpenRouterClient` implements exponential backoff for rate limits (429) and server errors (5xx), ensuring transient API issues do not crash the pipeline.
