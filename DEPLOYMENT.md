# Production Deployment Guide

This guide walks you through deploying HouseIQ to production on Railway (backend) and Vercel (frontend).

## Table of Contents
1. [Backend Deployment Environment Variables](#backend-environment-variables)
2. [Frontend Deployment Environment Variables](#frontend-environment-variables)
3. [Railway Deployment (Backend)](#railway-deployment-backend)
4. [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Troubleshooting](#troubleshooting)

---

## Backend Environment Variables

### Railway Backend (.env in production)

Set these environment variables in your Railway project settings before deployment:

| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `SUPABASE_URL` | String | **YES** | Your Supabase project URL | `https://abc123def456.supabase.co` |
| `SUPABASE_KEY` | String | **YES** | Service role secret key (NOT the publishable key) | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `MODEL_PATH` | String | No | Path to trained model pickle file | `ml/artifacts/model.pkl` |
| `PIPELINE_PATH` | String | No | Path to preprocessing pipeline | `ml/artifacts/pipeline.pkl` |
| `CORS_ORIGINS` | String | No | Comma-separated allowed origins for CORS | `https://houseiq.vercel.app` |
| `PORT` | Number | No | Server port (auto-set by Railway) | `8000` |

### How to Get Supabase Credentials

1. Go to [supabase.com](https://supabase.com) and sign in
2. Open your project
3. Click "Settings" → "API"
4. Copy the **Project URL** → set as `SUPABASE_URL`
5. Click the key icon next to "service_role secret" → **Copy** → set as `SUPABASE_KEY`
   - ⚠️ DO NOT use the "anon" / "public" key
   - ⚠️ DO use the "service_role" / "secret" key

### Prepare .env for Deployment

Before pushing to Railway, verify your backend `.env` file contains (at repo root):

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
MODEL_PATH=ml/artifacts/model.pkl
PIPELINE_PATH=ml/artifacts/pipeline.pkl
CORS_ORIGINS=https://your-vercel-domain.vercel.app
```

---

## Frontend Environment Variables

### Vercel Frontend

Set this environment variable in your Vercel project settings:

| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | String | **YES** | Backend API base URL (must start with `https://` in production) | `https://houseiq-api.up.railway.app` |

### Prepare .env.local for Vercel

Create `.env.local` in the project root (this file is in .gitignore and NOT pushed to git):

```
NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app
```

---

## Railway Deployment (Backend)

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Click "Deploy from GitHub"
4. Select your GitHub account and authorize Railway
5. Search for and select your `houseiq` repository
6. Click "Deploy"

Railway will auto-detect the Dockerfile and start building the Docker image.

### Step 2: Wait for Build Completion

- Railway builds the Docker image from your Dockerfile
- This takes 2-5 minutes
- You can view build logs in the Railway dashboard
- Once complete, Railway automatically deploys the container

### Step 3: Configure Environment Variables

1. In the Railway dashboard, click on your project
2. Click the "houseiq" service
3. Navigate to "Variables" tab
4. Click "+ New Variable" for each:
   - Name: `SUPABASE_URL` → Value: `https://abc123.supabase.co`
   - Name: `SUPABASE_KEY` → Value: `eyJhbGciOi...` (service role key, not anon key)
   - Name: `CORS_ORIGINS` → Value: `https://your-vercel-domain.vercel.app` (add after Vercel deployment)

5. Click "Save"
6. Railway automatically redeploys with new environment variables

### Step 4: Get Your Backend URL

1. In Railway dashboard, click your project
2. Click the "houseiq" service
3. Look for "Deployments" or "Public URL"
4. Your backend URL will be something like: `https://houseiq-production.up.railway.app`
5. **Copy this URL** — you'll need it for Vercel deployment

### Step 5: Verify Backend Deployment

Open your browser and visit:

```
https://your-railway-url/health
```

You should see:
```json
{
  "status": "ok",
  "model_version": "1.0"
}
```

If you see an error, check:
- Railway deployment logs for errors
- Database credentials are correct in environment variables
- Model artifacts exist in `ml/artifacts/` directory

---

## Vercel Deployment (Frontend)

### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Click "Import Git Repository"
4. Select your GitHub account and authorize Vercel
5. Search for and select your `houseiq` repository
6. Click "Import"

### Step 2: Configure Build Settings

Vercel auto-detects Next.js. Verify:
- **Framework Preset**: Next.js ✓
- **Build Command**: `npm run build` ✓
- **Output Directory**: `.next` ✓
- **Install Command**: `npm install` ✓
- **Root Directory**: `./` (default) ✓

### Step 3: Set Environment Variables

1. In Vercel, on the import screen, click "Environment Variables"
2. Add a new variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Railway backend URL from Step 4 above
     - Example: `https://houseiq-production.up.railway.app`
3. Click "Save"

### Step 4: Deploy

1. Click "Deploy"
2. Vercel builds and deploys your app (takes 1-3 minutes)
3. You'll get a frontend URL like: `https://houseiq.vercel.app`
4. Click the URL to open your live app

### Step 5: Update Backend CORS_ORIGINS

Now that you have your Vercel URL, update the Railway backend CORS settings:

1. Go to Railway dashboard
2. Click your project → click "houseiq" service
3. Click "Variables" tab
4. Edit `CORS_ORIGINS` value → replace with your Vercel URL
   - Example: `https://houseiq.vercel.app`
5. Click "Save"
6. Railway automatically redeploys

---

## Post-Deployment Verification

### Test 1: Health Check

```bash
curl https://your-railway-url/health
```

Expected response:
```json
{"status":"ok","model_version":"1.0"}
```

### Test 2: API Connectivity

In your browser console (on the Vercel frontend), run:

```javascript
fetch('https://your-railway-url/health').then(r => r.json()).then(console.log)
```

Expected output:
```
{status: 'ok', model_version: '1.0'}
```

### Test 3: Full Prediction Flow

1. Open `https://your-vercel-domain.vercel.app`
2. Fill in the prediction form with sample data
3. Click "Get Valuation"
4. Verify a price prediction appears
5. Check browser network tab — should see successful API calls
6. Go to "Prediction History" — your prediction should appear

### Test 4: Supabase Database

1. Go to [supabase.com](https://supabase.com) dashboard
2. Click your project
3. Click "SQL Editor"
4. Run:
   ```sql
   SELECT COUNT(*) as prediction_count FROM predictions;
   ```
5. Should show the predictions you made through the UI

---

## Troubleshooting

### Issue: CORS Error in Browser Console

**Error**: `Access to XMLHttpRequest at 'https://api.railway.app' from origin 'https://houseiq.vercel.app' has been blocked by CORS policy`

**Cause**: `CORS_ORIGINS` environment variable on Railway doesn't include your Vercel domain

**Fix**:
1. Go to Railway dashboard
2. Find your backend API service
3. Click "Variables"
4. Edit `CORS_ORIGINS` to include your Vercel URL:
   ```
   https://houseiq.vercel.app,https://another-domain.vercel.app
   ```
5. Save and wait for Railway to redeploy

---

### Issue: 502 Bad Gateway on Vercel

**Error**: Vercel shows a 502 error page

**Cause**: Backend is down or not responding within timeout

**Fix**:
1. Check Railway deployment status
2. Visit `https://your-railway-url/health` to verify backend is up
3. Check Railway logs for error messages
4. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correctly set
5. Trigger a redeploy: Push a new commit to GitHub

---

### Issue: "Connection refused" or Backend Service Unavailable

**Error**: Frontend shows "Failed to connect to API" or network error

**Cause**: `NEXT_PUBLIC_API_URL` is incorrect or backend service crashed

**Fix**:
1. Verify Railway backend is running: `https://your-railway-url/health`
2. Check `NEXT_PUBLIC_API_URL` in Vercel environment variables
3. Check Vercel deployment logs for build errors
4. Redeploy: Push a new commit or click "Redeploy" in Vercel dashboard

---

### Issue: Predictions Work but History is Empty

**Error**: Predictions are made but don't appear in history

**Cause**: Supabase database connection issue or permissions

**Fix**:
1. Check Railway environment variable `SUPABASE_KEY` is the **service role key**, not anon key
2. Verify `SUPABASE_URL` is correct
3. In Supabase dashboard, check "SQL Editor" → run:
   ```sql
   SELECT * FROM predictions ORDER BY created_at DESC LIMIT 1;
   ```
4. If query returns data, check Vercel logs for history fetch error
5. If query returns nothing, model is not inserting to DB — check Railway logs

---

### Issue: Model Artifacts Not Found

**Error**: Railway logs show `FileNotFoundError: ml/artifacts/model.pkl not found`

**Cause**: Model artifact files not committed to git or not in correct directory

**Fix**:
1. In your local repo, verify files exist:
   ```bash
   ls -la ml/artifacts/
   ```
   Should show: `model.pkl`, `pipeline.pkl`, `metadata.json`

2. If files exist locally but not in git:
   ```bash
   git status ml/artifacts/
   git add ml/artifacts/
   git commit -m "Add ML model artifacts"
   git push origin main
   ```

3. Trigger Railway redeploy: Go to Railway dashboard → click deploy button

---

### Issue: Vercel Build Fails

**Error**: Vercel deployment shows build error

**Cause**: Node.js version mismatch or missing environment variables

**Fix**:
1. Check Vercel build logs for specific error
2. Ensure `NEXT_PUBLIC_API_URL` is set in Vercel dashboard
3. Verify Node.js version in Vercel project settings (should be 20+)
4. Try manual redeploy: Click "Redeploy" in Vercel dashboard

---

### Issue: 500 Error on /api/v1/predict

**Error**: API returns error 500 when making prediction

**Cause**: Backend error processing prediction

**Fix**:
1. Check Railway logs for error details
2. Verify model artifacts are loaded: Visit `https://railway-url/api/v1/model`
3. Verify Supabase connection: Try creating a new prediction — check Railway logs
4. Test locally: Run backend and frontend locally, make prediction
5. Check if model input validation is failing

---

### Issue: "NEXT_PUBLIC_API_URL is not configured"

**Error**: Vercel build fails with "NEXT_PUBLIC_API_URL is not configured"

**Cause**: Environment variable not set in Vercel before build

**Fix**:
1. Go to Vercel dashboard → Project Settings
2. Navigate to "Environment Variables"
3. Add `NEXT_PUBLIC_API_URL` with Railway backend URL
4. Redeploy: Push new commit or use Vercel redeploy button

---

## Monitoring

### View Logs

**Railway Logs**:
1. Go to railway.app dashboard
2. Click your project
3. Click your service
4. Click "Logs" tab
5. View real-time logs

**Vercel Logs**:
1. Go to vercel.com dashboard
2. Click your project
3. Click your deployment
4. Click "Logs" tab
5. View build and runtime logs

---

## Scaling & Performance

### Railway
- Default tier has 100MB RAM and auto-scales
- For higher traffic, upgrade to higher tier in Railway dashboard
- Enable "Auto Deploy on Push" to auto-redeploy on git commits

### Vercel
- Vercel automatically scales based on traffic
- No configuration needed for most use cases
- Check "Analytics" tab for request patterns

---

## CI/CD Pipeline

GitHub Actions automatically runs on every push:

1. Backend syntax check
2. Frontend build verification

View results:
1. Go to github.com
2. Click your repository
3. Click "Actions" tab
4. View workflow runs

Only push to `main` branch for production; use `develop` branch for testing.

---

## Related Documentation

- [README.md](README.md) - Project overview and local setup
- [Supabase Docs](https://supabase.com/docs)
- [Railway Docs](https://railway.app/docs)
- [Vercel Next.js Docs](https://vercel.com/docs/frameworks/nextjs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
