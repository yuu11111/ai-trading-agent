# Nocturne: AI Trading Agent on Hyperliquid

This project implements an AI-powered trading agent that leverages LLM models to analyze real-time market data from TAAPI, make informed trading decisions, and execute trades on the Hyperliquid decentralized exchange. The agent runs in a continuous loop, monitoring specified cryptocurrency assets at configurable intervals, using technical indicators to decide on buy/sell/hold actions, and manages positions with take-profit and stop-loss orders.

## Table of Contents

- [Disclaimer](#disclaimer)
- [Architecture](#architecture)
- [Nocturne Live Agents](#nocturne-live-agents)
- [Structure](#structure)
- [Env Configuration](#env-configuration)
- [Usage](#usage)
- [Tool Calling](#tool-calling)
- [Deployment to EigenCloud](#deployment-to-eigencloud)

## Disclaimer

There is no guarantee of any returns. This code has not been audited. Please use at your own risk.

## Architecture

See the full [Architecture Documentation](docs/ARCHITECTURE.md) for subsystems, data flow, and design principles.

![Architecture Diagram](docs/architecture.png)

[reference trader](https://www.youtube.com/watch?v=FocPtUVFs3Y)

## Nocturne Live Agents

[deepseek](https://hypurrscan.io/address/0x01FaB0C5D62782472B7cB9667bc29150dcaeA4ab#txs)

## Structure

- `src/main.py`: Entry point, handles user input and main trading loop.
- `src/agent/decision_maker.py`: LLM logic for trade decisions (OpenRouter with tool calling for TAAPI indicators).
- `src/indicators/taapi_client.py`: Fetches indicators from TAAPI.
- `src/trading/hyperliquid_api.py`: Executes trades on Hyperliquid.
- `src/config_loader.py`: Centralized config loaded from `.env`.

## Env Configuration

Populate `.env` (use `.env.example` as reference):

- TAAPI_API_KEY
- HYPERLIQUID_PRIVATE_KEY (or LIGHTER_PRIVATE_KEY)
- OPENROUTER_API_KEY
- LLM_MODEL
- Optional: OPENROUTER_BASE_URL (`https://openrouter.ai/api/v1`), OPENROUTER_REFERER, OPENROUTER_APP_TITLE

### Obtaining API Keys

- **TAAPI_API_KEY**: Sign up at [TAAPI.io](https://taapi.io/) and generate an API key from your dashboard.
- **HYPERLIQUID_PRIVATE_KEY**: Generate an Ethereum-compatible private key for Hyperliquid. Use tools like MetaMask or `eth_account` library. For security, never share this key.
- **OPENROUTER_API_KEY**: Create an account at [OpenRouter.ai](https://openrouter.ai/), then generate an API key in your account settings.
- **LLM_MODEL**: No key needed; specify a model name like "x-ai/grok-4" (see OpenRouter models list).

## Usage

Run: `poetry run python src/main.py --assets BTC ETH --interval 1h`

### Local API Endpoints

When the agent runs, it also serves a minimal API:

- `GET /diary?limit=200` — returns recent JSONL diary entries as JSON.
- `GET /logs?path=llm_requests.log&limit=2000` — tails the specified log file.

Configure bind host/port via env:

- `API_HOST` (default `0.0.0.0`)
- `API_PORT` or `APP_PORT` (default `3000`)

Docker:

```bash
docker build --platform linux/amd64 -t trading-agent .
docker run --rm -p 3000:3000 --env-file .env trading-agent
# Now: curl http://localhost:3000/diary
```

## Tool Calling

The agent can dynamically fetch any TAAPI indicator (e.g., EMA, RSI) via tool calls. See [TAAPI Indicators](https://taapi.io/indicators/) and [EMA Example](https://taapi.io/indicators/exponential-moving-average/) for details.

## Deployment to Google Cloud Run

Google Cloud Run allows deploying this trading agent as a serverless containerized application.

### Prerequisites

- Google Cloud project with billing enabled.
- Docker installed locally.
- gcloud CLI installed and authenticated.

### Installation

Install the gcloud CLI:

```bash
# macOS
brew install google-cloud-sdk

# Or download from https://cloud.google.com/sdk/docs/install
```

### Initial Setup

```bash
# Authenticate and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Deploy the Agent

From the project directory:

```bash
# Build and push Docker image
docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/trading-agent/trading-agent .
docker push asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/trading-agent/trading-agent

# Deploy to Cloud Run
gcloud run deploy trading-agent \
  --image asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/trading-agent/trading-agent \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars TAAPI_API_KEY=YOUR_TAAPI_KEY \
  --set-env-vars HYPERLIQUID_PRIVATE_KEY=YOUR_PRIVATE_KEY \
  --set-env-vars OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY \
  --set-env-vars ASSETS="BTC ETH" \
  --set-env-vars INTERVAL="10m" \
  --set-env-vars LLM_MODEL="x-ai/grok-4" \
  --memory 4Gi \
  --cpu 1 \
  --max-instances 1 \
  --timeout 3600
```

### Monitoring

```bash
# View logs
gcloud run logs read --region us-central1

# Check service status
gcloud run services describe trading-agent --region us-central1
```

For full CLI reference, see the [Google Cloud Run Documentation](https://cloud.google.com/run/docs).
