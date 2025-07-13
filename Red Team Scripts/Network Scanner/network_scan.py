import scapy.all as scapy
import socket
from concurrent.futures import ThreadPoolExecutor
import argparse

# Common ports to scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

def scan_network(ip_range):
    """
    Perform an ARP scan to find live hosts in the network.
    """
    print(f"Scanning network {ip_range} for live hosts...")
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    clients = []
    for element in answered_list:
        clients.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return clients

def scan_ports(ip, ports):
    """
    Scan specified ports on a given IP address.
    """
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Network device and port scanner")
    parser.add_argument("ip_range", help="IP range to scan (e.g., 192.168.1.0/24, 10.0.0.0/16, 172.16.0.0/12, 192.168.0.0/24)")
    args = parser.parse_args()

    clients = scan_network(args.ip_range)
    print(f"Found {len(clients)} devices on the network.\n")

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ip = {executor.submit(scan_ports, client['ip'], COMMON_PORTS): client for client in clients}

        for future in future_to_ip:
            client = future_to_ip[future]
            try:
                open_ports = future.result()
                print(f"IP: {client['ip']} | MAC: {client['mac']} | Open Ports: {open_ports if open_ports else 'None'}")
            except Exception as e:
                print(f"Error scanning {client['ip']}: {e}")

if __name__ == "__main__":
    main()
