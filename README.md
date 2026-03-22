# HouseIQ — California House Price Predictor

HouseIQ is a production-grade machine learning web application that predicts California house prices using a trained RandomForest regression model. The app features a modern, dark-themed interface built with Next.js 14, powered by a FastAPI backend, and backed by Supabase for persistent prediction history. Deploy the backend to Railway and the frontend to Vercel for a fully serverless setup.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser (User)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
                         ▼
         ┌───────────────────────────────┐
         │    Vercel (Next.js Frontend)  │
         │  - UI/UX with Framer Motion   │
         │  - Predict Form               │
         │  - History Table              │
         │  - Model Info                 │
         └────────────┬──────────────────┘
                      │ JSON over HTTPS
                      ▼
         ┌───────────────────────────────┐
         │   Railway (FastAPI Backend)   │
         │  ┌─────────────────────────┐  │
         │  │  Model Artifacts        │  │
         │  │ ├─ model.pkl            │  │
         │  │ ├─ pipeline.pkl         │  │
         │  │ └─ metadata.json        │  │
         │  └─────────────────────────┘  │
         │  - /health                    │
         │  - /api/v1/predict            │
         │  - /api/v1/predictions        │
         │  - /api/v1/model              │
         └────────────┬──────────────────┘
                      │ SQL
                      ▼
         ┌───────────────────────────────┐
         │    Supabase (PostgreSQL)      │
         │  - predictions table          │
         │  - model_runs table           │
         └───────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14, React 18, TypeScript | Modern web framework with SSR/SSG |
| **Frontend Styling** | Tailwind CSS 3.4, Framer Motion | Responsive design, smooth animations |
| **Frontend UI** | Recharts, Lucide React, shadcn/ui | Charts, icons, reusable components |
| **Backend** | FastAPI 0.115.6, Uvicorn | High-performance async REST API |
| **ML Model** | scikit-learn 1.3.2, RandomForest | Regression model for price prediction |
| **ML Pipeline** | Pandas, NumPy | Data preprocessing, feature engineering |
| **Database** | Supabase (PostgreSQL) | Serverless relational DB with RLS |
| **Backend Deploy** | Railway | Docker-based platform for backend |
| **Frontend Deploy** | Vercel | Optimized Next.js hosting |
| **ML Artifact Storage** | Filesystem (in Railway container) | Serialized model and pipeline |

## Local Setup

Follow these steps to run the project locally:

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/houseiq.git
cd houseiq
```

### 2. Create and Activate Python Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your Supabase credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-service-role-key
```

### 5. Train the ML Model (if artifacts missing)
```bash
python -m ml.train --data-path data/housing.csv --output-dir ml/artifacts
```
This generates `model.pkl`, `pipeline.pkl`, and `metadata.json` in `ml/artifacts/`.

### 6. Start the FastAPI Backend
```bash
uvicorn api.main:app --reload --port 8000
```
Backend will be available at `http://localhost:8000`. Check health at `http://localhost:8000/health`.

### 7. Install Frontend Dependencies and Start Dev Server
```bash
npm install
npm run dev
```
Frontend will be available at `http://localhost:3000`.

### 8. Test the App
- Open `http://localhost:3000` in your browser
- Fill the prediction form and submit
- View your prediction history and model metrics

## Environment Variables

### Backend (.env at root)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SUPABASE_URL` | Yes | Supabase project URL | `https://abc123.supabase.co` |
| `SUPABASE_KEY` | Yes | Supabase service role key (not publishable key) | `eyJ0eXAiOiJK...` |
| `MODEL_PATH` | No | Path to model.pkl | `ml/artifacts/model.pkl` |
| `PIPELINE_PATH` | No | Path to pipeline.pkl | `ml/artifacts/pipeline.pkl` |
| `CORS_ORIGINS` | No | Comma-separated allowed origins (prod only) | `https://app.houseiq.com,https://app.vercel.app` |

### Frontend (.env.local at root)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API base URL | `http://localhost:8000` (dev) or `https://api.railway.app` (prod) |

## API Reference

### Health Check
```
GET /health
```
Returns API health status and model version.
```json
{
  "status": "ok",
  "model_version": "1.0"
}
```

### Single Prediction
```
POST /api/v1/predict
Content-Type: application/json

{
  "longitude": -121.45,
  "latitude": 46.23,
  "housing_median_age": 25,
  "total_rooms": 4000,
  "total_bedrooms": 800,
  "population": 1000,
  "households": 300,
  "median_income": 8.3,
  "ocean_proximity": "INLAND"
}
```
Returns:
```json
{
  "predicted_price": 385250.50,
  "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
  "model_version": "1.0",
  "created_at": "2026-03-22T10:30:45Z"
}
```

### Prediction History
```
GET /api/v1/predictions?limit=50&offset=0
```
Returns paginated list of past predictions with all input features.
```json
{
  "records": [
    {
      "predicted_price": 385250.50,
      "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
      "model_version": "1.0",
      "created_at": "2026-03-22T10:30:45Z",
      "longitude": -121.45,
      "latitude": 46.23,
      ...
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

### Model Info
```
GET /api/v1/model
```
Returns model metadata, performance metrics, and feature list.
```json
{
  "version": "1.0",
  "rmse": 47015.44,
  "mae": 30806.78,
  "r2": 0.8304,
  "features_used": ["longitude", "latitude", "housing_median_age", ...],
  "trained_at": "2026-03-22T08:15:30Z"
}
```

## Deployment

### Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Create a new project

2. **Connect GitHub Repository**
   - In Railway dashboard: "New Project" → "Deploy from GitHub"
   - Authorize and select your `houseiq` repository
   - Railway automatically detects the Dockerfile

3. **Set Environment Variables**
   - In Railway project settings, add variables:
     - `SUPABASE_URL` = your Supabase project URL
     - `SUPABASE_KEY` = your service role key
     - `CORS_ORIGINS` = your Vercel frontend URL (e.g., `https://houseiq.vercel.app`)

