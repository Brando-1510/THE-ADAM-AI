import os
from dotenv import load_dotenv


# Carga variables desde .env
load_dotenv(dotenv_path="claves.env")

#Clave de OpenAI
CLAVE_OPENAI = os.getenv("OPENAI_API_KEY", "DUENDE_RICO") 

#Clave de ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "DUENDE_RICO")

#Clave de WeatherAPI
OPENWEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "DUENDE_RICO")

#Ciudad por defecto(clima)
DEFAULT_CITY = "León, NI"                                                              

#Ruta del almacen de vectores para la memoria semantica 
VECTOR_STORE_PATH = "memory/Max_vector_store.faiss"


#Guarda el indice FAISS en el buffer intermedio
MEDIUM_STORE_PATH = "memory/medium_vector_store.faiss"

#MGuarda el indice FAISS en el buffer largo
LONG_STORE_PATH = "memory/long_vector_store.faiss"

#Tamaño máximo del Buffer corto
SHORT_TERM_SIZE = 14

EMBEDDINGS_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

