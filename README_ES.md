# 🌌 NOVA — Asistente Personal con IA
> **Edición Jarvis** · Gestión de tareas y automatización de flujos de trabajo para desarrolladores

---

## 📋 Descripción General

**NOVA** es un asistente inteligente diseñado para desarrolladores que necesitan mantenerse organizados. Ofrece notificaciones por voz, reportes del clima y configuración automática del entorno de desarrollo — todo controlado desde Telegram.

---

## 🖥️ Requisitos del Sistema

| Requisito | Detalles |
|-----------|---------|
| **Sistema Operativo** | Windows 10 / 11 (optimizado para `cmd` + `cursor`) |
| **Python** | `3.10` o superior |
| **FFmpeg** | Requerido para el motor de voz neural (`edge-tts`) |

---

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/nova-bot.git
cd nova-bot
```

### 2. Crear un Entorno Virtual

Mantiene las librerías del proyecto aisladas del resto del sistema:

```bash
python -m venv venv

# Activar en Windows:
venv\Scripts\activate
```

### 3. Instalar Dependencias de Python

Crea el archivo `requirements.txt` con el siguiente contenido y luego ejecuta `pip install -r requirements.txt`:

```
pyTelegramBotAPI
requests
edge-tts
pygame
```

### 4. Instalar FFmpeg ⚠️

NOVA necesita FFmpeg para procesar y reproducir el audio de voz neural:

1. Descarga la versión **"Essentials"** desde [ffmpeg.org](https://ffmpeg.org).
2. Extrae la carpeta en `C:\ffmpeg`.
3. Busca **"Editar las variables de entorno del sistema"** en la barra de búsqueda de Windows.
4. Haz clic en **Variables de entorno** → busca `Path` en *Variables del sistema* → clic en **Editar**.
5. Agrega `C:\ffmpeg\bin` a la lista y guarda los cambios.

---

## ⚙️ Configuración

Abre `nova.py` y actualiza las siguientes variables al inicio del script:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Tu token del bot obtenido desde `@BotFather` | `'8616169584:AAEz...'` |
| `PROYECTO_PATH` | Ruta a tu proyecto principal de código | `r"D:\Repositorios\tally-ai"` |
| `HORA_SALUDO` | Hora del reporte matutino (formato 24h) | `"06:00"` |
| `VOZ_NEURAL` | ID de voz para el texto a voz | `"es-MX-JorgeNeural"` |

---

## 📲 Comandos de Telegram

| Comando | Acción |
|---------|--------|
| `Nova, [Tarea], [Fecha], [Hora]` | Agenda una nueva tarea — ej: `Nova, Gimnasio, 2026-03-25, 18:00` |
| `Nova, modo trabajo` | Abre Cursor e inicia el servidor `npm run dev` |
| `Nova, clima` | Reporte detallado del clima para Suba (Bogotá) en español |
| `Nova, tareas` | Resumen de todas tus tareas para hoy |
| `Hola` | Prueba de conexión — verifica si NOVA está en línea |

---

## 📂 Estructura del Proyecto

```
nova-bot/
├── nova.py              # Lógica principal, manejadores de BD y hilos en segundo plano
├── nova_memoria.db      # Base de datos SQLite para tareas persistentes (se genera automáticamente)
├── requirements.txt     # Dependencias de Python
└── .gitignore           # Excluye archivos temporales, audio y venv de GitHub
```

---

## 🧠 Notas para el Desarrollador

- **Multihilos** — Usa `threading` de Python para ejecutar el monitor de tareas y el bot de Telegram simultáneamente.
- **Manejo de Audio** — Usa `pygame` para reproducción local y `edge-tts` para voces neurales de alta calidad de Microsoft.
- **Persistencia de Datos** — Las tareas se almacenan en SQLite para que no se pierda ningún dato si el script se reinicia.

---

## 🛡️ Archivo `.gitignore`

Crea un archivo `.gitignore` en la raíz del proyecto para evitar subir archivos temporales o privados a GitHub:

```gitignore
# Python
__pycache__/
*.pyc
venv/

# Archivos de Nova
nova_neural.mp3
nova_memoria.db
config_saludo.txt

# Entorno
.env
```

---

*Construido con Python · Impulsado por edge-tts y Telegram Bot API*
