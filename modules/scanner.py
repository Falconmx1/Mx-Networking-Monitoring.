import nmap
import socket

class NetworkScanner:
    def __init__(self, target):
        self.target = target
        self.nm = nmap.PortScanner()

    def scan_network(self):
        """Escanea la red y retorna una lista de dispositivos activos"""
        try:
            print(f"Escaneando {self.target}...")
            self.nm.scan(hosts=self.target, arguments='-sn')  # Ping scan
            devices = []
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    try:
                        hostname = socket.gethostbyaddr(host)[0]
                    except:
                        hostname = "Desconocido"
                    devices.append({
                        'ip': host,
                        'hostname': hostname,
                        'status': 'Activo'
                    })
            return devices
        except Exception as e:
            print(f"Error en el escaneo: {e}")
            return []

    def scan_ports(self, ip, ports="22,80,443"):
        """Escanea puertos específicos en una IP"""
        try:
            self.nm.scan(ip, arguments=f'-p {ports} -T4')
            open_ports = []
            if ip in self.nm:
                for proto in self.nm[ip].all_protocols():
                    ports_list = self.nm[ip][proto].keys()
                    for port in ports_list:
                        if self.nm[ip][proto][port]['state'] == 'open':
                            open_ports.append(port)
            return open_ports
        except Exception as e:
            print(f"Error escaneando puertos: {e}")
            return []
