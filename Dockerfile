FROM python:3.12-slim

WORKDIR /app

# システム依存
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

# プロジェクトコピー
COPY pyproject.toml README.md ./
COPY src ./src

# 依存インストール
RUN pip install --no-cache-dir .

# 実行
CMD ["python", "src/main.py"]
