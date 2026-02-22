# 🤖 Ultima Bot 6

**Ultima Bot 6** is a full-stack, AI-powered trading automation system for **cryptocurrency and equities**. It supports real-time, multi-broker execution with confidence-based trade scaling, model orchestration, and a real-time dashboard. The backend runs an async trading loop: **Discovery → Scoring (forecast/model) → Risk checks → Execution → Auto-close (TP/SL/trailing)**.

**Strategy evolution context:** The product lineage is **Easy E\*TRADE Strategy** → **Easy ORB Strategy** → **Easy ORB 0DTE Strategy**. Ultima Bot 6 is the unified automation platform that supports multi-broker execution (including E\*TRADE), multiple discovery and execution strategies, and is positioned to support ORB/0DTE logic as strategy modules when added.

---

## 1. Overview

- **Backend:** FastAPI, WebSockets, async trading loop, discovery cache, risk/forecast/execution/auto-close engines. Persistence: PostgreSQL and Firestore (per deployment).
- **Frontend:** React + Vite + TailwindCSS, real-time dashboard, broker/wallet connect, themes (e.g. Light/Dark, PlayStation/Xbox style).
- **Deployment:** Docker Compose (local), GCP Cloud Run–ready (see `GCP_DEPLOYMENT_GUIDE.md`).

---

## 2. Features

| Area | Description |
|------|-------------|
| **Multi-broker & wallets** | **Stocks:** E\*TRADE, Robinhood, Interactive Brokers, TD Ameritrade, Alpaca. **Crypto CEX:** Coinbase, Binance, Kraken, KuCoin, Bitfinex. **Wallets:** MetaMask, Trust Wallet, Coinbase Wallet, Phantom. |
| **AI trade models** | Alphacoin, Antimatter, Hexacoin, Cryptanium, Radiant, TitanFusion, Dianastone (joblib + `performance.json`). |
| **Trading modes** | Easy, Normal, Hard (UI: Easy / Hard / Hero) with different TP/SL multipliers and confidence scaling. |
| **Live engines** | Discovery, Strategy, Risk, Forecast, Auto-Close, Trade Scaling (Power Trades). |
| **Power Trades** | Confidence-driven scaling with trailing TP/SL and dynamic capital allocation. |
| **Discovery strategies** | **Crypto:** CMC_TRENDING, CMC_VOLUME, GMGN_TRENDING, ORIGINAL, VOLUME_SPIKE, MID_LOW_CAP, MICRO_CAP_MOONSHOT. **Stocks:** FRESHMAN, TOP_VOLUME, LARGE_CAP, SUPER_LEVERAGE, CAMERON. |
| **Dashboard** | Open trades, live charts, broker account stats, model pairings. Light (PlayStation) and Dark (Xbox) themes with animated SVG backgrounds. |
| **Sound & UX** | Customizable event sounds and win-streak audio feedback. |
| **Real-time updates** | WebSocket-powered UI with streaming trade, chart, and sentiment data. |
| **Deployment** | Docker Compose (backend + frontend + PostgreSQL). GCP Cloud Run–ready; see `GCP_DEPLOYMENT_GUIDE.md`. |

---

## 3. Architecture and Data Flow

```
  Discovery (cache refresh, CMC/fetchers, feature strategy router)
         │
         ▼
  Scoring (forecast engine + model confidence)
         │
         ▼
  Risk checks (capital floor, allocation %, drawdown, power tiers, volatility filter)
         │
         ▼
  Execution (TradeExecutor: size, liquidity, open/close)
         │
         ▼
  Auto-close (TP/SL, trailing stop, confidence exit, hero timeout)
```

- **Discovery engine:** Cache refresh, CMC and other daily fetchers, feature-based strategy router, token filters, chain-aware enrichment. Strategy priority is updated from trade results (gain %, confidence, streak).
- **Strategy engine:** StrategyManager, confidence floor, scaling multiplier by mode.
- **Risk engine:** Capital floor, allocation %, max account/trade risk, power tiers, win-streak scaling, volatility filter.
- **Forecast engine:** ATR, trend strength, confidence, TP/SL/trailing by mode, optional trail-to-moon.
- **Auto-close engine:** TP/SL hit, trailing stop, confidence exit, hero-mode timeout.
- **Execution engine:** TradeExecutor (position sizing, liquidity check, open/close). Symbol and trade monitors.

Broker-specific clients live under `backend/app/utils/broker_clients/` (e.g. `etrade_client.py`). Session restore and active sessions are supported on startup.

---

## 4. Technologies Used

| Layer | Tech Stack |
|-------|------------|
| Frontend | React, Vite, TailwindCSS, Framer Motion |
| Components | Custom hooks, Chart.js, TP/SL visuals, particle backgrounds |
| Backend | FastAPI, WebSockets, PostgreSQL, Pydantic |
| Models | joblib (.pkl) Python models with `performance.json` |
| Infrastructure | Docker, Cloud Run, NGINX |

---

## 5. Project Structure

```
ultima-bot-6/
├── backend/
│   ├── app/
│   │   ├── engines/
│   │   │   ├── discovery_engine/   # CMC fetchers, cache, feature strategy router, trade candidate filter
│   │   │   ├── strategy_engine/    # StrategyManager, mode_manager, compounding, reentry
│   │   │   ├── risk_engine/        # RiskManager, power_trade_scaling
│   │   │   ├── forecast_engine/    # Forecast, reaction curve
│   │   │   ├── execution_engine/   # TradeExecutor, trade_monitor, symbol_monitor
│   │   │   ├── auto_close_engine/  # TP/SL, trailing, confidence exit
│   │   │   ├── demo_engine/        # Demo / mock trade execution
│   │   │   └── trading_loop.py     # Main async loop
│   │   ├── services/              # Discovery, trade executor, WebSocket, session storage
│   │   ├── routers/               # API routes (trading, trades)
│   │   ├── utils/                 # Broker clients, market data, account data
│   │   └── main.py
│   ├── models/                    # joblib AI models
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── nginx.conf
│   ├── Dockerfile
│   └── index.html
│
├── docker-compose.yml             # backend + frontend + postgres
├── README.md
├── EXECUTIVE_SUMMARY.md           # State, capabilities, tests, recommendations
└── GCP_DEPLOYMENT_GUIDE.md        # Cloud Run, domain, env vars
```

