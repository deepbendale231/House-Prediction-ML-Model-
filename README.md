# HouseIQ

![Railway](https://img.shields.io/badge/Railway-Backend-black?style=flat-square&logo=railway) ![Vercel](https://img.shields.io/badge/Vercel-Frontend-black?style=flat-square&logo=vercel) ![Supabase](https://img.shields.io/badge/Supabase-Database-black?style=flat-square&logo=supabase)

Predict California house prices in milliseconds. Built with RandomForest ML, FastAPI, Next.js, and Supabase.

---

> Add a screenshot here after deployment

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 + TypeScript + Tailwind + Framer Motion |
| Backend | FastAPI + Uvicorn |
| ML Model | scikit-learn RandomForestRegressor |
| Database | Supabase (PostgreSQL) |
| Backend Deploy | Railway (Docker) |
| Frontend Deploy | Vercel |

---

## Architecture

```text
Browser
  -> Vercel (Next.js)
  -> Railway (FastAPI + ML artifacts)
  -> Supabase
```

---

## Quickstart

1. Clone repo
```bash
git clone https://github.com/deepbendale231/House-Prediction-ML-Model-.git && cd House-Prediction-ML-Model-
```

2. Create virtual environment and activate
```bash
python3 -m venv .venv && source .venv/bin/activate
```

3. Install backend dependencies
```bash
pip install -r requirements.txt
```

4. Configure backend environment
```bash
cp .env.example .env
```
Fill `SUPABASE_URL` and `SUPABASE_KEY` in `.env`.

5. Train model and generate artifacts
```bash
python -m ml.train --data-path data/housing.csv --output-dir ml/artifacts
```

6. Start backend API
```bash
uvicorn api.main:app --reload --port 8000
```

7. Start frontend
```bash
cd frontend && npm install && npm run dev
```

---

## API

| Method | Route | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /api/v1/predict | Run prediction |
| GET | /api/v1/predictions | Fetch history |
| GET | /api/v1/model | Model metadata |

---

## Deploy

### Railway

- Create a new project from this GitHub repository.
- Set `SUPABASE_URL`, `SUPABASE_KEY`, and `CORS_ORIGINS`.
- Railway builds using `Dockerfile` and deploys automatically.
- Verify backend at `/health` on your Railway domain.

### Vercel

- Import the same GitHub repository into Vercel.
- Set `NEXT_PUBLIC_API_URL` to your Railway backend URL.
- Deploy with default Next.js build settings.
- Open the Vercel URL and test prediction flow.

---

## Environment Variables

| Variable | Required | Used By | Example |
|---|---|---|---|
| SUPABASE_URL | Yes | Backend | https://xyzcompany.supabase.co |
| SUPABASE_KEY | Yes | Backend | sb_secret_xxxxxxxxxxxxx |
| CORS_ORIGINS | Yes (prod) | Backend | https://houseiq.vercel.app |
| MODEL_PATH | No | Backend | ml/artifacts/model.pkl |
| NEXT_PUBLIC_API_URL | Yes | Frontend | https://houseiq.up.railway.app |

---

MIT License · Built by Deep Bendale
