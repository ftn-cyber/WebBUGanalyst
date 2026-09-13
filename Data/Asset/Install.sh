#!/bin/bash
# WebBUGanalyst Installer — Fixed for interactive input
# Supports: curl | sh → will auto-fallback to local exec if needed

set -e

URL_PY="https://raw.githubusercontent.com/ftn-cyber/WebBUGanalyst/refs/heads/main/Data/Asset/Python%20file/WebBUGanalyst.py"
TMP="/tmp/WebBUGanalyst.py"

echo "[*] WebBUGanalyst v1.0 — Bug Bounty Helper"
echo "[*] Mengunduh skrip..."

# Unduh
if command -v curl >/dev/null 2>&1; then
    curl -sSfL "$URL_PY" -o "$TMP" || { echo "[-] curl gagal"; exit 1; }
elif command -v wget >/dev/null 2>&1; then
    wget -q "$URL_PY" -O "$TMP" || { echo "[-] wget gagal"; exit 1; }
else
    echo "[-] curl/wget tidak tersedia"
    exit 1
fi

[ -s "$TMP" ] || { echo "[-] File kosong/tidak ditemukan"; rm -f "$TMP"; exit 1; }

# Coba jalankan di TTY nyata
if [ -t 0 ] || command -v script >/dev/null 2>&1; then
    # Jika di terminal langsung atau script tersedia
    if command -v script >/dev/null 2>&1; then
        script -qec "python3 '$TMP' 2>/dev/null || python '$TMP'" /dev/null
    else
        python3 "$TMP" 2>/dev/null || python "$TMP"
    fi
else
    # Jika di pipe (curl | bash), beri petunjuk
    echo ""
    echo "[!] Jalankan secara lokal untuk interaksi:"
    echo "    curl -fsSL $0 > install.sh && chmod +x install.sh && ./install.sh"
    rm -f "$TMP"
    exit 1
fi

rm -f "$TMP" 2>/dev/null
