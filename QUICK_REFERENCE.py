#!/usr/bin/env python3
"""
Quick Reference - Copy-Paste Commands
Universal Supabase-Ready Lab
"""

# ============================================
# COPY-PASTE THESE COMMANDS IN ORDER
# ============================================

# FOR WINDOWS USERS (in Command Prompt or PowerShell):

# 1. Go to project directory
# cd c:\Users\muazt\OneDrive\Desktop\pdc

# 2. Install dependencies
# pip install -r requirements.txt && pip install -r api/requirements.txt

# 3. Setup Supabase (Interactive Wizard - Recommended)
# python setup_supabase.py

# 4. Generate sample test files
# python generate_sample_files.py

# 5. Optional: Verify everything is ready
# python preflight_check.py

# 6. Run the lab
# python run_lab.py

# 7. When prompted, choose: 7 (Run ALL tests)


# ============================================
# FOR MACOS/LINUX USERS (in Terminal):

# 1. Go to project directory
# cd ~/Desktop/pdc

# 2. Create virtual environment (optional but recommended)
# python3 -m venv venv
# source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
# pip install -r requirements.txt && pip install -r api/requirements.txt

# 4. Setup Supabase (Interactive Wizard)
# python3 setup_supabase.py

# 5. Generate sample test files
# python3 generate_sample_files.py

# 6. Run the lab
# python3 run_lab.py

# 7. When prompted, choose: 7 (Run ALL tests)


# ============================================
# INDIVIDUAL COMMANDS (If you prefer step-by-step)

# Generate sample files only
# python generate_sample_files.py

# Run sequential operations only
# python sequential_operations.py

# Run parallel operations only
# python parallel_operations.py

# Run complete test suite (all at once)
# python complete_test_suite.py

# Start API server (in separate terminal)
# python -m api.app

# Test API client
# python api/client.py

# Verify configuration
# python preflight_check.py

# Reconfigure Supabase
# python setup_supabase.py


# ============================================
# ALL-IN-ONE ONE-LINER

# For those who want to copy-paste ONE command:

# Windows:
# python -c "import subprocess; subprocess.call('setup_supabase.py'); subprocess.call('generate_sample_files.py'); subprocess.call('run_lab.py')"

# macOS/Linux:
# python3 setup_supabase.py && python3 generate_sample_files.py && python3 run_lab.py


# ============================================
# EXPECTED OUTPUTS

# After setup_supabase.py:
# ✅ Supabase is configured
# ✅ Connected to bucket
# Ready to run lab!

# After generate_sample_files.py:
# ✅ Generated 15 sample files
# ✅ Total size: ~100MB
# Ready for testing!

# After run_lab.py -> Option 7:
# ✅ All tests completed
# ✅ Performance report generated
# ✅ JSON/CSV results available
# Ready to write your report!


# ============================================
# FILE STRUCTURE AFTER RUNNING

# pdc/
# ├── sample_files/        (15 generated test files)
# ├── downloads/           (files downloaded directly)
# ├── api_downloads/       (files downloaded via API)
# ├── performance_report_*.json
# ├── performance_summary_*.csv
# ├── complete_report_*.json
# └── (other original files)


# ============================================
# NEXT STEPS AFTER LAB RUNS

# 1. Review generated reports
#    - Check performance_report_*.json
#    - Open performance_summary_*.csv in Excel
#    - Read analysis in complete_report_*.json

# 2. Write your lab report
#    - Open REPORT_TEMPLATE.md
#    - Fill in results from reports
#    - Add your analysis
#    - Write conclusions

# 3. Submit your work
#    - Results JSON/CSV files
#    - Your completed report (1-2 pages)
#    - Optional: screenshots


# ============================================
# TROUBLESHOOTING QUICK COMMANDS

# Issue: "Module not found"
# Fix: pip install -r requirements.txt && pip install -r api/requirements.txt

# Issue: "Cannot connect to Supabase"
# Fix: python setup_supabase.py
# (Re-run configuration wizard)

# Issue: "API not running"
# Fix: python -m api.app
# (In separate terminal)

# Issue: "Tests running slowly"
# Check: python preflight_check.py
# (Get diagnostic info)

# Issue: "Want to see everything working"
# Run: python run_lab.py --auto
# (Full automatic execution)


# ============================================
# KEY FILES TO KNOW

print("""
KEY FILES REFERENCE:

📖 Documentation:
  - START_HERE.md         → 60-second intro
  - README.md             → Full guide
  - QUICKSTART.md         → Quick setup
  - TROUBLESHOOTING.md    → Problem solving

🔧 Setup Scripts:
  - setup_supabase.py     → Configure Supabase (interactive)
  - preflight_check.py    → Verify environment
  - run_lab.py            → Main orchestration (interactive menu)

🧪 Test Scripts:
  - sequential_operations.py     → Baseline test
  - parallel_operations.py       → Parallel test
  - complete_test_suite.py       → All tests at once
  - performance_comparison.py    → Direct comparison

🌐 API:
  - api/app.py            → Flask API server
  - api/client.py         → API client for testing

📋 Report:
  - REPORT_TEMPLATE.md    → Write your 1-2 page report here

⚙️ Configuration:
  - cloud_config.py       → Credentials (auto-filled by wizard)
  - requirements.txt      → Python packages
  - api/requirements.txt  → API packages
""")


# ============================================
# QUICK STATS

print("""
TYPICAL TIMING:

Setup:
  - Install packages:        2 min
  - Run Supabase wizard:     5 min
  - Generate test files:     1 min
  - Total Setup:            ~8 min

Lab Execution:
  - Sequential operations:   2 min
  - Parallel operations:     1 min
  - API testing:            2 min
  - Analysis:               1 min
  - Total Execution:        ~6 min

Reporting:
  - Review results:         5 min
  - Write report:          30 min
  - Total Reporting:       ~35 min

GRAND TOTAL: ~50 minutes (including report)
""")


# ============================================
# FINAL CHECKLIST

print("""
✅ BEFORE RUNNING LAB:

  □ Python 3.6+ installed
  □ Internet connection active
  □ 2GB+ disk space free
  □ ~1 hour available
  □ pip working (test: pip --version)

✅ BEFORE RUNNING run_lab.py:

  □ Dependencies installed (pip install -r requirements.txt)
  □ Supabase configured (python setup_supabase.py)
  □ Sample files generated (python generate_sample_files.py)
  □ Environment verified (python preflight_check.py) - OPTIONAL

✅ AFTER LAB COMPLETES:

  □ Check downloads/ folder (has files)
  □ Check api_downloads/ folder (has files)
  □ Check for JSON/CSV reports
  □ Review performance data

✅ BEFORE SUBMITTING:

  □ Complete REPORT_TEMPLATE.md
  □ Add your analysis
  □ Write conclusions
  □ Save report
  □ Gather all output files
""")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB QUICK REFERENCE")
    print("="*70)
    print("\nUSAGE: Copy commands from this file and run in terminal\n")
    print("RECOMMENDED STARTING PATH:")
    print("  python setup_supabase.py      (interactive setup)")
    print("  python generate_sample_files.py (create test data)")
    print("  python run_lab.py              (interactive menu)")
    print("  → Choose: 7 (Run ALL tests)")
    print("\n" + "="*70 + "\n")
