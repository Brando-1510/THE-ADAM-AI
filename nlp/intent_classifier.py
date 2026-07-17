
from typing import Tuple

INTENT_KEYWORDS = {
    "weather": ["clima", "temperatura", "lluvia", "pronóstico"],
    "reminder": ["recuérdame", "recordar", "avísame", "notificar", "notifícame", "alarma"],
    "device": ["enciende", "apaga", "activa", "desactiva", "encender", "apagado"],
    "set_name": ["me llamo", "me llamas", "mi nombre es", "yo soy", "el es", "ella es"],
    "set_location": ["dónde está", "ubicación", "lugar", "sitio"],
    "time": ["hora", "tiempo"]
}

EMOTIONAL_TONES = {
    "happy": ["geníal", "perfecto", "gracias", "contento", "me ecanta"],
    "angry": ["odio", "molesto", "no sirve", "que porqueria", "muy mal", "chucha", "puta"],
    "sad": ["deprimido", "miedo", "no quiero", "me siento mal", "angustia", "aburrido"],
    "urgent": ["rápido", "ya", "apurate", "es urgente", "muy importante", "necesario"]

}

UNRECOGNIZED_LOG = []
def detect_emotion(text: str) -> str:
    """Detecta el tono emocinal del texto (usuario)"""
    t = text.lower()
    for tone, keywords in EMOTIONAL_TONES.items():
        if any(k in t for k in keywords):
            return tone
    return "neutral"

def log_unrecognized(text: str):
    """Registra frases no clasificadas para mejorar el aprendizaje incremental"""
    UNRECOGNIZED_LOG.append(text)


def classify_intent(text: str) -> Tuple[str, str]:
    """Determina la intención del usuario y su tono emocional.
       Devuelve una tupla tipo (intent, emotion)
    """
    t = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in t for k in keywords):
            emotion = detect_emotion(t)
            return intent, emotion
        log_unrecognized(text)
        return "General", detect_emotion(t)