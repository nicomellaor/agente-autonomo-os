def extraer_nombre_archivo(contexto: str) -> str:
    pass


def buscar_archivo(nombre_archivo: str) -> str:
    pass


def abrir_archivo(contexto: str) -> None:
    nombre_archivo = extraer_nombre_archivo(contexto)
    ruta_archivo = buscar_archivo(nombre_archivo)
    if ruta_archivo:
        print(f"Abriendo el archivo: {ruta_archivo}")
    else:
        print(f"No se encontró el archivo: {nombre_archivo}")