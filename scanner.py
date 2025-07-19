import argparse
import os
import json
from modules import headers, dirscan, template_engine

def main():
    parser = argparse.ArgumentParser(description="🛡️ Pendeteksi – Scan tool ala Tuanku Ujang Riswanto")
    parser.add_argument("-u", "--url", help="Target URL (e.g. https://example.com)", required=True)
    parser.add_argument("-t", "--templates", help="Path to templates folder", required=True)
    parser.add_argument("-w", "--wordlist", help="Wordlist for directory scan (optional)", default="wordlists/common.txt")
    parser.add_argument("-o", "--output", help="Output file (JSON)", default=None)

    args = parser.parse_args()
    target = args.url
    results = []

    print(f"\n📡 Scanning target: {target}\n")

    # Header Scanner
    print("[*] Checking security headers...")
    results += headers.scan_headers(target)

    # Directory Bruteforce
    print("[*] Bruteforce sensitive directories...")
    results += dirscan.scan_dirs(target, args.wordlist)

    # Template Engine
    print("[*] Running template-based scan...")
    template_results = template_engine.run_templates(target, args.templates)
    if template_results:
        results += template_results

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Hasil scan disimpan di: {args.output}")

    print("\n✅ Scan completed.\n")

    try:
        results += template_engine.run_templates(target, args.templates)
    except Exception as e:
        print(f"{Fore.RED}[!] Template scan error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
