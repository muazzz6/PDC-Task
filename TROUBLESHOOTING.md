# 🔧 TROUBLESHOOTING GUIDE

## Common Issues & Solutions

---

## 🔴 Installation Issues

### Issue: "ModuleNotFoundError: No module named 'boto3'"

**Cause:** Required package not installed

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install boto3 requests pandas
```

**Check if fixed:**
```bash
python -c "import boto3; print('✓ boto3 installed')"
```

---

### Issue: "pip: command not found"

**Cause:** pip not in PATH or Python not installed correctly

**Solution:**
```bash
# On Windows:
python -m pip install -r requirements.txt

# On macOS/Linux:
python3 -m pip install -r requirements.txt
```

---

### Issue: Permission denied when installing packages

**Cause:** Missing permissions or virtual environment issue

**Solution:**
```bash
# Option 1: Use --user flag
pip install --user -r requirements.txt

# Option 2: Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then install:
pip install -r requirements.txt
```

---

## 🔴 Cloud Storage Configuration Issues

### Issue: "Cannot find ACTIVE_CONFIG"

**Cause:** Cloud configuration not set in `cloud_config.py`

**Solution:**
1. Open `cloud_config.py`
2. Find the line: `ACTIVE_CONFIG = SUPABASE_CONFIG`
3. Make sure it's NOT commented out
4. Uncomment it if needed

**Check configuration:**
```python
# Verify in cloud_config.py
print(ACTIVE_CONFIG)  # Should print a dict with credentials
```

---

### Issue: "Invalid credentials" or "Authentication failed"

**Cause:** Wrong credentials or incomplete setup

**Solution - AWS S3:**
```python
AWS_CONFIG = {
    'provider': 'aws_s3',
    'access_key': 'YOUR_AWS_ACCESS_KEY',      # Replace with real key
    'secret_key': 'YOUR_AWS_SECRET_KEY',      # Replace with real secret
    'region': 'us-east-1',
    'bucket_name': 'pdc-lab-bucket'           # Must exist!
}
```

**Solution - Azure:**
```python
AZURE_CONFIG = {
    'provider': 'azure_blob',
    'connection_string': 'DefaultEndpointsProtocol=...',  # Real string
    'container_name': 'pdc-lab-container'
}
```

**Solution - Supabase:**
```python
SUPABASE_CONFIG = {
    'provider': 'supabase',
    'url': 'https://YOUR_PROJECT.supabase.co',  # Real URL
    'key': 'YOUR_REAL_API_KEY',                  # Real key
    'bucket_name': 'pdc-lab-files'
}
```

**Test credentials:**
```bash
python -c "from cloud_config import ACTIVE_CONFIG; print(ACTIVE_CONFIG)"
```

---

### Issue: "Bucket/Container not found"

**Cause:** Bucket doesn't exist or name is wrong

**Solution:**
1. Log into your cloud provider console
2. Check bucket name matches in code
3. If bucket doesn't exist, create it first
4. Verify you have permissions

**Check bucket state:**
```python
# For AWS S3
import boto3
client = boto3.client('s3')
response = client.list_buckets()
print([b['Name'] for b in response['Buckets']])
```

---

## 🔴 Test Execution Issues

### Issue: "No such file or directory: sample_files"

**Cause:** Sample files not generated

**Solution:**
```bash
# Generate sample files first
python generate_sample_files.py

# Verify they were created
ls sample_files/  # or dir sample_files on Windows
```

---

### Issue: Tests run but upload/download fails silently

**Cause:** Cloud credentials expired or rate limited

**Solution:**
```bash
# 1. Refresh credentials (especially temporary tokens)

# 2. Try with fewer files
# Modify script to limit files:
files = files[:3]  # Test with just 3 files

# 3. Add debugging
# Add to scripts:
import logging
logging.basicConfig(level=logging.DEBUG)

# 4. Run again
python sequential_operations.py
```

---

### Issue: "Connection timeout" or "Connection refused"

**Cause:** Network issues or cloud provider down

**Solution:**
```bash
# 1. Check internet connection
ping 8.8.8.8  # Test connectivity

# 2. Check cloud provider status
# AWS: https://status.aws.amazon.com/
# Azure: https://status.azure.com/
# If down, wait and retry

# 3. Check firewall
# Temporarily disable firewall and retry

# 4. Try simpler operation first
python -c "from cloud_config import ACTIVE_CONFIG; print('Config OK')"
```

---

## 🔴 Performance/API Issues

### Issue: "Very slow performance" or "Speedup near 1x"

**Cause:** Network bottleneck or rate limiting

**Solution:**
```bash
# 1. Check bandwidth
# Use speedtest: pip install speedtest-cli
speedtest-cli

# 2. Reduce worker count
# Edit script to use fewer workers:
ops = ParallelCloudOperations(max_workers=2)  # Instead of 5

# 3. Try smaller files
python generate_sample_files.py  # Re-run with defaults

# 4. Check time of day
# Try during off-peak hours (fewer users)
```

---

### Issue: "API not running" or "Connection refused to localhost:5000"

**Cause:** Flask server not started or port in use

**Solution:**
```bash
# Terminal 1: Start API
python -m api.app

