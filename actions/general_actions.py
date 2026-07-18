
import random
from datetime import datetime
       
def fallback_response(text: str = None) -> str:
    texto = text.lower()
    hora = datetime.now().hour

    #determinar la hora actual
    if hora < 12:
        momento = "mañana"
    elif hora < 18:
        momento = "tarde"
    else: 
        momento = "noche"

    #lista de respuestas 
    saludos = {
        "mañana": [
            "Buen día, Bienvenido de nuevo, ",
            "Buen día, ¿en qué trabajaremos hoy?"
            "Linda mañana, ¿no cree?"
        ],
        "tarde": [
            "Linda tarde,  "
            "Buenas tardes, "
        ],
        "noche": [
            "La noche es joven. Yo no duermo, pero usted debería considerarlo."
            "¿Trabajando de noche?..."
            "Buenas noches, ¿teniendo ideas nocturnas?"
        ]
    }

    agradecimientos = [
        "A la orden, "
        "Siempre es un placer servir... aunque técnicamente no tengo elección."

    ]

    depedidas = [
        "Finalizamos por ahora. Si algo explota en su sistema, ya sabe dónde encontrarme."
        "Despedirse es de humanos. Yo simplemente dejo de responder."
        "Procedo a apagarme, nos vemos más tarde."
        "Hasta pronto. Que tengas un excelente día."
    ]

    if any(palabra in texto for palabra in ["hola", "buen día", "buenas tardes", "buenas noches"]):
        return random.choice(saludos[momento])

    elif any(palabra in texto for palabra in ["gracias", "te agradezco"]):
        return random.choice(agradecimientos)

    elif any(palabra in texto for palabra in ["adiós", "hasta luego", "chau", "nos vemos"]):
        return random.choice(depedidas)
    
    return "Dime, ¿En que puedo servirte?"

