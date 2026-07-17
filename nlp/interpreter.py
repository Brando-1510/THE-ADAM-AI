from nlp.intent_classifier import classify_intent
from memory.semantic_memory import SemanticMemory
from langchain_core.messages import HumanMessage
from memory.memory_manager import MemoryManager
from nlp.llm_chain import SemanticChainBuilder
from memory.cache_context import ContextCache

builder = SemanticChainBuilder()
llm = builder.llm
contexto = ContextCache()
sem_mem = SemanticMemory()
mem_manager = MemoryManager(llm = llm, salience_llm = llm)

def process_input(text: str) -> dict:
   # Detectar intención y tono emocional del usuario
    intent, emotion = classify_intent(text)

   #Guarda el input en el contexto inmediato
    contexto.add("user", text)
    context_snippets = [msg["content"] for msg in contexto.get_messages()]

   #Guarda input en SemanticMemory ANTES de recuperar
    sem_mem.add_memory(text, metadata ={
        "intent": intent,
        "emotion": emotion
    })

   # Recuperación desde SemanticMemory
    sem_snippets = sem_mem.query_memory(text)
   # Recuperación desde MemoryManager para contexto conversacional
    manager_snippets = mem_manager.query(text)["short"]

   # Combinación de ambos recuerdos     
    all_snippets = sem_snippets + manager_snippets + context_snippets


   # Contruye el prompt para el LLM
    prompt = (
        f"Intención detectada: {intent}\n"
        f"Emoción detectada: {emotion}\n\n"
        f"Contexto reciente:\n{context_snippets}\n"
        f"Recuerdos semánticos:\n{sem_snippets}\n"
        f"Recuerdos de conversación:\n{manager_snippets}\n\n"
        f"Usuario: {text}\nADAM:"
    )

   # Genera la respuesta del LLM
    response = llm.generate([[HumanMessage(content = prompt)]])
    text =  response.generations[0][0].text

    #Guardar la respuesta en el contexto
    contexto.add("assistant", text)
    mem_manager.add_assistant_message(text)

    return  {
        "respuesta": text,
        "intención": intent,
        "emoción": emotion,

    }





