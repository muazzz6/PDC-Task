"""
Cloud Storage Configuration Templates
Choose ONE provider and fill in credentials
"""

import os

# ============================================
# OPTION 1: AWS S3
# ============================================
AWS_CONFIG = {
    'provider': 'aws_s3',
    'access_key': 'YOUR_AWS_ACCESS_KEY',
    'secret_key': 'YOUR_AWS_SECRET_KEY',
    'region': 'us-east-1',
    'bucket_name': 'pdc-lab-bucket'
}

# ============================================
# OPTION 2: Azure Blob Storage
# ============================================
AZURE_CONFIG = {
    'provider': 'azure_blob',
    'connection_string': 'YOUR_AZURE_CONNECTION_STRING',
    'container_name': 'pdc-lab-container'
}

# ============================================
# OPTION 3: Firebase Storage
# ============================================
FIREBASE_CONFIG = {
    'provider': 'firebase',
    'api_key': 'YOUR_FIREBASE_API_KEY',
    'project_id': 'YOUR_FIREBASE_PROJECT_ID',
    'storage_bucket': 'YOUR_FIREBASE_BUCKET'
}

# ============================================
# OPTION 4: Supabase Storage
# ============================================
SUPABASE_CONFIG = {
    'provider': 'supabase',
    'url': os.getenv('SUPABASE_URL', 'https://mmgtpmperlhmucfsbqdg.supabase.co'),
    'key': os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tZ3RwbXBlcmxobXVjZnNicWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0NTg5ODQsImV4cCI6MjA5MzAzNDk4NH0.vEx2Yw394oPh8--vcniq3JaSZhPJI1N_OWiRQfn2o2k'),
    'bucket_name': os.getenv('SUPABASE_BUCKET', 'PDC')
}

# ============================================
# SELECTED PROVIDER (SUPABASE - RECOMMENDED)
# ============================================
# Set to your chosen provider
ACTIVE_CONFIG = SUPABASE_CONFIG  # Default: Supabase (easiest setup)

# To use other providers, uncomment one of these:
# ACTIVE_CONFIG = AWS_CONFIG
# ACTIVE_CONFIG = AZURE_CONFIG
# ACTIVE_CONFIG = FIREBASE_CONFIG

# Setup Instructions
SETUP_INSTRUCTIONS = """
=== QUICK SETUP GUIDE ===

1. AWS S3:
   - Go to aws.amazon.com/s3/
   - Create free account (12 months free)
   - Create IAM user with S3 permissions
   - Get Access Key and Secret Key
   - Create S3 bucket

2. Azure Blob:
   - Go to azure.microsoft.com/
   - Create free account ($200 credit)
   - Create Storage Account
   - Get Connection String
   - Create container

3. Firebase:
   - Go to firebase.google.com/
   - Create free project
   - Enable Storage
   - Download service account JSON
   - Create bucket

4. Supabase (RECOMMENDED):
   - Go to supabase.com/
   - Sign up (free)
   - Create new project
   - Go to Storage → Create bucket
   - Get credentials from Settings → API

Fill in your credentials above and set ACTIVE_CONFIG
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
