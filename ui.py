from pathlib import Path
from src.core.run_controller import run_zeus
from src.core.persistence import Persistence
from dotenv import load_dotenv
import streamlit as st
import asyncio
from src.utils.read_file import read_file_content
load_dotenv()


st.set_page_config(
    page_title="Zeus - Design Team Agent",
    layout="wide",
)

st.title("Zeus - Design Team Agent")
with st.sidebar:  
    st.toggle("Advanced Budget Settings", key="show_budget")
    if st.session_state.get("show_budget"):
        max_llm_calls = st.number_input("Max LLM Calls", value=8, min_value=1)
        total_timeout = st.number_input("Total Timeout (s)", value=900, min_value=60)
    else:
        max_llm_calls = None
        total_timeout = None



def get_persistence():
    # Helper to init persistence with correct path relative to CWD or package
    # Assuming CWD is project root
    return Persistence()

def format_evaluation_summary(response) -> str:
    """Format evaluation summary in readable Markdown format."""
    lines = []

    if hasattr(response,'reasoning_trace') and response.reasoning_trace:
        lines.append("## Reasoning Trace\n")
        lines.append(response.reasoning_trace)

    if hasattr(response,'comparison_analysis') and response.comparison_analysis:
        lines.append("## Comparison Analysis\n")
        lines.append(response.comparison_analysis)
    
    # Header
    lines.append("\n---\n")
    lines.append("## Evaluation Summary\n")

    # V2 Regression Analysis
    if hasattr(response, 'regression_analysis') and response.regression_analysis:
        reg = response.regression_analysis
        lines.append("\n### V2 Regression Analysis\n")
        
        status_text = "REGRESSION DETECTED" if reg.is_worse else "Improvement / Stable"
        status_emoji = "📉" if reg.is_worse else "📈"
        lines.append(f"- **Status:** {status_emoji} {status_text}\n")
        lines.append(f"- **Baseline Run:** {reg.baseline_run_id[:8]}\n")
        
        cov_sign = "+" if reg.coverage_delta >= 0 else ""
        lines.append(f"- **Coverage Delta:** {cov_sign}{int(reg.coverage_delta * 100)}%\n")
        
        iss_sign = "+" if reg.issues_delta > 0 else ""
        lines.append(f"- **Total Issues Delta:** {iss_sign}{reg.issues_delta}\n")
        
        if reg.blocker_delta != 0:
             b_sign = "+" if reg.blocker_delta > 0 else ""
             lines.append(f"- **Blockers Delta:** {b_sign}{reg.blocker_delta}\n")
             
        if reg.major_delta != 0:
             m_sign = "+" if reg.major_delta > 0 else ""
             lines.append(f"- **Majors Delta:** {m_sign}{reg.major_delta}\n")

        if reg.constraints_delta != 0:
             c_sign = "+" if reg.constraints_delta > 0 else ""
             lines.append(f"- **Constraints Delta:** {c_sign}{reg.constraints_delta}\n")
    
    # Confidence and Coverage
    lines.append("### Quality Metrics\n")
    conf_emoji = {"low": "🔴", "medium": "🟡", "high": "🟢"}.get(response.confidence, "⚪")
    coverage_pct = int(response.coverage_score * 100)
    lines.append(f"- **Confidence Level:** {conf_emoji} {response.confidence.upper()}\n")
    lines.append(f"- **Critique Coverage:** {coverage_pct}% ({int(response.coverage_score * 6)}/6 perspectives)\n")
    
    # Detailed evaluation if available
    if hasattr(response, 'evaluation_summary') and response.evaluation_summary:
        eval_sum = response.evaluation_summary
        
        lines.append("\n### Issue Breakdown\n")
        blockers = eval_sum.get('blockers', 0)
        majors = eval_sum.get('majors', 0)
        minors = eval_sum.get('minors', 0)
        total = eval_sum.get('total_issues', 0)
        
        lines.append("| Severity | Count | Status |\n")
        lines.append("|----------|-------|--------|\n")
        
        if blockers > 0:
            lines.append(f"| 🚫 Blockers | {blockers} | ⚠️ CRITICAL |\n")
        else:
            lines.append(f"| 🚫 Blockers | {blockers} | ✅ Clear |\n")
        
        if majors > 0:
            lines.append(f"| ⚠️ Majors | {majors} | Needs attention |\n")
        else:
            lines.append(f"| ⚠️ Majors | {majors} | ✅ Clear |\n")
        
        lines.append(f"| ℹ️ Minors | {minors} | Optional |\n")
        lines.append(f"| Total Issues | {total} | - |\n")
        
        # Missing perspectives
        missing = eval_sum.get('missing_perspectives', [])
        if missing:
            lines.append(f"\n### Missing Perspectives\n")
            lines.append("The following critique perspectives were not covered and should be considered:\n\n")
            for perspective in missing:
                lines.append(f"- **{perspective.title()}**\n")
        
        # Covered perspectives
        covered = eval_sum.get('covered_perspectives', [])
        if covered:
            lines.append(f"\n### Covered Perspectives\n")
            for perspective in covered:
                lines.append(f"- {perspective.title()}\n")
        
        # Issues by category
        issues_by_cat = eval_sum.get('issues_by_category', {})
        if issues_by_cat:
            lines.append(f"\n###  Issues by Category\n")
            lines.append("| Category | Count |\n")
            lines.append("|----------|-------|\n")
            for cat, count in sorted(issues_by_cat.items(), key=lambda x: x[1], reverse=True):
                cat_label = cat.replace('_', ' ').title()
                lines.append(f"| {cat_label} | {count} |\n")
    
    # V3 Verification
    if hasattr(response, 'verification_report') and response.verification_report:
        rep = response.verification_report
        lines.append("\n### 🛡️ Constraints Verification\n")
        lines.append(f"- **Coverage:** {int(rep.coverage_score * 100)}%\n\n")
        lines.append("| Status | Constraint | Evidence |\n")
        lines.append("|--------|------------|----------|\n")
        for c in rep.checks:
            icon = {"pass": "✅", "fail": "❌", "unverified": "❓"}.get(c.status, "❓")
            evidence = (c.evidence or "").replace("|", "\\|").replace("\n", " ")[:100]
            lines.append(f"| {icon} {c.status.upper()} | {c.constraint} | {evidence} |\n")

    # V3 Structured Issues
    if hasattr(response, 'structured_issues') and response.structured_issues:
        lines.append("\n### ⚠️ Known Issues Registry\n")
        lines.append("| Issue | Impact | Mitigation | Verification |\n")
        lines.append("|-------|--------|------------|--------------|\n")
        for si in response.structured_issues:
             lines.append(f"| {si.issue} | {si.impact} | {si.mitigation} | {si.verification_step} |\n")

    # Tradeoffs
    if response.tradeoffs:
        lines.append("\n###  Design Tradeoffs\n")
        lines.append("The following design tradeoffs were identified:\n\n")
        for tradeoff in response.tradeoffs:
            lines.append(f"- {tradeoff}\n")
    
    # Usage stats
    if response.usage:
        lines.append("\n### Resource Usage\n")
        lines.append(f"- **LLM Calls:** {response.usage.llm_calls}\n")
        lines.append(f"- **Input Tokens:** {response.usage.tokens_in:,}\n")
        lines.append(f"- **Output Tokens:** {response.usage.tokens_out:,}\n")
        lines.append(f"- **Total Tokens:** {response.usage.total_tokens:,}\n")
        lines.append(f"- **Estimated Cost:** ${response.usage.cost_usd:.4f}\n")
    

    
    return "".join(lines)

