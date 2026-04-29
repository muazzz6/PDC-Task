#!/usr/bin/env python3
"""
Supabase Setup Helper
Interactive guide to configure Supabase cloud storage
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print styled header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_step(num, text):
    """Print step"""
    print(f"\n📍 Step {num}: {text}")
    print(f"   {'─'*66}")


def check_config_file():
    """Check if config file exists"""
    config_path = Path("cloud_config.py")
    return config_path.exists()


def read_current_config():
    """Read current Supabase config"""
    try:
        from cloud_config import SUPABASE_CONFIG
        return SUPABASE_CONFIG
    except ImportError:
        return None


def validate_supabase_config(config):
    """Validate Supabase configuration"""
    required_fields = ['url', 'key', 'bucket_name']
    
    for field in required_fields:
        if field not in config:
            return False, f"Missing field: {field}"
        
        value = config[field]
        if not value or value.startswith('YOUR_'):
            return False, f"Not configured: {field}"
    
    if not config['url'].startswith('https://'):
        return False, "URL should start with https://"
    
    if len(config['key']) < 10:
        return False, "API key seems too short"
    
    return True, "Valid"


def test_supabase_connection(config):
    """Test Supabase connection"""
    print("\n🔗 Testing Supabase connection...")
    
    try:
        from supabase import create_client
        
        client = create_client(config['url'], config['key'])
        
        # Try to list files
        try:
            result = client.storage.from_(config['bucket_name']).list()
            print(f"   ✅ Connected successfully!")
            print(f"   ✅ Bucket '{config['bucket_name']}' accessible")
            print(f"   ✅ Files in bucket: {len(result)}")
            return True
        
        except Exception as e:
            if "not found" in str(e).lower():
                print(f"   ⚠️  Bucket '{config['bucket_name']}' not found")
                print(f"   Hint: Create bucket in Supabase console first")
                return False
            else:
                raise
    
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False


def interactive_setup():
    """Interactive setup wizard"""
    print_header("SUPABASE CONFIGURATION WIZARD")
    
    print("Welcome! This wizard will help you configure Supabase.")
    print("Takes about 2-3 minutes.\n")
    
    print("ℹ️  REQUIREMENTS:")
    print("   • Supabase account (free at https://supabase.com/)")
    print("   • Project created")
    print("   • Storage bucket created")
    print("   • API credentials copied")
    
    # Step 1: Welcome
    print_step(1, "Do you have Supabase credentials ready?")
    
    ready = input("\n   Have you created a Supabase project? (y/n): ").lower() == 'y'
    
    if not ready:
        show_supabase_setup_guide()
        return False
    
    # Step 2: Get credentials
    print_step(2, "Enter your Supabase credentials")
    
    print("\n   ℹ️  Where to find these:")
    print("      - URL: Settings → API → Project URL")
    print("      - Key: Settings → API → anon public")
    print("      - Bucket: Storage → Buckets → your bucket name")
    
    while True:
        url = input("\n   🔗 Supabase URL (https://...): ").strip()
        if url.startswith('https://') and '.supabase.co' in url:
            break
        print("   ❌ Invalid URL. Must start with https:// and contain .supabase.co")
    
    while True:
        key = input("\n   🔑 API Key (eyJ...): ").strip()
        if len(key) > 50:
            break
        print("   ❌ API Key seems too short")
    
    while True:
        bucket = input("\n   🗂️  Bucket name (e.g., 'pdc-lab-files'): ").strip()
        if bucket and ' ' not in bucket:
            break
        print("   ❌ Bucket name cannot be empty or have spaces")
    
    # Step 3: Verify credentials format
    print_step(3, "Verifying credentials format...")
    
    new_config = {
        'url': url,
        'key': key,
        'bucket_name': bucket
    }
    
    valid, msg = validate_supabase_config(new_config)
    
    if not valid:
        print(f"   ⚠️  Configuration warning: {msg}")
        proceed = input("   Try anyway? (y/n): ").lower() == 'y'
        if not proceed:
            return False
    else:
        print(f"   ✅ Format looks good!")
    
    # Step 4: Test connection
    print_step(4, "Testing connection to Supabase...")
    
    if not test_supabase_connection(new_config):
        print("   ⚠️  Connection test failed")
        print("   Please verify your credentials and bucket exists")
        retry = input("   Retry? (y/n): ").lower() == 'y'
        if not retry:
            return False
        return interactive_setup()  # Restart wizard
    
    # Step 5: Save configuration
    print_step(5, "Saving configuration...")
    
    update_cloud_config(new_config)
    print(f"   ✅ Configuration saved to cloud_config.py")
    
    # Step 6: Summary
    print_header("✅ SETUP COMPLETE!")
    
    print("Your Supabase configuration:")
    print(f"  URL:    {url[:50]}...")
    print(f"  Key:    {key[:20]}...")
    print(f"  Bucket: {bucket}")
    
    print("\n🚀 Next steps:")
    print("  1. Run: python generate_sample_files.py")
    print("  2. Run: python run_lab.py")
    print("  3. Choose: Run ALL tests (full lab)")
    
    return True


def update_cloud_config(config):
    """Update cloud_config.py with new Supabase settings"""
    config_path = Path("cloud_config.py")
    
    content = config_path.read_text()
    
    # Replace URL
    content = content.replace(
        "    'url': 'https://YOUR_PROJECT.supabase.co',",
        f"    'url': '{config['url']}',"
    )
    
    # Replace key
    content = content.replace(
        "    'key': 'YOUR_SUPABASE_API_KEY',",
        f"    'key': '{config['key']}',"
    )
    
    # Replace bucket name
    content = content.replace(
        "    'bucket_name': 'pdc-lab-files'",
        f"    'bucket_name': '{config['bucket_name']}'"
    )
    
    config_path.write_text(content)


def show_supabase_setup_guide():
    """Show Supabase setup guide"""
    print_header("SUPABASE SETUP GUIDE")
    
    print("Follow these steps to create a Supabase project:\n")
    
    print("1️⃣  SIGN UP")
    print("   • Go to: https://supabase.com/")
    print("   • Click 'Sign Up'")
    print("   • Use GitHub, Google, or email")
    print("   • Verify your email")
    
    print("\n2️⃣  CREATE PROJECT")
    print("   • Click 'New Project'")
    print("   • Choose organization (create if needed)")
    print("   • Enter project name (e.g., 'pdc-lab')")
    print("   • Choose region (closest to you)")
    print("   • Set database password (save it!)")
    print("   • Click 'Create new project'")
    print("   • Wait 1-2 minutes for project to initialize")
    
    print("\n3️⃣  CREATE STORAGE BUCKET")
    print("   • Go to: Storage (left sidebar)")
    print("   • Click 'Create bucket'")
    print("   • Enter name: 'pdc-lab-files'")
    print("   • Keep as 'Private' for now")
    print("   • Click 'Create bucket'")
    print("   • Note: Files will be auto-public for this demo")
    
    print("\n4️⃣  GET API CREDENTIALS")
    print("   • Go to: Settings (left sidebar)")
    print("   • Click: API")
    print("   • Copy 'Project URL' (looks like: https://xxx.supabase.co)")
    print("   • Copy 'anon public' key (starts with 'eyJ...')")
    print("   • Save both - you'll need them next")
    
    print("\n5️⃣  COME BACK HERE")
    print("   • Run this script again when ready: python setup_supabase.py")
    print("   • Paste your credentials")
    print("   • Test connection")
    print("   • Start lab!")
    
    print("\n⏱️  Total time: 3-5 minutes\n")


def verify_existing_setup():
    """Verify existing Supabase setup"""
    print_header("VERIFYING SUPABASE SETUP")
    
    config = read_current_config()
    
    if not config:
        print("❌ Could not read current configuration")
        return False
    
    valid, msg = validate_supabase_config(config)
    
    if not valid:
        print(f"❌ Configuration invalid: {msg}\n")
        return False
    
    print("📋 Current configuration:")
    print(f"   URL:    {config['url'][:50]}...")
    print(f"   Key:    {config['key'][:20]}...")
    print(f"   Bucket: {config['bucket_name']}")
    
    print("\n🔗 Testing connection...")
    
    if test_supabase_connection(config):
        print("\n✅ Supabase is properly configured!")
        print("\n🚀 Ready to run lab:")
        print("   python generate_sample_files.py  (create test data)")
        print("   python run_lab.py                (start lab)")
        return True
    else:
        print("\n❌ Cannot connect to Supabase")
        print("   Check credentials in cloud_config.py")
        return False


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--verify':
        verify_existing_setup()
    else:
        if not check_config_file():
            print("❌ cloud_config.py not found!")
            sys.exit(1)
        
        interactive_setup()


if __name__ == "__main__":
    main()
