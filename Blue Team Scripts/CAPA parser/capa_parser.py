import argparse
import subprocess
import json
import os
import sys

def run_capa(target_file, capa_path="capa-master/capa.exe"):
    if not os.path.exists(capa_path):
        print(f"[-] capa executable not found at: {capa_path}")
        sys.exit(1)

    try:
        result = subprocess.run(
            [capa_path, target_file, "-j"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error running capa: {e.stderr}")
        sys.exit(1)

def summarize_capabilities(capa_json):
    summary = {}

    rules = capa_json.get("rules", {})
    for rule_name, rule_info in rules.items():
        namespace = rule_info.get("meta", {}).get("namespace", "unknown")
        if namespace not in summary:
            summary[namespace] = []
        summary[namespace].append(rule_name)

    print("\n=== 🧠 Simplified CAPA Summary ===")
    for ns, rules in summary.items():
        print(f"\n🔹 {ns.capitalize()} Capabilities:")
        for rule in rules:
            print(f"  - {rule}")
    print("\n===================================")

def main():
    parser = argparse.ArgumentParser(description="Run capa on a binary and summarize its capabilities.")
    parser.add_argument("filename", help="Path to the binary file")
    args = parser.parse_args()

    target_file = os.path.abspath(args.filename)
    capa_exe = os.path.abspath("capa-master/capa.exe")

    print(f"[+] Running capa on: {target_file}")
    capa_output = run_capa(target_file, capa_exe)

    print("\n=== 🧪 Raw CAPA Output ===")
    for rule, data in capa_output.get("rules", {}).items():
        print(f"- {rule}: {data.get('meta', {}).get('description', '')}")

    summarize_capabilities(capa_output)

if __name__ == "__main__":
    main()
