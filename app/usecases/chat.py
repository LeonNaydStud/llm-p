from app.repositories.chat_messages import ChatMessageRepository
from app.schemas.chat import ChatMessageResponse
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:

    def __init__(
        self,
        chat_repo: ChatMessageRepository,
        llm_client: OpenRouterClient,
    ) -> None:
        self._chat_repo = chat_repo
        self._llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        history = await self._chat_repo.get_recent_messages(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        await self._chat_repo.add_message(user_id, "user", prompt)

        try:
            answer = await self._llm_client.chat_completion(messages)

            await self._chat_repo.add_message(user_id, "assistant", answer)

            return answer
        except Exception as e:
            error_message = f"[Ошибка]: {str(e)}"
            await self._chat_repo.add_message(user_id, "assistant", error_message)
            raise

    async def get_history(
        self, user_id: int, limit: int = 50
    ) -> list[ChatMessageResponse]:
        messages = await self._chat_repo.get_recent_messages(user_id, limit)
        return [
            ChatMessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat(),
            )
            for msg in messages
        ]

    async def clear_history(self, user_id: int) -> int:
        return await self._chat_repo.delete_all_for_user(user_id)
