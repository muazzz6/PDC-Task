"""
Generate sample text files for the lab task
Creates 15 sample files with varying sizes (100KB - 5MB)
"""

import os
import random
import string

def generate_sample_files(num_files=15, output_dir="sample_files"):
    """Generate sample files for testing"""
    os.makedirs(output_dir, exist_ok=True)
    
    file_sizes = [
        100 * 1024,      # 100KB
        250 * 1024,      # 250KB
        500 * 1024,      # 500KB
        1024 * 1024,     # 1MB
        2 * 1024 * 1024, # 2MB
        5 * 1024 * 1024  # 5MB
    ]
    
    print(f"Generating {num_files} sample files in '{output_dir}/'...")
    
    for i in range(1, num_files + 1):
        filename = f"sample_file_{i:02d}.txt"
        filepath = os.path.join(output_dir, filename)
        file_size = random.choice(file_sizes)
        
        # Generate random content
        content = ''.join(random.choices(string.ascii_letters + string.digits + '\n', k=file_size))
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        size_mb = file_size / (1024 * 1024)
        print(f"  ✓ Created {filename} ({size_mb:.2f} MB)")
    
    print(f"\n✅ Generated {num_files} sample files successfully!")
    return [f"sample_file_{i:02d}.txt" for i in range(1, num_files + 1)]

if __name__ == "__main__":
    generate_sample_files()
