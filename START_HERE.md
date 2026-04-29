# 🎯 GET STARTED IN 60 SECONDS

## Step-by-Step Absolute Quick Start

### ⏱️ Time: 60 seconds (literally!)

```bash
# 1. Install everything (15 sec)
pip install -r requirements.txt && pip install -r api/requirements.txt

# 2. Create test data (10 sec)
python generate_sample_files.py

# 3. Start the wizard (35 sec)
python run_lab.py
```

Choose option "7" for full lab run 🚀

---

## What Happens Next?

```
✅ All prerequisites checked
✅ Sample files generated (15 files)
⏳ Sequential upload/download... (2 min)
⏳ Parallel upload/download... (1 min)
🚀 API server starts
⏳ API download testing... (1 min)
⏳ Complete analysis... (1 min)
📊 Results generated!
```

**Total:** ~10 minutes from start to complete analysis

---

## Your Results Will Show

```
┌─────────────────────────────────────────┐
│  Sequential Upload        45.2 seconds  │
│  Parallel Upload (5 workers) 13.1 sec  │
│  ─────────────────────────────────────  │
│  Speedup:                    3.5x ✓    │
│  Efficiency:                 70% ✓     │
│  API Overhead:               12% ✓     │
│                                         │
│  Status: ✅ All tests passed           │
│  Files saved: 3                        │
│  Download complete!                    │
└─────────────────────────────────────────┘
```

---

## But First - Cloud Setup (2 minutes)

Before running tests, you need:

### ☁️ EASIEST WAY: Use Supabase (Recommended)

```bash
# Step 1: Run setup wizard
python setup_supabase.py

# Wizard will guide you through:
# - Creating free Supabase account
# - Setting up storage bucket
# - Configuring credentials
# - Testing connection
# (Takes 2-3 minutes)
```

**That's it!** The wizard handles everything. ✅

### 🔄 Alternative: Use Other Providers

If you prefer AWS, Azure, or Firebase:
1. Edit `cloud_config.py`
2. Follow setup instructions at top of file
3. Fill in your credentials
4. Set `ACTIVE_CONFIG = YOUR_PROVIDER_CONFIG`

---

## Running Different Tests

### Just Want Numbers? (5 min)
```bash
python complete_test_suite.py
```
Gets everything at once

### Want to Understand Each Step? (20 min)
```bash
python run_lab.py              # Choose tests one-by-one
```
Guided experience

### Test Specific Operation? (Each ~2 min)
```bash
python sequential_operations.py    # Baseline
python parallel_operations.py      # Parallel
python api/client.py             # API testing
```

### Full Automated Run? (10 min)
```bash
python run_lab.py --auto
```
Everything, no interaction

---

## 📊 What You'll Learn

### Theory ➜ Practice
```
Parallelism Concept
     ↓
Sequential Test (1 way)
     ↓
Parallel Test (5 workers)
     ↓
API Overhead Test
     ↓
Comprehensive Analysis
     ↓
Real numbers, real insights ✅
```

### Key Numbers From Lab

- **Speedup Factor:** 2-4x (typical)
- **Network Bottleneck:** Limits to ~100 MB/s
- **API Latency:** 10-50ms per request
- **Optimal Workers:** 5-10 threads
- **Real-world limit:** Network bandwidth

---

## 🎓 After the Lab

### What You'll Know
- ✅ How parallelism works in practice
- ✅ Why network is the bottleneck
- ✅ How to measure performance
- ✅ When to use threading vs async
- ✅ API overhead trade-offs

### Your Report
```
1. Open REPORT_TEMPLATE.md
2. Fill in your results
3. Add analysis (1-2 pages)
4. Submit ✅
```

### Further Experiments
- Try 10, 20 workers (see diminishing returns)
- Use async instead of threading
- Batch operations at API layer
- Compress files before upload
- Different file sizes

---

## 🆘 Troubleshooting (30 sec)

