from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:

    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url.rstrip("/")
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._site_url = settings.openrouter_site_url
        self._app_name = settings.openrouter_app_name

    async def chat_completion(self, messages: list[dict[str, str]]) -> str:
        if not self._api_key:
            raise ExternalServiceError("OpenRouter API key not configured")

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        if self._site_url:
            headers["HTTP-Referer"] = self._site_url
        if self._app_name:
            headers["X-Title"] = self._app_name

        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                f"OpenRouter HTTP error: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise ExternalServiceError(f"OpenRouter request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ExternalServiceError(f"OpenRouter invalid response format: {str(e)}")
