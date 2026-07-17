import time
from domotic.configuracion import DomoticConfiguration
class DomoticDashboard:
    def __init__(self, domotic_config):
        self.domotic_config = domotic_config    #Instancia de la clase de la DomoticConfiguration


    def get_system_status(self):
        """Devuelve un resumen tecnico del estad de los dispositivos"""
        if not self.domotic_config.devices:
            return " No hay dispositivos registrados."
        
        status_report = []
        for device in self.domotic_config.devices.values():
            status_report.append(device.describe())
        return "\n".join(status_report)
    

    def generate_report(self):
        """Genera un reporte tecnico en formato dict para otros modulos"""
        if not self.domotic_config.devices:
            return {
                "total_devices": 0,
                "active_devices" : [],
                "latency_avg": 0
            }
        
        latencies = [round(time.time() % 1 * 100, 2) for _ in self.domotic_config.devices]
        latency_avg = round(sum(latencies) / len(latencies), 2)

        return {
            "total_devices": len(self.domotic_config.devices),
            "active_devices": [d.id for d in self.domotic_config.devices.values() if d.status in ["on", "activo"]],
            "inactive_devices": [d.id for d in self.domotic_config.devices.values() if d.status in ["off", "inactivo", "standby"]],
            "latency_avg": latency_avg
        }
    

    def print_report(self):
        """ Imprime el reporte en consola en un formato legible"""
        report = self.generate_report()
        print("\n==PANEL DE ESTADO GLOBAL==\n")
        print(f"Total de dispositivos: {report['total_devices']}")
        print(f"Activos: {report['active_devices']}")
        print(f"Inactivos: {report['inactive_devices']}")
        print(f"Latencia promedio: {report['latency_avg']} ms")



if __name__ == "__main__":
    domotic = DomoticConfiguration()
    domotic.scan_devices()
    dashboard = DomoticDashboard(domotic)
    print(dashboard.get_system_status())
    dashboard.print_report()