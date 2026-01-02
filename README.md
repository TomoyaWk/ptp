# PTP - FastAPI Project

FastAPI + PostgreSQL + SQLModel を使用したWebアプリケーションプロジェクト

## 技術スタック

- **言語**: Python 3.11+
- **Webフレームワーク**: FastAPI
- **ORM**: SQLModel
- **データベース**: PostgreSQL
- **認証**: JWT (python-jose)
- **パスワードハッシュ化**: Passlib (bcrypt)
- **パッケージマネージャー**: uv
- **コンテナ**: Docker & Docker Compose

## プロジェクト構造

```
ptp/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーションのエントリーポイント
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 環境設定
│   │   ├── database.py      # データベース接続
│   │   └── security.py      # 認証・セキュリティユーティリティ
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # Userモデル
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # Pydanticスキーマ
│   └── api/
│       ├── __init__.py
│       ├── router.py        # APIルーター
│       └── endpoints/
│           ├── __init__.py
│           └── auth.py      # 認証エンドポイント
├── .env.example             # 環境変数のサンプル
├── .gitignore
├── pyproject.toml           # 依存関係定義
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

### 2. Docker Composeで起動

```bash
# コンテナをビルドして起動
docker-compose up -d

# ログを確認
docker-compose logs -f app
```

アプリケーションは http://localhost:8000 で起動します。

### 3. ローカル開発（Docker不使用）

```bash
# uvをインストール（まだの場合）
pip install uv

# 依存関係をインストール
uv pip install -r pyproject.toml

# PostgreSQLが起動していることを確認し、.envを設定

# アプリケーションを起動
uvicorn app.main:app --reload
```

## API エンドポイント

### 認証

- `POST /api/auth/register` - ユーザー登録
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - ログイン
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
  レスポンス:
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer"
  }
  ```

- `GET /api/auth/me` - 現在のユーザー情報取得（要認証）
  - Authorizationヘッダーに `Bearer <token>` を設定

### APIドキュメント

- Swagger UI: http://localhost:8000/docs
- OpenAPI仕様: http://localhost:8000/api/openapi.json

## データベース

PostgreSQL 16を使用。SQLModelが自動的にテーブルを作成します。

### Userテーブル

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INTEGER | 主キー（自動生成） |
| email | VARCHAR(255) | メールアドレス（一意、インデックス付き） |
| hashed_password | VARCHAR(255) | ハッシュ化されたパスワード |
| is_active | BOOLEAN | アクティブ状態（デフォルト: true） |
| created_at | TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | 更新日時 |

## 開発

### コンテナの停止

```bash
docker-compose down
```

### データベースをリセット

```bash
docker-compose down -v  # ボリュームも削除
docker-compose up -d
```

### コンテナ内でコマンドを実行

```bash
docker-compose exec app bash
```

## セキュリティ

- パスワードはbcryptでハッシュ化
- JWT（JSON Web Token）による認証
- 本番環境では必ず `.env` の `SECRET_KEY` を変更してください

## 今後の拡張

- [ ] メール検証機能
- [ ] パスワードリセット機能
- [ ] ユーザープロフィール管理
- [ ] Alembicによるマイグレーション管理
- [ ] テストコード
- [ ] CI/CD設定