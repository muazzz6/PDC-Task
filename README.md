# PDC Lab - Cloud Computing & Scaling

## Project Structure

```
pdc/
├── sample_files/              # Generated sample test files
├── downloads/                 # Downloaded files (direct method)
├── api_downloads/             # Downloaded files (API method)
├── api/                        # Flask API backend
│   ├── app.py                # Main API server
│   ├── client.py             # API client
│   └── requirements.txt       # API dependencies
├── generate_sample_files.py   # Create test data
├── cloud_config.py            # Cloud storage configuration
├── sequential_operations.py   # Sequential upload/download
├── parallel_operations.py     # Parallel upload/download (threading)
├── performance_comparison.py  # Direct comparison tool
├── complete_test_suite.py     # Comprehensive testing suite
├── requirements.txt           # Main dependencies
└── README.md                  # This file
```

## Quick Start Guide

### 1. Setup Cloud Storage (Choose ONE)

**AWS S3:**
```bash
# Create account: https://aws.amazon.com/s3/
# Get credentials and fill in cloud_config.py
ACTIVE_CONFIG = AWS_CONFIG
```

**Azure Blob:**
```bash
# Create account: https://azure.microsoft.com/
# Get connection string
ACTIVE_CONFIG = AZURE_CONFIG
```

**Firebase:**
```bash
# Create project: https://firebase.google.com/
# Enable storage bucket
ACTIVE_CONFIG = FIREBASE_CONFIG
```

**Supabase (Recommended):**
```bash
# Free tier: https://supabase.com/
# Create project → Storage → Create bucket
ACTIVE_CONFIG = SUPABASE_CONFIG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### 3. Generate Sample Files

```bash
python generate_sample_files.py
```

Creates 15 sample files (100KB - 5MB) in `sample_files/` directory.

### 4. Update Cloud Configuration

Edit `cloud_config.py` and fill in your cloud storage credentials:

```python
ACTIVE_CONFIG = SUPABASE_CONFIG  # or your chosen provider
```

### 5. Run Performance Tests

**Option A: Sequential vs Parallel Comparison**
```bash
python performance_comparison.py
```

**Option B: Complete Test Suite (with API)**
```bash
# Terminal 1: Start API server
python -m api.app

# Terminal 2: Run complete suite
python complete_test_suite.py
```

## Test Scenarios

### Scenario 1: Sequential Upload & Download

```bash
python sequential_operations.py
```

Measures baseline performance uploading/downloading files one by one.

**Output:**
- Total time
- Individual file metrics
- Average speed (MB/s)

### Scenario 2: Parallel Upload & Download (Threading)

```bash
python parallel_operations.py
```

Uses ThreadPoolExecutor with configurable workers (default: 5).

**Output:**
- Parallel execution time
- Worker efficiency
- Speedup factor

### Scenario 3: API-Based Operations

Start the Flask API:
```bash
cd api
python app.py
```

Run client from another terminal:
```bash
python api/client.py
```

### Scenario 4: Complete Comparison

```bash
python complete_test_suite.py
```

Runs all three methods and generates comprehensive analysis:
- Performance comparison table
- Speedup calculation
- Efficiency analysis
- Bottleneck identification
- API overhead measurement

## API Endpoints

The Flask API provides:

```
GET  /health              - Health check
GET  /info                - API documentation
GET  /files               - List all files
GET  /files/<filename>    - File metadata
GET  /download/<filename> - Download file
GET  /download-info/<fn>  - Download info (no transfer)
POST /upload              - Upload single file
POST /upload-multiple     - Upload multiple files
GET  /stats               - Performance statistics
```

Example usage:
```bash
# List files
curl http://localhost:5000/files

# Download file through API
curl http://localhost:5000/download/sample_file_01.txt > file.txt

