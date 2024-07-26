import sqlite3
import hashlib
import time
import os
import random
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

console.print(Markdown("""
# Cyber Security Simulation: John The Ripper

In this simulation, we'll explore how hackers can crack passwords using different methods. 
We'll set up user accounts with weak passwords, hash them using various algorithms, and then attempt to crack these hashes using a dictionary attack.
Let's dive into the world of cybersecurity and see how secure (or insecure) our passwords are!

## Group Members:
- Sifan Fira
- Salman Ali
- Obsu Kebede
- Fethiya Safi
- Abdulmunim Jundurahman
"""))
time.sleep(5)

# Step 1: Setting up the database
console.print("[bold green]Setting up the database...[/bold green]")
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    md5_hash TEXT,
    sha1_hash TEXT,
    sha256_hash TEXT
)
''')

def create_user(username, password):
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
    INSERT INTO users (username, password, md5_hash, sha1_hash, sha256_hash)
    VALUES (?, ?, ?, ?, ?)
    ''', (username, password, md5_hash, sha1_hash, sha256_hash))
    
    conn.commit()

def crack_hashes(wordlist):
    cursor.execute('SELECT username, md5_hash, sha1_hash, sha256_hash FROM users')
    users = cursor.fetchall()
    
    cracked_passwords = {}
    
    for user in users:
        username, md5_hash, sha1_hash, sha256_hash = user
        for word in wordlist:
            word_hash_md5 = hashlib.md5(word.encode()).hexdigest()
            word_hash_sha1 = hashlib.sha1(word.encode()).hexdigest()
            word_hash_sha256 = hashlib.sha256(word.encode()).hexdigest()
            
            if word_hash_md5 == md5_hash:
                cracked_passwords[(username, 'md5')] = word
            if word_hash_sha1 == sha1_hash:
                cracked_passwords[(username, 'sha1')] = word
            if word_hash_sha256 == sha256_hash:
                cracked_passwords[(username, 'sha256')] = word
    
    return cracked_passwords

# Explanation
console.print(Markdown("""
## Explanation of Each Step:

1. **Setting up the database**: 
   We create a SQLite database with a table for storing user information, including username, password, and hashed passwords using MD5, SHA1, and SHA256.

2. **Creating users with weak passwords**:
   We add several users to the database with commonly used weak passwords. Each password is hashed before storing.

3. **Obtaining the database**:
   We retrieve the list of users and their hashed passwords from the database. This simulates an attacker gaining access to the password database.

4. **Performing a dictionary attack**:
   We use a dictionary attack to crack the passwords. This involves hashing common passwords from a wordlist and comparing the result to the stored hashes.

5. **Presenting the cracked passwords**:
   We display the results of the dictionary attack, showing which passwords were successfully cracked.

Through this simulation, we demonstrate the importance of using strong, unique passwords.
"""))

time.sleep(5)
# Step 2: Creating users with weak passwords
console.print("[bold green]Creating user accounts with weak passwords...[/bold green]")
create_user('alice', 'password')
create_user('bob', '123456')
create_user('carol', 'qwerty')
create_user('dave', 'abc123')
create_user('eve', 'letmein')
create_user('frank', 'monkey')
time.sleep(3)

# Step 3: Simulating the process of obtaining the database
console.print("[bold green]Obtaining the database with user list and hashed passwords...[/bold green]")
cursor.execute('SELECT username, md5_hash, sha1_hash, sha256_hash FROM users')
users = cursor.fetchall()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Username")
table.add_column("MD5 Hash")
table.add_column("SHA1 Hash")
table.add_column("SHA256 Hash")

for user in users:
    username, md5_hash, sha1_hash, sha256_hash = user
    table.add_row(username, md5_hash, sha1_hash, sha256_hash)

console.print(table)
time.sleep(3)

# Step 4: Performing a dictionary attack
console.print("[bold green]Performing dictionary attack to crack the passwords...[/bold green]")
# Enhanced wordlist for more realistic attack
wordlist = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'monkey', 'dragon', '111111', 'baseball', 'iloveyou', 'trustno1']
for _ in track(range(100), description="Cracking hashes..."):
    time.sleep(0.1)
cracked_passwords = crack_hashes(wordlist)

# Step 5: Presenting the cracked passwords
console.print("[bold green]Cracking completed. Presenting the results:[/bold green]")
results_table = Table(show_header=True, header_style="bold magenta")
results_table.add_column("Username")
results_table.add_column("Hash Type")
results_table.add_column("Cracked Password")

for (username, hash_type), password in cracked_passwords.items():
    results_table.add_row(username, hash_type, password)

console.print(results_table)

# Closing the database connection
conn.close()
