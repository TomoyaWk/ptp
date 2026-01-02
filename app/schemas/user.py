from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """ユーザーベーススキーマ"""
    email: EmailStr


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""
    password: str


class UserLogin(BaseModel):
    """ユーザーログインスキーマ"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """ユーザーレスポンススキーマ"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    """トークンレスポンススキーマ"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """トークンデータスキーマ"""
    email: str | None = None
