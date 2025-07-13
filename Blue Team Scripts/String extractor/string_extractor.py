import sys
import re
from pathlib import Path

def extract_ascii_strings(filepath, min_length=4):
    with open(filepath, 'rb') as f:
        data = f.read()
    pattern = rb'[\x20-\x7E]{%d,}' % min_length  # printable ASCII chars
    return [match.decode('ascii') for match in re.findall(pattern, data)]

def extract_unicode_strings(filepath, min_length=4):
    with open(filepath, 'rb') as f:
        data = f.read()
    pattern = (b'(?:[%s]\x00){%d,}' % (b'\x20-\x7E', min_length)).decode('ascii')
    return [match.decode('utf-16le') for match in re.findall(pattern.encode(), data)]

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_strings.py <file> [--unicode]")
        sys.exit(1)

    file_path = Path(sys.argv[1]).resolve()
    if not file_path.exists():
        print(f"[-] File not found: {file_path}")
        sys.exit(1)

    use_unicode = "--unicode" in sys.argv

    print(f"[+] Extracting {'ASCII and Unicode' if use_unicode else 'ASCII'} strings from: {file_path.name}\n")

    ascii_strings = extract_ascii_strings(file_path)
    unicode_strings = extract_unicode_strings(file_path) if use_unicode else []

    combined = ascii_strings + unicode_strings
    for s in combined:
        print(s)

    print(f"\n[✓] Extracted {len(combined)} strings (min length: 4).")

if __name__ == "__main__":
    main()
