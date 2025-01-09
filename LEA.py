import os
import time
import pandas as pd
from Crypto.Cipher import ChaCha20
import hashlib

# LEA Parameters
BLOCK_SIZE = 16  # LEA block size is 128 bits
ROUND_KEYS = 24  # Number of rounds for LEA-128

def generate_lea_round_keys(key):
    """
    Generates round keys for LEA.
    Key size is 128 bits (16 bytes).
    """
    assert len(key) == BLOCK_SIZE, "LEA key must be 128 bits"
    keys = []
    for i in range(ROUND_KEYS):
        # Simple round key generation (example only, replace with real LEA logic)
        keys.append(key[i % len(key):] + key[:i % len(key)])
    return keys

def lea_encrypt_block(block, round_keys):
    """
    Encrypts a single block using LEA.
    """
    assert len(block) == BLOCK_SIZE, "LEA block must be 128 bits"
    encrypted_block = block
    for key in round_keys:
        # Example transformation (replace with actual LEA encryption logic)
        encrypted_block = bytes(b ^ k for b, k in zip(encrypted_block, key))
    return encrypted_block

def lea_encrypt(data, key):
    """
    Encrypts data using the LEA cipher in ECB mode.
    """
    round_keys = generate_lea_round_keys(key)
    encrypted_data = b""
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:  # Padding if necessary
            block = block.ljust(BLOCK_SIZE, b'\0')
        encrypted_data += lea_encrypt_block(block, round_keys)
    return encrypted_data
