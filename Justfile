default:
    @just --list

# Lint チェック（修正なし）
lint:
    docker-compose exec app uv run ruff check .

# Lint 自動修正
lint-fix:
    docker-compose exec app uv run ruff check --fix .

# フォーマットチェック
format-check:
    -docker-compose exec app uv run ruff format --check .

# フォーマット適用
format:
    docker-compose exec app uv run ruff format .

# 型チェック
typecheck:
    docker-compose exec app uv run mypy app tests

# すべてのテストを実行
test:
    docker-compose exec app uv run pytest

# コード品質チェック一括実行（Lint + Format + Type）
check:
    @echo "🔍 Running linter..."
    @just lint
    @echo "✨ Running formatter check..."
    @just format-check
    @echo "🔎 Running type checker..."
    @just typecheck
    @echo "✅ All checks passed!"

# コード修正一括実行（Lint fix + Format）
fix:
    @echo "🔧 Fixing lint issues..."
    @just lint-fix
    @echo "✨ Applying formatter..."
    @just format
    @echo "✅ All fixes applied!"

# フル検証（チェック + テスト）
ci: check test
    @echo "🎉 CI checks completed!"

