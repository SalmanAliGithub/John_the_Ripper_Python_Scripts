from Crypto.Cipher import AES
import binascii
import time

def encrypt(plaintext, key, iv):
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    return cipher.encrypt(plaintext)

# Values
plaintext_hex = "255044462d312e350a25d0d4c5d80a34"
ciphertext_hex = "d06bf9d0dab8e8ef880660d2af65aa82"
iv_hex = "09080706050403020100A2B2C2D2E2F2"
key = "95fa2030e73ed3f8da761b4eb805dfd7" # Key found by key_cracker.py

plaintext = bytearray.fromhex(plaintext_hex)
ciphertext = bytearray.fromhex(ciphertext_hex)
iv = bytearray.fromhex(iv_hex)
key = bytearray.fromhex(key)

print("VERIFICATION")
cipher = encrypt(plaintext, key, iv)
print("Ciphertext:", binascii.hexlify(cipher).decode())
print("Expected:", ciphertext_hex)