# Project Setup and Run Guide
## AI-Based Predictive Maintenance System for Industrial Equipment

**Purpose:** Complete guide for running the full system for academic defense presentation.

---

## PREREQUISITES

### Required Software
- **Python 3.8+** (with virtual environment)
- **Node.js 16+** and npm
- **PostgreSQL 17** (or compatible version)
- **Git** (optional, for version control)

### Python Dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install scikit-learn pandas numpy joblib
pip install pydantic pydantic-settings
```

### Node.js Dependencies
```bash
npm install
```

---

## DATABASE SETUP

### 1. Install PostgreSQL
- Download and install PostgreSQL from https://www.postgresql.org/download/
- During installation, set a secure password for the postgres user
- Make sure PostgreSQL is running

### 2. Create Database
**Option A: Using pgAdmin**
1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name it: `predictive_maintenance`
4. Click "Save"

**Option B: Using SQL**
```bash
psql -U postgres
CREATE DATABASE predictive_maintenance;
\q
```

### 3. Update Database Configuration
Edit `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/predictive_maintenance
```

### 4. Seed Database with Demo Data
```bash
cd backend
.\venv\Scripts\Activate.ps1
python seed_database.py
```

This creates:
- 8 machines with realistic sensor data
- ML predictions with balanced status distribution (5 Normal, 2 Monitor, 1 Critical)

---

## BACKEND SETUP

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary scikit-learn pandas numpy joblib pydantic pydantic-settings requests
```

### 3. Update Configuration
Edit `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/predictive_maintenance
MODEL_PATH=models/final_rul_model.joblib
SCALER_PATH=models/preprocessing_pipeline.joblib
DECISION_CONFIG_PATH=ml/results/decision_layer_config.json
```

### 4. Start Backend Server
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: http://localhost:8000

### 5. Verify Backend
- Check API health: http://localhost:8000/api/v1/health
- Check machines: http://localhost:8000/api/v1/machines/
- Check maintenance summary: http://localhost:8000/api/v1/maintenance/summary

---

## FRONTEND SETUP

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Update API Configuration
Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Start Frontend Server
```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:5173

### 4. Access Application
Open browser and navigate to: http://localhost:5173

---

## ML MODEL EVALUATION

### Run Official Test Evaluation
```bash
cd ml
python compare_predictions_vs_truth.py
```

This generates:
- **Scatter plot:** `ml/results/predictions_vs_truth.png`
- **Comparison table:** `ml/results/predictions_vs_truth.csv`
- **Metrics:** RMSE: 31.73 cycles, MAE: 23.39 cycles

---

## QUICK START (DEMO MODE)

### 1. Start All Services
**Terminal 1 - Backend:**
```bash
cd C:\Users\ULTRAPC\Desktop\PFA26\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\Users\ULTRAPC\Desktop\PFA26\frontend
npm run dev
```

### 2. Access Demo
- Open browser: http://localhost:5173
- Navigate through pages:
  - **Dashboard:** Overall statistics and charts
  - **Machines:** Machine list with predictions
  - **Maintenance:** Maintenance recommendations
  - **Test Prediction:** Manual sensor input for live demo

### 3. Use Test Prediction Page
1. Click "Test Prediction" in sidebar
2. Select a machine from dropdown
3. Click "Load Healthy Example" → "Predict" (should show NORMAL/MONITOR)
4. Click "Load Critical Example" → "Predict" (should show CRITICAL)

---

## PROJECT STRUCTURE

```
PFA26/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routes/              # API endpoints
│   │   └── services/            # Business logic
│   ├── models/                  # Saved ML artifacts
│   │   ├── final_rul_model.joblib
│   │   └── preprocessing_pipeline.joblib
│   ├── seed_database.py         # Database seeding script
│   └── .env                    # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API client
│   │   └── types/               # TypeScript types
│   └── .env                    # Environment variables
├── ml/
│   ├── src/                     # ML pipeline code
│   ├── models/                  # ML artifacts
│   ├── results/                 # Evaluation results
│   └── compare_predictions_vs_truth.py  # Official test evaluation
└── docs/                      # Documentation
```

---

## TROUBLESHOOTING

### Backend Issues

**Database Connection Error:**
```bash
# Check PostgreSQL is running
# Test connection:
python -c "from app.database import engine; print(engine.url)"
```

**Module Not Found:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1
# Install missing dependencies
pip install [module_name]
```

