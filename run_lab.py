#!/usr/bin/env python3
"""
Main Lab Orchestration Script
Run this to execute the entire cloud computing + scaling lab
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime


class LabRunner:
    """Orchestrate the entire lab execution"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = []
    
    def print_header(self, title, subtitle=""):
        """Print styled header"""
        print(f"\n{'#'*80}")
        print(f"# {title}")
        if subtitle:
            print(f"# {subtitle}")
        print(f"{'#'*80}\n")
    
    def print_step(self, number, title, description=""):
        """Print step header"""
        print(f"\n{'='*80}")
        print(f"STEP {number}: {title}")
        if description:
            print(f"{description}")
        print(f"{'='*80}\n")
    
    def run_command(self, command, description=""):
        """Run a shell command"""
        if description:
            print(f"\n📝 {description}")
        print(f"Running: {command}\n")
        
        result = subprocess.run(command, shell=True)
        return result.returncode == 0
    
    def check_prerequisites(self):
        """Check if all prerequisites are installed"""
        self.print_step(0, "PREREQUISITES CHECK", "Verifying required packages and configuration")
        
        required_packages = ['boto3', 'requests', 'pandas', 'supabase']
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package} is installed")
            except ImportError:
                print(f"✗ {package} is NOT installed")
                missing.append(package)
        
        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print("Installing missing packages...")
            for package in missing:
                self.run_command(f"pip install {package}")
        else:
            print(f"\n✅ All prerequisites installed")
        
        # Check Supabase configuration
        self._check_supabase_setup()
    
    def _check_supabase_setup(self):
        """Check Supabase setup"""
        try:
            from cloud_config import ACTIVE_CONFIG
            
            provider = ACTIVE_CONFIG.get('provider')
            
            if provider == 'supabase':
                # Check if configured
                url = ACTIVE_CONFIG.get('url', '').startswith('https://')
                key = len(ACTIVE_CONFIG.get('key', '')) > 10
                bucket = ACTIVE_CONFIG.get('bucket_name', '').strip()
                
                if url and key and bucket:
                    print(f"✓ Supabase is configured")
                else:
                    print(f"⚠️  Supabase configuration incomplete")
                    print(f"   Run: python setup_supabase.py")
            else:
                print(f"✓ Using provider: {provider}")
        
        except Exception as e:
            print(f"⚠️  Configuration check: {e}")
    
    def generate_sample_files(self):
        """Generate test data"""
        self.print_step(1, "GENERATE SAMPLE FILES", 
                       "Creating 15 test files (100KB - 5MB each)")
        
        sample_dir = "sample_files"
        if os.path.exists(sample_dir) and len(os.listdir(sample_dir)) > 0:
            print(f"✓ Sample files already exist in '{sample_dir}/'")
            print(f"  Files: {len(os.listdir(sample_dir))}")
            return True
        
        success = self.run_command("python generate_sample_files.py",
                                  "Generating sample files...")
        
        if success:
            print(f"✅ Sample files generated successfully")
            self.results.append(('Generate Files', 'SUCCESS'))
        else:
            print(f"❌ Failed to generate sample files")
            self.results.append(('Generate Files', 'FAILED'))
        
        return success
    
    def verify_cloud_config(self):
        """Verify cloud configuration is set"""
        self.print_step(2, "CLOUD CONFIGURATION", 
                       "Checking cloud storage setup")
        
        print("⚠️  IMPORTANT: You must configure cloud storage!")
        print("\nSteps:")
        print("1. Open 'cloud_config.py'")
        print("2. Choose your cloud provider (AWS S3 / Azure / Firebase / Supabase)")
        print("3. Get credentials from your cloud provider")
        print("4. Fill in ACTIVE_CONFIG in cloud_config.py")
        print("\nSupported Providers:")
        print("  • AWS S3:     aws.amazon.com/s3/")
        print("  • Azure Blob: azure.microsoft.com/")
        print("  • Firebase:   firebase.google.com/")
        print("  • Supabase:   supabase.com/ (RECOMMENDED)")
        
        configured = input("\nHave you configured cloud storage? (y/n): ").lower() == 'y'
        
        if configured:
            print("✅ Cloud configuration ready")
            self.results.append(('Cloud Config', 'SUCCESS'))
            return True
        else:
            print("⚠️  Skipping cloud tests - configuration incomplete")
            self.results.append(('Cloud Config', 'SKIPPED'))
            return False
    
    def test_sequential(self):
        """Run sequential operations test"""
        self.print_step(3, "SEQUENTIAL OPERATIONS TEST",
                       "Upload and download files one-by-one")
        
        print("Note: This is the baseline test")
        print("Expected duration: 2-5 minutes depending on file size and network\n")
        
        success = self.run_command("python sequential_operations.py",
                                  "Running sequential upload/download...")
        
        if success:
            print(f"✅ Sequential test completed")
            self.results.append(('Sequential Test', 'SUCCESS'))
        else:
            print(f"❌ Sequential test failed")
            self.results.append(('Sequential Test', 'FAILED'))
        
        return success
    
    def test_parallel(self):
        """Run parallel operations test"""
        self.print_step(4, "PARALLEL OPERATIONS TEST",
                       "Upload and download files with 5 concurrent threads")
        
        print("Expected duration: 1-2 minutes (faster than sequential)")
        print("Note: Should see significant speedup\n")
        
        success = self.run_command("python parallel_operations.py",
                                  "Running parallel upload/download...")
        
        if success:
            print(f"✅ Parallel test completed")
            self.results.append(('Parallel Test', 'SUCCESS'))
        else:
            print(f"❌ Parallel test failed")
            self.results.append(('Parallel Test', 'FAILED'))
        
        return success
    
    def start_api_server(self):
        """Start Flask API server"""
        self.print_step(5, "API SERVER SETUP",
                       "Starting Flask API for API-based downloads")
        
        print("The API server will run in the background.")
        print("You can stop it later with Ctrl+C\n")
        
        # Start API in background
        print("Starting API server on http://localhost:5000...")
        print("(This runs in the background)\n")
        
        try:
            # Use Windows-specific command if needed
            if sys.platform == 'win32':
                subprocess.Popen("python -m api.app", 
                                shell=True, 
                                creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen("python -m api.app", 
                                shell=True, 
                                preexec_fn=os.setsid)
            
            time.sleep(3)  # Give server time to start
            print("✅ API server started")
            print("  URL: http://localhost:5000")
            print("  Docs: http://localhost:5000/info\n")
            
            self.results.append(('Start API', 'SUCCESS'))
            return True
        
        except Exception as e:
            print(f"❌ Failed to start API: {e}")
            self.results.append(('Start API', 'FAILED'))
            return False
    
    def test_api(self):
        """Run API-based operations test"""
        self.print_step(6, "API-BASED OPERATIONS TEST",
                       "Download files through custom Flask API")
        
        print("Note: Uses files uploaded in parallel test")
        print("Measures API latency and overhead\n")
        
        success = self.run_command("python api\\client.py",
                                  "Running API download test...")
        
        if success:
            print(f"✅ API test completed")
            self.results.append(('API Test', 'SUCCESS'))
        else:
            print(f"❌ API test failed")
            self.results.append(('API Test', 'FAILED'))
        
        return success
    
    def run_complete_comparison(self):
        """Run complete comparison suite"""
        self.print_step(7, "COMPLETE PERFORMANCE COMPARISON",
                       "Comprehensive analysis combining all methods")
        
        print("This test runs all three methods and generates:")
        print("  • Performance comparison table")
        print("  • Speedup calculations")
        print("  • Efficiency analysis")
        print("  • JSON and CSV reports\n")
        
        success = self.run_command("python complete_test_suite.py",
                                  "Running complete test suite...")
        
        if success:
            print(f"✅ Complete comparison finished")
            self.results.append(('Complete Suite', 'SUCCESS'))
        else:
            print(f"❌ Complete comparison failed")
            self.results.append(('Complete Suite', 'FAILED'))
        
        return success
    
    def generate_report(self):
        """Generate lab report"""
        self.print_step(8, "GENERATE REPORT",
                       "Creating comprehensive lab report")
        
        print("📋 Report Template: REPORT_TEMPLATE.md")
        print("\nHow to complete the report:")
        print("1. Copy REPORT_TEMPLATE.md to YOUR_REPORT.md")
        print("2. Fill in results from JSON/CSV files")
        print("3. Add your analysis and observations")
        print("4. Complete with conclusion\n")
        
        # Show generated files
        print("📊 Generated Data Files:")
        for file in sorted(Path('.').glob('*.json')):
            print(f"  • {file.name}")
        for file in sorted(Path('.').glob('*.csv')):
            print(f"  • {file.name}")
        
        self.results.append(('Report', 'READY'))
        return True
    
    def print_summary(self):
        """Print final summary"""
        self.print_header("LAB EXECUTION COMPLETE",
                         f"Total Duration: {datetime.now() - self.start_time}")
        
        print("📊 RESULTS SUMMARY:\n")
        
        for step_name, status in self.results:
            symbol = '✅' if status == 'SUCCESS' else '⏭️ ' if status == 'SKIPPED' else '⚠️ ' if status == 'READY' else '❌'
            print(f"{symbol} {step_name:.<40} {status}")
        
        print(f"\n{'─'*80}")
        print("📋 Next Steps:")
        print("1. Review generated JSON/CSV files")
        print("2. Complete REPORT_TEMPLATE.md with your analysis")
        print("3. Check api/downloads for all downloaded files")
        print("4. Analyze performance bottlenecks")
        print("5. Document key findings")
        
        print(f"\n📁 Output Files:")
        print("   - performance_report_*.json (detailed metrics)")
        print("   - performance_summary_*.csv (summary data)")
        print("   - complete_report_*.json (full analysis)")
        print("   - downloads/ (directly downloaded files)")
        print("   - api_downloads/ (API-based downloaded files)")
        
        print(f"\n✅ Lab execution finished!\n")
    
    def run_interactive_menu(self):
        """Interactive menu for users to choose tests"""
        self.print_header("PDC LAB - CLOUD COMPUTING & SCALING")
        
        print("This lab demonstrates parallelism in cloud storage operations.")
        print("You'll compare sequential, parallel, and API-based approaches.\n")
        
        print("📋 Available Tests:")
        print("  1. Generate sample files (required first)")
        print("  2. Run sequential operations")
        print("  3. Run parallel operations")
        print("  4. Start API server")
        print("  5. Run API-based operations")
        print("  6. Run complete comparison")
        print("  7. Run ALL tests (full lab)")
        print("  8. Exit\n")
        
        while True:
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                self.generate_sample_files()
            elif choice == '2':
                if not os.path.exists("sample_files") or len(os.listdir("sample_files")) == 0:
                    print("⚠️  Generate sample files first!")
                else:
                    configured = self.verify_cloud_config()
                    if configured:
                        self.test_sequential()
            elif choice == '3':
                if not os.path.exists("sample_files") or len(os.listdir("sample_files")) == 0:
                    print("⚠️  Generate sample files first!")
                else:
                    configured = self.verify_cloud_config()
                    if configured:
                        self.test_parallel()
            elif choice == '4':
                self.start_api_server()
            elif choice == '5':
                self.test_api()
            elif choice == '6':
                self.run_complete_comparison()
            elif choice == '7':
                # Run all tests
                self.check_prerequisites()
                self.generate_sample_files()
                if self.verify_cloud_config():
                    self.test_sequential()
                    self.test_parallel()
                    self.start_api_server()
                    time.sleep(5)
                    self.test_api()
                    self.run_complete_comparison()
                self.generate_report()
                self.print_summary()
                break
            elif choice == '8':
                print("Goodbye! 👋")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")


def main():
    """Main entry point"""
    runner = LabRunner()
    
    # Check arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--auto':
            # Automatic mode - run all tests
            print("Running in automatic mode...\n")
            runner.check_prerequisites()
            if runner.generate_sample_files():
                if runner.verify_cloud_config():
                    runner.test_sequential()
                    runner.test_parallel()
                    runner.start_api_server()
                    time.sleep(5)
                    runner.test_api()
                    runner.run_complete_comparison()
                    runner.generate_report()
                    runner.print_summary()
        elif sys.argv[1] == '--help':
            print("Usage: python run_lab.py [options]")
            print("  --auto      Run all tests automatically")
            print("  --help      Show this help message")
            print("  (no args)   Interactive mode")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Interactive mode
        runner.run_interactive_menu()


if __name__ == "__main__":
    main()
