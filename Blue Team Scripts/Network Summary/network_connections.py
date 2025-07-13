import psutil
from datetime import datetime

def summarize_network_activity():
    print(f"\n[+] Network Activity Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
    connections = psutil.net_connections(kind='inet')
    process_cache = {}

    if not connections:
        print("[-] No active network connections found.")
        return

    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        pid = conn.pid

        # Skip if PID is None (system/unknown process)
        if pid is None:
            pname = "Unknown"
        elif pid in process_cache:
            pname = process_cache[pid]
        else:
            try:
                proc = psutil.Process(pid)
                pname = proc.name()
                process_cache[pid] = pname
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pname = "Unknown"

        print(f"Process: {pname} (PID: {pid if pid else 'N/A'})")
        print(f"  Local Address : {laddr}")
        print(f"  Remote Address: {raddr}")
        print(f"  Status        : {conn.status}")
        print("-" * 60)

def main():
    try:
        summarize_network_activity()
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