---

## 6. Setup Guide

### Prerequisites

- Docker & Docker Compose
- Node.js `>=18` (for local frontend dev)
- Python `3.11` (for local backend dev)
- Rust (optional; for Pydantic compilation if building from source)

### Run full stack (Docker)

From the repository root:

```bash
docker compose down -v --remove-orphans
docker compose build --no-cache
docker compose up
```

- **Frontend:** [http://localhost](http://localhost) (port 80)
- **Backend API:** [http://localhost:8080](http://localhost:8080) — docs at [http://localhost:8080/docs](http://localhost:8080/docs)
- **Database:** PostgreSQL on port 5432 (credentials in `docker-compose.yml`)

### Full wipe and rebuild (Docker)

If you need a clean slate:

```bash
docker compose down --volumes --remove-orphans
docker system prune -af --volumes
docker compose build --no-cache
docker compose up
```

### Refresh backend or frontend only

```bash
# Backend
docker compose build backend
docker compose up backend

# Frontend
docker compose build frontend
docker compose up frontend
```

### Local development (no Docker)

**Frontend only:**

```bash
cd frontend
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173).

**Backend only:**

```bash
cd backend
# Use venv and install deps from requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Ensure PostgreSQL (or your configured DB) is running and `.env` is set.

### Deploy to Google Cloud Run

See **`GCP_DEPLOYMENT_GUIDE.md`** for:

- GCP project and APIs setup
- Building and pushing images
- Deploying backend to Cloud Run
- Custom domain and frontend API URL
- Environment variables and access (e.g. auth key)

---

## 7. Testing

- **Discovery engine tests** live under `backend/app/engines/discovery_engine/tests/`:
  - `test_cmc_discovery_output.py` — CMC_TRENDING / CMC_VOLUME via feature-based strategy and `CryptoDiscoveryCache`
  - `crypto_discovery_test.py` — `CryptoDiscoveryTestEngine` (CoinMarketCap, GMGN, PumpFun, Original, Volume Spike, Mid-Low Cap, Micro Cap)
  - `run_discovery_test.py` — end-to-end discovery with test and real wallet clients (MetaMask, Phantom)
  - `test_broker_client.py` — test broker client usage

Run from the `backend` directory (with venv activated and deps installed), for example:

```bash
cd backend
python -m pytest app/engines/discovery_engine/tests/ -v
```

**Note:** There is no pytest suite yet for the other core engines (risk, forecast, auto_close, trade_executor, strategy_manager). Model performance is tracked in `performance.json` and the model registry for listing and selection, not as automated QA tests. See `EXECUTIVE_SUMMARY.md` for gaps and recommendations.

---

## 8. Model Training

New AI models compatible with the Ultima Bot backend can be trained in the **Model Training** environment (see `1. Model Training/README.md` in this workspace). That environment supports:

- Training **crypto** and **stock** models (e.g. Antimatter v2, Dianastone v2)
- Fetching OHLCV data (e.g. via configured data sources)
- Outputting joblib models and placing them in `backend/models/joblib/` for the model registry

Requirements (version alignment with the backend): Python `>=3.11`, `joblib`, `scikit-learn`, and a sklearn-compatible estimator with `predict_proba(X)` returning `[prob_class_0, prob_class_1]` (class 1 = trade signal). See the Model Training README for compatibility requirements, feature design, and evaluation metrics.

---

## 9. Documentation Map

| Document | Purpose |
|----------|---------|
| **README.md** (this file) | Overview, features, architecture, setup, testing, project structure. |
| **EXECUTIVE_SUMMARY.md** | Platform state, capabilities, performance tests, README assessment, findings and recommendations (integration gaps, strategy roadmap). |
| **GCP_DEPLOYMENT_GUIDE.md** | Prerequisites, GCP project/config, Cloud Run deploy, custom domain, frontend API URL, env vars, access and troubleshooting. |
| **1. Model Training/README.md** | Model training environment, compatibility requirements, quick start, dependencies. |

---

## 10. Development Status and Known Gaps

- **Trading loop integration:** The async trading loop and some engine APIs have known integration gaps (e.g. `get_valid_trade_candidates` arguments, forecast engine interface, RiskManager method naming). Details and suggested fixes are in **EXECUTIVE_SUMMARY.md**, Section 6.
- **ORB / 0DTE:** The codebase does not yet contain named "ORB" or "0DTE" strategy logic. E\*TRADE and stock discovery strategies (FRESHMAN, TOP_VOLUME, etc.) provide the base for adding ORB/0DTE as strategy modules later.
- **Tests:** Discovery tests exist; no pytest suite for risk/forecast/strategy/execution engines and no automated end-to-end integration test. See EXECUTIVE_SUMMARY for recommendations.

Once the integration issues in EXECUTIVE_SUMMARY are addressed and a minimal test suite is in place, the platform is in a strong position for controlled go-live and for adding Easy ORB and Easy ORB 0DTE strategies on top of the existing engine and broker stack.

---

## 11. License

MIT