def display_response(response):
    """Display response similar to CLI output."""
    # 1. Output
    st.markdown(response.output)
    
    # 2. V2 Regression Analysis
    if hasattr(response, 'regression_analysis') and response.regression_analysis:
        reg = response.regression_analysis
        status_text = "REGRESSION DETECTED" if reg.is_worse else "Improvement / Stable"
        
        st.markdown("### 📉 V2 Regression Analysis")
        with st.container(border=True):
             if reg.is_worse:
                  st.error(f"{status_text} vs Base Run: {reg.baseline_run_id[:8]}")
             else:
                  st.success(f"{status_text} vs Base Run: {reg.baseline_run_id[:8]}")
             
             cols = st.columns(4)
             
             # Coverage Delta
             cov_sign = "+" if reg.coverage_delta >= 0 else ""
             cols[0].metric("Coverage Delta", f"{cov_sign}{int(reg.coverage_delta * 100)}%")
             
             # Issues Delta
             cols[1].metric("Issues Delta", f"{reg.issues_delta}", delta=f"{reg.issues_delta}", delta_color="inverse")
             
             # Constraints Delta
             cols[2].metric("Constraints Delta", f"{reg.constraints_delta}", delta=f"{reg.constraints_delta}", delta_color="inverse")

             # Blockers/Majors
             cols[3].markdown(f"**Blockers:** {reg.blocker_delta:+d}  \n**Majors:** {reg.major_delta:+d}")

    # 3. V1 Evaluation
    # Check if we have evaluation data
    has_eval = response.confidence or response.coverage_score is not None or getattr(response, 'evaluation_summary', None)
    
    if has_eval:
        st.markdown("### 🎯 V1 Evaluation")
        with st.container(border=True):
            cols = st.columns(2)
            # Confidence
            if response.confidence:
                conf_colors = {"low": "🔴", "medium": "🟡", "high": "🟢"}
                conf_emoji = conf_colors.get(response.confidence, "⚪")
                cols[0].markdown(f"**Confidence:** {conf_emoji} {response.confidence.upper()}")
            
            # Coverage
            if response.coverage_score is not None:
                coverage_pct = int(response.coverage_score * 100)
                # Color logic from CLI
                if coverage_pct >= 83: cov_color = "🟢"
                elif coverage_pct >= 50: cov_color = "🟡"
                else: cov_color = "🔴"
                cols[1].markdown(f"**Coverage:** {cov_color} **{coverage_pct}%** ({int(response.coverage_score * 6)}/6 perspectives)")
            
            # Issue Breakdown
            if hasattr(response, 'evaluation_summary') and response.evaluation_summary:
                eval_sum = response.evaluation_summary
                st.markdown("---")
                st.markdown("**Issue Breakdown:**")
                
                blockers = eval_sum.get('blockers', 0)
                majors = eval_sum.get('majors', 0)
                minors = eval_sum.get('minors', 0)
                total = eval_sum.get('total_issues', 0)

                i_cols = st.columns(3)
                i_cols[0].markdown(f"🚫 **Blockers:** {blockers}")
                i_cols[1].markdown(f"⚠️ **Majors:** {majors}")
                i_cols[2].markdown(f"ℹ️ **Minors:** {minors}")
                
                if total == 0:
                    st.markdown("✨ No issues found")
                
                missing = eval_sum.get('missing_perspectives', [])
                if missing:
                    st.warning(f"Missing Perspectives: {', '.join(missing)}")
                covered = eval_sum.get('covered_perspectives', [])
                if covered:
                    st.success(f"Covered Perspectives: {', '.join(covered)}")

    # 3. Tradeoffs
    if response.tradeoffs:
        st.markdown("### ⚖️ Design Tradeoffs")
        with st.container(border=True):
            for t in response.tradeoffs:
                st.markdown(f"• {t}")

    # 4. Analysis & Rationale
    if response.reasoning_trace or response.comparison_analysis:
        st.markdown("### 🧠 Analysis & Rationale")
        if response.reasoning_trace:
             with st.expander("Reasoning Trace"):
                 st.markdown(response.reasoning_trace)
        if response.comparison_analysis:
             with st.expander("Comparison Analysis"):
                 st.markdown(response.comparison_analysis)

    # 5. Assumptions
    if response.assumptions:
         st.markdown("### 📋 Assumptions")
         with st.container(border=True):
            for a in response.assumptions:
                st.markdown(f"• {a}")

    # 5. V3 Signals
    # Verification Report
    if hasattr(response, 'verification_report') and response.verification_report:
        report = response.verification_report
        st.markdown("### 🛡️ Constraints Verification (V3)")
        with st.container(border=True):
             # Metric
             pct = int(report.coverage_score * 100)
             color = "🟢" if pct == 100 else "🟡" if pct > 50 else "🔴"
             st.markdown(f"**Verification Coverage:** {color} **{pct}%**")
             
             with st.expander("Detailed Checks"):
                 for check in report.checks:
                     icon = {"pass": "✅", "fail": "❌", "unverified": "❓"}.get(check.status, "❓")
                     st.markdown(f"**{icon} {check.status.upper()}**: {check.constraint}")
                     if check.evidence:
                         st.caption(f"Evidence: {check.evidence}")

    # Structured Issues (Prioritize over legacy known_issues)
    if hasattr(response, 'structured_issues') and response.structured_issues:
        st.markdown("### ⚠️ Known Issues Registry (V3)")
        for i, issue in enumerate(response.structured_issues):
            with st.expander(f"{i+1}. {issue.issue}"):
                st.markdown(f"**Impact:** {issue.impact}")
                st.markdown(f"**Mitigation:** {issue.mitigation}")
                st.markdown(f"**Verification:** {issue.verification_step}")
    elif response.known_issues:
         st.markdown("### ⚠️ Known Issues")
         with st.container(border=True):
            for i in response.known_issues:
                st.markdown(f"• {i}")

    # 6. Usage
    if response.usage:
        st.markdown("### 📊 Usage")
        with st.container(border=True):
            u = response.usage
            st.text(f"LLM Calls: {u.llm_calls}")
            st.text(f"Tokens: {u.tokens_in:,} in / {u.tokens_out:,} out ({u.total_tokens:,} total)")
            st.text(f"Cost: ${u.cost_usd:.4f}")

    # 7. Run ID
    st.caption(f"Run ID: {response.run_id}")

