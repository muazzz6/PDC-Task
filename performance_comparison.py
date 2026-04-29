"""
Performance Comparison & Analysis
Compare sequential vs parallel vs API-based operations
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd
from sequential_operations import SequentialCloudOperations
from parallel_operations import ParallelCloudOperations


class PerformanceAnalyzer:
    """Analyze and compare performance across different methods"""
    
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_all_tests(self, files: List[str], file_names: List[str], max_workers: int = 5):
        """Run all comparison tests"""
        print(f"\n{'#'*70}")
        print(f"# COMPREHENSIVE PERFORMANCE TEST")
        print(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"# Files: {len(files)}")
        print(f"# Workers: {max_workers}")
        print(f"{'#'*70}\n")
        
        # Sequential operations
        print("\n📊 PHASE 1: Sequential Operations")
        print("─" * 70)
        try:
            seq_ops = SequentialCloudOperations()
            seq_upload_time, seq_upload_stats = seq_ops.sequential_upload(files)
            seq_download_time, seq_download_stats = seq_ops.sequential_download(file_names)
            
            self.results['sequential'] = {
                'upload_time': seq_upload_time,
                'upload_stats': seq_upload_stats,
                'download_time': seq_download_time,
                'download_stats': seq_download_stats,
                'total_time': seq_upload_time + seq_download_time
            }
        except Exception as e:
            print(f"❌ Sequential operations failed: {e}")
            self.results['sequential'] = {'error': str(e)}
        
        # Parallel operations
        print("\n📊 PHASE 2: Parallel Operations")
        print("─" * 70)
        try:
            par_ops = ParallelCloudOperations(max_workers=max_workers)
            par_upload_time, par_upload_stats = par_ops.parallel_upload(files)
            par_download_time, par_download_stats = par_ops.parallel_download(file_names)
            
            self.results['parallel'] = {
                'upload_time': par_upload_time,
                'upload_stats': par_upload_stats,
                'download_time': par_download_time,
                'download_stats': par_download_stats,
                'total_time': par_upload_time + par_download_time,
                'workers': max_workers
            }
        except Exception as e:
            print(f"❌ Parallel operations failed: {e}")
            self.results['parallel'] = {'error': str(e)}
        
        # Generate comparison report
        self.generate_report()
    
    def generate_report(self):
        """Generate and display comparison report"""
        print(f"\n{'='*70}")
        print(f"PERFORMANCE COMPARISON REPORT")
        print(f"{'='*70}\n")
        
        # Create comparison table
        if 'sequential' in self.results and 'error' not in self.results['sequential']:
            seq = self.results['sequential']
            par = self.results['parallel']
            
            comparison_data = {
                'Operation': ['Upload', 'Download', 'Total'],
                'Sequential (s)': [
                    f"{seq['upload_time']:.2f}",
                    f"{seq['download_time']:.2f}",
                    f"{seq['total_time']:.2f}"
                ],
                'Parallel (s)': [
                    f"{par['upload_time']:.2f}",
                    f"{par['download_time']:.2f}",
                    f"{par['total_time']:.2f}"
                ],
                'Speedup': [
                    f"{seq['upload_time']/par['upload_time']:.2f}x",
                    f"{seq['download_time']/par['download_time']:.2f}x",
                    f"{seq['total_time']/par['total_time']:.2f}x"
                ]
            }
            
            df = pd.DataFrame(comparison_data)
            print(df.to_string(index=False))
            print("\n")
            
            # Speed analysis
            print(f"Upload Speed Comparison:")
            print(f"  Sequential: {seq['upload_stats']['average_speed']:.2f} MB/s")
            print(f"  Parallel:   {par['upload_stats']['average_speed']:.2f} MB/s")
            print(f"  Improvement: {(par['upload_stats']['average_speed'] / seq['upload_stats']['average_speed'] - 1) * 100:.1f}%")
            
            print(f"\nDownload Speed Comparison:")
            print(f"  Sequential: {seq['download_stats']['average_speed']:.2f} MB/s")
            print(f"  Parallel:   {par['download_stats']['average_speed']:.2f} MB/s")
            print(f"  Improvement: {(par['download_stats']['average_speed'] / seq['download_stats']['average_speed'] - 1) * 100:.1f}%")
            
            # Analysis
            self._analyze_results()
            
            # Save detailed report
            self._save_json_report()
    
    def _analyze_results(self):
        """Provide detailed analysis"""
        print(f"\n{'─'*70}")
        print("ANALYSIS & INSIGHTS")
        print(f"{'─'*70}\n")
        
        if 'sequential' not in self.results or 'error' in self.results['sequential']:
            print("⚠️  Could not complete analysis due to earlier errors.")
            return
        
        seq = self.results['sequential']
        par = self.results['parallel']
        
        speedup_factor = seq['total_time'] / par['total_time']
        
        print(f"✓ Speedup Factor: {speedup_factor:.2f}x")
        print(f"✓ Time Saved: {seq['total_time'] - par['total_time']:.2f} seconds")
        print(f"✓ Efficiency: {(speedup_factor / par['workers']) * 100:.1f}% (vs ideal)")
        
        print(f"\n📌 KEY OBSERVATIONS:")
        print(f"1. Parallel operations are {speedup_factor:.2f}x faster than sequential")
        print(f"2. With {par['workers']} workers, efficiency is {(speedup_factor / par['workers']) * 100:.1f}%")
        
        # Network bottleneck analysis
        if speedup_factor < par['workers'] * 0.8:
            print(f"3. ⚠️  Network/API may be the bottleneck (speedup < workers)")
        else:
            print(f"3. ✓ Good parallelization (speedup approaching worker count)")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"• Consider increasing workers if speedup < {par['workers']}")
        print(f"• Check network bandwidth (may limit parallel improvements)")
        print(f"• Monitor API rate limits and throttling")
        print(f"• For large-scale ops, consider async I/O")
    
    def _save_json_report(self):
        """Save detailed results to JSON"""
        filename = f"performance_report_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Detailed report saved: {filename}")
    
    def save_csv_summary(self):
        """Save summary to CSV for further analysis"""
        if 'sequential' not in self.results or 'error' in self.results['sequential']:
            print("Cannot save CSV - results incomplete")
            return
        
        seq = self.results['sequential']
        par = self.results['parallel']
        
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
                'Download Speed Parallel (MB/s)'
            ],
            'value': [
                seq['upload_time'],
                par['upload_time'],
                seq['download_time'],
                par['download_time'],
                seq['total_time'],
                par['total_time'],
                seq['total_time'] / par['total_time'],
                seq['upload_stats']['average_speed'],
                par['upload_stats']['average_speed'],
                seq['download_stats']['average_speed'],
                par['download_stats']['average_speed']
            ]
        }
        
        df = pd.DataFrame(summary)
        filename = f"performance_summary_{self.timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"✓ CSV summary saved: {filename}")


def main():
    """Run full performance comparison"""
    sample_dir = "sample_files"
    if not os.path.exists(sample_dir):
        print(f"Error: {sample_dir} not found!")
        print("Run: python generate_sample_files.py")
        return
    
    files = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith('.txt')]
    file_names = [os.path.basename(f) for f in files]
    
    analyzer = PerformanceAnalyzer()
    analyzer.run_all_tests(files, file_names, max_workers=5)
    analyzer.save_csv_summary()


if __name__ == "__main__":
    main()
