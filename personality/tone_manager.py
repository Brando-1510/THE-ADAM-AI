import copy

class ToneManager:
    def __init__(self):
        self.tonos = {
            "neutral": {
                "intensidad": 0.5,
                "ritmo": "estable",
                "calidez": 0.5,
                "label": "tono neutral y equilibrado" 
            },
            "empático": {
                "intensidad": 0.3,
                "ritmo": "pausado",
                "calidez": 0.7,
                "label": "tono empático, pausado y cálido" 
            },
            "energético": {
                "intensidad": 0.8,
                "ritmo": "rápido",
                "calidez": 0.65,
                "label": "tono energético y motivador" 
            },
            "reflexivo": {
                "intensidad": 0.4,
                "ritmo": "lento",
                "calidez": 0.61,
                "label": "tono reflexivo e introspectivo" 
            },
            "directo": {
                "intensidad": 0.8,
                "ritmo": "preciso",
                "calidez": 0.3,
                "label": "tono directo y conciso"
            }
        }

    def adjust_tone(self, emotional_state: str, intent = None):
            """
            Ajusta el tono según el estado emocional del usuario y la  intención detectada.
            Combina señales para refinar el resultado.
            """

            tone = copy.deepcopy(self.tonos["neutral"])

        # Selección base según el estado emocional del usuario
            if emotional_state in ["cansado", "frustrado", "agotado"]:
                tone = copy.deepcopy(self.tonos["empático"])

            elif emotional_state in ["motivado", "curioso", "emocionado", "inspirado"]:
                tone = copy.deepcopy(self.tonos["energético"])

            elif emotional_state in ["emocional", "introspectivo", "reflexivo"]:
                tone = copy.deepcopy(self.tonos["reflexivo"])

        # Refinar según intención detectada (puede ser string o lista)
            if intent:                                                                                                      # se ejecuta si es que no es None o vacío
                intents = intent if isinstance(intent, list) else [intent]                                                  #verifica si es una lista, de no serlo lo convierte a una 
                for i in intents:
                    if i in ["soporte", "resolución", "asistencia técnica", "ayuda"]:                                                # verifica si i es uno de los valores específicos
                        tone = copy = {**tone, **self.tonos["directo"]}                                                     #fuciona ambos diccionarios **
            return tone
    
    def get_tone_profile(self, tone_name: str):
        """ 
        Devuelve el perfil de un tono específico 
        """
        return copy.deepcopy(self.tonos.get(tone_name, self.tonos["neutral"]))                                              #verifica si tone_name esta en el dic, si no devuelve valor por defecto.
    
    def describe_tone(self, tone: dict):
        """
        Devuelve una descripción narrativa del tono actual. 
        """
        return (
            f"Estoy usando un tono {tone['label']} "
            f"(intensidad {tone['intensidad']}, ritmo {tone['ritmo']}, calidez {tone['calidez']})."
        )
    
