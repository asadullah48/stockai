import os
from typing import Optional
import httpx


class OllamaClient:
    """
    OllamaClient: Thin wrapper around a local Ollama server's /api/generate endpoint.

    Ollama (https://ollama.com) runs open-weight LLMs entirely on the local machine
    for free, with no API key and no per-token billing - a good fit for a demo
    service that should never depend on a paid, rate-limited third party to boot.

    The client is intentionally defensive: any connection error, timeout, or
    non-200 response returns ``None`` instead of raising, so callers can fall back
    to a deterministic response and the rest of the pipeline never breaks because
    an optional local model isn't running.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: float = 4.0,
    ):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self.timeout_seconds = timeout_seconds

    @property
    def enabled(self) -> bool:
        return os.getenv("OLLAMA_DISABLED", "").lower() not in ("1", "true", "yes")

    def generate(self, prompt: str) -> Optional[str]:
        """Return the model's completion for ``prompt``, or None if unavailable."""
        if not self.enabled:
            return None

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            return text or None
        except (httpx.HTTPError, ValueError, KeyError):
            # Ollama not installed/running, model not pulled, or malformed reply -
            # all treated the same way: the caller falls back to a template.
            return None
