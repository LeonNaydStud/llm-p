from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UnauthorizedError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)


async def get_chat_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ChatMessageRepository:
    return ChatMessageRepository(db)


def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    chat_repo: Annotated[ChatMessageRepository, Depends(get_chat_repository)],
    llm_client: Annotated[OpenRouterClient, Depends(get_llm_client)],
) -> ChatUseCase:
    return ChatUseCase(chat_repo, llm_client)


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub", 0))
        if not user_id:
            raise UnauthorizedError("Invalid token payload")
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
