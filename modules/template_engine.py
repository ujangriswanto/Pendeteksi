import os
import yaml
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings()

def run_templates(base_url, template_dir):
    all_results = []

    if not os.path.isdir(template_dir):
        print(f"{Fore.RED}[!] Template directory not found: {template_dir}{Style.RESET_ALL}")
        return []

    templates = [f for f in os.listdir(template_dir) if f.endswith(".yaml")]

    def run_single_template(template_file):
        local_results = []
        path = os.path.join(template_dir, template_file)
        try:
            with open(path, "r") as f:
                template = yaml.safe_load(f)
        except Exception as e:
            return []

        for req in template.get("requests", []):
            method = req.get("method", "GET").upper()
            for url_path in req.get("path", []):
                final_url = url_path.replace("{{BaseURL}}", base_url)

                try:
                    resp = requests.request(method, final_url, timeout=10, verify=False)

                    for matcher in req.get("matchers", []):
                        part = matcher.get("part", "body")
                        match_type = matcher.get("type", "word")
                        words = matcher.get("words", [])
                        target_text = resp.text if part == "body" else str(resp.headers)
                        matched = all(word in target_text for word in words)

                        if matched:
                            vuln_id = template.get("id", "unknown")
                            vuln_name = template["info"].get("name", "Unnamed Vulnerability")
                            severity = template["info"].get("severity", "info")

                            color = Fore.RED if severity == "high" else (Fore.YELLOW if severity == "medium" else Fore.GREEN)
                            print(f"{color}[VULN] {vuln_name} ({severity.upper()}) → {final_url}{Style.RESET_ALL}")

                            local_results.append({
                                "type": "vulnerability",
                                "id": vuln_id,
                                "name": vuln_name,
                                "severity": severity,
                                "url": final_url
                            })
                except Exception:
                    continue
        return local_results

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_template = {executor.submit(run_single_template, tmpl): tmpl for tmpl in templates}
        for future in as_completed(future_to_template):
            all_results.extend(future.result())

    return all_results
