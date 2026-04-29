"""
API Client for Cloud Storage Proxy
Used to compare direct vs API-based operations
"""

import requests
import os
import time
from typing import List, Tuple
from pathlib import Path


class APIClient:
    """Client for interacting with cloud storage API"""
    
    def __init__(self, api_url: str = "http://localhost:5000"):
        self.api_url = api_url
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if API is running"""
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_files(self) -> dict:
        """Get list of files from API"""
        response = self.session.get(f"{self.api_url}/files")
        return response.json()
    
    def get_file_info(self, filename: str) -> dict:
        """Get file metadata"""
        response = self.session.get(f"{self.api_url}/files/{filename}")
        return response.json()
    
    def download_file(self, filename: str, output_path: str) -> dict:
        """Download file through API"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.api_url}/download/{filename}", stream=True)
            response.raise_for_status()
            
            # Write to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            elapsed_time = time.time() - start_time
            file_size = os.path.getsize(output_path)
            
            return {
                'status': 'success',
                'filename': filename,
                'size_bytes': file_size,
                'time_s': elapsed_time,
                'speed_mbps': (file_size / (1024 * 1024)) / elapsed_time if elapsed_time > 0 else 0,
                'api_latency_ms': float(response.headers.get('X-Download-Time-Ms', 0))
            }
        except Exception as e:
            return {
                'status': 'error',
                'filename': filename,
                'error': str(e)
            }
    
    def upload_file(self, filepath: str) -> dict:
        """Upload file through API"""
        start_time = time.time()
        
        try:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f"{self.api_url}/upload", files=files)
            
            elapsed_time = time.time() - start_time
            result = response.json()
            result['total_time_s'] = elapsed_time
            
            return result
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def upload_multiple(self, file_paths: List[str]) -> dict:
        """Upload multiple files through API"""
        start_time = time.time()
        
        try:
            files = [('files', (os.path.basename(fp), open(fp, 'rb'))) for fp in file_paths]
            response = self.session.post(f"{self.api_url}/upload-multiple", files=files)
            
            # Close file handles
            for _, (_, f) in files:
                f.close()
            
            elapsed_time = time.time() - start_time
            result = response.json()
            result['total_time_s'] = elapsed_time
            
            return result
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def test_api_download():
    """Test API-based downloads"""
    print(f"\n{'='*60}")
    print(f"API-BASED DOWNLOAD TEST")
    print(f"{'='*60}\n")
    
    client = APIClient()
    
    # Check API health
    if not client.health_check():
        print("❌ API is not running!")
        print("Start the API with: python api/app.py")
        return
    
    print("✓ API is running")
    
    # Get file list
    try:
        files_response = client.list_files()
        files = [f['name'] for f in files_response.get('files', [])]
        print(f"✓ Retrieved {len(files)} files from cloud storage")
    except Exception as e:
        print(f"❌ Failed to get file list: {e}")
        return
    
    if not files:
        print("⚠️  No files found in storage!")
        return
    
    # Test API downloads
    os.makedirs("api_downloads", exist_ok=True)
    
    start_time = time.time()
    stats = {
        'total_files': len(files),
        'successful': 0,
        'failed': 0,
        'total_size': 0,
        'file_details': []
    }
    
    print(f"\nDownloading {len(files)} files through API...\n")
    
    for idx, filename in enumerate(files, 1):
        result = client.download_file(filename, f"api_downloads/{filename}")
        
        if result['status'] == 'success':
            print(f"  [{idx}/{len(files)}] ✓ {filename}")
            print(f"      Size: {result['size_bytes'] / (1024 * 1024):.2f} MB | Time: {result['time_s']:.2f}s | Speed: {result['speed_mbps']:.2f} MB/s")
            print(f"      API Latency: {result['api_latency_ms']:.2f} ms")
            stats['successful'] += 1
            stats['total_size'] += result['size_bytes']
            stats['file_details'].append(result)
        else:
            print(f"  [{idx}/{len(files)}] ✗ {filename}: {result.get('error', 'Unknown error')}")
            stats['failed'] += 1
    
    total_time = time.time() - start_time
    stats['total_time'] = total_time
    stats['average_speed'] = (stats['total_size'] / (1024 * 1024)) / total_time if total_time > 0 else 0
    
    # Print summary
    print(f"\n{'─'*60}")
    print(f"API DOWNLOAD SUMMARY")
    print(f"{'─'*60}")
    print(f"Total Time:      {total_time:.2f}s")
    print(f"Files:           {stats['successful']}/{stats['total_files']} successful")
    print(f"Total Size:      {stats['total_size'] / (1024 * 1024):.2f} MB")
    print(f"Avg Speed:       {stats['average_speed']:.2f} MB/s")
    print(f"{'='*60}\n")
    
    return total_time, stats


if __name__ == "__main__":
    test_api_download()