def run_zeus_ui(prompt, mode, constraints, context, file_uploads, human_suggestions=None, prior_solutions=None):
    
    # Process file uploads
    context_parts = []
    if context:
        context_parts.append(context)
        
    if file_uploads:
        for uploaded_file in file_uploads:
            # uploaded_file is a BytesIO-like object with a .name attribute
            try:
                name = uploaded_file.name
                content = read_file_content(uploaded_file, filename=name)
                context_parts.append(content)
                    
            except ImportError as e:
                st.error(f"Missing dependency for {uploaded_file.name}: {e}")
            except Exception as e:
                st.error(str(e))

    combined_context = "\n\n".join(context_parts) if context_parts else None
    
    status_container = st.empty()
    
    async def _run():
        def on_progress(msg):
            status_container.info(f"🚀 {msg}")
            
        return await run_zeus(
            prompt=prompt,
            mode=mode,
            constraints=constraints,
            context=combined_context,
            human_suggestions=human_suggestions,
            prior_solutions=prior_solutions,
            model=None,
            on_progress=on_progress,
            max_llm_calls=max_llm_calls,
            total_run_timeout=total_timeout
        )

    try:
        response = asyncio.run(_run())
        status_container.empty()
        return response
    except Exception as e:
        status_container.error(f"Error: {e}")
        return None

