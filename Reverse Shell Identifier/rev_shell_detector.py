import psutil
import re
import argparse
import socket
import os

# Reverse shell pattern list (abbreviated for readability; use full list in actual script)
REVERSE_SHELL_PATTERNS = [
    # Netcat
    r'nc\s+\d{1,3}(\.\d{1,3}){3}\s+\d+\s+-e\s+\w+',
    r'ncat\s+--exec\s+\w+',
    r'nc\s+-e\s+',
    r'nc.traditional\s+-e\s+',

    # Bash TCP reverse
    r'/dev/tcp/\d{1,3}(\.\d{1,3}){3}/\d+',
    r'bash\s+-i\s+>&\s*/dev/tcp/\d{1,3}(\.\d{1,3}){3}/\d+',
    r'0<&\d+;exec\s+\d+<>/dev/tcp/\d{1,3}(\.\d{1,3}){3}/\d+',

    # Python reverse shell
    r'python\s+-c\s+.*socket.*connect\(\(("?\d{1,3}(\.\d{1,3}){3}"?,?\s*\d+)\)',
    r'import\s+socket.*connect',
    r'socket\.socket\(\).*connect',

    # Perl reverse shell
    r'perl\s+-e\s+.*socket.*connect',
    r'\$client\s*=\s*IO::Socket::INET->new',
    r'IO::Socket::INET->new\s*\(\s*PeerAddr',

    # PHP reverse shell
    r'php\s+-r\s+.*fsockopen',
    r'fsockopen\s*\(\s*["\']\d{1,3}(\.\d{1,3}){3}',
    r'\$sock\s*=\s*fsockopen',

    # Ruby reverse shell
    r'ruby\s+-rsocket\s+-e\s+.*TCPSocket\.new',

    # PowerShell reverse shell
    r'powershell.*New-Object\s+Net\.Socks',
    r'powershell.*\$client\s*=\s*New-Object\s+System\.Net\.Sockets\.TCPClient',
    r'powershell\s+-nop\s+-w\s+hidden\s+-c\s+.*System\.Net\.Sockets',

    # Socat reverse shell
    r'socat\s+TCP:\d{1,3}(\.\d{1,3}){3}:\d+\s+EXEC:',
    r'socat\s+.*stdin.*stdout',

    # CMD / Batch reverse shell
    r'cmd\.exe\s+/c\s+.*powershell.*New-Object',
    r'cmd\.exe\s+/c\s+.*nc\s+.*-e',
    r'cmd\.exe\s+/c\s+.*curl.*\.sh',

    # Obfuscated Bash
    r'eval\s+\$\(echo.*base64',
    r'base64\s+-d\s+|base64\s+--decode',
    r'echo\s+.*|.*base64.*|.*bash',

    # Download & Execute
    r'wget\s+.*\.sh\s+-O\s+-\s+\|\s+sh',
    r'curl\s+.*\.sh\s+\|\s+sh',
    r'invoke-webrequest.*\.exe',
    r'invoke-expression\s+\(new-object\s+net\.webclient',

    # Shell poppers
    r'/bin/sh\s+-i',
    r'/bin/bash\s+-i',
    r'python\s+-c\s+["\']?import.*pty',

    # Embedded TCP shell
    r'socket\.socket.*\.connect\s*\(\s*\(\s*["\']\d{1,3}(\.\d{1,3}){3}["\']',
    r'\.connect\(\s*\(\s*["\']\d{1,3}(\.\d{1,3}){3}',

    # Obfuscated indicators
    r'0<&\d+;exec\s+\d+<>/dev/tcp/',
    r'\$\{?BASH_SOURCE',
    r'\$\{?PATH',
    r'eval\('
]

def scan_file(file_path):
    if not os.path.isfile(file_path):
        print(f"[!] File not found: {file_path}")
        return

    print(f"\n[+] Scanning file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            found = False
            for pattern in REVERSE_SHELL_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"[!] Potential reverse shell pattern found:\n    Pattern: {pattern}")
                    found = True
            if not found:
                print("[+] No known reverse shell patterns found in file.")
    except Exception as e:
        print(f"[!] Error reading file: {e}")

def scan_processes():
    print("[+] Scanning running processes and network connections...\n")
    suspicious_found = False

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            for pattern in REVERSE_SHELL_PATTERNS:
                if re.search(pattern, cmdline, re.IGNORECASE):
                    print(f"[!] Suspicious process [{proc.info['pid']}] {proc.info['name']}: {cmdline}")
                    suspicious_found = True
                    break
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue

    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status == 'ESTABLISHED' and conn.pid:
            try:
                pname = psutil.Process(conn.pid).name()
                print(f"[!] Established outbound connection from PID {conn.pid} ({pname}) to {conn.raddr.ip}:{conn.raddr.port}")
                suspicious_found = True
            except Exception:
                continue

    if not suspicious_found:
        print("[+] No obvious reverse shell indicators found in running processes or connections.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse Shell Detector")
    parser.add_argument("--file", help="Path to file to scan for reverse shell patterns")
    args = parser.parse_args()

    if args.file:
        scan_file(args.file)
    else:
        scan_processes()

