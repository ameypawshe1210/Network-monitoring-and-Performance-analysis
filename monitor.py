import subprocess
import time
import json
from scapy.all import ARP, Ether, srp

# Change this to match your router's IP range (e.g., 192.168.1.0/24)
TARGET_NETWORK = "192.168.0.0/24"

def discover_hosts():
    print(f"Scanning {TARGET_NETWORK} for live devices...")
    arp = ARP(pdst=TARGET_NETWORK)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    try:
        result = srp(packet, timeout=2, verbose=0)[0]
        return [received.psrc for sent, received in result]
    except Exception as e:
        print(f"Scan error: {e}")
        return ["8.8.8.8", "1.1.1.1"] # Fallback to public DNS if scan fails

while True:
    live_hosts = discover_hosts()
    data = []

    for host in live_hosts:
        # -n 1 (1 packet), -w 1000 (wait 1 second)
        cmd = ["ping", "-n", "1", "-w", "1000", host]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)

        if result.returncode == 0:
            status = "Active"
            # Extracts 'time=XXms' from the ping output
            latency = result.stdout.split("time=")[1].split("ms")[0].strip() if "time=" in result.stdout else "0"
        else:
            status = "Down"
            latency = "N/A"

        data.append({
            "host": host,
            "status": status,
            "latency": latency + "ms" if latency != "N/A" else "N/A"
        })

    with open("network_data.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Update complete. Found {len(live_hosts)} devices.")
    time.sleep(10)