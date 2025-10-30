FROM python:3.12-slim

WORKDIR /app

# システム依存
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

# Rye インストール
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
ENV PATH="/root/.rye/shims:$PATH"

# プロジェクトコピー
COPY pyproject.toml rye.lock* ./
COPY src ./src

# 依存同期（システム環境にインストール）
RUN rye sync --no-dev --system

# ポート設定
ENV APP_PORT=3000
EXPOSE 3000

# 実行
CMD ["python", "-m", "trading_agent.main"]
