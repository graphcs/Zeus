"""Tests for Critic V1 category parsing."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from zeus.models.schemas import (
    NormalizedProblem,
    Candidate,
    CritiqueIssue,
    VALID_ISSUE_CATEGORIES,
)
from zeus.core.critic import Critic


class TestCategoryInference:
    """Tests for category inference from role and description."""

    def setup_method(self):
        """Set up test fixtures."""
        mock_client = MagicMock()
        self.critic = Critic(mock_client)

    def test_infer_correctness(self):
        """Test inferring correctness category."""
        category = self.critic._infer_category("test", "This is wrong and has errors")
        assert category == "correctness"

    def test_infer_completeness(self):
        """Test inferring completeness category."""
        category = self.critic._infer_category("scope", "Missing requirements section")
        assert category == "completeness"

    def test_infer_clarity(self):
        """Test inferring clarity category."""
        category = self.critic._infer_category("test", "The description is unclear and ambiguous")
        assert category == "clarity"

    def test_infer_feasibility(self):
        """Test inferring feasibility category."""
        category = self.critic._infer_category("test", "This is unrealistic and infeasible")
        assert category == "feasibility"

    def test_infer_maintainability(self):
        """Test inferring maintainability category."""
        category = self.critic._infer_category("architecture", "Tight coupling creates technical debt")
        assert category == "maintainability"

    def test_infer_performance(self):
        """Test inferring performance category."""
        category = self.critic._infer_category("test", "This will be slow with high latency")
        assert category == "performance"

    def test_infer_security(self):
        """Test inferring security category."""
        category = self.critic._infer_category("test", "Potential SQL injection vulnerability")
        assert category == "security"

    def test_infer_compliance(self):
        """Test inferring compliance category."""
        category = self.critic._infer_category("test", "May violate GDPR regulations")
        assert category == "compliance"

    def test_infer_default(self):
        """Test default category when no keywords match."""
        category = self.critic._infer_category("general", "Some generic observation")
        assert category == "completeness"


class TestCategoryValidation:
    """Tests for category validation in critique parsing."""

    def setup_method(self):
        """Set up test fixtures."""
        mock_client = MagicMock()
        self.critic = Critic(mock_client)

    def test_valid_categories(self):
        """Test that all expected categories are valid."""
        expected = {
            "correctness", "completeness", "clarity", "feasibility",
            "maintainability", "performance", "security", "compliance"
        }
        assert VALID_ISSUE_CATEGORIES == expected

    def test_category_count(self):
        """Test that we have exactly 8 categories."""
        assert len(VALID_ISSUE_CATEGORIES) == 8


class TestCritiqueParsing:
    """Tests for critique parsing with categories."""

    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        client = MagicMock()
        client.generate_json = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_parse_issue_with_valid_category(self, mock_llm_client):
        """Test parsing issue with valid category from LLM."""
        mock_llm_client.generate_json.return_value = (
            {
                "issues": [
                    {
                        "role": "architecture",
                        "severity": "major",
                        "category": "maintainability",
                        "description": "Tight coupling",
                        "suggested_fix": "Use dependency injection",
                    }
                ],
                "constraint_violations": [],
                "missing_perspectives": [],
            },
            {"tokens_in": 100, "tokens_out": 50},
        )

        critic = Critic(mock_llm_client)
        problem = NormalizedProblem(
            problem_statement="Test problem",
            constraints=[],
            output_spec="Test output",
        )
        candidate = Candidate(content="Test content")

        critique, _ = await critic.critique(candidate, problem, "brief")

        # Find the architecture issue (not the meta issue)
        arch_issues = [i for i in critique.issues if i.role == "architecture"]
        assert len(arch_issues) == 1
        assert arch_issues[0].category == "maintainability"

    @pytest.mark.asyncio
    async def test_parse_issue_with_invalid_category_infers(self, mock_llm_client):
        """Test that invalid category triggers inference."""
        mock_llm_client.generate_json.return_value = (
            {
                "issues": [
                    {
                        "role": "security",
                        "severity": "blocker",
                        "category": "invalid_category",  # Invalid
                        "description": "SQL injection vulnerability found",
                    }
                ],
                "constraint_violations": [],
                "missing_perspectives": [],
            },
            {"tokens_in": 100, "tokens_out": 50},
        )

        critic = Critic(mock_llm_client)
        problem = NormalizedProblem(
            problem_statement="Test problem",
            constraints=[],
            output_spec="Test output",
        )
        candidate = Candidate(content="Test content")

        critique, _ = await critic.critique(candidate, problem, "brief")

        # Find the security issue
        sec_issues = [i for i in critique.issues if i.role == "security"]
        assert len(sec_issues) == 1
        # Should infer "security" from description
        assert sec_issues[0].category == "security"

    @pytest.mark.asyncio
    async def test_parse_issue_without_category_infers(self, mock_llm_client):
        """Test that missing category triggers inference."""
        mock_llm_client.generate_json.return_value = (
            {
                "issues": [
                    {
                        "role": "scope",
                        "severity": "minor",
                        # No category field
                        "description": "Missing error handling section",
                    }
                ],
                "constraint_violations": [],
                "missing_perspectives": [],
            },
            {"tokens_in": 100, "tokens_out": 50},
        )

        critic = Critic(mock_llm_client)
        problem = NormalizedProblem(
            problem_statement="Test problem",
            constraints=[],
            output_spec="Test output",
        )
        candidate = Candidate(content="Test content")

        critique, _ = await critic.critique(candidate, problem, "brief")

        # Find the scope issue
        scope_issues = [i for i in critique.issues if i.role == "scope"]
        assert len(scope_issues) == 1
        # Should infer "completeness" from "missing" keyword
        assert scope_issues[0].category == "completeness"
