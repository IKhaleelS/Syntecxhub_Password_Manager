# Syntecxhub Password Manager

Lightweight, local command-line password manager that encrypts credentials
with Fernet and protects access using a master password.

---

## Features

- Master password authentication with setup and confirmation on first run
- Encrypted vault using Fernet (symmetric AES-based encryption)
- Add, view, delete, and list stored credentials
- Strong password enforcement (min 8 chars, upper, lower, digit, special)
- Secure random password generator
- Brute-force protection (locks after 3 failed login attempts)

---

## Requirements

- Python 3.8+
- Python packages: `cryptography`, `colorama`

Install dependencies:

```bash
pip install cryptography colorama
```

---

## Run

From the project directory run:

```bash
python manager.py
```

On first run you will be prompted to create and confirm a master password. The
master password must meet the strength rules enforced by the program.

---

## Usage (menu)

1. Add password — save a credential (`service`, `username`, `password`)
2. View password — display stored username and password for a service
3. Delete password — remove a service from the vault
4. List services — show saved service names
5. Generate strong password — create a secure random password
6. Exit — encrypt and save the vault to disk

Notes:
- Passwords are validated for strength when added.
- The vault is kept in memory while the program runs and encrypted to disk
  on exit.

---

## Security details

- Master password is hashed with SHA-256 and stored in `master.hash`.
- The derived key (SHA-256 digest, base64-url-encoded) is used with Fernet to
  encrypt/decrypt the vault file `vault.enc`.
- The program locks after `MAX_ATTEMPTS` failed master-password attempts.

---

## Files

- `manager.py` — main application
- `vault.enc` — encrypted password vault (created on first save)
- `master.hash` — hashed master password (created on first run)

---

## Notes

This tool is intended for local, educational use. Keep your `master.hash` and
`vault.enc` files secure and back them up if you need persistent access.

---

## Author

Ibrahim Shafiu — Internship Project, 2026