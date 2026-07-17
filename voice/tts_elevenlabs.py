import io
import time
import logging
from typing import Optional

import requests   
from pydub import AudioSegment   
from pydub.playback import play                                                                   
from config import ELEVENLABS_API_KEY    

#Configuración del Logging, hora, nivel y mensaje de salida
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s"
)

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"                                   


def Speak(
    text : str, 
    voice_id : str = "gnPxliFHTp6OK6tcoA6i",
    stability : float = 0.5,                                                                   #consistencia de la entonación 
    similaritary_boost : float = 0.7,                                                          #que tan parecido debe sonar(audio) al modelo original
    max_retries : int = 2,                                                                     #número máximo de reintentos
    backoff_factor : float = 0.5                                                               #factor de espera entre reintentos
    ) -> None:

    """  
    Envía texto a ElevenLabs y reproduce el audio resultante desde memoria.
    
    Parámetros:
    - text: Texto a sintetizar.
    - voice_id: ID de la voz de ElevenLabs.
    - stability: Que tan estable debe ser la entonación (0.0-1.0).
    - simmilaritary_boost: Que tan parecido debe sonar al modelo original (0.0-1.0).
    - max_retries: Número maximo de reintentos si la red falla.
    - backoff_factor: Factor de espera entre reintentos (segundos). 

    """
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similaritary_boost
        }
    }
    url = ELEVEN_URL.format(voice_id=voice_id)

#Intentos con BackOff (problemas de conexión)
    for intentar in range(1, max_retries + 1):
        try:
            respuesta = requests.post(url, json=payload, headers=headers, timeout=10)
            respuesta.raise_for_status()
            break
        except Exception as error:
            logging.warning(
                "Intento %d/%d fallido: %s", 
                intentar, max_retries, error
            )
            if intentar == max_retries:
                logging.error("Todos los reintentos fallaron. Abortando TTS.")
                return
            time.sleep(backoff_factor * intentar)

#Reproducción desde memoria con PyDub
    try:
        audio_bytes = io.Bytes(respuesta.content)
        audio = AudioSegment.from_file(audio_bytes, format="mp3")
        play(audio)
        logging.info("Reproducción exitosa de TTS para texto: %r", text)

    except Exception as error:
        logging.error("Error en la reproducción del audio: %s", error)

        





