import hashlib
import sys
import os

# CONFIGURATION
# The Key used for XOR encryption
XOR_KEY = b"RUST" 

# The Target PIN Hash (SHA-256 of "4921")
# The user must brute-force this
TARGET_HASH = "1b16f3933c066324a30ddb947c6b453e9a72df525164f849c7161b4028564c48"

FLAG = "CTF{crypto_god_sha256}"

def xor_encrypt(data, key):
    """Basic XOR encryption/decryption"""
    encrypted = bytearray()
    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])
    return bytes(encrypted)

def generate_challenge_files():
    """Generates the 'flag.enc' file for the user to find"""
    # The plaintext usually has a known header. 
    # Let's say it's a proprietary config format starting with "HEADER:"
    plaintext = f"HEADER:CONFIDENTIAL_DATA|{FLAG}".encode()
    
    encrypted_data = xor_encrypt(plaintext, XOR_KEY)
    
    with open("flag.enc", "wb") as f:
        f.write(encrypted_data)
    
    print("[*] Generated 'flag.enc'. This is the file users found.")

def check_pin(pin_input):
    """Verifies the PIN using SHA-256"""
    # 1. Encode string to bytes
    pin_bytes = pin_input.encode('utf-8')
    
    # 2. Hash it
    pin_hash = hashlib.sha256(pin_bytes).hexdigest()
    
    if pin_hash == TARGET_HASH:
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        generate_challenge_files()
        sys.exit(0)

    print("=== SECURE VAULT v1.0 ===")
    print("This vault is locked with SHA-256.")
    
    user_pin = input("Enter 4-digit PIN to unlock: ")
    
    if check_pin(user_pin):
        print("\n[+] ACCESS GRANTED.")
        print(f"[+] The Master Flag is: {FLAG}")
    else:
        print("\n[-] ACCESS DENIED.")
