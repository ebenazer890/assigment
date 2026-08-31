# QUICK START GUIDE - Role-Level AI Intelligence Platform

## ⚡ 5-Minute Setup

### 1. Install Python Dependencies (2 min)

```bash
cd modus
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

### 2. Start PostgreSQL (1 min)

Option A: Using Docker (Easiest)
```bash
docker-compose up -d
```

Option B: Local PostgreSQL
- Ensure PostgreSQL is running
- Create database: `createdb role_ai_db`

### 3. Initialize Database (1 min)

```bash
cd backend
python -c "from app.db.database import init_db; init_db()"
echo "✅ Database initialized"
```

### 4. Start Backend API (Terminal 1)

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend Ready**: http://localhost:8000  
📖 **API Docs**: http://localhost:8000/docs

### 5. Start Frontend (Terminal 2)

```bash
cd frontend
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

✅ **Frontend Ready**: http://localhost:8501

---

## 🎯 First Demo (2 minutes)

### Step 1: Seed Banking Roles

In Browser (API Docs):
1. Go to http://localhost:8000/docs
2. Find `POST /seed-data/initialize`
3. Click "Try it out" → "Execute"

**Expected Response:**
```json
{
  "status": "success",
  "message": "Successfully seeded 20 banking roles with processes, activities, and skills"
}
```

### Step 2: Open Frontend Dashboard

1. Go to http://localhost:8501
2. Click "📊 Dashboard" in sidebar
3. See key metrics and top 5 affected roles

### Step 3: Analyze Data Analyst Role

1. Click "📈 Role Analysis" in sidebar
2. Select "Data Analyst"
3. View:
   - AI Exposure metrics
   - Activities breakdown
   - Future skills required

### Step 4: Compare Two Roles

1. Click "⚖️ Compare Roles"
2. Select "Data Analyst" and "Procurement Analyst"
3. See side-by-side comparison

### Step 5: Add New Role (Surprise Test)

1. Click "➕ Add New Role"
2. Fill in form:
   - **Role Name**: Supply Chain Analyst
   - **Description**: Manages supply chain operations
   - **Processes**: Copy-paste JSON below:

```json
[
  {
    "name": "Supplier Management",
    "description": "Managing supplier relationships",
    "activities": [
      {
        "name": "Vendor Evaluation",
        "description": "Evaluating suppliers",
        "repetitiveness": 0.4,
        "data_availability": 0.7,
        "rule_based_nature": 0.5,
        "language_cognitive_complexity": 0.6,
        "human_judgment_requirement": 0.8,
        "regulatory_sensitivity": 0.5,
        "human_interaction_requirement": 0.8
      }
    ]
  }
]
```

3. Click "✅ Create and Analyze Role"
4. View results (no code changes needed!)

---

## 📊 What You'll See

### Dashboard
- **4 Key Metrics**: Roles, Processes, Activities, Avg AI Exposure
- **Top 5 Roles**: Ranked by AI Impact
- **Future Skills**: Skills in demand

### Role Analysis
- **AI Exposure Score**: 0.0-1.0 scale
- **Activities Breakdown**: Automated, Augmented, Human-Led
- **Future Role Profile**: What the role becomes
- **New Responsibilities**: Skills needed

### Role Comparison
- **Side-by-Side Metrics**: AI exposure, automation, augmentation
- **Key Differences**: Which role changes more
- **Ranking**: Who's most affected

### AI Impact Ranking
- **Top 5 Most Affected Roles**: With scores
- **Reasoning**: Why they're affected

### Add New Role
- **Dynamic Analysis**: No code changes
- **Instant Results**: Real-time processing
- **Full Integration**: Roles queryable via API

---

## 🔗 API Endpoints

### Test in Terminal

