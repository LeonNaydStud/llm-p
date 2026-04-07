from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    prompt: str = Field(..., min_length=1, max_length=10000, description="User message")
    system: str | None = Field(
        None, max_length=1000, description="Optional system instruction"
    )
    max_history: int = Field(
        10, ge=0, le=50, description="Maximum history messages to include"
    )
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Model temperature")


class ChatResponse(BaseModel):

    answer: str = Field(..., description="Model response")


class ChatMessageResponse(BaseModel):

    id: int
    role: str
    content: str
    created_at: str
