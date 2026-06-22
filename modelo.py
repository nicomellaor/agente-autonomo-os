import os
import warnings
warnings.filterwarnings("ignore")
 
import torch
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSequenceClassification
 
MODELO_BASE = "dccuchile/bert-base-spanish-wwm-uncased" # 1024 dimensiones, 12 capas, 110M parámetros
RUTA_MODELO = "agente_os_model"
UMBRAL_CONFIANZA = 45.0
EPOCHS = 15

ACCIONES = [
    "REPORTE_DIA",      # 0
    "REVISAR_CORREOS",  # 1
    "GENERAR_ARCHIVO",  # 2
    "ABRIR_ARCHIVO",    # 3
    "EJECUTAR_PROGRAMA" # 4
]

DATASET_ENTRENAMIENTO = [
    # REPORTE_DIA (0)
    ("qué clima hace hoy", 0),
    ("cómo está el tiempo hoy", 0),
    ("dame el reporte del día", 0),
    ("cuáles son las noticias de hoy", 0),
    ("qué pasó hoy en el mundo", 0),
    ("dame un resumen del día", 0),
    ("qué novedades hay hoy", 0),
    ("qué temperatura hace afuera", 0),

    # REVISAR_CORREOS (1)
    ("revisa mi correo", 1),
    ("tengo mensajes nuevos", 1),
    ("hay correos sin leer", 1),
    ("muéstrame mi bandeja de entrada", 1),
    ("chequea el email", 1),
    ("algún correo importante", 1),
    ("revisa mis mensajes", 1),
    ("qué dice mi correo hoy", 1),

    # GENERAR_ARCHIVO (2)
    ("crea un archivo llamado informe.txt con el texto resumen diario", 2),
    ("genera un documento pdf con el contenido ventas de junio", 2),
    ("haz un archivo md que diga notas de la reunión", 2),
    ("crea un csv con el texto nombre,correo,estado", 2),
    ("genera un docx con el mensaje acta de seguimiento", 2),
    ("haz un xlsx con los datos producto,cantidad,precio", 2),
    ("guarda un archivo de texto con el contenido pendiente por revisar", 2),
    ("crea el archivo resumen_final.md con el texto conclusiones del proyecto", 2),

    # ABRIR_ARCHIVO (3)
    ("abre el archivo informe.txt", 3),
    ("quiero abrir el documento /home/nico/Downloads/contrato.pdf", 3),
    ("muéstrame el archivo notas.md", 3),
    ("abre el pdf llamado reporte_final.pdf", 3),
    ("quiero ver el archivo config.yaml", 3),
    ("carga el documento ventas.xlsx", 3),
    ("abre el archivo de logs sistema.log", 3),
    ("muéstrame el archivo presupuesto_2026.csv", 3),
    
    # EJECUTAR_PROGRAMA (4)
    ("abre firefox", 4),
    ("ejecuta vscode", 4),
    ("lanza chromium", 4),
    ("abre gimp", 4),
    ("inicia libreoffice", 4),
    ("ejecuta la calculadora", 4),
    ("corre el terminal", 4),
    ("abre el navegador de archivos", 4),
]

tokenizador = AutoTokenizer.from_pretrained(MODELO_BASE)
 
frases  = [item[0] for item in DATASET_ENTRENAMIENTO]
etiquetas = [item[1] for item in DATASET_ENTRENAMIENTO]
 
inputs = tokenizador(frases, padding=True, truncation=True, return_tensors="pt")
labels = torch.tensor(etiquetas) 
 

def entrenar() -> AutoModelForSequenceClassification:
    modelo = AutoModelForSequenceClassification.from_pretrained(
        MODELO_BASE,
        num_labels=len(ACCIONES)
    )
    optimizador = AdamW(modelo.parameters(), lr=2e-5)
 
    modelo.train()

    for epoch in range(EPOCHS):
        optimizador.zero_grad()
        outputs = modelo(**inputs, labels=labels)
        perdida = outputs.loss
        perdida.backward()
        optimizador.step()
        print(f"   Época {epoch+1}/{EPOCHS} | Error (Loss): {perdida.item():.4f}")
    print("\n ¡Entrenamiento completado!\n")

    modelo.save_pretrained(RUTA_MODELO)
    tokenizador.save_pretrained(RUTA_MODELO)
    print(f"\nModelo guardado en '{RUTA_MODELO}/'")
    return modelo
 
 
def cargar_modelo():
    modelo = AutoModelForSequenceClassification.from_pretrained(RUTA_MODELO)
    tok    = AutoTokenizer.from_pretrained(RUTA_MODELO)
    modelo.eval()
    return modelo, tok
 
 
def inferir(modelo, tok, texto: str) -> tuple[str, float]:
    inputs_usuario = tok(texto, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        logits = modelo(**inputs_usuario).logits
        probabilidades = torch.nn.functional.softmax(logits, dim=-1)[0]
        indice = torch.argmax(probabilidades).item()
        confianza = probabilidades[indice].item() * 100
    return ACCIONES[indice], confianza
 
 
if __name__ == "__main__":
    if os.path.exists(RUTA_MODELO):
        print(f"Cargando modelo desde '{RUTA_MODELO}'...")
        modelo, tokenizador = cargar_modelo()
    else:
        print(f"Descargando y entrenando '{MODELO_BASE}'...")
        modelo = entrenar()