```bash
# Get all roles
curl http://localhost:8000/roles

# Get role detail
curl http://localhost:8000/roles/1

# Analyze role
curl http://localhost:8000/roles/1/analysis

# Get top AI impact roles
curl http://localhost:8000/analytics/top-ai-impact

# Get dashboard stats
curl http://localhost:8000/analytics/dashboard

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the five roles most affected by AI?"}'
```

Or use Swagger UI at: http://localhost:8000/docs

---

## 🧪 Run Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

**Expected Output:**
```
tests/test_main.py::TestRoleRepository::test_create_role PASSED
tests/test_main.py::TestActivityRepository::test_ai_exposure_calculation PASSED
... (15+ tests)
===================== 15 passed in 2.45s =====================
```

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error

```
Error: could not connect to server
```

**Fix:**
```bash
# Check if Docker container is running
docker ps

# Start if needed
docker-compose up -d

# Verify connection
psql postgresql://postgres:postgres@localhost:5432/role_ai_db -c "SELECT 1"
```

### Port Already in Use

```
Address already in use
```

**Fix:**
```bash
# Change in .env
API_PORT=8001  # Change from 8000

# Or kill process on port
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

### Streamlit Connection Error

```
ConnectionError: Max retries exceeded
```

**Fix:**
- Ensure backend is running on port 8000
- Check API_BASE_URL in frontend/app.py (should be http://localhost:8000)

### Module Import Error

```
ModuleNotFoundError: No module named 'app'
```

**Fix:**
```bash
# Ensure you're in backend directory
cd backend
# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## 📚 Documentation

- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Data Model**: [docs/DATA_MODEL.md](docs/DATA_MODEL.md)
- **Methodology**: [docs/METHODOLOGY.md](docs/METHODOLOGY.md)
- **Full README**: [README.md](README.md)
- **Licenses**: [LICENSES.md](LICENSES.md)

---

## 🎬 Demo Flow (10 minutes)

```
1. Open Dashboard (1 min)
   - Show metrics: 20 roles, AI impact

2. Select Data Analyst (2 min)
   - Show processes and activities
   - Explain AI scoring methodology

3. Analyze Data Analyst (2 min)
   - Show automated, augmented, human-led activities
   - Display future skills

4. Compare Roles (2 min)
   - Data Analyst vs Procurement Analyst
   - Show differences

5. Add Supply Chain Analyst (3 min)
   - Create new role dynamically
   - Show it works without code changes
   - Explain this is "surprise test" capability
```

---

## 🚀 Production Deployment

For cloud deployment:

1. **Environment**: Set real DATABASE_URL
2. **API**: Use Gunicorn/uWSGI
3. **Frontend**: Use Streamlit Cloud or Docker
4. **Database**: Managed PostgreSQL (AWS RDS, Azure, etc.)
5. **LLM**: Keep Ollama on-premise or use managed service

See [README.md - Deployment](README.md#deployment) for details.

---

## 📞 Support

| Issue | Solution |
|-------|----------|
| API won't start | Check Python version (3.10+), requirements installed |
| Database errors | Verify PostgreSQL running, DATABASE_URL correct |
| Frontend blank | Check API is responding at /health endpoint |
| Slow performance | Increase resources, check database indices |
| Tests fail | Run `pytest -v` to see detailed errors |

---

## 📊 Data Integrity Checks

```bash
# Check database is populated
cd backend
python -c "
from app.db.database import SessionLocal
from app.repositories import AnalyticsRepository
db = SessionLocal()
stats = AnalyticsRepository.get_dashboard_stats(db)
print(f'Total roles: {stats[\"total_roles\"]}')
print(f'Total activities: {stats[\"total_activities\"]}')
print(f'Average AI exposure: {stats[\"average_ai_exposure\"]:.2%}')
db.close()
"
```

**Expected Output:**
```
Total roles: 20
Total activities: 100+
Average AI exposure: 45-55%
```

---

**Last Updated**: 2026-08-30  
**Application Version**: 1.0.0  
**Status**: Production Ready ✅
