from domotic.configuracion import DomoticConfiguration

def test_domotic_module():
    print("🧠 Iniciando test del módulo domótico de ADAM...\n")

    adam_domotics = DomoticConfiguration()

    # Escaneo simulado
    adam_domotics.scan_devices()

    # Control de dispositivos
    adam_domotics.control_device("light-001", "on")
    adam_domotics.control_device("sensor-002", "active")
    adam_domotics.control_device("sensor-003", "inactive")
    adam_domotics.control_device("sensor-003", "standby")
    adam_domotics.control_device("speaker-001", "off")

    # Verificación narrativa
    print("\n📋 Estado actual de los dispositivos:")
    for device in adam_domotics.devices.values():
        print(f" - {device.describe()}")

if __name__ == "__main__":
    test_domotic_module()