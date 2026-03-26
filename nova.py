import os
import sqlite3
import threading
import time
import subprocess
import telebot
import requests
import asyncio
import edge_tts 
import pygame
import re
import schedule
from datetime import datetime, timedelta

# ==========================================================
# --- CONFIGURACIÓN MANUAL ---
# ==========================================================
HORA_SALUDO = "22:00"  # <--- Cambie la hora aquí
PROYECTO_PATH = r"D:\Repositories\tally-ai" 
TELEGRAM_TOKEN = '8616169584:AAEzDtmkStJgd4-acNPZ0hD6RF58GOhKYN4'
VOZ_NEURAL = "es-MX-JorgeNeural"
# ==========================================================

user_chat_id = None 
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- DICCIONARIO DE CLIMA PERSONALIZADO ---
WEATHER_CODES = {
    '113': 'despejado, un día excelente para programar',
    '116': 'parcialmente nublado',
    '119': 'nublado',
    '122': 'muy nublado',
    '143': 'con neblina en la zona',
    '176': 'con probabilidad de chubascos dispersos',
    '182': 'con aguanieve ligera',
    '200': 'con posibles tormentas eléctricas',
    '263': 'con llovizna dispersa',
    '266': 'con llovizna ligera',
    '296': 'con lluvia ligera',
    '302': 'con lluvia moderada',
    '311': 'con lluvia ligera y aguanieve',
    '353': 'con lluvia ligera suave',
    '356': 'con lluvia moderada o fuerte',
}