### "Missing module"
```bash
pip install -r requirements.txt
```

### "Cannot connect to cloud"
- Check credentials in `cloud_config.py`
- Test: visit your cloud provider console

### "API not running"
```bash
# Terminal 1:
python -m api.app

# Terminal 2:
python complete_test_suite.py
```

### "Slow results"
- Check internet speed
- Try fewer workers
- Check cloud provider status

**More help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📂 File Structure After First Run

```
pdc/
├── 📄 Documentation (start here!)
├── 🔧 Scripts (run these)
├── 🌐 api/ backend
├── sample_files/₁₅            ← Generated test files
├── downloads/₁₅               ← Downloaded files
├── api_downloads/₁₅           ← API downloads
├── performance_report_*.json   ← Your data 📊
└── performance_summary_*.csv   ← Excel-friendly
```

---

## ⏱️ Timeline

```
+-----+----+--------+-----+----+--------+-----+------+
| 0-5 | 5  |  5-15  | 15  | 15 |  15-20 | 20  | 20+ |
+-----+----+--------+-----+----+--------+-----+------+
|Inst.| Gen| Seq    | Par | API| Report | CSV | Done|
|     |    | Upload | DL  | Up | Anal   |     |     |
+-----+----+--------+-----+----+--------+-----+------+
```

---

## 🚀 Let's Go!

### Command to Start NOW:
```bash
python run_lab.py
```

### Or Copy-Paste This:
```bash
pip install -r requirements.txt && pip install -r api/requirements.txt && python generate_sample_files.py && python run_lab.py
```

---

## Expected Output (First Run)

```
################################################################################
# PDC LAB - CLOUD COMPUTING & SCALING
################################################################################

📋 Available Tests:
  1. Generate sample files (required first)
  2. Run sequential operations
  3. Run parallel operations
  4. Start API server
  5. Run API-based operations
  6. Run complete comparison
  7. Run ALL tests (full lab) ← Pick this!
  8. Exit

Select option (1-8): 7
```

Then watch as tests run and results compile! 📈

---

## 🏁 When You're Done

### Deliverables
1. ✅ `performance_report_*.json` - Raw data
2. ✅ `performance_summary_*.csv` - Summary
3. ✅ `YOUR_REPORT.md` - Your analysis (use template)
4. ✅ Screenshots - Optional but good

### Your Report Should Show
- Performance table (sequential vs parallel vs API)
- Speedup calculation
- Explanation of bottlenecks
- Key findings (1-2 pages)

---

## Questions?

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Cloud auth fails | Check credentials in `cloud_config.py` |
| Slow results | Check internet speed or try fewer workers |
| API not working | Start API in separate terminal first |
| Need help? | Read `TROUBLESHOOTING.md` 📖 |

---

## 🎉 You're Ready!

```
1 command to run everything:  python run_lab.py
Expected time:                ~20 minutes
Learning value:               ★★★★★
Difficulty:                   ★★☆☆☆
Fun factor:                   ★★★★☆
```

**→ RUN IT NOW! →**

```bash
python run_lab.py
```

---

## Deploy API To Vercel

Use this when your instructor asks for cloud deployment of the API layer.

### 1) Install and login

```bash
npm i -g vercel
vercel login
```

### 2) Set production env vars in Vercel

```bash
vercel env add SUPABASE_URL production
vercel env add SUPABASE_KEY production
vercel env add SUPABASE_BUCKET production
```

Values to use:
- `SUPABASE_URL`: `https://mmgtpmperlhmucfsbqdg.supabase.co`
- `SUPABASE_KEY`: your anon key
- `SUPABASE_BUCKET`: `PDC`

### 3) Deploy

```bash
vercel --prod
```

### 4) Test deployment

```bash
curl https://YOUR-VERCEL-URL/health
curl https://YOUR-VERCEL-URL/files
```

If `/health` returns `status: healthy`, deployment is complete.

Good luck! 🚀📊💪
