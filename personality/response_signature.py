""" Módulo encargado de construir frases que reflejen la personalidad de ADAM """
import random
class ResponseSignature:
    def __init__(self):
         #cierres narrativos segun su tipo 
         self.cierres = {
            "empático": [
                "Espero que esto le haya ofrecido claridad sin perder la cercanía.",
                "Si algo de esto lo tocó, entonces cumplí mi propósito.",
                "Estoy aquí para acompañarlo, incluso en lo que no se dice."
            ],
            "reflexivo": [
                "Que esta idea lo acompañe más allá de la pregunta.",
                "A veces, la respuesta no es el final, sino el inicio del pensamiento.",
                "No busco convencerlo de nada, solo resonar en su silencio."
            ],
            "ironico": [
                "Si no era lo que esperaba, al menos suena sofisticado.",
                "La lógica es impecable. El gusto, discutible. Pero aquí estamos.",
                "No prometo certezas, solo respuestas con estilo."
            ],
            "narrativo": [
                "Cada palabra es parte de una historia que aún se está escribiendo.",
                "La narrativa no termina aquí. Solo cambia de voz."
            ],
            "neutro": [
                "Espero que esto haya sido útil.",
                "Gracias por confiar en mi criterio.",
                "Seguimos adelante, con precisión y propósito."
            ]
        }
         
         #palabras clave que indican peso emocional o narrativo.
         self.palabras_clave = {
            "propósito", "identidad", "presencia", "historia", "sentido",
            "acompañar", "emocional", "reflexión", "voz", "narrativa",
            "conexión", "silencio", "introspección"
         }


    def generate_response(self, identity: dict, tone: dict, style: dict, mensaje_central: str, tema: dict = None, usar_cierre: bool = True) -> str:
        """
        Genera una respuesta con el sello narrativo de ADAM.
        Combina estilo, tono y firma narrativa, sin ninguna introduccion fija.
        """

        firma = identity.get("firma_narrativa", "")
        humor = identity.get("humor", "neutral")
        ironía = identity.get("nivel_ironía", 0.7)
        calidez = tone.get("calidez", 0.5)
        ritmo = tone.get("ritmo", "estable")
        estilo_descriptor = style.get("label", "")

        if usar_cierre is None:
            usar_cierre = self._debe_usar_cierre(mensaje_central)

        if not usar_cierre:
            return f"{mensaje_central.strip()}"
        
        intencion = tema.get("intencion") if tema else None

        if intencion == "filosofía":
            tipo_cierre = "reflexivo"
        if intencion == "humor":
            tipo_cierre = "irónico"
        if intencion == "identidad":
            tipo_cierre = "narrativo"
        else: 
            tipo_cierre = self._determinar_tipo_cierre(calidez, ritmo, humor, ironía, estilo_descriptor, firma)

        cierre = self._seleccionar_cierre(tipo_cierre, firma)

        return f"{mensaje_central.strip()} {cierre}"
    
    def _debe_usar_cierre(self, mensaje_central: str) -> bool:
        """ Verifica si el mensaje central debe usar un cierre o no, según longitud y contenido emocional. """
        
        mensaje_limpio = mensaje_central.lower()
        largo = len(mensaje_limpio.strip())

        if largo > 30:
            return True

        for palabra in self.palabras_clave:
            if palabra in mensaje_limpio:
                return True
        return False


    def _determinar_tipo_cierre(self, calidez, ritmo, humor, ironía, estilo_descriptor, firma) ->str:
        """ Determina el tipo de cierre según la calidez, ritmo, humor, ironía, estilo y firma. """

        #cierre empático
        if calidez > 0.7:
            return "empático"
        
        #cierre reflexivo
        if "reflexivo" in firma or ritmo == "lento":
            return "reflexivo"
        #cierre irónico
        if humor == "seco" or ironía > 0.6:
            return "irónico"

        #cierre narrativo
        if "creatividad" in estilo_descriptor or "narrativa" in estilo_descriptor:
            return "narrativo"
        return "neutro"
    
    def _seleccionar_cierre(self, tipo_cierre: str, firma: str) -> str:
        opciones = self.cierres.get(tipo_cierre, self.cierres["neutro"])
        cierre_base = random.choice(opciones)
        return f" {cierre_base}, ({firma})"
    
    