4. **Deploy**
   - Railway automatically builds the Docker image and deploys
   - You'll receive a production URL like `https://houseiq-production.up.railway.app`

5. **Verify Backend**
   - Visit `https://your-railway-url/health`
   - Should see `{"status":"ok","model_version":"1.0"}`

6. **Note the Backend URL**
   - Save your Railway URL for the frontend deployment step

### Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project" → "Import Git Repository"
   - Select your `houseiq` repository

3. **Configure Build Settings**
   - Framework: Next.js (auto-detected)
   - Build command: `npm run build` (auto-detected)
   - Output directory: `.next` (auto-detected)
   - Root directory: `./` (default)

4. **Set Environment Variables**
   - Add in Vercel dashboard:
     - `NEXT_PUBLIC_API_URL` = your Railway backend URL (e.g., `https://houseiq-production.up.railway.app`)

5. **Deploy**
   - Click "Deploy"
   - Vercel builds and deploys automatically
   - You'll receive a frontend URL like `https://houseiq.vercel.app`

6. **Verify Frontend**
   - Visit your Vercel URL
   - The app should load and predictions should work
   - Check browser console for any API errors

### End-to-End Verification

1. Open your Vercel frontend URL
2. Fill the prediction form with sample data
3. Click "Get Valuation"
4. Verify the prediction appears (should see USD price)
5. Go to "Prediction History" page
6. Verify the prediction is listed
7. Go to "Model Intelligence" page
8. Verify model metrics load correctly

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `CORS error in browser console` | Backend CORS_ORIGINS doesn't include frontend URL | Update Railway env var: `CORS_ORIGINS=https://houseiq.vercel.app` |
| `500 error on /api/v1/predict` | Model artifacts missing in Railway | Ensure `ml/artifacts/` files are in git repo and pushed to Railway |
| `Supabase connection failed` | Wrong SUPABASE_KEY or wrong URL | Use service role key (not publishable), verify URL in Railway env vars |
| `NEXT_PUBLIC_API_URL is not configured` | Vercel env var not set or .env.local missing | Set `NEXT_PUBLIC_API_URL` in Vercel dashboard |
| `Frontend shows "Failed to fetch predictions"` | Backend is down or not reachable | Check Railway deployment status, verify backend URL in Vercel logs |
| `Model artifacts: model.pkl not found` | Files not committed to git | Add to git: `git add ml/artifacts/ && git commit -m "Add ML artifacts"` |
| `Build fails on Vercel` | Node.js version mismatch | Ensure Node 20+ in Vercel settings (Project Settings → Node.js Version) |
| `Build fails on Railway` | Python version mismatch | Ensure Dockerfile uses `python:3.11-slim` |

## File Structure

```
.
├── Dockerfile                 # Backend container definition
├── railway.json              # Railway deployment config
├── vercel.json               # Vercel deployment config
├── setup_git.sh              # Git initialization script
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
├── README.md                 # This file
├── DEPLOYMENT.md             # Detailed deployment guide
├── .env                      # Backend environment (production)
├── .env.example              # Backend environment template
├── .env.local.example        # Frontend environment template
├── .env.production.example   # Frontend environment (production)
├── .dockerignore             # Docker build excludes
├── .gitignore                # Git excludes
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── api/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── model_loader.py       # ML artifact loader
│   ├── db.py                 # Supabase client
│   ├── schemas.py            # Pydantic models
│   └── routes/
│       ├── predict.py        # POST /api/v1/predict
│       ├── history.py        # GET /api/v1/predictions
│       └── model_info.py     # GET /api/v1/model
├── ml/
│   ├── __init__.py
│   ├── pipeline_utils.py     # Shared ML utilities
│   ├── train.py              # Model training script
│   ├── evaluate.py           # Cross-validation evaluation
│   ├── predict.py            # Batch inference
│   └── artifacts/
│       ├── model.pkl         # Trained RandomForest
│       ├── pipeline.pkl      # Preprocessing pipeline
│       └── metadata.json     # Model metadata
├── data/
│   └── housing.csv           # Training data
├── app/
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles & design tokens
│   ├── page.tsx              # Predict page
│   ├── history/
│   │   ├── page.tsx          # History page
│   │   └── loading.tsx       # Loading skeleton
│   └── model/
│       └── page.tsx          # Model info page
├── components/
│   └── Sidebar.tsx           # Navigation sidebar
├── lib/
│   └── api.ts                # Typed fetch client
├── public/                   # Static assets
├── next.config.mjs           # Next.js config
├── tailwind.config.js        # Tailwind CSS config
└── tsconfig.json             # TypeScript config
```

## Development

### Run Locally
```bash
# Terminal 1: Backend
source .venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
npm run dev
```

### Train Model
```bash
python -m ml.train --data-path data/housing.csv --output-dir ml/artifacts
```

### Evaluate Model
```bash
python -m ml.evaluate --data-path data/housing.csv
```

### Make Predictions (Batch)
```bash
python -m ml.predict --input input.csv --output predictions.csv --artifacts-dir ml/artifacts
```

### Run Tests (GitHub Actions)
```bash
git push origin main
# CI pipeline runs automatically
```

## License

MIT License - see LICENSE file for details.

---

**Need Help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions or open an issue on GitHub.
