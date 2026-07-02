from modules.scanner import NetworkScanner
from modules.alerts import AlertSystem
import yaml
import time

def main():
    # Cargar configuración
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    scanner = NetworkScanner(config['network']['target'])
    alert_system = AlertSystem()

    print("🌐 Mx Networking Monitoring - Modo Consola")
    print("Presiona Ctrl+C para detener el monitoreo.\n")

    try:
        while True:
            devices = scanner.scan_network()
            print(f"\n--- Dispositivos Activos ({len(devices)}) ---")
            for device in devices:
                print(f"  - {device['hostname']} ({device['ip']})")
            
            if devices:
                alert_system.send_alert(f"Se encontraron {len(devices)} dispositivos activos en la red.")
            
            time.sleep(config['monitoring']['scan_interval'])
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")

if __name__ == "__main__":
    main()
