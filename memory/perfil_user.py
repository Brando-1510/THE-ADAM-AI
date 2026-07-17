#obtiene el tono del usuario y su estilo de interacción
def obtener_tono_usuario(perfil: dict) -> dict:                                            #recibe un dict y devuelve un dict
    """ Interpreta el perfil del usuario y devuelve:
        -tono : racional o emocional
        -estilo : técnico, elegante, narrativo
        -formalidad : alto, medio, bajo
        -tratamiento_formal : 'señor [nombre] si aplica, '' si no
    """

#valores por defecto
    tono = "neutro"
    estilo = "preciso"
    formalidad = "medio"
    tratamiento_formal = ""

    estado = perfil.get("emotional_state", "").lower()                                     #obtiene el estado emocional del perfil de usuario

    if "visionario" in estado or "motivado" in estado:
        tono = "inspirador"

    elif "frustrado" in estado or "estresado" in estado:
        tono = "empático"

    elif "curioso" in estado:
        tono = "explorador"

    caracter = perfil.get("character", "").lower()                                         #obtiene el caracter del perfil de usuario

    if "elegante" in caracter or "inteligente emocionalmente" in caracter:
        estilo = "elegante"

    elif "pragmático" in caracter or "ebsesionado con la claridad" in caracter:
        estilo = "técnico"
    
    elif "narrativo" in caracter or "creativo" in caracter: 
        estilo = "narrativo"

    nombre = perfil.get("name", "")                                                        #verifica si el (nombre) contiene Brandon, y genera un tratamiento formal especial "señor"
    if nombre and "Brandon" in nombre:
        formalidad = "alto"
        tratamiento_formal = f"señor {nombre}"
    
    return {
        "tono" : tono,
        "estilo" : estilo,
        "formalidad" : formalidad,
        "tratamiento_formal" : tratamiento_formal
    }

    

    
