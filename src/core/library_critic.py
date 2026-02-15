"""Library Critic - Phase 4: Library-Informed Critique."""

import asyncio
import logging
from src.models.schemas import (
    LibraryCritiqueIssue, LibraryCritiqueFinding, LibraryCritiqueResult,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.library_critique import LibraryCritiquePrompts
from src.core.library_loader import LibraryLoader

logger = logging.getLogger(__name__)


class LibraryCritic:
    """Runs parallel library-informed critics against a unified draft."""

    def __init__(self, llm_client: OpenRouterClient, library_loader: LibraryLoader):
        self.llm = llm_client
        self.library_loader = library_loader

    async def critique(
        self,
        draft: str,
        eval_criteria: str = "",
    ) -> tuple[LibraryCritiqueResult, dict[str, int]]:
        """Run all library critics in parallel.

        Args:
            draft: The unified draft to critique.
            eval_criteria: Evaluation criteria text.

        Returns:
            Tuple of (LibraryCritiqueResult, aggregated usage stats).
        """
        # Determine which libraries have content
        available_libs = self.library_loader.get_all()
        if not available_libs:
            logger.warning("No libraries available for critique")
            return LibraryCritiqueResult(), {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}

        # Run critics in parallel
        tasks = []
        critic_names = []
        for lib_name, lib_content in available_libs.items():
            if lib_content and lib_name in LibraryCritiquePrompts.CRITIQUE_TEMPLATES:
                tasks.append(self._run_single_critic(draft, lib_name, lib_content, eval_criteria))
                critic_names.append(lib_name)

        logger.info(f"Launching {len(tasks)} library critics in parallel: {critic_names}")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        findings = []
        all_issues = []
        total_usage = {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Critic '{critic_names[i]}' failed: {result}")
                continue
            finding, usage = result
            findings.append(finding)
            all_issues.extend(finding.issues)
            total_usage["tokens_in"] += usage.get("tokens_in", 0)
            total_usage["tokens_out"] += usage.get("tokens_out", 0)
            total_usage["llm_calls"] += 1
            issue_summary = f"{sum(1 for x in finding.issues if x.severity=='blocker')}B/" \
                            f"{sum(1 for x in finding.issues if x.severity=='major')}M/" \
                            f"{sum(1 for x in finding.issues if x.severity=='minor')}m"
            logger.info(f"Critic '{finding.library_name}' done — coverage {finding.coverage_pct:.0f}%, "
                         f"issues: {issue_summary}")

        # Count by severity
        blocker_count = sum(1 for i in all_issues if i.severity == "blocker")
        major_count = sum(1 for i in all_issues if i.severity == "major")
        minor_count = sum(1 for i in all_issues if i.severity == "minor")

        logger.info(f"All critics complete — total issues: {blocker_count} blockers, "
                     f"{major_count} major, {minor_count} minor")

        return LibraryCritiqueResult(
            findings=findings,
            all_issues=all_issues,
            blocker_count=blocker_count,
            major_count=major_count,
            minor_count=minor_count,
        ), total_usage

    async def _run_single_critic(
        self,
        draft: str,
        library_name: str,
        library_content: str,
        eval_criteria: str,
    ) -> tuple[LibraryCritiqueFinding, dict[str, int]]:
        """Run a single library critic."""
        logger.info(f"Critic '{library_name}': preparing prompt ({len(library_content)} chars library)...")
        template = LibraryCritiquePrompts.CRITIQUE_TEMPLATES[library_name]
        questions = "\n".join(f"- {q}" for q in template["questions"])

        # Truncate library content if too large
        if len(library_content) > 30000:
            library_content = library_content[:30000] + "\n\n[... truncated ...]"

        prompt = LibraryCritiquePrompts.CRITIQUE.format(
            critic_name=template["name"],
            draft=draft,
            library_name=library_name,
            library_content=library_content,
            eval_criteria=eval_criteria or "Not provided",
            questions=questions,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=LibraryCritiquePrompts.SYSTEM,
            temperature=0.5,
        )

        # Parse issues
        issues = []
        for issue_data in response.get("issues", []):
            severity = issue_data.get("severity", "minor")
            if severity not in ("blocker", "major", "minor"):
                severity = "minor"
            issues.append(LibraryCritiqueIssue(
                severity=severity,
                description=issue_data.get("description", ""),
                suggested_fix=issue_data.get("suggested_fix"),
            ))

        finding = LibraryCritiqueFinding(
            library_name=library_name,
            violations=response.get("violations", []),
            embodied=response.get("embodied", []),
            missing=response.get("missing", []),
            coverage_pct=min(100.0, max(0.0, float(response.get("coverage_pct", 0)))),
            issues=issues,
        )

        return finding, usage
