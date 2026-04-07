from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_recent_messages(
        self, user_id: int, limit: int = 10
    ) -> List[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def delete_all_for_user(self, user_id: int) -> int:
        result = await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()
        return result.rowcount
