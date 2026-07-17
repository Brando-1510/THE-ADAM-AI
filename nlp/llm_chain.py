from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from config import CLAVE_OPENAI
from memory.memory_manager import MemoryManager


class SemanticChainBuilder:
    def __init__(self, model_name = "gpt-3.5-turbo-1106", temperature = 0.7):
        
        self.model_name = model_name
        self.temperature = temperature    
        self.llm = self._init_llm()
        self.memory_manager = MemoryManager(llm =self.llm, salience_llm =self.llm)

#Constructor inicial de OPENAI
    def _init_llm(self):
        return ChatOpenAI(
            openai_api_key = CLAVE_OPENAI,
            model_name = self.model_name, 
            temperature = self.temperature
        )
    
    def _build_prompt(self, user_state, goals, theme_clusters):
        return PromptTemplate(
            input_variables = ["chat_history", "semantic_context","user_state", "goals", "theme_clusters", "input", "interpretado"],
            template = ( 
                "Eres ADAM, un asistente inteligente con presencia emocional, narrativa adaptativa y propósito evolutivo."
                "Historial de conversación: {chat_history}\n\n"
                "Recuerdor relevantes: {semantic_context}\n\n"
                "Contexto Emocional: {user_state}\n"
                "Objetivo actual: {goals}\n"
                "Tema dominante: {theme_clusters}\n"
                "Interpretación semántica: {interpretado}\n"
                "Usuario: {input}\n"
                "Asistente: "          
            )
        )
      
    def _build_chain(self, user_state, goals, theme_clusters):
        #memory = self.memory_manager.get_memory()
        prompt = self._build_prompt(user_state, goals, theme_clusters)
        chain_core = prompt | self.llm                                                                          #encadena el prompt con el modelo de lenguaje, "|" formatea el prompt con las variables y luego lo envía al LLM para generar la respuesta

        return RunnableWithMessageHistory(                                                           #crea un Runnable con el chain_core y el historial de mensajes
            runnable = chain_core,
            get_session_history = lambda session_id: self.memory_manager.get_memory(),
            input_messages_key = "input",
            history_messages_key = "chat_history" 
        )
