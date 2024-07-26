from Crypto.Cipher import AES
import binascii
import time

def encrypt(plaintext, key, iv):
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    return cipher.encrypt(plaintext)

def brute_force(ciphertext, iv, plaintext):
    keys = []
    with open("keys.txt", "r") as f:
        keys = [key.strip() for key in f.readlines()]
    keys_tested = 0
    failed_attempts = 0

    for key in keys:
        keys_tested += 1
        key_bytes = bytearray.fromhex(key)
        encrypted = encrypt(plaintext, key_bytes, iv)
        if encrypted == ciphertext:
            print(f"Key found after testing {keys_tested} keys.")
            return key
        else:
            failed_attempts += 1
            if failed_attempts % 500 == 0:  # Print progress every 100 failed attempts
                print(f"Progress: {keys_tested}/{len(keys)} keys tested, {failed_attempts} failed attempts.")
    print("Key not found.")
    return None

# Values
plaintext_hex = "255044462d312e350a25d0d4c5d80a34"
ciphertext_hex = "d06bf9d0dab8e8ef880660d2af65aa82"
iv_hex = "09080706050403020100A2B2C2D2E2F2"

plaintext = bytearray.fromhex(plaintext_hex)
ciphertext = bytearray.fromhex(ciphertext_hex)
iv = bytearray.fromhex(iv_hex)

key = brute_force(ciphertext, iv, plaintext)
if key:
    print("Key found:", key)
else:
    print("Key not found.")
