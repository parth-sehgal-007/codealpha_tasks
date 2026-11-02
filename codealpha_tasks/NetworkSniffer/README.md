# CodeAlpha_NetworkSniffer
Python packet sniffer built with Scapy. Shows time, protocol, source/destination IP and port, TCP flags, DNS queries and a printable payload preview, then prints a protocol summary.

## Setup
    pip install -r requirements.txt     # Windows: also install Npcap
    sudo python3 sniffer.py -c 20       # run as Administrator on Windows

## Options
- `-i eth0` choose interface  - `-c 50` stop after 50 packets  - `-f "tcp port 80"` BPF filter

## How it works
The NIC is put in capture mode, Scapy hands each frame to `handle()`, which parses the layers (Ethernet > IP > TCP/UDP > payload) and prints the useful fields.
Use only on networks you own or are allowed to monitor.
