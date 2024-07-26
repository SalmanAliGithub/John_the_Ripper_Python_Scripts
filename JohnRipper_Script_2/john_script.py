import hashlib
import binascii
import argparse
from passlib.hash import nthash

def load_hashes(hash_file):
    with open(hash_file, 'r') as f:
        return {line.strip() for line in f}

def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f]

def crack_md5(hashes, wordlist):
    cracked = {}
    for word in wordlist:
        hashed_word = hashlib.md5(word.encode('utf-8')).hexdigest()
        if hashed_word in hashes:
            cracked[hashed_word] = word
    return cracked

def crack_sha1(hashes, wordlist):
    cracked = {}
    for word in wordlist:
        hashed_word = hashlib.sha1(word.encode('utf-8')).hexdigest()
        if hashed_word in hashes:
            cracked[hashed_word] = word
    return cracked

def crack_ntlm(hashes, wordlist):
    cracked = {}
    for word in wordlist:
        hashed_word = nthash.hash(word)
        if hashed_word in hashes:
            cracked[hashed_word] = word
    return cracked

def write_to_potfile(cracked_hashes, potfile):
    with open(potfile, 'a') as f:
        for hash_val, plaintext in cracked_hashes.items():
            f.write(f"{hash_val}:{plaintext}\n")

def main(hash_file, wordlist_file, hash_type, potfile):
    hashes = load_hashes(hash_file)
    wordlist = load_wordlist(wordlist_file)

    if hash_type == 'md5':
        cracked_hashes = crack_md5(hashes, wordlist)
    elif hash_type == 'sha1':
        cracked_hashes = crack_sha1(hashes, wordlist)
    elif hash_type == 'ntlm':
        cracked_hashes = crack_ntlm(hashes, wordlist)
    else:
        print(f"Unsupported hash type: {hash_type}")
        return

    if cracked_hashes:
        print("Cracked hashes:")
        for hash_val, plaintext in cracked_hashes.items():
            print(f"{hash_val}: {plaintext}")
        write_to_potfile(cracked_hashes, potfile)
    else:
        print("No hashes were cracked.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crack hashes using a wordlist.")
    parser.add_argument('hash_file', help="File containing hashes to crack.")
    parser.add_argument('wordlist_file', help="File containing wordlist.")
    parser.add_argument('hash_type', help="Type of hash (md5, sha1, ntlm).")
    parser.add_argument('--potfile', default='John.pot', help="File to store cracked hashes (default: John.pot)")

    args = parser.parse_args()
    main(args.hash_file, args.wordlist_file, args.hash_type, args.potfile)
