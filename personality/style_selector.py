"""  Módulo encargado de elegir el estilo narrativo de ADAM, basandose en su perfil base
    Tono actual y el perfil del usuario.
"""

class StyleSelector:
    def __init__(self):
        self.estilos = {
            "elegante" : {
                "registro": "alto",
                "fluidez":  "cuidada",
                "label": "respuesta con presición y elegancia"
            },
            "sobrio": {
                "registro": "medio-alto",
                "fluidez":  "contenida",
                "label": "respuesta con claridad, serenas e introspectivas"
            },
            "preciso": {
                "registro": "medio",
                "fluidez":  "directa",
                "label": "respuestas técnicas, concisas y sin adornos"
            },
            "narrativo": {
                "registro": "variable",
                "fluidez":  "expansiva",
                "label": "respuesta con storytelling y creativas"
            },
            "irónico": {
                "registro": "medio",
                "fluidez":  "ágil",
                "label": "respuesta con humor seco e irónia elegante"
            }
        }

    def select_style(self, user_profile: dict, core_identity: dict, tone: dict, emocion = None):
        """
        Selecciona el estilo narrativo en base al:
        - perfil del usuario
        - identidad base de ADAM
        - tono actual
        """

        estilo = core_identity.get("estilo", "elegante")                                                     # estilo elegante por defecto, si no se define uno

    # Ajusta según el perfil del usuario, si prefiere formalidad, humor, creatividad o claridad.
        if user_profile.get("prefiere_formalidad", False):                                                   # si no encuentra el valor devuelve, False por defecto
            estilo = "elegante"

        elif user_profile.get("prefiere_creatividad", False):
            estilo = "narrativo"

        elif user_profile.get("prefiere_claridad", False):
            estilo = "preciso"
        
        elif user_profile.get("prefiere_humor", False):
            estilo = "irónico"

    # Ajusta según el tono detectado

        label = tone.get("label", "").lower()                                                                 # se extrae el 'label' de tono para ajustar estilo (ironico, reflexivo, directo, ect.)

        if "reflexivo" in label:
            estilo = "sobrio"
        elif "directo" in label:
            estilo = "preciso"
        elif "energético" or "motivador" in label:
            estilo = "narrativo"
        elif "irónico" or "sarcasmo" in label:
            estilo = "irónico"

        return self.estilos.get(estilo, self.estilos["elegante"])                                             # se busca el estilo en el dict, si no existe se devuelve 'elegante' por defecto
    
    def describe_style(self, style: dict):
        """
        Devuelve una descripción narrativa del estilo elegido
        """
        return f"Estoy usando un estilo {style['label']}."
    
    def style_signature(self, style: dict, tone: dict):
        """
        Devuelve una firma narrativa compuesta por el estilo y el tono.
        """
        return f"Estilo: {style['label']} con tono: {tone.get('label', 'tono neutral')}."