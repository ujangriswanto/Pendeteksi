# 🛡️ Pendeteksi

Tool vulnerability scanner berbasis Python, terinspirasi dari Nuclei dan Nikto. Cocok untuk pentester, devsecops, dan auditor internal.

## 🔧 Fitur
- Template-based scanning (YAML)
- Detection: LFI, RCE, SSTI, SSRF, XSS, dll
- Output JSON
- Multithreaded

## 🚀 Cara Install

```bash
git clone https://github.com/ujangriswanto/uvulnscan
cd uvulnscan
pip install -r requirements.txt
python scanner.py -u https://target.com -t templates/
```

Credits
Dibuat oleh Ujang Riswanto 👑
