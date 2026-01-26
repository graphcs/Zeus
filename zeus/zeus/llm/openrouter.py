"""OpenRouter LLM client for Zeus."""

import os
import json
import httpx
from typing import Any


class OpenRouterClient:
    """Client for OpenRouter API."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "anthropic/claude-sonnet-4"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        timeout: float = 120.0,
    ):
        """Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key. Defaults to OPENROUTER_API_KEY env var.
            model: Model to use for generation.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key required. Set OPENROUTER_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.model = model
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        json_mode: bool = False,
    ) -> tuple[str, dict[str, int]]:
        """Generate a response from the LLM.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            json_mode: Whether to request JSON output.

        Returns:
            Tuple of (response_content, usage_stats).

        Raises:
            OpenRouterError: If the API request fails.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/zeus-agent",
            "X-Title": "Zeus Design Agent",
        }

        try:
            response = await self._client.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            usage_stats = {
                "tokens_in": usage.get("prompt_tokens", 0),
                "tokens_out": usage.get("completion_tokens", 0),
            }

            return content, usage_stats

        except httpx.TimeoutException as e:
            raise OpenRouterTimeoutError(f"Request timed out after {self.timeout}s: {str(e)}") from e
        except httpx.HTTPStatusError as e:
            raise OpenRouterError(f"API request failed: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise OpenRouterError(f"Request failed: {str(e)}") from e
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise OpenRouterError(f"Invalid response format: {str(e)}") from e

    async def generate_json(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> tuple[dict, dict[str, int]]:
        """Generate a JSON response from the LLM.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            Tuple of (parsed_json, usage_stats).
        """
        content, usage = await self.generate(
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
        )

        try:
            # Strip markdown code blocks if present
            cleaned = content.strip()
            if cleaned.startswith("```"):
                # Remove opening ```json or ``` line
                lines = cleaned.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                # Remove closing ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines)

            parsed = json.loads(cleaned)
            return parsed, usage
        except json.JSONDecodeError as e:
            raise OpenRouterError(f"Failed to parse JSON response: {str(e)}") from e

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class OpenRouterError(Exception):
    """Error from OpenRouter API."""
    pass


class OpenRouterTimeoutError(OpenRouterError):
    """Timeout error from OpenRouter API."""
    pass