# Upload file
curl -F "file=@sample_file_01.txt" http://localhost:5000/upload
```

## Performance Analysis

### Key Metrics

1. **Upload/Download Speed (MB/s)**
   - Sequential baseline
   - Parallel achievement
   - API overhead impact

2. **Speedup Factor**
   - Parallel / Sequential time
   - Expected: Close to worker count
   - Actual: Limited by network/API

3. **Efficiency**
   - (Speedup / Number of Workers) × 100%
   - 100% = Perfect parallelization
   - <50% = Significant bottleneck

4. **API Latency (ms)**
   - Per-request overhead
   - Cumulative API overhead
   - Total vs direct comparison

### Analysis Interpretation

**High Speedup (close to worker count):**
- ✓ Good parallelization
- ✓ Network/API not saturated
- ✓ Threading effective

**Low Speedup (well below worker count):**
- ⚠️ Network bottleneck
- ⚠️ API rate limiting
- ⚠️ Thread contention
- **Solution:** Increase worker pool, optimize requests

**High API Overhead:**
- ⚠️ API proxy adds latency
- ⚠️ Additional serialization/deserialization
- ⚠️ Network hops
- **Solution:** Cache at API layer, batch requests

## Output Files

After running tests:

1. **Completed Downloads:**
   - `downloads/` - Direct downloads
   - `api_downloads/` - API downloads

2. **Performance Reports:**
   - `performance_report_*.json` - Detailed metrics
   - `performance_summary_*.csv` - Summary data
   - `complete_report_*.json` - Full analysis

## Expected Observations

### Parallelism Benefits
- 2-5x speedup typical with 5 workers
- I/O-bound operations see better gains
- Network latency becomes bottleneck

### API Overhead
- 10-50ms per API call
- Adds 5-10% overall latency
- Batch operations reduce impact

### Scaling Limitations
- Network bandwidth: ~100 MB/s typical
- Connection pool: Limits concurrent connections
- Rate limiting: Cloud provider throttling
- Thread overhead: Diminishing returns >10 workers

### Optimal Configuration
- **Workers:** 5-10 (I/O-bound sweet spot)
- **Batch Size:** 10-50 files per batch
- **Connection Pooling:** Essential for parallelism
- **Timeout:** Generous for large files

## Troubleshooting

**"ModuleNotFoundError: No module named 'boto3'"**
```bash
pip install -r requirements.txt
```

**"Connection refused" to cloud storage**
- Check credentials in `cloud_config.py`
- Verify bucket/container name
- Test connectivity: `ping cloudprovider.com`

**"API not running" error**
```bash
# Terminal 1:
python -m api.app

# Terminal 2:
python complete_test_suite.py
```

**Low speedup despite many workers**
- Network bandwidth may be saturated
- Try reducing worker count
- Check cloud provider rate limits
- Monitor actual network utilization

**Different results on repeated runs**
- Network conditions vary
- Cloud provider load fluctuates
- Run multiple times for average
- Use provided CSV to analyze trends

## Learning Outcomes Checklist

- ✓ Understand parallelism in I/O-bound operations
- ✓ Compare sequential vs parallel performance
- ✓ Learn cloud storage integration
- ✓ Understand API overhead and latency
- ✓ Identify real-world bottlenecks
- ✓ Measure network constraints
- ✓ Optimize concurrent operations
- ✓ Analyze performance trade-offs

## Next Steps / Advanced Experiments

1. **Increase Worker Count:**
   ```python
   ops = ParallelCloudOperations(max_workers=20)
   ```

2. **Use Async I/O Instead of Threading:**
   - Implement with `asyncio`, `aiohttp`
   - Better for high concurrency

3. **Connection Pooling:**
   - Reuse connections between requests
   - Reduce setup/teardown overhead

4. **Batch Operations:**
   - Group files for batch processing
   - API-level parallelization

5. **Compression:**
   - Compress before upload
   - Measure bandwidth savings

6. **Caching:**
   - Cache API responses
   - Reduce redundant calls

## References

- **Parallelism:** https://docs.python.org/3/library/concurrent.futures.html
- **AWS S3:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
- **Azure Blob:** https://docs.microsoft.com/en-us/azure/storage/blobs/
- **Flask:** https://flask.palletsprojects.com/
- **Async I/O:** https://docs.python.org/3/library/asyncio.html

---

**Lab Completion Date:** [Your Date]
**Total Time:** ~2 hours
**Status:** ✓ Complete
