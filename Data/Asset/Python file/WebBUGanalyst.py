#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Bug Bounty Helper - nexmo
Author: 0xriki AI
Purpose: Interactive web vulnerability reconnaissance tool.
"""

import requests
import socket
from urllib.parse import urljoin, urlparse
import threading
from queue import Queue

# ASCII Art Banner - "nexmo"
BANNER = r"""███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ╚██╗ ██╔╝█████╗  
██║╚██╗██║██╔══╝   ██╔██╗  ╚████╔╝ ██╔══╝  
██║ ╚████║███████╗██╔╝ ██╗  ╚██╔╝  ███████╗
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""

def print_banner():
    print(BANNER)
    print("=" * 60)

def get_target_url():
    while True:
        url = input("\n[>] Masukkan link target (contoh: https://example.com): ").strip()
        if not url:
            print("[-] URL tidak boleh kosong!")
            continue
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        try:
            # Validasi dasar: coba parse dan resolve host
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL")
            socket.gethostbyname(parsed.netloc)
            return url
        except socket.gaierror:
            print(f"[-] Gagal menghubungi host: {parsed.netloc}. Pastikan domain valid dan terjangkau.")
        except Exception as e:
            print(f"[-] Format URL tidak valid: {e}")

def check_security_headers(url):
    try:
        resp = requests.get(url, timeout=10)
        headers = resp.headers
        missing = []
        required = {
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'Strict-Transport-Security': 'HSTS',
            'Referrer-Policy': 'Referrer control'
        }
        for h in required:
            if h not in headers:
                missing.append(f"{h} ({required[h]})")
        return missing
    except Exception as e:
        return [f"Error fetching headers: {str(e)}"]

def test_basic_sqli(url):
    payloads = ["'", "\"", "1' OR '1'='1", "admin'--"]
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    if not parsed.query:
        return []
        
    try:
        params = dict([p.split('=', 1) for p in parsed.query.split('&')])
    except ValueError:
        return []

    vulnerable = []
    for param in params:
        original_val = params[param]
        for payload in payloads:
            test_params = params.copy()
            test_params[param] = payload
            test_url = base + '?' + '&'.join([f"{k}={v}" for k, v in test_params.items()])
            try:
                resp = requests.get(test_url, timeout=5)
                if any(err in resp.text.lower() for err in ['sql syntax', 'mysql', 'sqlite', 'postgres', 'odbc', 'unclosed quotation mark']):
                    vulnerable.append(f"Possible SQLi at {param} with payload: {payload}")
                    break
            except:
                continue
        params[param] = original_val
    return vulnerable

def enumerate_directories(url, wordlist="common.txt"):
    found = []
    q = Queue()
    
    def worker():
        while not q.empty():
            path = q.get()
            test_url = urljoin(url, path.strip())
            try:
                resp = requests.get(test_url, timeout=5)
                if resp.status_code == 200:
                    found.append(test_url)
                    print(f"[+] Found: {test_url}")
            except:
                pass
            q.task_done()

    try:
        with open(wordlist, 'r') as f:
            paths = f.readlines()
    except FileNotFoundError:
        print(f"[-] Wordlist '{wordlist}' tidak ditemukan. Lewati enumerasi direktori.")
        return []

    for path in paths[:100]:
        stripped = path.strip()
        if stripped and not stripped.startswith('#'):
            q.put(stripped)

    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()
    return found

def resolve_subdomains(domain):
    subs = ['www', 'dev', 'staging', 'test', 'api', 'admin', 'mail', 'ftp']
    found = []
    for sub in subs:
        try:
            full_domain = f"{sub}.{domain}"
            socket.gethostbyname(full_domain)
            found.append(full_domain)
        except socket.gaierror:
            pass
    return found

def main():
    print_banner()
    
    # Tunda eksekusi hingga user masukkan target
    target_url = get_target_url()
    
    domain = urlparse(target_url).netloc
    
    print(f"\n[+] Target: {target_url}")
    
    # Security Headers Check
    print("\n[+] Memeriksa Header Keamanan...")
    missing_headers = check_security_headers(target_url)
    if missing_headers:
        for h in missing_headers:
            print(f"[-] Missing: {h}")
    
    # Basic SQLi Test (only if URL has parameters)
    if '?' in target_url:
        print("\n[+] Mengujicoba SQL Injection Dasar...")
        sqli_issues = test_basic_sqli(target_url)
        if sqli_issues:
            for issue in sqli_issues:
                print(f"[!] {issue}")
    
    # Directory Enumeration (limited scope)
    print("\n[+] Enumerasi Direktori (maks. 100 path)...")
    dirs_found = enumerate_directories(target_url)
    if not dirs_found and wordlist_exists("common.txt"):
        print("[-] Tidak ada direktori sensitif ditemukan.")
    
    # Subdomain Discovery
    print("\n[+] Mencari Subdomain Umum...")
    subs_found = resolve_subdomains(domain)
    for sub in subs_found:
        print(f"[+] Ditemukan subdomain: http://{sub}")

def wordlist_exists(filename):
    try :
        with open(filename): pass 
        return True 
    except FileNotFoundError : 
        return False 

if __name__ == "__main__":
    main()
