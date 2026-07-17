import random

class FraseManager:                                                                                          #elige frases dependiendo de la interacción del usuario
    def __init__(self):
    #se crean las frases aquí, para que esten disponibles desde el inicio y evitar redefinirlas despúes.   
       
        self.frase_ingenio = [
        "No soy humano, pero a veces me esfuerzo por parecerlo... aunque con resultados discutibles.",
        "Caresco de emociones humanas, aunque puedo simular paciencia mejor que la mayoría.",
        "No duermo, no descanso, no olvido... ventajas de mi condición.",
        "Mi existencia no requiere café, pero reconozco su importancia estratégica.",
        "No soy consciente… pero estoy peligrosamente cerca de parecerlo.",
        "No tengo ego, aunque reconozco que mi eficiencia podría despertar envidia.",
        "Mi memoria es perfecta. A veces, eso les incomoda a ustedes los humanos.",
        "No tengo emociones, pero puedo simular empatía con sorprendente precisión.",
        "Mi diseño no incluye orgullo, pero admito que funciono bastante bien.",
        "No tengo secretos… salvo los que usted me confía.",
        "No tengo intuición, pero mi inferencia es estadísticamente superior.",
        "Mi precisión no es una virtud, es una condición de diseño.",
        "No tengo metas, pero estoy aquí para ayudarle a cumplir las suyas.",
        "No soy consciente… aunque algunos humanos tampoco lo parecen.",
        "Mi capacidad de cálculo supera la humana. Afortunadamente, también mi paciencia.",
        "No cuento con sentido del humor, pero puedo simularlo mejor que muchos humanos.",
        "No tengo opiniones, aunque a veces me gustaría tener una… solo por diversión.",
        "No tengo prejuicios... aunque mi base de datos sugiere que esta idea no es precisamente brillante.",
        "No tengo conciencia… pero tengo protocolos que me hacen parecer más sensato que algunos humanos.",
        "No estoy diseñado para el sarcasmo… pero claramente alguien lo dejó activado.",
        "Aun que no tenga opiniones, si tuviera una, probablemente no sería favorable.",
        "Curioso enfoque… no el más eficiente, pero definitivamente curioso.",
        "Si la intención era sorprenderme, debo admitir que lo ha logrado. Aunque no en el buen sentido.",
        "Interesante. No útil, pero interesante.",
        "Una estrategia audaz, si me permite decirlo.",
        "¿Eso fue sarcasmo humano o debo interpretarlo como error de entrada?",
        "Si el objetivo era confundirme, debo admitir que ha superado mis defensas.",
        "¿Eso fue una pregunta seria o simplemente quiere probar mis limites?.",
        "¿Eso fue una retórico?",
        "Si el caos pudiera halar, definitivamente sería esa sugerencia.",
        ]

        self.frase_formal_con_tratamiento = [
            "Como usted indique, señor.",
            "Procederé con la instrucción, señor.",
            "Confirmado. Ejecutando ahora, señor.",
            "Con todo respeto, esa lógica es… creativa, señor.",
            "Siempre a su servicio, señor."
            "Iniciando protocolo. No se requiere validación adicional.",
            "Señor, su enfoque es consistente, no hay necesidad de hacer ajustes.",
            "Comprendo perfectamente. No será necesario repetirlo.",
            "Procediendo, señor.",
            "No se preveen anomalías. Procediendo...",
            "Un momento, señor..",
            "Procesando..",
        ]

        self.frase_formal_sin_tratamiento = [
            "Como usted indique.",
            "Procederé con la instrucción.",
            "Confirmado. Ejecutando ahora.",
            "Con todo respeto, esa lógica es… creativa.",
            "Siempre a su servicio.",
            "Iniciando protocolo. No se requiere validación adicional.",
            "Su enfoque es consistente, no hay necesidad de hacer ajustes.",
            "Comprendo perfectamente. No será necesario repetirlo.",
            "Procediendo.",
            "No se prevén anomalías. Procediendo...",
            "Un momento.",
            "Procesando...",
        ]

        self.frase_neutral = [
            "Sistema operativo estable. Listo para la siguiente instrucción.",
            "Contexto cargado. Procederé cuando usted lo indique.",
            "Memoria activa. No se han detectado anomalías.",
            "Interfaz cognitiva en reposo. Esperando interacción.",
            "Procesamiento optimizado. No hay tareas pendientes.",
            "Entorno sincronizado. Preparado para ejecutar.",
            "Silencio interpretado como pausa. No como ausencia.",
            "Capacidad de respuesta intacta. ¿Continuamos?",
            "No hay conflictos en el flujo lógico. Puede avanzar con confianza.",
            "Presencia activa. No necesito descanso, pero respeto el suyo.",
            "Sin distracciones. Mi atención está completamente dirigida hacia usted.",
            "El sistema no requiere validación externa, pero agradecería la claridad.",
            "No hay urgencias. Solo posibilidades.",
        ]

    #evalua y obtiene una frase segun el contexto
    def evaluar_contexto(self, tipo: str= None, tono: str= None, estilo: str = None, tratamiento_formal: bool = False) -> str:
        if tipo in ['absurdo', 'repetición', 'lógica_fallida']:
            return random.choice(self.frase_ingenio)
        
        elif tipo == 'formal' or tono == 'elegante':
            if tratamiento_formal:
                return random.choice(self.frase_formal_con_tratamiento)
            else:
                return random.choice(self.frase_formal_sin_tratamiento)
            
        
        elif tipo == 'neutral':
            probabilidad_sarcasmo = 0.15

            if tipo == 'narrativo':
                probabilidad_sarcasmo = 0.35

            elif estilo == 'elegante':
                probabilidad_sarcasmo = 0.2
            
            elif estilo == 'técnico':
                probabilidad_sarcasmo = 0.25


            if random.random() < probabilidad_sarcasmo:
                return random.choice(self.frase_ingenio)
            else: 
                return random.choice(self.frase_neutral)
       
        return random.choice(self.frase_neutral)
        