tab1, tab2, tab3 = st.tabs(["Design Brief", "Target Solution", "History"])

with tab1:
    st.header("Generate Design Brief")
    brief_prompt = st.text_area("Idea / Problem Statement", height=150, placeholder="Describe your idea or problem...")
    brief_files = st.file_uploader("Context Files", accept_multiple_files=True, type=["md", "txt", "pdf", "docx"], key="brief_files")
    
    col1, col2 = st.columns(2)
    with col1:
        brief_constraints = st.text_area("Constraints (one per line)", placeholder="- Must be open source\n- Must use Python", help="Specific constraints the design must adhere to.")
    with col2:
        brief_context = st.text_area("Additional Context (Text)", placeholder="Paste any extra info here...")

    brief_suggestions = st.text_area("Human Suggestions (Optional)", placeholder="- Consider using X\n- Avoid Y", help="Guidance or candidate ideas.")
    brief_priors = st.text_area("Prior Solutions (Optional)", placeholder="Content of prior solutions...", help="Prior solution content to improve upon.")
    
    if st.button("Generate Brief", type="primary"):
        if not brief_prompt:
            st.warning("Please provide a prompt.")
        else:
            constraints_list = [c.strip() for c in brief_constraints.split("\n") if c.strip()]
            suggestions_list = [s.strip() for s in brief_suggestions.split("\n") if s.strip()]
            priors_list = [p.strip() for p in brief_priors.split("\n") if p.strip()] if brief_priors else []
            
            response = run_zeus_ui(brief_prompt, "brief", constraints_list, brief_context, brief_files, suggestions_list, priors_list)
            
            if response:
                st.session_state.brief_response = response

    if "brief_response" in st.session_state:
            response = st.session_state.brief_response
            st.success("Brief Generated!")
            
            # Prepare download content with evaluation summary
            download_content = response.output + format_evaluation_summary(response)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download Brief",
                    data=download_content,
                    file_name=f"design_brief_{response.run_id}.md",
                    mime="text/markdown"
                )
            with col2:
                if st.button("Set as Baseline", key=f"base_brief_{response.run_id}"):
                     p = get_persistence()
                     p.save_baseline(response.run_id, "baseline_brief")
                     st.success("Saved as baseline_brief")
            
            st.divider()
            display_response(response)

