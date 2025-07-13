import csv
import binascii
import os
import sys
import hashlib
import platform
import subprocess
from datetime import datetime

def load_magic_bytes(csv_path='magic_bytes.csv'):
    magic_dict = {}
    try:
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                signature = row['MagicBytes'].replace(" ", "").upper()
                file_type = row['FileType'].strip()
                magic_dict[signature] = file_type
    except FileNotFoundError:
        print(f"[ERROR] Could not find the CSV file: {csv_path}")
        sys.exit(1)
    return magic_dict

def get_file_hexdump(file_path):
    """Reads the entire file and returns its hex representation."""
    try:
        with open(file_path, 'rb') as f:
            return binascii.hexlify(f.read()).decode('utf-8').upper()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

def identify_file_type(file_path, magic_db):
    """Scans the full hex dump for known magic byte signatures."""
    hex_dump = get_file_hexdump(file_path)
    for magic, ftype in magic_db.items():
        if magic in hex_dump:
            return ftype
    return "Unknown file type"

def calculate_hashes(file_path):
    hashes = {'MD5': '', 'SHA1': '', 'SHA256': ''}
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            hashes['MD5'] = hashlib.md5(data).hexdigest()
            hashes['SHA1'] = hashlib.sha1(data).hexdigest()
            hashes['SHA256'] = hashlib.sha256(data).hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not hash file: {e}")
    return hashes

def get_file_metadata(file_path):
    stats = os.stat(file_path)
    return {
        'Size': stats.st_size,
        'Created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
        'Modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'Path': os.path.abspath(file_path)
    }

def detect_architecture(file_path):
    try:
        with open(file_path, 'rb') as f:
            magic = f.read(4)
        if magic.startswith(b'MZ'):
            return "Windows PE (Portable Executable)"
        elif magic == b'\x7fELF':
            return "Linux ELF"
        elif magic[:2] == b'\xcf\xfa':
            return "Mac Mach-O"
        else:
            return "Unknown/Not executable"
    except:
        return "Unknown"

def get_file_capabilities(file_path):
    if platform.system() != 'Linux':
        return "Not supported on this OS"
    try:
        result = subprocess.run(['getcap', file_path], capture_output=True, text=True)
        return result.stdout.strip() or "No capabilities"
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python file_identifier.py <filename>")
        sys.exit(1)

    file_to_check = sys.argv[1]
    if not os.path.isfile(file_to_check):
        print(f"[ERROR] Not a valid file: {file_to_check}")
        sys.exit(1)

    magic_db = load_magic_bytes()
    file_type = identify_file_type(file_to_check, magic_db)
    hashes = calculate_hashes(file_to_check)
    metadata = get_file_metadata(file_to_check)
    architecture = detect_architecture(file_to_check)
    capabilities = get_file_capabilities(file_to_check)

    print(f"\n[INFO] File Information Report")
    print(f"-------------------------------")
    print(f"Path         : {metadata['Path']}")
    print(f"File Type    : {file_type}")
    print(f"Architecture : {architecture}")
    print(f"Size         : {metadata['Size']} bytes")
    print(f"Created      : {metadata['Created']}")
    print(f"Modified     : {metadata['Modified']}")
    print(f"MD5          : {hashes['MD5']}")
    print(f"SHA1         : {hashes['SHA1']}")
    print(f"SHA256       : {hashes['SHA256']}")
    print(f"Capabilities : {capabilities}")
    print(f"-------------------------------\n")

if __name__ == "__main__":
    main()
