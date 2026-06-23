import subprocess
import shutil


PROGRAMAS_PERMITIDOS = {
    "firefox": "/usr/bin/firefox",
    "chromium": "/usr/bin/chromium-browser",
    "calculadora": "/usr/bin/gnome-calculator",
    "terminal": "/usr/bin/ptyxis",
    "editor de texto": "/usr/bin/gnome-text-editor",
    "navegador de archivos": "/usr/bin/nautilus",
    "vscode": "/usr/bin/code",
    "libreoffice": "/usr/bin/libreoffice",
    "gimp": "/usr/bin/gimp",
    "discord": "/var/lib/flatpak/exports/bin/com.discordapp.Discord",
    "spotify": "/var/lib/flatpak/exports/bin/com.spotify.Client",
}


def extraer_programa(contexto: str) -> str:
    contexto = contexto.lower()
    for programa in PROGRAMAS_PERMITIDOS:
        if programa in contexto:
            return programa
    return ""


def ejecutar_programa(contexto: str) -> None:
    programa = extraer_programa(contexto)
    ruta = PROGRAMAS_PERMITIDOS.get(programa)
    if not ruta:
        print(f"\nPrograma no permitido: {programa}")
    if not shutil.which(ruta):
        print(f"\nPrograma no encontrado en el sistema: {ruta}")    
    try:
        subprocess.Popen([ruta], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"\nEjecutando el programa: {programa}")
    except Exception as e:
        print(f"\nNo se pudo ejecutar el programa: {e}")