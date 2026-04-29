"""
Parallel Upload and Download Operations
Using threading for I/O-bound operations
"""

import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple
import boto3
from cloud_config import ACTIVE_CONFIG


class ParallelCloudOperations:
    """Handle parallel cloud operations with timing"""
    
    def __init__(self, config=None, max_workers=5):
        self.config = config or ACTIVE_CONFIG
        self.provider = self.config.get('provider')
        self.max_workers = max_workers
        self.setup_client()
        self.timings = {}
        self.lock = threading.Lock()
    
    def setup_client(self):
        """Initialize cloud storage client based on provider"""
        try:
            if self.provider == 'aws_s3':
                self.client = boto3.client(
                    's3',
                    aws_access_key_id=self.config['access_key'],
                    aws_secret_access_key=self.config['secret_key'],
                    region_name=self.config['region']
                )
                self.bucket = self.config['bucket_name']
            
            elif self.provider == 'supabase':
                from supabase import create_client
                self.client = create_client(self.config['url'], self.config['key'])
                self.bucket = self.config['bucket_name']
            
            else:
                raise ValueError(f"Provider {self.provider} not yet implemented")
        except Exception as e:
            print(f"\n❌ Failed to initialize {self.provider} client:")
            print(f"   Error: {e}")
            print(f"\n⚠️  SETUP REQUIRED:")
            print(f"   1. Edit cloud_config.py")
            print(f"   2. Fill in credentials for {self.provider}")
            print(f"   3. Set ACTIVE_CONFIG = {self.provider.upper()}_CONFIG")
            raise
    
    def _upload_single_file(self, filepath: str) -> dict:
        """Upload a single file (worker thread function)"""
        try:
            file_start = time.time()
            file_size = os.path.getsize(filepath)
            filename = os.path.basename(filepath)
            
            if self.provider == 'aws_s3':
                self.client.upload_file(filepath, self.bucket, filename)
            elif self.provider == 'supabase':
                with open(filepath, 'rb') as f:
                    self.client.storage.from_(self.bucket).upload(filename, f)
            
            file_time = time.time() - file_start
            size_mb = file_size / (1024 * 1024)
            speed_mbps = size_mb / file_time if file_time > 0 else 0
            
            return {
                'name': filename,
                'status': 'success',
                'size_mb': size_mb,
                'time_s': file_time,
                'speed_mbps': speed_mbps
            }
        except Exception as e:
            return {
                'name': os.path.basename(filepath),
                'status': 'failed',
                'error': str(e)
            }
    
    def _download_single_file(self, filename: str, output_dir: str) -> dict:
        """Download a single file (worker thread function)"""
        try:
            file_start = time.time()
            output_path = os.path.join(output_dir, filename)
            
            if self.provider == 'aws_s3':
                self.client.download_file(self.bucket, filename, output_path)
            elif self.provider == 'supabase':
                response = self.client.storage.from_(self.bucket).download(filename)
                with open(output_path, 'wb') as f:
                    f.write(response)
            
            file_time = time.time() - file_start
            file_size = os.path.getsize(output_path)
            size_mb = file_size / (1024 * 1024)
            speed_mbps = size_mb / file_time if file_time > 0 else 0
            
            return {
                'name': filename,
                'status': 'success',
                'size_mb': size_mb,
                'time_s': file_time,
                'speed_mbps': speed_mbps
            }
        except Exception as e:
            return {
                'name': filename,
                'status': 'failed',
                'error': str(e)
            }
    
    def parallel_upload(self, file_list: List[str]) -> Tuple[float, dict]:
        """
        Upload files in parallel using ThreadPoolExecutor
        
        Args:
            file_list: List of file paths to upload
            
        Returns:
            (total_time, stats_dict)
        """
        print(f"\n{'='*60}")
        print(f"PARALLEL UPLOAD - {len(file_list)} files ({self.max_workers} workers)")
        print(f"{'='*60}")
        
        start_time = time.time()
        stats = {
            'total_files': len(file_list),
            'successful': 0,
            'failed': 0,
            'total_size': 0,
            'file_details': []
        }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            futures = {executor.submit(self._upload_single_file, filepath): filepath for filepath in file_list}
            
            # Process results as they complete
            for idx, future in enumerate(as_completed(futures), 1):
                result = future.result()
                
                if result['status'] == 'success':
                    print(f"  [{idx}/{len(file_list)}] ✓ {result['name']}")
                    print(f"      Size: {result['size_mb']:.2f} MB | Time: {result['time_s']:.2f}s | Speed: {result['speed_mbps']:.2f} MB/s")
                    stats['successful'] += 1
                    stats['total_size'] += result['size_mb'] * (1024 * 1024)
                    stats['file_details'].append(result)
                else:
                    print(f"  [{idx}/{len(file_list)}] ✗ {result['name']}: {result.get('error', 'Unknown error')}")
                    stats['failed'] += 1
        
        total_time = time.time() - start_time
        stats['total_time'] = total_time
        stats['average_speed'] = (stats['total_size'] / (1024 * 1024)) / total_time if total_time > 0 else 0
        
        self._print_summary("PARALLEL UPLOAD", stats, total_time)
        return total_time, stats
    
    def parallel_download(self, file_list: List[str], output_dir: str = "downloads") -> Tuple[float, dict]:
        """
        Download files in parallel using ThreadPoolExecutor
        
        Args:
            file_list: List of file names to download
            output_dir: Directory to save downloaded files
            
        Returns:
            (total_time, stats_dict)
        """
        print(f"\n{'='*60}")
        print(f"PARALLEL DOWNLOAD - {len(file_list)} files ({self.max_workers} workers)")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        start_time = time.time()
        stats = {
            'total_files': len(file_list),
            'successful': 0,
            'failed': 0,
            'total_size': 0,
            'file_details': []
        }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            futures = {executor.submit(self._download_single_file, filename, output_dir): filename for filename in file_list}
            
            # Process results as they complete
            for idx, future in enumerate(as_completed(futures), 1):
                result = future.result()
                
                if result['status'] == 'success':
                    print(f"  [{idx}/{len(file_list)}] ✓ {result['name']}")
                    print(f"      Size: {result['size_mb']:.2f} MB | Time: {result['time_s']:.2f}s | Speed: {result['speed_mbps']:.2f} MB/s")
                    stats['successful'] += 1
                    stats['total_size'] += result['size_mb'] * (1024 * 1024)
                    stats['file_details'].append(result)
                else:
                    print(f"  [{idx}/{len(file_list)}] ✗ {result['name']}: {result.get('error', 'Unknown error')}")
                    stats['failed'] += 1
        
        total_time = time.time() - start_time
        stats['total_time'] = total_time
        stats['average_speed'] = (stats['total_size'] / (1024 * 1024)) / total_time if total_time > 0 else 0
        
        self._print_summary("PARALLEL DOWNLOAD", stats, total_time)
        return total_time, stats
    
    def _print_summary(self, operation_name: str, stats: dict, total_time: float):
        """Print operation summary"""
        print(f"\n{'─'*60}")
        print(f"SUMMARY - {operation_name}")
        print(f"{'─'*60}")
        print(f"Total Time:      {total_time:.2f}s")
        print(f"Files:           {stats['successful']}/{stats['total_files']} successful")
        print(f"Total Size:      {stats['total_size'] / (1024 * 1024):.2f} MB")
        print(f"Avg Speed:       {stats['average_speed']:.2f} MB/s")
        print(f"Workers:         {self.max_workers}")
        print(f"{'='*60}\n")


def main():
    """Test parallel operations"""
    ops = ParallelCloudOperations(max_workers=5)
    
    # Get sample files
    sample_dir = "sample_files"
    if not os.path.exists(sample_dir):
        print(f"Error: {sample_dir} directory not found!")
        print("Run: python generate_sample_files.py")
        return
    
    files = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith('.txt')]
    file_names = [os.path.basename(f) for f in files]
    
    print("\n🔧 Testing PARALLEL Operations...")
    print(f"Provider: {ops.provider}")
    print(f"Files: {len(files)}")
    print(f"Workers: {ops.max_workers}")
    
    # Test parallel upload
    try:
        upload_time, upload_stats = ops.parallel_upload(files)
    except Exception as e:
        print(f"❌ Parallel upload failed: {e}")
        print("Make sure cloud credentials are configured in cloud_config.py")
        return
    
    # Test parallel download
    try:
        download_time, download_stats = ops.parallel_download(file_names)
    except Exception as e:
        print(f"❌ Parallel download failed: {e}")
        return


if __name__ == "__main__":
    main()
