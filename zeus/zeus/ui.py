
import streamlit as st
import asyncio
from pathlib import Path
import sys
from zeus.core.run_controller import run_zeus
from zeus.core.persistence import Persistence
import pypdf
import docx
import pandas as pd




st.set_page_config(
    page_title="Zeus - Design Team Agent",
    layout="wide",
)

st.title("Zeus - Design Team Agent")
with st.sidebar:  
    st.toggle("Advanced Budget Settings", key="show_budget")
    if st.session_state.get("show_budget"):
        max_llm_calls = st.number_input("Max LLM Calls", value=6, min_value=1)
        total_timeout = st.number_input("Total Timeout (s)", value=300, min_value=60)
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
    
    # Header
    lines.append("\n---\n")
    lines.append("## Evaluation Summary\n")
    
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

def run_zeus_ui(prompt, mode, constraints, context, file_uploads):
    
    # Process file uploads
    context_parts = []
    if context:
        context_parts.append(context)
        
    if file_uploads:
        for uploaded_file in file_uploads:
            # uploaded_file is a BytesIO-like object with a .name attribute
            try:
                name = uploaded_file.name
                lower_name = name.lower()
                
                if lower_name.endswith(".pdf"):
                    reader = pypdf.PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    context_parts.append(f"--- File: {name} ---\n{text}\n")
                    
                elif lower_name.endswith((".docx", ".doc")):
                    doc = docx.Document(uploaded_file)
                    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    context_parts.append(f"--- File: {name} ---\n{text}\n")
                    
                else:
                    # Text based (md, txt, etc) using utf-8
                    stringio = uploaded_file.getvalue().decode("utf-8")
                    context_parts.append(f"--- File: {name} ---\n{stringio}\n")
                    
            except ImportError as e:
                st.error(f"Missing dependency for {uploaded_file.name}: {e}")
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")

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
            model=None,
            on_progress=on_progress,
            max_llm_calls=max_llm_calls,
            total_run_timeout=total_timeout
        )

    try:
        with st.spinner("Zeus is thinking..."):
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
        
    
    if st.button("Generate Brief", type="primary"):
        if not brief_prompt:
            st.warning("Please provide a prompt.")
        else:
            constraints_list = [c.strip() for c in brief_constraints.split("\n") if c.strip()]
            response = run_zeus_ui(brief_prompt, "brief", constraints_list, brief_context, brief_files)
            
            if response:
                st.session_state.brief_response = response

    if "brief_response" in st.session_state:
            response = st.session_state.brief_response
            st.success("Brief Generated!")
            
            # Prepare download content with evaluation summary
            download_content = response.output + format_evaluation_summary(response)
            
            st.download_button(
                label="Download Brief (with Evaluation)",
                data=download_content,
                file_name=f"design_brief_{response.run_id}.md",
                mime="text/markdown"
            )
            
            # V1: Evaluation Summary
            eval_col1, eval_col2 = st.columns(2)
            with eval_col1:
                # Confidence badge
                conf_colors = {"low": "🔴", "medium": "🟡", "high": "🟢"}
                conf_emoji = conf_colors.get(response.confidence, "⚪")
                st.metric("Confidence", f"{conf_emoji} {response.confidence.upper()}")
            with eval_col2:
                # Coverage score
                coverage_pct = int(response.coverage_score * 100)
                st.metric("Critique Coverage", f"{coverage_pct}%", 
                         f"{int(response.coverage_score * 6)}/6 perspectives")
            
            # Additional evaluation details
            if hasattr(response, 'evaluation_summary') and response.evaluation_summary:
                eval_sum = response.evaluation_summary
                st.markdown("#### 📊 Detailed Evaluation")
                
                issue_col1, issue_col2, issue_col3, issue_col4 = st.columns(4)
                with issue_col1:
                    st.metric("🚫 Blockers", eval_sum.get('blockers', 0))
                with issue_col2:
                    st.metric("⚠️ Majors", eval_sum.get('majors', 0))
                with issue_col3:
                    st.metric("ℹ️ Minors", eval_sum.get('minors', 0))
                with issue_col4:
                    st.metric("Total Issues", eval_sum.get('total_issues', 0))
                
                # Missing perspectives
                missing = eval_sum.get('missing_perspectives', [])
                if missing:
                    st.warning(f"Missing Perspectives: {', '.join(missing)}")
                
                # Issues by category
                issues_by_cat = eval_sum.get('issues_by_category', {})
                if issues_by_cat:
                    st.markdown("**Issues by Category:**")
                    cat_cols = st.columns(len(issues_by_cat) if len(issues_by_cat) <= 4 else 4)
                    for idx, (cat, count) in enumerate(issues_by_cat.items()):
                        with cat_cols[idx % 4]:
                            st.metric(cat.replace('_', ' ').title(), count)
            
            st.markdown("### Output")
            st.markdown(response.output)
            st.divider()
            
            # V1: Tradeoffs section
            if response.tradeoffs:
                with st.expander("⚖️ Design Tradeoffs", expanded=True):
                    for t in response.tradeoffs:
                        st.write(f"• {t}")
            
            with st.expander("Assumptions & Issues", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("📋 Assumptions")
                    if response.assumptions:
                        for a in response.assumptions:
                            st.write(f"• {a}")
                    else:
                        st.write("No assumptions made.")
                        
                with col_b:
                    st.subheader("⚠️ Known Issues")
                    if response.known_issues:
                        for i in response.known_issues:
                            st.write(f"• {i}")
                    else:
                        st.write("No known issues.")
            
            with st.expander("Usage Stats"):
                u = response.usage
                st.write(f"**LLM Calls:** {u.llm_calls}")
                st.write(f"**Tokens:** {u.tokens_in:,} in / {u.tokens_out:,} out ({u.total_tokens:,} total)")
                st.write(f"**Cost:** ${u.cost_usd:.4f}")
                st.caption(f"Run ID: {response.run_id}")

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
    

    if st.button("Generate Solution", type="primary"):
        if not sol_prompt:
            st.warning("Please provide a design brief.")
        else:
            constraints_list = [c.strip() for c in sol_constraints.split("\n") if c.strip()]
            response = run_zeus_ui(sol_prompt, "solution", constraints_list, sol_context, sol_files)
            
            if response:
                st.session_state.sol_response = response

    if "sol_response" in st.session_state:
        response = st.session_state.sol_response
        st.success("Solution Generated!")
        
        # Prepare download content with evaluation summary
        download_content = response.output + format_evaluation_summary(response)
        
        st.download_button(
            label="Download Solution (with Evaluation)",
            data=download_content,
            file_name=f"solution_{response.run_id}.md",
            mime="text/markdown"
        )
        
        # V1: Evaluation Summary
        eval_col1, eval_col2 = st.columns(2)
        with eval_col1:
            # Confidence badge
            conf_colors = {"low": "🔴", "medium": "🟡", "high": "🟢"}
            conf_emoji = conf_colors.get(response.confidence, "⚪")
            st.metric("Confidence", f"{conf_emoji} {response.confidence.upper()}")
        with eval_col2:
            # Coverage score
            coverage_pct = int(response.coverage_score * 100)
            st.metric("Critique Coverage", f"{coverage_pct}%", 
                     f"{int(response.coverage_score * 6)}/6 perspectives")
        
        # Additional evaluation details
        if hasattr(response, 'evaluation_summary') and response.evaluation_summary:
            eval_sum = response.evaluation_summary
            st.markdown("####  Detailed Evaluation")
            
            issue_col1, issue_col2, issue_col3, issue_col4 = st.columns(4)
            with issue_col1:
                st.metric("🚫 Blockers", eval_sum.get('blockers', 0))
            with issue_col2:
                st.metric("⚠️ Majors", eval_sum.get('majors', 0))
            with issue_col3:
                st.metric("ℹ️ Minors", eval_sum.get('minors', 0))
            with issue_col4:
                st.metric("Total Issues", eval_sum.get('total_issues', 0))
            
            # Missing perspectives
            missing = eval_sum.get('missing_perspectives', [])
            if missing:
                st.warning(f"Missing Perspectives: {', '.join(missing)}")
            
            # Issues by category
            issues_by_cat = eval_sum.get('issues_by_category', {})
            if issues_by_cat:
                st.markdown("**Issues by Category:**")
                cat_cols = st.columns(len(issues_by_cat) if len(issues_by_cat) <= 4 else 4)
                for idx, (cat, count) in enumerate(issues_by_cat.items()):
                    with cat_cols[idx % 4]:
                        st.metric(cat.replace('_', ' ').title(), count)
        
        st.markdown("### Output")
        st.markdown(response.output)
        st.divider()
        
        # V1: Tradeoffs section
        if response.tradeoffs:
            with st.expander("Design Tradeoffs", expanded=True):
                for t in response.tradeoffs:
                    st.write(f"• {t}")
        
        with st.expander("Assumptions & Issues", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("📋 Assumptions")
                if response.assumptions:
                    for a in response.assumptions:
                        st.write(f"• {a}")
                else:
                    st.write("No assumptions made.")
                    
            with col_b:
                st.subheader("⚠️ Known Issues")
                if response.known_issues:
                    for i in response.known_issues:
                        st.write(f"• {i}")
                else:
                    st.write("No known issues.")
        
        with st.expander("Usage Stats"):
            u = response.usage
            st.write(f"**LLM Calls:** {u.llm_calls}")
            st.write(f"**Tokens:** {u.tokens_in:,} in / {u.tokens_out:,} out ({u.total_tokens:,} total)")
            st.write(f"**Cost:** ${u.cost_usd:.4f}")
            st.caption(f"Run ID: {response.run_id}")

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
                            st.markdown(record.final_response.output)
                        else:
                            st.warning("No output available for this run.")
    except Exception as e:
        st.error(f"Error loading history: {e}")
