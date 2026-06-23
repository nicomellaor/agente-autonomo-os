import os
import subprocess
import re


DIRECTORIOS_BUSQUEDA = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~"),
]


def extraer_nombre_archivo(contexto: str) -> str:
    # Nombre entre comillas
    match = re.search(r'["\']([^"\']+\.\w+)["\']', contexto)
    if match:
        return match.group(1)

    # Nombre con extensión sin comillas
    match = re.search(r'\b([\w\-]+\.\w+)\b', contexto)
    if match:
        return match.group(1)

    return ""


def buscar_archivo(nombre_archivo: str) -> str:
    for directorio in DIRECTORIOS_BUSQUEDA:
        ruta = os.path.join(directorio, nombre_archivo)
        if os.path.exists(ruta):
            return ruta

    # Búsqueda recursiva si no se encontró
    for directorio in DIRECTORIOS_BUSQUEDA:
        for raiz, _, archivos in os.walk(directorio):
            if nombre_archivo in archivos:
                return os.path.join(raiz, nombre_archivo)

    return ""


def abrir_archivo(contexto: str) -> None:
    nombre_archivo = extraer_nombre_archivo(contexto)
    if not nombre_archivo:
        print("\nNo se detectó ningún archivo en el contexto.")
        return

    ruta_archivo = buscar_archivo(nombre_archivo)
    if ruta_archivo:
        print(f"\nAbriendo el archivo: {ruta_archivo}")
        subprocess.Popen(["xdg-open", ruta_archivo], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"\nNo se encontró el archivo: {nombre_archivo}")