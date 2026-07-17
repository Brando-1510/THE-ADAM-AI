import os 
import logging
from typing import List, Tuple, Dict, Optional

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

from datetime import datetime, timedelta, timezone
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

# Prametros configurables
N_CLUSTERS = 5                                                                        #Número de clusters para organizar la información
SIMILARITY_THRESHOLD = 0.85                                                           #Establece que tan preciso debe ser la similitud de elementos para que se agregue a un cluster
MAX_ITEMS_PER_TOPIC = 20                                                              #Número máximo de elementos por cluster
SUMMARY_STYLE = "narrativa"                                                           #define como se resume la información, estilo historia, texto fluido en vez de listas 
REFRESH_INTERVAL = timedelta(hours=6)                                                 #Tiempo mínimo entre actualizaciones de resumen

from config import (
    SHORT_TERM_SIZE,                                                                  # A) Cuantos doc acumular en RAM antes de flushear
    MEDIUM_STORE_PATH,                                                                # B) Carpeta en disco para el indice mediano plazo   
    LONG_STORE_PATH,                                                                  # C) Carpeta en disco para el indice largo plazo
    EMBEDDINGS_MODEL_NAME,                                                            # D) Modelo de embeddings a usar
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class SemanticMemory:
    """
    short_buffer:  Buffer en memoria RAM para guardar los últimos N fragmentos/docs, 
                usado para la fluides conversacional inmediata.

    medium_store:  Es el Indice FAISS que almacena los documentos flusheados desde Buffer, 
                para la memoria semántica contextual.

    long_store:    Es el Indice FAISS para resumenes historicos, más compacto.
                Utilizada para la memoria historica resumida.
   
    """
    def __init__(
            self,
            model_name: str = EMBEDDINGS_MODEL_NAME,
            medium_path: str = MEDIUM_STORE_PATH,
            long_path: str = LONG_STORE_PATH,
            short_size: int = SHORT_TERM_SIZE, 
            llm = None,                                                              #LLM externo para resumenes    
    ):
        self.embedding = HuggingFaceEmbeddings(model_name = model_name)              #Instancia que convierte texto en vectores semanticos
        self.short_buffer : List[Document] = []                                      #Lista vacia que retiene los docs recientes
        self.short_size = short_size                                                 #Tamaño máximo del Buffer corto 

        #Indices FAISS que se cargan o inicializan vacíos
        self.medium_store = self._load_or_init_store(medium_path)                    
        self.long_store = self._load_or_init_store(long_path) 
        #Rutas de disco para persistencia                       
        self.medium_path = medium_path
        self.long_path = long_path
        self.llm = llm 
        self.last_summary = datetime.min


    #Comprueba si el path existe, carga el indice FAISS o crea uno nuevo
    def _load_or_init_store(self, path: str) -> FAISS:
        if os.path.isdir(path):
            logger.info(f"Cargando el índice FAISS desde {path}")
            return FAISS.load_local(path, self.embedding)
        logger.info(f"Creando un nuevo índice FAISS en {path}")

    # Verifia si existe la funcion _load_documents, si existe carga los docs desde el disco, con self._load_documents(path), si no, le asigna una lista vacía
        docs = self._load_documents(path) if hasattr(self, "_load_documents") else []
     # Veifica si no hay documentos cargados, si no, crea un indice vacío, usa documentso ficticios para evitar errores al iniciar FAISS, asegurando un vector valido en el indice.
        
        if not docs:                                                                                          #comprueba si no se cargó ningún doc
            logger.info(f"No se encontraron documentos en {path},  inicializando indice vacío.")
            dummy_doc = Document(page_content = "Inicialización vacía")                                       #crea un documento ficticio para evitar errores al iniciar el indice
            return FAISS.from_documents([dummy_doc], self.embedding)                                          #crea un indice vacío con el documento ficticio
        
        return FAISS.from_documents(docs, self.embedding)                                 

    #Crea un Doc nuevo y lo añade al buffer corto, si sobrepasa el tamaño máximo, dispara el flush
    def add_memory(self, text: str, metadata:Optional[Dict] = None) -> None:
        doc = Document(page_content = text, metadata = metadata or {})
        # 1) Buffer de memoria corto plazo
        self.short_buffer.append(doc)
        logger.info(f"Buffer corto ({len(self.short_buffer)}/{self.short_size})")

        # 2) Si el Buffer se sobrepasa, se guarda en mediano plazo
        if len(self.short_buffer) >= self.short_size:
            self._flush_to_medium()

    def _flush_to_medium(self) -> None:
        logger.info(f"Flush: Moviendo buffer a mediano plazo")
        # Aqui se podrá chunkear y preprocesar cada doc
        self.medium_store.add_documents(self.short_buffer)                              #Añade en bloque los docs
        self.medium_store.save_local(self.medium_path)                                  #Mantiene el indice actualizado
        self.short_buffer.clear()

    def summarize_medium_to_long(self) -> None:
    
        now = datetime.now(timezone.utc)
        if now - self.last_summary < REFRESH_INTERVAL:
            return 
          
        # Extraemos todos los documentos del medio
        all_Docs = self.medium_store.get_all_documents()
        texts = [doc.page_content for doc in all_Docs]
        if not texts:
            return
        
        #1. Clusterizar por Tópico
        embedder = HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")
        embeddings = embedder.encode(texts, normalize_embeddings = True)
        kmeans = KMeans(n_clusters = N_CLUSTERS, random_state = 42).fit(embeddings)
        clusters = {i: [] for i in range(N_CLUSTERS)}
        for idx, label in enumerate(kmeans.labels_):
            clusters[label].append(texts[idx]) 

        #2. Filtrar redundancias 
        def dedupe(cluster):
            unique = []
            cluster_embs = embedder.encode(cluster, normalize_embeddings = True) 
            for i, text in enumerate(cluster):
                if all((cluster_embs[i] @ embedder.encode([u], normalize_embeddings=True)[0]) < SIMILARITY_THRESHOLD for u in unique):
                    unique.append(text)
            return unique[:MAX_ITEMS_PER_TOPIC ]
                
        clean_clusters = {i: dedupe(c) for i, c in clusters.items()}
        
        # Generar resumen con LLM
        prompt = PromptTemplate(
            input_variables = ["items", "style"],
            template = """ 
                Eres un asistente que genera resumenes {style}.
                Resume los siguientes puntos de forma clara y concisa: {items}
                """     
        )
        chain = LLMChain(llm= self.llm, prompt = prompt)

        for topic, items, in clean_clusters.items():
            if not items:
                continue
            text_block = "\n-" + "\n-".join(items)
            summary = chain.run(items = text_block, style = SUMMARY_STYLE)
            summary_doc = Document(
                page_content = summary,
                metadata = {
                    "type": "summary", 
                    "topic": f"cluster_{topic}",
                    "timestamp": now.isoformat(),
                    "source": "semantic_summary"
                }
            )
            self.long_store.add_documents([summary_doc])
            logger.info(f"Resumen generado para tópico {topic}")
        
        self.long_store.save_local(self.long_path)
        self.medium_store = FAISS.from_documents([], self.embedding)
        self.medium_store.save_local(self.medium_path)
        self.last_summary = now 
        logger.info("Resumenes guardados y memoria mediana limpiada")

    def get_langchain_memory(self):
        """ 
        Expone la memoria semántica como un valor compatible para langchain.
        Utiliza el índice de memoria a largo plazo como fuente principal.
        """
        retriever = self.long_store.as_retriever(search_kwargs={"k": 5})
        memory = VectorStoreRetrieverMemory(retriever = retriever)
        memory.memory_key = "semantic_context"
        return  memory

    def query_memory(self, query: str, k = 5) -> List[Tuple[Document, float]]:
        
        # Embeddings de consulta
        q_emb = self.embedding.embed_query(query)

        # 1) Buscamos en mediano plazo
        med_res = self.medium_store.similarity_search_with_score(query, k=k)  

        # 2) Buscamos en largo plazo
        long_res = self.long_store.similarity_search_with_score(query, k=k)

        # 3) Combinamos los resultados y ordenarlos por score
        combined = sorted(med_res + long_res, key=lambda x: -x[1])

        # 4) Añadimos matches del buffer corto plazo (búsqueda simple por substring)
        short_matches = [
            (doc, 1.0) for doc in self.short_buffer if query.lower() in doc.page_content.lower()
        ] 

        # Retornamos los top-k despues de eliminar duplicados 
        seen = set() 
        final = []
        for doc, score in short_matches + combined:
            if doc.page_content not in seen and len(final) < k:
                seen.add(doc.page_content)
                final.append((doc, score))
        return final
        

