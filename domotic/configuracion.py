import time

class Device:
    def __init__(self, id, name, type, protocol,  emotional_name = None):
        self.id = id
        self.name = name
        self.type = type
        self.protocol = protocol
        self.emotional_name = emotional_name or f"Dispositivo {name}"
        self.status = "desconocido"

    def describe(self):
        return f"{self.emotional_name} ({self.type}) conectado vía {self.protocol}. Estado: {self.status}"
    
class DomoticConfiguration:
    VALID_TYPES = ["light", "sensor", "speaker"]
    VALID_PROTOCOLS = ["MQTT", "HTTP", "HTTP", "WebSocket"]
    VALID_STATES = ["on", "off", "activo", "inactivo", "standby"]

    def __init__(self):
        self.devices = {}

    def scan_devices(self):
        print(" Escaneando dispositivos...")
        time.sleep(1)
        self.register_device("light-001", "Luz Sala", "light", "MQTT")
        self.register_device("sensor-002", "Sensor Puerta", "sensor", " HTTP")
        self.register_device("sensor-003", "Sensor Temperatura", "sensor", " HTTP")
        self.register_device("speaker-001", "Altavoz", "speaker", " HTTP")

    def register_device(self, id, name, type, protocol):
        if type not in self.VALID_TYPES:
            print(f"⚠️ Tipo desconocido: '{type}'. No me puedo vincular con este dispositivo.")
            return
        if protocol not in self.VALID_PROTOCOLS:
            print(f"⚠️ Protocolo no soportado: '{protocol}'. No puedo comunicarme con este dispositivo.")
            return
        
        emotional_name = self.generate_emotional_name(name, type)
        device = Device(id, name, type, protocol, emotional_name)
        self.devices[id] = device
        print(f"✅ Registrado: {device.describe()}")

    def remove(self, id):
        if id in self.devices:
            removed = self.devices.pop(id)
            print(f"🗑️ Dispositivo eliminado: {removed.name}")
        else:
            print(f"⚠️ Dispositivo: '{id}' no encontrado.")

    def control_device(self, id, action):
        device = self.devices.get(id)
        if not device:
            print(f"⚠️ Dispositivo '{id}' no encontrado. ¿Podrías verificar su conexión?")
            return
        if action not in self.VALID_STATES:
            print(f"⚠️ Estado inválido: '{action}'. No puedo interpretar esta acción correctamente.")
            return
        
        device.status = action
        print(f"{device.emotional_name} se encuentra en estado:  {device.status}")

    def diagnose_device(self, id):
        device = self.devices.get(id)
        if not device:
            print(f"⚠️ Dispositivo: '{id}' no encontrado.")
            return
        latency = round(time.time() % 1 * 100, 2)
        print(f" Diagnostico de {device.name}:  Estado: {device.status}. Protocolo: {device.protocol} Latencia: {latency}ms")

    def generate_emotional_name(self, name, type):
        if type == "light":
            return f"Luz cálida de {name}"
        elif type == "sensor":
            return f"Guardián silencioso de {name}"
        elif type == "speaker":
            return f"Voz ambiental de {name}"
        else:
            return f"Elemento conectado: {name}"
        
