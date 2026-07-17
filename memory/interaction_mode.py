
class InteractionModeManager:
    def __init__(self, profile):
        self.profile = profile

#Ejecución
    def get_execution_strategy(self):
        mode = self.profile.get("execution")
        strategies = {
            "reactive": self._reactive_execution,
            "deliberative": self._deliberative_execution,
            "hybrid" : self._hybrid_execution
        }
        
        return strategies.get(mode, self._default_execution)
    
#Tono y estilo visual
    def get_tone_and_style(self):
        return {
            "tone" : self.profile.get("tone"),
            "style" : self.profile.get("style")
        }

#Razonamiento 
    def get_reasoning_strategy(self):
        mode = self.profile.get("reasoning")
        strategies = {
            "analitic" : self._analitic_reasoning,
            "intuitive" : self._intuitive_reasoning,
            "narrativo" : self._narrative_reasoning
        }

        return strategies.get(mode, self._default_reasoning)

#Nivel de iniciativa
    def get_initiative_level(self):
        self.profile.get("initiative")

#Metodos internos
    def _reactive_execution(self, input_data):
        return (f"Ejecutando de forma reactiva: {input_data}")
    
    def _deliberative_execution(self, input_data):
        return (f"Evaluando contexto antes de ejecutar: {input_data}")
    
    def _hybrid_execution(self, input_data):
        return (f"Ejecutando con estrategia híbrida: {input_data}")

    def _default_execution(self, input_data):
        return (f"Ejecutando de forma por defecto: {input_data}")
        
    def _analitic_reasoning(self, input_data):
        return (f"Razonamiento analítico aplicado a: {input_data}")
    
    def _intuitive_reasoning(self, input_data):
        return (f"Razonamiento intuitivo aplicado a: {input_data}")
    
    def _narrative_reasoning(self, input_data):
        return (f"Construyendo una narrativa para: {input_data}")
    
    def _default_reasoning(self, input_data):
        return (f"Razonamiento por defecto aplicado a: {input_data}")

        