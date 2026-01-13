import socket
import subprocess
from scapy.all import ARP, Ether, srp

try:
    from mac_vendor_lookup import MacLookup
    mac_lookup = MacLookup()
except:
    mac_lookup = None


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None


def netbios_name(ip):
    try:
        output = subprocess.check_output(
            ["nbtstat", "-A", ip],
            stderr=subprocess.DEVNULL
        ).decode(errors="ignore")

        for line in output.splitlines():
            if "<00>" in line and "UNIQUE" in line:
                return line.split()[0]
    except:
        pass
    return None


def mac_vendor(mac):
    if not mac_lookup:
        return None
    try:
        return mac_lookup.lookup(mac)
    except:
        return None


def scan_network(cidr):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr)
    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []

    for _, received in result:
        ip = received.psrc
        mac = received.hwsrc

        name = (
            reverse_dns(ip)
            or netbios_name(ip)
            or "Unknown"
        )

        vendor = mac_vendor(mac) or "Unknown vendor"

        devices.append((ip, mac, name, vendor))

    return devices


if __name__ == "__main__":
    network = input("input the target network (default: 127.0.0.1): ").strip() or "127.0.0.1"

    for ip, mac, name, vendor in scan_network(network):
        print(f"{ip:15}  {name:25}  {vendor}")
