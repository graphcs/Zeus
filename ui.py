"""Zeus Agent - Capital Squared Dashboard"""

import streamlit as st
import asyncio
import logging
import threading
import time
import io
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from src.core.run_controller import run_zeus
from src.core.persistence import Persistence
from src.utils.read_file import read_file_content
from src.llm.openrouter import OpenRouterClient
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Page Config
# ============================================================================

st.set_page_config(
    page_title="Zeus Agent - Capital Squared",
    page_icon="\u26a1",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CSS
# ============================================================================

st.markdown("""<style>
/* Hide Streamlit chrome */
#MainMenu {visibility: hidden !important;}
header[data-testid="stHeader"] {display: none !important;}
footer {visibility: hidden !important;}
.stDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}

/* Reduce top padding */
.block-container {padding-top: 1.5rem !important; padding-bottom: 1rem !important;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #13142b;
    width: 230px !important;
    min-width: 230px !important;
}
section[data-testid="stSidebar"] > div:first-child {padding-top: 0;}
section[data-testid="stSidebar"] hr {border-color: #2a2b45 !important; margin: 8px 0 !important;}
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: transparent; border: none;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border: 1px solid #2a2b45 !important;
    border-radius: 8px !important;
}

/* Upload zone */
[data-testid="stFileUploader"] {
    border: 2px dashed #3a3b55;
    border-radius: 12px;
    background: #242540;
}
[data-testid="stFileUploader"]:hover {border-color: #4A7BF7;}
[data-testid="stFileUploader"] label {display: none !important;}
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}

/* Progress bar */
.stProgress > div > div > div > div {background-color: #4A7BF7 !important;}

/* Dividers */
hr {border-color: #2a2b45 !important;}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-size: 13px;
    transition: all 0.15s;
}
.stDownloadButton > button {
    border-radius: 8px;
    font-size: 13px;
    background: transparent !important;
    border: 1px solid #3a3b55 !important;
    color: #9898b0 !important;
}
.stDownloadButton > button:hover {
    border-color: #4A7BF7 !important;
    color: #4A7BF7 !important;
}

/* Horizontal block spacing */
[data-testid="stHorizontalBlock"] {gap: 0.5rem !important; align-items: center;}

/* Text input / text area */
.stTextArea textarea, .stTextInput input {
    background-color: #1e1f38 !important;
    border-color: #2a2b45 !important;
    color: #E8E8ED !important;
}

/* Custom classes for HTML elements */
.breadcrumb {color: #7878a0; font-size: 13px;}
.breadcrumb .current {color: #E8E8ED; font-weight: 500;}
.breadcrumb .sep {color: #5858a0; margin: 0 4px;}

.page-title {font-size: 28px; font-weight: 700; color: #E8E8ED; margin: 0 0 2px;}
.page-subtitle {font-size: 14px; color: #7878a0; margin: 0;}

.upload-visual {text-align: center; padding: 12px 0 4px;}
.upload-visual .icon {font-size: 28px; color: #7878a0; margin-bottom: 4px;}
.upload-visual .label {color: #4A7BF7; font-size: 15px; font-weight: 500;}
.upload-visual .hint {color: #5858a0; font-size: 12px; margin-top: 2px;}

.section-label {font-size: 18px; font-weight: 600; color: #E8E8ED;}

.dark-card {
    background: #242540;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 8px 0;
}

.table-header {
    color: #7878a0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.badge-completed {color: #4ade80; font-weight: 500;}
.badge-failed {color: #f87171; font-weight: 500;}
.badge-running {color: #f59e0b; font-weight: 500;}

.nav-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 20px 16px 12px; color: #E8E8ED;
}
.nav-brand-icon {font-size: 20px;}
.nav-brand-text {font-size: 15px; font-weight: 600;}

.nav-project {
    display: flex; align-items: center; gap: 6px;
    padding: 4px 16px 12px; color: #E8E8ED; font-size: 14px;
}
.nav-add-btn {
    background: #4A7BF7; color: white; border-radius: 50%;
    width: 20px; height: 20px; display: inline-flex;
    align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600; margin-left: auto;
}

.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 16px; margin: 1px 8px;
    border-radius: 8px; color: #6868a0; font-size: 14px;
}
.nav-item.active {background: #242540; color: #E8E8ED;}
.nav-item.section-active {color: #E8E8ED; font-weight: 500;}
.nav-item .icon {width: 18px; text-align: center; font-size: 13px;}
.nav-sub {padding-left: 44px;}

.nav-settings {
    padding: 12px 16px; color: #6868a0; font-size: 14px;
    display: flex; align-items: center; gap: 10px;
}

.dim {color: #5858a0; font-size: 12px;}
.row-border {border-bottom: 1px solid #1e1f38; padding-bottom: 4px; margin-bottom: 4px;}

/* Pagination */
.page-num {
    display: inline-block; padding: 3px 9px;
    border-radius: 4px; color: #7878a0; font-size: 13px;
}
.page-num.active {background: #4A7BF7; color: white;}

.live-indicator {
    color: #4ade80;
    font-weight: 600;
}

.status-card {
    background: #242540;
    border: 1px solid #2a2b45;
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 8px;
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.status-title {
    color: #E8E8ED;
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-subtitle {
    color: #9898b0;
    font-size: 12px;
    margin-top: 4px;
}

.status-meta {
    color: #7878a0;
    font-size: 12px;
}

.pulse-group {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4ade80;
    opacity: 0.25;
    animation: zeus-pulse 1.2s infinite ease-in-out;
}

.pulse-dot:nth-child(2) { animation-delay: 0.2s; }
.pulse-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes zeus-pulse {
    0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
    40% { opacity: 1; transform: translateY(-1px); }
}

.step-track {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
}

.step-pill {
    border: 1px solid #2a2b45;
    border-radius: 999px;
    font-size: 11px;
    padding: 3px 8px;
    color: #6868a0;
}

.step-pill.done {
    border-color: #4A7BF7;
    color: #4A7BF7;
}

.step-pill.active {
    border-color: #4ade80;
    color: #E8E8ED;
    background: #1e1f38;
}
</style>""", unsafe_allow_html=True)

# ============================================================================
# Session State
# ============================================================================

_defaults = {
    "uploaded_files": [],       # [{name, content, content_bytes, status}]
    "run_active": False,
    "current_response": None,
    "run_error": None,
    "run_warning": None,
    "run_budget_stop": None,
    "history_page": 1,
    "notes": {},                # run_id -> note text
    "favorites": set(),         # set of run_ids
    "num_inventors": 4,
    "cross_pollinate": False,
    "max_llm_calls": 30,
    "max_revisions": 3,
    "preset": "Normal",
    "prompt_text": "",
    "constraints_text": "",
    "objectives_text": "",
    "_reset_requested": False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# Apply deferred reset before widgets with bound keys are instantiated.
if st.session_state.get("_reset_requested"):
    st.session_state.uploaded_files = []
    st.session_state.current_response = None
    st.session_state.prompt_text = ""
    st.session_state.constraints_text = ""
    st.session_state.objectives_text = ""
    st.session_state.run_error = None
    st.session_state.run_warning = None
    st.session_state.run_budget_stop = None
    st.session_state["_final_logs"] = []
    st.session_state.pop("_constraints", None)
    st.session_state.pop("_objectives", None)
    st.session_state["_reset_requested"] = False

# ============================================================================
# Constants
# ============================================================================

PHASE_PROGRESS = {
    "Phase 0": 0.08,
    "Phase 1": 0.20,
    "Phase 2": 0.40,
    "Phase 3": 0.55,
    "Phase 4": 0.70,
    "Phase 5": 0.82,
    "Phase 6": 0.92,
    "Assembling": 0.96,
    "Saving": 0.99,
}

PIPELINE_STEPS = [
    "Phase 0",
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 6",
    "Saving",
]

STEP_DESCRIPTIONS = {
    "Starting": "Preparing Zeus pipeline and validating run settings.",
    "Phase 0": "Normalizing your input into a structured problem brief.",
    "Phase 1": "Running parallel inventors to generate diverse solution drafts.",
    "Phase 2": "Cross-pollinating inventor ideas to surface stronger options.",
    "Phase 3": "Synthesizing inventor outputs into one unified draft.",
    "Phase 4": "Critiquing draft quality using library-informed checks.",
    "Phase 5": "Refining the draft to address major critique findings.",
    "Phase 6": "Assembling deliverables and evaluation scorecard.",
    "Saving": "Persisting run record and final artifacts.",
}

DELIVERABLES = [
    ("Executive Summary", "executive_summary"),
    ("Solution Design Document", "solution_design_document"),
    ("Foundation Documentation", "foundation_documentation"),
    ("Self-Evaluation Scorecard", "self_evaluation_scorecard"),
    ("Run Log", "run_log"),
]

ROWS_PER_PAGE = 8

# -- Auto-detect reference doc paths --
_DOCS_DIR = Path("docs/updated-docs")
_OUTPUT_SPEC_PATH = _DOCS_DIR / "Output_Specification_v1 1.md"
_EVAL_CRITERIA_PATH = _DOCS_DIR / "Evaluation_Criteria_v1 1.md"
OUTPUT_SPEC_PATH = str(_OUTPUT_SPEC_PATH) if _OUTPUT_SPEC_PATH.exists() else None
EVAL_CRITERIA_PATH = str(_EVAL_CRITERIA_PATH) if _EVAL_CRITERIA_PATH.exists() else None

# -- Demo / example data (from docs/updated-docs) --
FALLBACK_PROBLEM = """\
Personal capital must be allocated — there is no "do nothing" option, as even holding cash is a choice with consequences.

Every allocation exposes the owner to three irreducible pains:
- Loss of Capital — the possibility of ending with less than you started
- Cognitive Requirement — the mental work the process demands
- Forgone Returns — underperformance relative to alternatives that were available

Design an investment system that minimizes these three pains while compounding capital in real purchasing power over time."""

FALLBACK_CONSTRAINTS = """\
Must be implementable by a startup of 5-10 people significantly augmented by AI (HARD)
Must use information and instruments accessible to the public (HARD)
Crypto-native — prefer solutions built on or around crypto/blockchain infrastructure (SOFT)
Prefer less regulated markets (SOFT)
Prefer solutions achievable with moderate starting capital $10K-$1M (SOFT)"""

FALLBACK_OBJECTIVES = """\
Preserve capital first, then maximize returns (MUST)"""

EXAMPLE_GEN_PROMPT = """\
Generate a creative, specific business or technology problem that needs a comprehensive solution design.

Return JSON with exactly these keys:
- "problem": A 3-5 sentence problem statement. Be specific about the domain, the pain points, and what needs to be designed. Pick a random interesting domain — fintech, healthtech, AI infrastructure, logistics, marketplace, climate tech, space, robotics, gaming, education, etc.
- "constraints": A list of 3-5 short constraint strings. Each must end with (HARD) or (SOFT). Include at least 1 HARD constraint about team size or budget, and at least 1 SOFT preference.
- "objectives": A list with 0 or 1 objective string. If included, tag it (MUST) or (COULD).

Be creative and varied. Do NOT generate generic problems. Make them feel like real startup or investment design challenges."""


def _generate_example():
    """Call Gemini Flash to generate a fresh random example."""
    loop = asyncio.new_event_loop()
    try:
        async def _call():
            async with OpenRouterClient(
                model="google/gemini-2.0-flash-001", timeout=15.0
            ) as client:
                result, _ = await client.generate_json(
                    prompt=EXAMPLE_GEN_PROMPT,
                    system="You generate creative business problem statements for solution design exercises. Return only JSON.",
                    temperature=1.0,
                    max_tokens=1024,
                )
                return result

        result = loop.run_until_complete(_call())
        return {
            "problem": result.get("problem", ""),
            "constraints": "\n".join(result.get("constraints", [])),
            "objectives": "\n".join(result.get("objectives", [])),
        }
    except Exception:
        return {
            "problem": FALLBACK_PROBLEM,
            "constraints": FALLBACK_CONSTRAINTS,
            "objectives": FALLBACK_OBJECTIVES,
        }
    finally:
        loop.close()

# ============================================================================
# Background Thread State (module-level for cross-thread communication)
# ============================================================================

# CRITICAL: Streamlit re-executes this entire script on every rerun/interaction.
# A plain module-level dict would be re-created each time, losing all data the
# background thread wrote.  By storing the dict on the `threading` module (which
# is imported once and cached by Python), the same object survives reruns.
if not hasattr(threading, "_zeus_state"):
    threading._zeus_state = {
        "active": False,
        "msg": "",
        "pct": 0.0,
        "start_time": 0.0,
        "response": None,
        "error": None,
        "warning": None,
        "budget_stop": None,
        "done": False,
        "logs": [],  # list of (timestamp_str, level, message)
    }
_thread_state = threading._zeus_state


class _ThreadLogHandler(logging.Handler):
    """Logging handler that captures log records into _thread_state['logs']."""

    def emit(self, record):
        try:
            ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            _thread_state["logs"].append((ts, record.levelname, self.format(record)))
        except Exception:
            pass


def _run_pipeline_thread(prompt, constraints, objectives, context, settings):
    """Run the Zeus pipeline in a background thread."""
    import traceback

    _thread_state.update({
        "active": True, "msg": "Starting...", "pct": 0.0,
        "start_time": time.time(), "response": None,
        "error": None, "warning": None, "budget_stop": None, "done": False, "logs": [],
    })

    handler = None

    def _log(msg, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        _thread_state["logs"].append((ts, level, msg))

    def on_progress(msg):
        _thread_state["msg"] = msg
        _log(msg)
        for key, pct in PHASE_PROGRESS.items():
            if key in msg:
                _thread_state["pct"] = pct
                break

    try:
        # Set up log capture for all src.* loggers
        handler = _ThreadLogHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger = logging.getLogger("src")
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)

        _log(f"Pipeline starting — {settings['num_inventors']} inventors, "
             f"budget {settings['max_llm_calls']} calls, "
               f"max {settings['max_revisions']} revisions")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(run_zeus(
            prompt=prompt,
            constraints=constraints,
            objectives=objectives,
            context=context,
            output_spec_path=settings.get("output_spec_path"),
            eval_criteria_path=settings.get("eval_criteria_path"),
            enable_cross_pollination=settings["cross_pollinate"],
            num_inventors=settings["num_inventors"],
            on_progress=on_progress,
            max_llm_calls=settings["max_llm_calls"],
            max_revisions=settings["max_revisions"],
        ))
        loop.close()
        _thread_state["response"] = response
        _thread_state["pct"] = 1.0
        _thread_state["msg"] = "Complete"
        _log(f"Pipeline complete — score {response.total_score:.1f}/{response.max_score:.0f}")

        # Detect actual pipeline errors in known_issues.
        # known_issues contains BOTH legitimate critique findings ([MAJOR], [MINOR],
        # [OPEN] prefixed) AND real pipeline errors (timeout, LLM errors, etc).
        # Only surface real pipeline errors — critique findings are expected output.
        _error_prefixes = (
            "LLM error:", "Budget exceeded:",
            "Assembly failed:", "Unexpected error:", "All inventors failed",
            "Synthesis produced empty", "Generation failed",
        )
        real_errors = [
            i for i in (response.known_issues or [])
            if any(i.startswith(p) for p in _error_prefixes)
        ]
        budget_errors = [i for i in real_errors if i.startswith("Budget exceeded:")]
        non_budget_errors = [i for i in real_errors if not i.startswith("Budget exceeded:")]

        if budget_errors:
            _thread_state["budget_stop"] = "; ".join(budget_errors)
            for err in budget_errors:
                _log(f"Run stopped by budget limit: {err}", "WARNING")

        if non_budget_errors:
            # If we still got usable output, treat as warning rather than hard failure.
            has_output = bool(response and response.output and response.output.strip())
            if has_output:
                _thread_state["warning"] = "; ".join(non_budget_errors)
                for err in non_budget_errors:
                    _log(f"Pipeline warning: {err} (output still produced)", "WARNING")
            else:
                _thread_state["error"] = "; ".join(non_budget_errors)
                for err in non_budget_errors:
                    _log(f"Pipeline error: {err}", "ERROR")
        if response.disqualified and not non_budget_errors and not budget_errors:
            _log("Note: solution was disqualified by evaluation scorecard", "WARNING")
    except Exception as e:
        tb = traceback.format_exc()
        _thread_state["error"] = str(e)
        _log(f"ERROR: {e}", "ERROR")
        _log(tb, "ERROR")
    finally:
        if handler:
            logging.getLogger("src").removeHandler(handler)
        _thread_state["active"] = False
        _thread_state["done"] = True


# ============================================================================
# Helpers
# ============================================================================

def get_persistence():
    return Persistence()


def format_elapsed(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s:02d}s"


def _make_outputs_zip(response):
    """Create a zip file of all output deliverables."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for _, field in DELIVERABLES:
            content = getattr(response, field, "")
            if content:
                zf.writestr(f"{field}.md", content)
        zf.writestr("full_output.md", response.output)
    return buf.getvalue()


def _get_current_step(msg: str) -> str:
    """Extract a concise pipeline step from progress message."""
    if not msg:
        return "Starting"

    for step in PIPELINE_STEPS:
        if step in msg:
            return step
    return "Starting"


def _get_step_description(step: str) -> str:
    """Get human-friendly description for the current pipeline step."""
    return STEP_DESCRIPTIONS.get(step, "Zeus is actively processing your request.")


def _render_scrollable_logs(logs: list[tuple[str, str, str]]) -> None:
    """Render logs in a fixed-height, scrollable panel."""
    if not logs:
        return
    log_text = "\n".join(f"[{ts}] {lvl:5s}  {m}" for ts, lvl, m in logs)
    with st.container(height=280):
        st.code(log_text, language="log", wrap_lines=True)


# ============================================================================
# Dialogs
# ============================================================================

@st.dialog("Add note")
def add_note_dialog(run_id):
    """Dialog for adding/editing a note on a run."""
    existing = st.session_state.notes.get(run_id, "")
    note = st.text_area("Note", value=existing, height=250, label_visibility="collapsed",
                        placeholder="Write your note here...")
    c1, c2, c3 = st.columns([4, 1, 1])
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with c3:
        if st.button("Save", type="primary", use_container_width=True):
            st.session_state.notes[run_id] = note
            st.rerun()


@st.dialog("Viewing Document", width="large")
def view_document_dialog(title, content):
    """Dialog for viewing a document's full content."""
    st.markdown(f"**Viewing: {title}**")
    st.divider()
    st.markdown(content)


@st.dialog("Run Outputs", width="large")
def view_outputs_dialog(run_id):
    """Dialog showing outputs for a history run."""
    st.caption(f"Run {run_id[:8]}")
    p = get_persistence()
    record = p.load(run_id)
    if record and record.final_response:
        resp = record.final_response
        for display_name, field in DELIVERABLES:
            content = getattr(resp, field, "")
            if content:
                c1, c2 = st.columns([8, 1])
                with c1:
                    st.markdown(display_name)
                with c2:
                    st.download_button(
                        "\u2b07", data=content, file_name=f"{field}.md",
                        mime="text/markdown", key=f"dlg_dl_{run_id}_{field}",
                    )
        st.divider()
        zip_data = _make_outputs_zip(resp)
        st.download_button(
            "\u2b07 Download All", data=zip_data,
            file_name=f"zeus_outputs_{run_id[:8]}.zip",
            mime="application/zip", key=f"dlg_dlall_{run_id}",
            use_container_width=True, type="primary",
        )
    else:
        st.info("No outputs available for this run.")


@st.dialog("Run Inputs")
def view_inputs_dialog(run_id):
    """Dialog showing inputs for a history run."""
    st.caption(f"Run {run_id[:8]}")
    p = get_persistence()
    record = p.load(run_id)
    if record:
        req = record.request
        if req.prompt:
            st.markdown("**Problem Statement:**")
            st.markdown(req.prompt)
        if req.constraints:
            st.markdown("**Constraints:**")
            for c in req.constraints:
                st.markdown(f"- {c}")
        if req.objectives:
            st.markdown("**Objectives:**")
            for o in req.objectives:
                st.markdown(f"- {o}")
        if not req.prompt and not req.constraints and not req.objectives:
            st.info("No input details recorded.")
    else:
        st.info("Run record not found.")


# ============================================================================
# Progress Fragment (auto-reruns every 2s to poll background thread)
# ============================================================================

@st.fragment(run_every=timedelta(seconds=1))
def show_progress():
    """Display run progress with live log, polling the background thread state."""
    # Check if thread finished
    if _thread_state.get("done") and not _thread_state.get("active"):
        if _thread_state.get("response"):
            st.session_state.current_response = _thread_state["response"]
            for f in st.session_state.uploaded_files:
                f["status"] = "processed"
        if _thread_state.get("budget_stop"):
            st.session_state.run_budget_stop = _thread_state["budget_stop"]
        if _thread_state.get("error"):
            st.session_state.run_error = _thread_state["error"]
        if _thread_state.get("warning"):
            st.session_state.run_warning = _thread_state["warning"]
        # Keep final logs visible
        st.session_state["_final_logs"] = list(_thread_state.get("logs", []))
        st.session_state.run_active = False
        _thread_state["done"] = False
        # MUST use scope="app" to rerun the full page, not just this fragment
        st.rerun(scope="app")
        return

    # Always show progress UI — even if thread is still starting up
    hcol1, hcol2 = st.columns([5, 1.5])
    with hcol1:
        st.markdown("**Run in progress**")
    with hcol2:
        if st.button("Stop Run", key="stop_btn"):
            st.session_state.run_active = False
            _thread_state["done"] = True
            _thread_state["active"] = False
            st.rerun(scope="app")

    pct = _thread_state.get("pct", 0.0)
    msg = _thread_state.get("msg", "Starting...")
    current_step = _get_current_step(msg)
    step_description = _get_step_description(current_step)
    elapsed = time.time() - _thread_state.get("start_time", time.time())

    st.progress(pct)


    heartbeat = datetime.now().strftime("%H:%M:%S")
    if current_step in PIPELINE_STEPS:
        active_idx = PIPELINE_STEPS.index(current_step)
    else:
        active_idx = -1

    step_labels = {
        "Phase 0": "P0 Intake",
        "Phase 1": "P1 Inventors",
        "Phase 2": "P2 Cross",
        "Phase 3": "P3 Synthesis",
        "Phase 4": "P4 Critique",
        "Phase 5": "P5 Refine",
        "Phase 6": "P6 Assembly",
        "Saving": "Saving",
    }

    pills = []
    for idx, step in enumerate(PIPELINE_STEPS):
        cls = "step-pill"
        if idx < active_idx:
            cls += " done"
        elif idx == active_idx:
            cls += " active"
        label = step_labels.get(step, step)
        pills.append(f'<span class="{cls}">{label}</span>')

    st.markdown(
        f'''<div class="status-card">
<div class="status-row">
  <div>
    <div class="status-title">
      <span class="pulse-group"><span class="pulse-dot"></span><span class="pulse-dot"></span><span class="pulse-dot"></span></span>
      <span>Current Step: {current_step}</span>
    </div>
    <div class="status-subtitle">{step_description}</div>
  </div>
  <div class="status-meta">Heartbeat {heartbeat}</div>
</div>
<div class="step-track">{"".join(pills)}</div>
</div>''',
        unsafe_allow_html=True,
    )

    # Live log
    logs = _thread_state.get("logs", [])
    _render_scrollable_logs(logs)


# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:
    # Brand
    st.markdown("""
    <div class="nav-brand">
        <span class="nav-brand-icon">\u26a1</span>
        <span class="nav-brand-text">Capital Squared</span>
    </div>
    """, unsafe_allow_html=True)

    # Project selector (decorative)
    st.markdown("""
    <div class="nav-project">
        <span>Projects Alpha</span>
        <span style="color:#5858a0; margin-left: 2px;">\u25be</span>
        <span class="nav-add-btn">+</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Navigation
    st.markdown("""
    <div class="nav-item">
        <span class="icon">\U0001f3e0</span> Pipeline Overview
    </div>
    <div class="nav-item section-active">
        <span class="icon">\U0001f916</span> Agents
    </div>
    <div class="nav-item active nav-sub">
        <span class="icon">\u26a1</span> Zeus
    </div>
    <div class="nav-item nav-sub">
        <span class="icon">\u23f1</span> Kronos
    </div>
    <div class="nav-item nav-sub">
        <span class="icon">\U0001f4aa</span> Hercules
    </div>
    <div class="nav-item nav-sub">
        <span class="icon">\u2600\ufe0f</span> Helios
    </div>
    <div class="nav-item nav-sub">
        <span class="icon">\U0001f319</span> Morpheus
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Speed presets
    PRESETS = {
        "Turbo": {
            "num_inventors": 1,
            "cross_pollinate": False,
            "max_llm_calls": 5,
            "max_revisions": 0,
            "desc": "~3-5 min — 1 inventor, no refinement, skip critique",
        },
        "Fast": {
            "num_inventors": 2,
            "cross_pollinate": False,
            "max_llm_calls": 12,
            "max_revisions": 1,
            "desc": "~5-10 min — 2 inventors, 1 refinement pass",
        },
        "Normal": {
            "num_inventors": 4,
            "cross_pollinate": False,
            "max_llm_calls": 30,
            "max_revisions": 3,
            "desc": "~10-20 min — 4 inventors, up to 3 refinements",
        },
        "Thorough": {
            "num_inventors": 5,
            "cross_pollinate": True,
            "max_llm_calls": 50,
            "max_revisions": 3,
            "desc": "~15-25 min — 5 inventors, cross-pollination, full critique",
        },
    }

    # Settings
    with st.expander("\u2699\ufe0f Settings", expanded=True):
        all_modes = list(PRESETS.keys()) #+ ["Custom"]
        current_idx = all_modes.index(st.session_state.preset) if st.session_state.preset in all_modes else 2

        def _apply_preset():
            name = st.session_state["_preset_sel"]
            st.session_state.preset = name
            if name in PRESETS:
                p = PRESETS[name]
                st.session_state.num_inventors = p["num_inventors"]
                st.session_state.cross_pollinate = p["cross_pollinate"]
                st.session_state.max_llm_calls = p["max_llm_calls"]
                st.session_state.max_revisions = p["max_revisions"]

        chosen = st.radio(
            "Run Mode",
            all_modes,
            index=current_idx,
            key="_preset_sel",
            on_change=_apply_preset,
            horizontal=True,
        )

        if chosen in PRESETS:
            st.caption(PRESETS[chosen]["desc"])
        # else:
        #     # Custom mode — show all controls
        #     st.session_state.num_inventors = st.slider(
        #         "Inventors", 1, 10, st.session_state.num_inventors, key="_inv"
        #     )
        #     st.session_state.max_revisions = st.slider(
        #         "Max Refinement Rounds", 0, 5, st.session_state.max_revisions, key="_rev"
        #     )
        #     st.session_state.cross_pollinate = st.toggle(
        #         "Cross-Pollination", st.session_state.cross_pollinate, key="_cp"
        #     )
        #     st.session_state.max_llm_calls = st.number_input(
        #         "Max LLM Calls", value=st.session_state.max_llm_calls, min_value=1, key="_llm"
        #     )


# ============================================================================
# Main Content
# ============================================================================

# -- Breadcrumb --
st.markdown("""
<div class="breadcrumb">
    <span>Projects</span><span class="sep">\u203a</span>
    <span>Project Alpha</span><span class="sep">\u203a</span>
    <span class="current">Zeus</span>
</div>
""", unsafe_allow_html=True)

# -- Header --
st.markdown("""
<div>
    <div class="page-title">Zeus Agent</div>
    <div class="page-subtitle">Upload design brief \u2192 Zeus generates solution</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# -- Upload Zone --
st.markdown("""
<div class="upload-visual">
    <div class="icon">\u2601</div>
    <div class="label">Upload</div>
    <div class="hint">Markdown, text, doc, or pdf</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    type=["md", "txt", "doc", "docx", "pdf"],
    label_visibility="collapsed",
)

# Copy uploaded files to session state immediately
if uploaded:
    existing_names = {f["name"] for f in st.session_state.uploaded_files}
    for f in uploaded:
        if f.name not in existing_names:
            try:
                content = read_file_content(f, filename=f.name)
                st.session_state.uploaded_files.append({
                    "name": f.name,
                    "content": content,
                    "content_bytes": f.getvalue(),
                    "status": "pending",
                })
            except Exception as e:
                st.error(f"Error reading {f.name}: {e}")

# -- Problem Statement --
st.markdown('<span class="section-label">Problem Statement</span>', unsafe_allow_html=True)

# Load Example button
if st.button("\U0001f4cb Load Example", key="load_demo", help="Generate a random example problem"):
    with st.spinner("Generating example..."):
        example = _generate_example()
    st.session_state.prompt_text = example["problem"]
    st.session_state["_constraints"] = example["constraints"]
    st.session_state["_objectives"] = example["objectives"]
    st.rerun()

st.session_state.prompt_text = st.text_area(
    "Problem Statement",
    value=st.session_state.prompt_text,
    placeholder="Describe the problem you want to solve...",
    height=120,
    label_visibility="collapsed",
)

# -- Constraints & Objectives --
co1, co2 = st.columns(2)
with co1:
    st.caption("Constraints (one per line)")
    # Initialize widget key from session state if not yet set
    if "_constraints" not in st.session_state and st.session_state.constraints_text:
        st.session_state["_constraints"] = st.session_state.constraints_text
    st.text_area(
        "Constraints",
        placeholder="Must be implementable by 5-10 person team (HARD)\nMust use public data (HARD)\nPrefer simplicity (SOFT)",
        height=120,
        label_visibility="collapsed",
        key="_constraints",
    )
    st.session_state.constraints_text = st.session_state.get("_constraints", "")
with co2:
    st.caption("Objectives (one per line)")
    if "_objectives" not in st.session_state and st.session_state.objectives_text:
        st.session_state["_objectives"] = st.session_state.objectives_text
    st.text_area(
        "Objectives",
        placeholder="Preserve capital first (MUST)\nMinimize cognitive burden (MUST)\nPrefer simplicity (COULD)",
        height=120,
        label_visibility="collapsed",
        key="_objectives",
    )
    st.session_state.objectives_text = st.session_state.get("_objectives", "")

# -- Inputs List --
if st.session_state.uploaded_files:
    hc1, hc2 = st.columns([7, 2])
    with hc1:
        st.markdown('<span class="section-label">Inputs</span>', unsafe_allow_html=True)
    with hc2:
        if len(st.session_state.uploaded_files) > 1:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                for fi in st.session_state.uploaded_files:
                    zf.writestr(fi["name"], fi.get("content_bytes", fi["content"].encode()))
            st.download_button(
                "\u2b07 Download All", data=buf.getvalue(),
                file_name="inputs.zip", mime="application/zip",
                key="dl_all_in", use_container_width=True,
            )

    files_to_remove = []
    for i, fi in enumerate(st.session_state.uploaded_files):
        cols = st.columns([0.4, 7, 0.8, 0.4])

        # Status icon
        with cols[0]:
            status = fi.get("status", "pending")
            if status == "processed":
                st.markdown(":white_check_mark:")
            elif status == "processing":
                st.markdown(":hourglass_flowing_sand:")
            else:
                st.markdown(":radio_button:")

        # Filename
        with cols[1]:
            st.markdown(fi["name"])

        # Download
        with cols[2]:
            raw = fi.get("content_bytes", fi["content"].encode())
            st.download_button(
                "\u2b07", data=raw, file_name=fi["name"],
                key=f"dl_f_{i}",
            )

        # Remove
        with cols[3]:
            if st.button("\u2715", key=f"rm_f_{i}"):
                files_to_remove.append(i)

    for idx in sorted(files_to_remove, reverse=True):
        st.session_state.uploaded_files.pop(idx)
    if files_to_remove:
        st.rerun()


# -- Transfer completed background run (fallback check) --
if _thread_state.get("done") and not st.session_state.run_active:
    if _thread_state.get("response"):
        st.session_state.current_response = _thread_state["response"]
        for f in st.session_state.uploaded_files:
            f["status"] = "processed"
    if _thread_state.get("budget_stop"):
        st.session_state.run_budget_stop = _thread_state["budget_stop"]
    if _thread_state.get("error"):
        st.session_state.run_error = _thread_state["error"]
    _thread_state["done"] = False


# -- Run Button / Progress --
if st.session_state.run_active or _thread_state.get("active"):
    show_progress()
elif not st.session_state.current_response:
    if st.button("\u26a1 Generate Solution", type="primary", use_container_width=True):
        if not st.session_state.prompt_text.strip() and not st.session_state.uploaded_files:
            st.warning("Please provide a problem statement or upload files.")
        else:
            # Build context from uploaded files
            context_parts = [f["content"] for f in st.session_state.uploaded_files]
            context = "\n\n".join(context_parts) if context_parts else None
            prompt = (
                st.session_state.prompt_text.strip()
                or "Analyze the uploaded documents and generate a comprehensive solution."
            )

            # Parse constraints and objectives (one per line)
            constraints = [
                c.strip() for c in st.session_state.constraints_text.split("\n") if c.strip()
            ]
            objectives = [
                o.strip() for o in st.session_state.objectives_text.split("\n") if o.strip()
            ]

            # Mark files as processing
            for f in st.session_state.uploaded_files:
                f["status"] = "processing"

            st.session_state.run_active = True
            st.session_state.current_response = None
            st.session_state.run_error = None
            st.session_state.run_warning = None
            st.session_state.run_budget_stop = None
            st.session_state["_final_logs"] = []

            settings = {
                "cross_pollinate": st.session_state.cross_pollinate,
                "num_inventors": st.session_state.num_inventors,
                "max_llm_calls": st.session_state.max_llm_calls,
                "max_revisions": st.session_state.max_revisions,
                "output_spec_path": OUTPUT_SPEC_PATH,
                "eval_criteria_path": EVAL_CRITERIA_PATH,
            }
            thread = threading.Thread(
                target=_run_pipeline_thread,
                args=(prompt, constraints, objectives, context, settings),
                daemon=True,
            )
            thread.start()
            st.rerun()


# -- Error / Warning Display --
if st.session_state.run_budget_stop:
    st.info(f"Run stopped due to budget limit: {st.session_state.run_budget_stop}")
if st.session_state.run_error:
    st.error(f"Run failed: {st.session_state.run_error}")
if st.session_state.run_warning:
    st.warning(f"Completed with issues: {st.session_state.run_warning}")

# -- Final run log (shown after completion) --
final_logs = st.session_state.get("_final_logs", [])
if final_logs and not st.session_state.run_active:
    with st.expander("Run Log", expanded=True):
        _render_scrollable_logs(final_logs)


# -- Outputs Section --
response = st.session_state.current_response
if response:
    st.markdown("")
    st.markdown('<span class="section-label">Outputs</span>', unsafe_allow_html=True)

    for display_name, field in DELIVERABLES:
        content = getattr(response, field, "")
        if content:
            oc1, oc2, oc3 = st.columns([8, 0.6, 0.6])
            with oc1:
                st.markdown(display_name)
            with oc2:
                if st.button("\U0001f4c4", key=f"view_{field}", help=f"View {display_name}"):
                    view_document_dialog(display_name, content)
            with oc3:
                st.download_button(
                    "\u2b07", data=content, file_name=f"{field}.md",
                    mime="text/markdown", key=f"dl_{field}",
                )

    # Score summary
    score_html = (
        f'<strong>Score:</strong> {response.total_score:.1f} / {response.max_score:.0f} '
        f'({response.score_percentage:.1f}%)'
    )
    if response.disqualified:
        score_html += ' <span class="badge-failed">\u2014 DISQUALIFIED</span>'
    st.markdown(f'<div class="dark-card">{score_html}</div>', unsafe_allow_html=True)

    # Action buttons
    st.markdown("")
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        st.button("Take to Kronos", disabled=True, key="btn_kronos", use_container_width=True)
    with ac2:
        if st.button("Clear and Restart", key="btn_clear", use_container_width=True):
            st.session_state["_reset_requested"] = True
            st.rerun()
    with ac3:
        if st.button("\u270f Add Note", key="btn_note", use_container_width=True):
            add_note_dialog(response.run_id)
    with ac4:
        zip_data = _make_outputs_zip(response)
        st.download_button(
            "\u2b07 Download All", data=zip_data,
            file_name=f"zeus_outputs_{response.run_id[:8]}.zip",
            mime="application/zip", key="dl_all_out",
            use_container_width=True,
        )


# ============================================================================
# Run History
# ============================================================================

st.markdown("")
st.markdown("")
st.markdown('<span class="section-label">Run History</span>', unsafe_allow_html=True)

try:
    persistence = get_persistence()
    all_runs = persistence.list_runs(limit=100)

    if not all_runs:
        st.caption("No runs found.")
    else:
        total_pages = max(1, -(-len(all_runs) // ROWS_PER_PAGE))  # ceiling division
        page = min(st.session_state.history_page, total_pages)
        start_idx = (page - 1) * ROWS_PER_PAGE
        page_runs = all_runs[start_idx:start_idx + ROWS_PER_PAGE]

        # Table header
        h = st.columns([1.2, 0.8, 2, 1, 1, 0.7, 0.7, 0.7, 0.6])
        labels = ["Run ID", "User", "Timestamp", "Status", "Run time",
                   "Inputs", "Outputs", "Notes", "Fav"]
        for col, label in zip(h, labels):
            col.markdown(f'<span class="table-header">{label}</span>', unsafe_allow_html=True)
        st.divider()

        # Table rows
        for run in page_runs:
            rid = run["run_id"]
            r = st.columns([1.2, 0.8, 2, 1, 1, 0.7, 0.7, 0.7, 0.6])

            # Run ID
            with r[0]:
                st.markdown(f"#{rid[:6]}")

            # User
            with r[1]:
                st.markdown("Local")

            # Timestamp
            with r[2]:
                ts = run.get("timestamp", "")
                try:
                    dt = datetime.fromisoformat(ts)
                    st.caption(dt.strftime("%Y-%m-%d %H:%M:%S"))
                except (ValueError, TypeError):
                    st.caption(str(ts)[:19])

            # Status
            with r[3]:
                status = run.get("status", "Unknown")
                if status == "Completed":
                    cls = "badge-completed"
                elif status in ("Completed (with issues)", "Stopped (Budget limit)"):
                    cls = "badge-running"
                else:
                    cls = "badge-failed"
                st.markdown(f'<span class="{cls}">{status}</span>', unsafe_allow_html=True)

            # Run time
            with r[4]:
                budget = run.get("budget_used", {})
                calls = budget.get("llm_calls", 0)
                if calls:
                    st.caption(f"{calls} calls")
                else:
                    st.caption("-")

            # Inputs
            with r[5]:
                ic = run.get("input_count", 0)
                if ic > 0:
                    if st.button(f"\U0001f4c1 +{ic}", key=f"hi_{rid}"):
                        view_inputs_dialog(rid)
                else:
                    st.markdown("\U0001f4c1")

            # Outputs
            with r[6]:
                if run.get("has_response"):
                    if st.button("\U0001f4c4", key=f"ho_{rid}"):
                        view_outputs_dialog(rid)
                else:
                    st.caption("\u2014")

            # Notes
            with r[7]:
                note = st.session_state.notes.get(rid, "")
                label = "\U0001f4dd" if not note else f"\U0001f4dd +1"
                if st.button(label, key=f"hn_{rid}"):
                    add_note_dialog(rid)

            # Favorite
            with r[8]:
                is_fav = rid in st.session_state.favorites
                star = "\u2b50" if is_fav else "\u2606"
                if st.button(star, key=f"hf_{rid}"):
                    if is_fav:
                        st.session_state.favorites.discard(rid)
                    else:
                        st.session_state.favorites.add(rid)
                    st.rerun()

        # Pagination
        if total_pages > 1:
            st.markdown("")
            pc1, pc2, pc3 = st.columns([1.5, 5, 1.5])

            with pc1:
                if page > 1:
                    if st.button("\u2190 Previous", key="pg_prev"):
                        st.session_state.history_page = page - 1
                        st.rerun()

            with pc2:
                # Build page number display
                nums = []
                for p in range(1, total_pages + 1):
                    if p <= 3 or p >= total_pages - 1 or abs(p - page) <= 1:
                        cls = "active" if p == page else ""
                        nums.append(f'<span class="page-num {cls}">{p}</span>')
                    elif nums and nums[-1] != "...":
                        nums.append("...")
                st.markdown(
                    '<div style="text-align:center;">' + " ".join(nums) + '</div>',
                    unsafe_allow_html=True,
                )

            with pc3:
                if page < total_pages:
                    if st.button("Next \u2192", key="pg_next"):
                        st.session_state.history_page = page + 1
                        st.rerun()

except Exception as e:
    st.error(f"Error loading history: {e}")
