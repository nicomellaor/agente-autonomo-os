# Diseño de un Agente Autónomo de Sistema Operativo

## Objetivo

> Diseñar y fundamentar la arquitectura de un asistente de escritorio automatizado basado en el mecanismo de Auto-Atención.

## Resumen

El repositorio contiene módulos para acciones concretas sobre el sistema (abrir archivos, ejecutar aplicaciones, revisar correos, generar archivos y reportes).

Estructura relevante:
- `main.py`: punto de entrada del agente (orquestación).
- `controlador.py`, `modelo.py`: componentes de control e interfaz con el modelo.
- `acciones/`: implementaciones por acción.

## Acciones realizadas (descripción de cada módulo en `acciones/`)

- `abrir.py`: busca archivos en ubicaciones típicas del usuario (`~/Documents`, `~/Downloads`, `~/Desktop`, `~`) y abre el archivo encontrado usando `xdg-open`. Incluye búsqueda recursiva si no se encuentra en los directorios principales.

- `correos.py`: conecta a Gmail vía IMAP para listar correos no leídos. Lee las credenciales desde variables de entorno (`GMAIL_USER`, `GMAIL_APP_PASSWORD`) y decodifica encabezados para mostrar remitente, asunto y fecha.

- `ejecutar.py`: permite lanzar aplicaciones predefinidas a través de rutas seguras (`PROGRAMAS_PERMITIDOS`). Hace comprobaciones básicas de existencia y permisos antes de ejecutar procesos con `subprocess.Popen`.

- `generar.py`: genera archivos en distintos formatos (`txt`, `md`, `pdf`, `docx`, `xlsx`, `csv`) a partir de un texto o contexto. Usa `FPDF` para PDF, `python-docx` para DOCX, `openpyxl` para XLSX y módulos estándar para CSV/TXT.

- `reporte_dia.py`: construye un breve reporte diario que integra el clima (OpenWeather) y noticias (NewsAPI). Lee las claves de API desde variables de entorno (`OPENWEATHER_API_KEY`, `NEWSAPI_KEY`) y realiza peticiones HTTP con `requests`.

## Librerías usadas

Las principales dependencias del proyecto son:

- `torch`, `transformers`, `tokenizers`, `safetensors`: inferencia con modelo local.
- `requests`: llamadas HTTP (clima, noticias).
- `python-dotenv`: carga de variables de entorno desde un archivo `.env` (opcional).
- `fpdf`, `python-docx`, `openpyxl`: generación de archivos (PDF, DOCX, XLSX).
- `imaplib`, `email`: lectura de correos vía IMAP.
- `openpyxl`, `csv`: manipulación de hojas y CSV.
- `rich`, `typer`: utilidades opcionales para CLI y salida enriquecida.

## Variables de entorno

- `OPENWEATHER_API_KEY`: clave para OpenWeather (usada en `acciones/reporte_dia.py`).
- `NEWSAPI_KEY`: clave para NewsAPI (usada en `acciones/reporte_dia.py`).
- `GMAIL_USER`: dirección de correo para conexión IMAP (usada en `acciones/correos.py`).
- `GMAIL_APP_PASSWORD`: contraseña o app password para IMAP (usada en `acciones/correos.py`).

## Resumen del modelo usado

Flujo de inferencia: cargar tokenizador y modelo con `transformers` / `safetensors` y ejecutar pasos de inferencia sobre inputs textuales. El repositorio incluye `requirements.txt` con `torch` y `transformers` para este propósito.

## Instalación y uso rápido

1. Crear un entorno virtual y activar:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Añadir variables de entorno (Copiar `.env.example` a `.env`).

3. Ejecutar el agente:

```bash
python main.py
```
