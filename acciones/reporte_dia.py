import os
import requests
from datetime import datetime, timedelta


def obtener_clima(ciudad: str = "Temuco,CL") -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es"
    }
    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        descripcion = datos["weather"][0]["description"]
        temperatura = datos["main"]["temp"]
        sensacion_termica = datos["main"]["feels_like"]
        return f"El clima en {ciudad} es {descripcion} con una temperatura de {temperatura}°C y sensación térmica de {sensacion_termica}°C."
    except requests.RequestException as e:
        return f"No se pudo obtener el clima: {e}"


def obtener_noticias(query: str = "chile", cantidad: int = 10) -> str:
    api_key = os.getenv("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "es",
        "sortBy": "popularity",
        "apiKey": api_key,
        "pageSize": cantidad,
        "from": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    }
    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        titulares = [articulo["title"] for articulo in datos.get("articles", [])]
        if not titulares:
            return "No se encontraron noticias para hoy."
        return "Noticias más populares:\n" + "\n".join(f"- {titulo}" for titulo in titulares)
    except requests.RequestException as e:
        return f"No se pudo obtener las noticias: {e}"


def generar_reporte_dia(contexto: str) -> None:
    clima = obtener_clima()
    noticias = obtener_noticias()
    fecha = datetime.now().strftime("%Y-%m-%d")
    reporte = f"\nReporte del día {fecha}:\n\n{clima}\n\n{noticias}"
    print(reporte)