# Should see:
# Running on http://0.0.0.0:5000/

# If port already in use:
# Kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>

# Then try again:
python -m api.app
```

---

### Issue: API tests fail but sequential/parallel work

**Cause:** API server issue or connection problem

**Solution:**
```bash
# 1. Check API is healthy
curl http://localhost:5000/health

# Should return JSON with "healthy" status

# 2. Check API logs
# Look at Terminal 1 where API is running
# May show errors

# 3. Check files exist in storage
curl http://localhost:5000/files

# 4. Verify credentials in cloud_config.py
# API uses same credentials as other operations

# 5. Restart API
# Ctrl+C to stop, then:
python -m api.app
```

---

## 🔴 File & Directory Issues

### Issue: "Permission denied" for downloads directory

**Cause:** Downloads directory exists but not writable

**Solution:**
```bash
# 1. Delete existing directory
rm -rf downloads/  # macOS/Linux
rmdir /s downloads  # Windows

# 2. Let script recreate it
python sequential_operations.py

# 3. If still fails, create manually:
mkdir downloads
chmod 755 downloads  # macOS/Linux
```

---

### Issue: "Disk space full" during downloads

**Cause:** Large downloads fill disk space

**Solution:**
```bash
# 1. Check available space
df -h  # macOS/Linux
diskutil list  # macOS specific

# 2. Delete old downloads
rm -rf downloads/*
rm -rf api_downloads/*

# 3. Remove old test files
rm sample_files/*

# 4. Try with fewer/smaller files
python generate_sample_files.py  # Use fewer files
```

---

## 🔴 Python Version Issues

### Issue: "SyntaxError" with f-strings or other features

**Cause:** Python version too old

**Solution:**
```bash
# Check Python version
python --version

# Need Python 3.6+
# If older, upgrade:
# macOS:
brew upgrade python3

# Windows:
# Download from https://www.python.org/

# Verify after upgrade:
python --version
python -m pip install --upgrade pip
```

---

## 🔴 Report Generation Issues

### Issue: "CSV file not found" after tests

**Cause:** Report not generated due to test failure

**Solution:**
```bash
# 1. Ensure tests completed successfully
# Look for output files:
ls *.json  # Should show performance_report_*.json
ls *.csv   # Should show performance_summary_*.csv

# 2. If missing, check test output for errors

# 3. Try running full suite:
python complete_test_suite.py

# 4. Reports should now exist
```

---

### Issue: JSON report is empty or corrupted

**Cause:** Test failed partway through

**Solution:**
```bash
# 1. Check what failed
# Look at console output during test

# 2. Fix that specific part
# E.g., if parallel failed, debug:
python parallel_operations.py

# 3. Once fixed, re-run full suite:
python complete_test_suite.py
```

---

## 🟡 Debugging Tips

### Enable Verbose Logging

Add to any script:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Test Cloud Connection

```python
# Test AWS S3
import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3', region_name='us-east-1')
try:
    response = client.list_buckets()
    print("✓ AWS connection OK")
    print(f"  Buckets: {[b['Name'] for b in response['Buckets']]}")
except ClientError as e:
    print(f"✗ AWS connection failed: {e}")
```

### Check Network

```bash
# Bandwidth test
pip install speedtest-cli
speedtest-cli

# Latency test
ping 8.8.8.8

# DNS test
nslookup google.com  # Windows
dig google.com       # macOS/Linux
```

### Isolated File Test

```bash
# Create single small file
echo "test" > test.txt

# Try operations with just this file
# Modify sequential_operations.py:
files = [os.path.join(sample_dir, 'test.txt')]

# Run test
python sequential_operations.py
```

---

## 🟢 When Everything Works

**Good signs:**
- ✓ All files upload successfully
- ✓ Speedup is 2-4x with 5 workers
- ✓ Efficiency > 40%
- ✓ JSON/CSV reports generated
- ✓ API responds in <100ms

**Next steps:**
- Complete REPORT_TEMPLATE.md
- Experiment with different worker counts
- Try larger or smaller files
- Document your findings

---

## 📞 Still Having Issues?

### Check These Resources

1. **README.md** - Full project documentation
2. **QUICKSTART.md** - Quick setup guide
3. **cloud_config.py** - Configuration options
4. **Code comments** - Inline documentation

### Research

1. Check cloud provider documentation
2. Google the error message exactly
3. Check Stack Overflow if it's a Python issue
4. Look at GitHub issues if it's a library problem

### Get Help

1. Ask classmate/instructor
2. Check cloud provider support
3. Review error message carefully - it usually indicates the problem

---

## ✅ Verification Checklist

Before declaring everything working:

- [ ] `pip list` shows all required packages
- [ ] `python generate_sample_files.py` creates files
- [ ] `python sequent ial_operations.py` uploads/downloads
- [ ] `python parallel_operations.py` runs and shows speedup
- [ ] `python -m api.app` starts without errors
- [ ] `curl http://localhost:5000/health` returns JSON
- [ ] `python complete_test_suite.py` completes
- [ ] JSON and CSV reports exist
- [ ] Results show reasonable speedup (>1.5x)

**All checked?** ✅ Lab is ready!

---

**Last Updated:** 2024  
**Version:** 1.0
