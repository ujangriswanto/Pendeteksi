import requests
from urllib.parse import urljoin
from tqdm import tqdm
from colorama import Fore, Style

# Matikan warning HTTPS (self-signed, dll)
requests.packages.urllib3.disable_warnings()

def scan_dirs(base_url, wordlist_path):
    try:
        with open(wordlist_path, "r") as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist not found: {wordlist_path}{Style.RESET_ALL}")
        return

    found = []
    result = []

    for path in tqdm(paths, desc="  Scanning paths", ncols=70):
        full_url = urljoin(base_url, path)
        try:
            response = requests.get(full_url, timeout=5, verify=False, allow_redirects=False)
            status = response.status_code
            if status in [200, 301, 403]:
                print(f"{Fore.GREEN}[+] Found: {full_url} (Status: {status})")
                found.append((full_url, status))
                result.append({
                    "type": "directory-found",
                    "path": path,
                    "url": full_url,
                    "status": status
                })
        except requests.RequestException:
            pass

    if not found:
        print(f"{Fore.YELLOW}[!] No interesting directories found.{Style.RESET_ALL}")
    else:
        print(Style.RESET_ALL, end="")

    return result
