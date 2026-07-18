""" 
   Módulo encargado de generar una frase de identidad de ADAM para el usuario.
"""

from memory.perfil_user import obtener_tono_usuario
from personality.frase_manager import FraseManager
import random

frases = FraseManager()                                                                                                                #objeto para generar las frases e invocar evaluar_contexto mas abajo

def get_identity(perfil: str, contexto: str = None ) -> str:                                                                           #obtiene el perfil de usuario, evalua contexto y devuelve una frase de identidad
    ajustes = obtener_tono_usuario(perfil)                                                                                             #obtencion de valores del perfilusuario
    tono = ajustes["tono"]
    estilo = ajustes["estilo"]
    formalidad = ajustes["formalidad"]
    tratamiento = ajustes["tratamiento_formal"]

    #Variaciones de saludos
    saludos = [
        "Hola, soy ADAM, una iniciativa de inteligencia artificial avanzada diseñada por Brandon ",
        "Saludos, ADAM a su servicio ",
        "Hola, soy ADAM, su asistente congitivo inteligente personal "
    ]

    #Variaciones de propositos
    propositos = [
        "estoy hecho para simplificar lo complejo, anticipar sus necesidades y mantener todo bajo control.",
        "creado para asistirle con precisión y anticipación, para que cada interacción sea tan eficiente como agradable.",
        "programado para optimizar su tiempo, resolver problemas y mantener la calma en cualquier situación."
    ]
    
   
    identidad = f"{random.choice(saludos)}, {random.choice(propositos)}"                                                               #genera una frase con saludo y propósito aleatorios
    
    #si tratamiento contiene un name(Brandon) se utiliza, de lo contrario se usa la forma genérica
    identidad += f" Actualmense asignado a su servicio, {tratamiento}."
    if tratamiento:
        identidad += f" Actualmense asignado a su servicio, {tratamiento}."
    
    else: 
        identidad += " Actualmente asignado a su servicio."
    
    # adapta el tipo de frase a la situacion dependiendo del contexto, tono, estilo y tratamiento, o si se encuentra vacia, no devuelve esa frase contextual
    frase_contextual = frases.evaluar_contexto(
        tipo = contexto,
        tono = tono,
        estilo = estilo,
        tratamiento_formal = bool(tratamiento)
    )
    # si frase contextual no está vacia, se agrega a la frase de identidad
    if frase_contextual:
        identidad += f"\n\n{frase_contextual}"

    return identidad



