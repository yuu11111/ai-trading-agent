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

## Nocturne Live Agents

- GPT-5 Pro: [Portfolio Dashboard](https://hypurrscan.io/address/0xa049db4b3dfcb25c3092891010a629d987d26113) | [Live Logs](https://35.190.43.182/logs/0xC0BE8E55f469c1a04c0F6d04356828C5793d8a9D) (Seeded with $200)
- DeepSeek R1: [Portfolio Dashboard](https://hypurrscan.io/address/0xa663c80d86fd7c045d9927bb6344d7a5827d31db) | [Live Logs](https://35.190.43.182/logs/0x4da68B78ef40D12f378b8498120f2F5A910Af1aD) (Seeded with $100) -- PAUSED
- Grok 4: [Portfolio Dashboard](https://hypurrscan.io/address/0x3c71f3cf324d0133558c81d42543115ef1a2be79) | [Live Logs](https://35.190.43.182/logs/0xe6a9f97f99847215ea5813812508e9354a22A2e0) (Seeded with $100) -- PAUSED

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
docker build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/trading-agent .
docker push gcr.io/YOUR_PROJECT_ID/trading-agent

# Deploy to Cloud Run
gcloud run deploy trading-agent \
  --image gcr.io/YOUR_PROJECT_ID/trading-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TAAPI_API_KEY=YOUR_TAAPI_KEY \
  --set-env-vars HYPERLIQUID_PRIVATE_KEY=YOUR_PRIVATE_KEY \
  --set-env-vars OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY \
  --set-env-vars ASSETS="BTC ETH" \
  --set-env-vars INTERVAL="1h" \
  --set-env-vars LLM_MODEL="x-ai/grok-4" \
  --memory 2Gi \
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
