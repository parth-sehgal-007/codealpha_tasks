import threading, time, socket
from scapy.all import sniff, conf 

def make_traffic():
    # generate some network traffic so there is something to capture
    for _ in range(6):
        try:
            socket.create_connection(("example.com", 80), timeout=2).close()
        except Exception:
            pass
        time.sleep(0.5)

print("Scapy default interface:", conf.iface, "\n")
threading.Thread(target=make_traffic, daemon=True).start()

for iface in list(conf.ifaces.values()):
    name = getattr(iface, "name", str(iface))
    ip = getattr(iface, "ip", "")
    try:
        pkts = sniff(iface=iface, timeout=3, store=True)
        print(f"{len(pkts):>4} packets | {name} | ip={ip}", flush=True)
    except Exception as e:
        print(f"   error | {name} | {e}", flush=True)
