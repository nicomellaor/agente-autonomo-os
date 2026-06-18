from acciones.reporte_dia import generar_reporte_dia
from acciones.correos import revisar_correos
from acciones.generar import generar_archivo
from acciones.abrir import abrir_archivo
from acciones.ejecutar import ejecutar_programa


def ejecutar_accion(accion:str, contexto: str) -> None:
    match accion:
        case "REPORTE_DIA":
            generar_reporte_dia(contexto)
        case "REVISAR_CORREOS":
            revisar_correos(contexto)
        case "GENERAR_ARCHIVO":
            generar_archivo(contexto)
        case "ABRIR_ARCHIVO":
            abrir_archivo(contexto)
        case "EJECUTAR_PROGRAMA":
            ejecutar_programa(contexto)
        case _:
            print(f"Acción no reconocida: '{accion}'")