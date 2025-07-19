import requests
from colorama import Fore, Style
requests.packages.urllib3.disable_warnings()


# List header keamanan yang kita cek
SECURITY_HEADERS = {
    "Strict-Transport-Security": "Melindungi terhadap downgrade attack",
    "Content-Security-Policy": "Mencegah XSS dan data injection",
    "X-Content-Type-Options": "Mencegah MIME sniffing",
    "X-Frame-Options": "Melindungi dari clickjacking",
    "Referrer-Policy": "Kontrol info referrer",
    "Permissions-Policy": "Kontrol API yang bisa diakses"
}

def scan_headers(url):
    result = []
    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers

        for header, desc in SECURITY_HEADERS.items():
            if header in headers:
                print(f"{Fore.GREEN}[+] {header}: {headers[header]} ✅")
            else:
                print(f"{Fore.RED}[-] {header} not set ❌ → {desc}")
                result.append({
                    "type": "missing-header",
                    "header": header,
                    "description": desc,
                    "url": url,
                    "severity": "low"
                })
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Request error: {e}{Style.RESET_ALL}")
    print(Style.RESET_ALL, end="")
    return result

