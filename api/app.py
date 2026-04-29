"""
Flask API for Cloud Storage Proxy
Demonstrates API layer overhead in cloud operations
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import os
import time
from datetime import datetime
from cloud_config import ACTIVE_CONFIG
import boto3
from demo_storage import DEMO_FILES, list_demo_files, get_demo_file_record, build_demo_file_bytes

app = Flask(__name__)
CORS(app)

# Initialize cloud client
def init_cloud_client():
    """Initialize cloud storage client"""
    provider = ACTIVE_CONFIG.get('provider')
    
    if provider == 'aws_s3':
        client = boto3.client(
            's3',
            aws_access_key_id=ACTIVE_CONFIG['access_key'],
            aws_secret_access_key=ACTIVE_CONFIG['secret_key'],
            region_name=ACTIVE_CONFIG['region']
        )
        return client, 'aws_s3'
    
    elif provider == 'supabase':
        from supabase import create_client
        client = create_client(ACTIVE_CONFIG['url'], ACTIVE_CONFIG['key'])
        return client, 'supabase'
    
    return None, None

client, provider = init_cloud_client()
BUCKET = ACTIVE_CONFIG.get('bucket_name')
DEMO_FALLBACK_ENABLED = os.getenv('ENABLE_DEMO_FALLBACK', 'true').lower() == 'true'


# ============================================
# HEALTH & INFO ENDPOINTS
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'provider': provider,
        'bucket': BUCKET
    })


@app.route('/info', methods=['GET'])
def api_info():
    """API information"""
    return jsonify({
        'name': 'Cloud Storage Proxy API',
        'version': '1.0.0',
        'provider': provider,
        'endpoints': {
            '/health': 'Health check',
            '/files': 'List all files',
            '/files/<filename>': 'Get file metadata',
            '/download/<filename>': 'Download file',
            '/upload': 'Upload file',
            '/upload-multiple': 'Upload multiple files'
        }
    })


# ============================================
# FILE LIST ENDPOINTS
# ============================================

@app.route('/files', methods=['GET'])
def list_files():
    """List all files in cloud storage"""
    start_time = time.time()
    
    try:
        files = []
        
        if provider == 'aws_s3':
            response = client.list_objects_v2(Bucket=BUCKET)
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'name': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
        
        elif provider == 'supabase':
            response = client.storage.from_(BUCKET).list()
            files = [
                {
                    'name': item['name'],
                    'size': item.get('metadata', {}).get('size', 0)
                }
                for item in response
            ]

            if not files and DEMO_FALLBACK_ENABLED:
                files = list_demo_files()
                source = 'demo'
            else:
                source = 'supabase'
        else:
            source = 'unknown'

        if provider != 'supabase':
            source = provider
        
        elapsed_time = time.time() - start_time
        
        return jsonify({
            'status': 'success',
            'count': len(files),
            'files': files,
            'source': source,
            'api_latency_ms': elapsed_time * 1000
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/files/<filename>', methods=['GET'])
def get_file_info(filename):
    """Get metadata for specific file"""
    start_time = time.time()
    
    try:
        if provider == 'aws_s3':
            response = client.head_object(Bucket=BUCKET, Key=filename)
            info = {
                'name': filename,
                'size': response['ContentLength'],
                'last_modified': response['LastModified'].isoformat(),
                'content_type': response.get('ContentType', 'unknown')
            }
        
        elif provider == 'supabase':
            # For Supabase, we need to list and filter
            response = client.storage.from_(BUCKET).list()
            info = None
            for item in response:
                if item['name'] == filename:
                    info = {
                        'name': filename,
                        'size': item.get('metadata', {}).get('size', 0)
                    }
                    break
            if not info and DEMO_FALLBACK_ENABLED:
                demo_record = get_demo_file_record(filename)
                if demo_record:
                    info = {
                        'name': filename,
                        'size': demo_record['size_bytes'],
                        'source': 'demo'
                    }
            
            if not info:
                return jsonify({'status': 'error', 'message': 'File not found'}), 404
        
        elapsed_time = time.time() - start_time
        
        return jsonify({
            'status': 'success',
            'file': info,
            'api_latency_ms': elapsed_time * 1000
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================
# DOWNLOAD ENDPOINTS
# ============================================

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Download file through API proxy
    Shows API overhead vs direct download
    """
    start_time = time.time()
    temp_file = f"/tmp/{filename}"
    
    try:
        # Download from cloud storage
        if provider == 'aws_s3':
            client.download_file(BUCKET, filename, temp_file)
        elif provider == 'supabase':
            try:
                response = client.storage.from_(BUCKET).download(filename)
                with open(temp_file, 'wb') as f:
                    f.write(response)
            except Exception:
                if not DEMO_FALLBACK_ENABLED:
                    raise
                demo_bytes = build_demo_file_bytes(filename)
                if not demo_bytes:
                    return jsonify({'status': 'error', 'message': 'File not found'}), 404
                with open(temp_file, 'wb') as f:
                    f.write(demo_bytes)
        
        download_time = time.time() - start_time
        file_size = os.path.getsize(temp_file)
        
        # Prepare response headers
        headers = {
            'X-Download-Time-Ms': str(download_time * 1000),
            'X-File-Size-Bytes': str(file_size)
        }
        
        # Send file
        response = send_file(
            temp_file,
            as_attachment=True,
            download_name=filename
        )
        
        # Add custom headers
        for key, value in headers.items():
            response.headers[key] = value
        
        # Cleanup after sending
        def cleanup(response):
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return response
        
        response.call_on_close(lambda: cleanup(response))
        
        return response
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/download-info/<filename>', methods=['GET'])
def download_info(filename):
    """
    Get download info without actual download
    Useful for measuring API overhead
    """
    start_time = time.time()
    
    try:
        if provider == 'aws_s3':
            response = client.head_object(Bucket=BUCKET, Key=filename)
            file_size = response['ContentLength']
        elif provider == 'supabase':
            response = client.storage.from_(BUCKET).list()
            file_size = 0
            for item in response:
                if item['name'] == filename:
                    file_size = item.get('metadata', {}).get('size', 0)
                    break

            if file_size == 0 and DEMO_FALLBACK_ENABLED:
                demo_record = get_demo_file_record(filename)
                if demo_record:
                    file_size = demo_record['size_bytes']
        
        elapsed_time = time.time() - start_time
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'size_bytes': file_size,
            'size_mb': file_size / (1024 * 1024),
            'api_latency_ms': elapsed_time * 1000,
            'estimated_download_time_s': file_size / (5 * 1024 * 1024)  # Assume 5 MB/s speed
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================
# UPLOAD ENDPOINTS
# ============================================

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload single file through API"""
    start_time = time.time()
    
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'Empty filename'}), 400
        
        # Save temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        # Upload to cloud
        if provider == 'aws_s3':
            client.upload_file(temp_path, BUCKET, file.filename)
        elif provider == 'supabase':
            with open(temp_path, 'rb') as f:
                client.storage.from_(BUCKET).upload(file.filename, f)
        
        elapsed_time = time.time() - start_time
        file_size = os.path.getsize(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        return jsonify({
            'status': 'success',
            'filename': file.filename,
            'size_bytes': file_size,
            'upload_time_ms': elapsed_time * 1000
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/upload-multiple', methods=['POST'])
def upload_multiple():
    """Upload multiple files in parallel through API"""
    start_time = time.time()
    results = []
    
    try:
        if 'files' not in request.files:
            return jsonify({'status': 'error', 'message': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        for file in files:
            file_start = time.time()
            temp_path = f"/tmp/{file.filename}"
            
            try:
                file.save(temp_path)
                
                if provider == 'aws_s3':
                    client.upload_file(temp_path, BUCKET, file.filename)
                elif provider == 'supabase':
                    with open(temp_path, 'rb') as f:
                        client.storage.from_(BUCKET).upload(file.filename, f)
                
                file_time = time.time() - file_start
                file_size = os.path.getsize(temp_path)
                os.remove(temp_path)
                
                results.append({
                    'filename': file.filename,
                    'status': 'success',
                    'size_bytes': file_size,
                    'upload_time_ms': file_time * 1000
                })
            
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': str(e)
                })
        
        elapsed_time = time.time() - start_time
        successful = sum(1 for r in results if r['status'] == 'success')
        
        return jsonify({
            'status': 'success',
            'total_files': len(files),
            'successful': successful,
            'total_time_ms': elapsed_time * 1000,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================
# PERFORMANCE MONITORING
# ============================================

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API performance statistics"""
    return jsonify({
        'status': 'success',
        'provider': provider,
        'bucket': BUCKET,
        'timestamp': datetime.now().isoformat()
    })


# ============================================
# ERROR HANDLING
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print(f"Starting API server...")
    print(f"Provider: {provider}")
    print(f"Bucket: {BUCKET}")
    print(f"Server: http://localhost:5000")
    print(f"Docs: http://localhost:5000/info")
    print(f"\nEndpoints:")
    print(f"  GET  /health              - Health check")
    print(f"  GET  /info                - API info")
    print(f"  GET  /files               - List files")
    print(f"  GET  /files/<filename>    - File metadata")
    print(f"  POST /upload              - Upload file")
    print(f"  POST /upload-multiple     - Upload multiple")
    print(f"  GET  /download/<filename> - Download file")
    print(f"  GET  /stats               - API stats")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
