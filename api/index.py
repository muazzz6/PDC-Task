"""Vercel serverless entrypoint for Flask API."""

import os
import sys

# Ensure root imports (for cloud_config.py) are available in serverless runtime.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from api.app import app
