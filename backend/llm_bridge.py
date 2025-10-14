"""
LLM bridge supporting two providers:
- OpenAI (cloud) via official SDK, when USE_OLLAMA is not true
- Ollama (local, free) via REST API when USE_OLLAMA=true

Environment variables:
  USE_OLLAMA=true|false
  OLLAMA_BASE_URL=http://127.0.0.1:11434
  OLLAMA_MODEL=qwen2.5:3b-instruct (recommended small) or llama3.2:3b-instruct
  OPENAI_API_KEY=...
  OPENAI_MODEL=gpt-4o-mini (default)
  OPENAI_ORG / OPENAI_ORGANIZATION (optional)
  OPENAI_PROJECT (optional)
"""
import os
from typing import Optional
import json
import requests

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


class LLMAssistant:
    def __init__(self, model: Optional[str] = None):
        # Provider selection
        self.use_ollama = str(os.getenv("USE_OLLAMA", "false")).lower() in {"1","true","yes","on"}
        if self.use_ollama:
            # Ollama configuration
            self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
            self.ollama_model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
            self.client = None
            self.model = self.ollama_model
        else:
            # OpenAI configuration
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key or not OpenAI:
                raise RuntimeError("OPENAI_API_KEY or OpenAI SDK not available")
            # The OpenAI Python SDK v1 reads env for project/org; we only optionally pass organization
            organization = os.getenv("OPENAI_ORG") or os.getenv("OPENAI_ORGANIZATION")
            try:
                if organization:
                    self.client = OpenAI(api_key=self.api_key, organization=organization)
                else:
                    self.client = OpenAI(api_key=self.api_key)
            except Exception as e:  # pragma: no cover
                raise RuntimeError(f"OpenAI client init failed: {e}")
            # Default lightweight, low-cost model
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, prompt: str, max_tokens: int = 400) -> str:
        if self.use_ollama:
            # Call Ollama REST API with simple retries
            url = f"{self.ollama_base}/api/generate"
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": max_tokens}
            }
            last_err = None
            for attempt in range(3):
                try:
                    r = requests.post(url, json=payload, timeout=180)
                    # If Ollama returns a gateway/5xx, try again
                    if r.status_code >= 500:
                        last_err = f"HTTP {r.status_code} {r.reason}"
                        continue
                    r.raise_for_status()
                    data = r.json()
                    return (data.get("response") or "").strip() or ""
                except requests.RequestException as e:
                    last_err = str(e)
                    continue
            return f"[LLM error - Ollama] unavailable after retries: {last_err}. Check that ollama serve is running, the model '{self.ollama_model}' is pulled, and OLLAMA_BASE_URL={self.ollama_base} is reachable."
        else:
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=max_tokens,
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"[LLM error] {e}"
