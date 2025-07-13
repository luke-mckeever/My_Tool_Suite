import argparse
import socket
import sys
import platform

def get_hosts_file_path():
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system in ("Linux", "Darwin"):
        return "/etc/hosts"
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"Could not resolve domain: {domain}")
        sys.exit(1)

def add_redirect_entry(hosts_path, domain_in, domain_out_ip):
    entry = f"{domain_out_ip} {domain_in}\n"
    try:
        with open(hosts_path, "r") as f:
            lines = f.readlines()
        
        # Remove existing entries for domain_in
        lines = [line for line in lines if domain_in not in line]

        # Add new redirect entry
        lines.append(entry)

        with open(hosts_path, "w") as f:
            f.writelines(lines)
        print(f"Redirect added: {domain_in} -> {domain_out_ip}")
    except PermissionError:
        print("Permission denied: Run this script as administrator/root.")
        sys.exit(1)
    except Exception as e:
        print(f"Error modifying hosts file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Redirect domain browsing by modifying hosts file.")
    parser.add_argument("-din", required=True, help="Input domain to redirect from")
    parser.add_argument("-dout", required=True, help="Output domain to redirect to")
    args = parser.parse_args()

    hosts_path = get_hosts_file_path()
    domain_out_ip = resolve_ip(args.dout)
    add_redirect_entry(hosts_path, args.din, domain_out_ip)

if __name__ == "__main__":
    main()
