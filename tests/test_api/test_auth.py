from fastapi.testclient import TestClient
from app.models.user import User


class TestRegister:
    """ユーザー登録APIのテスト"""
    
    def test_新規ユーザーを登録できる(self, client: TestClient):
        """新規ユーザーを登録できる"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["is_active"] is True
        assert "id" in data
    
    def test_既に登録されているメールアドレスでは登録できない(self, client: TestClient, test_user: User):
        """既に登録されているメールアドレスでは登録できない"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "既に登録されています" in response.json()["detail"]
    
    def test_無効なメールアドレスでは登録できない(self, client: TestClient):
        """無効なメールアドレスでは登録できない"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123"
            }
        )
        assert response.status_code == 422


class TestLogin:
    """ログインAPIのテスト"""
    
    def test_正しい認証情報でログインできる(self, client: TestClient, test_user: User):
        """正しい認証情報でログインできる"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_間違ったパスワードでログインできない(self, client: TestClient, test_user: User):
        """間違ったパスワードでログインできない"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
    
    def test_存在しないユーザーでログインできない(self, client: TestClient):
        """存在しないユーザーでログインできない"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401


class TestGetCurrentUser:
    """現在のユーザー情報取得APIのテスト"""
    
    def test_認証済みユーザーの情報を取得できる(self, client: TestClient, test_user: User, test_token: str):
        """認証済みユーザーの情報を取得できる"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == test_user.id
    
    def test_認証なしではアクセスできない(self, client: TestClient):
        """認証なしではアクセスできない"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
    
    def test_無効なトークンではアクセスできない(self, client: TestClient):
        """無効なトークンでアクセスできない"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


# TODO: 以下のテストケースを実装してください
# - test_login_inactive_user: 無効化されたユーザーでログインできない
# - test_refresh_token: トークンのリフレッシュ
# - test_logout: ログアウト