with tab2:
    st.header("Generate Target Solution")
    sol_prompt = st.text_area("Design Brief Content", height=300, placeholder="Paste the design brief here...")
    sol_file = st.file_uploader("Or upload Design Brief", type=["md", "txt"], key="sol_file")
    sol_files = st.file_uploader("Context Files", accept_multiple_files=True, type=["md", "txt", "pdf", "docx"], key="sol_files")
    
    if sol_file:
        sol_prompt = sol_file.getvalue().decode("utf-8")
    
    col1, col2 = st.columns(2)
    with col1:
        sol_constraints = st.text_area("Constraints (one per line)", placeholder="- Kubernetes deployment\n- Use PostgreSQL", key="sol_constraints")
    with col2:
        sol_context = st.text_area("Additional Context (Text)", placeholder="Paste any extra info here...", key="sol_context")
    
    sol_suggestions = st.text_area("Human Suggestions (Optional)", placeholder="- Use microservices\n- Event sourcing", key="sol_suggestions")
    sol_priors = st.text_area("Prior Solutions (Optional)", placeholder="Prior architecture content...", key="sol_priors")

    if st.button("Generate Solution", type="primary"):
        if not sol_prompt:
            st.warning("Please provide a design brief.")
        else:
            constraints_list = [c.strip() for c in sol_constraints.split("\n") if c.strip()]
            suggestions_list = [s.strip() for s in sol_suggestions.split("\n") if s.strip()]
            priors_list = [p.strip() for p in sol_priors.split("\n") if p.strip()] if sol_priors else []
            
            response = run_zeus_ui(sol_prompt, "solution", constraints_list, sol_context, sol_files, suggestions_list, priors_list)
            
            if response:
                st.session_state.sol_response = response

    if "sol_response" in st.session_state:
        response = st.session_state.sol_response
        st.success("Solution Generated!")
        
        # Prepare download content with evaluation summary
        download_content = response.output + format_evaluation_summary(response)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Solution",
                data=download_content,  
                file_name=f"solution_{response.run_id}.md",
                mime="text/markdown"
            )
        with col2:
            if st.button("Set as Baseline", key=f"base_sol_{response.run_id}"):
                    p = get_persistence()
                    p.save_baseline(response.run_id, "baseline_solution")
                    st.success("Saved as baseline_solution")
        
        st.divider()
        display_response(response)

with tab3:
    st.header("Recent Runs")
    if st.button("Refresh History"):
        st.rerun()

    try:
        persistence = get_persistence()
        runs = persistence.list_runs(limit=20)
        
        if not runs:
             st.info("No runs found.")
        
        for run in runs:
            status_icon = "✅" if run['has_response'] else "❌"
            mode_icon = "Brief Solution : " if run['mode'] == "brief" else "Target Solution : "
            
            with st.expander(f"{status_icon} {mode_icon} {run['timestamp']} - {run['run_id'][:8]}"):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Mode:** {run['mode']}")
                c2.write(f"**ID:** {run['run_id']}")
                
                if run.get('errors'):
                    st.error(f"Errors: {run['errors']}")
                
                download_col1, download_col2 = st.columns(2)
                
                with download_col1:
                    if st.button("View Output", key=f"view_{run['run_id']}"):
                        record = persistence.load(run['run_id'])
                        if record and record.final_response:
                            st.markdown("---")
                            display_response(record.final_response)
                        else:
                            st.warning("No output available for this run.")
    except Exception as e:
        st.error(f"Error loading history: {e}")
