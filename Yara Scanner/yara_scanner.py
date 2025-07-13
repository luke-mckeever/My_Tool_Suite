import os
import sys
import subprocess
from pathlib import Path

# Set paths
YARA_EXE = Path("../../Defensive Security Toolkit (BLUE)/yara64.exe").resolve()
RULES_DIR = Path("../../Defensive Security Toolkit (BLUE)/Yara-rules-master").resolve()

def collect_yara_rules(directory):
    return [
        Path(root) / file
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith((".yar", ".yara"))
    ]

def run_yara_scan(rule_file, target_file):
    try:
        result = subprocess.run(
            [str(YARA_EXE), str(rule_file), str(target_file)],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():  # Only output actual matches
            print(f"\n[+] Match found with rule: {rule_file.name}\n{result.stdout.strip()}")
    except Exception:
        pass  # Suppress all errors for a clean output

def main():
    if len(sys.argv) != 2:
        print("Usage: python yara_scanner.py <target_file>")
        sys.exit(1)

    target_file = Path(sys.argv[1]).resolve()
    if not target_file.exists():
        print(f"[-] File not found: {target_file}")
        sys.exit(1)

    if not YARA_EXE.exists():
        print(f"[-] YARA executable not found at: {YARA_EXE}")
        sys.exit(1)

    if not RULES_DIR.exists():
        print(f"[-] YARA rules directory not found at: {RULES_DIR}")
        sys.exit(1)

    rules = collect_yara_rules(RULES_DIR)
    if not rules:
        print("[-] No YARA rule files found.")
        sys.exit(1)

    print(f"[+] Scanning '{target_file.name}' with {len(rules)} YARA rule(s)...")

    for rule in rules:
        run_yara_scan(rule, target_file)

    print("\n[✓] Scan complete. Only positive matches are shown.")

if __name__ == "__main__":
    main()