def init_db():
    conn = sqlite3.connect('nova_memoria.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tareas 
                      (id INTEGER PRIMARY KEY, descripcion TEXT, fecha TEXT, hora TEXT,
                       notificado_pre INTEGER DEFAULT 0, notificado_ahora INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# --- 1. MOTOR DE AUDIO ---
async def generar_voz_async(texto):
    archivo_voz = "nova_neural.mp3"
    texto_con_pausa = "... , ... , " + texto 
    communicate = edge_tts.Communicate(texto_con_pausa, VOZ_NEURAL, rate="+25%")
    await communicate.save(archivo_voz)
    return archivo_voz

def hablar(texto, enviar_a_celular=True):
    print(f"\n[NOVA DICE]: {texto}")
    archivo = None
    try:
        archivo = asyncio.run(generar_voz_async(texto))
        if user_chat_id:
            with open(archivo, 'rb') as audio_file:
                bot.send_voice(user_chat_id, audio_file)
        
        if pygame.mixer.get_init(): pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load(archivo)
        time.sleep(0.5)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): time.sleep(0.1)
        pygame.mixer.music.unload()
        pygame.mixer.quit()
    except: pass
    finally:
        if archivo and os.path.exists(archivo):
            try: os.remove(archivo)
            except: pass

# --- 2. LÓGICA DE CLIMA TRADUCIDA ---
def obtener_clima():
    try:
        # Pedimos el código (%c) y la temperatura (%t)
        res = requests.get("https://wttr.in/Suba?format=%c+%t", timeout=5)
        if res.status_code == 200:
            # wttr.in a veces devuelve iconos, probamos con el formato de código numérico
            res_code = requests.get("https://wttr.in/Suba?format=%k", timeout=5)
            code = res_code.text.strip()
            temp = res.text.split()[-1] # Extrae la temperatura (ej: +15°C)

            estado = WEATHER_CODES.get(code, "con un clima estable")
            return f"{estado} y una temperatura de {temp}"
    except: pass
    return "un clima agradable en la localidad de Suba"

def obtener_resumen_hoy():
    hoy = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect('nova_memoria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion, hora FROM tareas WHERE fecha=?", (hoy,))
    tareas = cursor.fetchall()
    conn.close()
    if not tareas: return "No hay tareas pendientes en la agenda para el día de hoy."
    lista = ", ".join([f"{t[0]} a las {t[1]}" for t in tareas])
    return f"Sus compromisos para hoy son: {lista}."

# --- 3. FUNCIONES DE AUTOMATIZACIÓN ---
def reporte_matutino():
    clima = obtener_clima()
    tareas = obtener_resumen_hoy()
    mensaje = (
      f"Hola. Buenos días, señor Jonathan y señorita Camila. Son las {HORA_SALUDO}. Hoy en suba estamos {clima}. "
      f"{tareas} Recuerden mantenerse enfocados y dar lo mejor de sí mismos. Éxitos en su jornada."
    )
    hablar(mensaje)

# --- 4. LOS VIGILANTES ---
def vigilante_tareas():
    while True:
        try:
            ahora = datetime.now()
            h_actual = ahora.strftime("%H:%M")
            f_hoy = ahora.strftime("%Y-%m-%d")
            h_pre = (ahora + timedelta(minutes=30)).strftime("%H:%M")
            
            conn = sqlite3.connect('nova_memoria.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, descripcion FROM tareas WHERE fecha=? AND hora=? AND notificado_pre=0", (f_hoy, h_pre))
            for t in cursor.fetchall():
                hablar(f"Señor Jonathan, recordatorio: en 30 minutos tiene {t[1]}.")
                cursor.execute("UPDATE tareas SET notificado_pre=1 WHERE id=?", (t[0],))

            cursor.execute("SELECT id, descripcion FROM tareas WHERE fecha=? AND hora=? AND notificado_ahora=0", (f_hoy, h_actual))
            for t in cursor.fetchall():
                hablar(f"Señor Jonathan, atención. Ya es hora de: {t[1]}.")
                cursor.execute("UPDATE tareas SET notificado_ahora=1 WHERE id=?", (t[0],))
            
            conn.commit()
            conn.close()
        except: pass
        time.sleep(15)

def vigilante_schedule():
    schedule.every().day.at(HORA_SALUDO).do(reporte_matutino)
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=vigilante_tareas, daemon=True).start()
threading.Thread(target=vigilante_schedule, daemon=True).start()

# --- 5. MANEJADOR DE MENSAJES ---
@bot.message_handler(func=lambda m: True)
def manejar_mensajes(m):
    global user_chat_id
    user_chat_id = m.chat.id
    texto = m.text
    t = texto.lower()
    
    if "nova" in t:
        f_m = re.search(r'\d{4}-\d{2}-\d{2}', texto)
        h_m = re.search(r'\d{2}:\d{2}', texto)
        
        if f_m and h_m:
            f, h = f_m.group(), h_m.group()
            desc = re.sub(r'(?i)nova|anotar', '', texto).replace(f, "").replace(h, "").replace(",", "").strip()
            conn = sqlite3.connect('nova_memoria.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tareas (descripcion, fecha, hora) VALUES (?, ?, ?)", (desc, f, h))
            conn.commit()
            conn.close()
            hablar(f"Entendido señor Jonathan. He agendado '{desc}' para el {f} a las {h}.")
        
        elif "clima" in t:
            hablar(f"Señor Jonathan, el cielo en Suba se encuentra {obtener_clima()}.")
        elif "modo trabajo" in t:
            hablar("Iniciando herramientas de desarrollo, señor Jonathan.")
            subprocess.Popen(['cursor', PROYECTO_PATH], shell=True)
            subprocess.Popen(f'start cmd /K "cd /d {PROYECTO_PATH} && npm run dev"', shell=True)
        elif "resumen" in t or "tareas" in t:
            hablar(obtener_resumen_hoy())
        elif "hola" in t:
            hablar("A sus órdenes, señor Jonathan.")
        else:
            hablar("Dígame, señor Jonathan, ¿en qué puedo ayudarle?")

print(f"--- [ NOVA ONLINE | Saludo a las {HORA_SALUDO} ] ---")
bot.polling(non_stop=True)