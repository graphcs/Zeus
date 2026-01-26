"""OpenRouter LLM client for Zeus."""

import os
import json
import httpx
from typing import Any, Type, TypeVar
import re
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


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
        response_format: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, int]]:
        """Generate a response from the LLM.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            response_format: Optional structured output format.

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

        if response_format:
            payload["response_format"] = response_format

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

        except httpx.HTTPStatusError as e:
            raise OpenRouterError(f"API request failed: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise OpenRouterError(f"Request failed: {str(e)}") from e
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise OpenRouterError(f"Invalid response format: {str(e)}") from e

    async def generate_json(
        self,
        prompt: str,
        response_model: Type[BaseModel] | None = None,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> tuple[dict, dict[str, int]]:
        """Generate a JSON response from the LLM.

        Args:
            prompt: User prompt.
            response_model: Pydantic model class for structured output.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            Tuple of (parsed_json, usage_stats).
        """
        response_format = None
        if response_model:
            schema = response_model.model_json_schema()
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": schema,
                    "strict": False
                }
            }

        content, usage = await self.generate(
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )

        try:
            # Clean up response if it contains markdown markers or other text
            content = content.strip()
            match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if match:
                content = match.group(1).strip()
            else:
                # If no markdown, try to find the first '{' and last '}'
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    content = content[start : end + 1]

            parsed = json.loads(content)

            # Validate against model if provided
            if response_model:
                validated = response_model.model_validate(parsed)
                return validated.model_dump(), usage

            return parsed, usage
        except (json.JSONDecodeError, Exception) as e:
            raise OpenRouterError(
                f"Failed to parse or validate JSON response: {str(e)}\n"
                f"Content was: {content[:1000]}"
            ) from e

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
