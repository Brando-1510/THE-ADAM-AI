
def device_action(text: str, ) -> str:
    if "enciende" in text:
        dispositivo = text.split("enciende")[-1].strip()
        return f"He encendido {dispositivo}, Señor"
    
    elif "apaga" in text:
        dispositivo = text.split("apaga")[-1].strip()
        return f"He encendido {dispositivo}, Señor"
    else:
        return "No entendiendo que se refiere"