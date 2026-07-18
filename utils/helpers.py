import re
from datetime import datetime

def capitalizar(texto: str) -> str:
    """Capitaliza la primera letra de cada palabra sin alterar al resto del texto"""
    return texto[0].upper() + texto[1:] if texto else " "

def extraer_perfil_contexto(texto: str) -> tuple:
    """Extrae el perfil y contexto para poder generar una respuesta. """
    partes = texto.split("|")
    perfil = partes[0].strip()
    contexto = partes[1].strip() if len(partes) > 1 else None
    return perfil, contexto

def quitar_espacios(texto: str) -> str:
    """Quita los espacios en blanco y normaliza el texto"""
    return " ".join(texto.split())

def formatear_nombre(nombre: str) -> str:
    """Limpia y capitaliza nombres propios"""
    return nombre.strip().title()

def generar_timestamp(formato: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Genera la hora y fecha actual en un formato legible"""
    return datetime.now().strftime(formato)

def pregunta(texto: str) -> bool:
    """Verifica si es una pregunta simple"""
    return texto.strip().endswith("?")

def normalizar_contexto(texto: str) -> str:
    """Covierte el texto en un contexto conocido si aplica"""
    texto = texto.lower()

    if "error" in texto or "fallo" in texto:
        return "logica-fallida"
    
    elif "repetición" in texto or "repetir" in texto:
        return "repetición"
    
    elif "petición" in texto or "orden" in texto or "solicitud" in texto:
        return "formal"
    
    elif "narrativo" in texto or "narrar" in texto: 
        return "narrativo"
    
    return "neutral"
    