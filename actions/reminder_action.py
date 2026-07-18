import os 
import json
from datetime import datetime

REMINDER_PATH = "recordatorios.json"

def get_reminders(text: str)-> str:
    """
    Obtiene los recordatorios almacenados en un archivo JSON
    """
    recordatorio = {
        "texto": text,
        "fecha": datetime.now().isoformat()
    }
    
    try:
        if not os.path.exists(REMINDER_PATH):
            with open(REMINDER_PATH, "w") as f:
                json.dump([], f)

        with open(REMINDER_PATH, "r", encoding="utf-8") as f:
            recordatorios = json.load(f)

        with open(REMINDER_PATH, "w", encoding="utf-8") as f:
            json.dump(recordatorios, f, indent = 4, ensure_ascii = False)

    except Exception as e:
        print(f"[Ocurrió un error al intentar guardar su recordatorio!]{e}")
        return "⚠️ Ocurrió un error al guardar, quizá quiera intentar de nuevo más tarde."
        
def delete_reminder(index: int) -> str:
    """ Elimina cualquier recordatorio de la memoria"""
    try:
        if not os.path.exists(REMINDER_PATH):
            return"⚠️ No hay recordatorios guardados aún."
        
        with open(REMINDER_PATH, "r", encoding= "utf-8") as f:
            recordatorios = json.load(f)

        if index < 0 or index > len(recordatorios):
            return f"❌ El recordatorio {index} al que se refiere no existe."
        
        eliminado = recordatorios.pop(index)
        
        with open(REMINDER_PATH, "w", encoding= "utf-8") as f:
            json.dump(recordatorios, f, indent= 4, ensure_ascii = False)

        return (
            f"✅ Su recordatorio {index} ha sido eliminado con exito.\n"
            f"● \"-{eliminado['texto']}\""
        )
        
    except Exception as e:
        print(f"[Ocurrió un error al intentar eliminar su recordatorio!]{e}")
        return "⚠️ Ocurrió un error al eliminar, quizá quiera intentar de nuevo más tarde."

        



