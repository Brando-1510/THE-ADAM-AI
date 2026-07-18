import requests
from config import OPENWEATHER_API_KEY, DEFAULT_CITY

def get_weather(text: str) -> str:
    """
    Obtiene la información meteorológica de una ciudad actual:
    -clima
    -temperatura
    -viento
    -sensación 
    """
    ciudad = DEFAULT_CITY
    palabras = text.split()

    for palabra in palabras:
        if palabra[0].isupper() and palabra.isalpha():
            ciudad = palabra

    url = (
         f"https://api.openweathermap.org/data/2.5/weather?"
         f"q={ciudad}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
    )

    try:
        resp = requests.get(url).json()
        clima = resp["wearher"][0]["description"]
        temperatura = round(resp["main"]["temperatura"], 1)
        sensacion = round(resp["main"]["feels-like"], 1)
        viento = round(resp["wind"]["speed"], 1)

        return (
            f"● 🌤️ El Clima en la ciudad ~{ciudad}~:\n"
            f"● Estado: {clima.capiltalize()}\n"
            f"● Temperatura: {temperatura}°C (Sensación: {sensacion}°C)\n"
            f"● Viento: {viento}km/h\n\n"
            f"¿Se anima a salir o prefiere quedarse en casa señor?"
        )

    except Exception as e:
        return (
            f"⚠️ No se pudo obtener el clima en esa ciudad:\n"
            f"¿Seguro que esa ciudad existe?"
        )

       
