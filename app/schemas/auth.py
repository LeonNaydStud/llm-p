from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ..., min_length=6, max_length=100, description="User password"
    )


class TokenResponse(BaseModel):

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
