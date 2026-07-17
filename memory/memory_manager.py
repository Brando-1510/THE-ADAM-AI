from memory.cache_context import ContextCache
from memory.semantic_memory import SemanticMemory

import time
import logging
from datetime import datetime, timezone
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.memory import CombinedMemory

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MemoryManager:
    def __init__(self, llm, salience_llm, short_len: int = 10, salience_threshold: float = 0.5):
        self.cache = ContextCache(max_len = short_len)                                                             #fija cuantos mensajes guardar antes de borrar el más viejo
        self.semantic = SemanticMemory(llm = llm)                                                                  #usa el llm para generar resumenes para almacenar/razonar 
        self.salience_chain = LLMChain(                                                                            #evalua la importancia de cada mensaje para guardar en memoria segun puntaje 0 a 1 
            llm = salience_llm,
            prompt = PromptTemplate(
                input_variables = ["text"],                                                                        #define la entrada (text) y la estructura del prompt
                template = "En una escala del 0-1, ¿qué tan importante es este mensaje para guardar en memoria?\n Texto: {text}"
            )
        )
        self.salience_threshold = salience_threshold                                                               #umbral minimo para egregar a memoria segun (score)             
        self.last_flush = datetime.now(timezone.utc)                                                               #marca del ultimo volcado de cache, se actualiza por cada flush


    def add_user_message(self, text: str):                                                                         #añade el mensaje del usuario al buffer de contexto (corto) guardando el rol y contenido
        self.cache.add(role = "user", content = text)                                                                       
        self._process_turn("user", text)                                                                           #procesa el turno del usuario, (analisis semantico, saliencia, guardado en memoria semantica, etc)

    def add_assistant_message(self, text: str):
        self.cache.add(role="assistant", content = text)
        self._process_turn("assistant", text)                                                                      #procesa el turno del asistente con la misma logica del usuario

    #procesa cada turno del usuario/asistente centraliza logica de evaluacion, persistencia y flush de memoria
    def _process_turn(self, role: str, text: str):
        score = float(self.salience_chain.run(text=text).strip())                                                  #ejecuta un llm para evaluar la saliencia del mensaje
        logger.info(f"Saliencia de turno ({role}): {score:.2f}")                                                   #imprime el rol y puntaje de saliencia en el log

        if score >= self.salience_threshold:  
    #diccionario con info: role, timestamp, salience                                                               #compara el puntaje y el umbral minimo para guardar en memoria
            metadata = {
                "role": role,
                "timestamp": datetime.now(timezone.utc).isformat(),
                "salience" : score
            }
            self.semantic.add_memory(text, metadata)

    #obtiene la zona horaria UTC 
        now = datetime.now(timezone.utc)
    #verifica si paso el intervalo de tiempo para flushear memoria, evita flushes inecesarios
        if now - self.lastflush > self.last_summary_interval:
            self._flush_cache_to_memory()                                                                          #consolida el contexto reciente en un resumen util
            self.last_flush = now                                                                                  #actualiza la marca de tiempo del último flush

    #resume el buffer corto y guarda en memoria semántica       
    def _flush_cache_to_memory(self):
        buffer = self.cache.get_messages()                                                                         #obtiene los mensajes almacenados en buffer corto
        items = [f"{m['role']}: {m['content']}" for m in buffer]                                                   #convierte los mensajes en formato role: content (m son los diccionarios dentro del buffer)
        mini = self.semantic.llm_chain.run(items = "\n".join(items), style ="bullets")   
        self.semantic.add_memory(mini, metadata = {"type": "cache_summary"})                                       #llama al llm para generar el reumen en formato viñeta
        self.cache.history.clear()
        logger.info("Flush de cache con mini-resumen a memoria semántica")

    #genera un resumen semantico para mantener el resumen sin perder el contexto 
    def summarize_background(self):
        self.semantic.sumarize_to_long()

    def get_memory(self):
        """ 
        Devuelve una memoria combinada que incluye:
        
        -ContextCache: memoria de corto plazo,
        -SemanticMemory: memoria semántica persistente
       
        """
        semantic_memory = self.semantic.get_langchain_memory()
        return CombinedMemory(memories = [
            self.cache,
            semantic_memory
        ])

    #recupera info relevante del historial de conversación
    def query(self, query: str, k: int = 5):                                                                       #query: texto a buscar | k : top-k número de resultados semanticos deseados  
        short = [m for m in self.cache.get_messages() if query.lower() in m["content"].lower()]                    #filtra los mensajes para encontrar el texto exacto

        #busca en memoria semantica, escencial en la memoria evolutiva
        sem = self.semantic.query_memory(query, k = k)                                   
        return {"short": short, "semantic": sem}
        
        #short = coincidencias literales
        #semantic = coincidencias semanticas








