#!/bin/bash

# WebBUGanalyst Installer
# One-liner: curl -fsSL https://raw.githubusercontent.com/ftn-cyber/WebBUGanalyst/main/install-webbug.sh | bash
#             or wget -qO- https://raw.githubusercontent.com/ftn-cyber/WebBUGanalyst/main/install-webbug.sh | bash

set -e

PYTHON_URL="https://raw.githubusercontent.com/ftn-cyber/WebBUGanalyst/refs/heads/main/Data/Asset/Python%20file/WebBUGanalyst.py"
TEMP_SCRIPT="/tmp/WebBUGanalyst.py"

echo "[*] Mengunduh WebBUGanalyst dari GitHub..."

# Unduh file Python
if command -v curl >/dev/null 2>&1; then
    curl -sSfL "$PYTHON_URL" -o "$TEMP_SCRIPT"
elif command -v wget >/dev/null 2>&1; then
    wget -q --no-check-certificate "$PYTHON_URL" -O "$TEMP_SCRIPT"
else
    echo "[-] Diperlukan curl atau wget untuk mengunduh."
    exit 1
fi

# Verifikasi file berhasil diunduh
if [ ! -s "$TEMP_SCRIPT" ]; then
    echo "[-] Gagal mengunduh file Python. Periksa koneksi atau URL."
    rm -f "$TEMP_SCRIPT"
    exit 1
fi

echo "[+] File berhasil diunduh. Menjalankan..."

# Jalankan dengan python3 (prioritas) atau python
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$TEMP_SCRIPT"
elif command -v python >/dev/null 2>&1; then
    exec python "$TEMP_SCRIPT"
else
    echo "[-] Python tidak ditemukan. Instal python3 terlebih dahulu."
    rm -f "$TEMP_SCRIPT"
    exit 1
fi
