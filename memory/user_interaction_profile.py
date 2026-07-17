#Verifica y adapta la interacción hacia el usuario
class UserInteractionProfile:
    def __init__(self, user_id = None):
        self.user_id = user_id

    # diccionario con las 5 dimensiones del interacción
        self.profile = {
            "execution": "reactive",                      #reactive | deliberative | hybrid
            "tone" : "neutral",                           #neutral | emphatetic | emotional
            "initiative" : "proactive",                   #proactive | passive | adaptive 
            "style" : "elegant",                          #elegant | minimal | expressive
            "reasoning" : "analitic",                     #analitic | intuitive | narrative
        }

    def get(self, dimension : str):
        return self.profile.get(dimension)
    
    def Set(self, dimension : str, value : str):
        if dimension in self.profile:
            self.profile[dimension] = value
        else:
            raise ValueError(f"Tu dimensión está fuera de rango: {dimension}")
    
    def get_full_profile(self):
        return self.profile.copy()
    
    def update_profile(self, updates : dict):
        for key, value in updates.items():
            self.set(key, value)

    




