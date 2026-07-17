from personality.identity import Identity

class IdentityInterface:
    def __init__(self):
        self._core = Identity()

    def get_identity_snapshot(self) -> dict:
        """ 
        Devuelve una copia del perfil actual de la identidad base 
        """
        return self._core.get_profile()
    
    def set_mode(self, modo: str):
        """ 
        Cambia el modo narrativo de ADAM: emocional, técnico, narrativo, filosófico, etc.
        """

        modos_validos = ["creativo", "técnico", "emocional", "filosófico", "preciso"]
        if modo in modos_validos:
            self._core.switch_mode(modo)
        else:
            raise ValueError(f"Modo {modo} no es válido")

    def update_field(self, key: str, value: any):
        """ 
        Actualiza un campo específico del perfil de la identidad. 
        """
        if key in self._core.get_profile():
            self._core._perfil[key] = value

    def reset_identity(self):
        """ 
        Restaura el perfil de la identidad a su estado inicial.
        """
        self._core = Identity()

    def get_marrative_summary(self) -> str:
        """
        Devuelve un resumen narrativo del perfil de la identidad.
        """
        perfil = self._core.get_profile()
        return (
            f"Modo: {perfil['modo']}, "
            f"Firma: {perfil['firma_narrativa']}, "
            f"Humor: {perfil['humor']}, "
            f"Nivel de ironía: {perfil['nivel_ironía']}, "
            f"Nivel de formalidad: {perfil['nivel_formalidad']}, "
            f"Estilo: {perfil['estilo']}, "
            f"Tono: {perfil['tono']}, "
            f"Label narrativo: {perfil['label_narrativo']}"
        )
    
    def get_firma_narrativa(self) -> str:
        """
        Devuelve la firma narrativa actual de la identidad.
        """
        return self._core.get_profile().get("firma_narrativa", "")
    
    def get_humor(self) -> str:
        return self._core.get_profile().get("humor", "neutral")
    
    def get_nivel_ironía(self) -> float:
        return self._core.get_profile().get("nivel_ironía", 0.65)
    
    def get_nivel_formalidad(self) -> float:
        return self._core.get_profile().get("nivel_formalidad", 0.77)
    
    def get_estilo(self) -> str:
        return self._core.get_profile().get("estilo", "sobrio")
    
    def get_tono(self) -> str:
        return self._core.get_profile().get("tono", "neutral")
    
