import time
import argparse
from datetime import datetime
from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, DNS, Raw

PROTOS = {1: "ICMP", 6: "TCP", 17: "UDP"}
stats = {}

def payload_preview(pkt, n=60):
    if pkt.haslayer(Raw):
        data = bytes(pkt[Raw].load)[:n]
        return "".join(chr(b) if 32 <= b < 127 else "." for b in data)
    return ""

def handle(pkt):
    if not (pkt.haslayer(IP) or pkt.haslayer(IPv6)):
        return
    ip = pkt[IP] if pkt.haslayer(IP) else pkt[IPv6]
    proto = PROTOS.get(getattr(ip, "proto", None), "Other")
    stats[proto] = stats.get(proto, 0) + 1
    sport = dport = ""
    flags = ""
    if pkt.haslayer(TCP):
        sport, dport, flags = pkt[TCP].sport, pkt[TCP].dport, str(pkt[TCP].flags)
    elif pkt.haslayer(UDP):
        sport, dport = pkt[UDP].sport, pkt[UDP].dport
    extra = ""
    if pkt.haslayer(DNS) and pkt[DNS].qd:
        extra = f" DNS query: {pkt[DNS].qd.qname.decode(errors='ignore')}"
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {proto:<5} {ip.src}:{sport} -> {ip.dst}:{dport} "
          f"len={len(pkt)} flags={flags}{extra}")
    p = payload_preview(pkt)
    if p:
        print(f"           payload: {p}")

def main():
    ap = argparse.ArgumentParser(description="Basic network sniffer")
    ap.add_argument("-i", "--iface", help="interface (default: auto)")
    ap.add_argument("-c", "--count", type=int, default=0, help="stop after N packets (0 = no limit)")
    ap.add_argument("-t", "--time", type=int, default=0, help="stop after N seconds (0 = no limit)")
    ap.add_argument("-f", "--filter", default="", help="BPF filter, e.g. 'tcp port 80'")
    a = ap.parse_args()
    print("Sniffing... press Ctrl+C to stop.\n", flush=True)
    start = time.time()
    try:
        while True:
            sniff(iface=a.iface, filter=a.filter, prn=handle, timeout=1, store=False)
            if a.count and sum(stats.values()) >= a.count:
                break
            if a.time and time.time() - start >= a.time:
                break
    except KeyboardInterrupt:
        pass
    print("\nSummary:", stats or "no IP packets captured")

if __name__ == "__main__":
    main()