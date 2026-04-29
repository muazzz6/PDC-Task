# ⚡ QUICKSTART GUIDE - Cloud Computing Lab

**Expected Time:** 30 minutes for first run

## 🚀 Super Quick Start (5 mins)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### 2. Generate Test Files
```bash
python generate_sample_files.py
```

✓ Creates 15 sample files in `sample_files/` directory

### 3. Choose Cloud Provider

Edit `cloud_config.py` and set your provider:

```python
# Choose ONE of these:
ACTIVE_CONFIG = AWS_CONFIG         # AWS S3
# ACTIVE_CONFIG = AZURE_CONFIG      # Azure Blob
# ACTIVE_CONFIG = FIREBASE_CONFIG   # Firebase
# ACTIVE_CONFIG = SUPABASE_CONFIG   # Supabase
```

Then fill in your credentials (see instructions in cloud_config.py)

### 4. Run Tests

**Option A: Run Everything Automatically**
```bash
python run_lab.py --auto
```

**Option B: Interactive Menu**
```bash
python run_lab.py
```

**Option C: Run Individual Tests**
```bash
python sequential_operations.py      # Baseline
python parallel_operations.py        # Parallel threading
python complete_test_suite.py        # Full comparison
```

---

## 📊 What You'll Get

After running tests, you'll have:

1. **Performance Data:**
   - `performance_report_*.json` → Detailed metrics
   - `performance_summary_*.csv` → Excel-friendly summary

2. **Downloaded Files:**
   - `downloads/` → Sequential downloads
   - `api_downloads/` → API-based downloads

3. **Analysis:**
   - Speedup calculations
   - Efficiency metrics
   - Bottleneck identification

---

## 🏃 Fastest Path (Minimum Viable Run)

```bash
# Terminal: Install and setup
pip install -r requirements.txt
pip install -r api/requirements.txt

# Run setup wizard (interactive, 2 mins)
python setup_supabase.py

# Generate test files
python generate_sample_files.py

# Run complete test suite
python complete_test_suite.py
```

**Total time:** ~10-15 minutes

---

## 📈 Expected Results

### Speedup Factor
- **Without parallelism:** Baseline time
- **With 5 parallel threads:** 2-5x faster
- Expected typical: **3-3.5x speedup**

### Speed Metrics
- **Upload speed:** 5-20 MB/s (depends on connection)
- **Download speed:** 5-20 MB/s
- **API overhead:** 10-50ms per request

### Sample Output
```
═══════════════════════════════════════════════════════════
SUMMARY - SEQUENTIAL UPLOAD
───────────────────────────────────────────────────────────
Total Time:      45.23s
Files:           15/15 successful
Total Size:      125.50 MB
Avg Speed:       2.77 MB/s
═══════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════
SUMMARY - PARALLEL UPLOAD
───────────────────────────────────────────────────────────
Total Time:      15.67s
Files:           15/15 successful
Total Size:      125.50 MB
Avg Speed:       8.01 MB/s
Speedup:         3.48x faster!
═══════════════════════════════════════════════════════════
```

---

## 🔧 Cloud Provider Setup (2 mins)

### AWS S3
1. Go to https://aws.amazon.com/s3/
2. Sign up (free 12-month tier)
3. Create IAM user with S3 permissions
4. Get Access Key & Secret Key
5. Create S3 bucket (e.g., "pdc-lab-bucket")

### Azure Blob (QUICKEST)
1. Go to https://azure.microsoft.com/
2. Sign up ($200 free credit)
3. Create Storage Account
4. Get connection string
5. Create container

### Firebase
1. Go to https://firebase.google.com/
2. Create new project (free)
3. Enable Cloud Storage
4. Download service account JSON
5. Note your bucket name

### Supabase ⭐ (EASIEST)
1. Go to https://supabase.com/
2. Sign up (free)
3. Create new project
4. Go to Storage → Create bucket (e.g., "pdc-lab-files")
5. Go to Settings → API → Get URL and Key

