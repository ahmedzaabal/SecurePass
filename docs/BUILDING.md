# Building Executables

This guide will help you build standalone executables for Windows, macOS, and Linux.

## Prerequisites

Install all dependencies first:
```bash
pip install -r requirements.txt
```

## Linux (Zorin OS/Debian)

### Using PyInstaller
```bash
pyinstaller --name SecurePass \
            --windowed \
            --onefile \
            --add-data "src:src" \
            main.py
```

The executable will be in `dist/SecurePass`

### Creating a .deb package (optional)
```bash
# Install fpm
sudo gem install fpm

# Create package
fpm -s dir -t deb -n securepass -v 1.0.0 \
    --prefix /opt/securepass \
    dist/SecurePass=/opt/securepass/ \
    --after-install scripts/postinst \
    --before-remove scripts/prerm
```

## Windows

### On Windows
```bash
pyinstaller --name SecurePass ^
            --windowed ^
            --onefile ^
            --icon=assets/icon.ico ^
            --add-data "src;src" ^
            main.py
```

The executable will be in `dist\SecurePass.exe`

## macOS

### On macOS
```bash
pyinstaller --name SecurePass \
            --windowed \
            --onefile \
            --icon=assets/icon.icns \
            --add-data "src:src" \
            main.py
```

For a proper .app bundle:
```bash
pyinstaller --name SecurePass \
            --windowed \
            --onedir \
            --icon=assets/icon.icns \
            --add-data "src:src" \
            main.py
```

Then create a DMG using `create-dmg` or Disk Utility.

## Tips

- For better compatibility, build on the target platform
- Test the executable before distributing
- The vault is stored in platform-specific locations as noted in the code
