import imaplib
import email
import os
from email.header import decode_header


def decodificar_campo(campo: str) -> str:
    partes = decode_header(campo)
    resultado = []
    for contenido, codificacion in partes:
        if isinstance(contenido, bytes):
            resultado.append(contenido.decode(codificacion or "utf-8", errors="replace"))
        else:
            resultado.append(contenido)
    return "".join(resultado)


def revisar_correos(contexto: str, cantidad: int = 5) -> None:
    usuario = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD").replace(" ", "")

    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(usuario, password)
        imap.select("INBOX")

        _, mensajes = imap.search(None, "UNSEEN")
        ids = mensajes[0].split()[-cantidad:]

        if not ids:
            print("No hay correos nuevos sin leer.")
            return
        
        for uid in reversed(ids):
            _, data = imap.fetch(uid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            print(f"\nDe: {decodificar_campo(msg['From'])}")
            print(f"Asunto: {decodificar_campo(msg['Subject'])}")
            print(f"Fecha: {msg['Date']}")
            print("-" * 40)