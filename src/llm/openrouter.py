"""OpenRouter LLM client for Zeus."""

import asyncio
import os
import json
import logging
import httpx
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Retry configuration
# ---------------------------------------------------------------------------

_RETRY_MAX_ATTEMPTS = 3
_RETRY_BASE_DELAY = 1.5   # seconds; doubles each attempt
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class OpenRouterClient:
    """Async client for the OpenRouter API.

    Wraps every LLM call with:
    - Configurable per-call timeout
    - Automatic retry (up to 3×) with exponential back-off on transient
      failures (timeouts, 429, 5xx).
    - JSON-repair pass on parse failure.
    - Defensive content validation so callers never receive None.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODELS_URL = "https://openrouter.ai/api/v1/models"
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
            timeout: Request timeout in seconds (applied per attempt).
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

    # ------------------------------------------------------------------
    # Public generation methods
    # ------------------------------------------------------------------

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        json_mode: bool = False,
        model: str | None = None,
    ) -> tuple[str, dict[str, int]]:
        """Generate a response from the LLM with automatic retry.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            json_mode: Whether to request JSON output.

        Returns:
            Tuple of (response_content, usage_stats).

        Raises:
            OpenRouterError: If all retry attempts fail.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": model or self.model,
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

        logger.info(
            f"LLM request → {payload['model']} | temp={temperature} max_tokens={max_tokens} "
            f"json_mode={json_mode} msgs={len(messages)}"
        )

        last_error: Exception | None = None

        for attempt in range(1, _RETRY_MAX_ATTEMPTS + 1):
            try:
                content, usage_stats = await self._single_request(
                    payload, headers, attempt
                )
                return content, usage_stats

            except OpenRouterRateLimitError as e:
                last_error = e
                if attempt < _RETRY_MAX_ATTEMPTS:
                    delay = _RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    logger.warning(
                        f"Rate limited (attempt {attempt}/{_RETRY_MAX_ATTEMPTS}) — "
                        f"retrying in {delay:.1f}s: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Rate limit persisted after {_RETRY_MAX_ATTEMPTS} attempts")

            except OpenRouterTransientError as e:
                last_error = e
                if attempt < _RETRY_MAX_ATTEMPTS:
                    delay = _RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    logger.warning(
                        f"Transient error (attempt {attempt}/{_RETRY_MAX_ATTEMPTS}) — "
                        f"retrying in {delay:.1f}s: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Transient error persisted after {_RETRY_MAX_ATTEMPTS} attempts")

            except OpenRouterTimeoutError as e:
                last_error = e
                if attempt < _RETRY_MAX_ATTEMPTS:
                    delay = _RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    logger.warning(
                        f"Request timeout (attempt {attempt}/{_RETRY_MAX_ATTEMPTS}) — "
                        f"retrying in {delay:.1f}s"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Request timed out after {_RETRY_MAX_ATTEMPTS} attempts")

            except (OpenRouterError, Exception):
                # Non-retryable: re-raise immediately
                raise

        # All retries exhausted
        raise last_error or OpenRouterError("All retry attempts failed")

    async def generate_json(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        model: str | None = None,
    ) -> tuple[dict, dict[str, int]]:
        """Generate a JSON response from the LLM.

        Includes one repair pass on parse failure before raising an error.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            Tuple of (parsed_json, total_usage_stats).
        """
        content, usage = await self.generate(
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
            model=model,
        )

        # First attempt: try to parse the response
        cleaned = self._clean_json_response(content)
        parse_error = None

        try:
            parsed = json.loads(cleaned)
            return parsed, usage
        except json.JSONDecodeError as e:
            parse_error = e

        # Repair pass: ask LLM to fix the malformed JSON
        logger.warning(f"JSON parse failed — attempting LLM repair pass: {parse_error}")
        repair_prompt = self._build_repair_prompt(content, str(parse_error))

        try:
            repaired_content, repair_usage = await self.generate(
                prompt=repair_prompt,
                system="You are a JSON repair assistant. Output only valid JSON, no explanations.",
                temperature=0.0,  # Deterministic for repair
                max_tokens=max_tokens,
                json_mode=True,
                model=model,
            )

            # Combine usage stats
            total_usage = {
                "tokens_in": usage.get("tokens_in", 0) + repair_usage.get("tokens_in", 0),
                "tokens_out": usage.get("tokens_out", 0) + repair_usage.get("tokens_out", 0),
            }

            cleaned_repair = self._clean_json_response(repaired_content)
            parsed = json.loads(cleaned_repair)
            return parsed, total_usage

        except (json.JSONDecodeError, OpenRouterError) as repair_error:
            raise OpenRouterError(
                f"Failed to parse JSON response after repair attempt. "
                f"Original error: {parse_error}. Repair error: {repair_error}"
            ) from parse_error

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _single_request(
        self,
        payload: dict[str, Any],
        headers: dict[str, str],
        attempt: int,
    ) -> tuple[str, dict[str, int]]:
        """Execute a single HTTP request and return (content, usage_stats).

        Raises typed subclasses of OpenRouterError so callers can decide
        whether to retry.
        """
        import time as _time
        _t0 = _time.monotonic()

        try:
            response = await self._client.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
            )

            # Surface HTTP errors with specific types
            if response.status_code == 429:
                raise OpenRouterRateLimitError(
                    f"Rate limited (HTTP 429): {response.text[:200]}"
                )
            if response.status_code in _RETRYABLE_STATUS_CODES:
                raise OpenRouterTransientError(
                    f"Transient server error (HTTP {response.status_code}): {response.text[:200]}"
                )
            response.raise_for_status()

            data = response.json()

            # Defensive: guard against missing/empty choices
            choices = data.get("choices")
            if not choices or not isinstance(choices, list):
                raise OpenRouterError(
                    f"Invalid response: missing or empty 'choices' (attempt {attempt}). "
                    f"Response keys: {list(data.keys())}"
                )

            message = choices[0].get("message") or {}
            content = message.get("content")
            if content is None:
                # Some models return finish_reason='content_filter' with no content
                finish_reason = choices[0].get("finish_reason", "unknown")
                raise OpenRouterError(
                    f"No content in response (finish_reason={finish_reason!r}). "
                    "The model may have filtered this request."
                )

            usage = data.get("usage", {})
            usage_stats = {
                "tokens_in": usage.get("prompt_tokens", 0),
                "tokens_out": usage.get("completion_tokens", 0),
            }

            elapsed = _time.monotonic() - _t0
            logger.info(
                f"LLM response ← {usage_stats['tokens_in']:,} in / "
                f"{usage_stats['tokens_out']:,} out tokens "
                f"({elapsed:.1f}s)"
            )

            return content, usage_stats

        except httpx.TimeoutException as e:
            logger.error(f"LLM timeout after {self.timeout}s (attempt {attempt}): {e}")
            raise OpenRouterTimeoutError(
                f"Request timed out after {self.timeout}s: {str(e)}"
            ) from e
        except httpx.HTTPStatusError as e:
            logger.error(
                f"LLM HTTP error {e.response.status_code} (attempt {attempt}): "
                f"{e.response.text[:200]}"
            )
            raise OpenRouterError(
                f"API request failed: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            logger.error(f"LLM request error (attempt {attempt}): {e}")
            raise OpenRouterTransientError(f"Network request failed: {str(e)}") from e
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"LLM response parse error (attempt {attempt}): {e}")
            raise OpenRouterError(f"Invalid response format: {str(e)}") from e

    def _clean_json_response(self, content: str) -> str:
        """Clean JSON response by stripping markdown code blocks."""
        cleaned = content.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)
        return cleaned

    def _build_repair_prompt(self, malformed_json: str, error_message: str) -> str:
        """Build a prompt to repair malformed JSON."""
        return (
            f"The following JSON is malformed and failed to parse:\n\n"
            f"```\n{malformed_json}\n```\n\n"
            f"Parse error: {error_message}\n\n"
            "Please fix the JSON and return only the corrected, valid JSON object. "
            "Do not include any explanation or markdown formatting."
        )

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Model listing
    # ------------------------------------------------------------------

    @classmethod
    async def fetch_text_models(
        cls,
        api_key: str | None = None,
        timeout: float = 20.0,
    ) -> list[str]:
        """Fetch available text-input/text-output model IDs from OpenRouter.

        Returns:
            Sorted list of model IDs that support text input and output.

        Raises:
            OpenRouterError: If model retrieval or parsing fails.
        """
        models_with_meta = await cls.fetch_text_models_with_meta(
            api_key=api_key, timeout=timeout
        )
        return [m["id"] for m in models_with_meta]

    @classmethod
    async def fetch_text_models_with_meta(
        cls,
        api_key: str | None = None,
        timeout: float = 20.0,
    ) -> list[dict[str, Any]]:
        """Fetch text-capable models with rich metadata.

        Returns a list of dicts, each with:
            - ``id``: model identifier string (e.g. ``"anthropic/claude-3-5-sonnet"``)
            - ``name``: human-readable display name
            - ``context_length``: max context window in tokens (int, 0 if unknown)
            - ``description``: short description (may be empty)

        The list is sorted by ``id`` ascending.

        Raises:
            OpenRouterError: If model retrieval or parsing fails.
        """
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/zeus-agent",
            "X-Title": "Zeus Design Agent",
        }

        resolved_api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if resolved_api_key:
            headers["Authorization"] = f"Bearer {resolved_api_key}"

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(cls.MODELS_URL, headers=headers)
                response.raise_for_status()
                payload = response.json()
        except httpx.TimeoutException as e:
            raise OpenRouterTimeoutError(
                f"Model list request timed out after {timeout}s"
            ) from e
        except httpx.HTTPStatusError as e:
            raise OpenRouterError(
                f"Model list request failed: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise OpenRouterError(f"Model list request failed: {str(e)}") from e
        except json.JSONDecodeError as e:
            raise OpenRouterError(
                f"Invalid model list response format: {str(e)}"
            ) from e

        data = payload.get("data")
        if not isinstance(data, list):
            raise OpenRouterError("Invalid model list response: missing 'data' array")

        models: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            model_id = item.get("id")
            if not isinstance(model_id, str) or not model_id.strip():
                continue
            if not cls._supports_text_io(item):
                continue

            context_length = item.get("context_length", 0)
            try:
                context_length = int(context_length or 0)
            except (TypeError, ValueError):
                context_length = 0

            models.append({
                "id": model_id.strip(),
                "name": item.get("name") or model_id.strip(),
                "context_length": context_length,
                "description": (item.get("description") or "").strip(),
            })

        models.sort(key=lambda m: m["id"])
        return models

    @staticmethod
    def _supports_text_io(model_data: dict[str, Any]) -> bool:
        """Return True when model metadata indicates text input and text output support."""
        architecture = model_data.get("architecture")
        if not isinstance(architecture, dict):
            architecture = {}

        input_modalities = architecture.get("input_modalities")
        output_modalities = architecture.get("output_modalities")

        if not isinstance(input_modalities, list):
            input_modalities = model_data.get("input_modalities")
        if not isinstance(output_modalities, list):
            output_modalities = model_data.get("output_modalities")

        modalities = model_data.get("modalities")
        if not isinstance(modalities, list):
            modalities = []

        in_set = {str(m).lower() for m in (input_modalities or [])}
        out_set = {str(m).lower() for m in (output_modalities or [])}
        modal_set = {str(m).lower() for m in modalities}

        if in_set and out_set:
            return "text" in in_set and "text" in out_set

        if in_set or out_set:
            merged = in_set | out_set
            return "text" in merged

        return "text" in modal_set

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

class OpenRouterError(Exception):
    """Base error for OpenRouter API failures."""
    pass


class OpenRouterTimeoutError(OpenRouterError):
    """Raised when an OpenRouter request times out."""
    pass


class OpenRouterRateLimitError(OpenRouterError):
    """Raised on HTTP 429 rate-limit responses."""
    pass


class OpenRouterTransientError(OpenRouterError):
    """Raised on transient server errors (5xx, network failures) that are safe to retry."""
    pass
