import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.user import User


class TestGetUsers:
    """ユーザー一覧取得APIのテスト"""
    
    def test_認証済みユーザーがユーザー一覧を取得できる(self, client: TestClient, test_user: User, test_token: str):
        """認証済みユーザーがユーザー一覧を取得できる"""

        
        response = client.get(
            "/api/users/",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        print(response.json())  # デバッグ用出力
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["email"] == test_user.email
    
    def test_get_users_with_pagination(self, client: TestClient, test_user: User, test_token: str):
        """ページネーションパラメータが正しく動作する"""
        response = client.get(
            "/api/users/?skip=0&limit=10",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_users_unauthorized(self, client: TestClient):
        """認証なしではアクセスできない"""
        response = client.get("/api/users/")
        assert response.status_code == 401
    
    def test_get_users_invalid_token(self, client: TestClient):
        """無効なトークンでアクセスできない"""
        response = client.get(
            "/api/users/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestUserModel:
    """Userモデルのテスト"""
    
    def test_create_user(self, session: Session):
        """ユーザーを作成できる"""
        from app.core.security import get_password_hash
        
        user = User(
            email="newuser@example.com",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_user_email_unique(self, session: Session, test_user: User):
        """同じメールアドレスのユーザーは作成できない"""
        from app.core.security import get_password_hash
        from sqlalchemy.exc import IntegrityError
        
        duplicate_user = User(
            email=test_user.email,  # 既存のメールアドレス
            hashed_password=get_password_hash("password123"),
        )
        session.add(duplicate_user)
        
        with pytest.raises(IntegrityError):
            session.commit()


# TODO: 以下のテストケースを実装してください
# - test_get_user_by_id: 特定のユーザーを取得
# - test_update_user: ユーザー情報の更新
# - test_delete_user: ユーザーの削除
# - test_deactivate_user: ユーザーの無効化
