# DPassGen - Secure Password Generator CLI

A premium, cyberpunk-themed password generator for terminal.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS%20%7C%20WSL-orange.svg)

## Features

- 🔐 **Secure Password Generation** - Generate cryptographically secure passwords
- 📦 **Bulk Password Generator** - Generate multiple passwords at once
- 💪 **Password Strength Checker** - Check password strength and security
- 🔎 **Password Analyzer** - Analyze password for vulnerabilities
- 📝 **Passphrase Generator** - Generate memorable passphrases
- 🔑 **Hash Generator** - Generate cryptographic hashes (MD5, SHA1, SHA256, SHA384, SHA512)
- ⚙ **Configurable Settings** - Customize default options
- 🎨 **Cyberpunk Theme UI** - Beautiful, modern terminal interface

## Requirements

- Python 3.7+
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/dikaoffic-z/DPassGen.git
cd DPassGen

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Interactive Mode

```bash
python main.py
```

### Command Line Mode

```bash
# Generate a password
python main.py --generate --length 24

# Check password strength
python main.py --strength "YourPassword123!"

# Generate hash
python main.py --hash "YourText" --type sha256

# Generate passphrase
python main.py --passphrase --words 5
```

## Options

- `--generate, -g` - Generate a single password
- `--length, -l` - Password length (default: 16)
- `--strength, -s` - Check password strength
- `--hash` - Generate hash of text
- `--type` - Hash type (md5, sha1, sha256, sha384, sha512)
- `--passphrase, -p` - Generate a passphrase
- `--words, -w` - Number of words for passphrase
- `--version, -v` - Show version

## Security

DPassGen uses Python's `secrets` module for cryptographic security:

- Uses `secrets.choice()` for secure character selection
- Uses `secrets.token_bytes()` for secure random bytes
- Uses `os.urandom()` for additional entropy
- No password storage - all passwords exist only in memory
- Does NOT use `random` module for security-critical operations

## Supported Platforms

- 📱 Termux (Android)
- 🐧 Linux
- 🪟 Ubuntu / Debian / Arch / Alpine
- 💻 WSL (Windows Subsystem for Linux)
- 🍎 macOS
- ☁️ VPS

## Project Structure

```
DPassGen/
├── main.py              # Main application entry point
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── core/
│   ├── generator.py     # Password generator
│   ├── analyzer.py      # Password analyzer
│   └── security.py      # Security utilities
├── modules/
│   ├── password.py      # Password module
│   ├── bulk.py          # Bulk generator module
│   ├── passphrase.py    # Passphrase module
│   └── hash.py          # Hash module
├── ui/
│   ├── banner.py        # ASCII banners
│   ├── menu.py          # Interactive menu
│   └── theme.py         # Cyberpunk theme
└── utils/
    └── helper.py        # Helper utilities
```

## License

MIT License

## Developer

**DIKA OFFICIAL**

### Connect With Us

📱 **WhatsApp**: [Chat Now](https://wa.me/6281234567890)

🎵 **TikTok**: [@dikaofficial](https://tiktok.com/@dikaofficial)

📸 **Instagram**: [@dikaofficial](https://instagram.com/dikaofficial)

---

⚠️ **Disclaimer**: This tool is for educational and legitimate security purposes only. Always follow security best practices and applicable laws in your jurisdiction.
