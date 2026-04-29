#!/usr/bin/env python3
"""
Pre-Flight Check - Verify lab environment is ready
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print styled header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def check_item(name, check_fn):
    """Check and report on an item"""
    try:
        result = check_fn()
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        return result
    except Exception as e:
        print(f"❌ {name}")
        print(f"   Error: {e}")
        return False


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    return version.major >= 3 and version.minor >= 6


def check_file_exists(filename):
    """Check if file exists"""
    return Path(filename).exists()


def check_directory_exists(dirname):
    """Check if directory exists"""
    return Path(dirname).exists()


def check_package(package_name):
    """Check if package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def check_supabase_config():
    """Check Supabase configuration"""
    try:
        from cloud_config import SUPABASE_CONFIG, ACTIVE_CONFIG
        
        # Check if Supabase is active
        if ACTIVE_CONFIG.get('provider') != 'supabase':
            return False
        
        # Check required fields
        required = ['url', 'key', 'bucket_name']
        for field in required:
            if not SUPABASE_CONFIG.get(field):
                return False
            if SUPABASE_CONFIG[field].startswith('YOUR_'):
                return False
        
        return True
    except:
        return False


def check_supabase_connection():
    """Test Supabase connection"""
    try:
        from cloud_config import ACTIVE_CONFIG
        
        if ACTIVE_CONFIG.get('provider') != 'supabase':
            return None  # Skip if not using Supabase
        
        from supabase import create_client
        
        client = create_client(ACTIVE_CONFIG['url'], ACTIVE_CONFIG['key'])
        result = client.storage.from_(ACTIVE_CONFIG['bucket_name']).list()
        return True
    except Exception as e:
        return False


def main():
    """Run all checks"""
    print_header("PRE-FLIGHT CHECK - Lab Environment Verification")
    
    print("📋 Checking system components...\n")
    
    # System checks
    checks = [
        ("Python version (3.6+)", check_python_version),
        ("cloud_config.py exists", lambda: check_file_exists("cloud_config.py")),
        ("sample_files/ directory", lambda: check_directory_exists("sample_files")),
        ("api/ directory", lambda: check_directory_exists("api")),
    ]
    
    system_ok = all(check_item(name, fn) for name, fn in checks)
    
    print("\n📦 Checking Python packages...\n")
    
    packages = [
        ("boto3", "boto3"),
        ("requests", "requests"),
        ("pandas", "pandas"),
        ("Flask", "flask"),
        ("Supabase", "supabase"),
    ]
    
    packages_ok = all(check_item(name, lambda p=pkg: check_package(p)) 
                     for name, pkg in packages)
    
    print("\n☁️  Checking Supabase configuration...\n")
    
    config_ok = check_item("Supabase config filled in", check_supabase_config)
    
    if config_ok:
        print(f"   Testing connection...", end=" ", flush=True)
        try:
            result = check_supabase_connection()
            if result:
                print("✅ Connected")
                connection_ok = True
            else:
                print("❌ Connection failed")
                print("   - Check credentials in cloud_config.py")
                print("   - Check bucket exists in Supabase console")
                connection_ok = False
        except:
            print("❌ Connection error")
            connection_ok = False
    else:
        print("   ⚠️  Configuration not complete")
        print("   Run: python setup_supabase.py")
        connection_ok = False
    
    # Summary
    print_header("SUMMARY")
    
    print("Status:")
    print(f"  System components:  {'✅ OK' if system_ok else '❌ Issues found'}")
    print(f"  Python packages:    {'✅ OK' if packages_ok else '❌ Issues found'}")
    print(f"  Supabase config:    {'✅ OK' if config_ok else '⚠️  Not configured'}")
    print(f"  Supabase connection: {'✅ OK' if connection_ok else '❌ Cannot connect'}")
    
    all_ok = system_ok and packages_ok and config_ok and connection_ok
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ ALL CHECKS PASSED - Lab is ready to run!\n")
        print("Next steps:")
        print("  1. Run: python generate_sample_files.py")
        print("  2. Run: python run_lab.py")
        print("  3. Choose: Option 7 (Run ALL tests)")
        print("\n" + "="*70 + "\n")
        return 0
    else:
        print("❌ ISSUES FOUND - Please fix before running lab\n")
        
        if not packages_ok:
            print("Fix packages:")
            print("  pip install -r requirements.txt")
            print("  pip install -r api/requirements.txt")
        
        if not config_ok:
            print("Fix configuration:")
            print("  python setup_supabase.py")
        
        if not connection_ok:
            print("Fix connection:")
            print("  - Verify credentials in cloud_config.py")
            print("  - Check Supabase bucket exists")
            print("  - Test credentials: python setup_supabase.py --verify")
        
        print("\n" + "="*70 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
