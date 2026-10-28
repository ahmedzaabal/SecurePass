# SecurePass - Cross-Platform Password Manager

A secure, offline-first password manager built with Python and PyQt6. All data is encrypted locally using AES-256-GCM with keys derived from your master password via Argon2id.

## Features

- **End-to-end encryption**: Vault encrypted with AES-256-GCM, master key derived with Argon2id
- **Offline-first**: All data stored locally, no cloud sync
- **Cross-platform**: Works on Linux (Zorin/Debian), Windows, and macOS
- **Password generator**: Create strong, customizable passwords
- **Secure clipboard**: Auto-clear copied passwords after timeout
- **Auto-lock**: Lock vault after inactivity
- **Search & organize**: Quickly find entries by name, URL, or username
- **Encrypted backups**: Export/import encrypted vault files

## Security Design

- Master password never stored to disk
- Encryption key derived using Argon2id with high memory/time cost
- Each vault file uses unique nonce for AES-GCM
- All sensitive data only held in memory while unlocked
- Clipboard cleared automatically after copying

## Installation

### Prerequisites
- Python 3.10 or higher

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the application
```bash
python main.py
```

## First Use

1. Launch the app - you'll be prompted to create a master password
2. Choose a strong, unique master password (this cannot be recovered if lost!)
3. Start adding your passwords

## Building Executables

See [docs/BUILDING.md](docs/BUILDING.md) for instructions on building standalone executables for each platform.

## Project Structure

```
Password_manager/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── core/           # Crypto, vault, and database logic
│   ├── ui/             # PyQt6 user interface
│   └── utils/          # Helper utilities
├── assets/             # Icons and resources
├── config/             # Configuration files
└── docs/               # Documentation
```

## Warning

**Your master password is the only way to decrypt your vault. If you forget it, your data cannot be recovered.** Store it securely.

## License

MIT License - see LICENSE file for details
