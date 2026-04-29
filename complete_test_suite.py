"""
Complete Test Suite - All Operations
Tests sequential, parallel, and API-based approaches
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

# Import all operations
from sequential_operations import SequentialCloudOperations
from parallel_operations import ParallelCloudOperations
from api.client import APIClient


class ComprehensiveTestSuite:
    """Run complete testing suite with all methods"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'configuration': {},
            'tests': {}
        }
    
    def setup(self, files: List[str], file_names: List[str], max_workers: int = 5, api_url: str = None):
        """Setup test configuration"""
        self.files = files
        self.file_names = file_names
        self.max_workers = max_workers
        self.api_url = api_url or "http://localhost:5000"
        
        self.results['configuration'] = {
            'total_files': len(files),
            'workers': max_workers,
            'api_url': self.api_url,
            'total_size_mb': sum(os.path.getsize(f) for f in files) / (1024 * 1024)
        }
    
    def run_complete_suite(self) -> Dict:
        """Run all tests"""
        print(f"\n{'#'*80}")
        print(f"# COMPLETE PERFORMANCE TEST SUITE")
        print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"#{'─'*78}#")
        print(f"# Files: {self.results['configuration']['total_files']}")
        print(f"# Total Size: {self.results['configuration']['total_size_mb']:.2f} MB")
        print(f"# Workers: {self.max_workers}")
        print(f"# API: {self.api_url}")
        print(f"{'#'*80}\n")
        
        # Test 1: Sequential Operations
        self._test_sequential()
        
        # Test 2: Parallel Operations
        self._test_parallel()
        
        # Test 3: API-Based Operations
        self._test_api()
        
        # Generate comprehensive report
        self._generate_comprehensive_report()
        
        return self.results
    
    def _test_sequential(self):
        """Test sequential operations"""
        print(f"\n{'='*80}")
        print(f"TEST 1: SEQUENTIAL OPERATIONS")
        print(f"{'='*80}\n")
        
        try:
            seq_ops = SequentialCloudOperations()
            upload_time, upload_stats = seq_ops.sequential_upload(self.files)
            download_time, download_stats = seq_ops.sequential_download(self.file_names)
            
            self.results['tests']['sequential'] = {
                'status': 'success',
                'upload': {
                    'time_s': upload_time,
                    'stats': upload_stats
                },
                'download': {
                    'time_s': download_time,
                    'stats': download_stats
                },
                'total_time_s': upload_time + download_time
            }
        except Exception as e:
            print(f"❌ Sequential operations failed: {e}")
            self.results['tests']['sequential'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _test_parallel(self):
        """Test parallel operations"""
        print(f"\n{'='*80}")
        print(f"TEST 2: PARALLEL OPERATIONS (workers={self.max_workers})")
        print(f"{'='*80}\n")
        
        try:
            par_ops = ParallelCloudOperations(max_workers=self.max_workers)
            upload_time, upload_stats = par_ops.parallel_upload(self.files)
            download_time, download_stats = par_ops.parallel_download(self.file_names)
            
            self.results['tests']['parallel'] = {
                'status': 'success',
                'workers': self.max_workers,
                'upload': {
                    'time_s': upload_time,
                    'stats': upload_stats
                },
                'download': {
                    'time_s': download_time,
                    'stats': download_stats
                },
                'total_time_s': upload_time + download_time
            }
        except Exception as e:
            print(f"❌ Parallel operations failed: {e}")
            self.results['tests']['parallel'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _test_api(self):
        """Test API-based operations"""
        print(f"\n{'='*80}")
        print(f"TEST 3: API-BASED OPERATIONS")
        print(f"{'='*80}\n")
        
        api_client = APIClient(self.api_url)
        
        # Check API health
        if not api_client.health_check():
            print(f"⚠️  API is not running at {self.api_url}")
            print(f"Start with: python -m api.app")
            self.results['tests']['api'] = {
                'status': 'skipped',
                'reason': 'API not running'
            }
            return
        
        try:
            # Test API downloads only (uploads already tested via parallel/sequential)
            print(f"Testing API-based downloads...")
            
            os.makedirs("api_downloads", exist_ok=True)
            start_time = time.time()
            
            stats = {
                'total_files': len(self.file_names),
                'successful': 0,
                'failed': 0,
                'total_size': 0,
                'file_details': []
            }
            
            api_latencies = []
            
            for idx, filename in enumerate(self.file_names, 1):
                result = api_client.download_file(filename, f"api_downloads/{filename}")
                
                if result['status'] == 'success':
                    print(f"  [{idx}/{len(self.file_names)}] ✓ {filename}")
                    print(f"      Time: {result['time_s']:.2f}s | Speed: {result['speed_mbps']:.2f} MB/s | API Latency: {result['api_latency_ms']:.2f}ms")
                    
                    stats['successful'] += 1
                    stats['total_size'] += result['size_bytes']
                    stats['file_details'].append(result)
                    api_latencies.append(result['api_latency_ms'])
                else:
                    print(f"  [{idx}/{len(self.file_names)}] ✗ {filename}: {result.get('error')}")
                    stats['failed'] += 1
            
            total_time = time.time() - start_time
            stats['total_time'] = total_time
            stats['average_speed'] = (stats['total_size'] / (1024 * 1024)) / total_time if total_time > 0 else 0
            stats['api_avg_latency_ms'] = sum(api_latencies) / len(api_latencies) if api_latencies else 0
            
            self.results['tests']['api'] = {
                'status': 'success',
                'download': {
                    'time_s': total_time,
                    'stats': stats
                },
                'total_time_s': total_time
            }
            
        except Exception as e:
            print(f"❌ API operations failed: {e}")
            self.results['tests']['api'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _generate_comprehensive_report(self):
        """Generate comprehensive comparison report"""
        print(f"\n{'#'*80}")
        print(f"# COMPREHENSIVE ANALYSIS & REPORT")
        print(f"{'#'*80}\n")
        
        # Check if all tests completed successfully
        if not all(self.results['tests'].get(t, {}).get('status') == 'success' 
                  for t in ['sequential', 'parallel', 'api']):
            print("⚠️  Not all tests completed successfully. Showing available results...\n")
        
        # Performance comparison table
        self._print_performance_table()
        
        # Detailed analysis
        self._print_analysis()
        
        # Observations
        self._print_observations()
        
        # Save reports
        self._save_reports()
    
    def _print_performance_table(self):
        """Print performance comparison table"""
        if 'sequential' not in self.results['tests'] or self.results['tests']['sequential'].get('status') != 'success':
            print("Skipping table - incomplete data\n")
            return
        
        print(f"{'─'*80}")
        print(f"PERFORMANCE COMPARISON TABLE")
        print(f"{'─'*80}\n")
        
        seq = self.results['tests']['sequential']
        par = self.results['tests']['parallel']
        api = self.results['tests'].get('api', {})
        
        # Build comparison data
        data = {
            'Operation': ['Upload', 'Download', 'Total'],
            'Sequential (s)': [
                f"{seq['upload']['time_s']:.2f}",
                f"{seq['download']['time_s']:.2f}",
                f"{seq['total_time_s']:.2f}"
            ],
            'Parallel (s)': [
                f"{par['upload']['time_s']:.2f}",
                f"{par['download']['time_s']:.2f}",
                f"{par['total_time_s']:.2f}"
            ]
        }
        
        # Add API column if available
        if api.get('status') == 'success':
            data['API (s)'] = [
                'N/A',
                f"{api['download']['time_s']:.2f}",
                f"{api['total_time_s']:.2f}"
            ]
        
        # Add speedup column
        data['Parallel Speedup'] = [
            f"{seq['upload']['time_s'] / par['upload']['time_s']:.2f}x",
            f"{seq['download']['time_s'] / par['download']['time_s']:.2f}x",
            f"{seq['total_time_s'] / par['total_time_s']:.2f}x"
        ]
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        print("\n")
    
    def _print_analysis(self):
        """Print detailed analysis"""
        print(f"{'─'*80}")
        print(f"DETAILED ANALYSIS")
        print(f"{'─'*80}\n")
        
        if 'sequential' not in self.results['tests'] or self.results['tests']['sequential'].get('status') != 'success':
            print("Cannot perform analysis - incomplete data\n")
            return
        
        seq = self.results['tests']['sequential']
        par = self.results['tests']['parallel']
        
        speedup = seq['total_time_s'] / par['total_time_s']
        efficiency = (speedup / par['workers']) * 100
        
        print(f"✓ Overall Speedup: {speedup:.2f}x (from {par['workers']} workers)")
        print(f"✓ Parallel Efficiency: {efficiency:.1f}%")
        print(f"✓ Time Saved: {seq['total_time_s'] - par['total_time_s']:.2f} seconds")
        
        # Upload analysis
        print(f"\n📤 UPLOAD Performance:")
        seq_upload_speed = seq['upload']['stats']['average_speed']
        par_upload_speed = par['upload']['stats']['average_speed']
        print(f"  Sequential: {seq_upload_speed:.2f} MB/s")
        print(f"  Parallel:   {par_upload_speed:.2f} MB/s")
        print(f"  Improvement: {(par_upload_speed / seq_upload_speed - 1) * 100:.1f}%")
        
        # Download analysis
        print(f"\n📥 DOWNLOAD Performance:")
        seq_download_speed = seq['download']['stats']['average_speed']
        par_download_speed = par['download']['stats']['average_speed']
        print(f"  Sequential: {seq_download_speed:.2f} MB/s")
        print(f"  Parallel:   {par_download_speed:.2f} MB/s")
        print(f"  Improvement: {(par_download_speed / seq_download_speed - 1) * 100:.1f}%")
        
        # API analysis
        if 'api' in self.results['tests'] and self.results['tests']['api'].get('status') == 'success':
            print(f"\n🌐 API OVERHEAD Analysis:")
            api_stats = self.results['tests']['api']['download']['stats']
            api_latency = api_stats['api_avg_latency_ms']
            api_speed = api_stats['average_speed']
            direct_speed = par['download']['stats']['average_speed']
            
            print(f"  API Average Latency: {api_latency:.2f} ms")
            print(f"  API Download Speed: {api_speed:.2f} MB/s")
            print(f"  Direct Download Speed: {direct_speed:.2f} MB/s")
            print(f"  API Overhead: {(direct_speed / api_speed - 1) * 100:.1f}%")
    
    def _print_observations(self):
        """Print key observations"""
        print(f"\n{'─'*80}")
        print(f"KEY OBSERVATIONS & INSIGHTS")
        print(f"{'─'*80}\n")
        
        seq = self.results['tests'].get('sequential', {})
        par = self.results['tests'].get('parallel', {})
        api = self.results['tests'].get('api', {})
        
        if seq.get('status') != 'success' or par.get('status') != 'success':
            print("Cannot generate observations - incomplete data\n")
            return
        
        speedup = seq['total_time_s'] / par['total_time_s']
        efficiency = (speedup / par['workers']) * 100
        
        print(f"1️⃣  Parallelism Impact:")
        if speedup >= par['workers'] * 0.9:
            print(f"   ✓ Excellent: Speedup ({speedup:.2f}x) approaches ideal ({par['workers']}x)")
        elif speedup >= par['workers'] * 0.5:
            print(f"   ⚠️  Good: Speedup ({speedup:.2f}x) is reasonable but below ideal")
            print(f"      → Suggests network/API throttling might be occurring")
        else:
            print(f"   ⚠️  Limited: Speedup ({speedup:.2f}x) is well below ideal ({par['workers']}x)")
            print(f"      → Indicates significant contention or bottleneck")
        
        print(f"\n2️⃣  Efficiency Metrics:")
        print(f"   • Parallel Efficiency: {efficiency:.1f}%")
        if efficiency > 80:
            print(f"   ✓ Very efficient parallelization detected")
        elif efficiency > 50:
            print(f"   ⚠️  Moderate efficiency - room for improvement")
        else:
            print(f"   ⚠️  Low efficiency - investigate bottlenecks")
        
        print(f"\n3️⃣  Bottleneck Analysis:")
        if speedup > par['workers'] * 0.8:
            print(f"   ✓ No major bottleneck detected")
        else:
            print(f"   ⚠️  Likely bottleneck: Network bandwidth or API rate limits")
            print(f"      → Consider: connection pooling, request optimization")
        
        print(f"\n4️⃣  API Overhead:")
        if api.get('status') == 'success':
            api_stats = api['download']['stats']
            api_latency = api_stats['api_avg_latency_ms']
            print(f"   • Average API Latency: {api_latency:.2f} ms per request")
            if api_latency > 100:
                print(f"   ⚠️  High latency - may be network or server issues")
            else:
                print(f"   ✓ Good latency performance")
        else:
            print(f"   ⚠️  API tests not available")
        
        print("\n")
    
    def _save_reports(self):
        """Save detailed reports to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_file = f"complete_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✓ Saved JSON report: {json_file}")
        
        # Save summary CSV
        if 'sequential' in self.results['tests'] and self.results['tests']['sequential'].get('status') == 'success':
            seq = self.results['tests']['sequential']
            par = self.results['tests']['parallel']
            
            summary = {
                'metric': [
                    'Sequential Upload (s)',
                    'Parallel Upload (s)',
                    'Sequential Download (s)',
                    'Parallel Download (s)',
                    'Total Sequential (s)',
                    'Total Parallel (s)',
                    'Speedup Factor',
                    'Upload Speed Sequential (MB/s)',
                    'Upload Speed Parallel (MB/s)',
                    'Download Speed Sequential (MB/s)',
                    'Download Speed Parallel (MB/s)',
                    'Parallel Efficiency (%)'
                ],
                'value': [
                    seq['upload']['time_s'],
                    par['upload']['time_s'],
                    seq['download']['time_s'],
                    par['download']['time_s'],
                    seq['total_time_s'],
                    par['total_time_s'],
                    seq['total_time_s'] / par['total_time_s'],
                    seq['upload']['stats']['average_speed'],
                    par['upload']['stats']['average_speed'],
                    seq['download']['stats']['average_speed'],
                    par['download']['stats']['average_speed'],
                    (seq['total_time_s'] / par['total_time_s'] / par['workers']) * 100
                ]
            }
            
            df = pd.DataFrame(summary)
            csv_file = f"performance_summary_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            print(f"✓ Saved CSV summary: {csv_file}")


def main():
    """Run complete test suite"""
    # Setup
    sample_dir = "sample_files"
    if not os.path.exists(sample_dir):
        print(f"Error: {sample_dir} not found!")
        print("Run: python generate_sample_files.py")
        return
    
    files = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith('.txt')]
    file_names = [os.path.basename(f) for f in files]
    
    if not files:
        print(f"Error: No sample files found in {sample_dir}")
        return
    
    # Run test suite
    suite = ComprehensiveTestSuite()
    suite.setup(files, file_names, max_workers=5)
    suite.run_complete_suite()


if __name__ == "__main__":
    main()
