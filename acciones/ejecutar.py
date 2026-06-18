PROGRAMAS_PERMITIDOS = {

}


def extraer_programa(contexto: str) -> str:
    pass


def ejecutar_programa(contexto: str) -> None:
    programa = extraer_programa(contexto)
    if programa in PROGRAMAS_PERMITIDOS:
        print(f"Ejecutando el programa: {programa}")
    else:
        print(f"Programa no permitido: {programa}")