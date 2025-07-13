import re
import sys
from pathlib import Path

def extract_iocs(text):
    return {
        "IPv4": re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text),
        "URLs": re.findall(r'https?://[^\s\'"<>]+', text),
        "Domains": re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', text),
        "MAC Addresses": re.findall(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b', text),
        "MD5 Hashes": re.findall(r'\b[a-fA-F\d]{32}\b', text),
        "SHA256 Hashes": re.findall(r'\b[a-fA-F\d]{64}\b', text),
        "Email Addresses": re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
    }

def write_to_file(output_path, iocs):
    with open(output_path, 'w') as f:
        f.write("=== Extracted IOCs ===\n")
        for category, items in iocs.items():
            f.write(f"\n{category}:\n")
            if items:
                for item in sorted(set(items)):
                    f.write(f"  - {item}\n")
            else:
                f.write("  None found\n")

def print_to_console(iocs):
    print("\n=== Extracted IOCs ===")
    for category, items in iocs.items():
        print(f"\n{category}:")
        if items:
            for item in sorted(set(items)):
                print(f"  - {item}")
        else:
            print("  None found")

def main():
    if len(sys.argv) < 2:
        print("Usage: python IOC_Extractor.py <filename> [-output outputfile.txt]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    output_file = None
    if "-output" in sys.argv:
        try:
            output_index = sys.argv.index("-output")
            output_file = Path(sys.argv[output_index + 1])
        except IndexError:
            print("Error: You must specify a file name after -output.")
            sys.exit(1)

    content = input_file.read_text(encoding='utf-8', errors='ignore')
    iocs = extract_iocs(content)

    if output_file:
        write_to_file(output_file, iocs)
        print(f"Results saved to: {output_file}")
    else:
        print_to_console(iocs)

if __name__ == "__main__":
    main()
