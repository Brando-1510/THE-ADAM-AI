
"""Módulo encargado de ser el Cerebro y Corazón del asistente """
import sys
import logging
from datetime import datetime 
from dotenv import load_dotenv

load_dotenv(dotenv_path="claves.env")
from openai import RateLimitError

# NLP
from nlp.intent_classifier import classify_intent, detect_emotion, log_unrecognized
from nlp.interpreter import process_input
from nlp.llm_chain import SemanticChainBuilder

# Acciones
from actions.device_action import device_action
from actions.reminder_action import get_reminders, delete_reminder
from actions.weather_action import get_weather
from actions.general_actions import fallback_response
from actions.identity_action import get_identity

# Voz
from voice.tts_elevenlabs import Speak
from voice.stt_whisper import transcribe_audio

# Domotica
from domotic.configuracion import DomoticConfiguration

# Configuración
from config import (
    CLAVE_OPENAI,
    ELEVENLABS_API_KEY,
    OPENWEATHER_API_KEY,
    DEFAULT_CITY,
    VECTOR_STORE_PATH,
# Parámetros opcionales, por si se utilizan más adelante.
    SHORT_TERM_SIZE,
    MEDIUM_STORE_PATH,
    LONG_STORE_PATH,
    EMBEDDINGS_MODEL_NAME
)

# Memoria 
from memory.cache_context import ContextCache
from memory.memory_manager import MemoryManager
from memory.semantic_memory import SemanticMemory
from memory.perfil_user import obtener_tono_usuario
from memory.user_interaction_profile import UserInteractionProfile
from memory.interaction_mode import InteractionModeManager

# Personalidad 
from personality.core_identity import CoreIdentity
from personality.core_purpose import CorePurpose
from personality.evolution_tracker import EvolutionTracker
from personality.frase_manager import FraseManager
from personality.identity_interface import IdentityInterface
from personality.identity import Identity
from personality.response_signature import ResponseSignature
from personality.style_selector import StyleSelector
from personality.tone_manager import ToneManager


# Utilidades
from utils.helpers import (
    extraer_perfil_contexto,
    capitalizar,
    quitar_espacios,
    formatear_nombre,
    generar_timestamp,
    pregunta,
    normalizar_contexto
)

# Carga del modelo LLM 
from langchain_community.chat_models import ChatOpenAI
llm = ChatOpenAI(openai_api_key = CLAVE_OPENAI )

# Inicialización de Componentes 

context_cache = ContextCache(max_len = 20)
semantic_memory = SemanticMemory()
memory_manager = MemoryManager(llm = llm, salience_llm = llm)
identity = Identity()
core_identity = CoreIdentity()
purpose = CorePurpose()
signature = ResponseSignature()
frase_manager = FraseManager()
identity_interface = IdentityInterface()
style_selector = StyleSelector()
tone_manager = ToneManager()
evolution_tracker = EvolutionTracker()
user_profile = UserInteractionProfile(user_id = "Brandon")
interaction_mode = InteractionModeManager(profile = user_profile.get_full_profile())
domotica = DomoticConfiguration()

#parametros persistentes 
GOALS = ["anticipar", "asistir", "amplificar", "acompañar", "priorizar"]
THEME_CLUSTERS = ["tecnología", "entorno", "creatividad", "tareas"]

# LLM Chain y cadena semántica para la generación de respuestas
llm_chain = SemanticChainBuilder()._build_chain(
    user_state = user_profile.get_full_profile(),
    goals = GOALS,
    theme_clusters = THEME_CLUSTERS
)

def diagnostico():
    print("\nDiagnóstico inicial de ADAM\n")

    checks = {
        "Memoria semántica" : semantic_memory is not None,
        "Buffer Corto" : isinstance(semantic_memory.short_buffer, list),
        "FAISS Medio" : semantic_memory.medium_store is not None,
        "FAISS Largo" : semantic_memory.long_store is not None,
        "Identidad" : identity is not None,
        "Propósito" : purpose is not None,
        "TTS (ElevenLabs)" : ELEVENLABS_API_KEY is not None and len(ELEVENLABS_API_KEY) > 10,
        "Clima API" : OPENWEATHER_API_KEY is not None and len(OPENWEATHER_API_KEY) > 10,
        "Perfil de Usuario": user_profile.get_full_profile() is not None,
        "LLM Chain " : True,
    }
    for clave, estado in checks.items():
        estado_str = "✅ EN ORDEN" if estado else "❌ ERROR"
        print(f"{clave.ljust(25)} → {estado_str}")

    print("\n🔌 Escaneando entorno domótico...")
    domotica.scan_devices()

    print("\nSi ves errores ❌, revisa claves, rutas o inicialización de módulos\n")




