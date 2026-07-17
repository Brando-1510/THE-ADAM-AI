import os 
import logging                                                          #gestiona la salida de mensajes informativos y errores
from typing import Optional

import openai
from config import CLAVE_OPENAI 

# Configuracion de la libreria de logging, hora, nivel y mensaje de salida 
logging.basicConfig( 
    level = logging.INFO, 
    format = "%(asctime)s [%(levelname)s] %(message)s"
)
   

# Llave de OpenAI
openai.api_key = CLAVE_OPENAI  

# Trancripción de audio usando "WHISPER"
def transcribe_audio(
    audio_file_path: str,                                                             #ruta al archivo de audio
    modelo: str = "Whisper-1",
    normalize: bool = True                                                            #decide si se normaliza el texto transcrito
) -> str: 
    """
    Transcribe un archivo de audio usando Whisper de OpenAI.

    Parámetros:
    - audio_file_path: ruta al archivo de audio (debe existir).
    - modelo: Nombre del modelo de Whisper a usar. (Por defecto: Whisper-1)
    - normalize: si True, aplica strip().lower() al texto transcrito.

    Retorna:
    - Cadena con el texto transcrito (o un string en caso de error).
    """

    #Validaciones 
    if not isinstance(audio_file_path, str):                                          #verifica que el path sea una cadena de texto
        raise ValueError("El path debe ser una cadena de texto (str).")               
    if not os.path.isfile(audio_file_path):                                           #verifica si existe el archivo
        raise FileNotFoundError(f"No se encontró el archivo: {audio_file_path}.")
    
    try: 
        #lectura del archivo de audio en binario y llamada a la API de OpenAI
        with  open(audio_file_path, "rb") as f:                                       #abre el archivo en modo binario
            response = openai.Audio.transcribe(                                       #envia el audio a OpenAI y espera respuesta 
            modelo = modelo,
            archivo = f 
        )
            
        texto = response.get("text", " ")                                             #obtiene el texto transcrito
        if normalize:                                                                 #normaliza el texto 
            texto = texto.strip().lower()
          
        logging.info("Transcripción exitosa: %s", audio_file_path)                    #mensaje de salida
        return texto

    except Exception as err:
        logging.error("Error en la transcripción Whisper: %s", err)
        return " "
    
    