**Port Already in Use:**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID [PID] /F
```

### Frontend Issues

**Module Not Found:**
```bash
cd frontend
npm install
```

**Port Already in Use:**
```bash
# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID [PID] /F
```

**API Connection Error:**
- Ensure backend is running on port 8000
- Check `frontend/.env` has correct API URL
- Check browser console for CORS errors

### Database Issues

**Tables Not Created:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python seed_database.py
```

**No Data in Tables:**
- Verify seed script completed successfully
- Check pgAdmin for table contents
- Re-run seed script if needed

---

## ACADEMIC DEFENSE CHECKLIST

### Before Defense:
- [ ] Backend runs on http://localhost:8000
- [ ] Frontend runs on http://localhost:5173
- [ ] Database contains 8 machines with predictions
- [ ] All pages load without errors (Dashboard, Machines, Maintenance, Test Prediction)
- [ ] Test Prediction page works with both healthy and critical examples
- [ ] ML evaluation script produces correct metrics (RMSE: 31.73, MAE: 23.39)
- [ ] Scatter plot and CSV generated from evaluation script

### During Defense:
- [ ] Show Dashboard first (overview of system)
- [ ] Navigate to Machines page (show individual predictions)
- [ ] Navigate to Maintenance page (show actionable recommendations)
- [ ] Use Test Prediction page for live demo (show healthy vs critical outcomes)
- [ ] Present ML evaluation metrics and scatter plot
- [ ] Explain decision layer (safety margin, health score, maintenance status)

---

## KEY METRICS FOR DEFENSE

### Model Configuration
- **Type:** Random Forest Regressor
- **Hyperparameters:** n_estimators=77, max_depth=9, min_samples_split=10, min_samples_leaf=7, max_features=log2
- **Features:** 18 (3 settings + 15 sensors, NO relative_cycle)
- **Data Leakage Check:** PASSED

### Performance Metrics
- **Validation RMSE:** 41.80 cycles
- **Official Test RMSE:** 31.73 cycles
- **Validation MAE:** 31.72 cycles
- **Official Test MAE:** 23.39 cycles
- **Validation R²:** 0.62
- **Official Test R²:** 0.42

### Decision Layer
- **Safety Margin:** 49 cycles
- **Critical Threshold:** RUL ≤ 20 cycles
- **Maintenance Threshold:** 20 < RUL ≤ 50 cycles
- **Monitor Threshold:** 50 < RUL ≤ 100 cycles
- **Normal Threshold:** RUL > 100 cycles

---

## SUPPORT FILES

### Documentation
- `docs/FINAL_VERIFIED_RESULTS.md` - Verified metrics from saved artifacts
- `docs/FOLLOW_UP_ANALYSIS.md` - Training metrics and RMSE/R² analysis
- `ML_RESULTS.md` - Original ML training results
- `PHASE_2_5_RESULTS.md` - Leakage audit results
- `PHASE_2_6_RESULTS.md` - Model optimization results

### ML Artifacts
- `models/final_rul_model.joblib` - Trained Random Forest model
- `models/preprocessing_pipeline.joblib` - Fitted StandardScaler
- `models/model_metadata.json` - Complete model metadata

### Evaluation Results
- `ml/results/predictions_vs_truth.png` - Scatter plot for defense
- `ml/results/predictions_vs_truth.csv` - Full comparison table
- `ml/results/computed_training_metrics.json` - Training metrics
- `ml/results/rul_distribution_analysis.json` - RUL distribution analysis

---

## CONTACT & SUPPORT

For issues during defense setup:
1. Check Troubleshooting section above
2. Verify all services are running (backend, frontend, database)
3. Check environment variables in `.env` files
4. Review error messages in terminal/console

**Good luck with your defense!**
