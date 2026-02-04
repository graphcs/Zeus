"""Issue Structurer - V3 Structured Known Issues."""

import json
import logging
from src.models.schemas import StructuredKnownIssue
from src.llm.openrouter import OpenRouterClient
from src.prompts.issue_structurer import IssueStructurePrompts

logger = logging.getLogger(__name__)

class IssueStructurer:
    """Converts unstructured issue lists into structured records."""

    def __init__(self, client: OpenRouterClient):
        self.client = client

    async def structure_issues(self, raw_issues: list[str]) -> tuple[list[StructuredKnownIssue], dict[str, int]]:
        """Convert raw issue strings to structured issues.
        
        Args:
            raw_issues: List of issue descriptions strings.
            
        Returns:
            Tuple of (List of StructuredKnownIssue objects, usage_stats).
        """
        empty_usage = {"tokens_in": 0, "tokens_out": 0}

        if not raw_issues:
            return [], empty_usage

        try:
            # Prepare prompt
            issues_text = "\n".join(f"- {issue}" for issue in raw_issues)
            prompt = IssueStructurePrompts.STRUCTURE_ISSUES.format(
                issues_list=issues_text
            )

            # Note: generate returns (content, usage)
            data, usage = await self.client.generate_json(
                system=IssueStructurePrompts.SYSTEM,
                prompt=prompt
            )

            # Parse results
            issues_data = data.get("structured_issues", [])
            
            structured_issues = []
            for item in issues_data:
                structured_issues.append(StructuredKnownIssue(
                    issue=item.get("issue", "Unknown issue"),
                    impact=item.get("impact", "Unknown impact"),
                    mitigation=item.get("mitigation", "TBD"),
                    verification_step=item.get("verification_step", "TBD")
                ))

            return structured_issues, usage

        except Exception as e:
            logger.error(f"Issue structuring failed: {e}")
            # Fallback: wrap raw issues
            return [
                StructuredKnownIssue(
                    issue=issue,
                    impact="Unknown (Structuring failed)",
                    mitigation="TBD",
                    verification_step="TBD"
                )
                for issue in raw_issues
            ], empty_usage
