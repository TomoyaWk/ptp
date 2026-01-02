from fastapi import APIRouter
from app.api.endpoints import auth, user

api_router = APIRouter()

# 認証関連のエンドポイント
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# ユーザー関連のエンドポイント
api_router.include_router(user.router, prefix="/users", tags=["users"])
