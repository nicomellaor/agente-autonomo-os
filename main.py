import os
from pyfiglet import figlet_format
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.traceback import install
from modelo import inferir, entrenar, cargar_modelo, RUTA_MODELO, UMBRAL_CONFIANZA
from controlador import ejecutar_accion


install()
console = Console()


def iniciar_modelo():
    if os.path.exists(RUTA_MODELO):
        return cargar_modelo()
    else:
        print("Entrenando modelo por primera vez...")
        modelo = entrenar()
        return modelo, None


def bucle_interactivo(modelo, tokenizador):
    console.print(figlet_format("AGENTE OS"), style="bold magenta")

    table = Table(title="Acciones Disponibles", title_justify="left")
    table.add_column("Acción", style="cyan", justify="center")
    table.add_column("Descripción", style="green")
    table.add_row("REPORTE_DIA", "Genera un reporte del día")
    table.add_row("REVISAR_CORREOS", "Revisa tus correos electrónicos")
    table.add_row("GENERAR_ARCHIVO", "Genera un archivo específico")
    table.add_row("ABRIR_ARCHIVO", "Abre un archivo existente")
    table.add_row("EJECUTAR_PROGRAMA", "Ejecuta un programa permitido")
    console.print(table)

    console.print("Describe qué acción deseas realizar (o 'salir' para terminar):", style="bold yellow")

    while True:
        texto = Prompt.ask(f"\n[magenta]>[/magenta]").strip()

        if not texto:
            continue

        if texto.lower() == "salir":
            console.print("   [green][AGENTE][/green]: ¡Hasta luego!")
            break

        accion, confianza = inferir(modelo, tokenizador, texto)
        console.print(f"   [cyan italic][AGENTE DETECTA][/cyan italic]: {accion} | Confianza: {confianza:.1f}%")

        if confianza < UMBRAL_CONFIANZA:
            console.print("   [bold red][AGENTE][/bold red]: No estoy seguro. ¿Puedes reformular?")
        else:
            console.print(f"   [green][AGENTE][/green]: Ejecutando acción '{accion}'")
            ejecutar_accion(accion, texto)

        console.rule(style="dim")


if __name__ == "__main__":
    modelo, tokenizador = iniciar_modelo()
    bucle_interactivo(modelo, tokenizador)