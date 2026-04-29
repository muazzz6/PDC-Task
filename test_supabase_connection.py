#!/usr/bin/env python3
"""
Simple Supabase Connection Test
Tests if your credentials are valid
"""

import sys

print("Testing Supabase Configuration...")
print("=" * 70)

# Read config
try:
    from cloud_config import SUPABASE_CONFIG
    print("\n✅ Config loaded successfully")
    print(f"   URL:    {SUPABASE_CONFIG.get('url', 'NOT SET')}")
    print(f"   Bucket: {SUPABASE_CONFIG.get('bucket_name', 'NOT SET')}")
    print(f"   Key:    {SUPABASE_CONFIG.get('key', 'NOT SET')[:30]}...")
except Exception as e:
    print(f"\n❌ Failed to load config: {e}")
    sys.exit(1)

# Try to import supabase
print("\n📦 Checking if supabase is installed...")
try:
    import supabase
    print("   ✅ supabase module found")
except ImportError:
    print("   ⚠️  supabase not installed yet")
    print("   Run: python -m pip install supabase --no-build-isolation")
    sys.exit(1)

# Test connection
print("\n🔗 Testing connection to Supabase...")
try:
    from supabase import create_client
    
    url = SUPABASE_CONFIG['url']
    key = SUPABASE_CONFIG['key']
    bucket = SUPABASE_CONFIG['bucket_name']
    
    client = create_client(url, key)
    print("   ✅ Client created")
    
    # Try to access bucket
    result = client.storage.from_(bucket).list()
    print(f"   ✅ Bucket '{bucket}' accessible!")
    print(f"   ✅ Files in bucket: {len(result)}")
    
    print("\n" + "=" * 70)
    print("✅ CONNECTION SUCCESSFUL!")
    print("=" * 70)
    
except Exception as e:
    error_msg = str(e).lower()
    
    print(f"   ❌ Error: {e}")
    
    print("\n⚠️  TROUBLESHOOTING:")
    
    if "not found" in error_msg:
        print("   Issue: Bucket doesn't exist in Supabase")
        print("   Fix: Create bucket named 'PDC' in Supabase console")
    elif "invalid" in error_msg or "unauthorized" in error_msg:
        print("   Issue: Invalid credentials")
        print("   Fix: Check URL and API key in cloud_config.py")
    elif "connection" in error_msg or "network" in error_msg:
        print("   Issue: Network problem")
        print("   Fix: Check your internet connection")
    else:
        print("   Issue: Unknown")
        print(f"   Details: {e}")
    
    print("\n📝 Your current config in cloud_config.py:")
    print(f"   URL:    {SUPABASE_CONFIG.get('url', 'NOT SET')}")
    print(f"   Bucket: {SUPABASE_CONFIG.get('bucket_name', 'NOT SET')}")
    
    sys.exit(1)
