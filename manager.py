import json
import os
import secrets
import string
import hashlib
import sys
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from colorama import Fore, Style, init

init()

VAULT_FILE = "vault.enc"
MASTER_FILE = "master.hash"
MAX_ATTEMPTS = 3

# ---------- Color Helpers ----------
def success(msg):
    print(Fore.GREEN + msg + Style.RESET_ALL)

def error(msg):
    print(Fore.RED + msg + Style.RESET_ALL)

def info(msg):
    print(Fore.CYAN + msg + Style.RESET_ALL)

# ---------- Key Generation ----------
def generate_key(master_password):
    hashed = hashlib.sha256(master_password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hashed))

# ---------- Master Password ----------
def load_master():
    if not os.path.exists(MASTER_FILE):
        info("First time setup")
        while True:
            master = getpass("Create master password: ")
            confirm = getpass("Confirm master password: ")
            if master != confirm:
                error("Passwords do not match. Try again.")
                continue
            if not check_strength(master):
                error("Master password too weak! Use 8+ chars, upper, lower, number & symbol.")
                continue
            hashed = hashlib.sha256(master.encode()).hexdigest()
            with open(MASTER_FILE, "w") as f:
                f.write(hashed)
            success("Master password set successfully.")
            return master
    else:
        attempts = 0
        with open(MASTER_FILE) as f:
            stored = f.read().strip()
        while attempts < MAX_ATTEMPTS:
            master = getpass("Enter master password: ")
            hashed = hashlib.sha256(master.encode()).hexdigest()
            if hashed == stored:
                success("Login successful.")
                return master
            attempts += 1
            error(f"Incorrect password ({attempts}/{MAX_ATTEMPTS})")
        error("Too many attempts. Account locked.")
        sys.exit(1)

# ---------- Vault Handling ----------
def load_vault(fernet):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted.decode())

def save_vault(fernet, data):
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

# ---------- Core Functions ----------
def add_password(vault):
    service = input("Service name: ")
    username = input("Username: ")
    password = getpass("Password: ")
    if not check_strength(password):
        error("Weak password! Use 8+ chars, upper, lower, number & symbol.")
        return
    vault[service] = {"username": username, "password": password}
    success("Password saved.")

def view_password(vault):
    service = input("Service name: ")
    if service in vault:
        success("Username: " + vault[service]["username"])
        success("Password: " + vault[service]["password"])
    else:
        error("Service not found.")

def delete_password(vault):
    service = input("Service name: ")
    if service in vault:
        del vault[service]
        success("Deleted successfully.")
    else:
        error("Service not found.")

def check_strength(password):
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_digit and has_special

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


# ---------- Main ----------
def main():
    info("=== WELCOME TO SYNTECXHUB PASSWORD MANAGER ===")
    master = load_master()
    fernet = generate_key(master)
    vault = load_vault(fernet)

    while True:
        info("\n--- Menu ---")
        print("1. Add password")
        print("2. View password")
        print("3. Delete password")
        print("4. List services")
        print("5. Generate strong password")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_password(vault)
        elif choice == "2":
            view_password(vault)
        elif choice == "3":
            delete_password(vault)
        elif choice == "4":
            success("Services: " + ", ".join(vault.keys()))
        elif choice == "5":
            pwd = generate_password()
            success("Generated Password: " + pwd)
        elif choice == "6":
            save_vault(fernet, vault)
            success("Vault encrypted and Saved. Goodbye.")
            break
        else:
            error("Invalid option.")

if __name__ == "__main__":
    main()