def diagnostico_claves():
    print("\nDiagnóstico inicial de las claves API\n")
    errores = []

    if not CLAVE_OPENAI or CLAVE_OPENAI == "DUENDE_RICO":
        errores.append("⚠️ ADAM no puede acceder a su mente. Falta la clave OPENAI_API_KEY.")
    
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "DUENDE_RICO":
        errores.append("⚠️ Voz desactivada. Falta la clave ELEVENLABS_API_KEY.")

    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "DUENDE_RICO":
        errores.append("⚠️ Sensores ambientales desactivados. Falta la clave OPENWEATHER_API_KEY.")

    if errores:
        print("❌ Diagnóstico de claves:")
        for error in errores:
            print(error)
        exit()
    else:
        print("✅ Todas las Claves de API cargadas correctamente.")



def process_adam(text: str) -> str:
    # Interpreta semánticamente el texto
    interpretado = process_input(text)
    respuesta_interpretada = interpretado["respuesta"]
    emocion = interpretado["emoción"]

    # Clasificación de intención y emoción detectadas
    intent = classify_intent(text)
    emotion  = detect_emotion(text)

    # Memoria del sistema 
    context_cache.add(text, text)
    semantic_context = semantic_memory.query(text)
    memory_manager._process_turn("user", text)

    # Detección de intenciones 
    if intent == "reminder":
        respuesta_accion = get_reminders(text)
    
    elif intent == "delete_reminder":
        respuesta_accion = delete_reminder(text)
    
    elif intent == "weather":
        respuesta_accion = get_weather(text)
    
    elif intent == "device":
        respuesta_accion = device_action(text)
    
    elif intent == "identity":
        perfil, contexto = extraer_perfil_contexto(text)
        respuesta_accion = get_identity(perfil, contexto)
    
    else:
        respuesta_accion = fallback_response(text)

    # Genera la respuesta del LLM
    respuesta_llm = llm_chain.invoke(
        {
            "input": text,
            "user_state": user_profile.get_full_profile(),
            "goals": GOALS,
            "theme_clusters": THEME_CLUSTERS,
            "semantic_context": semantic_context,
            "interpretado": interpretado,

        },
        config = {"configurable": {"session_id": "Brandon"}}
    )


    # Obtención de identidad y tono
    perfil = identity.to_dict()
    tono_usuario = obtener_tono_usuario(perfil)
    tono_actual = tone_manager.get_tone_profile(tono_usuario.get("tono", "neutral"))
    estilo_actual = style_selector.select_style(user_profile.get_full_profile(), perfil, tono_actual, emocion)

    # Proposito narrativo
    contexto = "filosófico" if any(k in text.lower() for k in ["¿qué eres?", "proposito", "razón", "¿para qué?"]) else "neutro"
    base = purpose.explain_self(contexto)


    # Frase contextual
    frase = frase_manager.evaluar_contexto(
        tipo = contexto,
        tono = tono_actual,
        estilo = estilo_actual,
        tratamiento_formal = True 
    )
    if frase:
        base = f"{respuesta_interpretada}\n\n{frase} {base}"

    # Firma narrativa
    respuesta_final = signature.generate_response(
         identity = perfil,
         tono = tono_actual,
         style = estilo_actual,
         mensaje_central = base,
         tema = {"intencion": intent},
         usar_cierre = None
    )

    # Evolución 
    nuevo_perfil = identity.to_dict()
    cambio = evolution_tracker.detect_narrative_shift(perfil, nuevo_perfil)
    if cambio:
        evolution_tracker.record_change(
            source = "user",
            before = perfil,
            after = nuevo_perfil,
            reason = "cambio de usuario detectado",
            user_profile = user_profile
        )
   
    #conbina respuesta accion con narrativa, si aplica
    return f"{respuesta_accion}\n\n{respuesta_llm.content}\n\n{respuesta_final}"

def run_console():
        
    print("Hola, estoy listo para servirte, Brandon. Escribe tu mensaje o di 'adam' para entrada de audio. ")
    while True:
        entrada = input("User: ").strip()
        if entrada in ("salir", "exit", "quit"):
            print("ADAM: Hasta luego.")
            break
        
        elif entrada == "voz":
            texto = transcribe_audio()
            print(f"Usuario (voz): {texto}")

        else: 
            texto = entrada

        respuesta = process_adam(texto)
        print(f"ADAM: {respuesta}")
        Speak(respuesta)

if __name__ == "__main__":
    diagnostico()
    diagnostico_claves()
    run_console()