---

## ❓ Troubleshooting Quick Fixes

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### "Cannot connect to cloud storage"
- Check credentials in `cloud_config.py`
- Verify bucket name is correct
- Test credentials: `python -c "import boto3; print(boto3.__version__)"`

### "API not running"
```bash
# Terminal 1: Start API
python -m api.app

# Terminal 2: Run tests
python complete_test_suite.py
```

### Slow performance
- Check network speed: `speedtest-cli`
- Try reducing worker count: `ParallelCloudOperations(max_workers=3)`
- Check cloud provider rate limits

### Tests failing randomly
- Network may be unstable
- Run multiple times and average results
- Check cloud provider status page

---

## 📋 What Each Script Does

| Script | Purpose | Time |
|--------|---------|------|
| `generate_sample_files.py` | Create test data | <1 min |
| `sequential_operations.py` | Baseline performance | 1-3 min |
| `parallel_operations.py` | Parallel testing | 1-2 min |
| `complete_test_suite.py` | Full comparison | 3-5 min |
| `api/app.py` | Start API server | Runs continuously |
| `api/client.py` | Test API performance | 1-2 min |
| `run_lab.py` | Interactive orchestration | - |

---

## 🎯 Learning Checklist

After completing this lab, you will understand:

- ✅ How parallelism speeds up I/O operations
- ✅ Threading vs sequential execution trade-offs
- ✅ Cloud storage integration with Python
- ✅ API overhead and latency measurement
- ✅ Performance optimization bottlenecks
- ✅ Real-world scaling limitations
- ✅ How to measure and analyze performance

---

## 📊 Sample Results Interpretation

**Good Results Look Like:**
- Speedup factor: 2-4x (with 5 workers)
- Efficiency: 40-80%
- API overhead: 10-30%

**Means:**
- ✅ Parallelization working well
- ✅ Network not saturated
- ✅ API layer reasonable

**Poor Results Look Like:**
- Speedup factor: <1.5x
- Efficiency: <30%
- High variance between runs

**Indicates:**
- ⚠️ Network bottleneck
- ⚠️ Rate limiting
- ⚠️ Connection pooling issue

---

## 🚀 Next Steps After Lab Completion

1. **Complete the Report**
   - Use `REPORT_TEMPLATE.md`
   - Fill in your results
   - Add analysis

2. **Experiment Further**
   - Try different worker counts (3, 5, 10, 20)
   - Use larger file sizes
   - Test with different times of day

3. **Implement Optimizations**
   - Connection pooling
   - Request batching
   - Async I/O instead of threading

4. **Share Findings**
   - Compare results with classmates
   - Discuss bottlenecks
   - Share optimizations

---

## 📚 Additional Resources

- Python Threading: https://docs.python.org/3/library/concurrent.futures.html
- Cloud Storage APIs:
  - AWS S3: https://boto3.amazonaws.com/
  - Azure: https://docs.microsoft.com/azure/
  - Firebase: https://firebase.google.com/docs/
- Performance Analysis: https://www.datadoghq.com/
- Async I/O: https://docs.python.org/3/library/asyncio.html

---

## ⏱️ Time Breakdown

| Phase | Time | Notes |
|-------|------|-------|
| Setup | 5 min | Install, configure, generate files |
| Sequential Test | 2 min | Baseline measurement |
| Parallel Test | 1 min | ~3x faster than sequential |
| API Setup | 2 min | Start Flask server |
| API Test | 1 min | Measure API overhead |
| Analysis | 5 min | Review results |
| **Total** | **~20 min** | Ready for full lab |

**With Report Writing:** Add 30-45 minutes

---

**Ready to start? Run:**
```bash
python run_lab.py
```

**Questions? Check:** `README.md` or `TROUBLESHOOTING.md`

Have fun! 🎉
