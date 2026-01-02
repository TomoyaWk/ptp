# GitHub Copilot Instructions

本ファイルは、このリポジトリにおける **コーディング規約・技術スタック・開発方針** を
GitHub Copilot に伝えるためのものです。
既存コードの流儀を最優先し、勝手な技術選定・設計変更は行わないでください。
このファイルを読み込んでいるかを確認したいため、読み込んだ際は「copilot-instructions.mdを読み込みました」と応答に記述してください。

---

## 1. 前提技術スタック（固定）

- 言語: Python
- Webフレームワーク: FastAPI
- ORM / モデル: SQLModel
- テスト: pytest
- パッケージ管理 / コマンド実行: **uv（必須）**

### 重要
- `pip`, `poetry`, `pdm`, `conda` は **一切使用しない**
- 仮想環境の直接操作 (`python -m venv`) は行わない
- **すべてのコマンドは uv 経由で実行する**

---

## 2. uv の使用ルール（厳守）

各コマンドはdocker-compose 経由で実行されることを前提とする。(docker-compose app uv ...)
### 依存関係管理
- 依存追加（本番）:  
  `uv add <package>`
- 依存追加（開発・テスト）:  
  `uv add --dev <package>`
- 依存削除:  
  `uv remove <package>`
- インストール同期:  
  `uv sync`

### コマンド実行
- アプリ実行:  
  `uv run python ...`
- テスト実行:  
  `uv run pytest`
- 単一テスト・絞り込み:  
  `uv run pytest -k <pattern>`

Copilot は **pip コマンドを提案してはいけない**。

---

## 3. Python / 型の方針

- Python 3.12 以上を想定
- 型ヒントは原則必須
  - 引数 / 戻り値
  - public な関数・メソッド
- `Any` の使用は最小限（理由がある場合のみ）
- API の入出力は **明示的なモデル** を定義する

---

## 4. FastAPI の設計方針

- `APIRouter` を利用し、責務ごとに分離
- Router は薄く保つ
  - 業務ロジックは service 層へ
- `Depends` による依存注入を使用
- ステータスコードとレスポンスモデルを明示する

例:
```python
@router.post(
    "/items",
    status_code=201,
    response_model=ItemRead,
)
```

### エラーハンドリング
  想定内エラー: HTTPException
  内部エラーの詳細をレスポンスに含めない
  detail は安定したメッセージにする

## 5. SQLModel の利用ルール
  SQLModel を前提とした設計を行う

  テーブル定義 (table=True) と
  Create / Read / Update 用モデルは必要に応じて分離
  Field() を使って制約・デフォルトを明示
  セッションは共通の仕組みを使い、直接生成しない

### 禁止事項
  生 SQL の文字列連結
  
## 6. レイヤ構成の考え方
  (ここに各ディレクトリと概要を簡潔に示す)
  原則:
  Router にロジックを書かない
  DB 操作を API から直接呼ばない

## 7. テスト（pytest）
  新しい挙動には必ずテストを書く
  pytest を前提とする
  各テストメソッド名は可能な限り日本語で記述する
  前提データ用意ではfixture を積極的に使う
  fixtureでは対応するjsonファイルを読み込む形でデータを作成する
  TestClient
  DB セッション（分離されたもの）
  
### 実行コマンド
  ```sh
  # すべてのテストを実行
  docker-compose app uv run pytest
  
  # 特定のテストファイルを実行
  docker-compose app uv run pytest tests/test_api/test_user.py
```

## 8. コードスタイル・品質

勝手に新しいツールを導入しない
秘密情報をログに出さない

## 9. セキュリティ・安全性
入力値は常に検証する

認証・認可は既存の依存注入パターンに従う

内部構造・例外トレースを外部に漏らさない

## 10. 変更時の基本姿勢
差分は最小限にする
無関係なリファクタリングは行わない
迷ったら既存コードを優先
一貫性を最優先する

## 11. Copilot の出力に求める内容
コード提案時は以下を含めること:
  変更・追加するファイルパス
  完全なコード（省略しない）
  必要な uv コマンド
  なぜこの実装が既存設計に合うかの簡潔な説明