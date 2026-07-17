"""
Modulo encargado de almacenar el contexto inmediato de la conversación, implementa el historial 
de conversación de corto plazo o envía a memoria semántica, de ser relevante.
"""

from collections import deque 
from datetime import datetime
from typing import Dict, List, Optional
#ignora errores especificos, evita que una excepcion interrumpa la ejecucion, lo hace más legible.
from contextlib import suppress                                            

# Importación necesaria para los modelos de memoria/conversacional de langchain
from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage
# Importacion necesaria para evitar la serialización de objetos privados como los datos de conversación en (deque)
from pydantic import PrivateAttr

#importa la funcion, pero si no existe o no se pudo importar, laza un error, (suppress) lo captura silenciosamente
with suppress(ImportError):                 
    from semantic_memory import add_memory

class ContextCache(BaseMemory):
    _history: deque = PrivateAttr()

    def __init__(self, max_len: int = 10):
        super().__init__()
        self._history = deque(maxlen = max_len)

    def add(self, role: str, content: str):
        timestamp = datetime.now().isoformat()
        evento = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        self._history.append(evento)
    
#Guarda en memoria semática solo si el contexto lo requiere (contenido de usuario, asistente, cargaemocional, identidad usuario, info recordatorio)
        if role in ["user", "assistant", "emotional", "identity", "reminder"]:
            with suppress(Exception):
                add_memory(
                    text = content,
                    metadata = {"role": role, "timestamp": timestamp}
                )
#devuelve los mensajes almacenados en el historial en una lista copia del mismo
    def get_messages(self):
        return list(self._history)
    
#obtiene el ultimo mensaje almacenado en el historial cpn [-1] y verifica si no está vacia, devuelve None para evitar errores.
    def get_last(self):
        return self._history[-1] if self._history else None
    
#limpia historial
    def clear(self):
        self._history.clear()

#compatibilidad (indispensable) con Langchain, metodos requeridos
 
    def load_memory_variables(self, inputs: Dict[str, any]) -> Dict[str, any]:
        return {"chat_history": self._convert_to_langchain_messages()}

    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]) -> None:
        if "input" in inputs:
            self.add("user", inputs["input"])
        if "output" in outputs:
            self.add("assistant", outputs["output"])

    @property
    def memory_variables(self) -> List[str]:
        return ["chat_history"]
    

#convierte el historial de conversación a mensajes que Langchain pueda procesar
    def _convert_to_langchain_messages(self) -> List:
        messages = []
        for m in self._history:
            role = m["role"]
            content = m["content"]
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
        
        return messages

