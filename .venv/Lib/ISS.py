import os
import time
import pandas as pd
from Cryptodome.Cipher import ChaCha20
import hashlib

def lea_encrypt(data, key):
    return data[::-1]

def chacha20_encrypt(data, key):
    cipher = ChaCha20.new(key=key, nonce=os.urandom(12))
    return cipher.encrypt(data)

def hybrid_encrypt(data, key):
    if len(data) <= 128:
        return lea_encrypt(data, key[:16])  # Use LEA for small data
    else:
        return chacha20_encrypt(data, key)  # Use ChaCha20 for large data

def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()

    start_time = time.time()  # Start timer
    encrypted_data = hybrid_encrypt(data, key)  # Encrypt data
    end_time = time.time()  # End timer

    encryption_time = end_time - start_time  # Time in seconds
    throughput = 1 / encryption_time  # Throughput in KB/s
    memory_usage = len(encrypted_data) / (1024 * 1024)  # Memory usage in MB

    return encryption_time, throughput, memory_usage



def process_files():
    sizes_kb = [10, 30, 90, 240]

    key = os.urandom(32)  # Generate a random encryption key

    results = []

    for size in sizes_kb:
        file_path = f"data_{size}KB.txt"
        encryption_time, throughput, memory_usage = encrypt_file(file_path, key)
        results.append({
            "File Size (KB)": size,
            "Encryption Time (s)": encryption_time,
            "Throughput (KB/s)": throughput,
            "Memory Usage (MB)": memory_usage,
        })

    results_df = pd.DataFrame(results)
    print("Encryption Metrics:")
    print(results_df)

    output_file = "encryption_metrics.csv"
    results_df.to_csv(output_file, index=False)
    print(f"Metrics saved to {output_file}")

if __name__ == "__main__":
    process_files()
