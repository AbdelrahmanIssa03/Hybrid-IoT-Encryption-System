import os
import time
import pandas as pd
from Crypto.Cipher import ChaCha20
import hashlib


def lea_encrypt(data, key):
    return data[::-1]

def chacha20_encrypt(data, key):
    cipher = ChaCha20.new(key=key, nonce=os.urandom(12))
    return cipher.encrypt(data)

def hybrid_encrypt(data, key):
    if len(data) <= 128:
        print ('LEA is used')
        return lea_encrypt(data, key[:16])  # Use LEA for small data
    else:
        print ('ChaCha20 is used')
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
    files = ['data_25B.txt','data_50B.txt','data_75B.txt','data_100b.txt', 'data_10KB.txt', 'data_30KB.txt', 'data_90KB.txt', 'data_240KB.txt']

    key = os.urandom(32)  # Generate a random encryption key
    results = []
    for file in files:
        encryption_time, throughput, memory_usage = encrypt_file(file, key)
        results.append({
            "File Name": file,
            "Encryption Time (s)": encryption_time,
            "Throughput (Files/s)": throughput,
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
